# `charts/` — Exploratory and secondary figures

This directory contains **earlier exploratory plots** produced during the study. They predate the paper's v3 publication figures in [`../figures/`](../figures/). Prefer `figures/` for paper claims.

A few of these charts are still useful for readers who want auxiliary views (e.g., subject-specific judge agreement, or the Hamerton/Franklin contrast visualized rather than tabulated), so they remain in the repo.

## Chart catalog

| File | What it shows | Status / where to look now |
|---|---|---|
| `bimodal_to_gradient.png` | Earlier framing: the shift from viewing the result as a "bimodal known/unknown split" to viewing it as a continuous gradient on baseline. | Historical. The gradient framing is the final one — see `figures/fig1_global_gradient.png` and §4 of the paper. |
| `compression_story.png` | Earlier view of the compression argument (tokens in vs. score). | Superseded by `figures/fig2_compression_curve.png`. |
| `franklin_judge_agreement.png` | Judge agreement on the Franklin known-figure battery. | Secondary. Useful as a subject-level sanity check on §4.7 (Franklin ceiling). |
| `hamerton_full_hierarchy.png` | Condition-by-condition breakdown for Hamerton (the deep-dive reference subject). | Secondary. Useful companion to §4.1 and §4.5. |
| `hamerton_vs_franklin.png` | Side-by-side contrast of the Hamerton (low-baseline) and Franklin (high-baseline) responses to the same conditions. | Secondary. Directly visualizes the "spec is a tool for the unknown" framing. |
| `judge_agreement.png` | Earlier inter-judge agreement view. | Superseded by `figures/fig8_judge_agreement.png`. |
| `unknown_vs_known.png` | Early "unknown vs known" framing plot. | Historical. The final paper uses the continuous-gradient framing (fig1), not a binary split. |
| `pipeline_diagram.md` | **Text description of the pipeline**, not an image. Intended as a spec for an external designer to render. See §3 of the paper for the corresponding narrative description of extract → embed → author → compose → serve. | Source-of-truth description of the pipeline stages; no image has been rendered from it for this release. |

## Relationship to `figures/`

| If you want... | Look here |
|---|---|
| A figure that supports a specific paper claim | [`../figures/README.md`](../figures/README.md) |
| An exploratory subject-specific view | This directory |
| The pipeline as a diagram | `pipeline_diagram.md` (text spec) |
