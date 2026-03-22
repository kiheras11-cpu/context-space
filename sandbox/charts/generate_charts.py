"""
Chart Generator — C1 + C2 Results
Internal QOS Run + Unified Corpus Run
Outputs: qos_chart.txt + unified_chart.txt (ASCII — no dependencies)
"""

# ── QOS INTERNAL RUN ─────────────────────────────────────────────────────────

qos_results = [
    # temp_class, author, year, velocity, mode, domain, weight
    ('COLD',       'Nielsen_Chuang',        2000, 1603.1, 'FOUNDATION', 'quantum_foundations',   4),
    ('COLD',       'Landauer',              1961,  168.7, 'GATEWAY',    'thermodynamics_info',   3),
    ('COLD',       'Dalibard_Castin_Molmer',1992,  277.8, 'PROTOCOL',   'quantum_physics',       3),
    ('COLD',       'Ratcliff',              1978,  290.5, 'PROTOCOL',   'neuroscience',          2),
    ('COLD',       'Shadlen_Newsome',       2001,  309.5, 'PROTOCOL',   'neuroscience',          2),
    ('COLD',       'Penrose',               1989,  483.9, 'PROTOCOL',   'consciousness',         2),
    ('COLD',       'Aharonov_et_al',        1988,  136.1, 'GATEWAY',    'quantum_physics',       2),
    ('COLD',       'Hameroff_Penrose',      1996,  139.1, 'GATEWAY',    'consciousness',         2),
    ('COLD',       'Molmer_Castin_Dalibard',1993,  174.4, 'GATEWAY',    'quantum_physics',       2),
    ('COLD',       'Ekert_et_al',           2002,   86.6, 'GATEWAY',    'quantum_physics',       2),
    ('A-UNANCHORED','Mi_et_al_Google',      2021, 1800.0, 'FOUNDATION', 'quantum_hardware',      3),
    ('A-UNANCHORED','Wilczek',              2012,  770.0, 'PROTOCOL',   'quantum_physics',       2),
    ('A-UNANCHORED','Else_Bauer_Nayak',     2016,  231.0, 'PROTOCOL',   'quantum_physics',       2),
    ('A-UNANCHORED','Preskill',             2018,  310.0, 'PROTOCOL',   'quantum_hardware',      2),
    ('A-UNANCHORED','Krantz_et_al',         2019,  301.0, 'PROTOCOL',   'quantum_hardware',      2),
    ('A-UNANCHORED','Hameroff_Penrose_2014',2014,  173.0, 'GATEWAY',    'consciousness',         2),
    ('SR-FI',      'Feynman',               1948,  108.7, 'GATEWAY',    'quantum_physics',       1),
    ('SR-FI',      'Szilard',               1929,   28.8, 'GATEWAY',    'thermodynamics_info',   1),
    ('SR-FI',      'Bennett',               1982,   92.8, 'GATEWAY',    'thermodynamics_info',   1),
    ('SR-FI',      'Peskin_Schroeder',      1995,  705.1, 'PROTOCOL',   'quantum_field_theory',  1),
    ('SR-FI',      'Gottesman',             1997,  287.0, 'PROTOCOL',   'quantum_error_corr',    1),
    ('SR-FI',      'Tegmark',               2000,  110.0, 'GATEWAY',    'neuroscience',          1),
    ('SR-FI',      'Farhi_et_al',           2001,  137.0, 'GATEWAY',    'quantum_computing',     1),
    ('FLOOR',      'Zhang_et_al',           2017,  203.0, 'PROTOCOL',   'quantum_physics',       1),
    ('FLOOR',      'Choi_et_al',            2017,  203.0, 'PROTOCOL',   'quantum_physics',       1),
    ('FLOOR',      'Cross_OpenQASM',        2017,   89.0, 'GATEWAY',    'quantum_software',      1),
    ('FLOOR',      'IonQ',                  2024,   40.0, 'GATEWAY',    'quantum_hardware',      1),
]

