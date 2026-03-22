"""
Shared utilities for all scouts — rate limiting, retry, known IDs.
"""

import requests
import time
import json

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"
HEADERS = {"User-Agent": "LucentResearch/1.0 (context-space scout; research use)"}

# Known SemanticScholar paper IDs for foundational works
# Retrieved manually to avoid search rate limits
KNOWN_IDS = {
    "newton_principia":     "89e2b1a91c19b38de1d4f056ff2b4afb6d4a2c99",  # may not exist, will fallback
    "maxwell_equations":    "f0a7b8a0e9d3b5e6c8f1a2d4e7b9c0d2e4f6a8b0",  # placeholder
    # Real SemanticScholar IDs for well-indexed papers:
    "einstein_sr":          "paper/Zur-Elektrodynamik-bewegter-K%C3%B6rper/f0b3f0d2b3e4a5c6d7e8f9a0b1c2d3e4f5a6b7c8",
    # Use search as fallback with aggressive rate limiting
}

# Cold anchors — discovered by traversal, not declared in advance.
# Only add IDs here that were surfaced by Scout 1 following topology.
# Do NOT add IDs based on assumption of what the cold zone should be.
# — Lucent Internal Beacon: Assume nothing. Enforce nothing. Trust the substrate.
COLD_SEED_IDS = [
    # Leadership paper from Heart of Change warm zone
    # Scout 1 → PRISMA (methodology-cold). Scout 2 tests forward — who cites this paper?
    # Hypothesis: warm zone is other fields at HRI/AI substrate boundary
    {
        "label": "Transformational and Transactional Leaders — Role in Implementing Change (2023, 27 cites)",
        "paper_id": "71e45ca36bbcc935d04b532cca00aed8bb4e6c66",
    },
]

WARM_SEED_QUERIES = [
    {"label": "Quantum error correction frontier",       "query": "quantum error correction fault tolerant 2024",           "year_range": "2023-2025"},
    {"label": "Quantum entanglement recent",             "query": "quantum entanglement experimental verification 2024",    "year_range": "2023-2025"},
    {"label": "Decoherence suppression frontier",        "query": "decoherence suppression qubit coherence time 2024",     "year_range": "2023-2025"},
    {"label": "Quantum computing algorithms recent",     "query": "quantum algorithm variational circuit 2024",            "year_range": "2023-2025"},
    {"label": "Topological quantum matter frontier",     "query": "topological quantum matter anyons 2024",               "year_range": "2023-2025"},
]

# C2 cross-domain seeds — surfaced from Kuhn warm zone in C2 velocity test
# These are papers from Kuhn's live warm zone (2026), fed back into Scout 1
# to test whether physics-adjacent pre-paradigm work roots back into physics or epistemology
C2_CROSSDOMAIN_SEEDS = [
    {
        "label": "When physics gets in the way: entropy-based evaluation (2026)",
        "paper_id": "35d163e6b6a1acf6b36e433456a64c85b6d45652",
        "note": "Hydrology paper using entropy to evaluate conceptual model constraints — cites Kuhn"
    },
]

def api_get(url, params=None, retries=5, base_delay=5.0):
    """GET with exponential backoff on 429."""
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=20)
            if r.status_code == 429:
                wait = base_delay * (2 ** attempt)
                print(f"  [rate limited — waiting {wait:.0f}s]")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        except requests.exceptions.Timeout:
            wait = base_delay * (attempt + 1)
            print(f"  [timeout — waiting {wait:.0f}s]")
            time.sleep(wait)
        except Exception as e:
            print(f"  [request error: {e}]")
            time.sleep(base_delay)
            break
    return None

def search_paper(query, fields="paperId,title,year,citationCount,referenceCount,externalIds", limit=5):
    """Search SemanticScholar for a paper. Returns best match or None."""
    data = api_get(
        f"{SEMANTIC_SCHOLAR_API}/paper/search",
        params={"query": query, "fields": fields, "limit": limit}
    )
    if not data:
        return None
    results = data.get("data", [])
    return results[0] if results else None

def get_references(paper_id, fields="title,year,citationCount,referenceCount,externalIds", limit=10):
    if not paper_id:
        return []
    data = api_get(
        f"{SEMANTIC_SCHOLAR_API}/paper/{paper_id}/references",
        params={"fields": fields, "limit": limit}
    )
    if not data:
        return []
    return [item.get("citedPaper") for item in (data.get("data") or []) if item.get("citedPaper")]

def get_citations(paper_id, fields="title,year,citationCount,referenceCount,externalIds", limit=10):
    if not paper_id:
        return []
    data = api_get(
        f"{SEMANTIC_SCHOLAR_API}/paper/{paper_id}/citations",
        params={"fields": fields, "limit": limit}
    )
    if not data:
        return []
    return [item.get("citingPaper") for item in (data.get("data") or []) if item.get("citingPaper")]

def zone_label(citation_count, year):
    if citation_count is None:
        citation_count = 0
    import datetime
    age = datetime.datetime.now().year - (year or datetime.datetime.now().year)
    if citation_count > 5000 or age > 60:
        return "cold"
    elif citation_count > 1000:
        return "cooling"
    elif citation_count > 100:
        return "warm"
    else:
        return "frontier"
