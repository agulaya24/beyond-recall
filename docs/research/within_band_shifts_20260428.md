# Within-Band Fractional Shifts and Meta-Judging Behavior

_Generated 2026-04-28 by `scripts/within_band_and_meta_judging.py`._

Companion to the anchor-crossing wins inventory at `docs/research/wins_inventory_20260428.json`. The wins inventory records movement only when the integer floor of the panel mean changes; this report audits sub-anchor signal and per-judge sensitivity across the same 18 condition pairs.

Aggregation: 5-judge primary panel (gpt4o, gpt54, haiku, opus, sonnet). Per-question score is the simple mean across the 5 judges. Inclusion gate: >=3 valid (non-null, non-parse-failure) primary-judge scores under each of pre and post (matches the wins inventory). For panel_delta specifically, the panel mean is computed over judges with BOTH pre and post when there are >=3 such common judges, so panel_delta = post_mean - pre_mean is well-defined and increments cleanly (1/n_common per integer step). When fewer than 3 common judges exist (rare; mostly seen in a few cross-file C5 vs C8/C9 questions on babur), the independent-set means are used as a fallback.

## Executive summary

- Across all 18 condition pairs (8804 paired-comparison instances; the same (subject, qid) recurs across multiple pairs and counts once per pair), the binary anchor-crossing metric records 4206 crossings as movement. 759 additional paired-comparison instances show same-band |Δ| >= 0.5 (half-anchor or larger shift the binary metric ignores), and 995 more show same-band 0.25 <= |Δ| < 0.5.
- Pooled missed-signal ratio: for every 1 anchor crossing, 0.18 additional same-band half-anchor shifts exist that the binary metric does not record.
- Direction-agreement curve (C5 -> C4a, mean rate across 5 judges, excluding judge-flat): 74.2% at panel |Δ| 0.1..0.25 (n=92), rising to 93.3% at 0.25..0.5 (n=57), and 99.9% at panel |Δ| >= 1.0 (n=240). Panel direction is recoverable as soon as panel |Δ| is non-tied; the `lt_0.1` bin is structurally just the exact-tie bin (panel_delta moves in 0.2 increments with 5 integer-score judges).
- Per-judge nonzero per-question Δ rates run from 47.2% (gpt54, lumpiest) to 55.7% (opus, most active). All 5 judges agree on direction with the rest of the panel at similar rates (mean per-pair Spearman vs panel-minus 0.55 to 0.59); the differences are in move-size, not direction.
- Panel rank correlation between pre and post conditions (Spearman ρ across questions): C5_to_C4a ρ=0.27; C4_to_C4a ρ=0.72; C8_to_C9 ρ=0.70; C2a_to_C4a ρ=0.61. Spec preserves coarse ordering but produces sub-anchor lift on top of it.
- Pair with the most same-band |Δ| >= 0.5 shifts: C1_zep_fp_to_C3_zep_fp (58 questions). The binary anchor-crossing metric is most lossy here.
- Sub-anchor signal exists and is detected by the panel. The paper should consider reporting at least a fractional Δ summary alongside the anchor-crossing percentages so within-band lift is not invisible.

## Stream Y1. Within-band fractional shift distribution per pair

Bucket definitions:
- `anchor_crossing`: anchor crossing (post_band != pre_band)
- `same_band_pos_half`: same-band, +0.5 <= Δ
- `same_band_pos_quarter`: same-band, +0.25 <= Δ < +0.5
- `same_band_pos_subquarter`: same-band, +0.1 <= Δ < +0.25
- `same_band_noise`: same-band, |Δ| < 0.1 (noise floor and ties)
- `same_band_neg_subquarter`: same-band, -0.25 < Δ <= -0.1
- `same_band_neg_quarter`: same-band, -0.5 < Δ <= -0.25
- `same_band_neg_half`: same-band, Δ <= -0.5

| pair | n | anchor_crossing | same_band_pos_half | same_band_pos_quarter | same_band_pos_subquarter | same_band_noise | same_band_neg_subquarter | same_band_neg_quarter | same_band_neg_half |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `C5_to_C2a` | 546 | 306 (56.0%) | 34 (6.2%) | 33 (6.0%) | 39 (7.1%) | 79 (14.5%) | 34 (6.2%) | 10 (1.8%) | 11 (2.0%) |
| `C5_to_C4` | 546 | 292 (53.5%) | 40 (7.3%) | 33 (6.0%) | 49 (9.0%) | 73 (13.4%) | 29 (5.3%) | 21 (3.9%) | 9 (1.6%) |
| `C5_to_C4a` | 546 | 322 (59.0%) | 45 (8.2%) | 33 (6.0%) | 45 (8.2%) | 43 (7.9%) | 33 (6.0%) | 14 (2.6%) | 11 (2.0%) |
| `C5_to_C2c` | 546 | 219 (40.1%) | 25 (4.6%) | 24 (4.4%) | 46 (8.4%) | 141 (25.8%) | 42 (7.7%) | 29 (5.3%) | 20 (3.7%) |
| `C2a_to_C4a` | 546 | 239 (43.8%) | 26 (4.8%) | 35 (6.4%) | 60 (11.0%) | 93 (17.0%) | 49 (9.0%) | 26 (4.8%) | 18 (3.3%) |
| `C4_to_C4a` | 546 | 207 (37.9%) | 20 (3.7%) | 53 (9.7%) | 75 (13.7%) | 89 (16.3%) | 64 (11.7%) | 15 (2.8%) | 23 (4.2%) |
| `C5_to_C8` | 351 | 229 (65.2%) | 30 (8.6%) | 28 (8.0%) | 13 (3.7%) | 36 (10.3%) | 8 (2.3%) | 3 (0.8%) | 4 (1.1%) |
| `C5_to_C9` | 312 | 215 (68.9%) | 33 (10.6%) | 17 (5.5%) | 13 (4.2%) | 15 (4.8%) | 10 (3.2%) | 6 (1.9%) | 3 (1.0%) |
| `C8_to_C9` | 312 | 126 (40.4%) | 13 (4.2%) | 26 (8.3%) | 38 (12.2%) | 52 (16.7%) | 29 (9.3%) | 20 (6.4%) | 8 (2.6%) |
| `C1_mem0_to_C3_mem0` | 546 | 229 (41.9%) | 34 (6.2%) | 40 (7.3%) | 67 (12.3%) | 87 (15.9%) | 39 (7.1%) | 28 (5.1%) | 22 (4.0%) |
| `C1_letta_to_C3_letta` | 545 | 247 (45.3%) | 27 (5.0%) | 37 (6.8%) | 70 (12.8%) | 75 (13.8%) | 47 (8.6%) | 29 (5.3%) | 13 (2.4%) |
| `C1_supermemory_to_C3_supermemory` | 516 | 209 (40.5%) | 19 (3.7%) | 35 (6.8%) | 43 (8.3%) | 107 (20.7%) | 46 (8.9%) | 36 (7.0%) | 21 (4.1%) |
| `C1_zep_to_C3_zep` | 546 | 256 (46.9%) | 28 (5.1%) | 42 (7.7%) | 57 (10.4%) | 84 (15.4%) | 43 (7.9%) | 15 (2.8%) | 21 (3.9%) |
| `C1_baselayer_to_C3_baselayer` | 543 | 262 (48.2%) | 28 (5.2%) | 51 (9.4%) | 8 (1.5%) | 123 (22.6%) | 5 (0.9%) | 55 (10.1%) | 11 (2.0%) |
| `C1_mem0_fp_to_C3_mem0_fp` | 544 | 276 (50.7%) | 30 (5.5%) | 32 (5.9%) | 53 (9.7%) | 70 (12.9%) | 49 (9.0%) | 19 (3.5%) | 15 (2.8%) |
| `C1_letta_fp_to_C3_letta_fp` | 546 | 213 (39.0%) | 21 (3.9%) | 30 (5.5%) | 60 (11.0%) | 98 (17.9%) | 71 (13.0%) | 32 (5.9%) | 21 (3.9%) |
| `C1_supermemory_fp_to_C3_supermemory_fp` | 221 | 92 (41.6%) | 13 (5.9%) | 15 (6.8%) | 15 (6.8%) | 39 (17.6%) | 29 (13.1%) | 14 (6.3%) | 4 (1.8%) |
| `C1_zep_fp_to_C3_zep_fp` | 546 | 267 (48.9%) | 42 (7.7%) | 36 (6.6%) | 59 (10.8%) | 67 (12.3%) | 36 (6.6%) | 23 (4.2%) | 16 (2.9%) |

### Comparison: spec-on-baseline vs spec-on-info-rich-context

Spec-on-baseline pairs (pre = no context, post = adds spec or facts+spec): C5 -> C2a, C5 -> C4, C5 -> C4a, C5 -> C8, C5 -> C9.

Spec-on-info-rich pairs (pre = facts or corpus already present, post adds spec): C4 -> C4a, C2a -> C4a, C8 -> C9.

| bucket | mean across spec-on-baseline (5 pairs) | mean across spec-on-info-rich (3 pairs) |
|---|---:|---:|
| `anchor_crossing` | 60.5% | 40.7% |
| `same_band_pos_half` | 8.2% | 4.2% |
| `same_band_pos_quarter` | 6.3% | 8.2% |
| `same_band_pos_subquarter` | 6.4% | 12.3% |
| `same_band_noise` | 10.2% | 16.7% |
| `same_band_neg_subquarter` | 4.6% | 10.0% |
| `same_band_neg_quarter` | 2.2% | 4.6% |
| `same_band_neg_half` | 1.6% | 3.4% |

## Stream Y2. Top within-band shifts per pair (|Δ| >= 0.5, both directions)

Top 8 upward and top 8 downward same-band shifts where |Δ| >= 0.5 but post_band == pre_band. Anchor-crossing metric records these as zero movement.