# ── UNIFIED RUN ──────────────────────────────────────────────────────────────

unified_results = [
    ('COLD',       'Nielsen_Chuang',        2000, 1603.1, 'FOUNDATION', 'quantum_foundations',   2),
    ('COLD',       'Peskin_Schroeder',       1995,  705.1, 'PROTOCOL',   'quantum_field_theory',  2),
    ('COLD',       'Penrose_1989',           1989,  483.9, 'PROTOCOL',   'consciousness',         3),
    ('COLD',       'Shadlen_Newsome',        2001,  309.5, 'PROTOCOL',   'neuroscience',          2),
    ('COLD',       'Ratcliff',               1978,  290.5, 'PROTOCOL',   'neuroscience',          3),
    ('COLD',       'Dalibard_Castin_Molmer', 1992,  277.8, 'PROTOCOL',   'quantum_physics',       2),
    ('COLD',       'Landauer',               1961,  168.7, 'GATEWAY',    'thermodynamics_info',   3),
    ('COLD',       'Hameroff_Penrose_1996',  1996,  139.1, 'GATEWAY',    'consciousness',         2),
    ('COLD',       'Aharonov_et_al',         1988,  136.1, 'GATEWAY',    'quantum_physics',       2),
    ('COLD',       'Kuhn',                   1962,  111.3, 'GATEWAY',    'epistemology',          7),
    ('COLD',       'Feynman_1948',           1948,  108.7, 'GATEWAY',    'quantum_physics',       2),
    ('COLD',       'Bennett_1982',           1982,   92.8, 'GATEWAY',    'thermodynamics_info',   2),
    ('COLD',       'Kotter_Cohen',           2002,   34.7, 'GATEWAY',    'org_change',            2),
    ('COLD',       'Szilard',                1929,   28.8, 'GATEWAY',    'thermodynamics_info',   2),
    ('A-UNANCHORED','OpenAI_GPT4',           2023, 7651.0, 'FOUNDATION', 'ai_llm',                4),
    ('A-UNANCHORED','Moher_PRISMA',          2015, 1568.0, 'FOUNDATION', 'methodology',           3),
    ('A-UNANCHORED','Preskill',              2018,  310.0, 'PROTOCOL',   'quantum_hardware',      2),
    ('A-UNANCHORED','Kotter_2012',           2012,  308.4, 'PROTOCOL',   'org_change',            5),
    ('A-UNANCHORED','Krantz_et_al',          2019,  301.0, 'PROTOCOL',   'quantum_hardware',      2),
    ('A-UNANCHORED','Mi_et_al_Google',       2021,  450.0, 'PROTOCOL',   'quantum_hardware',      2),
    ('A-UNANCHORED','Levin_2019',            2019,   47.0, 'GATEWAY',    'bioelectric',           2),
    ('A-UNANCHORED','Entropy_Hydrology',     2026,    1.0, 'GATEWAY',    'hydrology_physics',     2),
]


def ascii_bar(value, max_val, width=40):
    filled = int((value / max_val) * width)
    return '█' * filled + '░' * (width - filled)

def mode_symbol(mode):
    return {'FOUNDATION': '◆', 'PROTOCOL': '●', 'GATEWAY': '○'}.get(mode, '?')

def temp_color(temp):
    return {'COLD': '[C]', 'A-UNANCHORED': '[A]', 'SR-FI': '[S]', 'FLOOR': '[F]'}.get(temp, '[?]')


