# S114 Session-Close Handoff (2026-04-21)

Read this first when resuming tomorrow.

## What got locked today

Working draft: `docs/beyond_recall_v8_draft.md`

- **Title:** "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization" (changed from "Missing Primitive" after 6-provider panel)
- **§1 (all)** — now with H1-H5 hypothesis block + primary/secondary outcomes + 5-judge primary numbers (sweep applied during session close)
- **§2 (all)**
- **§3 (through §3.7.6)** — new subsection §3.7.6 surfaces rubric-handling validity audit; §3.7 opener names recursive-evaluation structure
- **§4.1 + §4.1.1 Franklin + §4.1.2 Living-user pilot (author)** — Δ +2.00, study's largest lift, 75% anchor-crossing
- **§4.2 + §4.2.1 Question-Improvement Rate** — compression efficiency + new secondary metric proposal (win rate against baseline + reporting triplet + failure modes)

## Numbers now canonical (5-judge primary, all in v8)

- Gradient slope: −0.96 [95% CI −1.24, −0.67], R² = 0.82, p < 0.001
- Wilcoxon C5 vs C4a: W = 11, p = 0.007
- Wilcoxon C5 vs C2a: W = 10, p = 0.005
- All-14 positive on Δ_C4a: 12 of 14
- Low-baseline (n=9) mean Δ_C4a: +0.89
- Per-response anchor-crossing rate (low-baseline): 55.0%
- Spec-alone question-improvement rate: 70.9%
- Franklin baseline (5-judge primary): 3.77 (was 4.10 Haiku-only)
- Author pilot: C5=1.03, C2a=2.86, C2c=2.59, C4=2.93, C4a=3.02

## Figures generated

- `figures/fig_4_1_gradient_scatter.png` + `.pdf`
- `figures/fig_4_2_compression.png` + `.pdf`

## Cross-section sweep applied during session close

The final collective review (4-provider panel, at `docs/reviews/s114_final_locked_content_review_20260421_215603.md`) caught major §1-vs-§4 inconsistencies. Fixed during session close:

- §1.2 "four claims" → "five claims"
- §1.3 gradient numbers updated from 7-judge (slope −0.98, p 0.0063, low-baseline +1.04) to 5-judge primary (−0.96, p 0.007, +0.89)
- §1.3 Compression numbers updated: Hamerton C2a 3.04 → 2.63, C8 2.32 → 2.27, C4a 3.22 → 2.77
- §1.3 compression framing rewritten from "spec beats raw source" to "spec captures most of corpus lift at 5% of context"
- §1.4 pilot reconciliation: removed contaminated N=10 pilot reference; now points at §4.1.2's clean N=40 pilot
- §1.4 "two highest baseline subjects" fact corrected (Zitkala-Sa and Equiano are mid-baseline, not highest)
- §3.1 "seven judges" → "five primary judges"
- §3.2 Franklin 4.10 → 3.77 on 5-judge primary (with legacy note)
- §4.1.3 forward reference removed (§4.1.3 doesn't exist; content deferred to §4.1 + §4.6)
- §3.6 §4.4 hedging reference → §4.3 (hedging lives in Mechanism, not Memory-System Composition)

## Panel issues flagged but NOT yet fixed (tomorrow's first items)

Ordered by urgency:

### Critical — must fix before §4.3

1. **§2.5 stub.** GPT-5.4 and Opus both flagged: §2.5 "LLM-as-judge" appears as a header with minimal or no content. Check the section and either fill it or remove the stub.
2. **§1.3 "The correct specification shifts response models in the opposite direction: baseline hedging of 25.0% drops to 2.6%..."** — the 25.0% / 2.6% / 0.6% numbers still need verification against 5-judge primary. May be 7-judge leftover.

### High — should fix before §5 Discussion

3. **§1.1 "No current benchmark is built to measure it"** — Opus flagged: Twin-2K (§2.3) is acknowledged as measuring behavioral prediction. Qualify or sharpen.
4. **§1.4 "baseline is at or below 1.0 by construction"** — GPT-5.4 flagged as too strong. Author pilot landed at 1.03 which is consistent, but "by construction" reads as a priori not empirical. Consider softening to "as an empirical expectation."
5. **§1.4 "Language models optimize for the median"** paragraph — GPT-5.4 flagged as easy to attack. Consider removing or softening.
6. **§1.3 Keckley Q21 "informative positive finding, not a specification defect"** — Mistral + GPT-5.4 both flagged as too defensive. Reframe as interpretation rather than settled conclusion.
7. **§1.3 wrong-spec "The 60.6% is a content-grounded detection rate"** — Mistral flagged: present as lower-bound rather than definitive.
8. **§2.3 Twin-2K "71.83% accuracy at 18:1 compression (p=0.008)"** — Opus flagged: p-value unexplained, methodology not given, ungrounded in Related Work. Add brief methodology note or move to §4.8.

### Medium — fix during next sweep

9. **§4.1.2 author-pilot review vulnerability.** Opus's most-severe flag: the wrong-spec control (+1.56) vs. correct spec (+1.84) gap of 0.28 points on N=40 is not clearly distinguishable from noise. Current text addresses it as "Franklin happens to share values-based scaffolding," which reads as post-hoc. Consider sharpening — this is the single most reviewable vulnerability in §4.1 as Opus notes.
10. **Voice check.** Mistral flagged: "beats the baseline" in §1.3 Mechanism (replace with "outperforms"), "flipped the prediction" in §4.1 Example B (replace with "corrected"), "picking up" in §4.2.1 (replace with "capturing").

## Pending structural tasks

- §4.3 through §4.8 — draft next
- §5 Discussion
- §6 Limitations
- §7 (folded into §2 or standalone?)
- §8 Future Work (task #49 — includes differentiated rubric, length-controlled scoring, benchmark proposal, multi-subject living-user replication, human validation, component ablation)
- Appendix C (task #26 — extended experimental conditions)
- Appendix D (tasks #29 + #50 consolidated — per-subject breakdown + validity audit)
- Appendix E (task #16 — extended benchmark analysis)
- Abstract (last)

## Session completion tasks that need attention

| # | Task | Status |
|---|---|---|
| 27 | Paper-wide condition-identifier gloss sweep | pending |
| 30 | Paper-wide units consistency sweep (chars/words/tokens) | pending |
| 32 | Paper-wide 7→5-judge sweep | in progress — deterministic fixes applied; framing flags above remain |
| 41 | Pre-release outline/title/heading alignment | pending (do near launch) |

## What to start with tomorrow

1. Read this file.
2. Apply Critical + High fixes above (§2.5 stub, hedging numbers verification, softenings).
3. Begin §4.3 Mechanism with spec-activation numbers (78.6% correct / 50% wrong-spec tag citation) + three collective-identified mechanism types (identity disambiguation, directional correction, interpretive inference).

## Data / code state

- Paper working draft: `docs/beyond_recall_v8_draft.md`
- Canonical recompute: `docs/research/recompute_5judge_primary.md`
- Spec activation: `docs/research/spec_activation_analysis.json`
- Anchor crossing: `scripts/compute_anchor_crossing.py` output
- Question improvement: computed in recompute script
- Validity audit: `docs/research/s114_low_end_inflation_audit.json`
- Author pilot: `_internal/aarik_clean_pilot/` (private, internal-only)
- Figures: `figures/fig_4_1_gradient_scatter.{png,pdf}` + `fig_4_2_compression.{png,pdf}`
- Knowledge index (FTS + semantic): last refreshed today, 3,872 chunks at `workspace/study_knowledge.db`

## Git status

~100 uncommitted files in study repo. Not committed per protocol; needs explicit commit request from author tomorrow.

## Voice rules active (do not relax)

- No em-dashes in prose (tables / code blocks OK)
- No GTM verbs (beats / crushes / dominates) — prefer outperforms / exceeds
- Layman-first on findings, technical body follows
- No reader-addressing in methodology sections
- Direct declaratives
- Condition gloss on first mention per section (task #27 still pending)
- "Raw data available at..." convention
- Primary-source references
- Title: "Interpretive Layer" not "Missing Primitive"
