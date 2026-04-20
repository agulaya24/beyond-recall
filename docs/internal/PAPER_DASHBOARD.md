# Beyond Recall — Launch Dashboard

**Updated:** 2026-04-17 (S113)
**Launch target:** Tuesday 2026-04-21 (4 days out)

Status key: ✅ done | 🟡 in progress | ⬜ not started | ❗ needs review

---

## PAPER — v6 Draft

| Item | Status | Notes |
|---|---|---|
| v6 written end-to-end | ✅ | `docs/beyond_recall_v6_draft.md` |
| Abstract | ✅ | 4 claims structure, representational accuracy frame |
| §1 Introduction | ✅ | §1.1 "Facts do not carry significance" as opener |
| §3 Study Design | ✅ | 3.1 rep accuracy definition, 3.4.1 circularity controls |
| §4 Results (all tables filled) | ✅ | Real numbers from RESULTS_S113.json |
| §5 Discussion | ✅ | 5.1 4-rebuttal primitive defense, 5.6 cross-provider |
| §6 Limitations | ✅ | 14 items |
| §7 Future Work | ✅ | Includes Letta agent-loop diff test |
| §8 Conclusion | ✅ | Opens with "Representational accuracy matters" |
| Editorial checklist at top of draft | ✅ | Aarik to work through before push |
| Aarik voice pass on full paper | ❗ | **Needs your read** |
| Title decision | ❗ | "Missing Primitive" — keep / soften? |

---

## EXPERIMENTS — Data Collection

