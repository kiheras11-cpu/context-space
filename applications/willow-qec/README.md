# Context Space Applied: Google Willow QEC

## What This Is

Context Space instruments applied to the Google Willow quantum error correction dataset (Acharya et al. 2024, *Nature*, arXiv:2408.13687).

This is the first application of Context Space outside citation networks — run against experimental physics data to probe the structure beneath a published result.

**Core finding:** Lambda_observed (2.04) is 66% below Lambda_flat (6.13, surface code theory prediction). Three independent signals confirm the gap is structural, not noise. The topology is pointing toward non-flat probability space at the 10⁻³ working scale, with Ricci curvature as the candidate geometric mechanism.

---

## The Finding

Standard surface code theory predicts:

```
Lambda_flat = p_threshold / p_physical = 0.01 / 0.00163 ≈ 6.13
```

Google Willow measured Lambda = 2.04. That's 34% of theoretical maximum.

### Three independent curvature signals

| Signal | Observed | Flat-space prediction |
|--------|----------|----------------------|
| Lambda_obs / Lambda_flat | 0.3401 | 1.0 |
| Lambda_variance / Lambda_LER | 1.5291 | 1.0 |
| Log-linearity deviation | 0.000201 | 0.0 |

All three point to the same cause: the working space at 10⁻³ is non-flat. Lambda is not purely a decoder efficiency metric — it encodes the geometry of the space correction is happening in.

### Warm/cold taxonomy compression

In flat citation-network space, Context Space uses:
- Cold threshold: 50,000 citations
- Warm threshold: 5,000 citations

In the actual working geometry of this experiment:
- Cold threshold compresses to: **17.0**
- Warm threshold compresses to: **1.7**
- Combined correction factor: **3.4 × 10⁻⁴**

A node that reads as cold in flat space registers as active in the real working geometry.

### Ricci curvature bridge

Nexus (Phi-4 local, full C1–C4 + 4 Scout treatment) independently identified Ricci curvature as the mathematical structure explaining the variance/LER asymmetry. In Riemannian geometry, Ricci curvature governs how volume growth differs across dimensions — the same mechanism that produces faster variance suppression relative to mean LER.

This was not in the prompt. It emerged from the structural analysis.

---

## What's Still Open

**1. p_physical verification**
The curvature factor scales linearly with p_physical. We estimated ~0.163% from public sources. This needs verification against the Acharya et al. 2024 supplementary materials. The direction of the finding doesn't change with reasonable p_physical values; the exact magnitude does.

> **If you have access to the verified p_physical from the Acharya et al. supplementary, we want to hear from you.** Open an issue or reach out at [@kiheras on X](https://x.com/kiheras).

**2. Curvature corpus**
We ran Archie (our SemanticScholar traversal instrument) against five curvature-adjacent domains: Riemannian geometry, information geometry, QEC threshold theory, quantum geometric phase, and Ising universality classes. API quota constraints limited the run to one completed seed query today — landing in 3D Ising with power-law correlated disorder, a direct neighbor to our alpha~2.7 finding from TFIM simulations.

The remaining four domains (Ricci curvature, information geometry, QEC threshold, quantum geometry) are queued. Updates coming as quota resets.

**3. TFIM alpha~2.7 connection**
Our separate TFIM simulations (N=3,4,5) found alpha = 2.640–2.741 near the purity maximum t*. The 3D Ising universality class with power-law correlated disorder operates in the same exponent range. Whether these share a universality class is an open question. The Archie harvest into Ising literature is the next step.

---

## Files

| File | Description |
|------|-------------|
| `willow_backcalc.py` | Back-calculation script — pure math, no LLM |
| `willow_backcalc.json` | Structured results |
| `NEXUS_BACKCALC_REPORT.md` | Phi-4 full topology treatment (C1–C4 + 4 Scouts + Summary) |
| `archie-curvature-ss-2026-03-27.json` | Archie SS harvest — Ising universality class corpus (28 papers) |

---

## How to Run

```bash
pip install requests
python3 willow_backcalc.py
```

No API key needed. No LLM required. Pure math from the Willow dataset.

To run the Nexus treatment (requires Ollama + phi4:latest):
```bash
# From the nexus-poc directory
python3 nexus_backcalc_run.py
```

---

## Context

This application is part of an ongoing series using Context Space as a live instrument — not just on citation networks, but on any structured dataset with topology.

Prior applications:
- **Context Space on academic citation networks** — see [ARXIV_DRAFT_v0.1.md](../../ARXIV_DRAFT_v0.1.md) for the full methodology
- **TFIM t* power law** — threshold distribution near quantum purity maximum, N=3,4,5 (separate repository, results to be published)

---

## Citation

```
Kanyita, E., Tsosie, L., & Erastus (2026).
Context Space: A Topology Instrument for Citation and Structured Data Analysis.
GitHub: github.com/kiheras11-cpu/context-space
```

*Source data: Acharya et al. (2024). Quantum error correction below the surface code threshold. Nature. arXiv:2408.13687*
