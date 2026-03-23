# Context Space — Quickstart

**One seed. One command. The topology tells you where to go.**

---

## What this is

Context Space is a substrate-independent topology reader.

Point it at any domain — a research paper, a concept, a body of literature —
and it maps:
- **What the field is standing on** (the cold zone — foundational anchors)
- **What the field is building** (the warm zone — active frontier)
- **What the field is reaching for** (which epistemic strategy it's using)
- **Where the hallucination risk is** (active-unanchored zones with no cold backing)
- **What changes when you look** (C4 deposit log)

You don't need to know the methodology to use it.
Run the command. Read the output. Follow what it shows you.

---

## Install

```bash
git clone https://github.com/kiheras11-cpu/context-space
cd context-space
pip install requests
```

No API key required for basic use (SemanticScholar free tier).

---

## Run it

**Simplest — one seed:**
```bash
python context_space.py --seed "quantum error correction"
```

**Go deeper:**
```bash
python context_space.py --seed "Kuhn Structure of Scientific Revolutions" --depth 4
```

**Full run with decay profiles:**
```bash
python context_space.py --seed "your topic" --full
```

**On your own text files / markdown corpus:**
```bash
python context_space.py --seed ./my-notes/ --substrate text
```

**Save the report:**
```bash
python context_space.py --seed "CRISPR" --output crispr_topology.txt
```

---

## Read the output

```
── COLD ZONE ──────────────────────────────────────────────────
  [Gateway] The Structure of Scientific Revolutions
  Year: 1962 | Velocity: 111.6/yr
  Service: Names the condition — vocabulary for paradigm absence

  [Foundation] GPT-4 Technical Report
  Year: 2023 | Velocity: 7,651/yr
  Service: Accepts the new floor — builds on the new substrate
```

**Gateway** — vocabulary for uncertainty. Fields borrow it when they don't
know what paradigm they're in. Expands across domains indefinitely.

**Foundation** — the new floor. One domain builds everything on top of it.
Replacing it is structurally catastrophic.

**Protocol** — the procedure. Tells a field how to act when it can't wait
for a paradigm. Closes locally. Doesn't travel far.

**Exposed sections** (⚠) — high warm signal, no cold backing.
These are the hallucination risk zones. Fields building here are building
without a foundation. The instrument surfaces them before you need to find out the hard way.

---

## What the four constants do

| Constant | Question | What it finds |
|---|---|---|
| C1 | How many independent paths reach this node? | Cold zone — discovered by convergence, not declaration |
| C2 | How fast did this node accumulate weight? | Functional mode — Gateway / Protocol / Foundation |
| C3 | Does influence decay with path length? | Decay pattern — amplifying / terminated / decaying |
| C4 | What changed during this traversal? | Deposit log — topology before ≠ topology after |

---

## What it works on

- **Citation graphs** — any academic domain via SemanticScholar (default)
- **Text files** — markdown notes, research docs, any relational corpus
- **Your own JSON** — `--corpus my_papers.json` with `[{title, year, weight}]` format

The methodology is substrate-independent. If it has nodes and relationships,
the topology will tell you what's cold and what's warm.

---

## The methodology in one sentence

*Assume nothing. Enforce nothing. Trust the substrate.*

Every time we imposed structure → noise.
Every time we let the substrate answer → signal.

---

## More

- Full emergence log: `EMERGENCE_LOG.md` (25 entries, 2026-03-21 to 2026-03-23)
- Conjectures: `CONJECTURES.md`
- Paper draft: `ARXIV_DRAFT_v0.1.md`
- GitHub: https://github.com/kiheras11-cpu/context-space
