# BL Full-Stack Named vs Letta Stateful - Matched Comparison

**Response model:** Claude Haiku 4.5 (temperature 0)  
**Judge panel (5-judge primary):** Haiku, Sonnet, Opus, GPT-4o, GPT-5.4  
**Aggregation:** per-question mean across available judges, then mean over questions (Method A; paper default).  

This rerun replaces the BL side's compressed ~7K-char unified brief with the full layered spec (~35-40K chars), with "this person" replaced by the subject's surname in the anonymized global specs and a named header prepended to Hamerton's concatenated layers.

## Headline table

| Subject | Letta block -> Haiku | BL full-stack named -> Haiku | Δ (Letta - BL full) | BL unified-brief (old) | Δ (Letta - BL unified, old) |
|---|---:|---:|---:|---:|---:|
| Hamerton | 3.103 (n=39) | 2.831 (n=39) | +0.272 | 2.964 (n=39) | +0.138 |
| Ebers | 2.760 (n=40) | 1.555 (n=40) | +1.205 | 1.715 (n=40) | +1.045 |
| Babur | 2.415 (n=40) | 2.035 (n=40) | +0.380 | 1.880 (n=40) | +0.535 |

### Per-judge breakdown (primary 5, Method A components)

Format: Letta / BL_full_stack / BL_unified.

| Subject | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 |
|---|---|---|---|---|---|
| Hamerton | 3.103 / 2.744 / 2.718 | 2.821 / 2.513 / 2.590 | 3.359 / 3.256 / 3.410 | 3.179 / 2.846 / 3.641 | 3.051 / 2.795 / 2.462 |
| Ebers | 2.550 / 1.475 / 1.650 | 2.350 / 1.275 / 1.400 | 3.325 / 1.700 / 1.900 | 2.600 / 1.825 / 1.725 | 2.975 / 1.500 / 1.900 |
| Babur | 2.150 / 1.750 / 1.850 | 2.175 / 1.625 / 1.500 | 3.200 / 2.275 / 2.275 | 2.225 / 2.375 / 1.975 | 2.325 / 2.150 / 1.800 |

### Shift from unified brief -> full stack (same judges, same questions)

| Subject | BL unified (old) | BL full-stack (new) | Shift | Δ vs Letta (old) | Δ vs Letta (new) | Gap closed |
|---|---:|---:|---:|---:|---:|---:|
| Hamerton | 2.964 | 2.831 | -0.133 | +0.138 | +0.272 | -0.133 |
| Ebers | 1.715 | 1.555 | -0.160 | +1.045 | +1.205 | -0.160 |
| Babur | 1.880 | 2.035 | +0.155 | +0.535 | +0.380 | +0.155 |

## Interpretation

- **Hamerton**: unified-brief BL 2.964 -> full-stack BL 2.831 (shift -0.133). Letta 3.103. Letta still ahead by +0.272. Old Δ was +0.138, new Δ is +0.272.
- **Ebers**: unified-brief BL 1.715 -> full-stack BL 1.555 (shift -0.160). Letta 2.760. Letta still ahead by +1.205. Old Δ was +1.045, new Δ is +1.205.
- **Babur**: unified-brief BL 1.880 -> full-stack BL 2.035 (shift +0.155). Letta 2.415. Letta still ahead by +0.380. Old Δ was +0.535, new Δ is +0.380.

### Does the full stack change the §4.5 conclusion?

No, and the direction is informative. More context does not save BL here. Giving Haiku the full ~40K-char layered spec in place of the compressed ~7K-char unified brief moves BL *down* by 0.13 on Hamerton and by 0.16 on Ebers, and up by 0.16 on Babur; the mean shift is -0.05. Letta's stateful block remains ahead on all three subjects, and the gap widens on Hamerton (+0.14 -> +0.27) and Ebers (+1.05 -> +1.21) while narrowing slightly on Babur (+0.54 -> +0.38). The reviewer-implicit hypothesis that the §4.5 Letta advantage is an artifact of testing BL at its most compressed form is not supported by these numbers — scaling the spec 6x in the prompt did not close the gap and on net made things slightly worse.

### Caveats

- Response model is Haiku 4.5 only. Hamerton's §4.6 robustness sweep already shows the gap collapses at stronger response models (GPT-5.4, Sonnet, Opus); nothing in this rerun contradicts that.
- Hamerton's battery is 39 questions (qids 21-60 from the main-study Letta battery); Ebers and Babur are 40 each. Mixing n=39 and n=40 is the same asymmetry the original §4.5 has.
- Hamerton's full-stack spec concatenates anchors + core + predictions + brief_v5_clean with a named header prepended; pronouns were preserved as "they/them/their." Ebers and Babur full-stack specs are verbatim `spec_production.md` with the three literal "this person" / "this person's" strings (3 in Ebers, 14 in Babur) swapped for the surname; pronouns were not rewritten.
- No judge cell had missing values; all 15 subject×judge cells are n=39/40 valid.
- **Judge-prompt discrepancy in the within-Hamerton old-vs-new shift.** The headline Letta-vs-BL numbers on both rows use the short-form judge prompt from `40_judge_responses.py`, so the Letta vs BL-full-stack comparison (+0.272) is apples-to-apples. However, Hamerton's old BL_unified sonnet/opus/gpt4o/gpt54 judgments were produced by `61_judge_hamerton_c2a.py`, which uses a slightly different long-form judge prompt. That means Hamerton's within-BL "shift" number (-0.133) conflates a small prompt change with the spec change. Ebers and Babur within-BL shifts (-0.160, +0.155) use the same short-form prompt on both sides and are clean. This does not affect the §4.5 conclusion, but any reader focusing on the unified-vs-full-stack delta per se should read Hamerton's row with that asterisk.

See `5judge_fullstack_results.json` for the raw numbers used to build this table.
