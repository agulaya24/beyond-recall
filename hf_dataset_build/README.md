---
license: cc-by-4.0
language:
- en
pretty_name: Beyond Recall Benchmark
tags:
- behavioral-specification
- personalization
- representational-accuracy
- llm-evaluation
- digital-twin
configs:
- config_name: specifications
  data_files: specifications.jsonl
  default: true
- config_name: batteries
  data_files: batteries.jsonl
- config_name: facts
  data_files: facts.jsonl
- config_name: corpora
  data_files: corpora.jsonl
- config_name: results
  data_files: results.jsonl
---

# Beyond Recall Benchmark

Companion data for **Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization** ([arXiv:2605.28969](https://arxiv.org/abs/2605.28969)). Code: https://github.com/agulaya24/beyond-recall

## Benchmark inputs vs. experimental outputs
This dataset deliberately separates the **benchmark (data)** from the **results (experimental outputs)**.

**Benchmark (data):**
- `specifications` — behavioral specifications per subject (`layer`: anchors, core, predictions, brief, full_spec).
- `batteries` — held-out behavioral-prediction questions per subject.
- `facts` — extracted behavioral facts per subject.
- `corpora` — public-domain source autobiographies (14 subjects).

**Results (experimental outputs):**
- `results` — per-memory-system / per-judge evaluation outputs used in the paper.

## Usage
```python
from datasets import load_dataset
specs = load_dataset("agulaya24/beyond-recall", "specifications")
questions = load_dataset("agulaya24/beyond-recall", "batteries")
results = load_dataset("agulaya24/beyond-recall", "results")
```

## License
CC-BY-4.0 for specifications, facts, and results. Source corpora are public domain (Project Gutenberg / Internet Archive).
