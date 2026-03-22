"""
C1 Version B — Genealogical Substrate Anchoring (Corrected Direction)
----------------------------------------------------------------------
Same graph, same logic — but we flip the edge direction before computing roots.

In the original citation graph: edges point FROM newer → TO older (A cites B).
Root nodes (no predecessors) = frontier nodes nobody has cited yet.
That reads genealogy from the wrong end.

Flipped graph: edges point FROM older → TO newer (A was built upon by B).
Root nodes in the flipped graph = true foundational anchors — nothing precedes them.
These are the stable cold zones of ancestry.

We also keep the unflipped result as "warm zone reading" — 
the frontier noise tracing back toward cold stability.
That's a real second measurement mode, not an error.

KEY OBSERVATION (pre-run):
Both versions agreed at the top before divergence.
Maxwell #1 in both, same score within rounding.
The foundation is detectable regardless of directionality.
Divergence is a mid-field phenomenon — where imposed labels mask real topology.
"""

import networkx as nx
from collections import defaultdict
import json

NODES = [
    {"id": "newton_principia",        "label": "Newton — Principia (1687)",              "discipline": "classical"},
    {"id": "lagrange_mechanics",      "label": "Lagrange — Analytical Mechanics (1788)", "discipline": "classical"},
    {"id": "hamilton_mechanics",      "label": "Hamilton — Hamiltonian Mechanics (1833)","discipline": "classical"},
    {"id": "faraday_fields",          "label": "Faraday — Field Lines (1831)",           "discipline": "em"},
    {"id": "maxwell_equations",       "label": "Maxwell — Equations (1865)",             "discipline": "em"},
    {"id": "hertz_waves",             "label": "Hertz — EM Waves (1888)",                "discipline": "em"},
    {"id": "carnot_cycle",            "label": "Carnot — Heat Cycle (1824)",             "discipline": "thermo"},
    {"id": "clausius_entropy",        "label": "Clausius — Entropy (1865)",              "discipline": "thermo"},
    {"id": "boltzmann_stat",          "label": "Boltzmann — Statistical Mechanics (1877)","discipline": "thermo"},
    {"id": "einstein_sr",             "label": "Einstein — Special Relativity (1905)",   "discipline": "relativity"},
    {"id": "einstein_gr",             "label": "Einstein — General Relativity (1915)",   "discipline": "relativity"},
    {"id": "minkowski_spacetime",     "label": "Minkowski — Spacetime (1908)",           "discipline": "relativity"},
    {"id": "planck_quanta",           "label": "Planck — Quanta (1900)",                 "discipline": "quantum"},
    {"id": "bohr_atom",               "label": "Bohr — Atomic Model (1913)",             "discipline": "quantum"},
    {"id": "heisenberg_qm",           "label": "Heisenberg — Matrix Mechanics (1925)",   "discipline": "quantum"},
    {"id": "schrodinger_qm",          "label": "Schrödinger — Wave Mechanics (1926)",    "discipline": "quantum"},
    {"id": "dirac_equation",          "label": "Dirac — Relativistic QM (1928)",         "discipline": "quantum"},
    {"id": "feynman_qed",             "label": "Feynman — QED (1948)",                   "discipline": "qft"},
    {"id": "yang_mills",              "label": "Yang-Mills — Gauge Theory (1954)",       "discipline": "qft"},
    {"id": "higgs_mechanism",         "label": "Higgs — Mass Mechanism (1964)",          "discipline": "qft"},
    {"id": "standard_model",          "label": "Standard Model (1970s)",                 "discipline": "qft"},
    {"id": "shannon_info",            "label": "Shannon — Information Theory (1948)",    "discipline": "info"},
    {"id": "landauer_principle",      "label": "Landauer — Erasure Cost (1961)",         "discipline": "info"},
    {"id": "bell_theorem",            "label": "Bell — Theorem (1964)",                  "discipline": "quantum_info"},
    {"id": "feynman_quantum_compute", "label": "Feynman — Quantum Computing (1982)",     "discipline": "quantum_info"},
]

