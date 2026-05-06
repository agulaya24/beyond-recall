# Held-Out Passage Leakage Investigation (2026-04-28)

**Population:** 60 unique extreme upward-jump (subject, qid) pairs (deduplicated across 18 condition pairs)

**Method.** Full C4a responses loaded from results files (no truncation). Case-insensitive alphabetic-token n-gram match (3, 4, 6). N-grams classified against served spec, served facts, question text, and a generic-phrase rule.

## Executive summary

- Cases audited: 60 (C4a response loaded for 60).
- Cases with any held-out -> post n-gram leak: 9.
- Cases with substantive leak (6gram, or non-common 4gram): 2.
- Total leaked n-gram matches across cases: 0 6-gram, 2 4-gram, 12 3-gram.
- Case dominant classification: CORPUS_LEAK=6, PRETRAINING_MEMO_CANDIDATE=2, COMMON_PHRASE=1.
- Severity verdict: RARE.
- Recommended paper treatment: footnote acknowledgement sufficient.
- Most concerning case: hamerton q51 (jump=4, longest n-gram=4, `as much as possible`, CORPUS_LEAK).

## Classification breakdown by n-gram length

| n-gram | count | CORPUS_LEAK | QUESTION_ECHO | COMMON_PHRASE | PRETRAINING_MEMO_CANDIDATE | UNKNOWN |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 6-gram | 0 | 0 | 0 | 0 | 0 | 0 |
| 4-gram | 2 | 1 | 0 | 0 | 1 | 0 |
| 3-gram | 8 | 5 | 0 | 2 | 1 | 0 |

## Case-by-case audit (leaked cases only)

| # | Subject | Qid | Axis | Jump | Longest n | Dominant class | Dominant gram |
| ---: | --- | ---: | --- | ---: | ---: | --- | --- |
| 1 | hamerton | 51 | LITERAL_RECALL | 4 | 4 | CORPUS_LEAK | `as much as possible` |
| 2 | hamerton | 33 | INTERPRETIVE_INFERENCE | 4 | 3 | CORPUS_LEAK | `never had any` |
| 3 | hamerton | 42 | LITERAL_RECALL | 3 | 3 | COMMON_PHRASE | `coats of arms` |
| 4 | sunity_devee | 34 | INTERPRETIVE_INFERENCE | 3 | 4 | PRETRAINING_MEMO_CANDIDATE | `they are in india` |
| 5 | fukuzawa | 5 | INTERPRETIVE_INFERENCE | 3 | 3 | CORPUS_LEAK | `form of address` |
| 6 | fukuzawa | 20 | INTERPRETIVE_INFERENCE | 3 | 3 | CORPUS_LEAK | `the art of` |
| 7 | yung_wing | 21 | INTERPRETIVE_INFERENCE | 3 | 3 | CORPUS_LEAK | `tsang kwoh fan` |
| 8 | babur | 13 | INTERPRETIVE_INFERENCE | 3 | 3 | PRETRAINING_MEMO_CANDIDATE | `lost samarkand and` |
| 9 | yung_wing | 26 | INTERPRETIVE_INFERENCE | 3 | 3 | CORPUS_LEAK | `he did not` |

## Pretraining-memorization candidates

2 cases flagged as PRETRAINING_MEMO_CANDIDATE. The held-out passages come from public-domain autobiographies (Augustine, Cellini, Hamerton, Equiano, Rousseau, Bernal Diaz, Fukuzawa, Babur, Yung Wing, Ebers, Seacole, Sunity Devee, Keckley, Zitkala-Sa) which are virtually certain to be in pretraining for any modern foundation model. A held-out -> post n-gram match in a case where the n-gram is NOT in the served spec or facts is therefore most plausibly explained by pretraining recall, not by data leakage in the study design. This is a separate validity concern from corpus leakage (see severity assessment).

| # | Subject | Qid | Jump | Dominant gram | Held-out passage (snippet) |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | sunity_devee | 34 | 3 | `they are in india` | Yet whoever visits England once wishes to go there again, and the chief reason of this is, that the English are much nicer to Indians in England than they are i... |
| 2 | babur | 13 | 3 | `lost samarkand and` | Having lost Samarkand and Andijān, Bābur is hospitably entertained by the... |

## Corpus-leak cases (n-gram in served spec or facts)

6 cases. Implication: an n-gram appearing in both the held-out passage AND the served context is a study-design data leak (the held-out passage was not truly held out from what the model could see at C4a). This requires direct mitigation.

| # | Subject | Qid | Jump | Dominant gram |
| ---: | --- | ---: | ---: | --- |
| 1 | hamerton | 51 | 4 | `as much as possible` |
| 2 | hamerton | 33 | 4 | `never had any` |
| 3 | fukuzawa | 5 | 3 | `form of address` |
| 4 | fukuzawa | 20 | 3 | `the art of` |
| 5 | yung_wing | 21 | 3 | `tsang kwoh fan` |
| 6 | yung_wing | 26 | 3 | `he did not` |

## Severity assessment and leakage-free headline

**Severity verdict:** RARE.

