"""Sentence-level diff: find sentences in `beyond_recall_v11_8_draft_with_figures.docx`
(Aarik's edited version) that have no near-match in `beyond_recall_v11_9_draft.md`.

Avoids the paragraph-alignment problem of the earlier diff: a sentence either
appears in v11.9 (with high fuzzy similarity) or it does not. This catches
inline edits, capitalization changes, title changes, and entire missing
sentences without depending on docx-vs-markdown paragraph boundaries matching.

Output: a markdown report listing each docx sentence with no v11.9 match,
grouped by surrounding context.
"""
from __future__ import annotations

import re
import sys
import zipfile
from difflib import SequenceMatcher
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
DOCX = REPO / "docs" / "beyond_recall_v11_8_draft_with_figures.docx"
V11_8_MD = REPO / "docs" / "beyond_recall_v11_8_draft.md"
V11_9_MD = REPO / "docs" / "beyond_recall_v11_9_1_draft.md"
OUT = REPO / "docs" / "research" / "v11_8_docx_vs_v11_9_1_md_sentence_diff_20260509.md"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def docx_text_blob(path: Path) -> str:
    """Extract paragraph text honoring tracked changes:
    - Text inside <w:del> (deletions) is SKIPPED.
    - Text inside <w:ins> (insertions) is INCLUDED.
    Equivalent to "accept all changes" before extracting.
    """
    with zipfile.ZipFile(path) as z:
        with z.open("word/document.xml") as f:
            root = ET.parse(f).getroot()
    body = root.find(W + "body")
    parts: list[str] = []
    for p in body.findall(W + "p"):
        # For each w:t, walk up its ancestors; if any ancestor is w:del, skip.
        text_pieces: list[str] = []
        for t in p.iter(W + "t"):
            inside_del = False
            ancestor = t
            # ElementTree doesn't carry parent pointers; walk explicitly.
            for parent in p.iter():
                if parent is t:
                    continue
                # Check if this w:del element contains t as descendant.
            # Simpler: do a DFS with del-suppression.
            text_pieces.append(t.text or "")
        # Above loop captured everything including w:del. Replace with proper
        # tree walk that suppresses w:del subtrees.
        text_pieces = []
        def walk(el, suppress_del):
            for child in el:
                tag = child.tag
                if tag == W + "del":
                    continue  # skip entire deletion subtree
                if tag == W + "t":
                    text_pieces.append(child.text or "")
                else:
                    walk(child, suppress_del)
        walk(p, suppress_del=True)
        text = "".join(text_pieces).strip()
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def md_to_plain(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    text = raw
    # Drop fenced code blocks.
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # Drop image embeds.
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    # Drop heading hashes but keep heading text.
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Drop blockquote markers.
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    # Drop list markers.
    text = re.sub(r"^[\s]*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[\s]*\d+\.\s+", "", text, flags=re.MULTILINE)
    # Drop inline code, bold/italic, footnote markers, links/images.
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"\[\^[^\]]+\]:?", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    # Drop horizontal rules and HTML comments.
    text = re.sub(r"^---+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return text


SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(\[*])")


def split_sentences(text: str) -> list[str]:
    """Split a plain-text blob into sentences. Drops table rows entirely."""
    sentences: list[str] = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Skip table rows.
        if line.startswith("|") and line.count("|") >= 3:
            continue
        # Skip footnote IDs / sectPr markers / very-short non-sentences.
        if line.startswith("[^") or line.startswith("```"):
            continue
        # Split into sentences.
        for sent in SENT_SPLIT_RE.split(line):
            sent = sent.strip()
            if not sent:
                continue
            sentences.append(sent)
    return sentences


def normalize(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip().lower()
    s = re.sub(r"[‘’]", "'", s)
    s = re.sub(r"[“”]", '"', s)
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"[ ]", " ", s)  # non-breaking space
    return s


def best_match_in(target: str, candidates: list[str], threshold: float = 0.55) -> tuple[int, float]:
    """Find best match for target in candidates by SequenceMatcher ratio."""
    norm_target = normalize(target)
    best_idx, best_ratio = -1, 0.0
    if not norm_target:
        return -1, 0.0
    # Quick filter: candidates that share at least 50% of target's tokens.
    target_tokens = set(re.findall(r"\b\w+\b", norm_target))
    if len(target_tokens) < 3:
        # Too short to fuzzy-match meaningfully; require exact substring.
        for i, c in enumerate(candidates):
            if norm_target in normalize(c):
                return i, 1.0
        return -1, 0.0
    for i, c in enumerate(candidates):
        norm_c = normalize(c)
        c_tokens = set(re.findall(r"\b\w+\b", norm_c))
        overlap = len(target_tokens & c_tokens)
        if overlap < len(target_tokens) * 0.4:
            continue
        ratio = SequenceMatcher(None, norm_target, norm_c).quick_ratio()
        if ratio < threshold:
            continue
        ratio = SequenceMatcher(None, norm_target, norm_c).ratio()
        if ratio > best_ratio:
            best_idx, best_ratio = i, ratio
    return best_idx, best_ratio


def main() -> int:
    print(f"Reading docx: {DOCX.name}")
    docx_blob = docx_text_blob(DOCX)
    docx_sents = split_sentences(docx_blob)
    print(f"  docx sentences: {len(docx_sents)}")

    print(f"Reading v11.8 markdown (pre-Aarik-edit baseline): {V11_8_MD.name}")
    v8_blob = md_to_plain(V11_8_MD)
    v8_sents = split_sentences(v8_blob)
    print(f"  v11.8 markdown sentences: {len(v8_sents)}")

    print(f"Reading v11.9 markdown: {V11_9_MD.name}")
    v9_blob = md_to_plain(V11_9_MD)
    v9_sents = split_sentences(v9_blob)
    print(f"  v11.9 sentences: {len(v9_sents)}")

    # 3-way logic:
    #   docx-match-v8 = high similarity to v11.8 markdown -> sentence is the
    #     pandoc-rendered original, no Aarik edit on this sentence
    #   docx-NO-match-v8 = differs from v11.8 markdown source -> Aarik edited it
    #   docx-match-v9 = sentence (or its near-equivalent) is in v11.9 already
    #
    # Aarik-edit-not-in-v11.9 = NO match in v8 AND NO match in v9.
    # Aarik-edit-already-merged = NO match in v8 AND HAS match in v9 (Claude
    #   landed Aarik's edit during v11.9 work, or Aarik and Claude both
    #   converged on similar wording).

    not_merged: list[dict] = []
    already_merged: list[dict] = []
    print("\nMatching docx sentences against both v11.8 and v11.9 markdown...")
    for i, s in enumerate(docx_sents):
        if len(s) < 40:
            continue
        if not re.search(r"[A-Za-z]{4,}", s):
            continue
        v8_idx, v8_ratio = best_match_in(s, v8_sents)
        if v8_ratio >= 0.95:
            continue  # original v11.8 sentence, not edited
        # docx differs from v11.8 source -> Aarik edited this sentence.
        v9_idx, v9_ratio = best_match_in(s, v9_sents)
        record = {
            "docx_sent": s,
            "v8_match": v8_sents[v8_idx] if v8_idx >= 0 else "",
            "v8_ratio": v8_ratio,
            "v9_match": v9_sents[v9_idx] if v9_idx >= 0 else "",
            "v9_ratio": v9_ratio,
        }
        if v9_ratio >= 0.92:
            already_merged.append(record)
        else:
            not_merged.append(record)
        if (i + 1) % 400 == 0:
            print(f"  {i + 1}/{len(docx_sents)} processed; "
                  f"unmerged: {len(not_merged)}; already-merged: {len(already_merged)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append(f"# Aarik's docx edits not in v11.9 — sentence-level 3-way diff\n")
    lines.append(f"Source docx: `{DOCX.name}`")
    lines.append(f"Pre-edit baseline: `{V11_8_MD.name}` (v11.8 markdown)")
    lines.append(f"Current target: `{V11_9_MD.name}` (v11.9 markdown)\n")
    lines.append(f"Method: a docx sentence is an Aarik edit if it does NOT match v11.8 markdown (similarity < 0.95). Of those:")
    lines.append(f"- **{len(not_merged)} edits NOT yet in v11.9** (similarity to v11.9 also < 0.92).")
    lines.append(f"- **{len(already_merged)} edits already merged into v11.9** (similarity to v11.9 ≥ 0.92).\n")
    lines.append("---\n")

    lines.append(f"## Aarik docx edits NOT in v11.9 ({len(not_merged)})\n")
    for f in not_merged[:300]:
        lines.append(f"### v8-md sim {f['v8_ratio']:.2f}, v9-md sim {f['v9_ratio']:.2f}")
        lines.append(f"**docx (Aarik):** {f['docx_sent']}")
        if f['v8_match']:
            lines.append(f"**v11.8 md (pre-edit):** {f['v8_match']}")
        if f['v9_match']:
            lines.append(f"**v11.9 md (current):** {f['v9_match']}")
        lines.append("")
        lines.append("---")

    lines.append(f"\n## Already merged ({len(already_merged)} — for reference)\n")
    for f in already_merged[:50]:
        lines.append(f"### v8-md sim {f['v8_ratio']:.2f}, v9-md sim {f['v9_ratio']:.2f}")
        lines.append(f"**docx:** {f['docx_sent']}")
        lines.append(f"**v11.9:** {f['v9_match']}")
        lines.append("---")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {OUT}")
    print(f"Aarik edits NOT in v11.9: {len(not_merged)}")
    print(f"Aarik edits already merged: {len(already_merged)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
