# Paper Reviews — Index

**Paper:** `docs/beyond_recall_v6_draft.md` ("Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization")

**Review protocol:** Recursive cross-LLM review. Each round, the current paper draft is sent to multiple free-tier LLM providers plus Claude (run directly). Substantive findings are triaged into (a) fixable now, (b) requires expanded experiment, (c) stylistic only. (a) gets applied; the draft is re-run until no substantive (a) items remain. See `LLM_REVIEW_FIXES.md` for the consolidated fix tracker.

**Review script:** `scripts/review_paper.py` (Round 1 onward).

---

## Substantive rounds (read these)

### Round 2 — 2026-04-18 (current draft = v6)

| File | Reviewers (of those returning substantive content) | Status |
|---|---|---|
| `round_02_20260418_150505.md` | Gemini 2.5 Flash (truncated), Gemini 2.5 Pro, Groq Llama 3.3 70B, Cerebras Qwen3 235B (focused payload), Mistral Large, Groq minimal payload | Primary Round 2 output |
| `round_02_focused_20260418_150610.md` + `round_02_focused_payload_20260418_150610.md` | Cerebras Qwen3 235B on focused sections (Abstract + §1 intro + §4.3/4.3.1 + §4.4 + §5.7 + §5.8 + Limitations) | Focused-section re-run (payload split) |
| `round_02_focused_20260418_150655.md` + `round_02_focused_payload_20260418_150655.md` | Cerebras re-submit (full Round 2 payload split) | Duplicate of above; same model, same content |
| `round_02_groq_minimal_20260418_150805.md` + `round_02_minimal_payload_20260418_150805.md` | Groq Llama 3.3 70B with 36k-char minimal payload (Groq rejected larger) | Smaller-payload Groq response |

**Round 2 focus questions:** (1) Does §4.4 land honestly, or read as defensive? (2) Is §5.7 fair or biased? (3) Is the abstract's 3-claim disaggregation clear? (4) Is §4.3.1 n=1 Letta result handled with humility? (5) Any overclaiming elsewhere?

**Round 2 verdicts (summary):**
- **Gemini 2.5 Pro:** Substantial and well-argued; repositioning lands honestly; abstract disaggregation exceptionally clear; Letta parity handled with humility. **Critical issues:** (a) central gradient is methodologically circular (C5-as-pretraining-proxy), (b) Letta comparison incomplete (n=1 stateful-agent vs. 14-subject archival misconfiguration). **Methodology concerns:** Gemini judges should be relegated to sensitivity analysis. §5.8 personal tone is unconventional.
- **Mistral Large:** Ready for submission with revisions. Same two critical issues (circularity + Letta n=1). Flags §5.7 Zep "most consistent performer" as residual overclaim. Extrapolation to living users rests on untested source-data equivalence.
- **Cerebras Qwen3 235B (focused):** Framing intellectually honest, methodologically transparent. Flags §5.7 "Zep is the most consistent performer in our data" as overclaim — hedge with "in this study." No critical issues in sections provided.
- **Groq Llama 3.3 70B (minimal payload):** Honest repositioning; main issue is further testing needed for generalization to living users. No fatal flaws.
- **Gemini 2.5 Flash:** Truncated at ~1,179 chars mid-sentence; positive tone ("substantially improved manuscript") but not substantive enough to treat as a full review.

**Round 2 status:** All (a) items being triaged into `LLM_REVIEW_FIXES.md` Round 2 section. Two critical issues (circularity, Letta full generalization) are category (b) "requires expanded experiment" — deferred to Future Work, flagged honestly in Limitations §12 and §7.

---

### Round 1 — 2026-04-14 (against arxiv draft / S109 paper)

| File | Reviewers | Notes |
|---|---|---|
| `round_01_20260414_121257.md` | Groq Llama 3.3 (Gemini Flash/Pro returned 404) | First attempt; Gemini endpoints failed |
| `round_01_20260414_121653.md` | Groq Llama 3.3 (Gemini 404 again) | Retry; still Gemini-down |
| `round_01_20260414_122032.md` | Gemini 2.5 Flash (partial), Cerebras Qwen3, Mistral Large, Groq (413 payload too large) | Substantive round; primary Round 1 content |

**Round 1 key findings (Cerebras, Mistral, Gemini Flash):**
- **Gemini Flash:** No human evaluation, circular LLM-judging-LLM. A- verdict.
- **Cerebras Qwen3:** % calculation misleading, Cohen's d misuse on ordinal data, no aggregate stats across subjects. Major revision requested.
- **Mistral Large:** Historical texts ≠ real users; post-hoc not prediction; statistical overreach on extrapolation. Not ready.
- **Groq:** Payload 413 error, needs truncation to ~30k chars.
- **Gemini Pro:** 503 service unavailable.

**Round 1 fixes applied:** See `LLM_REVIEW_FIXES.md` → "FIXES APPLIED (S110)". Percentage calculation clarified with absolute gains, Cohen's d caveat added, calibration language corrected, "every real user" scoped to "vast majority," hedging metric promoted to §5.5, historical texts acknowledged as proxy in Limitations.

---

### Round 6 — 2026-04-17 (pre-v6 variant, S112)

| File | Reviewers |
|---|---|
| `round_06_20260417_003545.md` | Gemini 2.5 Flash, Gemini 2.5 Pro |

**Round 6 findings:** Paper presents compelling argument. Critical issue flagged: LLM-as-judge validity (Section 3.7). Addressed partially via calibration framework; human validation planned as follow-up.

---

### Earlier Gemini-only reviews (v2/v3 and abstract-only)

| File | Scope | Notes |
|---|---|---|
| `gemini_draft_review.md` | Full draft | Early draft; findings largely superseded by later rounds |
| `gemini_flash_paper_review_v2.md` | v2 paper | Gemini Flash feedback on v2 |
| `gemini_pro_paper_review_v2.md` | v2 paper | Gemini Pro feedback on v2 |
| `gemini_gemini-25-flash_full_review_v3.md` | v3 paper | Gemini 2.5 Flash on v3 |
| `gemini_pro_final_review.md` | Pre-S113 | Gemini Pro "A-" verdict |
| `gemini_abstract_review_gemini-25-flash.md` | Abstract only | Abstract-focused feedback |

These are historical. The v6 draft supersedes v2/v3. Round 2 (2026-04-18) is the current canonical review.

---

## Meta-notes

- **Anthropic (Claude) reviews** are run directly in Claude Code against the paper draft; they are not captured in scripted review files. See `AARIK_REVIEW_S110.md` for the Aarik + Claude pass that drove the S110-S111 overhaul (80 comments).
- **Known provider issues (Round 2):**
  - Gemini 2.5 Flash response truncated at ~1,179 chars.
  - Gemini 2.5 Pro and Mistral Large saw the full 141k-char paper.
  - Cerebras dropped Llama 3.3 70B from free tier since Round 1 (404); fell back to Qwen3 235B.
  - Groq free tier rejected 62k-char focused-sections payload; succeeded on 36k minimal payload.

---

## How to run a new round

```bash
python scripts/review_paper.py --draft docs/beyond_recall_v6_draft.md --round 3 --focus "new focus questions"
```

Results land in this directory as `round_NN_<timestamp>.md`. Update this README after each round.

---

*Last updated: 2026-04-18 (S113). Round 2 complete; no further review rounds needed before Tuesday launch unless substantive claims change.*
