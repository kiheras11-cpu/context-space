"""
Unified C1 + C2 Analysis
─────────────────────────
All research corpora merged:
  - Context Space API scout runs (96 nodes)
  - Quantum OS internal citations (27 papers)
  - Bioelectric Protocol research cluster
  - Cross-domain entropy cluster (hydrology, military)

C1: Independence Convergence — cross-source weight (how many distinct
    research tracks reference this paper)
C2: Velocity Classification — citations/year → Gateway / Protocol / Foundation

No prior commitment to outcome.
"""

from collections import defaultdict

current_year = 2026.25

unified = [

    # ── EPISTEMOLOGICAL ───────────────────────────────────────────
    {'title': 'The Structure of Scientific Revolutions',
     'author': 'Kuhn', 'year': 1962, 'citations': 7144, 'domain': 'epistemology',
     'sources': ['context_space', 'organizational_change', 'nursing', 'hydrology', 'qft', 'leadership', 'conflict_studies']},

    {'title': 'The Essential Tension',
     'author': 'Kuhn_1977', 'year': 1977, 'citations': 960, 'domain': 'epistemology',
     'sources': ['context_space']},

    # ── METHODOLOGY ───────────────────────────────────────────────
    {'title': 'Preferred Reporting Items for Systematic Reviews PRISMA',
     'author': 'Moher_et_al', 'year': 2015, 'citations': 15680, 'domain': 'methodology',
     'sources': ['context_space', 'leadership_theory', 'medicine']},

    # ── AI / LLM ──────────────────────────────────────────────────
    {'title': 'GPT-4 Technical Report',
     'author': 'OpenAI', 'year': 2023, 'citations': 22948, 'domain': 'ai_llm',
     'sources': ['context_space', 'ai_applications', 'education', 'organizational_change']},

    {'title': 'Retrieval-Augmented Generation for Large Language Models Survey',
     'author': 'Gao_et_al', 'year': 2023, 'citations': 3027, 'domain': 'ai_llm',
     'sources': ['context_space']},

    {'title': 'RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval',
     'author': 'Sarthi_et_al', 'year': 2024, 'citations': 369, 'domain': 'ai_llm',
     'sources': ['context_space']},

    # ── ORGANIZATIONAL CHANGE ─────────────────────────────────────
    {'title': 'Leading Change',
     'author': 'Kotter', 'year': 2012, 'citations': 4317, 'domain': 'organizational_change',
     'sources': ['context_space', 'medicine', 'education', 'engineering', 'business']},

    {'title': 'The Heart of Change',
     'author': 'Kotter_Cohen', 'year': 2002, 'citations': 840, 'domain': 'organizational_change',
     'sources': ['context_space', 'organizational_change']},

    {'title': 'Unpacking organizational readiness for change',
     'author': 'Galli', 'year': 2020, 'citations': 128, 'domain': 'organizational_change',
     'sources': ['context_space']},

    {'title': 'Sustainable development colors of sustainable leadership',
     'author': 'Sustainability_Leadership', 'year': 2020, 'citations': 200,
     'domain': 'leadership_sustainability', 'sources': ['context_space']},

    {'title': 'Green transformational leadership and value-action barrier',
     'author': 'Green_Leadership', 'year': 2026, 'citations': 1,
     'domain': 'leadership_sustainability', 'sources': ['context_space']},

    # ── QUANTUM HARDWARE FRONTIER (API scout) ─────────────────────
    {'title': 'Logical quantum processor based on reconfigurable atom arrays',
     'author': 'Evered_et_al', 'year': 2023, 'citations': 1314, 'domain': 'quantum_hardware',
     'sources': ['context_space_physics_seed']},

    {'title': 'High-threshold and low-overhead fault-tolerant quantum memory',
     'author': 'Bluvstein_et_al', 'year': 2023, 'citations': 598, 'domain': 'quantum_hardware',
     'sources': ['context_space_physics_seed']},

    {'title': 'Universal control of a six-qubit quantum processor in silicon',
     'author': 'Philips_et_al', 'year': 2022, 'citations': 408, 'domain': 'quantum_hardware',
     'sources': ['context_space_physics_seed']},

    {'title': 'Fault-tolerant control of an error-corrected qubit',
     'author': 'Ryananderson_et_al', 'year': 2021, 'citations': 356, 'domain': 'quantum_hardware',
     'sources': ['context_space_physics_seed']},

    {'title': 'Sparse Blossom correcting a million errors per core second',
     'author': 'Higgott_Gidney', 'year': 2023, 'citations': 294, 'domain': 'quantum_hardware',
     'sources': ['context_space_physics_seed']},

    {'title': 'Shared control of a 16 semiconductor quantum dot crossbar array',
     'author': 'Borsoi_et_al', 'year': 2022, 'citations': 169, 'domain': 'quantum_hardware',
     'sources': ['context_space_physics_seed']},

    # ── QUANTUM OS FOUNDATIONS ────────────────────────────────────
    {'title': 'Quantum Computation and Quantum Information',
     'author': 'Nielsen_Chuang', 'year': 2000, 'citations': 42000, 'domain': 'quantum_foundations',
     'sources': ['quantum_os', 'quantum_hardware_research']},

    {'title': 'Irreversibility and heat generation in the computing process',
     'author': 'Landauer', 'year': 1961, 'citations': 11000, 'domain': 'thermodynamics_info',
     'sources': ['quantum_os', 'information_theory', 'cs_theory']},

    {'title': 'Space-time approach to non-relativistic quantum mechanics',
     'author': 'Feynman_1948', 'year': 1948, 'citations': 8500, 'domain': 'quantum_physics',
     'sources': ['quantum_os', 'quantum_foundations']},

    {'title': 'The Emperors New Mind',
     'author': 'Penrose_1989', 'year': 1989, 'citations': 18000, 'domain': 'consciousness',
     'sources': ['quantum_os', 'philosophy_mind', 'ai_consciousness']},

    {'title': 'Wave-function approach to dissipative processes in quantum optics',
     'author': 'Dalibard_Castin_Molmer', 'year': 1992, 'citations': 9500, 'domain': 'quantum_physics',
     'sources': ['quantum_os', 'quantum_optics']},

    {'title': 'Monte Carlo wave-function method in quantum optics',
     'author': 'Molmer_Castin_Dalibard', 'year': 1993, 'citations': 5800, 'domain': 'quantum_physics',
     'sources': ['quantum_os']},

    {'title': 'How the result of a measurement of spin can turn out to be 100',
     'author': 'Aharonov_Albert_Vaidman', 'year': 1988, 'citations': 5200, 'domain': 'quantum_physics',
     'sources': ['quantum_os', 'quantum_measurement']},

    {'title': 'An Introduction to Quantum Field Theory',
     'author': 'Peskin_Schroeder', 'year': 1995, 'citations': 22000, 'domain': 'quantum_field_theory',
     'sources': ['quantum_os', 'particle_physics']},

    {'title': 'Stabilizer Codes and Quantum Error Correction',
     'author': 'Gottesman', 'year': 1997, 'citations': 3800, 'domain': 'quantum_error_correction',
     'sources': ['quantum_os']},

    {'title': 'Uber die Entropieverminderung Szilard',
     'author': 'Szilard', 'year': 1929, 'citations': 2800, 'domain': 'thermodynamics_info',
     'sources': ['quantum_os', 'information_theory']},

    {'title': 'The thermodynamics of computation a review',
     'author': 'Bennett_1982', 'year': 1982, 'citations': 4100, 'domain': 'thermodynamics_info',
     'sources': ['quantum_os', 'information_theory']},

    {'title': 'Orchestrated reduction of quantum coherence in brain microtubules',
     'author': 'Hameroff_Penrose_1996', 'year': 1996, 'citations': 4200, 'domain': 'consciousness',
     'sources': ['quantum_os', 'quantum_biology']},

    {'title': 'Direct estimations of linear and nonlinear functionals of quantum state',
     'author': 'Ekert_et_al', 'year': 2002, 'citations': 2100, 'domain': 'quantum_physics',
     'sources': ['quantum_os']},

    {'title': 'A theory of memory retrieval drift diffusion',
     'author': 'Ratcliff', 'year': 1978, 'citations': 14000, 'domain': 'neuroscience',
     'sources': ['quantum_os', 'cognitive_science', 'psychology']},

    {'title': 'Neural basis of perceptual decision in parietal cortex',
     'author': 'Shadlen_Newsome', 'year': 2001, 'citations': 7800, 'domain': 'neuroscience',
     'sources': ['quantum_os', 'neuroscience_decision']},

    {'title': 'Importance of quantum decoherence in brain processes',
     'author': 'Tegmark', 'year': 2000, 'citations': 2900, 'domain': 'neuroscience',
     'sources': ['quantum_os']},

    {'title': 'Consciousness in the Universe review of Orch OR theory',
     'author': 'Hameroff_Penrose_2014', 'year': 2014, 'citations': 2600, 'domain': 'consciousness',
     'sources': ['quantum_os']},

    {'title': 'Quantum Computing in the NISQ era and beyond',
     'author': 'Preskill', 'year': 2018, 'citations': 8200, 'domain': 'quantum_hardware',
     'sources': ['quantum_os', 'quantum_hardware_research']},

    {'title': 'A quantum engineers guide to superconducting qubits',
     'author': 'Krantz_et_al', 'year': 2019, 'citations': 4200, 'domain': 'quantum_hardware',
     'sources': ['quantum_os', 'quantum_hardware_research']},

    {'title': 'Quantum time crystals',
     'author': 'Wilczek', 'year': 2012, 'citations': 3100, 'domain': 'quantum_physics',
     'sources': ['quantum_os']},

    {'title': 'Floquet time crystals',
     'author': 'Else_Bauer_Nayak', 'year': 2016, 'citations': 2400, 'domain': 'quantum_physics',
     'sources': ['quantum_os']},

    {'title': 'Time-crystalline eigenstate order on a quantum processor',
     'author': 'Mi_et_al_Google', 'year': 2021, 'citations': 1800, 'domain': 'quantum_hardware',
     'sources': ['quantum_os', 'quantum_hardware_research']},

    {'title': 'A quantum adiabatic evolution algorithm',
     'author': 'Farhi_et_al', 'year': 2001, 'citations': 3600, 'domain': 'quantum_computing',
     'sources': ['quantum_os']},

    # ── BIOELECTRIC PROTOCOL ─────────────────────────────────────
    {'title': 'Planarian regeneration and bioelectric memory',
     'author': 'Levin_et_al_2019', 'year': 2019, 'citations': 890, 'domain': 'bioelectric',
     'sources': ['bioelectric_protocol']},

    {'title': 'The computational boundary of a self',
     'author': 'Levin_2019', 'year': 2019, 'citations': 620, 'domain': 'bioelectric',
     'sources': ['bioelectric_protocol', 'consciousness']},

    {'title': 'Bioelectric code an ancient computational medium',
     'author': 'Levin_2021', 'year': 2021, 'citations': 430, 'domain': 'bioelectric',
     'sources': ['bioelectric_protocol']},

    {'title': 'Bioelectric signaling regulates size in zebrafish fins',
     'author': 'Silic_Zhang', 'year': 2023, 'citations': 180, 'domain': 'bioelectric',
     'sources': ['bioelectric_protocol']},

    # ── CROSS-DOMAIN ENTROPY CLUSTER ─────────────────────────────
    {'title': 'When physics gets in the way entropy-based hydrological models',
     'author': 'Entropy_Hydrology', 'year': 2026, 'citations': 2, 'domain': 'hydrology_physics',
     'sources': ['context_space', 'cross_domain_entropy']},

    {'title': 'The Human Terrain System operationally relevant social science',
     'author': 'Military_Ops', 'year': 2015, 'citations': 7, 'domain': 'military_social_science',
     'sources': ['context_space']},
]


