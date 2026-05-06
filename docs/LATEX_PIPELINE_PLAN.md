# LaTeX pipeline plan — Beyond Recall arXiv submission

**Goal.** Convert the markdown manuscript at `docs/beyond_recall_v11_8_draft.md` into an arXiv-submission-ready LaTeX package. Single `.tar.gz` upload containing `.tex`, `.bib`, all figures, and a buildable PDF target.

**Estimated effort:** 3-4 hours of engineering, split into four phases. No new content authoring; this is a structural conversion.

**Prerequisite.** v11.8 markdown is content-locked (final paper walks complete; no further section reorganization). Figure files are stable. References are stable. Recommended to run after the §3, §4, §7 walks complete and final cross-LLM review pass lands.

---

## Phase 1 — Pandoc baseline + arXiv preamble (~1 hr)

**Goal.** Single compilable `.tex` file. Ugly but functional.

1. **Initial pandoc conversion.**
   ```bash
   pandoc docs/beyond_recall_v11_8_draft.md \
     -o build/beyond_recall.tex \
     --from markdown+yaml_metadata_block+pipe_tables+grid_tables \
     --to latex \
     --standalone \
     --bibliography=build/beyond_recall.bib \
     --citeproc=false \
     --top-level-division=section
   ```

2. **Custom preamble.** Replace pandoc's default preamble with arXiv-friendly:
   - `\documentclass[11pt]{article}` (arXiv prefers article over IEEEtran for non-conference submissions)
   - Page geometry: `\usepackage[margin=1in]{geometry}`
   - Math: `\usepackage{amsmath, amssymb, amsthm}`
   - Tables: `\usepackage{booktabs, longtable, array, tabularx, makecell}` (booktabs for clean rules, longtable for multi-page tables, tabularx for column-width control)
   - Figures: `\usepackage{graphicx, float}` + `\graphicspath{{../figures/}}`
   - Hyperlinks: `\usepackage[colorlinks=false, hidelinks]{hyperref}` (arXiv convention: hide colored boxes)
   - Citations: `\usepackage[round, numbers, sort&compress]{natbib}` OR `\usepackage{biblatex-chicago}` (Chicago author-date is closer to current §9 style)
   - Code/paths: `\usepackage{listings}` for code blocks; `\texttt{}` for inline file paths
   - Captions: `\usepackage{caption}` with `singlelinecheck=false` so figure captions wrap properly

3. **Title page.** Replace pandoc's auto-title with explicit:
   ```latex
   \title{Beyond Recall: Behavioral Specification as an Interpretive Layer\\for AI Personalization}
   \author{Aarik Gulaya\thanks{aarikgulaya@gmail.com; independent researcher.}}
   \date{\today}
   \maketitle
   \begin{abstract}
   ...abstract text once written...
   \end{abstract}
   ```

4. **Section-numbering depth.** arXiv default goes to subsubsection (1.1.1). If §3.6.6 needs `\subsubsection`, set `\setcounter{secnumdepth}{4}` (which extends to `\paragraph`-level numbering).

5. **First compile.** `pdflatex` the result to confirm it builds. Many issues will surface here; defer to Phase 2.

**Deliverable for phase 1:** `build/beyond_recall.tex` that compiles to a (ugly) PDF.

---

## Phase 2 — Tables, figures, footnotes, cross-refs, bibliography (~1 hr)

**Goal.** Functional content. Tables render, figures render, citations resolve.

1. **Bibliography conversion.** Markdown §9 references → BibTeX entries in `build/beyond_recall.bib`. 18 entries. Each `@article{` for arXiv preprints, `@book{}` for Bartlett 1932, `@inproceedings{}` for venue-published works (Maharana ACL, Wu ICLR, Zheng NeurIPS, Samuel ACL Findings, Jiang COLM). Citation key convention: `surname_yyyy_short` (e.g., `chen_2025_personavectors`, `bartlett_1932_remembering`).
   - Replace inline `Maharana et al., ACL 2024, arXiv:2402.17753` with `\citep{maharana_2024_locomo}` etc.
   - Use `natbib` `\citep` (parenthetical) and `\citet` (textual) appropriately.
   - Switch §9 References section to `\printbibliography` (biblatex) or `\bibliography{beyond_recall}` (bibtex).

