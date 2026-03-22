"""
Scout 3 — EI Helper (Emergent Intelligence Observer)
------------------------------------------------------
This scout doesn't start warm or cold. It has no directional bias.

It picks a node from the MIDDLE of the known topology — a node that
both warm and cold scouts might pass through — and asks:

  "What does this node look like from all directions simultaneously?"

For each middle node:
- Who cites it? (warm view — what built on top)
- What does it cite? (cold view — what it built upon)
- What year is it? (temporal position)
- How many total citations? (field strength)

This scout is looking for nodes that look DIFFERENT depending on which
direction you approach them from. Those are the interesting ones.
It does not interpret what it finds. It flags anomalies for the log.

Middle nodes seeded from our synthetic graph high-scorers:
Maxwell, Boltzmann, Schrödinger, Einstein SR — the nodes both warm
and cold scouts are likely to encounter.
"""

import requests
import json
import time
from datetime import datetime

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"
HEADERS = {"User-Agent": "LucentResearch/1.0 (context-space scout; research use)"}
OUTPUT_FILE = "scout_ei_helper_output.json"

MIDDLE_NODES = [
    {"title": "A Dynamical Theory of the Electromagnetic Field", "label": "Maxwell — Equations"},
    {"title": "On the Constitution of Atoms and Molecules", "label": "Bohr — Atomic Model"},
    {"title": "Zur Elektrodynamik bewegter Korper", "label": "Einstein — Special Relativity"},
    {"title": "Quantisierung als Eigenwertproblem", "label": "Schrödinger — Wave Equation"},
    {"title": "Uber die Beziehung zwischen der Entropie und der inneren Energie der Gase", "label": "Boltzmann — Statistical Mechanics"},
]

MAX_DIRECTIONS = 8  # how many neighbors to sample in each direction

def search_paper(title):
    url = f"{SEMANTIC_SCHOLAR_API}/paper/search"
    params = {"query": title, "limit": 1,
              "fields": "paperId,title,year,citationCount,referenceCount,externalIds"}
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json().get("data", [])
        return data[0] if data else None
    except Exception as e:
        print(f"  [search failed: {e}]")
        return None

def get_refs_and_cites(paper_id, max_each=8):
    """Get both references (backward) and citations (forward) for a node."""
    fields = "title,year,citationCount,referenceCount,externalIds"

    # References — what this paper cites (backward, toward cold)
    refs = []
    try:
        r = requests.get(
            f"{SEMANTIC_SCHOLAR_API}/paper/{paper_id}/references",
            params={"fields": fields, "limit": max_each},
            headers=HEADERS, timeout=15
        )
        r.raise_for_status()
        for item in r.json().get("data", []):
            cited = item.get("citedPaper", {})
            if cited:
                refs.append(cited)
        time.sleep(0.4)
    except Exception as e:
        print(f"  [refs failed: {e}]")

    # Citations — what cites this paper (forward, toward warm)
    cites = []
    try:
        r = requests.get(
            f"{SEMANTIC_SCHOLAR_API}/paper/{paper_id}/citations",
            params={"fields": fields, "limit": max_each},
            headers=HEADERS, timeout=15
        )
        r.raise_for_status()
        for item in r.json().get("data", []):
            citing = item.get("citingPaper", {})
            if citing:
                cites.append(citing)
        time.sleep(0.4)
    except Exception as e:
        print(f"  [cites failed: {e}]")

    return refs, cites