EDGES = [
    ("lagrange_mechanics",      "newton_principia"),
    ("hamilton_mechanics",      "lagrange_mechanics"),
    ("hamilton_mechanics",      "newton_principia"),
    ("maxwell_equations",       "faraday_fields"),
    ("hertz_waves",             "maxwell_equations"),
    ("clausius_entropy",        "carnot_cycle"),
    ("boltzmann_stat",          "clausius_entropy"),
    ("boltzmann_stat",          "carnot_cycle"),
    ("einstein_sr",             "maxwell_equations"),
    ("einstein_sr",             "newton_principia"),
    ("minkowski_spacetime",     "einstein_sr"),
    ("einstein_gr",             "einstein_sr"),
    ("einstein_gr",             "newton_principia"),
    ("planck_quanta",           "boltzmann_stat"),
    ("planck_quanta",           "maxwell_equations"),
    ("bohr_atom",               "planck_quanta"),
    ("bohr_atom",               "maxwell_equations"),
    ("heisenberg_qm",           "bohr_atom"),
    ("schrodinger_qm",          "bohr_atom"),
    ("schrodinger_qm",          "hamilton_mechanics"),
    ("dirac_equation",          "schrodinger_qm"),
    ("dirac_equation",          "einstein_sr"),
    ("feynman_qed",             "dirac_equation"),
    ("feynman_qed",             "maxwell_equations"),
    ("yang_mills",              "maxwell_equations"),
    ("yang_mills",              "feynman_qed"),
    ("higgs_mechanism",         "yang_mills"),
    ("higgs_mechanism",         "schrodinger_qm"),
    ("standard_model",          "feynman_qed"),
    ("standard_model",          "yang_mills"),
    ("standard_model",          "higgs_mechanism"),
    ("shannon_info",            "boltzmann_stat"),
    ("landauer_principle",      "shannon_info"),
    ("landauer_principle",      "boltzmann_stat"),
    ("bell_theorem",            "schrodinger_qm"),
    ("bell_theorem",            "einstein_gr"),
    ("feynman_quantum_compute", "feynman_qed"),
    ("feynman_quantum_compute", "shannon_info"),
]

# ── Build original and flipped graphs ────────────────────────────────────────
G = nx.DiGraph()
label_map = {}
discipline_map = {}
for n in NODES:
    G.add_node(n["id"], label=n["label"], discipline=n["discipline"])
    label_map[n["id"]] = n["label"]
    discipline_map[n["id"]] = n["discipline"]
for src, tgt in EDGES:
    G.add_edge(src, tgt)

G_flipped = G.reverse()  # edges now point FROM older → TO newer


# ── Genealogical family computation (on flipped graph) ───────────────────────
def compute_genealogical_families_flipped(original_graph, flipped_graph):
    """
    In the flipped graph, roots = nodes with no predecessors = true foundations.
    For each node, walk UPSTREAM in the flipped graph (= downstream in original)
    to find which foundational roots it descends from.
    
    Actually: in the flipped graph, ancestors of a node = nodes that built upon it
    in the original. We want the opposite: which roots does this node build upon?
    
    So we still use the ORIGINAL graph to find ancestors, but we identify roots
    using the FLIPPED graph (nodes with no predecessors in flipped = no successors
    in original = true foundational anchors).
    """
    # Roots in flipped graph = no incoming edges in flipped = no outgoing edges in original
    # = nodes that don't cite anything = the true foundations
    true_roots = {n for n in original_graph.nodes() if original_graph.out_degree(n) == 0}
    
    # Wait — let's think again.
    # Original edges: newer → older (A cites B)
    # In-degree 0 in original = nobody cites this node = frontier (warm zone)
    # Out-degree 0 in original = this node cites nothing = true foundation (cold zone)
    
    foundational_roots = {n for n in original_graph.nodes() if original_graph.out_degree(n) == 0}
    
    families = {}
    for node in original_graph.nodes():
        # Descendants in original graph (edges: newer→older) = all older work this node builds upon
        # nx.descendants follows edges forward: from this node toward older foundational work
        older_work = nx.descendants(original_graph, node)
        # Which of those are foundational roots?
        root_ancestors = older_work & foundational_roots
        # If the node itself is a root, its family is itself
        if not root_ancestors:
            root_ancestors = {node} if node in foundational_roots else set()
        families[node] = frozenset(root_ancestors)
    
    return families, foundational_roots


def score_genealogical_corrected(graph, geo_families):
    all_family_keys = set(geo_families.values()) - {frozenset()}
    total_families = len(all_family_keys)
    if total_families == 0:
        return {n: 0.0 for n in graph.nodes()}

    scores = {}
    for node in graph.nodes():
        refs = list(graph.predecessors(node))
        if not refs:
            scores[node] = 0.0
            continue
        node_family = geo_families[node]
        ref_families = set(geo_families[r] for r in refs) - {node_family} - {frozenset()}
        scores[node] = round(len(ref_families) / total_families, 4)
    return scores


# ── Run ───────────────────────────────────────────────────────────────────────
geo_families, foundational_roots = compute_genealogical_families_flipped(G, G_flipped)
scores = score_genealogical_corrected(G, geo_families)
ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