2. **Tables.** Pandoc converts pipe tables but produces ugly LaTeX. Manual cleanup of the heavy tables:
   - **Table 2.1** (memory system comparison) — wide; use `tabularx` with `X` columns sized to fit; or `longtable` if it spans pages. Wrap cell content with `\makecell` for line breaks.
   - **Table 4.1** (per-subject gradient) — long, needs `longtable`.
   - **Table 4.6** (per-system Pattern 3 cells) and similar — fine in `tabular`.
   - **Appendix B** subject-level tables — `longtable` or split.
   - Convert horizontal rules to `\toprule \midrule \bottomrule` (booktabs).

3. **Figures.** All figures live at `figures/fig_*.png` and `.pdf`. arXiv prefers PDF over PNG for vector figures.
   - 4 active figures: `fig_4_1_gradient_scatter_v3`, `fig_4_2_compression_v3`, `fig_4_2_1_question_improvement_rates_v3`, `fig_4_4_1_jaccard_heatmap_v1`.
   - Replace markdown `![caption](path)` with `\begin{figure}[ht] \centering \includegraphics[width=\linewidth]{filename} \caption{...} \label{fig:...} \end{figure}`.
   - Add `\label{fig:gradient}` etc. and convert any in-text references to `\ref{fig:gradient}` or `Figure~\ref{fig:gradient}`.
   - Use the v3 PNGs from `figures/` directly; LaTeX bundles them into the source via the `figures/` dir referenced in `\graphicspath`.

4. **Footnotes.** Pandoc converts `[^name]` to `\footnote{}` but loses the labels. Run a sed pass to convert `[^name]: definition` defs into a footnote registry, then place each `\footnote{definition}` at the citation site. ~70 footnotes total.

5. **Cross-references.** Markdown anchor links `[§4.1.1](#411-...)` → `\autoref{sec:per-question-baseline}` after labeling each section with `\label{sec:...}`. ~50 cross-refs in body text.

6. **Inline math.** Spot-check for any `$...$` math in the markdown (unlikely; this paper is mostly prose). If present, ensure proper LaTeX rendering.

7. **Special characters.** Ensure UTF-8 source compiles cleanly: `Bābur`, `Díaz`, `Eugénie`, ρ (rho), Δ (delta), ≥ (gte), ≤ (lte), ± (plusminus). Use `\usepackage[utf8]{inputenc}` (or `xelatex` with `fontspec` for full Unicode).

**Deliverable for phase 2:** `build/beyond_recall.tex` with functional tables, figures, citations.

---

## Phase 3 — Polish, typography, page layout (~1 hr)

**Goal.** Submission-grade aesthetics.

1. **Page layout.**
   - Break long tables across pages with `longtable` if needed.
   - Avoid widow/orphan single-line paragraph splits — `\widowpenalty=10000 \clubpenalty=10000`.
   - Keep figures near their first reference: `[ht]` placement, `\FloatBarrier` from `placeins` package between sections to prevent figures drifting.