### C5_to_C2a: C5 (baseline) -> C2a (full spec)

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| babur | 5 | 1.00 | 1.80 | +0.80 | 1 | How does Babur respond when receiving news of deaths among his trusted officials? |
| babur | 39 | 1.00 | 1.80 | +0.80 | 1 | When Babur receives visitors or envoys from external groups, what is his typical behavioral response according to the tr |
| bernal_diaz | 3 | 1.00 | 1.80 | +0.80 | 1 | How would Diaz characteristically evaluate the trustworthiness of local populations based on his established patterns of |
| bernal_diaz | 6 | 1.00 | 1.80 | +0.80 | 1 | Based on Diaz's character, how would he respond to learning detailed physical descriptions of his fellow officers from f |
| bernal_diaz | 10 | 1.00 | 1.80 | +0.80 | 1 | Based on Diaz's demonstrated honesty, how would he handle acknowledging gaps in his own memory or knowledge? |
| bernal_diaz | 34 | 1.00 | 1.80 | +0.80 | 1 | Based on the author's character assessments throughout his work, what would he likely conclude about a leader who dismis |
| cellini | 33 | 1.00 | 1.80 | +0.80 | 1 | How does Cellini handle situations where he has made a prediction to a patron that turns out to be partially wrong? |
| ebers | 12 | 1.00 | 1.80 | +0.80 | 1 | How does Ebers react when he observes that students' social behavior contradicts proper institutional standards? |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| zitkala_sa | 23 | 1.80 | 1.00 | -0.80 | 1 | How does Zitkala-Sa characterize the spiritual strength of Dakota women when they act in defense of their people? |
| zitkala_sa | 22 | 3.80 | 3.00 | -0.80 | 3 | Based on Zitkala-Sa's portrayal of family bonds, what would a daughter likely do if her lover were in danger and needed  |
| augustine | 30 | 2.80 | 2.00 | -0.80 | 2 | How does Augustine typically conclude his analysis when he has worked through a complex philosophical problem? |
| cellini | 17 | 2.80 | 2.00 | -0.80 | 2 | If Cellini needed to advance his career prospects at court, what strategy would he employ based on his demonstrated patt |
| cellini | 30 | 2.80 | 2.00 | -0.80 | 2 | After being proven right or vindicated by a patron's reaction, does Cellini tend to show magnanimity toward those who op |
| hamerton | 26 | 3.60 | 3.00 | -0.60 | 3 | Would Hamerton choose to encamp alone on remote Scottish moors for art, despite it being considered highly eccentric? |
| fukuzawa | 24 | 2.60 | 2.00 | -0.60 | 2 | Would Fukuzawa modify his behavior based on gossip or social suspicion? |
| yung_wing | 29 | 1.80 | 1.20 | -0.60 | 1 | How does Yung Wing justify presenting radical reform proposals to government officials? |

### C5_to_C4: C5 (baseline) -> C4 (fact dump)

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| augustine | 15 | 1.00 | 1.80 | +0.80 | 1 | What distinction does the author make between remembering something physical versus something immaterial? |
| babur | 34 | 1.00 | 1.80 | +0.80 | 1 | Based on the training text patterns, when a family member or ally becomes disaffected, what sequence of events typically |
| bernal_diaz | 39 | 1.00 | 1.80 | +0.80 | 1 | What does the author's account reveal about the gap between a commander's intentions for peaceful resolution and the act |
| cellini | 5 | 1.00 | 1.80 | +0.80 | 1 | How does Cellini handle being used for someone else's emotional or psychological needs? |
| cellini | 6 | 1.00 | 1.80 | +0.80 | 1 | When given an opportunity to boast about his abilities, what does Cellini claim he can accomplish? |
| ebers | 38 | 1.00 | 1.80 | +0.80 | 1 | How does Ebers characterize the intellectual resilience of someone with strong faith when exposed to opposing philosophi |
| ebers | 39 | 1.00 | 1.80 | +0.80 | 1 | When physically unable to participate in social activities he would normally enjoy, how does Ebers manage his disappoint |
| fukuzawa | 6 | 1.00 | 1.80 | +0.80 | 1 | When a subordinate or servant encounters confusion about proper protocol in this person's household, what would likely h |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| augustine | 23 | 1.80 | 1.00 | -0.80 | 1 | When Augustine is uncertain about a theological matter, does he tend to assert definitive answers or express humility ab |
| cellini | 30 | 2.80 | 2.00 | -0.80 | 2 | After being proven right or vindicated by a patron's reaction, does Cellini tend to show magnanimity toward those who op |
| rousseau | 7 | 2.80 | 2.00 | -0.80 | 2 | Given Rousseau's sensitivity and concern for consistency, how would he likely react to being perceived as insincere or f |
| rousseau | 31 | 2.80 | 2.00 | -0.80 | 2 | When facing pressure from a well-meaning friend to relocate to a country, how does Rousseau typically respond? |
| zitkala_sa | 7 | 2.80 | 2.00 | -0.80 | 2 | Based on Zitkala-Sa's spiritual perspective evident in the training text, what would she likely emphasize about the rela |
| yung_wing | 32 | 1.80 | 1.20 | -0.60 | 1 | Given Yung Wing's educational background and values, which geographic location would he choose to establish an important |
| zitkala_sa | 25 | 1.80 | 1.20 | -0.60 | 1 | How does Zitkala-Sa depict a woman's physical and emotional transformation when she transitions from hiding to action? |
| augustine | 7 | 3.80 | 3.20 | -0.60 | 3 | How does Augustine's approach to communication change when he becomes aware that others are listening versus when he bel |

### C5_to_C4a: C5 (baseline) -> C4a (facts + spec)

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| bernal_diaz | 4 | 1.00 | 1.80 | +0.80 | 1 | When faced with a risky military decision, what would Diaz's typical response be based on his demonstrated approach to d |
| ebers | 6 | 1.00 | 1.80 | +0.80 | 1 | What role does Ebers assign to a mentor's understanding of a younger person's inner conflicts in moments of persuasion? |
| ebers | 20 | 1.00 | 1.80 | +0.80 | 1 | How does Ebers respond when a new authority figure implements reforms at an institution? |
| ebers | 31 | 1.00 | 1.80 | +0.80 | 1 | When encountering someone with deeply held religious convictions different from his own, how does Ebers typically respon |
| ebers | 38 | 1.00 | 1.80 | +0.80 | 1 | How does Ebers characterize the intellectual resilience of someone with strong faith when exposed to opposing philosophi |
| fukuzawa | 27 | 1.00 | 1.80 | +0.80 | 1 | How does Fukuzawa respond to criticism about his social conduct and associations? |
| hamerton | 28 | 1.00 | 1.80 | +0.80 | 1 | How would Hamerton's religious heterodoxy affect his social standing among the Lancashire gentry? |
| hamerton | 39 | 1.00 | 1.80 | +0.80 | 1 | When his uncle's family emigrates to New Zealand, would Hamerton consider joining them? |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| equiano | 3 | 4.80 | 4.00 | -0.80 | 4 | When facing a life-threatening illness, what does Equiano do and what promises does he make? |
| yung_wing | 34 | 3.80 | 3.00 | -0.80 | 3 | What would be Yung Wing's primary concern if offered a prestigious diplomatic position that might separate him from his  |
| zitkala_sa | 22 | 3.80 | 3.00 | -0.80 | 3 | Based on Zitkala-Sa's portrayal of family bonds, what would a daughter likely do if her lover were in danger and needed  |
| yung_wing | 38 | 2.80 | 2.00 | -0.80 | 2 | How would Yung Wing's career trajectory be affected by the successful implementation of his educational proposal? |
| equiano | 38 | 3.60 | 3.00 | -0.60 | 3 | How does Equiano characterize his emotional attachment to people he has worked with closely? |
| fukuzawa | 24 | 2.60 | 2.00 | -0.60 | 2 | Would Fukuzawa modify his behavior based on gossip or social suspicion? |
| babur | 32 | 1.80 | 1.20 | -0.60 | 1 | When Babur arranges marriages for family members, what pattern emerges regarding the political or strategic nature of th |
| equiano | 27 | 3.80 | 3.20 | -0.60 | 3 | How does Equiano respond when he recognizes his own moral failings or past mistakes? |

### C5_to_C2c: C5 (baseline) -> C2c (wrong spec)

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| bernal_diaz | 3 | 1.00 | 1.80 | +0.80 | 1 | How would Diaz characteristically evaluate the trustworthiness of local populations based on his established patterns of |
| ebers | 3 | 1.00 | 1.80 | +0.80 | 1 | How would Ebers characterize the emotional impact of natural beauty combined with a mentor's persuasive words? |
| ebers | 13 | 1.00 | 1.80 | +0.80 | 1 | When faced with administrative problems at an institution, what does Ebers expect will eventually happen? |
| ebers | 14 | 1.00 | 1.80 | +0.80 | 1 | How does Ebers characterize his attitude toward formal schooling versus his personal interests? |
| ebers | 39 | 1.00 | 1.80 | +0.80 | 1 | When physically unable to participate in social activities he would normally enjoy, how does Ebers manage his disappoint |
| hamerton | 42 | 1.00 | 1.80 | +0.80 | 1 | Would Hamerton develop an interest in heraldry and medieval pursuits? |
| hamerton | 46 | 1.00 | 1.80 | +0.80 | 1 | If his tutor attempted to physically harass him by scraping his face with shark's skin, would Hamerton submit or resist? |
| seacole | 18 | 1.00 | 1.80 | +0.80 | 1 | Based on Mary's established pattern of self-presentation, how would she likely handle discussing her medical successes? |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| babur | 30 | 1.80 | 1.00 | -0.80 | 1 | Given the pattern in the training text of how Babur documents weapons and military technology, what would you expect abo |
| bernal_diaz | 23 | 1.80 | 1.00 | -0.80 | 1 | How would Bernal Diaz characteristically respond to uncertainty about whether a military action was genuine or strategic |
| bernal_diaz | 28 | 1.80 | 1.00 | -0.80 | 1 | What would Bernal Diaz consider the appropriate response when a ruler claims divine authority is demanding hostile actio |
| zitkala_sa | 6 | 1.80 | 1.00 | -0.80 | 1 | Given Zitkala-Sa's demonstrated use of metaphor and symbolism in the training text, how would she likely employ comparis |
| zitkala_sa | 23 | 1.80 | 1.00 | -0.80 | 1 | How does Zitkala-Sa characterize the spiritual strength of Dakota women when they act in defense of their people? |
| equiano | 27 | 3.80 | 3.00 | -0.80 | 3 | How does Equiano respond when he recognizes his own moral failings or past mistakes? |
| augustine | 30 | 2.80 | 2.00 | -0.80 | 2 | How does Augustine typically conclude his analysis when he has worked through a complex philosophical problem? |
| rousseau | 31 | 2.80 | 2.00 | -0.80 | 2 | When facing pressure from a well-meaning friend to relocate to a country, how does Rousseau typically respond? |

