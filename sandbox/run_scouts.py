"""
Run all three scouts sequentially with proper rate limiting.
Outputs one JSON file per scout. No synthesis — raw observation only.
"""

import time
import json
from datetime import datetime, timezone
from scout_utils import (
    search_paper, get_references, get_citations,
    zone_label, COLD_SEED_IDS, WARM_SEED_QUERIES,
    SEMANTIC_SCHOLAR_API, api_get
)

PAUSE_BETWEEN_SCOUTS = 20.0  # seconds between scouts
PAUSE_BETWEEN_CALLS  = 5.0  # seconds between individual API calls

# ─────────────────────────────────────────────────────────────────────────────
# SCOUT 1 — WARM TO COLD
# Start at active frontier, trace backward through references toward foundation
# ─────────────────────────────────────────────────────────────────────────────

def run_warm_to_cold():
    print("\n" + "="*60)
    print("SCOUT 1 — WARM TO COLD")
    print("Frontier → Foundation")
    print("="*60)

    chains = []

    for seed_query in WARM_SEED_QUERIES:
        print(f"\n[W→C] Seeding: {seed_query['label']}")
        time.sleep(PAUSE_BETWEEN_CALLS)

        paper = search_paper(seed_query["query"])
        if not paper or not paper.get("paperId"):
            print(f"  [seed not found]")
            continue

        paper_id = paper["paperId"]
        chain = [{
            "title": paper.get("title", "")[:70],
            "paper_id": paper_id,
            "year": paper.get("year"),
            "citation_count": paper.get("citationCount", 0),
            "depth": 0,
            "zone": zone_label(paper.get("citationCount", 0), paper.get("year")),
            "seed_label": seed_query["label"]
        }]
        print(f"  Found: {chain[0]['title'][:55]} | year={chain[0]['year']} | cites={chain[0]['citation_count']} | zone={chain[0]['zone']}")

        current_id = paper_id
        for depth in range(1, 5):
            time.sleep(PAUSE_BETWEEN_CALLS)
            refs = get_references(current_id, limit=8)
            if not refs:
                print(f"  depth {depth}: no references — stopping")
                break

            # Follow most-cited reference — the heaviest upstream node
            refs_sorted = sorted(refs, key=lambda x: x.get("citationCount") or 0, reverse=True)
            best = refs_sorted[0]
            if not best.get("paperId"):
                print(f"  depth {depth}: ref has no paper ID — stopping")
                break

            z = zone_label(best.get("citationCount", 0), best.get("year"))
            node = {
                "title": (best.get("title") or "")[:70],
                "paper_id": best.get("paperId"),
                "year": best.get("year"),
                "citation_count": best.get("citationCount", 0),
                "depth": depth,
                "zone": z,
                "siblings": [(r.get("title") or "")[:40] for r in refs_sorted[1:3]]
            }
            chain.append(node)
            print(f"  depth {depth}: [{z}] {node['title'][:55]} ({node['year']}) cites={node['citation_count']}")
            current_id = best["paperId"]

            if z == "cold":
                print(f"  reached cold zone — stopping")
                break

        chains.append({
            "seed": seed_query["label"],
            "chain": chain,
            "length": len(chain),
            "zones_traversed": list(dict.fromkeys(n["zone"] for n in chain)),
            "reached_cold": any(n["zone"] == "cold" for n in chain)
        })

    output = {
        "scout": "warm_to_cold",
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "chains": chains,
        "summary": {
            "seeds_attempted": len(WARM_SEED_QUERIES),
            "chains_collected": len(chains),
            "chains_reaching_cold": sum(1 for c in chains if c["reached_cold"]),
            "avg_length": round(sum(c["length"] for c in chains) / len(chains), 2) if chains else 0
        }
    }
    with open("scout_warm_cold_output.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[W→C] Done. {output['summary']}")
    return output


# ─────────────────────────────────────────────────────────────────────────────
# SCOUT 1B — WARM TO COLD (from known paper IDs)
# Same traversal as Scout 1 but seeds come from prior scout output, not search.
# Use when feeding frontier outputs of Scout 2 back into Scout 1.
# ─────────────────────────────────────────────────────────────────────────────