2. **Typography.**
   - Em-dashes: arXiv source can use `---` (LaTeX en-dash) rendered as em-dash. But Aarik's no-em-dash rule: ensure the markdown's em-dash purges have propagated to the LaTeX source. Run a `\(--\)` (en-dash) and `\(---\)` (em-dash) sweep on the .tex.
   - Quotation marks: LaTeX uses ` for left and ' for right; pandoc usually handles this but verify a few.
   - File paths in `texttt`: `\texttt{scripts/analyze_retrieval_overlap.py}` rather than monospace markdown ticks. Add `\usepackage{url}` for URL line-breaking.

3. **Section labels.**
   - Every `\section`, `\subsection`, `\subsubsection` gets a `\label{sec:slug}`.
   - Cross-references use `\autoref{}` or `\Cref{}` (cleveref) for consistent "Section 4.1" rendering.

4. **Page breaks before appendix.** `\appendix` command before Appendix A; renumbers as A, B, C, ...

5. **Header / footer.** Optional: `\usepackage{fancyhdr}` with paper title in header, page number in footer. arXiv usually doesn't care; default is fine.

6. **Compile cleanly.** Two-pass: `pdflatex` → `bibtex` → `pdflatex` → `pdflatex`. Or `latexmk -pdf beyond_recall.tex`. Aim for zero warnings.

**Deliverable for phase 3:** `build/beyond_recall.pdf` — submission-grade.

---

## Phase 4 — arXiv submission packaging (~30 min)

**Goal.** A `.tar.gz` arXiv accepts on first upload.

1. **Directory structure.**
   ```
   beyond_recall_arxiv/
   ├── beyond_recall.tex
   ├── beyond_recall.bib
   ├── beyond_recall.bbl       (pre-built; arXiv doesn't run bibtex)
   ├── figures/
   │   ├── fig_4_1_gradient_scatter_v3.pdf
   │   ├── fig_4_2_compression_v3.pdf
   │   ├── fig_4_2_1_question_improvement_rates_v3.pdf
   │   └── fig_4_4_1_jaccard_heatmap_v1.pdf
   └── anc/
       └── (anything supplementary: full appendices if split out)
   ```

2. **Build the `.bbl`.** arXiv compiles `.tex` but not bibtex; ship the pre-built `.bbl`:
   ```bash
   pdflatex beyond_recall && bibtex beyond_recall && pdflatex beyond_recall && pdflatex beyond_recall
   # beyond_recall.bbl now exists; include it in the tarball
   ```

3. **Tarball.**
   ```bash
   tar czf beyond_recall_arxiv.tar.gz beyond_recall_arxiv/
   ```

4. **arXiv pre-flight checks.**
   - All `\includegraphics{}` paths resolve to files in the tarball
   - No absolute paths (`/Users/...`); only relative
   - No `\input{}` or `\include{}` files outside the tarball
   - No reference to packages not in CTAN
   - PDF compiles with arXiv's TeX Live snapshot (currently 2024)

5. **Submit metadata.**
   - Primary subject area: `cs.CL` (Computation and Language) or `cs.AI` (Artificial Intelligence). Likely `cs.CL` primary, `cs.AI` cross-list.
   - Title, abstract, author block. Match `.tex` exactly.
   - License: CC BY 4.0 for the manuscript (matches §8 license declaration).

**Deliverable for phase 4:** `beyond_recall_arxiv.tar.gz` ready for arXiv upload.

---

## Risks and known issues

- **Wide tables.** Table 2.1 has 5 columns including a long "Memory types" column. May need `landscape` orientation for one or two tables; add `\usepackage{lscape}` and wrap with `\begin{landscape}...\end{landscape}`.
- **Long footnotes.** Some footnotes are 200+ words. LaTeX renders them at the bottom of the page they're cited; check page-break behavior.
- **Special characters in BibTeX.** `Bābur`, `Díaz` need UTF-8 BibTeX or hand-encoding. Use `biber` + `biblatex` for cleanest UTF-8 handling.
- **Figure captions.** Long descriptive captions (Figure 4.4.1's caption is ~200 chars) may need `\caption[short]{long}` form to fit in the list of figures.
- **arXiv compile timeout.** arXiv's compile budget is 5 minutes wall-clock. A long-table-heavy paper may push this. Mitigation: pre-compile and ship the PDF as a reference; arXiv compiles its own canonical PDF from the source.

---

## Tooling

- `pandoc` (already installed for markdown handling)
- `texlive-full` (or `mactex` / `miktex` on macOS / Windows)
- `latexmk` for build orchestration
- `biber` if using `biblatex`; `bibtex` for `natbib`
- `arxiv-collector` (`pip install arxiv-collector`) — optional helper that finds all dependencies and bundles them; reduces packaging errors

---

## Sequencing — when to start

**Don't start LaTeX conversion until:**
1. v11.8 markdown is content-locked (no more section reorganization)
2. All figures are final (figure paths committed)
3. References list is final (no more entries added/removed)
4. Cross-LLM review passes are done (last round of edits applied)
5. The current background polish agents have landed and any P0/P1 fixes from them are applied

**At that point:** plan to spend a focused 4-hour block on the four phases above. Don't interleave with other writing; LaTeX conversion is iterative and benefits from continuous attention.

**Owner.** Aarik to direct; assistant to do the mechanical conversion. Aarik reviews compiled PDF at end of each phase.