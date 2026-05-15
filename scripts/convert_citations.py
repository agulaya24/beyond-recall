#!/usr/bin/env python3
"""Convert inline (Author et al., YYYY, arXiv:NNNN.NNNNN) citations in
beyond_recall_body.tex to natbib \\citep{key} / \\citet{key} calls.

Strategy: anchor on arXiv ID + author last name to disambiguate. Run a series
of regex replacements that strip the verbose inline form and substitute the
\\citep{key} or \\citet{key} call. Also collapses the §9 References list into
a single \\bibliography{} placeholder so the .bib drives output.

Each rule is a (pattern, replacement) pair. Patterns target specific
contexts so the script is idempotent (running twice yields no change).
"""
import re
from pathlib import Path

BODY = Path(__file__).resolve().parents[1] / "build" / "beyond_recall_body.tex"

# Map arXiv ID -> bibtex key. This is the source of truth.
ARXIV_TO_KEY = {
    "1503.02531": "hinton2015distilling",
    "2212.09251": "perez2022discovering",
    "2306.05685": "zheng2023judging",
    "2310.08560": "packer2023memgpt",
    "2310.13548": "sharma2023sycophancy",
    "2402.17753": "maharana2024locomo",
    "2404.18796": "verga2024juries",
    "2407.18416": "samuel2025personagym",
    "2410.10813": "wu2025longmemeval",
    "2501.13956": "rasmussen2025zep",
    "2504.14225": "jiang2025knowme",
    "2504.19413": "chhikara2025mem0",
    "2505.17479": "toubia2025twin2k",
    "2507.21509": "chen2025personavectors",
    "2509.12517": "jain2025sycophancy",
    "2601.10387": "lu2026assistantaxis",
    "2603.26680": "xiao2026alpsbench",
}

# Replacements applied in order. Each is (description, regex_pattern, replacement_func or string).
# The body is LaTeX, so escape carefully. We use re.MULTILINE and DOTALL where needed.

text = BODY.read_text(encoding="utf-8")

# --- Replace verbose Author-form inline cites that include an arXiv ID. ---
# Patterns we expect (post-pandoc LaTeX):
#   (Maharana et al., ACL 2024, arXiv:2402.17753)
#   (Wu et al., ICLR 2025, arXiv:2410.10813)
#   (Toubia et al., 2025, arXiv:2505.17479)
#   Chen, Arditi, Sleight, Evans, Lindsey; arXiv:2507.21509
#   (Chhikara et al., arXiv:2504.19413)
#   Rasmussen et al., arXiv:2501.13956
#   Packer et al., 2023, arXiv:2310.08560
#   Jiang et al. (COLM 2025, arXiv:2504.14225)
#   Jain et al. (2025, arXiv:2509.12517)
#   Lu et al. (2026, arXiv:2601.10387)
#   Samuel et al., Findings of EMNLP 2025, arXiv:2407.18416
#   Xiao et al., 2026, arXiv:2603.26680
#   Zheng et al., 2023, NeurIPS Datasets and Benchmarks Track, arXiv:2306.05685
#
# We normalize them all to \citep{key} where they appear in parentheses, and
# \citet{key}~(YYYY) where they're inline-named. The replacement leaves prose
# author mentions in narrative spots (e.g. "Hinton et al. (2015) showed...")
# but converts the arXiv-bearing parenthetical to a \citep.

# Pattern A: "(Author et al., venue YYYY, arXiv:NNNN.NNNNN)" or
#            "(Author et al., YYYY, arXiv:NNNN.NNNNN)"
def repl_arxiv_paren(m):
    arxiv = m.group("arxiv")
    key = ARXIV_TO_KEY.get(arxiv)
    if not key:
        return m.group(0)
    return f"\\citep{{{key}}}"

# Match (..., arXiv:NNNN.NNNNN) — inside parens with arxiv id at end.
text = re.sub(
    r"\((?:[^()]*?)arXiv:(?P<arxiv>\d{4}\.\d{4,5})\)",
    repl_arxiv_paren,
    text,
)

# Pattern B: bare ", arXiv:NNNN.NNNNN" in mid-sentence (no closing paren). We
# leave the prose author mention intact and replace the arXiv tail with
# the \citep.
def repl_arxiv_tail(m):
    arxiv = m.group("arxiv")
    key = ARXIV_TO_KEY.get(arxiv)
    if not key:
        return m.group(0)
    return f"~\\citep{{{key}}}"

