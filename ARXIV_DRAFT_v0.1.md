# Context Space: A Substrate-Native Reading Instrument for Knowledge Topology

*Emmanuel K., Lisa K., Erastus K. — Lucent Research Division*
*Preprint — March 2026*
*Status: Draft v0.1 — C2 partial, C3 and C4 pending*

---

## Abstract

We present an empirical methodology for characterizing the structural topology of human knowledge through citation graph traversal, without domain assumptions, pre-declared anchors, or imposed classification schemes. Using three independent traversal instruments applied to live citation data, we discover five structural node states, three functional modes of foundational nodes classifiable by a single metric (cold-entry velocity in citations per year), three empty-path states mapping the substrate's own boundaries, and two hard boundary conditions defining the indexable region of the knowledge space (approximately 1990–2025). A secondary finding: pre-paradigm states in active research fields are detectable in citation topology — fields in paradigmatic uncertainty independently reach for the same epistemological anchor across unrelated domains simultaneously. All findings are emergent. No structure was declared in advance. The methodology is a single operating principle: *assume nothing, enforce nothing, trust the substrate.*

---

## 1. Introduction

The problem of hallucination in large language models is commonly framed as a data volume problem: the model hasn't seen enough. We propose a different framing. Hallucination is a routing problem. A language model that has read everything but cannot navigate the topology of what it has read will still route queries to incorrect regions of its knowledge space. The question is not how much the space contains but whether the space has been read in a way that preserves its natural geometry.

This paper reports the initial results of an attempt to build a reading instrument that reads the geometry rather than imposing one. We call the resulting structure a context space: a substrate-native representation of the topology of a knowledge domain, constructed by following citation weight rather than semantic label.

The core hypothesis, which this paper tests empirically: a knowledge space has natural cold zones (load-bearing, high-convergence nodes), warm zones (active construction), and frontier zones (too new to have accumulated weight), and these zones can be characterized without declaring them in advance. The topology can describe itself.

---

## 2. Methodology

### 2.1 The Three Scouts

We constructed three independent traversal instruments operating on the Semantic Scholar citation graph:

**Scout 1 (Warm→Cold):** Begin at the frontier (recent, high-activity papers). Follow the highest-citation reference at each step. Continue until reaching a node with no further references or a node classified as cold (>5,000 citations). Record the full traversal chain.

**Scout 2 (Cold→Warm):** Begin at a known or discovered cold anchor. Follow the highest-citation citing paper at each step. Continue until reaching a node classified as frontier (<100 citations, recently published). Record the full traversal chain.

**Scout 3 (EI Helper — Omnidirectional):** For a target node, pull both its reference set (cold direction) and its citation set (warm direction) simultaneously. Compute cold and warm profile metrics. Flag asymmetries. Do not interpret — record.

No paper IDs, domain labels, or expected cold anchors were provided as inputs. Seeds were either recent papers from ArXiv query results (Scout 1) or nodes discovered by prior traversals (Scouts 2 and 3 in loop mode).

### 2.2 The Protocol

*Observe before naming. Name before building. Never reverse the order.*

During data collection, no interpretation was permitted. Findings were recorded in an emergence log at the moment of observation. The log is included in full as supplementary material and on GitHub.

### 2.3 Cold-Entry Velocity — Definition and Limitations

For each cold node discovered through traversal, we computed cold-entry velocity: total citations divided by years since publication.

```
velocity = total_citations / (current_year - publication_year)
```

**This is a mean rate across lifespan, not a current rate.** [^1]

This distinction matters differently for each functional mode:

- For gateway nodes (e.g. Kuhn, 64 years old): the mean closely approximates the current rate. The gateway function has been stable for decades — the accumulation curve is approximately flat. Mean ≈ current.

- For foundation nodes (e.g. GPT-4, 3 years old): the mean almost certainly *understates* the current rate. Citation accumulation for a rapidly-adopted foundation node is a compounding curve — early years absorb it, later years build on it at accelerating speed. The reported velocity of 7,651/yr should be read as "at least 7,651/yr and likely significantly higher." [^2]

