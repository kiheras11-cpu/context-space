"""
C2 Velocity — All Discovered Cold Nodes
-----------------------------------------
Runs the velocity approximation on every cold node discovered
through traversal today. No pre-selected list — only nodes the
topology surfaced. Domain is an annotation, not a constraint.

Nodes:
1. Kuhn (gateway, epistemology-cold, 64yr) — already run, re-running for comparison
2. GPT-4 Technical Report (foundation, weight-cold, 2yr)
3. Kotter / Leading Change (protocol, 7yr)
4. Hydrology paper (lag state, 0yr — baseline for empty cold profile)

Output: one JSON per node + comparative summary.
"""

import json
import time
from datetime import datetime, timezone
from scout_utils import api_get, get_citations, get_references, zone_label, SEMANTIC_SCHOLAR_API

PAUSE = 6.0
CURRENT_YEAR = 2026

NODES = [
    {
        "label":    "Kuhn — Structure of Scientific Revolutions (1962)",
        "paper_id": "5f1885ae9a528b6449c14a46a19e1b8f81cac7c5",
        "pub_year": 1962,
        "functional_mode": "gateway",
    },
    {
        "label":    "GPT-4 Technical Report (2023)",
        "paper_id": "163b4d6a79a5b19af88b8585456363340d9efd04",
        "pub_year": 2023,
        "functional_mode": "foundation",
    },
    {
        "label":    "Kotter — Leading Change (2012/2018)",
        "paper_id": "789ba356e469b65f4a2743925a5e725b27cc61d6",
        "pub_year": 2012,
        "functional_mode": "protocol",
    },
    {
        "label":    "Entropy/Hydrology — When physics gets in the way (2026)",
        "paper_id": "35d163e6b6a1acf6b36e433456a64c85b6d45652",
        "pub_year": 2026,
        "functional_mode": "lag_state_baseline",
    },
]

def compute_velocity(citation_count, pub_year):
    age = CURRENT_YEAR - pub_year
    if age <= 0:
        return None
    return round(citation_count / age, 1)

def warm_zone_profile(citing_papers, pub_year):
    if not citing_papers:
        return {"sample_size": 0}

    years  = [p.get("year") for p in citing_papers if p.get("year")]
    cites  = [p.get("citationCount") or 0 for p in citing_papers]
    recent = [y for y in years if y and y >= 2021]

    velocities = []
    for p in citing_papers:
        y = p.get("year")
        c = p.get("citationCount") or 0
        if y and y < CURRENT_YEAR:
            velocities.append(round(c / (CURRENT_YEAR - y), 1))

    domains_raw = [p.get("title", "") for p in citing_papers]

    return {
        "sample_size":        len(citing_papers),
        "year_range":         [min(years), max(years)] if years else None,
        "recency_fraction":   round(len(recent) / len(years), 3) if years else None,
        "avg_citations":      round(sum(cites) / len(cites), 1) if cites else None,
        "max_citations":      max(cites) if cites else None,
        "avg_velocity":       round(sum(velocities) / len(velocities), 1) if velocities else None,
        "top_citing_papers":  sorted(
            [{"title": (p.get("title") or "")[:65],
              "year":  p.get("year"),
              "citations": p.get("citationCount") or 0}
             for p in citing_papers],
            key=lambda x: x["citations"], reverse=True
        )[:8]
    }

def run_node(node_info):
    print(f"\n{'='*60}")
    print(f"[C2] {node_info['label']}")
    print(f"     functional_mode={node_info['functional_mode']}")
    print(f"{'='*60}")

    time.sleep(PAUSE)
    data = api_get(
        f"{SEMANTIC_SCHOLAR_API}/paper/{node_info['paper_id']}",
        params={"fields": "paperId,title,year,citationCount,referenceCount,influentialCitationCount"}
    )
    if not data or not data.get("paperId"):
        print(f"  [failed to fetch]")
        return None

    citation_count = data.get("citationCount", 0)
    influential    = data.get("influentialCitationCount", 0)
    velocity       = compute_velocity(citation_count, node_info["pub_year"])
    influence_rate = round(influential / citation_count, 3) if citation_count else None

    print(f"  citations={citation_count} | influential={influential} | velocity={velocity}/yr")

    time.sleep(PAUSE)
    citing = []
    raw = api_get(
        f"{SEMANTIC_SCHOLAR_API}/paper/{node_info['paper_id']}/citations",
        params={"fields": "citingPaper.paperId,citingPaper.title,citingPaper.year,citingPaper.citationCount", "limit": 50}
    )
    if raw and raw.get("data"):
        citing = [item["citingPaper"] for item in raw["data"] if item.get("citingPaper")]

    warm = warm_zone_profile(citing, node_info["pub_year"])
    cold_velocity = velocity
    warm_velocity = warm.get("avg_velocity")
    ratio = round(warm_velocity / cold_velocity, 3) if (cold_velocity and warm_velocity and cold_velocity > 0) else None

    print(f"  warm_zone: sample={warm.get('sample_size')} recency={warm.get('recency_fraction')} avg_cites={warm.get('avg_citations')} avg_vel={warm_velocity}")
    print(f"  velocity_ratio (warm/cold): {ratio}")
    print(f"  top citing papers:")
    for p in (warm.get("top_citing_papers") or [])[:5]:
        print(f"    [{p['citations']}] ({p['year']}) {p['title'][:55]}")

    return {
        "label":            node_info["label"],
        "paper_id":         node_info["paper_id"],
        "functional_mode":  node_info["functional_mode"],
        "pub_year":         node_info["pub_year"],
        "citation_count":   citation_count,
        "influential_citations": influential,
        "influence_rate":   influence_rate,
        "cold_entry_velocity": velocity,
        "warm_zone":        warm,
        "velocity_ratio":   ratio,
    }

def run():
    print("\nC2 VELOCITY — ALL DISCOVERED COLD NODES")
    print("Running sequentially. Observe before comparing.")
    print("Nodes surfaced by traversal — not declared in advance.\n")

    results = []
    for node in NODES:
        r = run_node(node)
        if r:
            results.append(r)
        time.sleep(PAUSE * 2)  # longer pause between nodes

    # Comparative summary
    print("\n" + "="*60)
    print("COMPARATIVE SUMMARY")
    print("="*60)
    print(f"{'Label':<45} {'Mode':<12} {'Cold vel':<10} {'Warm vel':<10} {'Ratio':<8} {'Recency'}")
    print("-"*100)
    for r in results:
        wz = r.get("warm_zone", {})
        print(f"{r['label'][:44]:<45} {r['functional_mode']:<12} "
              f"{str(r['cold_entry_velocity']):<10} "
              f"{str(wz.get('avg_velocity','—')):<10} "
              f"{str(r.get('velocity_ratio','—')):<8} "
              f"{str(wz.get('recency_fraction','—'))}")

    output = {
        "constant": "C2_velocity_all_nodes",
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "nodes": results,
    }
    with open("c2_velocity_all_output.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[C2] Complete. Output: c2_velocity_all_output.json")

if __name__ == "__main__":
    run()