def render_chart(results, title, subtitle):
    lines = []
    lines.append('=' * 78)
    lines.append(title.center(78))
    lines.append(subtitle.center(78))
    lines.append('=' * 78)
    lines.append('')

    # Velocity axis chart
    lines.append('── C2 VELOCITY MAP (citations/year) ──')
    lines.append('   ◆ FOUNDATION >1000/yr   ● PROTOCOL 200-1000/yr   ○ GATEWAY <200/yr')
    lines.append('   [C]=COLD  [A]=ACTIVE-UNANCHORED  [S]=STRUCT-REAL-FRONTIER-INVISIBLE  [F]=FLOOR')
    lines.append('')

    max_vel = max(r[3] for r in results)
    cold = sorted([r for r in results if r[0] == 'COLD'], key=lambda x: -x[3])
    active = sorted([r for r in results if r[0] == 'A-UNANCHORED'], key=lambda x: -x[3])
    srfi = sorted([r for r in results if r[0] == 'SR-FI'], key=lambda x: -x[3])
    floor = sorted([r for r in results if r[0] == 'FLOOR'], key=lambda x: -x[3])

    for group, label in [(cold, 'COLD ZONE'), (active, 'ACTIVE-UNANCHORED'),
                          (srfi, 'STRUCT-REAL-FRONTIER-INVISIBLE'), (floor, 'FLOOR')]:
        if not group:
            continue
        lines.append(f'  ┌─ {label} ({len(group)}) ─────────────────────────────────────────────────────┐')
        for r in group:
            temp, author, year, vel, mode, domain, nsrc = r
            bar = ascii_bar(vel, max_vel, width=30)
            sym = mode_symbol(mode)
            tc = temp_color(temp)
            lines.append(f'  │ {tc} {sym} {author[:22]:22} {year} │{bar}│ {vel:>7}/yr  src={nsrc}')
        lines.append(f'  └────────────────────────────────────────────────────────────────────────┘')
        lines.append('')

    # Cross-section weight chart (C1)
    lines.append('── C1 CROSS-SOURCE WEIGHT MAP (how many research tracks cite this node) ──')
    lines.append('')
    max_src = max(r[6] for r in results)
    all_sorted = sorted(results, key=lambda x: (-x[6], -x[3]))
    for r in all_sorted:
        temp, author, year, vel, mode, domain, nsrc = r
        bar = ascii_bar(nsrc, max_src, width=25)
        sym = mode_symbol(mode)
        tc = temp_color(temp)
        lines.append(f'  {tc} {sym} {author[:24]:24} {year}  [{bar}] {nsrc} src  {vel}/yr  {domain[:20]}')

    lines.append('')
    lines.append('── LEGEND ──')
    lines.append('  ◆ FOUNDATION (>1000/yr)   ● PROTOCOL (200-1000/yr)   ○ GATEWAY (<200/yr)')
    lines.append('  [C] COLD — old + multi-source (confirmed foundational)')
    lines.append('  [A] ACTIVE-UNANCHORED — recent + multi-source (moving fast, not yet cold)')
    lines.append('  [S] STRUCT-REAL-FRONTIER-INVISIBLE — old + single source (undervalued seam)')
    lines.append('  [F] FLOOR — recent + single source (instrumental)')
    lines.append('')
    lines.append('  src = number of distinct research tracks that reference this node')
    lines.append('  vel = citations per year since publication (C2 velocity)')
    lines.append('=' * 78)

    return '\n'.join(lines)


qos_chart = render_chart(
    qos_results,
    'C1 + C2 ANALYSIS — QUANTUM OS INTERNAL CITATION CORPUS',
    'QOS paper reference list only | 27 papers | Run: 2026-03-22'
)

unified_chart = render_chart(
    unified_results,
    'C1 + C2 ANALYSIS — UNIFIED CORPUS (ALL RESEARCH TRACKS)',
    'Context Space + QOS + Bioelectric | 46 papers | 31 research areas | Run: 2026-03-22'
)

with open('charts/qos_chart.txt', 'w') as f:
    f.write(qos_chart)

with open('charts/unified_chart.txt', 'w') as f:
    f.write(unified_chart)

print(qos_chart)
print()
print()
print(unified_chart)

print('\n\nCharts written to charts/qos_chart.txt and charts/unified_chart.txt')