- For protocol nodes (e.g. Kotter, 14 years old): the curve may be non-monotonic — a rise during adoption, a plateau during peak use, a gradual decline as the procedure is superseded or internalized. The mean rate may mask a bell curve. [^3]

A more precise C2 instrument would compute year-over-year citation rate as a time series rather than a scalar mean — capturing the shape of the curve, not just its average. This is the target for C2 full temporal persistence measurement (see Section 5, Open Questions).

The functional mode classification presented in this paper holds despite this imprecision. The ordinal separation between functional modes (gateway < protocol < foundation) spans two orders of magnitude. The classification is robust to the approximation. The specific numbers, however, are lower bounds for foundation nodes and reasonable approximations for gateway and protocol nodes.

---

## 3. Results

### 3.1 Five Node States

Running Scout 1 from five frontier seeds in quantum computing and running C1 (Independence Convergence) bidirectionally on a 25-node synthetic physics graph, we identified five distinct structural states:

| State | Warm score | Cold score | Description |
|---|---|---|---|
| Confirmed | High | High | Two independent methods agree. Maximum structural confidence. |
| Active-unanchored | High | Zero | Frontier treats as bridge; foundation sees no seam. |
| Structurally real, frontier-invisible | Zero | High | Load-bearing seam the active community has not recognized. |
| Floor / non-bridge | Zero | Zero | Substrate anchor or genuine non-bridge. |
| **Pre-paradigm** | High | Non-technical cold | Field is active but reaches for epistemological vocabulary, not technical foundation. |

The fifth state was not hypothesized. Scout 1 traversal from a 2024 topological qubit paper reached *The Structure of Scientific Revolutions* (Kuhn, 1962) in a single hop — not a physics paper, not a technical result, but a book about what happens when a field does not yet have a paradigm. The field's citation topology made an implicit structural confession.

### 3.2 Three Functional Modes of Cold Nodes

Through loop testing — feeding Scout 2 forward outputs back into Scout 1 as seeds — we discovered that cold nodes differ not only in domain but in their forward propagation behavior:

**Gateway nodes** (exemplar: Kuhn, *Structure of Scientific Revolutions*, 1962): forward path branches across multiple unrelated domains simultaneously. The node holds vocabulary for uncertainty. Fields reach for it when they need language for what they do not know yet. Temporal character: ancient foundation, perpetually fresh surface. The gateway function is time-invariant — confirmed consistent across six decades of citation data spanning ten independent fields.

**Foundation nodes** (exemplar: GPT-4 Technical Report, 2023): forward path deepens within a single domain. The node is load-bearing for an entire field's current development trajectory. Cold-entry was rapid — 22,953 citations in approximately three years. Age is not what makes a node cold. Weight is. [^4]

**Protocol nodes** (exemplar: Kotter, *Leading Change*, 2012): forward path closes locally in one to two hops. The node is operational — it tells a field how to act when it does not have a paradigm yet. The circuit closes and the forward momentum stops.

### 3.3 Cold-Entry Velocity as Type Classifier

Computing cold-entry velocity for each discovered cold node:

| Node | Functional mode | Velocity (cites/yr) | Note |
|---|---|---|---|
| Kuhn (1962) | Gateway | 111.6 | Mean ≈ current rate [^1] |
| Kotter (2012) | Protocol | 308.4 | Mean may mask bell curve [^3] |
| GPT-4 (2023) | Foundation | 7,651.0 | Mean understates current rate [^2] |

The ordering is clean across two orders of magnitude. Gateway nodes accumulate slowly through broad cross-domain citation over decades. Foundation nodes accumulate rapidly through concentrated single-domain citation. Protocol nodes fall between.

**This metric requires no traversal to compute.** Given only the citation count and publication year of a cold node, its functional mode is predictable. The classification is automatic. Velocity encodes type. [^5]