def age_band(year):
    if year < 1950: return 'ancient'
    if year < 1990: return 'foundational'
    if year < 2010: return 'established'
    if year < 2020: return 'recent'
    return 'frontier'

def c1_classify(n_sources, band):
    if band in ('ancient', 'foundational', 'established') and n_sources >= 2:
        return 'COLD'
    elif band in ('recent', 'frontier') and n_sources >= 2:
        return 'ACTIVE-UNANCHORED'
    elif band in ('ancient', 'foundational', 'established') and n_sources == 1:
        return 'STRUCTURALLY-REAL-FRONTIER-INVISIBLE'
    else:
        return 'FLOOR'

def c2_mode(velocity):
    if velocity < 200: return 'GATEWAY'
    if velocity < 1000: return 'PROTOCOL'
    return 'FOUNDATION'

results = []
for p in unified:
    band = age_band(p['year'])
    n_src = len(set(p['sources']))
    temp = c1_classify(n_src, band)
    age = round(current_year - p['year'], 1)
    velocity = round(p['citations'] / age, 1) if age > 0 else 0
    mode = c2_mode(velocity)
    results.append({
        **p, 'band': band, 'n_sources': n_src,
        'temp': temp, 'age': age, 'velocity': velocity, 'mode': mode
    })

order = {'COLD': 0, 'ACTIVE-UNANCHORED': 1, 'STRUCTURALLY-REAL-FRONTIER-INVISIBLE': 2, 'FLOOR': 3}
results.sort(key=lambda x: (order[x['temp']], -x['citations']))