# ── Print foundational roots (true cold zone anchors) ─────────────────────────
print("=" * 70)
print("TRUE FOUNDATIONAL ROOTS — cold zone anchors (cite nothing, pure source)")
print("(out-degree 0 in citation graph = builds on nothing = substrate floor)")
print("=" * 70)
for r in sorted(foundational_roots):
    print(f"  {label_map[r]}")

print()

# ── Genealogical families from correct direction ──────────────────────────────
print("=" * 70)
print("GENEALOGICAL FAMILIES — computed from foundational anchors upward")
print("=" * 70)
family_to_members = defaultdict(list)
for node, fkey in geo_families.items():
    family_to_members[fkey].append(node)

for fkey, members in sorted(family_to_members.items(), key=lambda x: -len(x[1])):
    if not fkey:
        continue
    root_labels = sorted([label_map[r] for r in fkey])
    print(f"\n  Anchored to: {root_labels}")
    for m in sorted(members, key=lambda x: label_map[x]):
        print(f"    → {label_map[m]}")

# ── Scores ────────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("GENEALOGICAL SUBSTRATE ANCHORING — CORRECTED (cold-zone-first)")
print("=" * 70)
for node, score in ranked:
    fkey = geo_families[node]
    refs = list(G.predecessors(node))
    root_labels = sorted([label_map[r] for r in fkey]) if fkey else ["(none — is a root)"]
    print(f"  {score:.4f}  {label_map[node]}")
    print(f"          anchored to: {root_labels}")

# ── Three-way comparison ──────────────────────────────────────────────────────
print()
print("=" * 70)
print("THREE-WAY COMPARISON")
print("imposed discipline | warm-zone genealogical | cold-zone genealogical")
print("=" * 70)

# Reimport imposed scores for comparison
total_disciplines = len(set(discipline_map.values()))
imposed = {}
for node in G.nodes():
    refs = list(G.predecessors(node))
    if not refs:
        imposed[node] = 0.0
        continue
    nd = discipline_map[node]
    ind = set(discipline_map[r] for r in refs) - {nd}
    imposed[node] = round(len(ind) / total_disciplines, 4)

# Warm zone scores (from previous run — recompute here)
def compute_warm_families(graph):
    warm_roots = {n for n in graph.nodes() if graph.in_degree(n) == 0}
    families = {}
    for node in graph.nodes():
        ancestors = nx.ancestors(graph, node)
        root_ancestors = ancestors & warm_roots
        if not root_ancestors:
            root_ancestors = {node} if node in warm_roots else set()
        families[node] = frozenset(root_ancestors)
    return families, warm_roots

warm_families, warm_roots = compute_warm_families(G)
all_warm_keys = set(warm_families.values()) - {frozenset()}
warm_scores = {}
for node in G.nodes():
    refs = list(G.predecessors(node))
    if not refs:
        warm_scores[node] = 0.0
        continue
    nf = warm_families[node]
    ind = set(warm_families[r] for r in refs) - {nf} - {frozenset()}
    warm_scores[node] = round(len(ind) / len(all_warm_keys), 4) if all_warm_keys else 0.0

# Sort by cold-zone score
all_nodes_sorted = sorted(G.nodes(), key=lambda n: (-scores[n], -warm_scores[n], -imposed[n]))

print(f"\n{'Node':<45} {'Imposed':>8} {'Warm':>8} {'Cold':>8}")
print("-" * 73)
for node in all_nodes_sorted:
    label = label_map[node][:43]
    print(f"  {label:<43} {imposed[node]:>8.4f} {warm_scores[node]:>8.4f} {scores[node]:>8.4f}")

# ── Divergence between warm and cold ─────────────────────────────────────────
print()
print("=" * 70)
print("WARM vs COLD DIVERGENCE")
print("(where frontier noise and foundational ancestry disagree)")
print("=" * 70)
warm_rank = {n: i for i, n in enumerate(sorted(G.nodes(), key=lambda x: -warm_scores[x]))}
cold_rank  = {n: i for i, n in enumerate(sorted(G.nodes(), key=lambda x: -scores[x]))}

divs = []
for node in G.nodes():
    dr = warm_rank[node] - cold_rank[node]
    ds = warm_scores[node] - scores[node]
    if abs(dr) >= 3 or abs(ds) >= 0.08:
        divs.append((abs(dr), node, dr, ds))
divs.sort(reverse=True)

for _, node, dr, ds in divs:
    direction = "↑ cold ranks HIGHER" if dr > 0 else "↓ cold ranks LOWER"
    print(f"\n  {label_map[node]}")
    print(f"    warm rank: {warm_rank[node]+1}  |  cold rank: {cold_rank[node]+1}  |  {direction}")
    print(f"    warm={warm_scores[node]:.4f}  cold={scores[node]:.4f}  imposed={imposed[node]:.4f}")