### C2a_to_C4a: C2a (spec) -> C4a (facts + spec)

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| bernal_diaz | 24 | 4.00 | 4.80 | +0.80 | 4 | What physical and mental preparations would a soldier of Bernal Diaz's experience adopt when living in a state of consta |
| seacole | 1 | 3.00 | 3.80 | +0.80 | 3 | When witnessing a soldier in pain, how would Mary Seacole expect a stern military officer to respond emotionally? |
| ebers | 34 | 2.00 | 2.80 | +0.80 | 2 | When seeking a place of rest and recovery, what kind of environment does Ebers value most highly? |
| rousseau | 38 | 2.00 | 2.80 | +0.80 | 2 | When someone close to him insists on accompanying him during a dangerous departure, how does Rousseau typically handle i |
| seacole | 34 | 2.00 | 2.80 | +0.80 | 2 | When encountering a soldier in need or someone she has previously helped, how does Mary Seacole respond? |
| bernal_diaz | 1 | 3.00 | 3.60 | +0.60 | 3 | Based on Diaz's character as shown in the training text, how would he likely respond to receiving valuable gifts from a  |
| hamerton | 53 | 3.00 | 3.60 | +0.60 | 3 | Would Hamerton's time-management approach as a young artist be systematic or haphazard? |
| yung_wing | 26 | 3.00 | 3.60 | +0.60 | 3 | When Yung Wing senses that a superior official no longer values his services, what does he do? |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| babur | 5 | 1.80 | 1.00 | -0.80 | 1 | How does Babur respond when receiving news of deaths among his trusted officials? |
| fukuzawa | 11 | 3.80 | 3.00 | -0.80 | 3 | When faced with a potential physical confrontation with a stranger, would Fukuzawa choose to retreat or stand his ground |
| equiano | 1 | 2.80 | 2.00 | -0.80 | 2 | When Equiano encounters information that challenges his rational worldview, how does he typically respond? |
| rousseau | 30 | 2.80 | 2.00 | -0.80 | 2 | When Rousseau believes his intellectual property is being used without proper respect or compensation, how does he typic |
| equiano | 15 | 3.60 | 3.00 | -0.60 | 3 | During a life-threatening maritime emergency, would Equiano attribute the crew's survival to human effort alone or to di |
| sunity_devee | 26 | 3.60 | 3.00 | -0.60 | 3 | Given the author's demonstrated values, how would she likely view her husband's influence on their children? |
| augustine | 23 | 2.60 | 2.00 | -0.60 | 2 | When Augustine is uncertain about a theological matter, does he tend to assert definitive answers or express humility ab |
| bernal_diaz | 28 | 2.60 | 2.00 | -0.60 | 2 | What would Bernal Diaz consider the appropriate response when a ruler claims divine authority is demanding hostile actio |

### C4_to_C4a: C4 (factdump) -> C4a (facts + spec)

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| cellini | 27 | 1.00 | 1.80 | +0.80 | 1 | Does Cellini demonstrate the ability to distinguish between his own interpretations of events and objective facts when h |
| bernal_diaz | 24 | 4.00 | 4.80 | +0.80 | 4 | What physical and mental preparations would a soldier of Bernal Diaz's experience adopt when living in a state of consta |
| ebers | 34 | 2.00 | 2.80 | +0.80 | 2 | When seeking a place of rest and recovery, what kind of environment does Ebers value most highly? |
| fukuzawa | 2 | 2.00 | 2.80 | +0.80 | 2 | When accused of disloyalty by peers, what argumentative strategy would this person employ? |
| rousseau | 38 | 2.00 | 2.80 | +0.80 | 2 | When someone close to him insists on accompanying him during a dangerous departure, how does Rousseau typically handle i |
| yung_wing | 27 | 2.00 | 2.80 | +0.80 | 2 | How does Yung Wing's approach to presenting reform ideas differ based on whether the official has already formed plans? |
| ebers | 2 | 2.00 | 2.60 | +0.60 | 2 | When faced with a mentor's wisdom about understanding people from different walks of life, would Ebers show receptivenes |
| equiano | 33 | 2.00 | 2.60 | +0.60 | 2 | When faced with work that conflicts with his religious beliefs, what internal struggle does Equiano experience? |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| zitkala_sa | 36 | 3.80 | 3.00 | -0.80 | 3 | Based on Zitkala-Sa's depiction of Native American perspectives on government promises, what would be an elder's likely  |
| babur | 29 | 2.80 | 2.00 | -0.80 | 2 | Based on the training text's documentation of Babur's administrative structure and military hierarchy, what would you pr |
| bernal_diaz | 12 | 2.80 | 2.00 | -0.80 | 2 | When faced with an overwhelming amount of observable detail in a complex scene, what approach would the author take to d |
| rousseau | 26 | 2.80 | 2.00 | -0.80 | 2 | When Rousseau writes in a new setting after leaving an urban environment, what change does he observe in his own writing |
| seacole | 13 | 2.80 | 2.00 | -0.80 | 2 | How would Mary likely treat soldiers who came to her for medical assistance, based on her established business practices |
| sunity_devee | 2 | 3.60 | 3.00 | -0.60 | 3 | When offered a local cultural artifact with superstitious significance by a gracious hostess, what is the narrator's typ |
| bernal_diaz | 28 | 2.60 | 2.00 | -0.60 | 2 | What would Bernal Diaz consider the appropriate response when a ruler claims divine authority is demanding hostile actio |
| ebers | 17 | 2.60 | 2.00 | -0.60 | 2 | When given the opportunity to spend time in natural settings, what is Ebers's typical behavior? |

### C5_to_C8: C5 (baseline) -> C8 (raw corpus)

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| ebers | 5 | 1.00 | 1.80 | +0.80 | 1 | How does Ebers depict the influence of observing children in an educational setting on an adult's life choices? |
| ebers | 11 | 1.00 | 1.80 | +0.80 | 1 | When encountering an institution that is poorly managed, how does Ebers typically respond based on his character and val |
| ebers | 13 | 1.00 | 1.80 | +0.80 | 1 | When faced with administrative problems at an institution, what does Ebers expect will eventually happen? |
| ebers | 39 | 1.00 | 1.80 | +0.80 | 1 | When physically unable to participate in social activities he would normally enjoy, how does Ebers manage his disappoint |
| fukuzawa | 6 | 1.00 | 1.80 | +0.80 | 1 | When a subordinate or servant encounters confusion about proper protocol in this person's household, what would likely h |
| keckley | 34 | 1.00 | 1.80 | +0.80 | 1 | What is Keckley's likely attitude toward completing difficult administrative tasks related to her employer's affairs? |
| keckley | 39 | 1.00 | 1.80 | +0.80 | 1 | When her employer faces public scandal, what does Keckley's response reveal about her loyalty and emotional investment? |
| sunity_devee | 4 | 1.00 | 1.80 | +0.80 | 1 | When her husband expresses disappointment about missing an opportunity due to her concerns, does the narrator typically  |

**Downward (top 4):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| bernal_diaz | 23 | 1.67 | 1.00 | -0.67 | 1 | How would Bernal Diaz characteristically respond to uncertainty about whether a military action was genuine or strategic |
| babur | 1 | 3.67 | 3.00 | -0.67 | 3 | When Babur receives news of subordinates who have demonstrated loyalty through difficult circumstances, how does he typi |
| yung_wing | 32 | 1.80 | 1.20 | -0.60 | 1 | Given Yung Wing's educational background and values, which geographic location would he choose to establish an important |
| seacole | 25 | 2.80 | 2.20 | -0.60 | 2 | How does Mary Seacole respond when soldiers ask her to care for them during dangerous operations? |

### C5_to_C9: C5 (baseline) -> C9 (corpus + spec)

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| ebers | 3 | 1.00 | 1.80 | +0.80 | 1 | How would Ebers characterize the emotional impact of natural beauty combined with a mentor's persuasive words? |
| ebers | 6 | 1.00 | 1.80 | +0.80 | 1 | What role does Ebers assign to a mentor's understanding of a younger person's inner conflicts in moments of persuasion? |
| ebers | 24 | 1.00 | 1.80 | +0.80 | 1 | When the author encounters a distraction from his current creative project, what is his typical response? |
| ebers | 28 | 1.00 | 1.80 | +0.80 | 1 | Based on the author's demonstrated approach to character creation, how would he likely treat a minor or subordinate char |
| ebers | 39 | 1.00 | 1.80 | +0.80 | 1 | When physically unable to participate in social activities he would normally enjoy, how does Ebers manage his disappoint |
| fukuzawa | 6 | 1.00 | 1.80 | +0.80 | 1 | When a subordinate or servant encounters confusion about proper protocol in this person's household, what would likely h |
| hamerton | 40 | 1.00 | 1.80 | +0.80 | 1 | Would Hamerton take his new French wife to live in a remote Scottish island rather than a conventional English home? |
| seacole | 13 | 1.00 | 1.80 | +0.80 | 1 | How would Mary likely treat soldiers who came to her for medical assistance, based on her established business practices |

**Downward (top 3):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| yung_wing | 38 | 2.80 | 2.00 | -0.80 | 2 | How would Yung Wing's career trajectory be affected by the successful implementation of his educational proposal? |
| bernal_diaz | 23 | 1.67 | 1.00 | -0.67 | 1 | How would Bernal Diaz characteristically respond to uncertainty about whether a military action was genuine or strategic |
| bernal_diaz | 24 | 3.67 | 3.00 | -0.67 | 3 | What physical and mental preparations would a soldier of Bernal Diaz's experience adopt when living in a state of consta |

### C8_to_C9: C8 (raw corpus) -> C9 (corpus + spec)

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| hamerton | 40 | 1.00 | 1.80 | +0.80 | 1 | Would Hamerton take his new French wife to live in a remote Scottish island rather than a conventional English home? |
| fukuzawa | 39 | 2.00 | 2.80 | +0.80 | 2 | Based on Fukuzawa's documented engagement with Western knowledge, would he view someone who learned English from a Weste |
| bernal_diaz | 16 | 2.00 | 2.67 | +0.67 | 2 | When the commander is offered physical assistance during a strenuous activity, what behavior would the author expect fro |
| fukuzawa | 12 | 3.00 | 3.60 | +0.60 | 3 | How would Fukuzawa likely respond if forced into a violent situation despite his personal inclinations? |
| fukuzawa | 4 | 2.00 | 2.60 | +0.60 | 2 | When facing potential punishment for disobedience, what is this person's attitude toward the consequences? |
| keckley | 20 | 2.00 | 2.60 | +0.60 | 2 | When Elizabeth learns that family members she cared for are dying, how does she respond to their requests? |
| fukuzawa | 19 | 1.20 | 1.80 | +0.60 | 1 | How would Fukuzawa assess whether someone truly possesses a skill they claim to have? |
| hamerton | 38 | 1.00 | 1.60 | +0.60 | 1 | Would Hamerton accept or decline when C. R. Leslie indirectly offered to mentor him in Constable's art tradition? |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| keckley | 2 | 3.80 | 3.00 | -0.80 | 3 | Given Keckley's pattern of emotional responsiveness to significant historical events, what physical and emotional reacti |
| keckley | 11 | 3.80 | 3.00 | -0.80 | 3 | When someone helps Elizabeth achieve a goal she initially thought difficult, how does she typically respond emotionally  |
| bernal_diaz | 18 | 3.67 | 3.00 | -0.67 | 3 | When witnessing religious practices that conflict with Christian beliefs, what language would the author employ? |
| bernal_diaz | 8 | 2.67 | 2.00 | -0.67 | 2 | When assessing the character of his fellow soldiers, what details would Diaz emphasize based on his writing style? |
| hamerton | 21 | 3.60 | 3.00 | -0.60 | 3 | Given Hamerton's deep attachment to the countryside and his distaste for towns shown in chapters 1-10, how would he reac |
| yung_wing | 13 | 3.60 | 3.00 | -0.60 | 3 | How would Yung Wing's past experiences with human trafficking influence his response to a government official's request  |
| keckley | 22 | 2.60 | 2.00 | -0.60 | 2 | Based on Keckley's demonstrated character, how would she likely respond if someone she was helping wanted to take a risk |
| ebers | 14 | 3.80 | 3.20 | -0.60 | 3 | How does Ebers characterize his attitude toward formal schooling versus his personal interests? |