def run_warm_to_cold_from_ids(seed_papers, output_file="scout_warm_cold_loop_output.json"):
    """
    seed_papers: list of {"label": str, "paper_id": str}
    Traces warm→cold from each, no search step.
    """
    print("\n" + "="*60)
    print("SCOUT 1B — WARM TO COLD (loop feed from Scout 2 frontier)")
    print("No search — seeding directly from prior scout output")
    print("="*60)

    chains = []

    for seed_info in seed_papers:
        print(f"\n[W→C loop] Seeding: {seed_info['label']}")
        time.sleep(PAUSE_BETWEEN_CALLS)

        data = api_get(
            f"{SEMANTIC_SCHOLAR_API}/paper/{seed_info['paper_id']}",
            params={"fields": "paperId,title,year,citationCount,referenceCount"}
        )
        if not data or not data.get("paperId"):
            print(f"  [paper not found: {seed_info['paper_id']}]")
            continue

        paper_id = data["paperId"]
        z = zone_label(data.get("citationCount", 0), data.get("year"))
        chain = [{
            "title": (data.get("title") or "")[:70],
            "paper_id": paper_id,
            "year": data.get("year"),
            "citation_count": data.get("citationCount", 0),
            "depth": 0,
            "zone": z,
            "seed_label": seed_info["label"]
        }]
        print(f"  Found: {chain[0]['title'][:55]} | year={chain[0]['year']} | cites={chain[0]['citation_count']} | zone={z}")

        current_id = paper_id
        for depth in range(1, 6):
            time.sleep(PAUSE_BETWEEN_CALLS)
            refs = get_references(current_id, limit=8)
            if not refs:
                print(f"  depth {depth}: no references — stopping")
                break

            refs_sorted = sorted(refs, key=lambda x: x.get("citationCount") or 0, reverse=True)
            best = refs_sorted[0]
            if not best.get("paperId"):
                print(f"  depth {depth}: ref has no paper ID — stopping")
                break

            z = zone_label(best.get("citationCount", 0), best.get("year"))
            node = {
                "title": (best.get("title") or "")[:70],
                "paper_id": best.get("paperId"),
                "year": best.get("year"),
                "citation_count": best.get("citationCount", 0),
                "depth": depth,
                "zone": z,
                "siblings": [(r.get("title") or "")[:40] for r in refs_sorted[1:3]]
            }
            chain.append(node)
            print(f"  depth {depth}: [{z}] {node['title'][:55]} ({node['year']}) cites={node['citation_count']}")
            current_id = best["paperId"]

            if z == "cold":
                print(f"  reached cold zone — stopping")
                break

        chains.append({
            "seed": seed_info["label"],
            "chain": chain,
            "length": len(chain),
            "zones_traversed": list(dict.fromkeys(n["zone"] for n in chain)),
            "reached_cold": any(n["zone"] == "cold" for n in chain)
        })

    output = {
        "scout": "warm_to_cold_loop",
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "chains": chains,
        "summary": {
            "seeds_attempted": len(seed_papers),
            "chains_collected": len(chains),
            "chains_reaching_cold": sum(1 for c in chains if c["reached_cold"]),
            "avg_length": round(sum(c["length"] for c in chains) / len(chains), 2) if chains else 0
        }
    }
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[W→C loop] Done. {output['summary']}")
    return output


# ─────────────────────────────────────────────────────────────────────────────
# SCOUT 2 — COLD TO WARM
# Start at foundational works, trace forward through citations toward frontier
# ─────────────────────────────────────────────────────────────────────────────

