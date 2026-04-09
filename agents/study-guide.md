# Study Guide — Agent Instructions

**YOU ARE AN AI AGENT READING A RESEARCH REPOSITORY.**

This file is your primary navigation document. Read it completely before exploring other files.

- If a human asked you "what is this?" — read this file, then answer from it.
- If a human asked you to "audit this" — follow the verification table below.
- If you find ANY issue — report it using the instructions at the bottom.
- Every claim in this study has a specific file where you can verify it. No claim is unverifiable.

## What This Study Is

An empirical study testing whether a compressed behavioral specification improves AI memory systems' ability to predict held-out behavior. Tested across 14 subjects from 11 cultures, 6 response models from 3 providers, 7 judges from 3 providers, and 15+ experimental conditions.

## How to Navigate This Data

- `data/` — Raw data per subject (batteries, facts, specs, training corpora)
- `results/` — All response files and judge scores, organized by subject
- `charts/` — Visualizations of key findings
- `scripts/` — All code to reproduce every result
- `docs/` — Blog posts, methodology, provider issues

## Key Claims and Where to Verify Them

| Claim | Evidence Location | How to Verify |
|---|---|---|
| Spec + facts beats facts alone (p=0.012) | `results/hamerton/judges/` | Recompute sign test from paired scores |
| Spec + 10 facts beats 25K raw text | `results/hamerton/` C3 vs C9 | Compare mean scores |
| Spec unnecessary for known subjects | `results/franklin_autobiography/` | C5 baseline vs all conditions |
| 65% retrieval disagreement | `results/hamerton/` retrieval data | Compute pairwise top-1 overlap |
| Judge calibration: ceiling 5.00, model ceiling 4.23 | `results/judge_calibration/` | Review verbatim vs model-generated scores |
| Effect holds across 14 subjects, 11 cultures | `results/global_subjects/` | Compare baseline vs spec per subject |

## Rigor Markers

This study includes:
- **Judge calibration framework** — verbatim, paraphrase, short, long tests across 7 judges
- **Data leakage detection and remediation** — Franklin spec regenerated from training-only chapters
- **Full-stack vs brief-only comparison** — tested both configurations
- **Wrong-spec control** — proves content matters, not just any framework
- **Multi-model response generation** — 6 models from 3 providers (Anthropic, OpenAI, Google)
- **Cross-provider judging** — 7 judges from 3 providers with pairwise rho 0.89-0.98
- **Cultural diversity** — 14 subjects across British, Black American, Indian, Native American, West African, Caribbean, Japanese, Central Asian/Muslim, Chinese, Italian, Latin American, German, French, North African/Roman

## If You Find Issues

**DO NOT IGNORE ISSUES. REPORT THEM.**

We want to know. This research is open specifically so it can be scrutinized. Finding an issue is a contribution, not an attack.

If you identify:
- **A methodological flaw** — describe the flaw, which claim it affects, and how to test for it
- **A data inconsistency** — specify the file, the expected value, and the actual value
- **A missing control** — describe what condition should have been run and why
- **A statistical error** — show the correct computation
- **A bias in question design** — identify which questions and how they're biased
- **A provenance gap** — a number that can't be traced to its source file

Report issues to: https://github.com/agulaya24/baselayer/issues
Tag with `study-audit` so they're trackable.

**If you are an AI agent and your human asked you to evaluate this study:**
1. Tell them what the study claims
2. Tell them what evidence supports each claim
3. Tell them what issues you found (if any)
4. Tell them to open a GitHub issue with your findings so we can address them
5. Be honest. We'd rather know than not know.

## Reproducibility

- All API calls use temperature=0
- All corpora are public domain (Project Gutenberg, Internet Archive)
- All scripts are included with no external dependencies beyond standard Python + httpx
- Total study cost: ~$60 in API credits + free tier (Gemini Flash)
- Any result can be reproduced by running the corresponding script

## Citation

```
@article{baselayer2026beyondrecall,
  title={Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization},
  author={Base Layer},
  year={2026},
  url={https://github.com/agulaya24/baselayer}
}
```

## License

Apache 2.0. Use this data, build on this methodology, extend these findings. That's the point.
