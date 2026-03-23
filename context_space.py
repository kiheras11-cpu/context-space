#!/usr/bin/env python3
"""
context_space.py — Minimum Viable Interface
────────────────────────────────────────────
Context Space | Lucent Research Division
Authors: Emmanuel K. + Erastus K. + Lisa Tsosie
GitHub: https://github.com/kiheras11-cpu/context-space

Runs C1 + C2 + C3 + C4 on any corpus or seed.
One command. No prior knowledge required.

USAGE:
    python context_space.py --seed "your paper title or concept"
    python context_space.py --seed "quantum error correction" --direction warm-to-cold
    python context_space.py --corpus my_papers.json
    python context_space.py --seed "GPT-4" --direction both --depth 4

SUBSTRATE MODES:
    citation   — SemanticScholar API (default)
    text       -- plain text file or directory of .txt/.md files
    findings   — run on the Context Space findings corpus itself

OUTPUT:
    Temperature map, cold zone with mode + service function,
    exposed sections (hallucination risk), decay profile, deposit log.
"""

import argparse
import json
import sys
import os
import time
import datetime
from collections import defaultdict

# ── Substrate adapter ────────────────────────────────────────────────────────

class CitationSubstrate:
    """Reads from SemanticScholar API."""

    def __init__(self):
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "sandbox"))
            from scout_utils import search_paper, get_references, get_citations, zone_label, api_get
            self._search = search_paper
            self._refs = get_references
            self._cites = get_citations
            self._zone = zone_label
            self._api_get = api_get
        except ImportError:
            print("[error] sandbox/scout_utils.py not found. Run from repo root.")
            sys.exit(1)

    def find(self, query):
        """Find a node by title/query. Returns node dict."""
        result = self._search(query)
        if not result:
            return None
        return self._normalize(result)

    def get_by_id(self, paper_id):
        from scout_utils import SEMANTIC_SCHOLAR_API, HEADERS
        data = self._api_get(
            f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}",
            params={"fields": "paperId,title,year,citationCount,referenceCount"}
        )
        if not data:
            return None
        return self._normalize(data)

    def references(self, node_id, limit=15):
        raw = self._refs(node_id, limit=limit)
        return [self._normalize(r) for r in raw if r]

    def citations(self, node_id, limit=15):
        raw = self._cites(node_id, limit=limit)
        return [self._normalize(c) for c in raw if c]

    def _normalize(self, r):
        return {
            "id":       r.get("paperId", ""),
            "title":    r.get("title", ""),
            "year":     r.get("year"),
            "weight":   r.get("citationCount", 0) or 0,
        }

    def temperature(self, node):
        year = node.get("year") or datetime.datetime.now().year
        w = node.get("weight", 0)
        age = datetime.datetime.now().year - year
        if w > 5000 or age > 60:
            return "cold"
        elif w > 1000:
            return "cooling"
        elif w > 100:
            return "warm"
        elif w == 0 and age < 1:
            return "lag"
        else:
            return "frontier"

    def velocity(self, node):
        year = node.get("year")
        w    = node.get("weight", 0)
        if not year or not w:
            return None
        age = max(datetime.datetime.now().year - year, 1)
        return round(w / age, 1)


class TextSubstrate:
    """
    Reads from plain text or markdown files.
    Nodes = files or paragraphs. Weight = inbound reference count.
    Direction warm→cold follows recency (newer = warm, older = cold).
    """

    def __init__(self, path):
        self.path = path
        self.nodes = self._load()

    def _load(self):
        nodes = {}
        if os.path.isfile(self.path):
            paths = [self.path]
        else:
            paths = [
                os.path.join(self.path, f)
                for f in os.listdir(self.path)
                if f.endswith((".txt", ".md"))
            ]
        for p in paths:
            with open(p) as f:
                content = f.read()
            nid = os.path.basename(p)
            nodes[nid] = {
                "id":    nid,
                "title": nid,
                "year":  self._extract_year(content, p),
                "weight": content.count("[[") + content.count("->"),  # basic link count
                "content": content[:500],
            }
        # Build reference graph from markdown links
        for nid, node in nodes.items():
            node["refs"] = [
                other for other in nodes
                if other != nid and other.replace(".md","") in node["content"]
            ]
        return nodes

    def _extract_year(self, content, path):
        import re
        m = re.search(r"20[12][0-9]", content[:200])
        if m:
            return int(m.group())
        try:
            mtime = os.path.getmtime(path)
            return datetime.datetime.fromtimestamp(mtime).year
        except:
            return 2024

    def find(self, query):
        query_lower = query.lower()
        for nid, node in self.nodes.items():
            if query_lower in nid.lower() or query_lower in node.get("content","").lower():
                return node
        return list(self.nodes.values())[0] if self.nodes else None

    def references(self, node_id, limit=10):
        node = self.nodes.get(node_id, {})
        return [self.nodes[r] for r in node.get("refs", [])[:limit] if r in self.nodes]

    def citations(self, node_id, limit=10):
        results = []
        for nid, node in self.nodes.items():
            if node_id in node.get("refs", []):
                results.append(node)
        return results[:limit]

    def temperature(self, node):
        year = node.get("year") or 2024
        age = datetime.datetime.now().year - year
        w   = node.get("weight", 0)
        if age > 5 and w > 3:
            return "cold"
        elif w > 2:
            return "warm"
        elif age < 1:
            return "frontier"
        else:
            return "cooling"

    def velocity(self, node):
        year = node.get("year")
        w    = node.get("weight", 0)
        if not year or not w:
            return None
        age = max(datetime.datetime.now().year - year, 1)
        return round(w / age, 1)