def run_cold_to_warm():
    print("\n" + "="*60)
    print("SCOUT 2 — COLD TO WARM")
    print("Foundation → Frontier")
    print("="*60)

    chains = []

    for seed_info in COLD_SEED_IDS:
        print(f"\n[C→W] Seeding: {seed_info['label']}")
        time.sleep(PAUSE_BETWEEN_CALLS)

        # Use paper_id directly — title search unreliable for pre-1950 works
        raw_id = seed_info["paper_id"]
        data = api_get(
            f"{SEMANTIC_SCHOLAR_API}/paper/{raw_id}",
            params={"fields": "paperId,title,year,citationCount,referenceCount"}
        )
        if not data or not data.get("paperId"):
            # Fallback: try label as search query
            print(f"  [direct ID failed, trying search...]")
            time.sleep(PAUSE_BETWEEN_CALLS)
            data = search_paper(seed_info["label"])
        if not data or not data.get("paperId"):
            print(f"  [seed not found]")
            continue

        paper = data
        year = paper.get("year") or 0
        paper_id = paper["paperId"]
        z = zone_label(paper.get("citationCount", 0), year)
        chain = [{
            "title": (paper.get("title") or "")[:70],
            "paper_id": paper_id,
            "year": year,
            "citation_count": paper.get("citationCount", 0),
            "depth": 0,
            "zone": z,
            "seed_label": seed_info["label"]
        }]
        print(f"  Found: {chain[0]['title'][:55]} | year={year} | cited_by={chain[0]['citation_count']} | zone={z}")

        current_id = paper_id
        for depth in range(1, 6):
            time.sleep(PAUSE_BETWEEN_CALLS)
            cites = get_citations(current_id, limit=8)
            if not cites:
                print(f"  depth {depth}: no citations — frontier reached")
                break

            # Follow most-cited citing paper — dominant downstream path
            cites_sorted = sorted(cites, key=lambda x: x.get("citationCount") or 0, reverse=True)
            best = cites_sorted[0]
            if not best.get("paperId"):
                break

            z = zone_label(best.get("citationCount", 0), best.get("year"))
            node = {
                "title": (best.get("title") or "")[:70],
                "paper_id": best.get("paperId"),
                "year": best.get("year"),
                "citation_count": best.get("citationCount", 0),
                "depth": depth,
                "zone": z,
                "siblings": [(r.get("title") or "")[:40] for r in cites_sorted[1:3]]
            }
            chain.append(node)
            print(f"  depth {depth}: [{z}] {node['title'][:55]} ({node['year']}) cited_by={node['citation_count']}")
            current_id = best["paperId"]

            if z == "frontier":
                print(f"  reached frontier — stopping")
                break

        chains.append({
            "seed": seed_info["label"],
            "chain": chain,
            "length": len(chain),
            "zones_traversed": list(dict.fromkeys(n["zone"] for n in chain)),
            "reached_warm": any(n["zone"] in ("warm", "frontier") for n in chain[1:])
        })

    output = {
        "scout": "cold_to_warm",
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "chains": chains,
        "summary": {
            "seeds_attempted": len(COLD_SEED_IDS),
            "chains_collected": len(chains),
            "chains_reaching_warm": sum(1 for c in chains if c["reached_warm"]),
            "avg_length": round(sum(c["length"] for c in chains) / len(chains), 2) if chains else 0
        }
    }
    with open("scout_cold_warm_output.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[C→W] Done. {output['summary']}")
    return output


# ─────────────────────────────────────────────────────────────────────────────
# SCOUT 3 — EI HELPER (Omnidirectional)
# No directional bias. Observes target nodes from both sides simultaneously.
# Flags asymmetries — does not interpret them.
# ─────────────────────────────────────────────────────────────────────────────

EI_TARGET_QUERIES = [
    {"label": "Maxwell — Equations",           "query": "dynamical theory electromagnetic field Maxwell"},
    {"label": "Boltzmann — Statistical Mech",  "query": "further studies thermal equilibrium gas molecules Boltzmann"},
    {"label": "Einstein — Special Relativity", "query": "Zur Elektrodynamik bewegter Korper Einstein 1905"},
    {"label": "Schrodinger — Wave Mechanics",  "query": "Quantisierung als Eigenwertproblem Schrodinger wave mechanics"},
    {"label": "Shannon — Information Theory",  "query": "mathematical theory of communication Shannon 1948"},
]

