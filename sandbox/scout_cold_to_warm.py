"""
Scout 2 — Cold to Warm
------------------------
Starts at the foundation. Takes known foundational physics works
and traces FORWARD through what built upon them — following the
lineage from cold stable ground toward the warm active frontier.

Strategy:
- Seed with known cold-zone anchors (Newton, Carnot, Faraday equivalents in arXiv)
  We use SemanticScholar for pre-arXiv foundational works by DOI/title search
- For each: find papers that CITE this node (forward citation)
- Follow citations forward, picking the most-cited descendant at each step
- Output: chain from foundation → frontier

This scout does NOT interpret. Path is the data.
"""

import requests
import json
import time
from datetime import datetime

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"
HEADERS = {"User-Agent": "LucentResearch/1.0 (context-space scout; research use)"}
OUTPUT_FILE = "scout_cold_warm_output.json"

MAX_DEPTH = 5
MAX_CITATIONS_PER_NODE = 5

# Cold-zone seed works — foundational physics
# Using SemanticScholar paper search by title
COLD_SEEDS = [
    {"title": "Philosophiae Naturalis Principia Mathematica", "author": "Newton", "year": 1687, "label": "Newton — Principia"},
    {"title": "A Dynamical Theory of the Electromagnetic Field", "author": "Maxwell", "year": 1865, "label": "Maxwell — Equations"},
    {"title": "Uber die von der molekularkinetischen Theorie der Warme geforderte Bewegung", "author": "Einstein", "year": 1905, "label": "Einstein — Brownian Motion"},
    {"title": "On the Constitution of Atoms and Molecules", "author": "Bohr", "year": 1913, "label": "Bohr — Atomic Model"},
    {"title": "Quantisierung als Eigenwertproblem", "author": "Schrodinger", "year": 1926, "label": "Schrödinger — Wave Equation"},
]

def search_semantic_scholar(title, limit=1):
    """Find a paper by title on SemanticScholar."""
    url = f"{SEMANTIC_SCHOLAR_API}/paper/search"
    params = {
        "query": title,
        "limit": limit,
        "fields": "paperId,title,year,citationCount,externalIds"
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        results = data.get("data", [])
        return results[0] if results else None
    except Exception as e:
        print(f"  [search failed: {e}]")
        return None

def get_citations(paper_id, max_citations=5):
    """Get papers that CITE this paper — forward in time, toward warm zone."""
    url = f"{SEMANTIC_SCHOLAR_API}/paper/{paper_id}/citations"
    params = {
        "fields": "title,year,citationCount,externalIds",
        "limit": 50
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        cites = data.get("data", [])
        # Extract citing papers
        papers = []
        for c in cites:
            citing = c.get("citingPaper", {})
            if citing:
                papers.append(citing)
        # Sort by citation count — follow the most-impactful downstream path
        papers_sorted = sorted(papers, key=lambda x: x.get("citationCount", 0), reverse=True)
        return papers_sorted[:max_citations]
    except Exception as e:
        print(f"  [citation lookup failed: {e}]")
        return []

def classify_zone(citation_count, year):
    """Rough zone classification by citation count and recency."""
    if citation_count is None:
        citation_count = 0
    current_year = datetime.utcnow().year
    age = current_year - (year or current_year)
    if age > 50:
        return "cold"
    elif citation_count > 5000:
        return "cold"  # old and highly cited = foundational = cold
    elif citation_count > 1000:
        return "cooling"
    elif citation_count > 100:
        return "warm"
    else:
        return "frontier"

def trace_cold_to_warm(seed, max_depth=5, max_cites=5):
    """Trace forward from a cold seed toward the warm frontier."""
    print(f"\n[COLD→WARM] Seeding from: {seed['label']}")

    # Find the seed paper on SemanticScholar
    time.sleep(0.5)
    result = search_semantic_scholar(seed["title"])
    if not result:
        print(f"  [not found on SemanticScholar]")
        return None

    paper_id = result.get("paperId")
    citation_count = result.get("citationCount", 0)
    year = result.get("year", seed["year"])

    chain = [{
        "title": result.get("title", seed["title"]),
        "paper_id": paper_id,
        "year": year,
        "citation_count": citation_count,
        "depth": 0,
        "zone": classify_zone(citation_count, year),
        "label": seed["label"]
    }]

    print(f"  Found: {result.get('title', '')[:55]} | citations={citation_count} | zone={chain[0]['zone']}")

    current_id = paper_id

    for depth in range(1, max_depth + 1):
        time.sleep(0.6)
        citations = get_citations(current_id, max_citations=max_cites)

        if not citations:
            print(f"  depth {depth}: no citations found — frontier reached")
            break

        # Pick most-cited downstream paper (dominant path toward warm)
        best = citations[0]
        best_title = best.get("title", "Unknown")
        best_year = best.get("year") or 0
        best_count = best.get("citationCount", 0)
        best_id = best.get("paperId")
        ext_ids = best.get("externalIds", {}) or {}
        best_arxiv = ext_ids.get("ArXiv")

        zone = classify_zone(best_count, best_year)

        node = {
            "title": best_title,
            "paper_id": best_id,
            "arxiv_id": best_arxiv,
            "year": best_year,
            "citation_count": best_count,
            "depth": depth,
            "zone": zone,
            "siblings_considered": [p.get("title", "?")[:50] for p in citations[1:3]]
        }
        chain.append(node)
        print(f"  depth {depth}: [{zone}] {best_title[:55]} ({best_year}) cites={best_count}")

        if best_id:
            current_id = best_id
        else:
            break

    return {
        "seed_label": seed["label"],
        "chain": chain,
        "chain_length": len(chain),
        "reached_warm": any(n["zone"] in ("warm", "frontier") for n in chain[1:])
    }

def run():
    print("=" * 60)
    print("SCOUT 2 — COLD TO WARM")
    print("Starting at foundation, tracing toward frontier")
    print("=" * 60)

    chains = []
    for seed in COLD_SEEDS:
        result = trace_cold_to_warm(seed, max_depth=MAX_DEPTH, max_cites=MAX_CITATIONS_PER_NODE)
        if result:
            chains.append(result)
        time.sleep(1.0)

    output = {
        "scout": "cold_to_warm",
        "run_timestamp": datetime.utcnow().isoformat(),
        "seed_count": len(COLD_SEEDS),
        "chains": chains,
        "summary": {
            "total_chains": len(chains),
            "chains_reaching_warm": sum(1 for c in chains if c.get("reached_warm")),
            "avg_chain_length": round(sum(c["chain_length"] for c in chains) / len(chains), 2) if chains else 0,
        }
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n[COLD→WARM] Complete. {len(chains)} chains. Output: {OUTPUT_FILE}")
    print(f"Summary: {output['summary']}")

if __name__ == "__main__":
    run()
