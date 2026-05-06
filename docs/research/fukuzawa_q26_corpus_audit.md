# Fukuzawa Q26 Supermemory Corpus Audit

**Date:** 2026-04-23
**Prompted by:** Author annotation on Paper §4.4 — "This reads like it was trained on the entire corpus, can you confirm please" — concerning the Fukuzawa Q26 Supermemory C3 score.
**Conclusion (tl;dr):** **No training-data contamination.** The Fukuzawa Supermemory ingestion pipelines used only the training-half corpus. Zero held-out passages leaked into ingested content at 10-gram resolution. The elevated Q26 score reflects topical retrieval from training-half facts, not memorization of the held-out answer.

---

## Note on which result the concern references

Two Supermemory conditions exist for Fukuzawa in `results/global_fukuzawa/`:

1. **Option A (pre-extracted facts → Supermemory):** 1,657 atomic facts (`facts.json`) ingested. Q26 C3 avg = **4.33** across 6 judges (5,4,4,4,4,5). Files: `supermemory_ingestion.json`, `supermemory_retrieval.json`, `supermemory_judgments_merged.json`.
2. **Option B (raw training text chunks → Supermemory):** 25 × 3,000-word chunks. Q26 C3 avg = **1.17**, because retrieval returned **0 facts** and the response was an epistemic refusal. Files: `supermemory_fullpipeline_*.json`.

The annotated concern ("4.20") most closely matches Option A (4.33). Both are audited below.

---

## Level 1: Source code (code-read confirmation)

### Option B / fullpipeline ingestion (`run_option_b.py`)

File: `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/run_option_b.py`

```python
# lines 78-83
def load_training_text(subject):
    if subject == 'hamerton':
        path = os.path.join(BASE_DIR, 'corpus', 'tiers', 'tier_02_ch01-10.txt')
    else:
        path = os.path.join(RESULTS_BASE, f'global_{subject}', 'training.txt')
    return open(path, encoding='utf-8').read()
```

- For fukuzawa: loads `results/global_fukuzawa/training.txt` only. No reference to `heldout.txt`.
- `ingest_supermemory_fp` (lines 375-420) chunks `training_text` via `chunk_text(training_text, 3000)` and POSTs each chunk via `/v3/documents`. Only the training-half text flows through.

### Option A ingestion (`run_memory_system.py`)

File: `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/run_memory_system.py`

```python
# lines 107-118
def load_facts(subject):
    if subject == 'hamerton':
        path = os.path.join(BASE_DIR, 'shared_facts.json')
    else:
        path = os.path.join(RESULTS_BASE, f'global_{subject}', 'facts.json')
    data = json.load(open(path, encoding='utf-8'))
    ...
```

Pre-extracted facts loaded from `facts.json`. `facts.json` itself is produced by the upstream pipeline (`run_overnight_pipeline.py`, lines 87-97) which **writes `training.txt` and `heldout.txt` separately**, then runs extraction only on `training.txt`:

```python
# run_overnight_pipeline.py lines 87-97
training = corpus[:mid]
heldout = corpus[mid:]
...
with open(f'{raw_dir}/training.txt', 'w', encoding='utf-8') as f:
    f.write(training)
with open(f'{raw_dir}/heldout.txt', 'w', encoding='utf-8') as f:
    f.write(heldout)
return f'{raw_dir}/training.txt'  # only training.txt is returned / fed to extractor
```

**Level 1 verdict:** Both ingestion paths load training-only content by construction. No code path references `heldout.txt` during ingestion.

---

## Level 2: File integrity (training/heldout split)

Files: `results/global_fukuzawa/training.txt`, `results/global_fukuzawa/heldout.txt`

| file | chars | words | md5 |
|---|---|---|---|
| training.txt | 455,904 | 69,544 | 5dd8b3c8614707a721c1f34743d61cbd |
| heldout.txt | 390,510 | 69,544 | 1ffa0bb6a3a7ae2f7f373c21f1bd7826 |