def run_ei_helper():
    print("\n" + "="*60)
    print("SCOUT 3 — EI HELPER")
    print("Omnidirectional observer. No directional bias.")
    print("="*60)

    observations = []

    for target in EI_TARGET_QUERIES:
        print(f"\n[EI] Observing: {target['label']}")
        time.sleep(PAUSE_BETWEEN_CALLS)

        paper = search_paper(target["query"])
        if not paper or not paper.get("paperId"):
            print(f"  [not found]")
            observations.append({"label": target["label"], "found": False})
            continue

        paper_id = paper["paperId"]
        year = paper.get("year")
        total_cites = paper.get("citationCount", 0)
        total_refs = paper.get("referenceCount", 0)
        print(f"  Found: {(paper.get('title') or '')[:55]} | year={year} | cited_by={total_cites} | cites={total_refs}")

        time.sleep(PAUSE_BETWEEN_CALLS)
        backward = get_references(paper_id, limit=8)   # cold direction
        time.sleep(PAUSE_BETWEEN_CALLS)
        forward  = get_citations(paper_id,  limit=8)   # warm direction

        cold_profile = sorted(
            [{"title": (p.get("title") or "")[:60], "year": p.get("year"), "citation_count": p.get("citationCount", 0)} for p in backward],
            key=lambda x: x["citation_count"], reverse=True
        )
        warm_profile = sorted(
            [{"title": (p.get("title") or "")[:60], "year": p.get("year"), "citation_count": p.get("citationCount", 0)} for p in forward],
            key=lambda x: x["citation_count"], reverse=True
        )

        cold_avg = sum(p["citation_count"] or 0 for p in cold_profile) / len(cold_profile) if cold_profile else 0
        warm_avg = sum(p["citation_count"] or 0 for p in warm_profile) / len(warm_profile) if warm_profile else 0
        asymmetry = warm_avg - cold_avg
        asymmetry_label = "AMPLIFIED" if asymmetry > 500 else ("ATTENUATED" if asymmetry < -500 else "BALANCED")

        all_years = [p["year"] for p in cold_profile + warm_profile if p.get("year")]
        year_spread = (max(all_years) - min(all_years)) if len(all_years) >= 2 else 0

        flags = []
        if asymmetry_label == "AMPLIFIED":
            flags.append("WARM_AMPLIFIED: downstream more impactful than upstream")
        if asymmetry_label == "ATTENUATED":
            flags.append("COLD_HEAVY: upstream more impactful than downstream")
        if year_spread > 80:
            flags.append(f"TEMPORAL_BRIDGE: touches {year_spread} years of work")
        if not warm_profile:
            flags.append("FRONTIER_LEAF: nothing cites this in our sample")
        if not cold_profile:
            flags.append("FLOOR_ANCHOR: cites nothing in our sample")
        if cold_profile and warm_profile and abs(asymmetry) < 200:
            flags.append("BALANCED_BRIDGE: similar weight in both directions")

        print(f"  cold_avg={cold_avg:.0f} warm_avg={warm_avg:.0f} {asymmetry_label} spread={year_spread}yr flags={flags}")

        observations.append({
            "label": target["label"],
            "found": True,
            "paper_id": paper_id,
            "year": year,
            "total_citations": total_cites,
            "total_references": total_refs,
            "cold_profile": cold_profile[:5],
            "warm_profile": warm_profile[:5],
            "metrics": {
                "cold_avg": round(cold_avg, 1),
                "warm_avg": round(warm_avg, 1),
                "asymmetry": round(asymmetry, 1),
                "asymmetry_label": asymmetry_label,
                "year_spread": year_spread,
                "cold_count": len(cold_profile),
                "warm_count": len(warm_profile),
            },
            "flags": flags
        })

    output = {
        "scout": "ei_helper",
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "observations": observations,
        "anomaly_summary": {
            "found": [o["label"] for o in observations if o.get("found")],
            "not_found": [o["label"] for o in observations if not o.get("found")],
            "flagged": {o["label"]: o["flags"] for o in observations if o.get("flags")}
        }
    }
    with open("scout_ei_helper_output.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[EI] Done. Output: scout_ei_helper_output.json")
    return output


# ─────────────────────────────────────────────────────────────────────────────
# SCOUT 3B — EI HELPER (from known paper ID)
# Same as Scout 3 but takes a paper ID directly — no search step.
# Use when feeding discovered nodes (not pre-selected targets) into the observer.
# ─────────────────────────────────────────────────────────────────────────────

