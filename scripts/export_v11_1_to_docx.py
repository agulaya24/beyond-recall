"""Export v11 paper draft to .docx with v2/v3 figures and enriched cross-refs.

Adapted from export_v10_to_docx.py:
- Target: docs/beyond_recall_v11_1_draft.md
- v11 retains the same heading anchors used by FIGURE_MAP (4.1, 4.2, 4.3,
  4.4.1, 4.5, 3.7.4, ## 4. Results, ## Appendix D.) so figure injection,
  landscape sectPr wrapping for D.4, and footnote/section-link rewrites
  carry over unchanged.

Changes from export_v9_to_docx.py:
- Target: docs/beyond_recall_v10_1_draft.md (not v9)
- FIGURE_MAP updated for the v9 post-restructure tree:
    * section 4.4 -> 4.4.1 Aggregate Performance Across Systems
    * 4.5 is now Letta Stateful-Agent (was 4.7)
    * 4.6 is now Robustness and Sensitivity (was 4.5)
    * 4.6.1 is now Cross-provider Tier 2 replication (was 4.5.1)
    * 4.8 removed entirely (content moved to 5.5)
- v3 figures swapped in (publication polish, 2026-04-23)
- Figure 9 (cultural baseline) moved to appendix (injected under ## Appendix D)
- Figure 11 (Tier 2) dropped per author decision

New in v10 export (2026-04-23):
- Clickable internal section hyperlinks: every §X.Y cross-reference in body
  prose is rewritten to a markdown link targeting an explicit heading anchor
  injected during preprocessing. Approach uses explicit {#sec-X-Y} anchors
  rather than relying on pandoc's auto-slug (avoids slug-algorithm drift).
- Word footnotes for long parentheticals: parentheticals with > 15 words
  that are not citations, statistics, section-refs, or code-path patterns
  are rewritten to pandoc footnote syntax (Word footnotes in final docx).
- Dry-run mode (--dry-run): report hyperlink count, footnote count,
  and unresolved section references without rewriting the docx.
- Post-export verification: inspects the produced docx for w:hyperlink
  and footnotes.xml entries and prints live counts.

Output: docs/beyond_recall_v11_1_draft.docx
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import pypandoc

REPO = Path(__file__).resolve().parent.parent
MD = REPO / "docs" / "beyond_recall_v11_1_draft.md"
FIGS = REPO / "figures"
OUT_MD = REPO / "docs" / "beyond_recall_v11_1_draft.clean.md"
OUT_DOCX = REPO / "docs" / "beyond_recall_v11_1_draft.docx"

# Each entry: (line-starts-with anchor, png filename, caption).
# Captions are conclusion-led: each leads with what the figure shows, then
# describes the visual elements and load-bearing numbers, then names the
# section (§) the figure supports. v10 rewrite addresses v9 docx comment #21.
FIGURE_MAP = [
    ("### 4.1 The cross-subject gradient", "fig_4_1_gradient_scatter_v3.png",
     "Figure 4.1: How to read this figure. Start at the horizontal red line at Δ = 0. Above the red line means the specification produced a positive change in score versus the no-context baseline; below the red line means a negative change. The x-axis is the no-context baseline score (C5) on the 1-5 rubric. Subjects in the left half of the plot (C5 ≤ 2.0) are the 9 low-baseline subjects (the population of relevance); Subjects in the right half (C5 > 2.0) are the 5 mid-baseline subjects plus Franklin as the high-baseline reference. The y-axis is the per-subject lift the specification produces over baseline (Δ_C4a = C4a − C5). "
     "All 9 low-baseline subjects sit above the red line in the upper-left, all with positive Δ ranging from Babur at +0.25 to Hamerton at +1.51. Franklin sits in the lower-right at C5 = 3.77, Δ = −0.13, the high-baseline anchor where pretraining already covers the subject and the specification adds nothing. "
     "The dotted regression line slopes downward from upper-left to lower-right (slope −0.96, R² = 0.82); read it as: the better the model already knows the subject, the smaller the lift the specification produces. The substantive read is that the specification raises subjects toward a roughly constant operating quality near C4a ≈ 2.46, so the lift is largest where the floor is lowest. (§4.1.) Per-question anchor-crossing distributions are reported separately in the §4.1 transition table."),
    ("### 4.2 Compression: structure vs. raw text", "fig_4_2_compression_v3.png",
     "Figure 4.2: How to read this figure. The x-axis is context size in tokens (log scale, spanning roughly 1K to 400K). The y-axis is the 5-judge primary score on the 1-5 rubric. Each faint trace is one of the 9 low-baseline subjects; the bold curve is the median-across-subjects aggregate. The leftmost point (smallest context) is the no-context baseline (C5, mean 1.52). Moving rightward, the curve passes through the ~7K-token Behavioral Specification alone (C2a, mean 2.23), then the structured fact corpus (C4, mean 2.35), then the full raw corpus (C8, ~80K-400K tokens, mean 2.45), then facts plus spec (C4a, mean 2.45) and corpus plus spec (C9, mean 2.50). "
     "In every condition where the specification is added or served alone, the score sits at or above the no-spec equivalent at the same context size. The curve has a steep initial slope and a long plateau: the first ~7K tokens of structured specification buy +0.68 points of lift over baseline; the next 10x to 50x more tokens of raw corpus buy only an additional +0.22. That shape is the substantive claim: the behaviorally relevant signal in autobiographical text is sparse and compressible, and most of what matters can be packaged into a compact structured document. (§4.2; this figure is the Hamerton-style compression story aggregated across the 9 low-baseline subjects.)"),
    ("### 4.3 Mechanism: Content, Not Format", "fig6_wrong_spec_control.png",
     "Figure 6: How to read this figure. Each cluster on the x-axis is one of the 13 global subjects (Hamerton excluded; he has no wrong-spec run); subjects are sorted by C5 baseline left to right so low-baseline subjects sit on the left and mid-baseline subjects sit on the right. The y-axis is the 5-judge primary score on the 1-5 rubric. Within each subject cluster, four bars show the no-context baseline (C5), the correct specification (C2a, aggregate Δ = +0.35), the random-derangement wrong spec (C2c v2, aggregate Δ = +0.22), and the adversarial maximum-distance wrong spec (C2c v1, aggregate Δ = −0.25). "
     "In every one of the 13 subjects, the wrong specification (under either v1 or v2 pairing) scored lower than the correct specification served on the same subject. Under the adversarial v1 pairing, 8 of the 13 subjects (Augustine, Babur, Cellini, Equiano, Keckley, Rousseau, Seacole, Zitkala-Sa) scored lower than the no-context C5 baseline; serving the wrong spec actively hurt the prediction relative to no context at all. "
     "The correct-vs-adversarial gap of 0.60 points on the 1-5 rubric (more than half a full rubric category) is the content effect: the lift is not coming from the prompt's structure or length, it is coming from the specification matching the actual subject. (§4.3.)"),
    ("### 4.3 Mechanism: Content, Not Format", "fig4_hedging_reduction.png",
     "Figure 4: Adding the Behavioral Specification near-eliminates baseline hedging and refusal on subjects the model does not already know. "
     "Refusal rate (y-axis) across the C5 → C2a → C4a context conditions (x-axis) on the 9 low-baseline subjects, under the narrow starts_refusal classifier (§4.3). "
     "Rate drops from 28.8% at no-context baseline to 1.4% with spec alone to 0.0% with facts plus spec, an order-of-magnitude reduction at each step. The broader-rule classifier (41.2% → 7.9% → 0.4%) shows the same direction."),
    ("### 4.4.1 Aggregate performance across systems", "fig7_memory_systems_v3.png",
     "Figure 7: How to read this figure. The y-axis lists each memory system (Zep, Letta archival, Mem0, Base Layer, Supermemory). The x-axis is the per-system spec delta (Δ_spec = C3 mean − C1 mean) across the 9 low-baseline subjects, where each system's bar runs from the C1 retrieval-only mean rightward (or leftward if negative) to the C3 retrieval-plus-spec mean. Positive-subject counts (subjects with Δ > 0) sit on each system label. "
     "Zep (Δ +0.17, 9/9 subjects positive) and Letta archival (Δ +0.17, 8/9) are the cleanest gains; Mem0 (Δ +0.10, 6/9) and Base Layer's local retrieval substrate (Δ +0.08, 6/9) are smaller but positive; Supermemory aggregates near zero (Δ −0.01, 5/9) because per-question swings cancel (median improvement +1.45, median worsening −1.41; treated in §4.4.2). "
     "At the per-question level, the share of low-baseline questions that crossed at least one rubric integer anchor upward when the specification was added on top of retrieval (controlled C1→C3 configuration, n = 351 paired questions per system across 9 subjects, all 9/9 subjects had at least one upward crossing per system): Base Layer 29.0%, Zep 27.9%, Letta 26.9%, Mem0 23.4%, Supermemory 20.2%. The aggregate Δ and the anchor-crossing rate agree on rank ordering: where the spec helps, it helps both at the subject mean and at the per-question category level. (§4.4.1.)"),
    ("### 4.4.1 Aggregate performance across systems", "fig3_retrieval_disagreement.png",
     "Figure 3: All-three-disagree rate across Mem0, Letta, and Supermemory at top-k = 1, 3, 5, and 10 in the controlled configuration where every system received the same pre-extracted fact pool. 93% of the 515 questions produce a fully disjoint top-1 across the three systems; 53% remain fully disjoint at top-10. (§4.4.1.)"),
    ("### 4.5 Exploratory case study: Letta stateful-agent", "fig10_letta_scaling.png",
     "Figure 10: Letta's self-editing memory block grows roughly linearly with source corpus size and hits an API ingestion ceiling at large scale, while Base Layer's compose step stays bounded. "
     "Letta block size in characters (left panel) and verbatim-sentence duplication share at the largest subject (right panel) as source corpus grows from Hamerton (25K words → 22K-char block) to Ebers (48K words → 68K-char block) to Babur (223K words → 335K-char block at the ~333K Letta API ceiling), with the Base Layer specification footprint (~34-40K characters across all three) overlaid for reference (§4.5). "
     "At the ceiling, 25.4% of the Babur block is verbatim-duplicated sentences (vs. 0% on Hamerton and Ebers), evidence the agent rewrites previously-written content rather than compressing it."),
    ("### 3.7.4 Inter-judge agreement", "fig8_judge_agreement.png",
     "Figure 8: Seven LLM judges across three providers converge on the direction of the specification effect, even where they disagree on absolute magnitude. "
     "Pairwise Spearman ρ heatmaps for the 5-judge primary panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4; left) and the 7-judge sensitivity panel adding Gemini Flash and Gemini Pro (right), colorblind-safe viridis colormap over ρ = 0.85 to 1.00 (§3.7.4). "
     "Pairwise ρ ranges 0.86 to 0.93 across all 21 judge pairs; Krippendorff α (ordinal) is 0.659 on the 5-judge primary (just below the 0.667 substantial-reliability threshold) and 0.535 on the 7-judge panel, where the Gemini judges' systematic +1-point inflation widens the absolute-magnitude disagreement without disturbing the rank ordering."),
    ("## Appendix D.", "fig9_cultural_baseline.png",
     "Figure D.1: Baseline pretraining coverage clusters by cultural region rather than by subject \"importance,\" motivating the C5 ≤ 2.0 low-baseline slice as the population of relevance. "
     "C5 baseline score (x-axis) per subject, sorted low to high, with color and hatching encoding whether the specification improved that subject (§3.2.1, §4.1). "
     "9 of 14 main-study subjects fall in the low-baseline band (Sunity Devee, Ebers, Hamerton, Fukuzawa, Bernal Diaz, Babur, Seacole, Keckley, Yung Wing); 5 fall in the mid-baseline band (Cellini, Zitkala-Sa, Rousseau, Augustine, Equiano); Franklin alone (3.77) sits in the high-baseline band as the known-figure control."),
    ("## 4. Results", "fig5_condition_effects_v3.png",
     "Figure 5: How to read this figure. The x-axis lays out four context conditions in order: behavioral specification alone (C2a), facts alone (C4), raw corpus alone (C8), and facts plus spec (C4a). The y-axis is the share of the 351 paired low-baseline questions (9 subjects times 39 questions) that improved, tied, or worsened relative to the no-context C5 baseline; each bar is a stacked outcome distribution. "
     "Reading from the left: the specification alone (C2a) improved 70.9% of questions; facts alone (C4) improved 72.9%; the raw corpus alone (C8) improved 78.3%; stacking the specification on top of the raw facts (C4a) improved 78.6%, the highest rate of any single-or-stacked condition. Stacking the spec on top of the corpus (C9, in the next figure) reaches the same plateau. "
     "The specification alone (C2a, ~7K tokens) matches the raw corpus's improvement rate (C8, 80K-400K tokens) within 8 percentage points at roughly an order of magnitude less context, and stacking the spec onto either fact representation produces the highest scores. The specification is providing a more aligned line of reasoning than what fact retrieval alone produces. "
     "Median Δ when improved = +1.00 rubric points (a full anchor-band move); median Δ when worsened = −0.40. The metric guards against tiny-gain inflation. (§4.2.1.)"),
]


LANDSCAPE_SECTPR = (
    '```{=openxml}\n'
    '<w:p><w:pPr><w:sectPr>'
    '<w:pgSz w:w="15840" w:h="12240" w:orient="landscape"/>'
    '<w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" '
    'w:header="720" w:footer="720" w:gutter="0"/>'
    '<w:cols w:space="720"/>'
    '<w:docGrid w:linePitch="360"/>'
    '</w:sectPr></w:pPr></w:p>\n'
    '```'
)

PORTRAIT_SECTPR = (
    '```{=openxml}\n'
    '<w:p><w:pPr><w:sectPr>'
    '<w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="720" w:footer="720" w:gutter="0"/>'
    '<w:cols w:space="720"/>'
    '<w:docGrid w:linePitch="360"/>'
    '</w:sectPr></w:pPr></w:p>\n'
    '```'
)

# Sections to render in landscape orientation. Each entry is a (start_header,
# end_header) pair. The section starting at start_header renders landscape; the
# paragraph at end_header reverts to portrait. Matching is exact-prefix.
LANDSCAPE_SECTIONS = [
    ("### D.4 Per-judge score matrices", "### D.5 "),
]


# =========================================================================
# Preprocessing helpers: heading anchors, section-ref hyperlinks, footnotes.
# =========================================================================

# Matches body section numbers at the start of a heading after the leading
# "##" / "###" / "####". Supports numeric (1, 1.2, 1.2.3) and appendix (A,
# A.1, A.1.2) headings. Appendix letters are A-E.
HEADING_LINE_RE = re.compile(
    r"^(?P<hashes>#{2,4})\s+(?P<num>(?:[A-E]|\d+)(?:\.\d+){0,3})\s+(?P<title>.+?)\s*$"
)

# Matches every in-prose section reference like
#    §1.3, §4.4.1, §C.2
# Requires at least one `.digit` so a bare `§` or `§X` without a sub-part is
# not matched (those are section symbols, not cross-refs). Appendix letters
# A-E are treated as numbered sections via explicit anchor injection below.
SECTION_REF_RE = re.compile(r"§(?P<ref>(?:[A-E]|\d+)(?:\.\d+)+)")

# Finds a single parenthetical at the outermost level. Because we use a
# negated character class, nested parens fall out: any `(...)` containing a
# further `(` is skipped. That is acceptable for the paper, which has no
# nested parens at scale.
PAREN_RE = re.compile(r"\(([^()\n]+)\)")


def section_anchor_id(section_num: str) -> str:
    """Canonical anchor id for a numeric/appendix section reference."""
    return "sec-" + section_num.replace(".", "-").lower()


def build_heading_anchor_map(lines: list[str]) -> dict[str, str]:
    """Scan the markdown for numbered headings and return section-ref -> anchor.

    The map keys are the section numbers as they appear in prose (e.g.
    "4.4.1", "C.2"), without the leading section symbol. Values are
    anchor ids of the form "sec-4-4-1" or "sec-c-2".
    """
    anchors: dict[str, str] = {}
    in_code = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = HEADING_LINE_RE.match(line)
        if not match:
            continue
        num = match.group("num")
        anchors[num] = section_anchor_id(num)
    return anchors


def inject_heading_anchors(lines: list[str], anchors: dict[str, str]) -> list[str]:
    """Append `{#sec-x-y}` attribute lists to every numbered heading.

    Pandoc's `header_attributes` extension is on by default for GFM/markdown
    inputs. Injecting an explicit id means we do not depend on pandoc's
    auto-slug algorithm, which varies across versions and quietly preserves
    characters like periods.
    """
    out: list[str] = []
    in_code = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        match = HEADING_LINE_RE.match(line)
        if not match:
            out.append(line)
            continue
        num = match.group("num")
        if num not in anchors:
            out.append(line)
            continue
        # Skip if the heading already carries an id attribute.
        if re.search(r"\{#[^}]+\}\s*$", line):
            out.append(line)
            continue
        anchor = anchors[num]
        out.append(f"{line.rstrip()} {{#{anchor}}}")
    return out


def iter_outside_code_and_links(line: str):
    """Yield (text, replaceable) chunks so callers can rewrite only prose.

    Chunks marked replaceable=False include inline code spans (backticks),
    markdown image/link payloads, and HTML tags. Everything else is
    replaceable.
    """
    # Split on inline code spans, markdown images, and markdown links.
    # Order matters: images (`![...](...)`) must be peeled before plain
    # links (`[...](...)`) so the `!` prefix is preserved.
    # We build one composite regex that captures any of these at their
    # natural boundaries.
    pattern = re.compile(
        r"(`[^`\n]*`"          # inline code
        r"|!\[[^\]]*\]\([^)]*\)"  # markdown image
        r"|\[[^\]]*\]\([^)]*\)"   # markdown link
        r"|<[^>]+>"               # html tag
        r")"
    )
    pos = 0
    for match in pattern.finditer(line):
        if match.start() > pos:
            yield line[pos:match.start()], True
        yield match.group(0), False
        pos = match.end()
    if pos < len(line):
        yield line[pos:], True


def rewrite_section_refs(
    lines: list[str],
    anchors: dict[str, str],
) -> tuple[list[str], int, set[str]]:
    """Rewrite §X.Y occurrences in prose to markdown links.

    Returns (new_lines, n_links_created, unresolved_refs).
    """
    out: list[str] = []
    n_links = 0
    unresolved: set[str] = set()
    in_code = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        # Skip heading lines: we do not want hashed anchors inside headings.
        if HEADING_LINE_RE.match(line):
            out.append(line)
            continue
        # Skip table rows: linking inside tables tends to break pandoc's
        # column sizing, and the refs in tables are already concise.
        if stripped.startswith("|"):
            out.append(line)
            continue
        # Skip image-only lines.
        if stripped.startswith("!["):
            out.append(line)
            continue

        rebuilt: list[str] = []
        for chunk, replaceable in iter_outside_code_and_links(line):
            if not replaceable:
                rebuilt.append(chunk)
                continue

            def _sub(match: re.Match) -> str:
                nonlocal n_links
                ref = match.group("ref")
                if ref in anchors:
                    n_links += 1
                    return f"[§{ref}](#{anchors[ref]})"
                unresolved.add(ref)
                return match.group(0)

            rebuilt.append(SECTION_REF_RE.sub(_sub, chunk))
        out.append("".join(rebuilt))
    return out, n_links, unresolved


# Word-boundary markers that indicate a parenthetical is a citation,
# statistic, code reference, or short-form tag that should stay inline.
_FOOTNOTE_EXCLUDE_SUBSTRINGS = (
    "arXiv:",
    " et al.",
    "et al.,",
    "et seq.",
    "Fig.",
    "Fig ",
    "Figure ",
    "Table ",
    "p. ",
    "pp. ",
    "R²",
    "R^2",
    "Δ",        # uppercase delta
    "δ",        # lowercase delta
    "e.g.,",
    "i.e.,",
    "cf.",
    ".py",
    ".md",
    ".json",
    ".ipynb",
    "scripts/",
    "docs/",
    "results/",
    "figures/",
    "data/",
    "memory-study-repo/",
)

_FOOTNOTE_EXCLUDE_PATTERNS = (
    re.compile(r"^\s*\d{4}(?:-\d{2}-\d{2})?\s*$"),    # date-only
    re.compile(r"\b\d{4}\b[,;\s]"),                  # 4-digit year
    re.compile(r"\br\s*=\s*[-−]?\d"),             # r = value
    re.compile(r"\bp\s*[<=]\s*\d"),                     # p < / p = value
    re.compile(r"\bn\s*=\s*\d"),                        # n = value
    re.compile(r"\bN\s*=\s*\d"),                        # N = value
    re.compile(r"\bmean\s+[A-Za-z0-9]+\s*="),         # mean X = value
    re.compile(r"\b[a-zA-Z]+\s*=\s*[-−]?\d"),     # generic var=num
    re.compile(r"\bC\d+[a-z]?\b"),                       # condition codes (C5, C2a)
    re.compile(r"^[\s-]*[-−]?\d+\.\d+"),         # leads with stat like -0.05
    re.compile(r"\$[^$]*\$"),                              # inline LaTeX
    re.compile(r"§"),                                       # already a section-ref
    re.compile(r"\\\\"),                                   # escaped LaTeX
)

# Word count gate.
_FOOTNOTE_MIN_WORDS = 16  # > 15 words in the task spec.


def _paren_content_is_excluded(content: str) -> bool:
    for marker in _FOOTNOTE_EXCLUDE_SUBSTRINGS:
        if marker in content:
            return True
    for pat in _FOOTNOTE_EXCLUDE_PATTERNS:
        if pat.search(content):
            return True
    return False


def rewrite_footnotes(
    lines: list[str],
) -> tuple[list[str], list[str], list[str]]:
    """Rewrite qualifying parentheticals to pandoc footnotes.

    Returns (new_lines, footnote_defs, converted_previews).
    - footnote_defs: lines of the form `[^fn12]: body...` to append.
    - converted_previews: first 120 chars of each converted parenthetical,
      for dry-run inspection.
    """
    out: list[str] = []
    footnote_defs: list[str] = []
    previews: list[str] = []
    in_code = False
    counter = 0

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        # Heading, table, and figure-caption lines are left alone.
        if HEADING_LINE_RE.match(line):
            out.append(line)
            continue
        if stripped.startswith("|"):
            out.append(line)
            continue
        if stripped.startswith("!["):
            out.append(line)
            continue
        # Paragraphs beginning with a single `*` italic (e.g. the figure
        # captions we inject) tend to be short and self-contained; skip.
        if stripped.startswith("*") and stripped.endswith("*") and len(stripped) < 300:
            out.append(line)
            continue

        rebuilt_parts: list[str] = []
        for chunk, replaceable in iter_outside_code_and_links(line):
            if not replaceable:
                rebuilt_parts.append(chunk)
                continue
            new_chunk_parts: list[str] = []
            pos = 0
            for match in PAREN_RE.finditer(chunk):
                new_chunk_parts.append(chunk[pos:match.start()])
                content = match.group(1).strip()
                word_count = len(content.split())
                if word_count < _FOOTNOTE_MIN_WORDS:
                    new_chunk_parts.append(match.group(0))
                elif _paren_content_is_excluded(content):
                    new_chunk_parts.append(match.group(0))
                else:
                    counter += 1
                    marker = f"[^fn{counter}]"
                    new_chunk_parts.append(marker)
                    footnote_defs.append(f"[^fn{counter}]: {content}")
                    previews.append(content[:160])
                pos = match.end()
            new_chunk_parts.append(chunk[pos:])
            rebuilt_parts.append("".join(new_chunk_parts))
        out.append("".join(rebuilt_parts))

    return out, footnote_defs, previews


# =========================================================================
# Main markdown build pipeline.
# =========================================================================


def build_clean_markdown() -> tuple[str, set, dict]:
    text = MD.read_text(encoding="utf-8")
    # Rewrite inline relative figure refs so pandoc can resolve them.
    abs_figs = FIGS.resolve().as_posix()
    text = text.replace("../figures/", abs_figs + "/")
    # Swap Fig 4.2.1 inline reference to the v3 polished rendering without
    # touching the v9 paper body source.
    text = text.replace(
        "fig_4_2_1_question_improvement_rates.png",
        "fig_4_2_1_question_improvement_rates_v3.png",
    )
    lines = text.split("\n")

    # Drop leading blank lines.
    while lines and lines[0].strip() == "":
        lines = lines[1:]

    # Pass 1: build anchor map from headings.
    anchors = build_heading_anchor_map(lines)

    # Pass 2: inject {#sec-...} attribute lists on numbered headings.
    lines = inject_heading_anchors(lines, anchors)

    # Pass 3: rewrite section references to clickable markdown links.
    lines, n_section_links, unresolved_refs = rewrite_section_refs(lines, anchors)

    # Pass 4: rewrite qualifying parentheticals to pandoc footnotes.
    lines, footnote_defs, footnote_previews = rewrite_footnotes(lines)

    # Append footnote definitions at the very end of the document. Pandoc
    # accepts footnote defs anywhere, but keeping them clustered makes the
    # intermediate markdown easier to audit.
    if footnote_defs:
        if lines and lines[-1].strip() != "":
            lines.append("")
        for fdef in footnote_defs:
            lines.append(fdef)
            lines.append("")

    # Pass 5: insert figures at mapped anchors. Heading prefix match is
    # tolerant of the appended `{#sec-x-y}` attribute because startswith
    # still holds.
    out_lines: list[str] = []
    used: set = set()
    i = 0
    while i < len(lines):
        line = lines[i]
        out_lines.append(line)
        matches: list = []
        for prefix, png, caption in FIGURE_MAP:
            key = (prefix, png)
            if key in used:
                continue
            if line.startswith(prefix):
                matches.append((prefix, png, caption))
        if matches:
            for prefix, png, caption in matches:
                used.add((prefix, png))
            j = i + 1
            while j < len(lines) and lines[j].strip() != "":
                out_lines.append(lines[j])
                j += 1
            out_lines.append("")
            for prefix, png, caption in matches:
                img_path = (FIGS / png).resolve().as_posix()
                out_lines.append(f"![{caption}]({img_path})")
                out_lines.append("")
                out_lines.append(f"*{caption}*")
                out_lines.append("")
            i = j
        i += 1

    # Pass 6: inject landscape section-break paragraphs around the
    # LANDSCAPE_SECTIONS ranges.
    final_lines: list[str] = []
    k = 0
    injected: list[str] = []
    landscape_pairs = list(LANDSCAPE_SECTIONS)
    while k < len(out_lines):
        line = out_lines[k]
        start_match = next(
            (pair for pair in landscape_pairs if line.startswith(pair[0])), None
        )
        if start_match:
            final_lines.append("")
            final_lines.append(PORTRAIT_SECTPR)
            final_lines.append("")
            final_lines.append(line)
            k += 1
            end_prefix = start_match[1]
            while k < len(out_lines) and not out_lines[k].startswith(end_prefix):
                final_lines.append(out_lines[k])
                k += 1
            final_lines.append("")
            final_lines.append(LANDSCAPE_SECTPR)
            final_lines.append("")
            injected.append(start_match[0])
            continue
        final_lines.append(line)
        k += 1

    stats = {
        "section_links": n_section_links,
        "unresolved_refs": sorted(unresolved_refs),
        "footnote_count": len(footnote_defs),
        "footnote_previews": footnote_previews,
        "anchors_built": len(anchors),
        "landscape_wrappers": injected,
    }
    return "\n".join(final_lines), used, stats


# =========================================================================
# Post-export verification helpers.
# =========================================================================


W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def count_docx_hyperlinks(docx_path: Path) -> int:
    """Count internal-anchor hyperlinks in the produced docx."""
    with zipfile.ZipFile(docx_path) as z:
        doc_xml = z.read("word/document.xml")
    root = ET.fromstring(doc_xml)
    ns = W_NS + "}"
    total = 0
    for el in root.iter(ns + "hyperlink"):
        # Internal anchors carry a w:anchor attribute.
        anchor = el.get(W_NS.lstrip("{") + "}anchor") or el.get("w:anchor")
        # ET strips namespace on attributes: try the unprefixed key too.
        if anchor is None:
            # ET does not prefix attribute names in iter; try all keys.
            for k in el.keys():
                if k.endswith("anchor"):
                    anchor = el.get(k)
                    break
        if anchor:
            total += 1
    return total


def count_docx_footnotes(docx_path: Path) -> int:
    """Count real footnotes in the produced docx (excluding boilerplate)."""
    with zipfile.ZipFile(docx_path) as z:
        if "word/footnotes.xml" not in z.namelist():
            return 0
        xml = z.read("word/footnotes.xml")
    root = ET.fromstring(xml)
    ns = W_NS + "}"
    total = 0
    for fn in root.iter(ns + "footnote"):
        # Skip the two default Word boilerplate footnotes: separator and
        # continuationSeparator. They carry w:type attributes.
        ftype = None
        for k in fn.keys():
            if k.endswith("type"):
                ftype = fn.get(k)
                break
        if ftype in ("separator", "continuationSeparator"):
            continue
        total += 1
    return total


# =========================================================================
# CLI entry point.
# =========================================================================


def _emit_stats(stats: dict, used: set, unmatched: list) -> None:
    print(f"Anchors indexed: {stats['anchors_built']}")
    print(f"Section hyperlinks created (markdown): {stats['section_links']}")
    print(f"Footnotes created: {stats['footnote_count']}")
    if stats["unresolved_refs"]:
        print(f"Unresolved section refs ({len(stats['unresolved_refs'])}):")
        for ref in stats["unresolved_refs"]:
            print(f"  - §{ref}")
    else:
        print("Unresolved section refs: 0")
    if stats["landscape_wrappers"]:
        for start in stats["landscape_wrappers"]:
            print(f"  + landscape wrapper around: {start[:70]}")
    print(f"Figures inserted: {len(used)} / {len(FIGURE_MAP)}")
    for prefix, png in sorted(used):
        print(f"  + {png}  @  {prefix[:70]}")
    if unmatched:
        print("Unmatched figure anchors (no figure inserted):")
        for prefix, png in unmatched:
            print(f"  - {png}  @  {prefix[:70]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build cleaned markdown and report counts without invoking pandoc.",
    )
    parser.add_argument(
        "--show-footnote-previews",
        action="store_true",
        help="Print first 160 chars of every parenthetical converted to a footnote.",
    )
    args = parser.parse_args()

    cleaned, used, stats = build_clean_markdown()
    OUT_MD.write_text(cleaned, encoding="utf-8")
    print(f"Intermediate markdown: {OUT_MD}")

    unmatched = [(p, f) for (p, f, _) in FIGURE_MAP if (p, f) not in used]
    _emit_stats(stats, used, unmatched)

    if args.show_footnote_previews:
        print("\nFootnote previews:")
        for idx, preview in enumerate(stats["footnote_previews"], 1):
            safe = preview.encode("ascii", "backslashreplace").decode("ascii")
            print(f"  [fn{idx}] {safe}")

    if args.dry_run:
        print("\n(dry-run) skipping pandoc conversion.")
        return 0

    if OUT_DOCX.exists():
        OUT_DOCX.unlink()
        print(f"Removed prior docx: {OUT_DOCX}")

    reference_docx = REPO / "docs" / "_reference_arxiv_11pt.docx"
    pypandoc.convert_file(
        str(OUT_MD),
        "docx",
        outputfile=str(OUT_DOCX),
        extra_args=[
            "--standalone",
            "--toc",
            "--toc-depth=3",
            "--resource-path=" + str(REPO),
            "--reference-doc=" + str(reference_docx),
        ],
    )
    size_kb = OUT_DOCX.stat().st_size / 1024
    print(f"Wrote: {OUT_DOCX}  ({size_kb:.0f} KB)")

    # Post-export verification.
    try:
        hyperlink_count = count_docx_hyperlinks(OUT_DOCX)
        footnote_count = count_docx_footnotes(OUT_DOCX)
        print(f"Verification: w:hyperlink elements with internal anchor = {hyperlink_count}")
        print(f"Verification: footnotes.xml real entries = {footnote_count}")
    except Exception as exc:
        print(f"Verification failed: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
