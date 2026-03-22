"""
C2 — Temporal Persistence: Velocity Approximation Test
-------------------------------------------------------
C2's full form requires historical snapshots (run twice, weeks apart).
This approximation uses what we have now:
  - citations-per-year since publication = cold-entry velocity
  - warm zone density = how much is actively building on top
  - velocity profile of the warm zone itself = is the building accelerating or decelerating?

First stress test: Kuhn (Structure of Scientific Revolutions)
  - Known cold anchor, discovered by Scout 1
  - Functional mode: Gateway
  - Question: what does the temporal profile of a gateway node look like?

Protocol: Observe before naming. Record what appears. Do not interpret during collection.
"""

import json
import time
from datetime import datetime, timezone
from scout_utils import api_get, get_citations, get_references, zone_label, SEMANTIC_SCHOLAR_API

PAUSE = 5.0
OUTPUT_FILE = "c2_velocity_kuhn_output.json"

KUHN_ID = "5f1885ae9a528b6449c14a46a19e1b8f81cac7c5"
KUHN_YEAR = 1962  # original publication; SS has 1964 edition

def get_paper_full(paper_id):
    return api_get(
        f"{SEMANTIC_SCHOLAR_API}/paper/{paper_id}",
        params={"fields": "paperId,title,year,citationCount,referenceCount,influentialCitationCount"}
    )

def get_citations_with_year(paper_id, limit=50):
    """Pull citing papers with year and citation count — warm zone sample."""
    data = api_get(
        f"{SEMANTIC_SCHOLAR_API}/paper/{paper_id}/citations",
        params={"fields": "citingPaper.paperId,citingPaper.title,citingPaper.year,citingPaper.citationCount", "limit": limit}
    )
    if not data:
        return []
    return [
        item["citingPaper"]
        for item in (data.get("data") or [])
        if item.get("citingPaper") and item["citingPaper"].get("paperId")
    ]

def compute_velocity(citation_count, pub_year, current_year=2026):
    """Citations per year since publication."""
    age = current_year - pub_year
    if age <= 0:
        return None
    return round(citation_count / age, 1)

def warm_zone_profile(citing_papers):
    """
    Characterize the warm zone above a cold node.
    - year distribution: when were the citing papers published?
    - citation density: how much is each citing paper itself cited?
    - velocity: citations/year for each citing paper
    - recency: what fraction published in last 5 years?
    """
    if not citing_papers:
        return {}

    current_year = 2026
    years = [p.get("year") for p in citing_papers if p.get("year")]
    cites = [p.get("citationCount") or 0 for p in citing_papers]

    recent = [y for y in years if y and y >= 2021]
    old = [y for y in years if y and y < 2000]

    velocities = []
    for p in citing_papers:
        y = p.get("year")
        c = p.get("citationCount") or 0
        if y and y < current_year:
            velocities.append(round(c / (current_year - y), 1))

    return {
        "sample_size": len(citing_papers),
        "year_range": [min(years), max(years)] if years else None,
        "recency_fraction": round(len(recent) / len(years), 3) if years else None,
        "pre_2000_fraction": round(len(old) / len(years), 3) if years else None,
        "avg_citations": round(sum(cites) / len(cites), 1) if cites else None,
        "max_citations": max(cites) if cites else None,
        "median_citations": sorted(cites)[len(cites)//2] if cites else None,
        "avg_velocity": round(sum(velocities) / len(velocities), 1) if velocities else None,
        "top_citing_papers": sorted(
            [{"title": (p.get("title") or "")[:65], "year": p.get("year"), "citations": p.get("citationCount") or 0}
             for p in citing_papers],
            key=lambda x: x["citations"], reverse=True
        )[:8]
    }

def run():
    print("=" * 60)
    print("C2 VELOCITY TEST — KUHN")
    print("Temporal persistence approximation")
    print("Stress test: gateway node profile")
    print("=" * 60)

    # Step 1: Pull the cold node itself
    print(f"\n[C2] Pulling Kuhn cold node...")
    time.sleep(PAUSE)
    kuhn = get_paper_full(KUHN_ID)
    if not kuhn:
        print("[C2] Failed to fetch Kuhn. Exiting.")
        return

    citation_count = kuhn.get("citationCount", 0)
    influential = kuhn.get("influentialCitationCount", 0)
    velocity = compute_velocity(citation_count, KUHN_YEAR)

    print(f"  Title: {kuhn.get('title')}")
    print(f"  Year: {KUHN_YEAR} (SS year: {kuhn.get('year')})")
    print(f"  Total citations: {citation_count}")
    print(f"  Influential citations: {influential}")
    print(f"  Cold-entry velocity: {velocity} citations/year (over {2026 - KUHN_YEAR} years)")

    # Step 2: Pull warm zone sample (papers citing Kuhn)
    print(f"\n[C2] Sampling warm zone (50 citing papers)...")
    time.sleep(PAUSE)
    citing = get_citations_with_year(KUHN_ID, limit=50)
    print(f"  Retrieved {len(citing)} citing papers")

    warm_profile = warm_zone_profile(citing)

    print(f"\n[C2] Warm zone profile:")
    print(f"  Sample size: {warm_profile.get('sample_size')}")
    print(f"  Year range: {warm_profile.get('year_range')}")
    print(f"  Recency fraction (2021+): {warm_profile.get('recency_fraction')}")
    print(f"  Pre-2000 fraction: {warm_profile.get('pre_2000_fraction')}")
    print(f"  Avg citations of citing papers: {warm_profile.get('avg_citations')}")
    print(f"  Max citations of citing paper: {warm_profile.get('max_citations')}")
    print(f"  Avg velocity of warm zone: {warm_profile.get('avg_velocity')} cites/yr")
    print(f"\n  Top citing papers:")
    for p in (warm_profile.get("top_citing_papers") or []):
        print(f"    [{p['citations']}] ({p['year']}) {p['title']}")

    # Step 3: Compute velocity ratio
    # Cold-entry velocity vs warm zone avg velocity
    cold_v = velocity
    warm_v = warm_profile.get("avg_velocity")
    ratio = round(warm_v / cold_v, 3) if (cold_v and warm_v and cold_v > 0) else None

    print(f"\n[C2] Velocity ratio (warm_avg / cold): {ratio}")
    if ratio:
        if ratio > 2.0:
            print(f"  → Warm zone is accelerating relative to the cold anchor")
        elif ratio < 0.5:
            print(f"  → Warm zone is slower than cold anchor — cold node is anomalously high-velocity")
        else:
            print(f"  → Warm and cold velocities are roughly proportional")

    output = {
        "constant": "C2_velocity_approximation",
        "test": "gateway_node_kuhn",
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "cold_node": {
            "paper_id": KUHN_ID,
            "title": kuhn.get("title"),
            "pub_year": KUHN_YEAR,
            "ss_year": kuhn.get("year"),
            "citation_count": citation_count,
            "influential_citations": influential,
            "cold_entry_velocity": velocity,
            "functional_mode": "gateway",
        },
        "warm_zone": warm_profile,
        "velocity_ratio": ratio,
        "observations": []
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n[C2] Complete. Output: {OUTPUT_FILE}")

if __name__ == "__main__":
    run()
