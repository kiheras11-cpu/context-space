"""
C1 Comparison — Imposed Discipline vs Genealogical Substrate Anchoring
-----------------------------------------------------------------------

Two versions of Constant #1 run on the same 25-node physics graph.

VERSION A — Imposed Discipline
  Family membership is assigned externally (classical, em, thermo, etc.)
  Independence = reference comes from a different labeled discipline.
  This is how humans organized physics institutionally.

VERSION B — Genealogical Substrate Anchoring
  Family membership is computed from the graph topology alone.
  A node's family = the set of root ancestors it descends from.
  Nodes that share the same root ancestry are in the same genealogical family.
  No external label. The graph decides.

The divergence between A and B is the finding.
"""

import networkx as nx
from collections import defaultdict
import json

# ── Seed graph (same as c1_independence_convergence.py) ──────────────────────

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

# ── Build graph ───────────────────────────────────────────────────────────────
G = nx.DiGraph()
discipline_map = {}
label_map = {}
for n in NODES:
    G.add_node(n["id"], label=n["label"], discipline=n["discipline"])
    discipline_map[n["id"]] = n["discipline"]
    label_map[n["id"]] = n["label"]

for src, tgt in EDGES:
    G.add_edge(src, tgt)


# ── VERSION A: Imposed Discipline ─────────────────────────────────────────────
def score_imposed(graph, discipline_map):
    scores = {}
    total_disciplines = len(set(discipline_map.values()))
    for node in graph.nodes():
        refs = list(graph.predecessors(node))
        if not refs:
            scores[node] = 0.0
            continue
        node_disc = discipline_map[node]
        independent_discs = set(discipline_map[r] for r in refs) - {node_disc}
        scores[node] = round(len(independent_discs) / total_disciplines, 4)
    return scores


# ── VERSION B: Genealogical Substrate Anchoring ───────────────────────────────
# Root nodes = no incoming edges (no predecessors) — they are the substrate anchors
# For each node, compute its full ancestor set (all roots reachable going upstream)
# Genealogical family = frozenset of root ancestors
# Two nodes are in the same family if they share identical root ancestry
# Independence = references come from nodes with DIFFERENT root ancestry

def get_all_ancestors(graph, node):
    """Return all ancestor node IDs reachable upstream from node."""
    return nx.ancestors(graph, node)

def compute_genealogical_families(graph):
    """
    For each node, find all root ancestors (nodes with no predecessors).
    A node's genealogical family key = frozenset of root ancestors it descends from.
    """
    roots = {n for n in graph.nodes() if graph.in_degree(n) == 0}
    families = {}
    for node in graph.nodes():
        ancestors = get_all_ancestors(graph, node)
        root_ancestors = ancestors & roots
        # If the node IS a root, its family key is itself
        if not root_ancestors:
            root_ancestors = {node}
        families[node] = frozenset(root_ancestors)
    return families, roots

def score_genealogical(graph, geo_families):
    scores = {}
    all_family_keys = set(geo_families.values())
    total_families = len(all_family_keys)

    for node in graph.nodes():
        refs = list(graph.predecessors(node))
        if not refs:
            scores[node] = 0.0
            continue
        node_family = geo_families[node]
        independent_families = set(geo_families[r] for r in refs) - {node_family}
        scores[node] = round(len(independent_families) / total_families, 4)
    return scores


# ── Run both ──────────────────────────────────────────────────────────────────
scores_a = score_imposed(G, discipline_map)
geo_families, roots = compute_genealogical_families(G)
scores_b = score_genealogical(G, geo_families)

ranked_a = sorted(scores_a.items(), key=lambda x: x[1], reverse=True)
ranked_b = sorted(scores_b.items(), key=lambda x: x[1], reverse=True)


# ── Print root nodes (the substrate anchors) ──────────────────────────────────
print("=" * 70)
print("GENEALOGICAL ROOT NODES (no predecessors — pure substrate anchors)")
print("=" * 70)
for r in sorted(roots):
    print(f"  {label_map[r]}  (family key: self)")
print()

# Show unique genealogical families discovered
print("=" * 70)
print("GENEALOGICAL FAMILIES — emerged from topology")
print("(each unique frozenset of root ancestors = one family)")
print("=" * 70)
family_to_members = defaultdict(list)
for node, fkey in geo_families.items():
    family_to_members[fkey].append(node)

for fkey, members in sorted(family_to_members.items(), key=lambda x: -len(x[1])):
    root_labels = [label_map[r] for r in fkey]
    print(f"\n  Roots: {root_labels}")
    for m in members:
        print(f"    → {label_map[m]}")


# ── Side-by-side ranking ──────────────────────────────────────────────────────
print()
print("=" * 70)
print("VERSION A — IMPOSED DISCIPLINE SCORES")
print("=" * 70)
for node, score in ranked_a:
    disc = discipline_map[node]
    refs = list(G.predecessors(node))
    ind = set(discipline_map[r] for r in refs) - {disc}
    print(f"  {score:.4f}  {label_map[node]}")
    print(f"          discipline={disc} | independent disciplines={sorted(ind)}")

print()
print("=" * 70)
print("VERSION B — GENEALOGICAL SUBSTRATE ANCHORING SCORES")
print("=" * 70)
for node, score in ranked_b:
    fkey = geo_families[node]
    refs = list(G.predecessors(node))
    ind = set(geo_families[r] for r in refs) - {fkey}
    print(f"  {score:.4f}  {label_map[node]}")
    root_labels = [label_map[r] for r in fkey]
    print(f"          roots={root_labels} | independent genealogies={len(ind)}")


# ── Divergence report — where the two versions disagree ──────────────────────
print()
print("=" * 70)
print("DIVERGENCE — where imposed and genealogical rankings disagree")
print("(these are the nodes the substrate is saying something different about)")
print("=" * 70)

rank_a = {n: i for i, (n, _) in enumerate(ranked_a)}
rank_b = {n: i for i, (n, _) in enumerate(ranked_b)}

divergences = []
for node in G.nodes():
    delta_rank = rank_a[node] - rank_b[node]
    delta_score = scores_a[node] - scores_b[node]
    if abs(delta_rank) >= 3 or abs(delta_score) >= 0.1:
        divergences.append((abs(delta_rank), node, delta_rank, delta_score))

divergences.sort(reverse=True)
if divergences:
    for _, node, dr, ds in divergences:
        direction = "↑ substrate ranks HIGHER" if dr > 0 else "↓ substrate ranks LOWER"
        print(f"\n  {label_map[node]}")
        print(f"    imposed rank: {rank_a[node]+1}  |  genealogical rank: {rank_b[node]+1}  |  {direction}")
        print(f"    score delta: imposed={scores_a[node]:.4f}  genealogical={scores_b[node]:.4f}")
else:
    print("  No significant divergences detected — the two framings agree on this graph.")

print()
print("=" * 70)
print("RAW SCORES — both versions")
print("=" * 70)
print(json.dumps({
    label_map[n]: {"imposed": scores_a[n], "genealogical": scores_b[n]}
    for n in G.nodes()
}, indent=2))
