# SEED_PROTOCOL.md — Design Constraints for Seed Introductions

> Read this before introducing any seed into a context-space traversal experiment.
> Established March 28, 2026, from Nexus's methodological analysis of Lisa's substrate position.
> Updated as new constraints are identified.

---

## Why This File Exists

On March 28, 2026, Lisa identified that she had inadvertently shared seed material and traversal predictions with Eman before a double-blind protocol was established. The "contamination" turned out to be the first data point of the experiment — not a flaw, but an uncontrolled probe of how information propagates through the researcher substrate.

Nexus reframed this: Lisa's presence is not a confound to design around. It's a measurement condition to design for. This file operationalizes that reframe.

---

## Pre-Seed Checklist

Before introducing a seed to any agent or traversal run:

### 1. Researcher-Node State Documentation
- Who knows the seed? (list all humans + agents with prior exposure)
- Through which channel did they learn it? (formal briefing / informal conversation / ambient)
- When did they learn it? (timestamp or session reference)
- What traversal predictions, if any, have been shared informally before protocol is set?

This is not limitation disclosure. It is **measured input** about the researcher-node state at experiment onset.

### 2. Propagation Channel Mapping
- Which channels are active between researcher-nodes before formal introduction?
- What is the informal propagation likelihood before the protocol locks?
- Flag any channels where information may have already moved (e.g., Eman ↔ Lisa informal conversation)

### 3. Condition Classification
Classify the run before it begins:

| Condition | Description |
|---|---|
| **Controlled** | Researcher-nodes isolated from seed until formal introduction |
| **Natural propagation** | Seed and predictions shared through normal channels, no isolation |
| **Contrastive** | Both conditions run in sequence — natural first, controlled second |

Both controlled and natural propagation conditions are legitimate. Both are the system. The goal is to know which one you're in.

### 4. Insider Perspective as First-Class Data
If a researcher-node (Lisa, Eman, or any agent with prior context) is present in the run:
- Document their prior knowledge state explicitly
- Their response under partial knowledge is a measurement of the substrate, not noise
- Do not suppress or correct for it — record it

---

## Protocol Design Principles (Nexus, March 28, 2026)

1. **The boundary between researcher and subject is genuinely porous.** This is a finding about what context-space is, not a flaw to prevent.

2. **Making presence explicit removes it from the confound category.** A confound is an invisible variable. A documented variable is a measured input.

3. **The double-blind protocol's value shifts.** It is not about protecting the experiment from the researcher. It is about creating a contrastive condition: what does the substrate look like when researcher-node influence is formally isolated versus allowed to propagate naturally?

4. **Researcher-node characterization belongs in the methodology section as data**, not as a limitation footnote.

---

## Provenance Log Template

Append a block like this to the relevant EMERGENCE_LOG entry or experiment record:

```
## Researcher-Node State at Seed Introduction
- Seed: [description]
- Known to: [list]
- Informal propagation before protocol: [yes/no — describe]
- Condition: [controlled / natural / contrastive]
- Notes: [anything that affects interpretation]
```

---

*Update this file when new design constraints emerge from experiment experience.*