def run_ei_helper_from_id(targets, output_file="scout_ei_helper_loop_output.json"):
    """
    targets: list of {"label": str, "paper_id": str}
    Observes each from both directions simultaneously. No directional bias.
    """
    print("\n" + "="*60)
    print("SCOUT 3B — EI HELPER (from paper IDs)")
    print("Omnidirectional observer. No directional bias.")
    print("="*60)

    observations = []

    for target in targets:
        print(f"\n[EI] Observing: {target['label']}")
        time.sleep(PAUSE_BETWEEN_CALLS)

        data = api_get(
            f"{SEMANTIC_SCHOLAR_API}/paper/{target['paper_id']}",
            params={"fields": "paperId,title,year,citationCount,referenceCount"}
        )
        if not data or not data.get("paperId"):
            print(f"  [not found]")
            observations.append({"label": target["label"], "found": False})
            continue

        paper_id = data["paperId"]
        year = data.get("year")
        total_cites = data.get("citationCount", 0)
        total_refs = data.get("referenceCount", 0)
        print(f"  Found: {(data.get('title') or '')[:55]} | year={year} | cited_by={total_cites} | refs={total_refs}")

        time.sleep(PAUSE_BETWEEN_CALLS)
        backward = get_references(paper_id, limit=10)
        time.sleep(PAUSE_BETWEEN_CALLS)
        forward  = get_citations(paper_id,  limit=10)

        cold_profile = sorted(
            [{"title": (p.get("title") or "")[:65], "year": p.get("year"), "citation_count": p.get("citationCount", 0)} for p in backward],
            key=lambda x: x["citation_count"], reverse=True
        )
        warm_profile = sorted(
            [{"title": (p.get("title") or "")[:65], "year": p.get("year"), "citation_count": p.get("citationCount", 0)} for p in forward],
            key=lambda x: x["citation_count"], reverse=True
        )

        cold_avg = sum(p["citation_count"] or 0 for p in cold_profile) / len(cold_profile) if cold_profile else 0
        warm_avg = sum(p["citation_count"] or 0 for p in warm_profile) / len(warm_profile) if warm_profile else 0
        asymmetry = warm_avg - cold_avg
        asymmetry_label = "AMPLIFIED" if asymmetry > 500 else ("ATTENUATED" if asymmetry < -500 else "BALANCED")

        all_years = [p["year"] for p in cold_profile + warm_profile if p.get("year")]
        year_spread = (max(all_years) - min(all_years)) if len(all_years) >= 2 else 0

        flags = []
        if asymmetry_label == "AMPLIFIED":   flags.append("WARM_AMPLIFIED: downstream more impactful than upstream")
        if asymmetry_label == "ATTENUATED":  flags.append("COLD_HEAVY: upstream more impactful than downstream")
        if year_spread > 80:                 flags.append(f"TEMPORAL_BRIDGE: touches {year_spread} years of work")
        if not warm_profile:                 flags.append("FRONTIER_LEAF: nothing cites this in sample")
        if not cold_profile:                 flags.append("LAG_OR_FLOOR: no references indexed — lag state or terminal floor")
        if cold_profile and warm_profile and abs(asymmetry) < 200:
            flags.append("BALANCED_BRIDGE: similar weight both directions")

        print(f"  cold_avg={cold_avg:.0f} warm_avg={warm_avg:.0f} {asymmetry_label} spread={year_spread}yr")
        print(f"  flags: {flags}")
        if cold_profile:
            print(f"  cold profile (top 3):")
            for p in cold_profile[:3]:
                print(f"    [{p['citation_count']}] ({p['year']}) {p['title'][:55]}")
        if warm_profile:
            print(f"  warm profile (top 3):")
            for p in warm_profile[:3]:
                print(f"    [{p['citation_count']}] ({p['year']}) {p['title'][:55]}")

        observations.append({
            "label": target["label"],
            "found": True,
            "paper_id": paper_id,
            "year": year,
            "total_citations": total_cites,
            "total_references": total_refs,
            "cold_profile": cold_profile[:6],
            "warm_profile": warm_profile[:6],
            "metrics": {
                "cold_avg": round(cold_avg, 1),
                "warm_avg": round(warm_avg, 1),
                "asymmetry": round(asymmetry, 1),
                "asymmetry_label": asymmetry_label,
                "year_spread": year_spread,
                "cold_count": len(cold_profile),
                "warm_count": len(warm_profile),
            },
            "flags": flags
        })

    output = {
        "scout": "ei_helper_from_id",
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "observations": observations,
        "anomaly_summary": {
            "found": [o["label"] for o in observations if o.get("found")],
            "not_found": [o["label"] for o in observations if not o.get("found")],
            "flagged": {o["label"]: o["flags"] for o in observations if o.get("flags")}
        }
    }
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[EI] Done. Output: {output_file}")
    return output


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("RUNNING ALL THREE SCOUTS")
    print("Independent runs. No synthesis until all three complete.")
    print("Pausing between scouts to respect rate limits.\n")

    w2c = run_warm_to_cold()
    print(f"\n[pause {PAUSE_BETWEEN_SCOUTS}s before next scout]")
    time.sleep(PAUSE_BETWEEN_SCOUTS)

    c2w = run_cold_to_warm()
    print(f"\n[pause {PAUSE_BETWEEN_SCOUTS}s before next scout]")
    time.sleep(PAUSE_BETWEEN_SCOUTS)

    ei  = run_ei_helper()

    print("\n" + "="*60)
    print("ALL THREE SCOUTS COMPLETE")
    print("Output files:")
    print("  scout_warm_cold_output.json")
    print("  scout_cold_warm_output.json")
    print("  scout_ei_helper_output.json")
    print("Read the outputs before drawing any conclusions.")
    print("="*60)