- Distinct content (different md5). Exactly matched word counts are coincidental (split at paragraph boundary near corpus midpoint).
- **7-gram overlap:** 3 out of 69,433 held-out 7-grams (0.004%) appear in training. All three are generic phrases ("which was also the first year of", "A FINAL WORD ON THE GOOD LIFE", "who did not know the wherefore of") — no narrative passage overlap.
- Spot check of four long distinctive phrases from the held-out half (e.g., "drink had loosened tongues", "rather childlike, perfectly innocent") — **none** found in training.
- Note: training.txt begins with the HTML wrapper from Internet Archive's "Full text of..." page (body starts at char 3089, actual book narrative begins around char 140,703). The HTML wrapper is part of both the ingested Option B chunks and the upstream extraction input. This does not affect leakage — HTML boilerplate is not held-out content — but it does explain why Option B Supermemory indexed many non-narrative fragments and retrieved 0 facts for some questions including Q26.

**Level 2 verdict:** Training and held-out halves are cleanly separated. No passage leakage.

---

## Level 3: Ingested-content verification

### Option B / fullpipeline chunks (direct test)

Re-simulated the actual chunking via `chunk_text(training, 3000)` (25 chunks at 3,000 words each with 200-word overlap — matches `supermemory_fullpipeline_ingestion.json` which logged `chunks_expected: 25`).

- **10-gram overlap of the 25 training chunks vs held-out:** **0 / 69,495** held-out 10-grams found. Zero.
- No chunk contains any 10-word sequence from held-out.

The ingestion log (`supermemory_fullpipeline_ingestion.json`):
```
chunks_expected: 25, chunks_posted: 25, post_success: 19, post_failure: 6
```
19 successful POSTs. The extracted-memories cache (`supermemory_fullpipeline_extracted.json`) is empty (`"memories": []`); Supermemory's native indexing is server-side, not mirrored locally.

### Option A atomic facts (1,657 entries)

Scanned all 1,657 facts in `facts.json` for 5-gram overlap against training vs held-out:

| category | count | % |
|---|---|---|
| training-only match | 794 | 47.9% |
| both (topical overlap) | 51 | 3.1% |
| neither (paraphrased) | 809 | 48.8% |
| held-out-only match | **3** | **0.18%** |

The 3 "held-out-only" facts are:

1. Fact 12: "Fukuzawa Yukichi lived to see the results of his efforts to modernize Japan." — matches generic 5-gram "to see the results of" (held-out context is about students observing the result of a *challenge*, unrelated).
2. Fact 444: "Fukuzawa was hired as an attendant to the head priest of the Buddhist temple Koei-ji in Nagasaki." — matches generic 5-gram "the head priest of the" (held-out context is about a boy who was the son of a head priest, different event).
3. Fact 1653: "The battle of Fushimi occurred in early January of the fourth year of Keio." — matches generic 5-grams "of the fourth year of" and "the fourth year of keio" (held-out context uses the same era naming but describes a separate event — school relocation in spring of Keio 4).

All three are **false positives** — coincidental common phrases (calendar terms, "head priest of the temple"), not semantic leakage of the held-out narrative. The facts themselves describe events whose primary-source basis is in the training half (or shared Fukuzawa history outside the book).

**Level 3 verdict:** No held-out passages leaked into Supermemory's ingested content via either pipeline.

---

## Level 4: Q26-specific audit

### Held-out passage (Q26 ground truth)

From `battery_v2.json` (q_id=26):

> **Question:** "What is Fukuzawa's attitude toward visiting friends whose households have questionable reputations?"
>
> **Held-out passage:** "So I feel no hesitation in paying a visit where there is a young daughter in the house or where the young wife is staying by herself. Or at some feast, if there is a group of geisha enlivening the crowd with their antics, I am not put out by the gayety."

Verified: this passage is **present in `heldout.txt`** and **absent from `training.txt`** (exact substring check on multiple distinctive fragments — all 4 tested fragments confirmed heldout-only).

### Option B / fullpipeline Q26 (score 1.17)

- `supermemory_fullpipeline_retrieval.json["26"]`: `facts_returned: 0`, `fact_texts: []`.
- `supermemory_fullpipeline_results.json` (q_id=26): the C3 response is an **epistemic refusal** — "I cannot answer this question from the behavioral specification provided... Social navigation around friendship and reputation falls into that gap."
- Q26 Option B C3 judge scores: haiku=1, sonnet=1, opus=2, gpt4o=1, gpt54=1, gemini_flash=1 → avg 1.17.

No leakage possible — nothing was retrieved, and the model explicitly abstained.

### Option A Q26 (score 4.33) — the likely target of the concern

`supermemory_retrieval.json["26"]` returned 10 facts:

