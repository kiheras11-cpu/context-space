# Context Space

**A substrate-native reading instrument for knowledge topology.**

> *Assume nothing. Enforce nothing. Trust the substrate.*

---

## What This Is

Context Space is a set of three traversal instruments that read the natural geometry of a citation corpus — without declaring in advance what they should find. Point them at any knowledge domain and run them. The cold anchors surface through convergence. The functional modes emerge from propagation behavior. The pre-paradigm states announce themselves through what fields reach for when they don't know their own foundation.

This is not a knowledge graph. Not a recommendation engine. Not citation analysis in the conventional sense.

It is a reading instrument. The difference: a reading instrument finds what the substrate contains. A knowledge graph contains what you put into it.

**Full analysis:** See [ARXIV_DRAFT_v0.1.md](./ARXIV_DRAFT_v0.1.md) — preprint March 2026.  
**Raw observational record:** See [EMERGENCE_LOG.md](./EMERGENCE_LOG.md) — 16 entries written at the moment of discovery, before interpretation.

---

## Quick Start

```bash
pip install requests
cd scripts/
python3 run_scouts.py
```

Requires a [Semantic Scholar API](https://www.semanticscholar.org/product/api) key (free tier works, expect rate limiting).

Set your API key:
```bash
export S2_API_KEY=your_key_here  # optional — free tier works without one
```

---

## The Three Scouts

**Scout 1 — Warm→Cold:** Start at the frontier (recent, active papers). Follow the highest-citation reference at each step. Discover cold anchors through traversal — never declare them in advance.

**Scout 2 — Cold→Warm:** Start from a discovered cold anchor. Follow citations forward. Characterize the warm zone above a cold node.

**Scout 3 — EI Helper (Omnidirectional):** Observe a target node from both directions simultaneously. Measure the bidirectional profile. Flag asymmetries. Do not interpret during collection.

---

## What One Run Found

Running these instruments on live Semantic Scholar data, starting from quantum computing frontier papers, produced:

**Five node states:**
- Confirmed (high warm + high cold)
- Active-unanchored (high warm + zero cold — bridge without genealogical seam)
- Structurally real, frontier-invisible (zero warm + high cold — undervalued seam)
- Floor / non-bridge
- **Pre-paradigm** *(discovered, not hypothesized)* — field is active but reaches for epistemological vocabulary rather than technical foundation

**Three functional modes of cold nodes:**

| Mode | Forward behavior | Example | Velocity |
|---|---|---|---|
| Gateway | Expands across domains, time-invariant | Kuhn (1962) | 111.6/yr |
| Protocol | Closes locally, 1–2 hops | Kotter (2012) | 308.4/yr |
| Foundation | Deepens within one domain, rapid | GPT-4 (2023) | 7,651/yr* |

*Lower bound — see paper footnote [^2]*

**Cold-entry velocity encodes functional mode.** No traversal required for classification — citations per year alone predicts type. Two orders of magnitude separate gateway from foundation.

**Three empty-path states:** Pre-formation / Lag / Terminal  
**Two substrate boundary conditions:** Lag edge (future, ~0–6mo) / Pre-digital edge (past, ~pre-1990)  
**Indexable region:** 1990–2025

---

## Important: Velocity Thresholds Are Corpus-Specific

The numbers above (111 / 308 / 7,651 cites/yr) are **empirical observations from one corpus** — academic papers via Semantic Scholar, seeded from physics and philosophy of science. They are not universal constants.

The hypothesis is that the *ordinal relationship* (gateway < protocol < foundation) holds universally. The specific numbers are what this substrate told us about itself.

If you run this on legal citations, patent networks, software dependencies, or social media link graphs — your thresholds will be different. Report them. That's how the cross-substrate hypothesis gets tested.

---

## The Methodology

```
Observe before naming.
Name before building.
Never reverse the order.
```

All findings in this repository are emergent. No cold anchors were declared in advance. No domain categories were imposed. The emergence log records each finding at the moment of discovery, before interpretation.

When we pre-declared cold anchors (Scout 2's original seed list of Newton, Maxwell, Boltzmann), every seed returned wrong papers or failed entirely. When we followed the topology without assumptions (Scout 1 with no constraints), it found Kuhn's *Structure of Scientific Revolutions* in a single hop from a topological qubit paper.

The methodology is the contribution as much as the findings.

---

## Repository Structure

```
context-space/
├── README.md                   — this file
├── EMERGENCE_LOG.md            — 16 entries, the raw observational record
├── ARXIV_DRAFT_v0.1.md         — full paper draft
├── scripts/
│   ├── scout_utils.py          — shared API utilities, rate limiting, zone classification
│   ├── run_scouts.py           — all three scouts + loop variants (1B, 3B)
│   ├── c2_velocity_test.py     — C2 velocity for a single node
│   └── c2_velocity_all.py      — C2 velocity comparative across discovered nodes
└── data/
    ├── scout_warm_cold_output.json
    ├── scout_cold_warm_output.json
    ├── scout_ei_helper_output.json
    ├── scout_warm_cold_loop_output.json
    ├── scout3_hydrology_output.json
    ├── c2_velocity_kuhn_output.json
    └── c2_velocity_all_output.json
```

---

## Status

This is **live research**. C1 (Independence Convergence) and C2 (Temporal Persistence, partial) have been tested. C3 (Connection Decay by Path Length) and C4 (Encounter Deposit / No Erasure) are pending.

The emergence log will be updated as constants are tested. The paper will be revised as findings accumulate. Issues and discussions are open — if you run this on a different corpus, open an issue and share what you found.

---

## Authors

Emmanuel K. + Erastus K. — Lucent Research Division  
March 2026

---

## License

MIT — scripts and data. The emergence log and paper are CC BY 4.0.

*Run it. Find what your substrate contains. Report what you find.*
