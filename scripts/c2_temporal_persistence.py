"""
C2 — Temporal Persistence: How Long Has Each Node Held Its Functional Mode?
----------------------------------------------------------------------------
For each discovered cold node, pull a large sample of citing papers (200+),
group by decade, and measure whether the functional mode signature has been
consistent over time.

Gateway: domain spread should be broad and consistent across decades
Foundation: domain should be narrow/concentrated, possibly accelerating
Protocol: circuit should close locally in every decade sampled

If the function has been stable across decades → the mode is structurally
assigned, not a momentary pattern.
If the function is recent → the node was something else before. That transition
is itself significant data.

Observe before naming. Do not interpret during collection.
"""

import json
import time
from datetime import datetime, timezone
from collections import defaultdict
from scout_utils import api_get, SEMANTIC_SCHOLAR_API

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
]

def get_citations_large(paper_id, limit=200):
    """Pull large sample of citing papers with year + citation count."""
    results = []
    offset = 0
    batch = 100
    while len(results) < limit:
        data = api_get(
            f"{SEMANTIC_SCHOLAR_API}/paper/{paper_id}/citations",
            params={
                "fields": "citingPaper.paperId,citingPaper.title,citingPaper.year,citingPaper.citationCount,citingPaper.fieldsOfStudy",
                "limit": batch,
                "offset": offset
            }
        )
        if not data or not data.get("data"):
            break
        batch_results = [
            item["citingPaper"]
            for item in data["data"]
            if item.get("citingPaper") and item["citingPaper"].get("paperId")
        ]
        results.extend(batch_results)
        if len(batch_results) < batch:
            break
        offset += batch
        time.sleep(PAUSE)
    return results[:limit]

def decade_of(year):
    if not year:
        return "unknown"
    return f"{(year // 10) * 10}s"

def analyze_decade(papers):
    """Characterize a set of citing papers from one decade."""
    if not papers:
        return {"count": 0}

    years  = [p.get("year") for p in papers if p.get("year")]
    cites  = [p.get("citationCount") or 0 for p in papers]

    # Field spread — how many distinct fieldsOfStudy represented
    fields = set()
    for p in papers:
        for f in (p.get("fieldsOfStudy") or []):
            if isinstance(f, dict):
                fields.add(f.get("category", str(f)))
            else:
                fields.add(str(f))

    # Top papers this decade
    top = sorted(papers, key=lambda x: x.get("citationCount") or 0, reverse=True)[:4]

    return {
        "count":          len(papers),
        "field_spread":   len(fields),
        "fields":         sorted(fields)[:8],
        "avg_citations":  round(sum(cites) / len(cites), 1) if cites else 0,
        "max_citations":  max(cites) if cites else 0,
        "top_papers":     [
            {
                "title":     (p.get("title") or "")[:60],
                "year":      p.get("year"),
                "citations": p.get("citationCount") or 0
            }
            for p in top
        ]
    }