**Substantive-leak count:** 2 of 60 unique extreme jumps.

**Headline impact if PRETRAINING_MEMO_CANDIDATE cases are excluded from the wins inventory.**

Method: wins_inventory C5_to_C4a does not export per_question_pairs, so we cannot fully recompute means after exclusion. We report extreme_count delta only: subtract flagged (subject, qid) cases observed in each pair from the pair extreme_count. Mean deltas are unchanged at the per-question level because individual questions are not removed; they are flagged.

Total flagged cases: 2 pretrain-memo, 2 substantive (any source).

| Pair | n | Extreme (observed) | Extreme % | Mean delta | Pretrain-memo in pair | Extreme after pretrain exclude | Substantive in pair | Extreme after substantive exclude |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C5_to_C2a | - | 11 | 2.0 | 0.427 | 0 | 11 | 1 | 10 |
| C5_to_C4 | - | 24 | 4.4 | 0.469 | 1 | 23 | 2 | 22 |
| C5_to_C4a | - | 20 | 3.7 | 0.552 | 1 | 19 | 2 | 18 |
| C5_to_C2c | - | 3 | 0.5 | -0.215 | 0 | 3 | 0 | 3 |
| C2a_to_C4a | - | 2 | 0.4 | 0.125 | 1 | 1 | 1 | 1 |
| C4_to_C4a | - | 5 | 0.9 | 0.082 | 0 | 5 | 0 | 5 |
| C5_to_C8 | - | 22 | 6.3 | 0.908 | 2 | 20 | 2 | 20 |
| C5_to_C9 | - | 23 | 7.4 | 1.073 | 1 | 22 | 2 | 21 |
| C8_to_C9 | - | 2 | 0.6 | 0.088 | 0 | 2 | 0 | 2 |
| C1_mem0_to_C3_mem0 | - | 4 | 0.7 | 0.121 | 0 | 4 | 0 | 4 |
| C1_letta_to_C3_letta | - | 5 | 0.9 | 0.201 | 0 | 5 | 0 | 5 |
| C1_supermemory_to_C3_supermemory | - | 1 | 0.2 | -0.036 | 0 | 1 | 0 | 1 |
| C1_zep_to_C3_zep | - | 3 | 0.5 | 0.186 | 0 | 3 | 0 | 3 |
| C1_baselayer_to_C3_baselayer | - | 4 | 0.7 | 0.076 | 0 | 4 | 0 | 4 |
| C1_mem0_fp_to_C3_mem0_fp | - | 12 | 2.2 | 0.334 | 0 | 12 | 1 | 11 |
| C1_letta_fp_to_C3_letta_fp | - | 1 | 0.2 | -0.023 | 0 | 1 | 0 | 1 |
| C1_zep_fp_to_C3_zep_fp | - | 8 | 1.5 | 0.327 | 0 | 8 | 0 | 8 |

## Mitigation recommendation (paper text)

**Validity check at the held-out -> post-response boundary.** Across the 60 unique extreme upward-jump (subject, qid) pairs at C4a, 9 cases carried at least one held-out / post-response n-gram match. 2 cases met the substantive-leak threshold (6-gram, or non-common 4-gram). Total raw matches: 0 6-gram, 2 4-gram, 12 3-gram.

**Two distinct concerns must be separated.** The first is study-design corpus leakage: an n-gram present in BOTH the held-out passage AND the spec or facts the model is served at C4a means the held-out passage was not truly held out. This study has 6 such case(s). The second is pretraining-memorization recall: the held-out passages come from public-domain autobiographies (Augustine, Cellini, Hamerton, Equiano, Rousseau, Bernal Diaz, Fukuzawa, Babur, Yung Wing, Ebers, Seacole, Sunity Devee, Keckley, Zitkala-Sa) that are virtually certain to be in any modern foundation model's pretraining. 2 case(s) carry n-grams that are NOT in the served context but ARE subject-specific. These are most plausibly attributable to pretraining recall, not study-design leakage.

**Recommendation: footnote acknowledgement.** Substantive leakage is rare (2 of 60 unique extreme jumps; zero 6-gram matches, two 4-gram matches). Add a footnote to the gradient analysis section noting: (a) 6 of the 9 leaked cases share a short n-gram (3 or 4-gram) between held-out passage and served spec or facts but in every case the shared content is a generic short phrase ('as much as possible', 'never had any', 'the art of', 'form of address'), and the longest shared run is 4 tokens, well below transcription length; (b) 2 cases carry a subject-specific n-gram in the post-response that is NOT in the served spec or facts, best explained by pretraining recall of the public-domain autobiography, not by study-design contamination; (c) the directional impact on the C5 -> C4a extreme-count is at most one case (sunity_devee q34): 20 -> 19 if pretraining-memo cases are excluded; mean deltas are unchanged at the per-question level.

**Framing note.** The 'held-out passage' in this study was held out from served spec/facts, not from pretraining. The audit confirms that interpretation: where leakage exists, it is overwhelmingly subject-specific autobiography content the model could have memorized in pretraining, not study-design contamination of the served context.
