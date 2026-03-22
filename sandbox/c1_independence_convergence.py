"""
Constant #1 — Independence Convergence
---------------------------------------
A node's coherence = number of independent, non-coordinating sources that reference it.
Coordination proxy: if two sources share a common upstream reference, they are not independent.

We run this on a hand-curated 25-node physics graph.
We do NOT assume what will emerge. We observe.

Output: coherence score per node. Then we look at what the scores are telling us.
"""

import networkx as nx
import json

# ── Hand-curated seed graph ──────────────────────────────────────────────────
# Nodes: foundational physics ideas/papers
# Edges: directed, A → B means "A references or builds on B"
# Source tagging: each node is assigned a 'family' (coordinating cluster)
#   Nodes in the same family share upstream references = not independent from each other

NODES = [
    # Classical mechanics family
    {"id": "newton_principia",       "label": "Newton — Principia (1687)",              "family": "classical"},
    {"id": "lagrange_mechanics",     "label": "Lagrange — Analytical Mechanics (1788)", "family": "classical"},
    {"id": "hamilton_mechanics",     "label": "Hamilton — Hamiltonian Mechanics (1833)","family": "classical"},

    # Electromagnetism family
    {"id": "faraday_fields",         "label": "Faraday — Field Lines (1831)",           "family": "em"},
    {"id": "maxwell_equations",      "label": "Maxwell — Equations (1865)",             "family": "em"},
    {"id": "hertz_waves",            "label": "Hertz — EM Waves (1888)",                "family": "em"},

    # Thermodynamics family
    {"id": "carnot_cycle",           "label": "Carnot — Heat Cycle (1824)",             "family": "thermo"},
    {"id": "clausius_entropy",       "label": "Clausius — Entropy (1865)",              "family": "thermo"},
    {"id": "boltzmann_stat",         "label": "Boltzmann — Statistical Mechanics (1877)","family": "thermo"},

    # Relativity family
    {"id": "einstein_sr",            "label": "Einstein — Special Relativity (1905)",   "family": "relativity"},
    {"id": "einstein_gr",            "label": "Einstein — General Relativity (1915)",   "family": "relativity"},
    {"id": "minkowski_spacetime",    "label": "Minkowski — Spacetime (1908)",           "family": "relativity"},

    # Quantum family
    {"id": "planck_quanta",          "label": "Planck — Quanta (1900)",                "family": "quantum"},
    {"id": "bohr_atom",              "label": "Bohr — Atomic Model (1913)",            "family": "quantum"},
    {"id": "heisenberg_qm",          "label": "Heisenberg — Matrix Mechanics (1925)",  "family": "quantum"},
    {"id": "schrodinger_qm",         "label": "Schrödinger — Wave Mechanics (1926)",   "family": "quantum"},
    {"id": "dirac_equation",         "label": "Dirac — Relativistic QM (1928)",        "family": "quantum"},

    # QFT / Unification family
    {"id": "feynman_qed",            "label": "Feynman — QED (1948)",                  "family": "qft"},
    {"id": "yang_mills",             "label": "Yang-Mills — Gauge Theory (1954)",      "family": "qft"},
    {"id": "higgs_mechanism",        "label": "Higgs — Mass Mechanism (1964)",         "family": "qft"},
    {"id": "standard_model",         "label": "Standard Model (1970s)",                "family": "qft"},

    # Information / Statistical bridges — cross-family nodes
    {"id": "shannon_info",           "label": "Shannon — Information Theory (1948)",   "family": "info"},
    {"id": "landauer_principle",     "label": "Landauer — Erasure Cost (1961)",        "family": "info"},
    {"id": "bell_theorem",           "label": "Bell — Theorem (1964)",                 "family": "quantum_info"},
    {"id": "feynman_quantum_compute","label": "Feynman — Quantum Computing (1982)",    "family": "quantum_info"},
]