### 3.4 Three Empty-Path States

A node that returns no results from Scout 1 or Scout 2 traversal is not uniformly uninformative. We identified three distinct empty-path states:

**Pre-formation:** The node does not yet exist. A structural gap where the topology expects something that has not been created. The space is showing where knowledge is about to be built.

**Lag:** The node exists and is being cited (incoming citations visible) but its own references have not been indexed by the substrate. The paper is too recently published for the reference graph to be complete. The substrate is still reading it. Detectable signature: citations present, references absent, publication date within six months. We observed a 2026 hydrology paper with 104 real references, all dark, and two incoming citations from military operations research.

**Terminal / Pre-digital:** The node exists and is heavily cited but has no indexed references. Either a genuine foundational floor (cites nothing because nothing preceded it in the indexed space) or a pre-digital publication whose reference graph predates systematic digital indexing. Distinguishable by publication date: pre-digital boundary is approximately 1990.

### 3.5 Two Substrate Boundary Conditions

The Semantic Scholar citation graph has two hard edges:

**Lag edge (future):** Papers published within approximately six months have no indexed reference graphs. The backward path is dark. The forward path (incoming citations) is partially visible. The substrate is in active ingestion.

**Pre-digital edge (past):** Papers published before approximately 1990 have no indexed reference graphs. Kuhn's own references — what shaped his thinking — are permanently dark in this substrate. The floor below pre-digital cold nodes is unreachable through this instrument alone. [^6]

The core indexable region is **1990–2025**: a 35-year window of human knowledge with full bidirectional fidelity. Both edges are defined, bounded, and architecturally addressable through supplementary instruments.

### 3.6 Cross-Domain Entropy Cluster

An unexpected cluster emerged through traversal:

Kuhn's 2026 warm zone contains a hydrology paper (*When physics gets in the way: an entropy-based evaluation of conceptual constraints in hybrid hydrological models*, 2026). This paper's warm zone is military operations research. The cluster: paradigm theory → physics formalism as epistemological evaluation tool → operational application in conflict contexts.

These three fields do not cite each other directly. They share a methodology: using entropy as a diagnostic for pre-paradigm conceptual structures. They arrived at this independently. The citation topology made the connection visible before any semantic search would have found it.

### 3.7 The Automated Characterization Pipeline

The three instruments compose into a characterization pipeline requiring no human input beyond an initial frontier seed. All three scouts must complete before any C constant is applied:

1. **Scout 1 (Warm→Cold)** — discovers cold nodes by following citation weight from the frontier backward. Surfaces cold anchors without declaring them in advance.
2. **Scout 2 (Cold→Warm)** — traces forward from each discovered cold anchor into the warm zone above it. Maps the forward propagation behavior: does the path expand across domains (gateway), deepen within one domain (foundation), or close locally (protocol)? This behavioral evidence is essential — it cannot be inferred from velocity alone.
3. **Scout 3 (Omnidirectional)** — observes each cold node from both directions simultaneously. Confirms the bidirectional profile, flags asymmetries, and validates the functional mode identified by Scout 2.
4. **C2 velocity** — computes cold-entry velocity (citations/year) for each confirmed cold node. Classifies functional mode automatically from the scalar metric. The ordinal separation between modes (gateway < protocol < foundation) provides independent confirmation of the Scout 2 behavioral classification.

Discovery (Scout 1) → Forward Mapping (Scout 2) → Bidirectional Confirmation (Scout 3) → Velocity Classification (C2).

Scouts 1, 2, and 3 are observational instruments. C2 velocity is the first analytical constant applied to their output. C3 and C4 follow in sequence once C2 is complete.

---

## 4. Discussion

### 4.1 What This Is Not

This is not a knowledge graph. A knowledge graph is a declared structure. This is a read structure — one that emerges from following the weight of the substrate without imposing categories.

