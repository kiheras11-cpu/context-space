"""
Scout 1 — Warm to Cold
------------------------
Starts at the frontier. Finds recent, high-activity physics papers
then traces back toward their foundational ancestry.

Strategy:
- Query arXiv for recent high-citation-density physics papers (last 2 years)
- For each: pull what it cites (SemanticScholar)
- Follow citations backward until we hit nodes with no further references
  (or until depth limit)
- Output: a chain from frontier → foundation, recording every node touched

This scout does NOT interpret. It collects and records the traversal path.
The path itself is the data.
"""

import requests
import json
import time
from datetime import datetime, timedelta

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"
ARXIV_API = "https://export.arxiv.org/api/query"

HEADERS = {"User-Agent": "LucentResearch/1.0 (context-space scout; research use)"}

OUTPUT_FILE = "scout_warm_cold_output.json"
MAX_DEPTH = 4          # how many hops back from frontier
MAX_SEED_PAPERS = 5    # frontier starting points
MAX_REFS_PER_NODE = 5  # how many references to follow per node

def search_arxiv_recent_physics(max_results=10):
    """Find recent high-activity physics papers via SemanticScholar — frontier zone."""
    # Use SemanticScholar bulk search for recent quantum physics papers
    url = f"{SEMANTIC_SCHOLAR_API}/paper/search"
    params = {
        "query": "quantum entanglement decoherence",
        "fields": "title,year,citationCount,externalIds,abstract",
        "limit": max_results * 3,
        "publicationDateOrYear": "2022-2025",
    }
    print(f"[WARM→COLD] Querying SemanticScholar for recent frontier papers...")
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        results = r.json().get("data", [])
        # Filter for papers with arXiv IDs and reasonable citation counts (active frontier)
        entries = []
        for p in results:
            ext = p.get("externalIds") or {}
            arxiv_id = ext.get("ArXiv")
            if arxiv_id and p.get("citationCount", 0) >= 5:
                entries.append({
                    "title": p.get("title", ""),
                    "arxiv_id": arxiv_id,
                    "published": str(p.get("year", "")),
                    "citation_count": p.get("citationCount", 0),
                    "source": "semantic_scholar_frontier"
                })
        # Sort by citation count — most active frontier nodes first
        entries.sort(key=lambda x: x["citation_count"], reverse=True)
        print(f"[WARM→COLD] Found {len(entries)} frontier papers")
        return entries[:max_results]
    except Exception as e:
        print(f"[WARM→COLD] SemanticScholar query failed: {e}")
        return []

def get_references_semantic_scholar(arxiv_id, max_refs=5):
    """Get what a paper cites — one hop backward toward foundation."""
    url = f"{SEMANTIC_SCHOLAR_API}/paper/arXiv:{arxiv_id}"
    params = {"fields": "title,year,referenceCount,references.title,references.year,references.externalIds,references.referenceCount"}
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if r.status_code == 404:
            return None, []
        r.raise_for_status()
        data = r.json()
        refs = data.get("references", [])
        # Sort by reference count descending — most-cited refs first (warmer nodes)
        refs_sorted = sorted(refs, key=lambda x: x.get("referenceCount", 0), reverse=True)
        return data, refs_sorted[:max_refs]
    except Exception as e:
        print(f"  [ref lookup failed for {arxiv_id}: {e}]")
        return None, []

def trace_warm_to_cold(seed_papers, max_depth=4, max_refs=5):
    """
    Starting from frontier seed papers, trace backward through references.
    Returns traversal chains: each chain = [frontier_node, ..., cold_node]
    """
    chains = []
    visited = set()

    for seed in seed_papers:
        print(f"\n[WARM→COLD] Tracing from: {seed['title'][:60]}...")
        chain = [{
            "title": seed["title"],
            "arxiv_id": seed["arxiv_id"],
            "year": seed.get("published", "")[:4],
            "depth": 0,
            "zone": "frontier",
            "ref_count": None
        }]

        current_id = seed["arxiv_id"]
        visited.add(current_id)

        for depth in range(1, max_depth + 1):
            time.sleep(0.5)  # rate limit respect
            paper_data, refs = get_references_semantic_scholar(current_id, max_refs=max_refs)

            if not refs:
                chain[-1]["zone"] = "cold_candidate" if depth > 1 else "frontier"
                print(f"  depth {depth}: no further references — cold candidate reached")
                break

            # Pick the most-referenced upstream node (the one the most work builds on)
            best_ref = refs[0]
            ref_title = best_ref.get("title", "Unknown")
            ref_year = best_ref.get("year", "?")
            ref_count = best_ref.get("referenceCount", 0)
            ext_ids = best_ref.get("externalIds", {}) or {}
            ref_arxiv = ext_ids.get("ArXiv", None)

            zone = "warm" if depth <= 2 else "cooling"
            if ref_count == 0 or ref_count is None:
                zone = "cold_candidate"

            node = {
                "title": ref_title,
                "arxiv_id": ref_arxiv,
                "year": ref_year,
                "depth": depth,
                "zone": zone,
                "ref_count": ref_count,
                "siblings_considered": [r.get("title", "?")[:50] for r in refs[1:3]]
            }
            chain.append(node)
            print(f"  depth {depth}: [{zone}] {ref_title[:55]} ({ref_year}) refs={ref_count}")

            if ref_arxiv and ref_arxiv not in visited:
                visited.add(ref_arxiv)
                current_id = ref_arxiv
            else:
                # Can't go deeper — no arXiv ID or already visited
                if not ref_arxiv:
                    node["zone"] = "cold_candidate"
                    print(f"  depth {depth}: no arXiv ID — likely foundational/pre-arXiv, cold candidate")
                break

        chains.append({
            "seed": seed["title"],
            "chain": chain,
            "chain_length": len(chain),
            "reached_cold": any(n["zone"] == "cold_candidate" for n in chain)
        })

    return chains

def run():
    print("=" * 60)
    print("SCOUT 1 — WARM TO COLD")
    print("Starting at the frontier, tracing toward foundation")
    print("=" * 60)

    seeds = search_arxiv_recent_physics(max_results=MAX_SEED_PAPERS + 5)
    seeds = seeds[:MAX_SEED_PAPERS]

    if not seeds:
        print("No seed papers found. Exiting.")
        return

    chains = trace_warm_to_cold(seeds, max_depth=MAX_DEPTH, max_refs=MAX_REFS_PER_NODE)

    output = {
        "scout": "warm_to_cold",
        "run_timestamp": datetime.utcnow().isoformat(),
        "seed_count": len(seeds),
        "chains": chains,
        "summary": {
            "total_chains": len(chains),
            "chains_reaching_cold": sum(1 for c in chains if c["reached_cold"]),
            "avg_chain_length": round(sum(c["chain_length"] for c in chains) / len(chains), 2) if chains else 0,
        }
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n[WARM→COLD] Complete. {len(chains)} chains. Output: {OUTPUT_FILE}")
    print(f"Summary: {output['summary']}")

if __name__ == "__main__":
    run()
