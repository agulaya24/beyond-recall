"""Find inline text edits Aarik made in `beyond_recall_v11_8_draft_with_figures.docx`
that have not been merged into `beyond_recall_v11_9_draft.md`.

Strategy:
  - Extract paragraphs from the docx body as plain text.
  - Strip markdown formatting from the v11.8 markdown source to plain text per
    paragraph; same for v11.9 markdown.
  - Build a text fingerprint for each paragraph and use difflib to align
    docx-paragraph -> v11.9-paragraph by best fuzzy match within a sliding
    window.
  - Compare paragraph-by-paragraph: where docx differs from v11.9 *and* the
    docx differs from v11.8 markdown (proving Aarik edited the docx after
    pandoc rendering), surface the diff.

Output: a markdown report listing every Aarik-edit paragraph not yet in v11.9.
"""
from __future__ import annotations

import re
import sys
import zipfile
from difflib import SequenceMatcher
from pathlib import Path
from xml.etree import ElementTree as ET

# Force UTF-8 stdout on Windows.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
DOCX = REPO / "docs" / "beyond_recall_v11_8_draft_with_figures.docx"
V11_8_MD = REPO / "docs" / "beyond_recall_v11_8_draft.md"
V11_9_MD = REPO / "docs" / "beyond_recall_v11_9_draft.md"
OUT = REPO / "docs" / "research" / "v11_8_docx_vs_v11_9_md_diff_20260509.md"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def docx_paragraphs(path: Path) -> list[str]:
    """Return body paragraph texts in order, ignoring empty paragraphs."""
    with zipfile.ZipFile(path) as z:
        with z.open("word/document.xml") as f:
            root = ET.parse(f).getroot()
    body = root.find(W + "body")
    out: list[str] = []
    for p in body.findall(W + "p"):
        text = "".join((t.text or "") for t in p.iter(W + "t"))
        text = text.strip()
        if not text:
            continue
        out.append(text)
    return out