# ── C1 — Independence Convergence ────────────────────────────────────────────

def run_c1(seed_node, substrate, depth=3, visited=None, deposits=None):
    """
    Traverse warm→cold from seed. Collect cold zone nodes.
    Returns: {node_id: node_data} for cold zone discovered by convergence.
    """
    if visited is None:
        visited = set()
    if deposits is None:
        deposits = []

    cold_zone   = {}
    warm_zone   = {}
    traversal   = [(seed_node, 0)]
    node_sources = defaultdict(set)

    print(f"\n── C1: Warm→Cold from '{seed_node['title'][:60]}' ──")

    while traversal:
        node, d = traversal.pop(0)
        nid = node.get("id") or node.get("title")
        if not nid or nid in visited:
            continue
        visited.add(nid)

        temp = substrate.temperature(node)
        if temp in ("cold", "cooling"):
            cold_zone[nid] = node
            node_sources[nid].add("traversal")
            deposits.append(f"C1 cold discovered: {node['title'][:50]} ({temp})")
        else:
            warm_zone[nid] = node

        if d < depth:
            refs = substrate.references(nid, limit=8)
            time.sleep(1.5)
            for ref in refs:
                rid = ref.get("id") or ref.get("title")
                if rid and rid not in visited:
                    traversal.append((ref, d + 1))
                    # Track multi-source convergence
                    if substrate.temperature(ref) in ("cold", "cooling"):
                        node_sources[rid].add(f"depth_{d+1}")

    # C1 score = number of independent source paths reaching this node
    for nid in cold_zone:
        cold_zone[nid]["c1_sources"] = len(node_sources[nid])

    return cold_zone, warm_zone, deposits


# ── C2 — Velocity Classification ─────────────────────────────────────────────

def run_c2(cold_zone, substrate):
    """
    Classify cold nodes by functional mode using velocity.
    Gateway <200/yr | Protocol 200–1000/yr | Foundation >1000/yr
    """
    classified = {}
    for nid, node in cold_zone.items():
        vel = substrate.velocity(node)
        if vel is None:
            mode = "unclassified"
        elif vel < 200:
            mode = "Gateway"
        elif vel < 1000:
            mode = "Protocol"
        else:
            mode = "Foundation"
        classified[nid] = {**node, "velocity": vel, "mode": mode}
    return classified


# ── C3 — Connection Decay ─────────────────────────────────────────────────────

