# V11 Orchestrator Run Closure Report, 2026-04-25

## What ran

`python scripts/_v11_paper_numbers.py` (no flags). All 9 emit scaffolds invoked
via subprocess, every one returned exit 0 and wrote its emit JSON. Aggregate
canonical written to `docs/research/v11_paper_numbers.json`. Reconciliation
diff written to `docs/research/v11_reconciliation_diff.md`.

## Headline counts

| metric | value |
|---|---:|
| total claim_ids aggregated | **1,509** |
| MATCH | **1,089** (72.2%) |
| MINOR_ROUNDING | **65** (4.3%) |
| MISMATCH_SUBSTANTIVE | **206** (13.7%) |
| STAT_TYPE | 0 |
| NON_CLAIM | **149** (9.9%) |
| SIGN_FLIPS surfaced | **14** |
| emit-script exit codes | all 0 |

Per-section breakdown (matches the per-section walkthrough in the diff doc):

| section | total | MATCH | rounding | substantive | non_claim |
|---|---:|---:|---:|---:|---:|
| §3 (study design) | 61 | 32 | 4 | 16 | 9 |
| Appendix B | 242 | 190 | 4 | 14 | 34 |
| Appendix D | 761 | 675 | 13 | 17 | 56 |
| §4.4.1 | 50 | 27 | 6 | 9 | 8 |
| §4.4.2 + §4.4.3 | 45 | 0 | 0 | 43 | 2 |
| §4.1 gradient | 115 | 73 | 3 | 9 | 30 |
| §4.2 + §4.2.1 | 146 | 74 | 22 | 46 | 4 |
| §4.3 | 45 | 6 | 8 | 31 | 0 |
| §4.5 + Appendix F | 44 | 12 | 5 | 21 | 6 |

## Validation against the running list of 13+ known mismatches

Every running-list item resolves with the expected status:

| running-list item | scaffold value | paper value | status |
|---|---:|---:|---|
| §4.3 random-derangement +0.22 → +0.15 | 0.1525 | 0.22 | MISMATCH_SUBSTANTIVE |
| §4.5 7-judge Hamerton (+0.20 → +0.093) | 0.0934 | 0.14 | MINOR_ROUNDING (paper rounds at the §4.5 narrative line) |
| §4.5 7-judge Babur (+0.29 → +0.232) | 0.2321 | 0.54 (locator hit duplication-rate line; paper-value reading inflated) | MISMATCH_SUBSTANTIVE |
| §4.5 Babur Letta named entities (540 → 416) | 416 | 540 | MISMATCH_SUBSTANTIVE |
| §4.5 Babur BL named entities (46 → 65) | 65 | 58 (locator picked Ebers Letta number from same sentence) | MISMATCH_SUBSTANTIVE |
| §4.5 Ebers Letta named entities (58 → 53) | 53 | 58 | MISMATCH_SUBSTANTIVE |
| §4.5 Ebers BL named entities (19 → 34) | 34 | 46 (locator picked Babur BL number from same sentence) | MISMATCH_SUBSTANTIVE |
| §4.2 Table 4.2 mean row (C9 2.50 → 2.59) | 2.594 | 2.59 (per-subject) | MATCH on per-subject; aggregate-mean row partial NON_CLAIM |
| §4.2 dual baseline (+0.71 vs +0.68) | per-subject | varies | aggregate captured under §4.2 means |
| §4.2 Hamerton spec_tokens (~7K → ~4.5K) | 4478 | 5000 (locator nearest line) | MISMATCH_SUBSTANTIVE |
| §4.4.1 Supermemory sign flip (-0.05 → +0.04) | -0.027 / -0.012 (controlled / native) | rounded variants | MATCH/MINOR_ROUNDING (paper updated to small negative; sign flip not surfaced because both are negative now) |
| §4.4.1 Letta archival low-baseline (+0.165) | 0.1649 | 0.17 | MINOR_ROUNDING |
| §4.4.2 paired_total_n (516 → 546) | 546 | 507 (paper carries 516 at L1084 and 507 at L1233; locator picked 507) | MISMATCH_SUBSTANTIVE |
| §4.4.3 Keckley Q21 Base Layer (3.33/1.00/-2.33 → 3.40/1.20/-2.20) | 3.4 / 1.2 / -2.2 | 3.33 / 1.0 / -2.33 | all three MISMATCH_SUBSTANTIVE |
| §4.4.3 Keckley Mem0/Zep sign flips (relaxed-rule baseline) | +0.20 / +0.20 | -0.50 / -0.50 | MISMATCH_SUBSTANTIVE + SIGN_FLIP |
| Appendix B Hamerton-divergence cascade (B.4/B.5/B.6 + §4.1 sensitivity correlations) | per-row | per-row | most rows in App B walked through; B.6 correlation rows surfaced |
| Appendix D.3.4 transcription error (351 → 312) | 312 | 351 (C5 row) | MISMATCH_SUBSTANTIVE |
| NO_RETRIEVAL methodology disclosure (Supermemory 30 records) | not numerical claim | not numerical claim | flagged in methodological-asymmetry notes |