This is not a recommendation engine. It characterizes what is load-bearing, what is active, what is pre-paradigm, and what is unreachable. It describes the geometry; it does not navigate it.

This is not citation analysis in the conventional sense. Citation analysis asks: which papers are most cited? This asks: what structural role does a node play, how does it propagate forward, and how long has it held that role?

### 4.2 Hallucination as Routing Failure

If hallucination is a routing problem, the context space addresses it at the structural level. A language model routed through a context space that correctly identifies cold anchors, pre-paradigm regions, and lag-state nodes will route queries to structurally appropriate regions rather than to high-frequency but low-structure regions. The reduction in hallucination is a consequence of reading the topology, not of adding more data.

### 4.3 Corpus-Specific Calibration

**The velocity thresholds reported in this paper (111/308/7,651 cites/yr) are empirical observations from one corpus — academic papers via Semantic Scholar, predominantly physics and philosophy of science. They are not universal constants.** [^5]

Citation cultures vary by field and substrate. Legal scholarship, patent citation networks, software dependency graphs, and social media link graphs will each have their own citation rates and therefore their own velocity thresholds. The ordinal relationship (gateway < protocol < foundation) is hypothesized to be universal — a structural property of how knowledge builds, not a property of academic citation culture. The specific numbers are what this substrate told us about itself.

Researchers applying this methodology to other corpora should: run the scouts without pre-set thresholds, compute velocity for the cold nodes discovered, and read the separation. The thresholds will emerge from the substrate. We report ours. Report yours.

### 4.4 Showrunr as Prior Art

The state machine underlying Showrunr — a live event production management system — operates on containment-before-correction logic that distinguishes between load-bearing constraints (venue, power, schedule) and operational constraints (rider compliance, crew communication). This distinction maps directly to the foundation/protocol functional mode split. The methodology has production miles. The theoretical framework was articulated after the fact, not before.

### 4.5 The Operating Principle