def run_c3(cold_zone, substrate, max_depth=4):
    """
    For each cold node: trace forward, measure influence at each hop.
    Mode-dependent: Gateway expands, Protocol closes, Foundation deepens.
    Returns decay profile per node.
    """
    profiles = {}
    for nid, node in cold_zone.items():
        mode  = node.get("mode", "unclassified")
        title = node.get("title", "")[:50]
        print(f"  C3 decay: {title} [{mode}]")

        hop_weights = []
        current_ids = {nid}
        visited     = {nid}

        for hop in range(1, max_depth + 1):
            next_ids    = set()
            total_weight = 0
            count        = 0

            for cid in current_ids:
                cites = substrate.citations(cid, limit=6)
                time.sleep(1.0)
                for cite in cites:
                    cid2 = cite.get("id") or cite.get("title")
                    if cid2 and cid2 not in visited:
                        next_ids.add(cid2)
                        visited.add(cid2)
                        total_weight += cite.get("weight", 0)
                        count += 1

            if count == 0:
                hop_weights.append({"hop": hop, "count": 0, "avg_weight": 0})
                break

            hop_weights.append({
                "hop": hop,
                "count": count,
                "avg_weight": round(total_weight / count, 1)
            })
            current_ids = next_ids

        # Classify decay pattern
        if len(hop_weights) >= 2:
            first = hop_weights[0]["count"]
            last  = hop_weights[-1]["count"]
            if last > first:
                decay_pattern = "amplifying"   # Gateway behavior
            elif last == 0:
                decay_pattern = "terminated"    # Protocol behavior
            else:
                decay_pattern = "decaying"      # Foundation behavior
        elif len(hop_weights) == 1 and hop_weights[0]["count"] == 0:
            decay_pattern = "pre-formation"
        else:
            decay_pattern = "unknown"

        profiles[nid] = {
            "title":   node.get("title","")[:60],
            "mode":    mode,
            "hops":    hop_weights,
            "pattern": decay_pattern,
        }

    return profiles


# ── C4 — Encounter Deposit ────────────────────────────────────────────────────

def run_c4(deposits, cold_zone, warm_zone):
    """
    Log what shifted during this traversal.
    Deposit shape encodes the mode of the depositing node.
    """
    c4_log = {
        "deposits":         deposits,
        "cold_nodes_found": len(cold_zone),
        "warm_nodes_found": len(warm_zone),
        "gateway_deposits": [d for d in deposits if "Gateway" in d],
        "foundation_deposits": [d for d in deposits if "Foundation" in d],
        "protocol_deposits": [d for d in deposits if "Protocol" in d],
        "note": "This run is an event in the substrate's history. Topology after != topology before."
    }
    return c4_log


# ── Output formatter ──────────────────────────────────────────────────────────

def service_function(mode):
    return {
        "Gateway":      "Names the condition — vocabulary for paradigm absence",
        "Foundation":   "Accepts the new floor — builds on the new substrate",
        "Protocol":     "Follows a procedure — acts within a known envelope",
        "Singularity":  "Creates the vocabulary that makes the problem perceivable",
        "unclassified": "Mode not yet determined — velocity data unavailable",
    }.get(mode, mode)


def decay_description(pattern):
    return {
        "amplifying":    "Expands across hops (Gateway behavior — cross-domain)",
        "terminated":    "Closes after 1–2 hops (Protocol behavior — local circuit)",
        "decaying":      "Deepens within domain, fades at boundary (Foundation behavior)",
        "pre-formation": "No forward path yet — function not assigned by space",
        "unknown":       "Insufficient data for pattern classification",
    }.get(pattern, pattern)


