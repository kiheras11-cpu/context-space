"""
Scout 1 — Warm to Cold (Microbiome Seed)
------------------------------------------
Orthogonality test: does the context space topology hold when seeded
from a domain with NO overlap with physics, CS, or organizational theory?

Microbiome research selected because:
- Active substrate change (gut-brain axis, cancer microbiome, antibiotic resistance)
- Completely orthogonal to prior seeds (quantum, LLMs, organizational change)
- Rich citation graph — high volume of recent frontier work
- If Kuhn appears here, it's structural, not a prior artifact

This scout does NOT interpret. It collects and records the traversal path.
The path itself is the data.

EMERGENCE LOG: Entry 021 (pending)
"""

import requests
import json
import time
from datetime import datetime

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"
HEADERS = {"User-Agent": "LucentResearch/1.0 (context-space scout; research use)"}
OUTPUT_FILE = "scout1_microbiome_output.json"

MAX_DEPTH = 5           # extra depth — microbiome is a newer field, cold may be further back
MAX_SEED_PAPERS = 5
MAX_REFS_PER_NODE = 8   # wider fan — we want to see what's being reached for


def search_frontier(max_results=15):
    """Find recent high-activity microbiome papers — frontier zone."""
    url = f"{SEMANTIC_SCHOLAR_API}/paper/search"
    params = {
        "query": "gut microbiome human health disease",
        "fields": "title,year,citationCount,externalIds,abstract",
        "limit": max_results * 3,
        "publicationDateOrYear": "2022-2025",
    }
    print(f"[SCOUT1-MICROBIOME] Querying SemanticScholar for microbiome frontier papers...")
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        results = r.json().get("data", [])
        entries = []
        for p in results:
            ext = p.get("externalIds") or {}
            # Accept papers with any external ID — microbiome may not be on arXiv
            paper_id = (ext.get("ArXiv") or ext.get("DOI") or
                        p.get("paperId"))
            if paper_id and p.get("citationCount", 0) >= 20:
                entries.append({
                    "title": p.get("title", ""),
                    "paper_id": p.get("paperId"),  # use SS paper ID as primary
                    "arxiv_id": ext.get("ArXiv"),
                    "doi": ext.get("DOI"),
                    "year": str(p.get("year", "")),
                    "citation_count": p.get("citationCount", 0),
                })
        entries.sort(key=lambda x: x["citation_count"], reverse=True)
        print(f"[SCOUT1-MICROBIOME] Found {len(entries)} frontier papers")
        return entries[:max_results]
    except Exception as e:
        print(f"[SCOUT1-MICROBIOME] Query failed: {e}")
        return []


def get_references(paper_id, max_refs=8):
    """Get what a paper cites — one hop backward toward foundation."""
    url = f"{SEMANTIC_SCHOLAR_API}/paper/{paper_id}"
    params = {
        "fields": (
            "title,year,citationCount,referenceCount,"
            "references.paperId,references.title,references.year,"
            "references.externalIds,references.citationCount,references.referenceCount"
        )
    }
    try:
        time.sleep(5)  # conservative rate limit — learned from last session
        r = requests.get(url, params=params, headers=HEADERS, timeout=20)
        if r.status_code == 429:
            print("  [rate limited — waiting 30s]")
            time.sleep(30)
            r = requests.get(url, params=params, headers=HEADERS, timeout=20)
        if r.status_code == 404:
            return None, []
        r.raise_for_status()
        data = r.json()
        refs = data.get("references", [])
        # Sort by citation count — most-cited references are the anchors the field leans on
        refs_sorted = sorted(refs, key=lambda x: x.get("citationCount", 0), reverse=True)
        return data, refs_sorted[:max_refs]
    except Exception as e:
        print(f"  [ref lookup failed: {e}]")
        return None, []


def classify_zone(citation_count, ref_count, year, depth):
    """Rough temperature classification."""
    try:
        yr = int(year)
    except (ValueError, TypeError):
        yr = 0

    if citation_count is None:
        citation_count = 0
    if ref_count is None:
        ref_count = 0

    # Cold: very high citations, likely foundational
    if citation_count > 5000:
        return "cold"
    if citation_count > 1000 and yr < 2010:
        return "cold"
    # Warm: recent, active
    if yr >= 2020 and citation_count < 500:
        return "warm"
    if yr >= 2018 and citation_count < 200:
        return "warm"
    # Cooling: middle zone
    return "cooling"