def persistence_signature(decade_profiles):
    """
    Derive whether the functional mode has been stable across decades.
    Looks at field_spread trend and citation density trend.
    """
    decades = sorted(k for k in decade_profiles if k != "unknown")
    if len(decades) < 2:
        return "insufficient_data"

    spreads = [decade_profiles[d]["field_spread"] for d in decades]
    counts  = [decade_profiles[d]["count"] for d in decades]

    # Is field spread consistently broad (gateway) or consistently narrow (foundation/protocol)?
    avg_spread = sum(spreads) / len(spreads)
    spread_variance = sum((s - avg_spread) ** 2 for s in spreads) / len(spreads)

    # Is activity accelerating (foundation), steady (gateway), or flat/declining (protocol)?
    if len(counts) >= 2:
        early = sum(counts[:len(counts)//2]) / (len(counts)//2)
        late  = sum(counts[len(counts)//2:]) / (len(counts) - len(counts)//2)
        trend = "accelerating" if late > early * 1.5 else ("decelerating" if late < early * 0.5 else "stable")
    else:
        trend = "insufficient_data"

    return {
        "decades_sampled": decades,
        "avg_field_spread": round(avg_spread, 1),
        "spread_variance":  round(spread_variance, 2),
        "activity_trend":   trend,
        "interpretation":   (
            "function_stable_gateway"     if avg_spread >= 3 and spread_variance < 4 and trend == "stable"     else
            "function_stable_foundation"  if avg_spread <= 2 and trend == "accelerating"                       else
            "function_stable_protocol"    if avg_spread <= 2 and trend in ("stable", "decelerating")           else
            "function_evolving"           if spread_variance >= 4                                               else
            "function_recently_assigned"  if decades[0] >= "2010s"                                             else
            "unclear"
        )
    }

def run_node(node_info):
    print(f"\n{'='*60}")
    print(f"[C2 PERSIST] {node_info['label']}")
    print(f"             functional_mode={node_info['functional_mode']}")
    print(f"{'='*60}")

    print(f"  Pulling up to 200 citing papers...")
    time.sleep(PAUSE)
    citing = get_citations_large(node_info["paper_id"], limit=200)
    print(f"  Retrieved {len(citing)} citing papers")

    # Group by decade
    by_decade = defaultdict(list)
    for p in citing:
        by_decade[decade_of(p.get("year"))].append(p)

    decade_profiles = {}
    for decade, papers in sorted(by_decade.items()):
        profile = analyze_decade(papers)
        decade_profiles[decade] = profile
        print(f"\n  [{decade}] count={profile['count']} field_spread={profile['field_spread']} avg_cites={profile['avg_citations']}")
        print(f"    fields: {profile['fields'][:5]}")
        for tp in profile["top_papers"][:2]:
            print(f"    [{tp['citations']}] ({tp['year']}) {tp['title'][:55]}")

    sig = persistence_signature(decade_profiles)
    if isinstance(sig, str):
        sig = {"interpretation": sig, "note": "only one decade in sample — SS returning most-recent citations only"}
    print(f"\n  Persistence signature:")
    print(f"    decades_sampled:   {sig.get('decades_sampled', '—')}")
    print(f"    avg_field_spread:  {sig.get('avg_field_spread', '—')}")
    print(f"    spread_variance:   {sig.get('spread_variance', '—')}")
    print(f"    activity_trend:    {sig.get('activity_trend', '—')}")
    print(f"    interpretation:    {sig.get('interpretation', '—')}")
    if sig.get('note'):
        print(f"    note:              {sig['note']}")

    return {
        "label":            node_info["label"],
        "paper_id":         node_info["paper_id"],
        "pub_year":         node_info["pub_year"],
        "functional_mode":  node_info["functional_mode"],
        "total_sampled":    len(citing),
        "decade_profiles":  decade_profiles,
        "persistence_sig":  sig,
    }

def run():
    print("\nC2 TEMPORAL PERSISTENCE — HOW LONG HAS EACH NODE HELD ITS FUNCTION?")
    print("Pulling large citation samples. Grouping by decade. Observing before naming.\n")

    results = []
    for node in NODES:
        r = run_node(node)
        results.append(r)
        time.sleep(PAUSE * 3)  # generous pause between nodes

    # Comparative summary
    print("\n" + "="*70)
    print("COMPARATIVE PERSISTENCE SUMMARY")
    print("="*70)
    print(f"{'Label':<45} {'Mode':<12} {'Decades':<8} {'Avg spread':<12} {'Trend':<14} {'Interpretation'}")
    print("-"*120)
    for r in results:
        sig = r.get("persistence_sig", {})
        decades = sig.get("decades_sampled", [])
        print(f"{r['label'][:44]:<45} {r['functional_mode']:<12} "
              f"{len(decades):<8} "
              f"{str(sig.get('avg_field_spread','—')):<12} "
              f"{str(sig.get('activity_trend','—')):<14} "
              f"{str(sig.get('interpretation','—'))}")

    output = {
        "constant":       "C2_temporal_persistence",
        "run_timestamp":  datetime.now(timezone.utc).isoformat(),
        "nodes":          results,
    }
    with open("c2_temporal_persistence_output.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[C2] Complete. Output: c2_temporal_persistence_output.json")
    return output

if __name__ == "__main__":
    run()