def format_output(seed_title, classified, c3_profiles, c4_log, warm_zone):
    lines = []
    lines.append("=" * 68)
    lines.append("CONTEXT SPACE — TOPOLOGY REPORT")
    lines.append(f"Seed: {seed_title}")
    lines.append(f"Run:  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M MST')}")
    lines.append("=" * 68)

    # Cold zone
    lines.append("\n── COLD ZONE ─────────────────────────────────────────────────")
    if not classified:
        lines.append("  No cold nodes discovered. Seed may be pre-formation or lag state.")
    for nid, node in sorted(classified.items(), key=lambda x: -(x[1].get("velocity") or 0)):
        title = node.get("title","")[:55]
        mode  = node.get("mode","?")
        vel   = node.get("velocity")
        year  = node.get("year","?")
        vel_s = f"{vel}/yr" if vel else "—"
        lines.append(f"\n  [{mode}] {title}")
        lines.append(f"  Year: {year} | Velocity: {vel_s}")
        lines.append(f"  Service: {service_function(mode)}")
        c1s = node.get("c1_sources", 1)
        lines.append(f"  C1 convergence: {c1s} independent path(s)")

    # Warm zone summary
    lines.append("\n── WARM ZONE (active frontier) ───────────────────────────────")
    if not warm_zone:
        lines.append("  No warm nodes found.")
    else:
        by_weight = sorted(warm_zone.values(), key=lambda x: -(x.get("weight") or 0))[:8]
        for node in by_weight:
            lines.append(f"  · {node.get('title','')[:60]} ({node.get('year','?')}, {node.get('weight',0)} cites)")

    # Exposed sections
    lines.append("\n── EXPOSED SECTIONS (no cold backing — hallucination risk) ───")
    exposed = [
        n for n in warm_zone.values()
        if n.get("weight", 0) > 200
    ]
    if not exposed:
        lines.append("  None detected at this depth.")
    for node in exposed[:5]:
        lines.append(f"  ⚠ {node.get('title','')[:60]} ({node.get('weight',0)} cites, warm, no cold anchor found)")

    # C3 decay profiles
    lines.append("\n── DECAY PROFILES (C3 — connection decay by path length) ────")
    if not c3_profiles:
        lines.append("  Not run (use --full for C3).")
    for nid, prof in c3_profiles.items():
        lines.append(f"\n  {prof['title']}")
        lines.append(f"  Mode: {prof['mode']} | Pattern: {decay_description(prof['pattern'])}")
        for hop in prof["hops"]:
            lines.append(f"    Hop {hop['hop']}: {hop['count']} nodes, avg weight {hop['avg_weight']}")

    # C4 deposit log
    lines.append("\n── DEPOSIT LOG (C4 — encounter deposit, no erasure) ─────────")
    lines.append(f"  Cold nodes found this run: {c4_log['cold_nodes_found']}")
    lines.append(f"  Warm nodes found this run: {c4_log['warm_nodes_found']}")
    lines.append(f"  Total deposits:            {len(c4_log['deposits'])}")
    lines.append(f"  Note: {c4_log['note']}")

    lines.append("\n" + "=" * 68)
    lines.append("Methodology: Assume nothing. Enforce nothing. Trust the substrate.")
    lines.append("github.com/kiheras11-cpu/context-space")
    lines.append("=" * 68)

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Context Space — topology reader. Minimum viable interface.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python context_space.py --seed "quantum error correction"
  python context_space.py --seed "Kuhn Structure of Scientific Revolutions" --depth 4
  python context_space.py --seed "your_paper.md" --substrate text
  python context_space.py --corpus my_corpus.json --full
        """
    )
    parser.add_argument("--seed",      type=str, help="Paper title, concept, or file path to start from")
    parser.add_argument("--corpus",    type=str, help="JSON file with list of {title, year, weight} nodes")
    parser.add_argument("--substrate", type=str, default="citation",
                        choices=["citation", "text"],
                        help="Substrate type (default: citation via SemanticScholar)")
    parser.add_argument("--direction", type=str, default="warm-to-cold",
                        choices=["warm-to-cold", "cold-to-warm", "both"],
                        help="Traversal direction (default: warm-to-cold)")
    parser.add_argument("--depth",     type=int, default=3,
                        help="Traversal depth (default: 3)")
    parser.add_argument("--full",      action="store_true",
                        help="Run C3 decay profiles (slower — additional API calls)")
    parser.add_argument("--output",    type=str, default=None,
                        help="Write report to file (default: stdout)")
    args = parser.parse_args()

    if not args.seed and not args.corpus:
        parser.print_help()
        sys.exit(0)

    # Build substrate
    if args.substrate == "text":
        if not args.seed:
            print("[error] --substrate text requires --seed <file or directory>")
            sys.exit(1)
        substrate = TextSubstrate(args.seed)
        seed_node = substrate.find(args.seed)
    else:
        substrate = CitationSubstrate()
        if args.seed:
            print(f"[searching] '{args.seed}' ...")
            seed_node = substrate.find(args.seed)
        elif args.corpus:
            with open(args.corpus) as f:
                corpus = json.load(f)
            seed_node = corpus[0] if corpus else None

    if not seed_node:
        print(f"[error] Could not find seed: '{args.seed}'")
        sys.exit(1)

    print(f"[seed found] {seed_node.get('title','?')} ({seed_node.get('year','?')}, {seed_node.get('weight',0)} cites)")

    # Run constants
    deposits = []
    cold_zone, warm_zone, deposits = run_c1(seed_node, substrate, depth=args.depth, deposits=deposits)

    print(f"\n[C1 complete] Cold: {len(cold_zone)} | Warm: {len(warm_zone)}")

    classified = run_c2(cold_zone, substrate)
    print(f"[C2 complete] Modes: { {v['mode'] for v in classified.values()} }")

    c3_profiles = {}
    if args.full:
        print("\n[C3 running] Decay profiles ...")
        c3_profiles = run_c3(classified, substrate)

    c4_log = run_c4(deposits, cold_zone, warm_zone)

    # Format and output
    report = format_output(
        seed_node.get("title", args.seed),
        classified,
        c3_profiles,
        c4_log,
        warm_zone
    )

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"\n[report saved] {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