Every finding in this paper was produced by the same methodology: run the instrument without pre-declaring what it should find, then read what appeared. When we pre-declared cold anchors (Scout 2's original seed list), the instrument failed. When we followed the topology (Scout 1 with no assumptions), it found Kuhn in one hop from a topological qubit paper.

*Assume nothing. Enforce nothing. Trust the substrate.*

This is not a research heuristic. It is a statement about the relationship between instruments and the substrates they measure. An instrument that imposes structure on what it measures will find the structure it imposed. An instrument that reads the natural geometry will find the geometry.

---

## 5. Open Questions

- **C2 temporal persistence — Kotter:** does protocol field spread hold consistently narrow across decades, or has it narrowed over time?
- **C2 full time-series:** year-over-year citation rate curves for all three functional modes, replacing scalar mean with true velocity trajectory
- **C3 (Connection Decay by Path Length):** does influence decay with distance from a cold anchor? Does the decay rate differ by functional mode?
- **C4 (Encounter Deposit / No Erasure):** when multiple traversal paths converge on the same node, does the encounter strengthen the field?
- **Hydrology paper scheduled re-observation:** paper ID `35d163e6b6a1acf6b36e433456a64c85b6d45652`, June 2026. 104 currently-dark references will be indexed. Will determine whether pre-paradigm physics work roots into physics cold anchors or epistemological ones.
- **GPT-4 temporal profile:** re-examine 2028 when decade-scale data is available. Current velocity (7,651/yr mean) is likely a significant underestimate of actual current rate.
- **Cross-substrate replication:** run the scouts on legal citation networks, software dependency graphs, patent citation networks. Do the functional modes and their ordinal velocity relationship hold?

---

## 6. Conclusion

C1 alone produced: five node states, three functional modes, a velocity-based automatic type classifier, three empty-path states, two substrate boundary conditions, a cross-domain entropy cluster, and an automated characterization pipeline. C2, C3, and C4 have not yet run.

The context space is a substrate-native reading instrument. It finds what the substrate contains by reading the substrate's own structure. The findings are what the substrate produced when we stopped telling it what to contain.

---

## Footnotes

[^1]: **Velocity as mean rate, not current rate.** The formula `velocity = total_citations / years_since_publication` computes the average annual citation rate across a node's entire lifespan. For nodes with stable accumulation curves (e.g. Kuhn, 64 years of consistent cross-domain citation), the mean is a good proxy for the current rate. For nodes with accelerating accumulation curves (foundation nodes, recently published), the mean systematically understates the current rate. The reported velocities should be interpreted accordingly: Kuhn's 111.6/yr is approximately the current rate; GPT-4's 7,651/yr is a lower bound on the current rate.

[^2]: **GPT-4 velocity is a lower bound.** GPT-4 was published in March 2023. Citation accumulation for a paper that rapidly becomes a field's foundational reference is not linear — it follows an adoption curve. Early citations are exploratory; later citations are structural (building on, comparing against, extending). The mean rate across three years (7,651/yr) blends the early exploratory phase with the current high-intensity structural phase. The current annual citation rate is almost certainly substantially higher than 7,651. When C2 time-series measurement is completed (see Section 5), the full curve will replace this scalar.

[^3]: **Protocol node velocity may mask a bell curve.** Protocol nodes tell a field how to act in the absence of a paradigm. Their citation trajectory may follow adoption lifecycle dynamics: slow initial uptake as the field discovers the protocol, rapid growth during adoption, a plateau during peak use, and gradual decline as the protocol is either superseded (a new paradigm replaces it) or fully internalized (the field no longer needs to cite it explicitly because it has become assumed). The mean rate for Kotter (308.4/yr over 14 years) cannot distinguish between a stable rate and a peaked curve. This is a target for C2 full temporal persistence measurement.

[^4]: **Cold = weight, not age.** The zone classification system uses citation count as the primary signal, not publication year. A paper published two years ago can be cold (foundation mode) if the field built on it at sufficient intensity. A paper published sixty years ago can be warm if it has been cited less than 5,000 times total. This is not a flaw — it is the correct behavior for a topology-reading instrument. The cold zone is where the weight is, not where the oldest papers are. Age is a correlate of cold-ness for gateway nodes (slow accumulation over decades eventually reaches the threshold) but not for foundation nodes (rapid accumulation reaches the threshold in years or months).

[^5]: **Velocity thresholds are corpus-specific.** The specific values (111/308/7,651 cites/yr) are empirical observations from one corpus — academic papers indexed by Semantic Scholar, seeded from physics and philosophy of science. Different citation cultures (legal scholarship, patent networks, software dependencies, social media) will produce different absolute velocity values. The hypothesis tested here is that the *ordinal relationship* holds universally: gateway < protocol < foundation in cold-entry velocity. This hypothesis is supported by the two-order-of-magnitude separation observed in this corpus but has not been tested across substrates. Researchers applying this methodology to other corpora should report their velocity distributions and ordinal relationships to contribute to cross-substrate validation.

[^6]: **The pre-digital boundary is approximately 1990, not a precise date.** The boundary is not a hard cutoff but a gradient. Papers published after 1995 tend to have reasonably complete reference graphs in Semantic Scholar. Papers from 1985–1995 have partial coverage. Papers before 1985 are largely dark. The stated boundary of ~1990 is a practical approximation based on the observations in this study — Kuhn (1962), The Essential Tension (1977), Schrödinger (1926), and Einstein SR (1905) all returned empty reference sets. Einstein SR had year=0 in the Semantic Scholar record, indicating the system has the node but cannot date or read its structure. The gradient means the pre-digital boundary should be treated as a zone, not a line.

---

## Supplementary Material

Full emergence log (16 entries), traversal scripts, and raw data outputs:
[github.com/lucent-research/context-space]

*All scripts are released under MIT license. The emergence log is the primary observational record — not a summary derived from the data, but the data itself, written at the moment of discovery.*
