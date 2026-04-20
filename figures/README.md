# `figures/` — Publication figures for the "Beyond Recall" paper

These 9 PNGs are the paper's publication-quality figures, rendered at 300 DPI. The v6 draft ([`../docs/beyond_recall_v6_draft.md`](../docs/beyond_recall_v6_draft.md)) embeds most of these only implicitly — the prose states the numerical claim, the figure visualizes it. Use the table below to map each figure to the claim it supports.

For the canonical numbers behind every figure, see [`../docs/DATA_REFERENCE.md`](../docs/DATA_REFERENCE.md).

## Figure catalog

| File | What it shows | Supports claim in paper | Underlying data |
|---|---|---|---|
| `fig1_global_gradient.png` | Per-subject baseline (C5) vs. spec+facts score across all 14 subjects, ordered by baseline. Visualizes the gradient result (spec helps most where baseline is low). | §1.3 Finding 1, §4.1-4.2 (the gradient table and Wilcoxon p=0.006, slope −0.98) | 14-subject baseline/spec arrays hardcoded in `generate_figures_v3.py` (sourced from the harmonized `summary.json` that produced `docs/DATA_REFERENCE.md`) |
| `fig2_compression_curve.png` | Log-tokens vs. normalized prediction score. Shows that ~5K-token spec beats 34K-token raw corpus. | Explicitly called out at line 715 of the v6 draft ("Figure 2: Compression curve"); supports §4.5 (Hamerton C2a 3.04 vs C8 2.32) | Hamerton C2a / C4a / C8 / C9 scores from `results/hamerton/` |
| `fig3_retrieval_disagreement.png` | Top-k retrieval disagreement rate across the three embedding-based memory systems (Mem0, Letta, Supermemory) at k=1, 3, 5, 10. | §1 abstract and §4 memory-systems discussion (93% disagreement at top-1, 53% at top-10) | Per-subject retrieval files `results/<subject>/{mem0,letta,supermemory}_retrieval.json` |
| `fig4_hedging_reduction.png` | Hedging/refusal rate across C5 → C2a → C4a conditions. Baseline 25.0% drops to 2.6% with spec, to 0.6% with facts+spec. | §1.3 Finding 4, §5 hedging analysis | Response-text analysis of `results/global_*/baselayer_results.json` and `results/global_*/c8_c9_results.json` |
| `fig5_condition_effects.png` | Condition-by-condition mean deltas across subjects. Multi-panel summary of the core conditions (C1, C2a, C2c, C3, C4, C4a, C5, C6, C7, C8, C9). | §4 core results tables; orientation figure for readers scanning the condition space | Aggregated from every `results/<subject>/*_results.json` |
| `fig6_wrong_spec_control.png` | Correct-spec score vs. wrong-spec (random derangement) score per subject. Shows wrong-spec lands near baseline. | §1.3 Finding 3 and §4.4 (content, not format) | C2c_wrong_spec condition output in `results/<subject>/baselayer_results.json` |
| `fig7_memory_systems.png` | Per-system spec delta (C3 minus C1) for Mem0, Letta, Supermemory, Zep, and Base Layer on the 9 low-baseline subjects. | §1.3 Finding 2 and §4.3 (spec is additive to every commercial system) | `results/<subject>/{mem0,letta,supermemory,zep}_results.json` + `baselayer_results.json` |
| `fig8_judge_agreement.png` | Inter-judge agreement across the 6-judge panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash). Correlations / alpha across subjects. | §3.6 judge calibration and §5 inter-judge reliability discussion | Per-judge `results/<subject>/*_judgments_{haiku,sonnet,opus,gpt4o,gpt54,gemini_flash}.json` + `judgments_merged.json` |
| `fig9_cultural_baseline.png` | Baseline score by subject culture / origin. Shows baseline is correlated with Western-canon pretraining exposure, not subject "quality". | §4 gradient discussion; addresses reviewer concern that the gradient might be confounded by corpus difficulty rather than pretraining density | 14-subject C5 baselines (same source as Figure 1) |

## How the figures are generated

| Script | Purpose |
|---|---|
| `generate_figures.py` | v1 — superseded. Kept for reference. |
| `generate_figures_v2.py` | v2 — superseded. Kept for reference. |
| `generate_figures_v3.py` | **Canonical.** Regenerates all 9 PNGs. The 14-subject baseline and spec arrays are inlined at the top of the script (sourced from the harmonized rerun `summary.json`). Run: `python generate_figures_v3.py` — writes PNGs next to the script. |

If you update the underlying scores, edit the inlined arrays in `generate_figures_v3.py` to match `../docs/DATA_REFERENCE.md` and rerun. The v3 generator does not re-read raw results files; it is the rendering layer, not the analysis layer.

## Older exploratory figures

Earlier exploratory plots (including figures that focus on individual subjects or judge behavior) live in [`../charts/`](../charts/). `charts/` predates the v3 publication figures. For paper claims, always prefer the `figures/` set.