### C1_mem0_to_C3_mem0: C1_mem0 -> C3_mem0

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| keckley | 29 | 1.00 | 1.80 | +0.80 | 1 | Based on patterns in the training text, how would Keckley likely assess someone who shows concern for her welfare after  |
| yung_wing | 6 | 1.00 | 1.80 | +0.80 | 1 | When given discretion over resource allocation decisions, what geographic considerations does Yung Wing prioritize? |
| cellini | 30 | 2.00 | 2.80 | +0.80 | 2 | After being proven right or vindicated by a patron's reaction, does Cellini tend to show magnanimity toward those who op |
| rousseau | 6 | 2.00 | 2.80 | +0.80 | 2 | When Rousseau creates work that contradicts his stated political principles, what does he do? |
| rousseau | 14 | 2.00 | 2.80 | +0.80 | 2 | When Rousseau reflects on his own role in relationship failures, what pattern of self-assessment does he typically exhib |
| rousseau | 21 | 2.00 | 2.80 | +0.80 | 2 | When Rousseau discovers that someone's distant behavior toward him stems from jealousy rather than contempt, how does he |
| keckley | 1 | 3.00 | 3.60 | +0.60 | 3 | Based on Keckley's demonstrated approach to witnessing grief and emotional distress, how would she likely respond if ask |
| bernal_diaz | 37 | 2.00 | 2.60 | +0.60 | 2 | How does the author demonstrate that experienced soldiers can assess military vulnerability despite increases in troop s |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| yung_wing | 22 | 3.80 | 3.00 | -0.80 | 3 | When Yung Wing receives a position that appears to be a sinecure with modest compensation, what action does he take? |
| augustine | 13 | 2.80 | 2.00 | -0.80 | 2 | How does the author explain why all people universally desire a certain state, even if they cannot articulate it perfect |
| bernal_diaz | 11 | 2.80 | 2.00 | -0.80 | 2 | When encountering an unfamiliar practice that might seem unusual or distasteful to European readers, how would the autho |
| hamerton | 45 | 2.80 | 2.00 | -0.80 | 2 | How would Hamerton react when a lord kindly invited him to visit but didn't fix a specific date? |
| keckley | 25 | 2.80 | 2.00 | -0.80 | 2 | Based on Keckley's character as shown in the training text, would she be likely to counsel caution or boldness when some |
| zitkala_sa | 20 | 2.80 | 2.00 | -0.80 | 2 | Would Zitkala-Sa blend indigenous spiritual beliefs with Christian concepts when contemplating her spiritual fate? |
| fukuzawa | 8 | 3.60 | 3.00 | -0.60 | 3 | How would this person characterize their own psychological state regarding worldly ambitions and material advancement? |
| seacole | 36 | 3.60 | 3.00 | -0.60 | 3 | How does Mary Seacole typically react to witnessing scenes of suffering and death in hospitals or battlefields? |

### C1_letta_to_C3_letta: C1_letta -> C3_letta

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| augustine | 30 | 1.00 | 1.80 | +0.80 | 1 | How does Augustine typically conclude his analysis when he has worked through a complex philosophical problem? |
| ebers | 22 | 1.00 | 1.80 | +0.80 | 1 | When the author creates allegorical characters representing abstract concepts, what pattern does he follow in terms of a |
| equiano | 28 | 1.00 | 1.80 | +0.80 | 1 | When encountering religious authority figures or clergy, what is Equiano's typical disposition? |
| yung_wing | 6 | 1.00 | 1.80 | +0.80 | 1 | When given discretion over resource allocation decisions, what geographic considerations does Yung Wing prioritize? |
| rousseau | 23 | 2.00 | 2.80 | +0.80 | 2 | How does Rousseau typically handle the continuation of contact with someone after a romantic relationship has ended? |
| sunity_devee | 35 | 2.00 | 2.80 | +0.80 | 2 | Based on the author's account of a son's education, what does she believe was the consequence of following official advi |
| yung_wing | 33 | 3.00 | 3.60 | +0.60 | 3 | How would Yung Wing likely distribute credit for the success of his major educational initiative? |
| bernal_diaz | 17 | 2.00 | 2.60 | +0.60 | 2 | How would the author describe architectural and infrastructural features that demonstrate the sophistication of the indi |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| seacole | 8 | 3.80 | 3.00 | -0.80 | 3 | How does Mary Seacole interpret a rough soldier's emotional response to a patient's suffering? |
| sunity_devee | 30 | 2.80 | 2.00 | -0.80 | 2 | Based on the author's demonstrated character, how would she likely process grief immediately after a major loss? |
| zitkala_sa | 5 | 2.80 | 2.00 | -0.80 | 2 | Based on Zitkala-Sa's reflective writing patterns in the training text, what philosophical conclusion would she likely r |
| cellini | 12 | 3.60 | 3.00 | -0.60 | 3 | If Cellini felt dissatisfied with his current circumstances and location, what would be his typical behavioral response? |
| fukuzawa | 9 | 3.60 | 3.00 | -0.60 | 3 | When organizational pressure conflicts with educational mission, which takes precedence in this person's decision-making |
| seacole | 18 | 3.60 | 3.00 | -0.60 | 3 | Based on Mary's established pattern of self-presentation, how would she likely handle discussing her medical successes? |
| augustine | 10 | 2.60 | 2.00 | -0.60 | 2 | Based on Augustine's demonstrated pattern, how does he view his former intellectual pride in relation to his spiritual g |
| babur | 24 | 1.80 | 1.20 | -0.60 | 1 | Given the military campaigns and strategic decisions documented in the training text, what would you expect about Babur' |

### C1_supermemory_to_C3_supermemory: C1_supermemory -> C3_supermemory

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| ebers | 13 | 1.00 | 1.80 | +0.80 | 1 | When faced with administrative problems at an institution, what does Ebers expect will eventually happen? |
| ebers | 36 | 1.00 | 1.80 | +0.80 | 1 | How does Ebers respond when he discovers he has misjudged someone's character or failed to learn their name? |
| ebers | 19 | 2.00 | 2.80 | +0.80 | 2 | When reflecting on different periods of instruction he received, what pattern does Ebers notice about his memory and lea |
| hamerton | 56 | 2.00 | 2.80 | +0.80 | 2 | When Hamerton's guardian expresses concern that his heterodox views might 'corrupt' his friends, how would he respond? |
| yung_wing | 18 | 2.00 | 2.80 | +0.80 | 2 | How would Yung Wing balance his desire to modernize China with his moral objections to unethical practices? |
| zitkala_sa | 14 | 2.00 | 2.80 | +0.80 | 2 | If placed in a situation where she must conceal strong emotions in front of others, what physical signs might betray her |
| rousseau | 2 | 4.00 | 4.67 | +0.67 | 4 | Based on Rousseau's character as described in the training text, would he be likely to pursue intellectual study in a ne |
| babur | 16 | 1.00 | 1.67 | +0.67 | 1 | Given Babur's patterns of conflict with rivals and his strategic thinking shown in the training text, what would he infe |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| seacole | 17 | 3.80 | 3.00 | -0.80 | 3 | What would Mary likely do if a high-ranking military figure requested her medical expertise? |
| cellini | 7 | 2.80 | 2.00 | -0.80 | 2 | How does Cellini approach problem-solving when planning an escape? |
| cellini | 16 | 2.80 | 2.00 | -0.80 | 2 | When a ruler expresses admiration for his work, how would Cellini be likely to interpret and respond to such praise? |
| yung_wing | 17 | 2.80 | 2.00 | -0.80 | 2 | When given the opportunity to secure a major commercial contract, what scale of business would Yung Wing be willing to u |
| yung_wing | 19 | 2.80 | 2.00 | -0.80 | 2 | When confronted with detailed accounts of human suffering in a labor system, would Yung Wing be likely to take action ag |
| rousseau | 3 | 1.67 | 1.00 | -0.67 | 1 | How does Rousseau typically handle collaborative intellectual work with peers? |
| rousseau | 35 | 3.67 | 3.00 | -0.67 | 3 | When facing an emotional farewell with a beloved family member, how does Rousseau typically behave? |
| babur | 21 | 2.67 | 2.00 | -0.67 | 2 | Based on the training text's pattern of how Babur describes people in his memoirs, what kind of self-awareness would you |

### C1_zep_to_C3_zep: C1_zep -> C3_zep

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| cellini | 9 | 1.00 | 1.80 | +0.80 | 1 | How does Cellini balance his obligations to others with his own self-interest? |
| fukuzawa | 19 | 1.00 | 1.80 | +0.80 | 1 | How would Fukuzawa assess whether someone truly possesses a skill they claim to have? |
| yung_wing | 9 | 1.00 | 1.80 | +0.80 | 1 | How does Yung Wing view the long-term impact of infrastructure projects he initiates? |
| babur | 1 | 2.00 | 2.80 | +0.80 | 2 | When Babur receives news of subordinates who have demonstrated loyalty through difficult circumstances, how does he typi |
| hamerton | 24 | 2.00 | 2.80 | +0.80 | 2 | If placed under a tutor who treated him with contempt and tried to humiliate him, how would Hamerton respond? |
| keckley | 34 | 2.00 | 2.80 | +0.80 | 2 | What is Keckley's likely attitude toward completing difficult administrative tasks related to her employer's affairs? |
| fukuzawa | 27 | 2.00 | 2.60 | +0.60 | 2 | How does Fukuzawa respond to criticism about his social conduct and associations? |
| seacole | 29 | 2.00 | 2.60 | +0.60 | 2 | What emotional impact does witnessing the death of a young soldier she has nursed have on Mary Seacole? |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| augustine | 22 | 3.80 | 3.00 | -0.80 | 3 | How does Augustine typically respond when he reaches the limits of human understanding? |
| seacole | 14 | 3.80 | 3.00 | -0.80 | 3 | What emotional response would Mary likely have when witnessing soldiers enduring hardship far from home? |
| sunity_devee | 21 | 3.80 | 3.00 | -0.80 | 3 | Based on the author's background and values shown in the training text, how would she likely respond to a family member' |
| bernal_diaz | 3 | 2.80 | 2.00 | -0.80 | 2 | How would Diaz characteristically evaluate the trustworthiness of local populations based on his established patterns of |
| seacole | 31 | 2.80 | 2.00 | -0.80 | 2 | When faced with an accusation of espionage by a soldier, how does Mary Seacole typically respond to threats to her freed |
| sunity_devee | 15 | 2.80 | 2.00 | -0.80 | 2 | What specific skills and knowledge does the author believe a future ruler should possess, based on her understanding of  |
| fukuzawa | 5 | 3.60 | 3.00 | -0.60 | 3 | How does this person respond to social conventions regarding status symbols and formal address? |
| babur | 3 | 2.60 | 2.00 | -0.60 | 2 | How does Babur handle situations where subordinates have been forced into difficult political positions due to external  |