def trace_warm_to_cold(seed_papers):
    chains = []
    visited = set()

    for seed in seed_papers[:MAX_SEED_PAPERS]:
        print(f"\n[CHAIN] Seed: {seed['title'][:70]}...")
        print(f"        Year: {seed['year']} | Citations: {seed['citation_count']}")

        chain = [{
            "title": seed["title"],
            "paper_id": seed["paper_id"],
            "year": seed["year"],
            "citation_count": seed["citation_count"],
            "depth": 0,
            "zone": "frontier",
        }]

        current_id = seed["paper_id"]
        visited.add(current_id)

        for depth in range(1, MAX_DEPTH + 1):
            paper_data, refs = get_references(current_id, max_refs=MAX_REFS_PER_NODE)

            if not refs:
                chain[-1]["zone"] = "cold_candidate"
                print(f"  depth {depth}: no further references — cold candidate")
                break

            best = refs[0]
            title = best.get("title", "Unknown")
            year = str(best.get("year", "?"))
            cites = best.get("citationCount", 0)
            ref_count = best.get("referenceCount", 0)
            pid = best.get("paperId")

            zone = classify_zone(cites, ref_count, year, depth)

            # Record all top refs as siblings so we can see what the field reaches for
            siblings = [
                {
                    "title": r.get("title", "?")[:60],
                    "year": str(r.get("year", "?")),
                    "citations": r.get("citationCount", 0),
                }
                for r in refs[1:5]
            ]

            node = {
                "title": title,
                "paper_id": pid,
                "year": year,
                "citation_count": cites,
                "reference_count": ref_count,
                "depth": depth,
                "zone": zone,
                "siblings": siblings,
            }
            chain.append(node)
            print(f"  depth {depth}: [{zone}] {title[:60]} ({year}) cites={cites}")

            if zone == "cold":
                print(f"  → Cold zone reached at depth {depth}")
                break

            if pid and pid not in visited:
                visited.add(pid)
                current_id = pid
            else:
                print(f"  depth {depth}: already visited or no ID — stopping chain")
                break

        chains.append({
            "seed": seed["title"],
            "seed_year": seed["year"],
            "seed_citations": seed["citation_count"],
            "chain": chain,
            "chain_length": len(chain),
            "reached_cold": any(n["zone"] in ("cold", "cold_candidate") for n in chain),
            "cold_node": next(
                (n for n in chain if n["zone"] in ("cold", "cold_candidate")), None
            ),
        })

        print(f"  Chain complete. Length: {len(chain)} | Cold reached: {chains[-1]['reached_cold']}")
        time.sleep(10)  # pause between seeds

    return chains


def run():
    print("=" * 65)
    print("SCOUT 1 — MICROBIOME SEED (Orthogonality Test)")
    print("Domain: Gut microbiome / human health")
    print("Question: Does the topology hold outside physics/CS?")
    print("=" * 65)

    seeds = search_frontier(max_results=MAX_SEED_PAPERS + 5)

    if not seeds:
        print("No seed papers found. Check API access.")
        return

    print(f"\nSeeds selected:")
    for s in seeds[:MAX_SEED_PAPERS]:
        print(f"  - {s['title'][:65]} ({s['year']}, {s['citation_count']} cites)")

    chains = trace_warm_to_cold(seeds)

    # Summary — raw topology only, no anchor recognition
    # Anchor classification is Scout 3's job — do not pre-interpret here
    cold_nodes = [c["cold_node"] for c in chains if c["cold_node"]]
    cold_titles = [n["title"] for n in cold_nodes]

    output = {
        "scout": "warm_to_cold_microbiome",
        "run_timestamp": datetime.utcnow().isoformat(),
        "domain": "gut microbiome / human health",
        "orthogonality_test": True,
        "seed_count": len(chains),
        "chains": chains,
        "summary": {
            "total_chains": len(chains),
            "chains_reaching_cold": sum(1 for c in chains if c["reached_cold"]),
            "avg_chain_length": round(
                sum(c["chain_length"] for c in chains) / len(chains), 2
            ) if chains else 0,
            "cold_nodes_found": cold_titles,
            # NOTE: No known-anchor detection here — that is Scout 3's role.
            # Scout 1 collects topology only. Interpretation is a separate pass.
        }
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n{'=' * 65}")
    print(f"COMPLETE — {len(chains)} chains | Output: {OUTPUT_FILE}")
    print(f"Cold reached: {output['summary']['chains_reaching_cold']}/{len(chains)}")
    print(f"Cold nodes found: {cold_titles}")
    print(f"NOTE: Anchor recognition deferred to Scout 3.")

if __name__ == "__main__":
    run()