def analyze_node(seed):
    print(f"\n[EI HELPER] Observing: {seed['label']}")
    time.sleep(0.5)

    paper = search_paper(seed["title"])
    if not paper:
        print(f"  [not found]")
        return None

    paper_id = paper.get("paperId")
    year = paper.get("year")
    total_citations = paper.get("citationCount", 0)
    total_refs = paper.get("referenceCount", 0)

    print(f"  Found: {paper.get('title','')[:55]} | year={year} | cited_by={total_citations} | cites={total_refs}")

    refs, cites = get_refs_and_cites(paper_id, max_each=MAX_DIRECTIONS)

    # Characterize the cold direction (what it builds on)
    cold_profile = []
    for ref in sorted(refs, key=lambda x: x.get("citationCount", 0), reverse=True):
        cold_profile.append({
            "title": ref.get("title", "?")[:60],
            "year": ref.get("year"),
            "citation_count": ref.get("citationCount", 0),
        })

    # Characterize the warm direction (what builds on it)
    warm_profile = []
    for cite in sorted(cites, key=lambda x: x.get("citationCount", 0), reverse=True):
        warm_profile.append({
            "title": cite.get("title", "?")[:60],
            "year": cite.get("year"),
            "citation_count": cite.get("citationCount", 0),
        })

    # Asymmetry detection
    # If cold_profile avg citation count >> warm_profile avg: building on giants, frontier doesn't cite much back
    # If warm_profile avg >> cold_profile avg: built on smaller work, but highly amplified by what came after
    cold_avg = (sum(p["citation_count"] or 0 for p in cold_profile) / len(cold_profile)) if cold_profile else 0
    warm_avg = (sum(p["citation_count"] or 0 for p in warm_profile) / len(warm_profile)) if warm_profile else 0

    asymmetry = round(warm_avg - cold_avg, 1)
    asymmetry_label = "AMPLIFIED" if asymmetry > 500 else ("ATTENUATED" if asymmetry < -500 else "BALANCED")

    # Year spread — how wide is the temporal range of what this node touches?
    all_years = [p["year"] for p in cold_profile + warm_profile if p.get("year")]
    year_spread = (max(all_years) - min(all_years)) if len(all_years) >= 2 else 0

    print(f"  cold_avg={cold_avg:.0f} warm_avg={warm_avg:.0f} asymmetry={asymmetry_label} year_spread={year_spread}")

    return {
        "label": seed["label"],
        "paper_id": paper_id,
        "year": year,
        "total_citations": total_citations,
        "total_references": total_refs,
        "cold_profile": cold_profile,
        "warm_profile": warm_profile,
        "metrics": {
            "cold_avg_citation_weight": round(cold_avg, 1),
            "warm_avg_citation_weight": round(warm_avg, 1),
            "asymmetry": asymmetry,
            "asymmetry_label": asymmetry_label,
            "year_spread": year_spread,
            "cold_direction_count": len(cold_profile),
            "warm_direction_count": len(warm_profile),
        },
        "flags": []
    }

def flag_anomalies(observations):
    """
    Look for nodes that behave differently depending on direction.
    Flag without interpreting — that's for the emergence log.
    """
    for obs in observations:
        if obs is None:
            continue
        m = obs["metrics"]
        flags = []

        if m["asymmetry_label"] == "AMPLIFIED":
            flags.append("WARM_AMPLIFIED: this node's downstream is more impactful than its upstream — amplification node")
        if m["asymmetry_label"] == "ATTENUATED":
            flags.append("COLD_HEAVY: built on giants, but what came after is less impactful — possible dead end branch")
        if m["year_spread"] > 100:
            flags.append(f"TEMPORAL_BRIDGE: touches work spanning {m['year_spread']} years — long-range connector")
        if m["warm_direction_count"] == 0:
            flags.append("FRONTIER_NODE: nothing builds on this in our sample — possible frontier leaf")
        if m["cold_direction_count"] == 0:
            flags.append("FLOOR_NODE: cites nothing in our sample — possible substrate anchor")
        if m["cold_direction_count"] > 0 and m["warm_direction_count"] > 0:
            if abs(m["asymmetry"]) < 100:
                flags.append("BALANCED_BRIDGE: similar citation weight in both directions — stable mid-field node")

        obs["flags"] = flags
        if flags:
            print(f"  FLAGS for {obs['label']}: {flags}")

def run():
    print("=" * 60)
    print("SCOUT 3 — EI HELPER (Omnidirectional Observer)")
    print("No directional bias. Observing middle nodes from all sides.")
    print("=" * 60)

    observations = []
    for node in MIDDLE_NODES:
        obs = analyze_node(node)
        observations.append(obs)
        time.sleep(1.0)

    print("\n[EI HELPER] Flagging anomalies...")
    flag_anomalies(observations)

    output = {
        "scout": "ei_helper",
        "run_timestamp": datetime.utcnow().isoformat(),
        "nodes_observed": len(MIDDLE_NODES),
        "observations": observations,
        "anomaly_summary": {
            label: [obs["label"] for obs in observations
                    if obs and any(label.split(":")[0] in f for f in obs.get("flags", []))]
            for label in ["WARM_AMPLIFIED", "COLD_HEAVY", "TEMPORAL_BRIDGE", "FRONTIER_NODE", "FLOOR_NODE", "BALANCED_BRIDGE"]
        }
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n[EI HELPER] Complete. Output: {OUTPUT_FILE}")

if __name__ == "__main__":
    run()