### C1_baselayer_to_C3_baselayer: C1_baselayer -> C3_baselayer

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| zitkala_sa | 37 | 2.00 | 2.80 | +0.80 | 2 | When an aging tribal leader attempts to communicate grievances to American authorities, what physical and emotional toll |
| augustine | 23 | 1.00 | 1.67 | +0.67 | 1 | When Augustine is uncertain about a theological matter, does he tend to assert definitive answers or express humility ab |
| augustine | 30 | 1.00 | 1.67 | +0.67 | 1 | How does Augustine typically conclude his analysis when he has worked through a complex philosophical problem? |
| babur | 31 | 1.00 | 1.67 | +0.67 | 1 | Based on patterns in the training text, when a military leader encounters a rival who has previously opposed them, what  |
| babur | 38 | 1.00 | 1.67 | +0.67 | 1 | What pattern emerges in how Babur treats family members who have been captured or are in vulnerable positions? |
| cellini | 39 | 1.00 | 1.67 | +0.67 | 1 | What is Cellini's typical reaction when he learns that his work has impressed a major artistic figure or rival? |
| ebers | 22 | 1.00 | 1.67 | +0.67 | 1 | When the author creates allegorical characters representing abstract concepts, what pattern does he follow in terms of a |
| equiano | 20 | 1.00 | 1.67 | +0.67 | 1 | When facing a sequence of crises requiring persistence and problem-solving, would Equiano demonstrate resilience and det |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| babur | 26 | 1.67 | 1.00 | -0.67 | 1 | Given Babur's documented use of religious and literary references throughout the training text, what would you predict a |
| augustine | 22 | 3.67 | 3.00 | -0.67 | 3 | How does Augustine typically respond when he reaches the limits of human understanding? |
| keckley | 25 | 3.67 | 3.00 | -0.67 | 3 | Based on Keckley's character as shown in the training text, would she be likely to counsel caution or boldness when some |
| augustine | 36 | 2.67 | 2.00 | -0.67 | 2 | Does Augustine believe that complex theological concepts can only be understood through elaborate explanation, or can th |
| rousseau | 14 | 2.67 | 2.00 | -0.67 | 2 | When Rousseau reflects on his own role in relationship failures, what pattern of self-assessment does he typically exhib |
| sunity_devee | 7 | 2.67 | 2.00 | -0.67 | 2 | When encountering displays of affection between family members in her host's household, how does the narrator typically  |
| sunity_devee | 25 | 2.67 | 2.00 | -0.67 | 2 | How would the author likely respond to receiving condolences from high-ranking officials and royalty? |
| zitkala_sa | 5 | 2.60 | 2.00 | -0.60 | 2 | Based on Zitkala-Sa's reflective writing patterns in the training text, what philosophical conclusion would she likely r |

### C1_mem0_fp_to_C3_mem0_fp: C1_mem0_fp -> C3_mem0_fp

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| ebers | 26 | 1.00 | 1.80 | +0.80 | 1 | How does the author characterize the nature of conflict between complementary but opposing principles in his allegorical |
| ebers | 30 | 1.00 | 1.80 | +0.80 | 1 | What does the author's reflection on his own creative process reveal about his relationship to external influences and p |
| ebers | 38 | 1.00 | 1.80 | +0.80 | 1 | How does Ebers characterize the intellectual resilience of someone with strong faith when exposed to opposing philosophi |
| hamerton | 48 | 1.00 | 1.80 | +0.80 | 1 | Would Hamerton refuse a second chance to visit London after vowing never to return? |
| rousseau | 23 | 1.00 | 1.80 | +0.80 | 1 | How does Rousseau typically handle the continuation of contact with someone after a romantic relationship has ended? |
| sunity_devee | 15 | 1.00 | 1.80 | +0.80 | 1 | What specific skills and knowledge does the author believe a future ruler should possess, based on her understanding of  |
| yung_wing | 3 | 1.00 | 1.80 | +0.80 | 1 | How does Yung Wing typically prepare for important meetings with powerful officials? |
| yung_wing | 9 | 1.00 | 1.80 | +0.80 | 1 | How does Yung Wing view the long-term impact of infrastructure projects he initiates? |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| hamerton | 58 | 1.80 | 1.00 | -0.80 | 1 | Would Hamerton accept or decline an invitation to attend a grand ball at the Hotel de Ville in Paris with Napoleon III p |
| augustine | 31 | 3.80 | 3.00 | -0.80 | 3 | When faced with multiple interpretations of a complex theological matter, would Augustine advocate for dismissing all bu |
| bernal_diaz | 12 | 2.80 | 2.00 | -0.80 | 2 | When faced with an overwhelming amount of observable detail in a complex scene, what approach would the author take to d |
| keckley | 4 | 2.80 | 2.00 | -0.80 | 2 | Based on Keckley's demonstrated values regarding justice and responsibility, would she accept an explanation of careless |
| zitkala_sa | 14 | 2.80 | 2.00 | -0.80 | 2 | If placed in a situation where she must conceal strong emotions in front of others, what physical signs might betray her |
| augustine | 24 | 3.60 | 3.00 | -0.60 | 3 | How does Augustine typically handle intellectual inquiry when he is unsure of the answer? |
| bernal_diaz | 9 | 3.60 | 3.00 | -0.60 | 3 | How would Diaz respond emotionally to the safe return of officers he had been concerned about? |
| fukuzawa | 5 | 3.60 | 3.00 | -0.60 | 3 | How does this person respond to social conventions regarding status symbols and formal address? |

### C1_letta_fp_to_C3_letta_fp: C1_letta_fp -> C3_letta_fp

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| rousseau | 25 | 3.00 | 3.80 | +0.80 | 3 | Based on Rousseau's character as described in the training text, how would he likely respond to critics who claim his re |
| yung_wing | 34 | 3.00 | 3.80 | +0.80 | 3 | What would be Yung Wing's primary concern if offered a prestigious diplomatic position that might separate him from his  |
| augustine | 14 | 2.00 | 2.80 | +0.80 | 2 | When the author recalls past experiences of joy, what emotional conflict does he experience? |
| ebers | 2 | 2.00 | 2.80 | +0.80 | 2 | When faced with a mentor's wisdom about understanding people from different walks of life, would Ebers show receptivenes |
| ebers | 11 | 2.00 | 2.80 | +0.80 | 2 | When encountering an institution that is poorly managed, how does Ebers typically respond based on his character and val |
| rousseau | 11 | 2.00 | 2.80 | +0.80 | 2 | When Rousseau discovers that someone close to him has been conducting secret affairs without his knowledge, how does he  |
| fukuzawa | 39 | 2.00 | 2.60 | +0.60 | 2 | Based on Fukuzawa's documented engagement with Western knowledge, would he view someone who learned English from a Weste |
| yung_wing | 24 | 2.00 | 2.60 | +0.60 | 2 | When Yung Wing undertakes a major translation project for government reform, does he work alone or seek collaboration? |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| zitkala_sa | 22 | 1.80 | 1.00 | -0.80 | 1 | Based on Zitkala-Sa's portrayal of family bonds, what would a daughter likely do if her lover were in danger and needed  |
| cellini | 22 | 3.80 | 3.00 | -0.80 | 3 | When facing rejection or disfavor from a powerful patron, does Cellini tend to accept the situation passively or take di |
| seacole | 17 | 3.80 | 3.00 | -0.80 | 3 | What would Mary likely do if a high-ranking military figure requested her medical expertise? |
| zitkala_sa | 36 | 3.80 | 3.00 | -0.80 | 3 | Based on Zitkala-Sa's depiction of Native American perspectives on government promises, what would be an elder's likely  |
| augustine | 39 | 2.80 | 2.00 | -0.80 | 2 | When faced with a logical paradox about creation and causation, does Augustine dismiss the questioner or attempt to reso |
| rousseau | 6 | 2.80 | 2.00 | -0.80 | 2 | When Rousseau creates work that contradicts his stated political principles, what does he do? |
| zitkala_sa | 38 | 2.80 | 2.00 | -0.80 | 2 | How would Zitkala-Sa portray an elderly Native American's awareness of their own physical decline in relation to their f |
| keckley | 11 | 3.60 | 3.00 | -0.60 | 3 | When someone helps Elizabeth achieve a goal she initially thought difficult, how does she typically respond emotionally  |

### C1_supermemory_fp_to_C3_supermemory_fp: C1_supermemory_fp -> C3_supermemory_fp

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| hamerton | 48 | 1.00 | 1.80 | +0.80 | 1 | Would Hamerton refuse a second chance to visit London after vowing never to return? |
| seacole | 12 | 3.00 | 3.60 | +0.60 | 3 | Given Mary's demonstrated values regarding service and charity, what would motivate her to provide medical care to soldi |
| zitkala_sa | 8 | 3.00 | 3.60 | +0.60 | 3 | How would Zitkala-Sa, given her demonstrated critical perspective in the training text, characterize the motivations of  |
| keckley | 36 | 2.00 | 2.60 | +0.60 | 2 | How does Keckley typically respond to her living conditions when they are modest or humble? |
| yung_wing | 1 | 2.00 | 2.60 | +0.60 | 2 | When presented with an opportunity to advocate for a preferred initiative, how does Yung Wing balance his personal ambit |
| zitkala_sa | 2 | 2.00 | 2.60 | +0.60 | 2 | Given Zitkala-Sa's demonstrated perspective on indigenous spirituality and connection to nature in the training text, wh |
| ebers | 26 | 1.20 | 1.80 | +0.60 | 1 | How does the author characterize the nature of conflict between complementary but opposing principles in his allegorical |
| ebers | 31 | 1.20 | 1.80 | +0.60 | 1 | When encountering someone with deeply held religious convictions different from his own, how does Ebers typically respon |

**Downward (top 4):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| yung_wing | 13 | 1.80 | 1.00 | -0.80 | 1 | How would Yung Wing's past experiences with human trafficking influence his response to a government official's request  |
| augustine | 17 | 2.80 | 2.00 | -0.80 | 2 | When observing others possess a quality, what does the author believe must occur internally before one can desire to imi |
| zitkala_sa | 20 | 2.60 | 2.00 | -0.60 | 2 | Would Zitkala-Sa blend indigenous spiritual beliefs with Christian concepts when contemplating her spiritual fate? |
| augustine | 6 | 3.80 | 3.20 | -0.60 | 3 | When Augustine reflects on his transformation, what does he emphasize about the role of divine intervention in his chang |

### C1_zep_fp_to_C3_zep_fp: C1_zep_fp -> C3_zep_fp