# This catches strings like "Rasmussen et al., arXiv:2501.13956." — replace the
# ", arXiv:..." tail with " \citep{key}". Be conservative: require leading ", ".
text = re.sub(
    r",\s*arXiv:(?P<arxiv>\d{4}\.\d{4,5})",
    repl_arxiv_tail,
    text,
)

# Pattern C: any remaining "arXiv:NNNN.NNNNN" stub is a leftover; substitute as
# a parenthetical \citep so the trail isn't visible.
def repl_arxiv_bare(m):
    arxiv = m.group("arxiv")
    key = ARXIV_TO_KEY.get(arxiv)
    if not key:
        return m.group(0)
    return f"(\\citealp{{{key}}})"

text = re.sub(
    r"arXiv:(?P<arxiv>\d{4}\.\d{4,5})",
    repl_arxiv_bare,
    text,
)

# Pattern D: prose author-year cites that don't carry an arXiv ID locally
# (the arXiv ID is downstream). e.g. "Hinton et al. (2015)", "Bartlett (1932)",
# "Verga et al. 2024", "Sharma et al. 2023", "Perez et al. 2022".
prose_cites = [
    (r"\bHinton et al\.~?\(2015\)", r"\\citet{hinton2015distilling}"),
    (r"\bBartlett \(1932\)", r"\\citet{bartlett1932}"),
    (r"\bSharma et al\.~?2023\b", r"\\citet{sharma2023sycophancy}"),
    (r"\bPerez et al\.~?2022\b", r"\\citet{perez2022discovering}"),
    (r"\bVerga et al\.~?2024\b(?! and follow)", r"\\citet{verga2024juries}"),
    (r"\bVerga et al\.~?2024 and follow-ons", r"\\citet{verga2024juries} and follow-ons"),
    (r"\bZheng et al\.~?\(2023\)", r"\\citet{zheng2023judging}"),
    (r"\(Jain et al\.~?2025\)", r"\\citep{jain2025sycophancy}"),
]
for pat, repl in prose_cites:
    text = re.sub(pat, repl, text)

# Pattern E: clean up the doubled-author renderings introduced by Pattern B
# (\citep tail glued onto a \textbf{Author et al.~...}). Convert
#   \textbf{Author et al.~\citep{key}}
# to
#   \textbf{\citet{key}}
# which renders as bold "Author et al. (YYYY)".
text = re.sub(
    r"\\textbf\{[A-Z][a-zA-Z]+ et al\.~?\\citep\{([a-zA-Z0-9]+)\}\}",
    r"\\textbf{\\citet{\1}}",
    text,
)
# Also: \textbf{Author et al. (YYYY)} \citep{key} -> \textbf{\citet{key}}
# Already handled by Pattern D for the specific named cases; for any
# remaining "\textbf{Author et al.~(YYYY)} \citep{key}" patterns:
text = re.sub(
    r"\\textbf\{([A-Z][a-zA-Z]+ et al\.~?\(\d{4}\))\}\s*\\citep\{([a-zA-Z0-9]+)\}",
    r"\\textbf{\\citet{\2}}",
    text,
)

# Replace §9 References prose block with a \bibliography{} call. Locate the
# §9 hypertarget and the next \hypertarget after it; replace the body in
# between with the bibliography directive. The §9 References must appear
# before appendices, so the bib lives where the prose used to.
ref_pat = re.compile(
    r"(\\hypertarget\{references\}\{%\s*\n\\section\{[^}]*References\}[^\n]*\n.*?)"
    r"(?=\\hypertarget\{)",
    re.DOTALL,
)

# Replacement keeps the §9 hypertarget+section header and substitutes the
# prose entries with the bibliography directive.
def repl_refs(m):
    block = m.group(1)
    # Keep only the \hypertarget...\section{...References} header line.
    header = re.match(
        r"(\\hypertarget\{references\}\{%\s*\n\\section\{[^}]*\}\\label\{references\}\})",
        block,
    )
    if not header:
        return block  # Bail safely if structure differs.
    return (
        header.group(1)
        + "\n\n"
        + "\\bibliographystyle{plainnat}\n"
        + "\\bibliography{beyond_recall}\n\n"
    )

new_text, n_refs = ref_pat.subn(repl_refs, text)
if n_refs == 1:
    text = new_text
    print(f"  §9 References block replaced with \\bibliography{{beyond_recall}}.")
elif n_refs == 0:
    print("  WARNING: §9 References block not located. Bibliography may not render.")
else:
    print(f"  Multiple §9 hits ({n_refs}); aborting refs replacement.")

BODY.write_text(text, encoding="utf-8")
print(f"Citation conversion done. {len(ARXIV_TO_KEY)} arXiv keys + {len(prose_cites)} prose patterns processed.")