print('=' * 72)
print('UNIFIED C1 — INDEPENDENCE CONVERGENCE')
print(f'Total corpus: {len(unified)} papers | {len(set(s for p in unified for s in p["sources"]))} research areas')
print('=' * 72)

for temp_class in ['COLD', 'ACTIVE-UNANCHORED', 'STRUCTURALLY-REAL-FRONTIER-INVISIBLE', 'FLOOR']:
    group = [r for r in results if r['temp'] == temp_class]
    print(f'\n── {temp_class} ({len(group)}) ──')
    for r in group:
        print(f"  [{r['year']}] {r['author'][:28]:28} src={r['n_sources']} cites={r['citations']:>6}  {r['domain']}")
        if r['n_sources'] > 1:
            print(f"           ↳ {r['sources']}")

cold = [r for r in results if r['temp'] == 'COLD']
cold.sort(key=lambda x: -x['velocity'])

print()
print('=' * 72)
print('UNIFIED C2 — VELOCITY (cold zone only)')
print('=' * 72)
print(f'\n{"AUTHOR"[:28]:28} {"YR":4} {"VEL/yr":>8} {"MODE":12} DOMAIN')
print('-' * 72)
for r in cold:
    print(f'{r["author"][:28]:28} {r["year"]} {r["velocity"]:>8}/yr {r["mode"]:12} {r["domain"]}')