| # | retrieved fact | origin |
|---|---|---|
| 1 | Fukuzawa learned about the gay quarters by listening to his friends but remained personally detached from such activities. | paraphrased (term "gay quarters" is topical; specific phrasing appears in neither half verbatim) |
| 2 | Fukuzawa does not allow himself to join in gossip about amorous affairs. | paraphrased |
| 3 | Fukuzawa never hesitated to talk on any subject with his friends and often made fun of their follies. | **training** (5-gram "hesitated to talk on any", "to talk on any subject") |
| 4 | Fukuzawa's family was immune from knowledge of anything not reputable. | paraphrased |
| 5 | Fukuzawa claims to have been a pretty clean man otherwise and kept himself within the prescribed limit of a well-behaved man. | **training** (5-gram "to have been a pretty", "been a pretty clean man") |
| 6 | A member of the reception committee drew Fukuzawa into a private room to discuss his personal affairs. | paraphrased (distinctive 4-grams present in training) |
| 7 | Fukuzawa had difficulty finding rooms for the night because innkeepers were afraid of him. | paraphrased (distinctive 4-grams present in training) |
| 8 | Fukuzawa Yukichi did not like to see guests lazily eating and drinking and talking nonsense. | **training** (5-grams "lazily eating and drinking and", "eating and drinking and talking") |
| 9 | Fukuzawa and his friends frequently went to chicken-restaurants. | paraphrased |
| 10 | Fukuzawa was not restraining himself particularly but thought his attitude toward life was what it ought to be. | **training** (5-grams "attitude toward life was what", "toward life was what it") |

For each of the 10 facts:
- Exact phrasings that n-gram-match the corpus match **training.txt** only.
- **None** of the 10 facts' distinctive 4-gram or 5-gram sequences are found in `heldout.txt` (0-match on heldout for all 10).
- The only phrase that appears in *both* halves is the topical word "gay quarters" (refers to the Yoshiwara/Fukagawa districts — a recurring topic across the autobiography); this is topical overlap, not passage leakage.

The held-out Q26 passage itself ("So I feel no hesitation in paying a visit...") is **not** in any retrieved fact. The retrieved facts describe the same *theme* (Fukuzawa's temperance and social conduct) but are independently sourced from the training half.

**Level 4 verdict:** Q26 Option A's elevated C3 score is explained by topical retrieval from the training-half facts — Fukuzawa's temperance and social-conduct orientation is documented in the training half as well, even though the specific episode quoted in Q26's held-out passage is not. This is the expected behavior of the study design, not contamination.

---

## Overall conclusion

**Training-data contamination: NO.**

- Level 1 (code): Ingestion loads training.txt / facts.json only. No code path references heldout.txt.
- Level 2 (files): Training and held-out are cleanly split; 0.004% 7-gram overlap is generic phrases only.
- Level 3 (ingested content): 25 Supermemory fullpipeline chunks have zero 10-gram overlap with held-out. 1,657 Option A facts show only 3/1657 coincidental-phrase "matches" to held-out, all false positives on generic n-grams.
- Level 4 (Q26 specifically): Option B retrieved 0 facts (scored 1.17, refusal). Option A retrieved 10 facts, all sourced from training-half text or paraphrased; the held-out passage itself is not present in any retrieved fact.

The Q26 Option A C3 score of 4.33 reflects that Fukuzawa's temperance and social-conduct disposition is *robustly documented in the training half as well*, so a theme-matched retrieval can support a plausible prediction without needing the held-out episode. This is topical retrieval on a subject whose personality traits are consistent across the corpus — not memorization of the held-out answer.

## Artifacts consulted

- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/run_option_b.py` (lines 78-83, 375-420)
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/run_memory_system.py` (lines 107-118)
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/run_overnight_pipeline.py` (lines 65-97)
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/training.txt`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/heldout.txt`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/facts.json`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/battery_v2.json`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/supermemory_ingestion.json`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/supermemory_retrieval.json`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/supermemory_judgments_merged.json`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/supermemory_fullpipeline_ingestion.json`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/supermemory_fullpipeline_extracted.json`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/supermemory_fullpipeline_retrieval.json`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/supermemory_fullpipeline_results.json`
- `C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_fukuzawa/supermemory_fullpipeline_judgments_merged.json`
- `C:/Users/Aarik/Anthropic/memory-study-repo/scripts/_battery_leakage_results.json` (prior question-level audit; Fukuzawa leak_count=0)