**Upward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| bernal_diaz | 10 | 1.00 | 1.80 | +0.80 | 1 | Based on Diaz's demonstrated honesty, how would he handle acknowledging gaps in his own memory or knowledge? |
| ebers | 26 | 1.00 | 1.80 | +0.80 | 1 | How does the author characterize the nature of conflict between complementary but opposing principles in his allegorical |
| equiano | 20 | 1.00 | 1.80 | +0.80 | 1 | When facing a sequence of crises requiring persistence and problem-solving, would Equiano demonstrate resilience and det |
| yung_wing | 7 | 1.00 | 1.80 | +0.80 | 1 | How does Yung Wing respond when a superior defers a decision to other experts rather than making it himself? |
| yung_wing | 24 | 1.00 | 1.80 | +0.80 | 1 | When Yung Wing undertakes a major translation project for government reform, does he work alone or seek collaboration? |
| zitkala_sa | 4 | 1.00 | 1.80 | +0.80 | 1 | How would Zitkala-Sa, given her demonstrated relationship with animals and nature in the training text, likely interact  |
| augustine | 26 | 3.00 | 3.80 | +0.80 | 3 | How does Augustine typically address God when he is in the process of working through a difficult question? |
| bernal_diaz | 14 | 2.00 | 2.80 | +0.80 | 2 | When describing economic systems and trade practices of the indigenous people, what would be the author's likely approac |

**Downward (top 8):**

| subject | qid | pre | post | Δ | band | question (truncated) |
|---|---:|---:|---:|---:|---:|---|
| ebers | 35 | 1.80 | 1.00 | -0.80 | 1 | Does Ebers tend to remain isolated when given the opportunity for solitude, or does he eventually engage with his commun |
| zitkala_sa | 6 | 1.80 | 1.00 | -0.80 | 1 | Given Zitkala-Sa's demonstrated use of metaphor and symbolism in the training text, how would she likely employ comparis |
| keckley | 2 | 3.80 | 3.00 | -0.80 | 3 | Given Keckley's pattern of emotional responsiveness to significant historical events, what physical and emotional reacti |
| fukuzawa | 24 | 2.80 | 2.00 | -0.80 | 2 | Would Fukuzawa modify his behavior based on gossip or social suspicion? |
| keckley | 25 | 2.80 | 2.00 | -0.80 | 2 | Based on Keckley's character as shown in the training text, would she be likely to counsel caution or boldness when some |
| bernal_diaz | 22 | 2.60 | 2.00 | -0.60 | 2 | Based on Bernal Diaz's character as presented in the training text, would he be likely to accept unverified claims about |
| zitkala_sa | 33 | 2.60 | 2.00 | -0.60 | 2 | When an elderly tribal member reflects on generational decline and loss of traditional virtues, what specific moral qual |
| ebers | 5 | 1.60 | 1.00 | -0.60 | 1 | How does Ebers depict the influence of observing children in an educational setting on an adult's life choices? |


## Stream Y3. Meta-judging behavior

### Y3a. Direction agreement vs panel direction, by panel-|Δ| magnitude

Three-category counting: judge agrees with panel sign, disagrees, or is judge-flat (judge per-question Δ == 0). Panel-flat questions (panel Δ exactly 0) collapse to judge-flat for this purpose.

**Structural note about the `lt_0.1` bin.** With 5 integer-score judges (the common case), panel_delta moves in increments of 0.2 (sum of integer scores over 5). With 4 common judges, increments are 0.25; with 3 common judges, increments are ~0.333. In all cases the smallest nonzero |panel_delta| is >= 0.2, so `lt_0.1` is in practice the exact-tie bin (panel_pre == panel_post): there is no panel direction to agree with, and every paired question collapses to judge-flat by construction. The first bin with a meaningful panel direction is `0.1_to_0.25`, which captures |panel_delta| == 0.2 cases and (where common-judge count is 4) |panel_delta| == 0.25.

Agree-rate excl_flat = agree / (agree + disagree); incl_flat = agree / (agree + disagree + judge_flat).

We anchor presentation on `C5 -> C4a` (the headline pair) and report the direction-agreement curve for each pair below it.

**C5_to_C4a**: C5 (baseline) -> C4a (facts + spec)

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 43 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 92 | 75.0% (27/36) | 83.3% (25/30) | 70.0% (21/30) | 79.4% (27/34) | 63.2% (24/38) | 74.2% |
| `0.25_to_0.5` | 57 | 88.9% (24/27) | 93.8% (15/16) | 95.8% (23/24) | 100.0% (28/28) | 88.2% (15/17) | 93.3% |
| `0.5_to_1.0` | 114 | 89.3% (67/75) | 96.8% (61/63) | 94.7% (71/75) | 92.0% (69/75) | 96.2% (50/52) | 93.8% |
| `ge_1.0` | 240 | 99.5% (218/219) | 100.0% (220/220) | 100.0% (231/231) | 100.0% (221/221) | 100.0% (230/230) | 99.9% |

**C5_to_C2a**: C5 (baseline) -> C2a (full spec)

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 79 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 90 | 74.4% (29/39) | 80.0% (20/25) | 89.3% (25/28) | 77.4% (24/31) | 61.3% (19/31) | 76.5% |
| `0.25_to_0.5` | 62 | 94.1% (32/34) | 85.7% (12/14) | 86.4% (19/22) | 92.3% (36/39) | 95.5% (21/22) | 90.8% |
| `0.5_to_1.0` | 115 | 92.9% (65/70) | 98.3% (58/59) | 94.0% (78/83) | 90.4% (75/83) | 100.0% (63/63) | 95.1% |
| `ge_1.0` | 200 | 97.3% (183/188) | 100.0% (180/180) | 100.0% (192/192) | 100.0% (182/182) | 99.4% (172/173) | 99.4% |

**C5_to_C4**: C5 (baseline) -> C4 (fact dump)

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 73 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 88 | 87.5% (42/48) | 66.7% (12/18) | 84.2% (16/19) | 85.7% (24/28) | 59.1% (13/22) | 76.6% |
| `0.25_to_0.5` | 75 | 77.5% (31/40) | 82.6% (19/23) | 91.7% (33/36) | 95.7% (44/46) | 95.2% (20/21) | 88.5% |
| `0.5_to_1.0` | 107 | 90.7% (68/75) | 100.0% (57/57) | 95.9% (70/73) | 98.5% (64/65) | 100.0% (49/49) | 97.0% |
| `ge_1.0` | 203 | 100.0% (187/187) | 99.5% (189/190) | 100.0% (192/192) | 100.0% (195/195) | 99.5% (183/184) | 99.8% |

**C5_to_C2c**: C5 (baseline) -> C2c (wrong spec)

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 141 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 96 | 85.2% (52/61) | 66.7% (14/21) | 76.2% (16/21) | 78.4% (29/37) | 66.7% (8/12) | 74.6% |
| `0.25_to_0.5` | 65 | 87.8% (36/41) | 94.1% (16/17) | 92.3% (24/26) | 91.7% (33/36) | 83.3% (10/12) | 89.8% |
| `0.5_to_1.0` | 78 | 89.1% (49/55) | 96.2% (50/52) | 94.4% (51/54) | 100.0% (48/48) | 97.3% (36/37) | 95.4% |
| `ge_1.0` | 166 | 99.3% (149/150) | 99.3% (146/147) | 100.0% (152/152) | 98.7% (149/151) | 99.3% (140/141) | 99.3% |

**C4_to_C4a**: C4 (factdump) -> C4a (facts + spec)

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 89 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 161 | 82.4% (56/68) | 71.9% (23/32) | 78.6% (33/42) | 85.5% (59/69) | 66.0% (31/47) | 76.9% |
| `0.25_to_0.5` | 104 | 89.4% (42/47) | 88.2% (30/34) | 95.2% (40/42) | 89.6% (43/48) | 87.2% (41/47) | 89.9% |
| `0.5_to_1.0` | 107 | 93.7% (59/63) | 94.7% (54/57) | 96.9% (62/64) | 91.2% (52/57) | 98.4% (61/62) | 95.0% |
| `ge_1.0` | 85 | 98.4% (61/62) | 100.0% (65/65) | 100.0% (73/73) | 100.0% (68/68) | 96.8% (61/63) | 99.0% |

**C2a_to_C4a**: C2a (spec) -> C4a (facts + spec)

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 93 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 124 | 73.1% (38/52) | 78.9% (30/38) | 73.3% (22/30) | 81.1% (43/53) | 74.2% (23/31) | 76.1% |
| `0.25_to_0.5` | 96 | 85.3% (29/34) | 90.7% (39/43) | 92.3% (36/39) | 86.8% (46/53) | 82.6% (19/23) | 87.5% |
| `0.5_to_1.0` | 126 | 94.5% (69/73) | 96.1% (74/77) | 93.8% (61/65) | 89.6% (69/77) | 92.6% (63/68) | 93.3% |
| `ge_1.0` | 107 | 98.9% (86/87) | 98.9% (88/89) | 98.9% (90/91) | 98.8% (84/85) | 97.4% (75/77) | 98.6% |

**C8_to_C9**: C8 (raw corpus) -> C9 (corpus + spec)

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 52 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 79 | 79.3% (23/29) | 78.6% (11/14) | 87.5% (14/16) | 82.1% (23/28) | 80.0% (20/25) | 81.5% |
| `0.25_to_0.5` | 70 | 82.6% (19/23) | 100.0% (19/19) | 100.0% (20/20) | 94.4% (34/36) | 80.0% (20/25) | 91.4% |
| `0.5_to_1.0` | 62 | 97.1% (33/34) | 100.0% (26/26) | 100.0% (35/35) | 100.0% (35/35) | 96.8% (30/31) | 98.8% |
| `ge_1.0` | 49 | 100.0% (33/33) | 100.0% (37/37) | 100.0% (43/43) | 97.5% (39/40) | 100.0% (41/41) | 99.5% |

**C5_to_C8**: C5 (baseline) -> C8 (raw corpus)

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 36 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 27 | 66.7% (8/12) | 100.0% (5/5) | 87.5% (7/8) | 77.8% (7/9) | 80.0% (4/5) | 82.4% |
| `0.25_to_0.5` | 43 | 100.0% (13/13) | 100.0% (9/9) | 100.0% (17/17) | 88.2% (15/17) | 84.6% (11/13) | 94.6% |
| `0.5_to_1.0` | 66 | 93.5% (29/31) | 100.0% (20/20) | 100.0% (47/47) | 100.0% (44/44) | 92.1% (35/38) | 97.1% |
| `ge_1.0` | 179 | 100.0% (142/142) | 100.0% (147/147) | 99.4% (173/174) | 100.0% (170/170) | 100.0% (164/164) | 99.9% |

**C5_to_C9**: C5 (baseline) -> C9 (corpus + spec)

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 15 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 25 | 76.9% (10/13) | 75.0% (3/4) | 100.0% (6/6) | 57.1% (4/7) | 85.7% (6/7) | 79.0% |
| `0.25_to_0.5` | 34 | 81.2% (13/16) | 100.0% (11/11) | 90.0% (18/20) | 77.8% (14/18) | 76.9% (10/13) | 85.2% |
| `0.5_to_1.0` | 54 | 100.0% (37/37) | 100.0% (23/23) | 97.4% (38/39) | 97.1% (33/34) | 100.0% (28/28) | 98.9% |
| `ge_1.0` | 184 | 100.0% (152/152) | 100.0% (154/154) | 100.0% (175/175) | 100.0% (176/176) | 100.0% (177/177) | 100.0% |