# Directed edges: A → B means A references/builds on B
EDGES = [
    # Classical chain
    ("lagrange_mechanics",   "newton_principia"),
    ("hamilton_mechanics",   "lagrange_mechanics"),
    ("hamilton_mechanics",   "newton_principia"),

    # EM chain
    ("maxwell_equations",    "faraday_fields"),
    ("hertz_waves",          "maxwell_equations"),

    # Thermo chain
    ("clausius_entropy",     "carnot_cycle"),
    ("boltzmann_stat",       "clausius_entropy"),
    ("boltzmann_stat",       "carnot_cycle"),

    # Relativity
    ("einstein_sr",          "maxwell_equations"),
    ("einstein_sr",          "newton_principia"),
    ("minkowski_spacetime",  "einstein_sr"),
    ("einstein_gr",          "einstein_sr"),
    ("einstein_gr",          "newton_principia"),

    # Quantum
    ("planck_quanta",        "boltzmann_stat"),
    ("planck_quanta",        "maxwell_equations"),
    ("bohr_atom",            "planck_quanta"),
    ("bohr_atom",            "maxwell_equations"),
    ("heisenberg_qm",        "bohr_atom"),
    ("schrodinger_qm",       "bohr_atom"),
    ("schrodinger_qm",       "hamilton_mechanics"),   # cross-family bridge
    ("dirac_equation",       "schrodinger_qm"),
    ("dirac_equation",       "einstein_sr"),          # cross-family bridge

    # QFT
    ("feynman_qed",          "dirac_equation"),
    ("feynman_qed",          "maxwell_equations"),    # cross-family bridge
    ("yang_mills",           "maxwell_equations"),    # cross-family bridge
    ("yang_mills",           "feynman_qed"),
    ("higgs_mechanism",      "yang_mills"),
    ("higgs_mechanism",      "schrodinger_qm"),       # cross-family bridge
    ("standard_model",       "feynman_qed"),
    ("standard_model",       "yang_mills"),
    ("standard_model",       "higgs_mechanism"),

    # Info bridges
    ("shannon_info",         "boltzmann_stat"),       # cross-family bridge
    ("landauer_principle",   "shannon_info"),
    ("landauer_principle",   "boltzmann_stat"),       # cross-family bridge

    # Quantum info
    ("bell_theorem",         "schrodinger_qm"),
    ("bell_theorem",         "einstein_gr"),          # EPR cross-family
    ("feynman_quantum_compute", "feynman_qed"),
    ("feynman_quantum_compute", "shannon_info"),      # cross-family bridge
]

# ── Build graph ───────────────────────────────────────────────────────────────
G = nx.DiGraph()
family_map = {}
for n in NODES:
    G.add_node(n["id"], label=n["label"], family=n["family"])
    family_map[n["id"]] = n["family"]

for src, tgt in EDGES:
    G.add_edge(src, tgt)

# ── Constant #1: Independence Convergence ─────────────────────────────────────
# For each node N, find all nodes that reference it (in-edges).
# Count only references from DIFFERENT families → independent sources.
# Nodes in the same family share upstream → coordinated → don't count.

def independence_convergence(graph, family_map):
    scores = {}
    for node in graph.nodes():
        referencing_nodes = list(graph.predecessors(node))
        if not referencing_nodes:
            scores[node] = 0.0
            continue

        # Group referencing nodes by family
        families_seen = set()
        for ref in referencing_nodes:
            families_seen.add(family_map[ref])

        # Independent count = number of distinct families referencing this node
        # (excluding the node's own family — same-family refs are coordinated)
        node_family = family_map[node]
        independent_families = families_seen - {node_family}

        # Raw score: independent family count / total possible families
        total_families = len(set(family_map.values()))
        score = len(independent_families) / total_families

        scores[node] = round(score, 4)

    return scores

scores = independence_convergence(G, family_map)

# ── Sort and display ──────────────────────────────────────────────────────────
ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

print("=" * 65)
print("CONSTANT #1 — INDEPENDENCE CONVERGENCE")
print("Coherence score = independent-family references / total families")
print("=" * 65)
print()

for node_id, score in ranked:
    label = G.nodes[node_id]["label"]
    family = family_map[node_id]
    preds = list(G.predecessors(node_id))
    ind_families = set(family_map[p] for p in preds) - {family}
    print(f"  {score:.4f}  {label}")
    print(f"          family={family} | in-refs={len(preds)} | independent families={sorted(ind_families)}")
    print()

# ── What to look for ─────────────────────────────────────────────────────────
print("=" * 65)
print("OBSERVATIONS — what is the output actually telling us?")
print("=" * 65)
high = [(n, s) for n, s in ranked if s >= 0.25]
zero = [(n, s) for n, s in ranked if s == 0.0]
print(f"\nHigh convergence nodes (score >= 0.25): {len(high)}")
for n, s in high:
    print(f"  {s:.4f}  {G.nodes[n]['label']}")

print(f"\nZero convergence nodes (no cross-family references): {len(zero)}")
for n, s in zero:
    print(f"  {s:.4f}  {G.nodes[n]['label']}")

print()
print("RAW SCORES JSON:")
print(json.dumps({G.nodes[n]["label"]: s for n, s in ranked}, indent=2))