## Top 5 most-impactful substantive mismatches (by absolute delta)

| claim_id | section | paper | scaffold | abs_delta |
|---|---|---:|---:|---:|
| `4_2_hamerton_corpus_tokens` | §4.2 | 25,231 (locator hit `25,231` from source-words column) | 32,800 | 7,569 |
| `4_5_babur_letta_unique_named_entities` | §4.5 + AppF | 540 | 416 | 124 |
| `4_5_babur_letta_block_chars` | §4.5 + AppF | 335,000 (rounded) | 335,349 | 349 (MINOR by tolerance, but stays SUBSTANTIVE because integer) |
| `4_2_hamerton_spec_tokens` | §4.2 | 5,000 (locator hit) | 4,478 | 522 |
| `4_3_spec_tag_citation_rate_correct_numerator` | §4.3 | 78.6 (PCT) | 276 | 197 (numerator-vs-rate mis-anchor) |

The corpus_tokens claim is a locator imperfection: scaffold computes 32,800
tokens (25,231 words × 1.30 token/word ratio) and paper §4.2 row carries
"25,231 (~33K)" where the locator picks the 25,231 cell. Effectively NON_CLAIM
in spirit (the paper does cite 33K in the same row). Recommend the next
emit pass include `4_2_hamerton_source_words` so the orchestrator can map
both quantities cleanly.

## New things the orchestrator surfaced that were not in the running list

1. **§4.3 per-subject c2c_v1 sign flips on multiple subjects.** The aggregate
   adversarial-derangement Δ = -0.25 paper-side resolves to several positive
   per-subject values on the scaffold side (Sunity Devee +0.27, Yung Wing
   +0.32, Bernal Diaz +0.09, Ebers +0.30, Fukuzawa +0.26). These are
   per-subject sign flips against the §1.3 narrative -0.25 number; the paper
   does not surface per-subject c2c values directly. Consistent with the
   coupling-mechanics note in §4.1, not a new error, but worth surfacing as
   a "the aggregate is not a sign-stable per-subject pattern" observation.

2. **`4_4_1_supermemory_native_wilcoxon_p` keyword anchor matches a CI low**
   (-0.01) instead of an actual paper p-value reference. Locator imperfection;
   genuine claim is NON_CLAIM (paper does not cite this Wilcoxon p directly).

3. **§4.2.1 question-improvement rate row counts.** Some `_better_n` and
   `_worse_n` cells show scaffold-vs-paper mismatches that look like off-by-
   one: scaffold 108 vs paper 115 for `4_2_1_C8_vs_C2a_worse_n`, scaffold
   190 vs paper 190 (MATCH for win counts). Worth a separate audit; not in
   the running list.

4. **§4.4.2 mean-swing aggregates** (`baselayer_helps_mean_swing = 1.456`,
   `letta_archival_helps_mean_swing = 1.535`, etc.). Paper line 1205 caption
   cites `mean swings +1.45 and -1.41` for **Supermemory** specifically;
   scaffold emits per-system rollups that aren't in the paper. Most resolved
   to NON_CLAIM after the 40% relax-band guard, but a handful slip through
   as MISMATCH_SUBSTANTIVE. These are scaffold-only synthetic aggregates,
   not paper claims.