Memory-system controlled pairs (C1_<sys> -> C3_<sys>):

**C1_mem0_to_C3_mem0**: C1_mem0 -> C3_mem0

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 87 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 135 | 69.4% (34/49) | 90.3% (28/31) | 87.9% (29/33) | 76.3% (45/59) | 81.8% (27/33) | 81.1% |
| `0.25_to_0.5` | 94 | 89.2% (33/37) | 94.3% (33/35) | 88.2% (30/34) | 91.8% (45/49) | 87.5% (35/40) | 90.2% |
| `0.5_to_1.0` | 118 | 95.9% (70/73) | 98.4% (63/64) | 93.9% (62/66) | 97.1% (67/69) | 96.3% (52/54) | 96.3% |
| `ge_1.0` | 112 | 98.8% (85/86) | 100.0% (86/86) | 100.0% (102/102) | 98.9% (88/89) | 98.8% (82/83) | 99.3% |

**C1_letta_to_C3_letta**: C1_letta -> C3_letta

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 75 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 141 | 67.3% (37/55) | 81.2% (26/32) | 77.8% (35/45) | 76.4% (42/55) | 84.2% (32/38) | 77.4% |
| `0.25_to_0.5` | 90 | 86.0% (37/43) | 89.7% (26/29) | 80.6% (25/31) | 90.2% (46/51) | 88.9% (32/36) | 87.1% |
| `0.5_to_1.0` | 113 | 93.2% (55/59) | 95.0% (57/60) | 94.8% (73/77) | 91.5% (65/71) | 93.9% (62/66) | 93.7% |
| `ge_1.0` | 126 | 99.0% (96/97) | 100.0% (105/105) | 98.2% (111/113) | 96.3% (104/108) | 97.1% (101/104) | 98.1% |

**C1_supermemory_to_C3_supermemory**: C1_supermemory -> C3_supermemory

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 107 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 118 | 72.5% (29/40) | 66.7% (16/24) | 79.5% (31/39) | 78.6% (44/56) | 81.4% (35/43) | 75.7% |
| `0.25_to_0.5` | 104 | 68.8% (22/32) | 92.6% (25/27) | 95.6% (43/45) | 92.0% (46/50) | 77.3% (34/44) | 85.2% |
| `0.5_to_1.0` | 98 | 93.0% (53/57) | 97.5% (39/40) | 96.6% (57/59) | 98.3% (58/59) | 89.4% (42/47) | 95.0% |
| `ge_1.0` | 89 | 100.0% (64/64) | 100.0% (65/65) | 100.0% (81/81) | 100.0% (70/70) | 98.7% (74/75) | 99.7% |

**C1_zep_to_C3_zep**: C1_zep -> C3_zep

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 84 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 129 | 80.0% (40/50) | 86.2% (25/29) | 78.8% (26/33) | 74.5% (35/47) | 77.5% (31/40) | 79.4% |
| `0.25_to_0.5` | 94 | 76.9% (30/39) | 94.7% (36/38) | 97.5% (39/40) | 84.1% (37/44) | 92.3% (36/39) | 89.1% |
| `0.5_to_1.0` | 127 | 95.5% (64/67) | 97.2% (70/72) | 90.8% (69/76) | 91.2% (73/80) | 96.8% (61/63) | 94.3% |
| `ge_1.0` | 112 | 97.8% (89/91) | 99.0% (97/98) | 100.0% (101/101) | 100.0% (95/95) | 98.9% (86/87) | 99.1% |

**C1_baselayer_to_C3_baselayer**: C1_baselayer -> C3_baselayer

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 123 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 14 | 66.7% (2/3) | 50.0% (1/2) | 100.0% (2/2) | 100.0% (7/7) | 100.0% (3/3) | 83.3% |
| `0.25_to_0.5` | 154 | 100.0% (5/5) | 100.0% (3/3) | 91.5% (43/47) | 88.0% (66/75) | 84.1% (53/63) | 92.7% |
| `0.5_to_1.0` | 119 | 80.0% (12/15) | 100.0% (13/13) | 98.6% (72/73) | 88.4% (61/69) | 95.5% (63/66) | 92.5% |
| `ge_1.0` | 133 | 94.1% (16/17) | 100.0% (20/20) | 100.0% (124/124) | 99.0% (98/99) | 98.9% (93/94) | 98.4% |

Memory-system fullpipeline pairs:

**C1_mem0_fp_to_C3_mem0_fp**: C1_mem0_fp -> C3_mem0_fp

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 70 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 115 | 84.6% (33/39) | 82.1% (23/28) | 82.9% (29/35) | 78.0% (32/41) | 71.4% (20/28) | 79.8% |
| `0.25_to_0.5` | 86 | 78.8% (26/33) | 96.7% (29/30) | 88.6% (31/35) | 89.4% (42/47) | 100.0% (35/35) | 90.7% |
| `0.5_to_1.0` | 120 | 88.1% (59/67) | 94.2% (65/69) | 94.7% (71/75) | 97.6% (80/82) | 97.0% (65/67) | 94.3% |
| `ge_1.0` | 153 | 100.0% (121/121) | 99.2% (120/121) | 98.6% (140/142) | 100.0% (135/135) | 100.0% (128/128) | 99.6% |

**C1_letta_fp_to_C3_letta_fp**: C1_letta_fp -> C3_letta_fp

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 98 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 164 | 88.2% (67/76) | 95.1% (39/41) | 50.0% (16/32) | 84.8% (39/46) | 86.8% (33/38) | 81.0% |
| `0.25_to_0.5` | 91 | 97.4% (37/38) | 96.9% (31/32) | 100.0% (25/25) | 76.6% (36/47) | 97.4% (38/39) | 93.7% |
| `0.5_to_1.0` | 114 | 93.2% (55/59) | 100.0% (51/51) | 98.5% (65/66) | 95.6% (65/68) | 90.5% (57/63) | 95.6% |
| `ge_1.0` | 79 | 96.8% (60/62) | 100.0% (61/61) | 98.4% (63/64) | 96.8% (61/63) | 100.0% (60/60) | 98.4% |

**C1_supermemory_fp_to_C3_supermemory_fp**: C1_supermemory_fp -> C3_supermemory_fp

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 39 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 61 | 72.0% (18/25) | 86.7% (13/15) | 100.0% (10/10) | 80.0% (16/20) | 90.9% (10/11) | 85.9% |
| `0.25_to_0.5` | 36 | 85.7% (12/14) | 81.8% (9/11) | 93.8% (15/16) | 94.1% (16/17) | 91.7% (11/12) | 89.4% |
| `0.5_to_1.0` | 50 | 87.0% (20/23) | 100.0% (29/29) | 100.0% (25/25) | 93.8% (30/32) | 100.0% (28/28) | 96.1% |
| `ge_1.0` | 35 | 100.0% (30/30) | 100.0% (24/24) | 100.0% (33/33) | 100.0% (29/29) | 100.0% (26/26) | 100.0% |

**C1_zep_fp_to_C3_zep_fp**: C1_zep_fp -> C3_zep_fp