| Experiment | Subjects | Configurations | Response models | Judges | Status |
|---|---|---|---|---|---|
| Core conditions (C5, C2a, C2c, C4, C4a) | 14/14 | single | 1 (Haiku) | 7 | ✅ |
| Memory systems controlled | 14/14 × 4 systems | 1 | 1 | 7 | ✅ |
| Memory systems native (fullpipeline) | 14/14 × 4 systems | 1 | 1 | 7 | ✅ |
| Base Layer (5th system) | 14/14 | 1 | 1 | 3-6 per subject | 🟡 OpenAI/Gemini backfill |
| C8/C9 raw corpus | 14/14 | 2 | 1 | 7 | ✅ |
| Tier 2 circularity | 3 × 2 response models | GPT-5.4 battery | Sonnet, Gemini Pro | 7 | 🟡 OpenAI backfill |
| Wrong-spec v2 (random derangement) | 14/14 | 1 | 1 (Haiku) | 5-7 per subject | 🟡 OpenAI backfill |
| Letta agent-loop (Packer's test) | 1 (Hamerton) | full loop | n/a | n/a | 🟡 running |
| Semantic top-k overlap | 14 | controlled + native | n/a | n/a (local MiniLM) | ✅ NEW |

### Judging coverage (backfill in progress)

| Judge | Main study | Tier 2 | Wrong-spec v2 | BL (5th system) |
|---|---|---|---|---|
| Haiku | ✅ | ✅ | ✅ | ✅ |
| Sonnet | ✅ | ✅ | ✅ | ✅ |
| Opus | ✅ | ✅ | ✅ | ✅ |
| GPT-4o | ✅ | 🟡 backfill | 🟡 backfill | 🟡 backfill |
| GPT-5.4 | ✅ | 🟡 backfill | 🟡 backfill | 🟡 backfill |
| Gemini Flash | ✅ | 🟡 backfill | 🟡 backfill | 🟡 backfill |
| Gemini Pro | partial (3/14) | ✅ Sonnet responses | ✅ | partial |

### Analysis deliverables

| Item | Status | Notes |
|---|---|---|
| Wilcoxon p=0.006 (C5 vs C4a, N=14) | ✅ | |
| Krippendorff α = 0.535 / 0.659 non-Gemini | ✅ | |
| Gradient regression slope −0.98 [CI −1.30, −0.74] | ✅ | |
| Bootstrap 95% CIs on all headline numbers | ✅ | In RESULTS_S113.json |
| Cross-subject hedging 25% → 0.6% | ✅ | |
| Top-k zero-overlap (exact string) | ✅ | 94%/84%/75%/56% |
| Semantic overlap (MiniLM cosine) | ✅ NEW | 7.6% all-3 top-1 match (controlled) |
| Refresh RESULTS_S113.json after backfill | ⬜ | Do after OpenAI + Gemini complete |
| Per-subject appendix tables | ⬜ | Auto-generate from RESULTS_S113 |

---

## FIGURES

| Figure | Source | Status |
|---|---|---|
| Fig 1 — Global gradient scatter | figures/fig1_global_gradient.png | ❗ regenerate from final data |
| Fig 2 — Compression curve (Hamerton) | fig2_compression_curve.png | ❗ regenerate |
| Fig 3 — Retrieval disagreement | fig3_retrieval_disagreement.png | ❗ regenerate cross-subject |
| Fig 4 — Hedging reduction | fig4_hedging_reduction.png | ❗ regenerate with 25%→0.6% |
| Fig 5 — Condition effects | fig5_condition_effects.png | ❗ regenerate |
| Fig 6 — Wrong-spec control (v1 + v2) | fig6_wrong_spec_control.png | ❗ regenerate |
| Fig 7 — Memory systems C3-C1 | fig7_memory_systems.png | ❗ regenerate honest |
| Fig 9 — Cultural baseline | fig9_cultural_baseline.png | ❗ decide: drop or reframe |

---

## PROVENANCE / TRANSPARENCY

| Item | Status |
|---|---|
| ANALYSIS_PLAN_LOCK.md committed pre-data | ✅ (commit de27b64, 2026-04-16) |
| PROVENANCE_INDEX.md updated to v6 numbers | ⬜ |
| RESULTS_S113.json latest | 🟡 will refresh post-backfill |
| Race conditions memory saved | ✅ |
| Brief-only vs full-stack fix documented | ✅ (§3.4.1) |

---

## OUTREACH — Phase 1 (Tuesday launch)

### Repo + data

| Item | Status |
|---|---|
| Study repo (agulaya24/memory-study-repo) public | ⬜ currently private |
| Main repo (agulaya24/base-layer / BaseLayer) public | ✅ |
| LICENSE Apache 2.0 verified | ✅ |
| README updated for paper launch | ⬜ |
| Link arXiv when ready | ⬜ |

### Grants

| Item | Status |
|---|---|
| AI Grant application | ⬜ |
| Emergent Ventures application | ⬜ |

### Emails (Phase 1 — no arXiv link needed)

| Target | Status |
|---|---|
| Taranjeet Singh (Mem0) follow-up with paper | ⬜ |
| Charles Packer (Letta) — ask for arXiv endorsement + paper | ⬜ |
| Dhruv Diddi (Supermemory) cold | ⬜ |
| Daniel Chalef (Zep) cold | ⬜ |
| Harrison Chase (LangChain) | ⬜ |
| Joao Moura (CrewAI) | ⬜ |
| Jerry Liu (LlamaIndex) | ⬜ |
| Flo Crivello (Lindy AI) | ⬜ |
| Shreya Rajpal (Guardrails AI) ASK FIRST | ⬜ |

### Social / content

| Item | Status |
|---|---|
| Blog post v2 drafted | 🟡 needs Aarik voice pass |
| Blog post goes live base-layer.ai | ⬜ |
| Twitter/X thread drafted | ⬜ |
| LinkedIn article drafted | ⬜ |
| Reddit r/MachineLearning post drafted | ⬜ |
| Reddit r/LocalLLaMA post drafted | ⬜ |
| Figure assets prepared for social | ⬜ |

### arXiv (parallel track)

| Item | Status |
|---|---|
| arXiv account | ⬜ |
| LaTeX conversion of paper | ⬜ |
| Endorsement request to Packer | ⬜ |
| Backup endorser Betley lined up | ⬜ |
| Categories cs.AI primary, cs.CL cross-list | ⬜ |
| License CC BY 4.0 | ⬜ |

---

## POST-LAUNCH / FOLLOW-UP

| Item | Status |
|---|---|
| Phase 2 emails (cited researchers, post-arXiv) | ⬜ |
| HN submission (Phase 2, with arXiv link) | ⬜ |
| Living-subject study (Aarik N=1 first) | ⬜ future work |
| Letta agent-loop diff test (Packer's suggestion) | ⬜ future work |
| Independent pretraining proxy | ⬜ future work |
| Layer ablation (anchors/core/predictions) | ⬜ future work |
| Human-judge validation subset | ⬜ future work |
| Cross-family generation pipeline | ⬜ future work |