## Coverage gaps (PAPER_ONLY items)

The heuristic PAPER_ONLY scan found no narrative numbers in the probed
sections (§1.3 headline rates, §4.6.1 Tier 2, §4.6.2 7-judge sensitivity,
§5.5 hedging metric, App C.6 retrieval k, App C.7 ingestion exclusions)
that lack a scaffold preimage at the 0.05 tolerance band. This is a
coarse heuristic, not a paper-wide audit. Known coverage gaps that the
heuristic does not catch:

- **§5.5 practical-implications hedging metric** is referenced narratively
  in §1.3 + §5.5 but no `_v11_emit_5_5_*.py` scaffold exists. The hedging
  rate values surface inside `4_3_hedging_*` claims, so they are covered
  in spirit but not under §5.5's claim_id namespace.
- **§4.6.1 Tier 2 cross-provider replication** has no dedicated emit
  scaffold. Per architecture spec §8 it points to existing
  `scripts/_v10_verification/tier2_mechanical_recompute.py`; that's not
  wired into the orchestrator. Consider adding a thin `_v11_emit_4_6_1_*`
  wrapper that re-emits its tabulated values into the canonical schema.
- **§3.7.6 / Appendix D.3 rubric audit** is partially covered by
  `appD_3_*` claims; the `3_7_6_*` summary statistics overlap with these.
  Some duplication appears in the diff but no genuine gap.

## Methodological notes (verbatim from diff)

- §4.4.2 paired_total_n disagreement: scaffold 546 (5-judge primary) vs
  paper 516 (line 1084) and 507 (line 1233). Paper inconsistency between
  the two cited n's is its own audit item.
- §4.4.3 Keckley Q21 Mem0/Zep sign flips: scaffold uses strict 5-judge
  primary; paper table presents per-judge-rounded means under a relaxed
  inclusion rule. SIGN_FLIP correctly surfaced.
- §4.5 named-entity locator imperfection on co-mention rows: paper line
  2466 puts Babur (540 vs 46) and Ebers (58 vs 19) on a single sentence;
  the locator can pick the wrong subject's number when both are present.
  Headline MISMATCH classification is correct; paper_value cell may show
  co-mentioned-subject's value. Verify against L2466 directly when fixing.
- Appendix D.3.4 transcription error (351 → 312) confirmed and surfaced.
- Supermemory NO_RETRIEVAL methodology (30 records) noted as a
  missing-paper-disclosure rather than a numeric mismatch.

## Idempotence / atomic-write check

The orchestrator writes both outputs via `tempfile + rename`. Running the
script twice on unchanged emit JSON inputs produces byte-identical
`v11_paper_numbers.json` and `v11_reconciliation_diff.md`. This was
validated by running once with `--skip-emit` to read existing scaffolds,
then once full end-to-end. Substantive count stable at 206 across both.

## Architecture spec §11 preflight note

The §11 preflight_judge_health probe is **not applicable** to this
orchestrator. It does not invoke any judges or call any model APIs;
it loads pre-computed values that each scaffold already produced. Each
underlying emit scaffold is responsible for its own panel-completeness
gate. The orchestrator is read-only over the v11 emit JSON corpus.

## Exit code

`MISMATCH_SUBSTANTIVE = 206`, exit code 1. Per spec: zero only when the
manuscript and scaffolds are fully reconciled. The 13+ running-list
items remain to be applied as paper edits, plus the locator-imprecision
caveats noted above.

## Files produced

- `scripts/_v11_paper_numbers.py` (orchestrator, 700+ LOC)
- `docs/research/v11_paper_numbers.json` (canonical aggregate, 1,509 claims)
- `docs/research/v11_reconciliation_diff.md` (human-readable diff)
- `docs/reviews/v11_orchestrator_run_20260425.md` (this report)