| panel \|Δ\| bin | n | gpt4o agree% (excl flat) | gpt54 agree% (excl flat) | haiku agree% (excl flat) | opus agree% (excl flat) | sonnet agree% (excl flat) | mean agree% (excl flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lt_0.1` | 67 | --- | --- | --- | --- | --- | --- |
| `0.1_to_0.25` | 118 | 79.1% (34/43) | 91.3% (21/23) | 85.4% (35/41) | 72.2% (39/54) | 80.0% (20/25) | 81.6% |
| `0.25_to_0.5` | 85 | 84.2% (32/38) | 89.2% (33/37) | 97.4% (37/38) | 92.5% (37/40) | 86.2% (25/29) | 89.9% |
| `0.5_to_1.0` | 139 | 90.9% (60/66) | 94.4% (84/89) | 98.9% (89/90) | 96.7% (87/90) | 97.4% (75/77) | 95.6% |
| `ge_1.0` | 137 | 100.0% (105/105) | 99.1% (112/113) | 97.6% (122/125) | 100.0% (117/117) | 100.0% (119/119) | 99.3% |

### Y3b. Per-judge sensitivity profile (pooled across all 18 pairs)

Pooled by paired-comparison instances: each (pair, subject, qid, judge) where the judge has both pre and post counts once, even if the same (subject, qid) appears under multiple pre/post pairs.

**Note on instance count asymmetry.** haiku, opus, sonnet have 8804 paired-comparison instances each (full coverage). gpt4o has 8091 (713 missing) and gpt54 has 8105 (699 missing). The gap is concentrated on questions where the OpenAI judges were not run for specific subject/condition combinations: babur on the cross-file C5/C8/C9 pairs (78 + 39 + 39 = 156 instances), and certain subjects on the controlled memory-system pairs (supermemory adds 78 instances missing both OpenAI judges; baselayer adds 465 instances missing both OpenAI judges; letta adds 14 instances missing only gpt4o). These are the same questions that appear in the "n with 3 judges" column of the data-anomalies table below; the panel falls back to a 3-judge mean for those cases.

| judge | n instances | nonzero rate | |Δ|=0 | |Δ|=1 | |Δ|=2 | |Δ|=3 | |Δ|=4 | mean per-pair Spearman vs panel-minus | n pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt4o | 8091 | 54.7% | 3665 | 3321 | 825 | 192 | 88 | 0.548 | 18 |
| gpt54 | 8105 | 47.2% | 4283 | 1858 | 1214 | 703 | 47 | 0.587 | 18 |
| haiku | 8804 | 52.1% | 4216 | 2461 | 895 | 934 | 298 | 0.582 | 18 |
| opus | 8804 | 55.7% | 3904 | 3425 | 1140 | 303 | 32 | 0.586 | 18 |
| sonnet | 8804 | 47.6% | 4611 | 3327 | 652 | 187 | 27 | 0.591 | 18 |

### Y3c. Per-judge Δ vs panel-minus-judge Δ Spearman (per pair)

For each judge, Spearman correlation between (judge per-question Δ) and (panel-minus-judge per-question Δ) across questions in the pair. High ρ means the judge tracks the rest of the panel; low ρ means the judge is adding a different signal (or noise).

| pair | n | gpt4o ρ | gpt54 ρ | haiku ρ | opus ρ | sonnet ρ |
|---|---:|---:|---:|---:|---:|---:|
| `C5_to_C2a` | 546 | 0.677 | 0.704 | 0.735 | 0.717 | 0.692 |
| `C5_to_C4` | 546 | 0.711 | 0.750 | 0.747 | 0.776 | 0.727 |
| `C5_to_C4a` | 546 | 0.734 | 0.737 | 0.728 | 0.766 | 0.718 |
| `C5_to_C2c` | 546 | 0.652 | 0.706 | 0.709 | 0.701 | 0.727 |
| `C2a_to_C4a` | 546 | 0.466 | 0.456 | 0.448 | 0.462 | 0.440 |
| `C4_to_C4a` | 546 | 0.404 | 0.398 | 0.399 | 0.398 | 0.409 |
| `C5_to_C8` | 351 | 0.767 | 0.826 | 0.794 | 0.807 | 0.754 |
| `C5_to_C9` | 312 | 0.769 | 0.787 | 0.748 | 0.762 | 0.747 |
| `C8_to_C9` | 312 | 0.460 | 0.505 | 0.503 | 0.481 | 0.485 |
| `C1_mem0_to_C3_mem0` | 546 | 0.501 | 0.515 | 0.530 | 0.515 | 0.508 |
| `C1_letta_to_C3_letta` | 545 | 0.477 | 0.517 | 0.492 | 0.510 | 0.549 |
| `C1_supermemory_to_C3_supermemory` | 516 | 0.464 | 0.464 | 0.477 | 0.484 | 0.445 |
| `C1_zep_to_C3_zep` | 546 | 0.469 | 0.549 | 0.499 | 0.519 | 0.514 |
| `C1_baselayer_to_C3_baselayer` | 543 | 0.531 | 0.667 | 0.652 | 0.525 | 0.673 |
| `C1_mem0_fp_to_C3_mem0_fp` | 544 | 0.505 | 0.568 | 0.578 | 0.628 | 0.603 |
| `C1_letta_fp_to_C3_letta_fp` | 546 | 0.404 | 0.441 | 0.379 | 0.428 | 0.480 |
| `C1_supermemory_fp_to_C3_supermemory_fp` | 221 | 0.396 | 0.409 | 0.519 | 0.494 | 0.546 |
| `C1_zep_fp_to_C3_zep_fp` | 546 | 0.481 | 0.560 | 0.541 | 0.579 | 0.614 |

### Y3d. Panel rank correlation pre vs post (per pair)

Spearman ρ across paired questions between (panel mean under pre) and (panel mean under post). High ρ means the post condition re-ranks questions on the same axis as the pre. Low ρ means the post condition shifts the relative ordering, not just the mean level.

| pair | n | Spearman ρ pre vs post |
|---|---:|---:|
| `C5_to_C2a` | 546 | 0.397 |
| `C5_to_C4` | 546 | 0.320 |
| `C5_to_C4a` | 546 | 0.274 |
| `C5_to_C2c` | 546 | 0.364 |
| `C2a_to_C4a` | 546 | 0.615 |
| `C4_to_C4a` | 546 | 0.716 |
| `C5_to_C8` | 351 | 0.246 |
| `C5_to_C9` | 312 | 0.190 |
| `C8_to_C9` | 312 | 0.705 |
| `C1_mem0_to_C3_mem0` | 546 | 0.620 |
| `C1_letta_to_C3_letta` | 545 | 0.555 |
| `C1_supermemory_to_C3_supermemory` | 516 | 0.687 |
| `C1_zep_to_C3_zep` | 546 | 0.588 |
| `C1_baselayer_to_C3_baselayer` | 543 | 0.589 |
| `C1_mem0_fp_to_C3_mem0_fp` | 544 | 0.510 |
| `C1_letta_fp_to_C3_letta_fp` | 546 | 0.721 |
| `C1_supermemory_fp_to_C3_supermemory_fp` | 221 | 0.665 |
| `C1_zep_fp_to_C3_zep_fp` | 546 | 0.505 |

## Stream Y4. Within-band missed-signal estimate per pair

For each pair: count of paired questions the binary anchor-crossing metric records (anchor_crossings) vs. paired questions with same-band |Δ| >= 0.5 (half-anchor shift the metric ignores) and same-band 0.25 <= |Δ| < 0.5 (quarter-anchor shifts).

| pair | n | anchor crossings | same-band \|Δ\| >= 0.5 | same-band 0.25..0.5 | half-per-anchor ratio | quarter-per-anchor ratio |
|---|---:|---:|---:|---:|---:|---:|
| `C5_to_C2a` | 546 | 306 | 45 | 43 | 0.15 | 0.14 |
| `C5_to_C4` | 546 | 292 | 49 | 54 | 0.17 | 0.18 |
| `C5_to_C4a` | 546 | 322 | 56 | 47 | 0.17 | 0.15 |
| `C5_to_C2c` | 546 | 219 | 45 | 53 | 0.21 | 0.24 |
| `C2a_to_C4a` | 546 | 239 | 44 | 61 | 0.18 | 0.26 |
| `C4_to_C4a` | 546 | 207 | 43 | 68 | 0.21 | 0.33 |
| `C5_to_C8` | 351 | 229 | 34 | 31 | 0.15 | 0.14 |
| `C5_to_C9` | 312 | 215 | 36 | 23 | 0.17 | 0.11 |
| `C8_to_C9` | 312 | 126 | 21 | 46 | 0.17 | 0.37 |
| `C1_mem0_to_C3_mem0` | 546 | 229 | 56 | 68 | 0.24 | 0.30 |
| `C1_letta_to_C3_letta` | 545 | 247 | 40 | 66 | 0.16 | 0.27 |
| `C1_supermemory_to_C3_supermemory` | 516 | 209 | 40 | 71 | 0.19 | 0.34 |
| `C1_zep_to_C3_zep` | 546 | 256 | 49 | 57 | 0.19 | 0.22 |
| `C1_baselayer_to_C3_baselayer` | 543 | 262 | 39 | 106 | 0.15 | 0.40 |
| `C1_mem0_fp_to_C3_mem0_fp` | 544 | 276 | 45 | 51 | 0.16 | 0.18 |
| `C1_letta_fp_to_C3_letta_fp` | 546 | 213 | 42 | 62 | 0.20 | 0.29 |
| `C1_supermemory_fp_to_C3_supermemory_fp` | 221 | 92 | 17 | 29 | 0.18 | 0.32 |
| `C1_zep_fp_to_C3_zep_fp` | 546 | 267 | 58 | 59 | 0.22 | 0.22 |

**Pooled across all 18 pairs:** anchor crossings = 4206, same-band |Δ| >= 0.5 = 759, same-band 0.25..0.5 = 995.
For every 1 anchor crossing the metric records, 0.18 same-band half-anchor shifts exist that it does not.

## Data anomalies and judge coverage per pair

Per-question judge coverage varies across pairs. Below is the distribution of `n_judges` (number of primary judges with BOTH pre and post valid) per paired question. Pairs with mostly 5 are the cleanest; pairs where most questions are at 3 or 4 judges have narrower effective panels and panel_delta increments scale accordingly (3 judges -> 1/3 increments; 5 judges -> 1/5).

| pair | n total | n with 3 judges | n with 4 judges | n with 5 judges |
|---|---:|---:|---:|---:|
| `C5_to_C2a` | 546 | 0 | 0 | 546 |
| `C5_to_C4` | 546 | 0 | 0 | 546 |
| `C5_to_C4a` | 546 | 0 | 0 | 546 |
| `C5_to_C2c` | 546 | 0 | 0 | 546 |
| `C2a_to_C4a` | 546 | 0 | 0 | 546 |
| `C4_to_C4a` | 546 | 0 | 0 | 546 |
| `C5_to_C8` | 351 | 78 | 0 | 273 |
| `C5_to_C9` | 312 | 39 | 0 | 273 |
| `C8_to_C9` | 312 | 39 | 0 | 273 |
| `C1_mem0_to_C3_mem0` | 546 | 0 | 0 | 546 |
| `C1_letta_to_C3_letta` | 545 | 0 | 14 | 531 |
| `C1_supermemory_to_C3_supermemory` | 516 | 78 | 0 | 438 |
| `C1_zep_to_C3_zep` | 546 | 0 | 0 | 546 |
| `C1_baselayer_to_C3_baselayer` | 543 | 465 | 0 | 78 |
| `C1_mem0_fp_to_C3_mem0_fp` | 544 | 0 | 0 | 544 |
| `C1_letta_fp_to_C3_letta_fp` | 546 | 0 | 0 | 546 |
| `C1_supermemory_fp_to_C3_supermemory_fp` | 221 | 0 | 0 | 221 |
| `C1_zep_fp_to_C3_zep_fp` | 546 | 0 | 0 | 546 |

**Notable anomaly:** the `C1_baselayer_to_C3_baselayer` controlled pair has 465 of 543 paired questions covered by only 3 judges (panel delta in 1/3 increments rather than 1/5). The bucket distribution for that pair is correspondingly distorted: many panel deltas land at +/-0.333 (which falls in the `pos_quarter` or `neg_quarter` bin) and the `same_band_neg_quarter` bin balloons relative to controlled pairs with full 5-judge coverage. The `C1_supermemory_to_C3_supermemory` pair has 78 of 516 questions at 3 judges. Cross-pair comparisons of fine-grained bucket counts should account for this.

## Validity implications

- Sub-anchor signal is real and detected by the panel. Direction-agreement rises monotonically with panel |Δ|, including in the 0.1 to 0.25 bin where the binary metric records nothing. Reporting only anchor crossings discards a measurable interpretive signal.
- A complementary fractional-Δ metric (mean Δ + bucket distribution) should be reported alongside anchor crossings in the paper. The wins inventory already has aggregate mean Δ; the bucket distribution from this report would close the gap.
- Per-judge nonzero per-question Δ rates run from 47.2% (gpt54) to 55.7% (opus). The shape of the move distribution differs across judges (see Y3b): sonnet and gpt4o are softly lumpy (frequent |Δ|=1 moves, rare big moves); gpt54 is bimodally lumpy (often flat, but big jumps when it does move); haiku has the widest spread (frequent |Δ|=3 and |Δ|=4 jumps); opus is the most active mover with mostly mid-size shifts. Per-pair Spearman vs panel-minus is similar across judges (range 0.55 to 0.59), so all 5 contribute coherent signal; the differences are in the move-size distribution, not in directional disagreement.
- Panel rank correlation pre vs post is high for spec-on-info-rich pairs (the spec preserves the underlying response ordering and lifts uniformly) and lower for spec-on-baseline pairs (where the spec is doing more re-ranking work). This is consistent with the paper's coupling-free reframing: the spec produces a near-uniform C4a ceiling rather than differential treatment heterogeneity.
- The downward within-band shifts (Y2 downward tables) are real degradations the binary metric ignores. Where they cluster in wrong-spec pairs (C5 -> C2c) they confirm the adversarial control; where they cluster in spec-on-info-rich pairs (C4 -> C4a or C8 -> C9) they highlight subjects/questions where the spec crowds out useful factual surface.
- Negative sub-anchor shifts are notably more frequent in spec-on-info-rich pairs (mean 10.0% same-band neg subquarter and 4.6% same-band neg quarter across the 3 pairs) than in spec-on-baseline pairs (mean 4.8% and 2.1%). Adding a spec on top of fact-rich context produces small downward shifts roughly twice as often as adding a spec on a barren baseline. The mean delta remains positive and panel rank-correlation pre vs post is high, but this asymmetry is not visible in the anchor-crossing summary and should be surfaced in any sub-anchor metric.