def strip_markdown(text: str) -> str:
    """Strip a (chunk of) markdown to plain text approximating what pandoc
    would render. Aggressive but consistent."""
    # Remove footnote definitions entirely.
    if text.lstrip().startswith("[^") and "]:" in text[:60]:
        return ""
    # Drop heading hashes.
    text = re.sub(r"^#{1,6}\s+", "", text)
    # Drop block quotes prefix.
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    # Drop list markers.
    text = re.sub(r"^[\s]*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[\s]*\d+\.\s+", "", text, flags=re.MULTILINE)
    # Inline code, bold, italic.
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    # Footnote markers.
    text = re.sub(r"\[\^[^\]]+\]", "", text)
    # Markdown links / images.
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    # Drop horizontal rules and HTML comments.
    text = re.sub(r"^---\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return text.strip()


def md_paragraphs(path: Path) -> list[str]:
    """Split a markdown file into paragraphs (blank-line separators) and strip
    formatting from each. Excludes table rows, code fences, image embeds,
    horizontal rules. Footnote defs preserved (stripped to plain text)."""
    raw = path.read_text(encoding="utf-8")
    out: list[str] = []
    for chunk in re.split(r"\n\n+", raw):
        chunk = chunk.strip()
        if not chunk:
            continue
        # Strip code fences.
        if chunk.startswith("```"):
            continue
        # Skip pure image embeds.
        if chunk.startswith("![") and "](" in chunk and not chunk.lstrip(">").lstrip().startswith("Subject"):
            continue
        # Skip pure horizontal rules.
        if chunk == "---":
            continue
        # Skip pure tables (every line starts with | and has many |).
        if all(line.lstrip().startswith("|") for line in chunk.splitlines()):
            continue
        plain = strip_markdown(chunk)
        plain = re.sub(r"\s+", " ", plain).strip()
        if plain:
            out.append(plain)
    return out


def normalize(s: str) -> str:
    """Aggressive normalization for pairing: lowercase, collapse whitespace,
    strip surrounding punctuation."""
    s = re.sub(r"\s+", " ", s).strip().lower()
    s = re.sub(r"[‘’“”]", "'", s)
    s = re.sub(r"[–—]", "-", s)
    return s


def find_best_match(target: str, candidates: list[str], start_hint: int = 0,
                    window: int = 80) -> tuple[int, float]:
    """Find best fuzzy match for target in candidates near start_hint.
    Returns (index, ratio). -1 if nothing above 0.55."""
    norm_target = normalize(target)[:300]
    best_idx, best_ratio = -1, 0.0
    lo, hi = max(0, start_hint - 5), min(len(candidates), start_hint + window)
    for i in range(lo, hi):
        norm_c = normalize(candidates[i])[:300]
        ratio = SequenceMatcher(None, norm_target, norm_c).quick_ratio()
        if ratio < 0.55:
            continue
        ratio = SequenceMatcher(None, norm_target, norm_c).ratio()
        if ratio > best_ratio:
            best_idx, best_ratio = i, ratio
    return best_idx, best_ratio


def main() -> int:
    print(f"Loading docx paragraphs from {DOCX.name}")
    docx_paras = docx_paragraphs(DOCX)
    print(f"  {len(docx_paras)} non-empty paragraphs")

    print(f"Loading v11.8 markdown paragraphs (pre-edit baseline)")
    v8_paras = md_paragraphs(V11_8_MD)
    print(f"  {len(v8_paras)} paragraphs")

    print(f"Loading v11.9 markdown paragraphs (current target)")
    v9_paras = md_paragraphs(V11_9_MD)
    print(f"  {len(v9_paras)} paragraphs")

    findings: list[dict] = []
    v8_cursor = 0
    v9_cursor = 0
    for i, dpara in enumerate(docx_paras):
        # Skip paragraphs that are likely figures, tables, or short non-prose.
        if len(dpara) < 60:
            continue

        # Find this docx paragraph in both v8 markdown and v9 markdown.
        v8_idx, v8_ratio = find_best_match(dpara, v8_paras, v8_cursor)
        v9_idx, v9_ratio = find_best_match(dpara, v9_paras, v9_cursor)

        # Advance cursors when matched.
        if v8_idx >= 0:
            v8_cursor = v8_idx
        if v9_idx >= 0:
            v9_cursor = v9_idx

        # If docx matches v8 source closely (>=0.97) and equally well to v9,
        # nothing changed — Aarik did not edit this paragraph.
        if v8_ratio >= 0.97 and v9_ratio >= 0.97:
            continue

        # If docx matches v8 closely but not v9, the v9 markdown may have been
        # changed AFTER the v8 docx was generated (e.g., my own edits) —
        # not Aarik's edit; skip.
        if v8_ratio >= 0.97 and v9_ratio < 0.95:
            # Could be either Aarik's edit OR my v11.9 edit. Surface but mark
            # as "likely-claude-edit" so Aarik can skim past mine.
            findings.append({
                "kind": "v9_diverged_from_v8",
                "docx_para_index": i,
                "docx_text": dpara,
                "v8_index": v8_idx, "v8_ratio": v8_ratio,
                "v9_index": v9_idx, "v9_ratio": v9_ratio,
                "v8_text": v8_paras[v8_idx] if v8_idx >= 0 else "",
                "v9_text": v9_paras[v9_idx] if v9_idx >= 0 else "(no match)",
            })
            continue

        # If docx differs from BOTH v8 and v9, this is most likely an Aarik
        # inline edit on the docx that survives in neither markdown.
        if v8_ratio < 0.97 and v9_ratio < 0.97:
            findings.append({
                "kind": "AARIK_DOCX_EDIT",
                "docx_para_index": i,
                "docx_text": dpara,
                "v8_index": v8_idx, "v8_ratio": v8_ratio,
                "v9_index": v9_idx, "v9_ratio": v9_ratio,
                "v8_text": v8_paras[v8_idx] if v8_idx >= 0 else "(no match)",
                "v9_text": v9_paras[v9_idx] if v9_idx >= 0 else "(no match)",
            })
            continue

    # Write report
    OUT.parent.mkdir(parents=True, exist_ok=True)
    aarik_edits = [f for f in findings if f["kind"] == "AARIK_DOCX_EDIT"]
    other = [f for f in findings if f["kind"] != "AARIK_DOCX_EDIT"]

    lines: list[str] = []
    lines.append(f"# v11.8 docx vs v11.9 markdown diff — {DOCX.name}\n")
    lines.append(f"Aarik-edit paragraphs (docx differs from v11.8 source AND from v11.9 markdown): **{len(aarik_edits)}**\n")
    lines.append(f"Likely Claude/me edits in v11.9 (docx matches v11.8 source but v11.9 differs): **{len(other)}**\n")
    lines.append(f"\n---\n")
    lines.append(f"\n## Aarik docx edits not in v11.9 (priority queue)\n")
    for f in aarik_edits:
        lines.append(f"### docx paragraph #{f['docx_para_index']}")
        lines.append(f"  - v8-md ratio: {f['v8_ratio']:.2f}  v9-md ratio: {f['v9_ratio']:.2f}")
        lines.append(f"\n**v11.8 markdown (pre-edit):**\n")
        lines.append(f"> {f['v8_text'][:500]}{'...' if len(f['v8_text']) > 500 else ''}\n")
        lines.append(f"\n**docx (Aarik's version):**\n")
        lines.append(f"> {f['docx_text'][:500]}{'...' if len(f['docx_text']) > 500 else ''}\n")
        lines.append(f"\n**v11.9 markdown (current):**\n")
        lines.append(f"> {f['v9_text'][:500]}{'...' if len(f['v9_text']) > 500 else ''}\n")
        lines.append("---")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {OUT}")
    print(f"Aarik docx edits not in v11.9: {len(aarik_edits)}")
    print(f"Other v9-vs-v8 differences (likely Claude/me edits): {len(other)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