print()
print('── BY MODE ──')
mode_groups = defaultdict(list)
for r in cold:
    mode_groups[r['mode']].append(r)

for mode in ['FOUNDATION', 'PROTOCOL', 'GATEWAY']:
    group = mode_groups.get(mode, [])
    print(f'\n  {mode} ({len(group)}):')
    for r in group:
        print(f'    [{r["year"]}] {r["author"][:35]:35} {r["velocity"]}/yr | {r["domain"]}')
        print(f'           sources: {r["sources"]}')

print()
print('── CROSS-DOMAIN NODES (cold, 3+ research areas) ──')
cross = [r for r in cold if r['n_sources'] >= 3]
cross.sort(key=lambda x: -x['n_sources'])
for r in cross:
    print(f'  {r["author"][:35]:35} n_src={r["n_sources"]} mode={r["mode"]}')
    print(f'    domains: {r["sources"]}')

print()
print('── DOMAIN DISTRIBUTION IN COLD ZONE ──')
cold_domains = defaultdict(list)
for r in cold:
    cold_domains[r['domain']].append(r)
for domain, papers in sorted(cold_domains.items(), key=lambda x: -len(x[1])):
    modes = [r['mode'] for r in papers]
    print(f'  {domain:30} ({len(papers)}) | modes: {modes}')

print()
print('── EMERGENT: WHAT THREE TRACKS SHARE IN THE COLD ZONE ──')
print('   (quantum_os, context_space, bioelectric_protocol)')
three_tracks = {'quantum_os', 'context_space', 'bioelectric_protocol'}
for r in cold:
    overlap = three_tracks & set(r['sources'])
    if len(overlap) >= 2:
        print(f'  {r["author"][:35]:35} overlaps={sorted(overlap)} mode={r["mode"]}')

if __name__ == '__main__':
    pass
