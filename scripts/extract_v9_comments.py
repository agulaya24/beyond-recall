"""Extract inline Word comments from beyond_recall_v9_draft.docx and produce a
structured markdown checklist for v10 integration.

Parses word/comments.xml (comment metadata + text) and word/document.xml
(anchor ranges + nearest preceding heading) without modifying the docx.
"""
from __future__ import annotations

import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

DOCX = r"C:/Users/Aarik/Anthropic/memory-study-repo/docs/beyond_recall_v9_draft.docx"
OUT_MD = r"C:/Users/Aarik/Anthropic/memory-study-repo/docs/reviews/v9_docx_comments.md"
TODAY = "2026-04-24"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"
W15_NS = "http://schemas.microsoft.com/office/word/2012/wordml"
NS = {"w": W_NS, "w14": W14_NS, "w15": W15_NS}


def read_part(docx_path: str, part: str) -> bytes:
    with zipfile.ZipFile(docx_path) as z:
        try:
            return z.read(part)
        except KeyError:
            return b""


def parse_comments(xml_bytes: bytes):
    """Return dict[id] = {author, date, text, paraIds}."""
    if not xml_bytes.strip():
        return {}
    root = ET.fromstring(xml_bytes)
    comments = {}
    for c in root.findall(f"{{{W_NS}}}comment"):
        cid = c.attrib.get(f"{{{W_NS}}}id")
        author = c.attrib.get(f"{{{W_NS}}}author", "")
        date = c.attrib.get(f"{{{W_NS}}}date", "")
        paragraphs = []
        paraIds = []
        for p in c.findall(f"{{{W_NS}}}p"):
            # paraId attribute lives in the w14 namespace
            pid = p.attrib.get(f"{{{W14_NS}}}paraId")
            if pid:
                paraIds.append(pid)
            txt = "".join(t.text or "" for t in p.findall(f".//{{{W_NS}}}t"))
            paragraphs.append(txt)
        text = "\n".join(p for p in paragraphs if p.strip())
        comments[cid] = {
            "author": author,
            "date": date,
            "text": text.strip(),
            "paraIds": paraIds,
        }
    return comments


def parse_comments_extended(xml_bytes: bytes):
    """Return set of paraIds that are REPLIES (have a paraIdParent)."""
    if not xml_bytes.strip():
        return set()
    root = ET.fromstring(xml_bytes)
    replies = set()
    for ex in root.findall(f"{{{W15_NS}}}commentEx"):
        parent = ex.attrib.get(f"{{{W15_NS}}}paraIdParent")
        pid = ex.attrib.get(f"{{{W15_NS}}}paraId")
        if parent and pid:
            replies.add(pid)
    return replies


def _para_heading(p_elem):
    """Return heading level (1..9) and text if paragraph is a heading, else None."""
    pPr = p_elem.find(f"{{{W_NS}}}pPr")
    if pPr is None:
        return None
    pStyle = pPr.find(f"{{{W_NS}}}pStyle")
    if pStyle is None:
        return None
    val = pStyle.attrib.get(f"{{{W_NS}}}val", "")
    m = re.match(r"Heading(\d)", val)
    if not m:
        return None
    level = int(m.group(1))
    text = "".join(t.text or "" for t in p_elem.findall(f".//{{{W_NS}}}t"))
    return level, text.strip()


def parse_document(xml_bytes: bytes):
    """Walk the body in order. Track nearest preceding heading stack.

    Returns list of dicts per comment range:
      {id, order_idx, anchor_text, heading_level, heading_text}
    in document order of commentRangeStart.
    """
    root = ET.fromstring(xml_bytes)
    body = root.find(f"{{{W_NS}}}body")
    if body is None:
        return []

    # We need to walk the body content in document order, tracking:
    #   - current heading breadcrumb (by level)
    #   - open comment ranges (id -> {start_order, collected_text, start_heading})
    # commentRangeStart/End can appear inside paragraphs, so walk recursively.

    heading_stack = {}  # level -> text (last seen)
    open_ranges = {}
    finished = []  # list of dicts
    order_counter = 0

    def record_text(s):
        for cid, info in open_ranges.items():
            info["text"].append(s)

    def walk(elem):
        nonlocal order_counter
        tag = elem.tag
        # Paragraph: check heading first (heading text itself is not anchor scope
        # unless comment range spans into it, which we still capture via w:t).
        if tag == f"{{{W_NS}}}p":
            h = _para_heading(elem)
            if h is not None:
                level, text = h
                # Clear deeper levels
                for lvl in list(heading_stack.keys()):
                    if lvl >= level:
                        heading_stack.pop(lvl, None)
                heading_stack[level] = text
            # Recurse children
            for child in elem:
                walk(child)
            # Paragraph break = newline in anchor text if any range is open
            if open_ranges:
                record_text("\n")
            return

        if tag == f"{{{W_NS}}}commentRangeStart":
            cid = elem.attrib.get(f"{{{W_NS}}}id")
            order_counter += 1
            # Snapshot heading breadcrumb at start
            heading_snapshot = dict(heading_stack)
            open_ranges[cid] = {
                "order": order_counter,
                "text": [],
                "heading": heading_snapshot,
            }
            return

        if tag == f"{{{W_NS}}}commentRangeEnd":
            cid = elem.attrib.get(f"{{{W_NS}}}id")
            info = open_ranges.pop(cid, None)
            if info is not None:
                anchor = "".join(info["text"]).strip()
                # Collapse whitespace
                anchor = re.sub(r"\s+", " ", anchor)
                # Determine most specific heading (highest level number available)
                heading = info["heading"]
                if heading:
                    max_level = max(heading.keys())
                    h_text = heading[max_level]
                    h_level = max_level
                else:
                    h_text = ""
                    h_level = 0
                finished.append({
                    "id": cid,
                    "order": info["order"],
                    "anchor_text": anchor,
                    "heading_level": h_level,
                    "heading_text": h_text,
                })
            return

        if tag == f"{{{W_NS}}}commentReference":
            # Some docs omit ranges and only have commentReference. Capture these
            # too using surrounding paragraph text if no ranges.
            cid = elem.attrib.get(f"{{{W_NS}}}id")
            # Only treat as anchor if we haven't already captured via range
            # We'll fill later if unmatched. Record placeholder.
            order_counter += 1
            if heading_stack:
                max_level = max(heading_stack.keys())
                h_text = heading_stack[max_level]
                h_level = max_level
            else:
                h_text = ""
                h_level = 0
            # Mark a sentinel; only used if no range found
            finished.append({
                "id": cid,
                "order": order_counter,
                "anchor_text": "",  # may be filled if absent
                "heading_level": h_level,
                "heading_text": h_text,
                "_from_ref": True,
            })
            return

        if tag == f"{{{W_NS}}}t":
            if open_ranges:
                record_text(elem.text or "")
            return

        # Other elements: recurse
        for child in elem:
            walk(child)

    walk(body)

    # De-duplicate: prefer range entries over ref-only entries per id
    best = {}
    for f in finished:
        cid = f["id"]
        if cid not in best:
            best[cid] = f
        else:
            # Prefer the one with non-empty anchor_text and not from ref
            existing = best[cid]
            if f.get("_from_ref") and not existing.get("_from_ref"):
                continue
            if existing.get("_from_ref") and not f.get("_from_ref"):
                best[cid] = f
            elif not existing["anchor_text"] and f["anchor_text"]:
                best[cid] = f
    result = list(best.values())
    result.sort(key=lambda d: d["order"])
    return result


def classify(text: str) -> tuple[str, str]:
    """Heuristic classification + one-line read."""
    t = text.strip().lower()
    note = text.strip().splitlines()[0][:180] if text.strip() else ""

    # DEFERRED: thought-for-later markers
    if re.search(r"\b(later|defer|future|someday|post[- ]?launch|not blocking|not a blocker)\b", t):
        return "DEFERRED", note

    # QUESTION: asks the pipeline/you to verify, check, look up, or answer a factual
    # query. Usually contains explicit "can we" / "verify" / "source?" cues.
    if re.search(r"\b(can we verify|verify this|double[- ]?check|source\?|cite\?|citation\?)\b", t):
        return "QUESTION", note

    # APPLY: mechanical / imperative changes. Broadened to include common directive
    # patterns used in these comments ("footnote", "put in footnote", "rename",
    # "expand title", "link it", "review for", "consider putting in").
    apply_patterns = [
        r"\b(change|replace|rename|re[- ]?name|rewrite|move|delete|remove|add|insert|tighten|cut|fix|shorten|lengthen|rephrase|reword|swap|update|expand|shorten|visualize|link|relabel|re[- ]?label|specify|format|reformat|review for)\b",
        r"\bfootnote\b",
        r"\bconsider (putting|moving|adding|cutting|using)\b",
        r"\bdon'?t phrase\b",
        r"\bneed to\b",
        r"\bshould (specify|state|include|use|be)\b",
    ]
    for pat in apply_patterns:
        if re.search(pat, t):
            return "APPLY", note

    # Author judgment fallback: direct question or ambiguous concern
    if "?" in text:
        return "AUTHOR_JUDGMENT", note
    return "AUTHOR_JUDGMENT", note


def main():
    if not os.path.exists(DOCX):
        print(f"Docx not found: {DOCX}")
        sys.exit(1)

    comments_xml = read_part(DOCX, "word/comments.xml")
    document_xml = read_part(DOCX, "word/document.xml")
    ext_xml = read_part(DOCX, "word/commentsExtended.xml")

    comments = parse_comments(comments_xml)
    reply_paraIds = parse_comments_extended(ext_xml)

    # Identify reply-only (empty autoreply) comment ids to suppress.
    # A comment is a reply if ANY of its paraIds are marked as replies.
    # We treat empty-text replies as Word auto-generated placeholders and drop them,
    # but if a reply carries its own text we keep it as a follow-up comment.
    suppressed = set()
    for cid, meta in list(comments.items()):
        is_reply = any(pid in reply_paraIds for pid in meta["paraIds"])
        if is_reply and not meta["text"]:
            suppressed.add(cid)
    for cid in suppressed:
        comments.pop(cid, None)

    if not comments:
        # Empty or missing comments part
        os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
        with open(OUT_MD, "w", encoding="utf-8") as f:
            f.write(f"# v9 Word Comments Extraction ({TODAY})\n\n")
            f.write("No comments found in `word/comments.xml` (empty or missing).\n")
        print("No comments found.")
        return

    anchors = parse_document(document_xml)
    anchor_by_id = {a["id"]: a for a in anchors}

    # Build ordered entries. Use anchor order if present, else fall back to
    # comment id numeric order.
    ordered = []
    for cid, meta in comments.items():
        a = anchor_by_id.get(cid)
        order = a["order"] if a else (int(cid) + 1_000_000)
        anchor_text = a["anchor_text"] if a else ""
        heading_level = a["heading_level"] if a else 0
        heading_text = a["heading_text"] if a else ""
        cls, note = classify(meta["text"])
        ordered.append({
            "id": cid,
            "order": order,
            "author": meta["author"],
            "date": meta["date"],
            "text": meta["text"],
            "anchor_text": anchor_text,
            "heading_level": heading_level,
            "heading_text": heading_text,
            "classification": cls,
            "one_line": note,
        })
    ordered.sort(key=lambda d: d["order"])

    # Summary stats
    total = len(ordered)
    by_class = {}
    by_section = {}
    questions = []
    directives = []
    for i, e in enumerate(ordered, 1):
        by_class[e["classification"]] = by_class.get(e["classification"], 0) + 1
        sec = e["heading_text"] or "(unheaded)"
        by_section[sec] = by_section.get(sec, 0) + 1
        if e["classification"] in ("QUESTION", "AUTHOR_JUDGMENT"):
            questions.append((i, e))
        elif e["classification"] == "APPLY":
            directives.append((i, e))

    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(f"# v9 Word Comments — Extraction & v10 Checklist\n\n")
        f.write(f"Source: `docs/beyond_recall_v9_draft.docx`\n")
        f.write(f"Extracted: {TODAY}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"**Total comments:** {total}\n\n")
        f.write(f"### Breakdown by classification\n\n")
        for k in ("APPLY", "AUTHOR_JUDGMENT", "QUESTION", "DEFERRED"):
            if k in by_class:
                f.write(f"- {k}: {by_class[k]}\n")
        f.write("\n")
        f.write(f"### Breakdown by section\n\n")
        for sec, n in sorted(by_section.items(), key=lambda kv: -kv[1]):
            f.write(f"- {sec}: {n}\n")
        f.write("\n")
        f.write(f"### Questions expecting an answer ({len(questions)})\n\n")
        for i, e in questions:
            f.write(f"- #{i} (§{e['heading_text']}): {e['one_line']}\n")
        f.write("\n")
        f.write(f"### Directives asking for a change ({len(directives)})\n\n")
        for i, e in directives:
            f.write(f"- #{i} (§{e['heading_text']}): {e['one_line']}\n")
        f.write("\n---\n\n")

        for i, e in enumerate(ordered, 1):
            heading_disp = e["heading_text"] or "(no heading)"
            f.write(f"## Comment {i} (id={e['id']}) — {heading_disp}\n\n")
            f.write(f"**Author:** {e['author'] or '(unknown)'}\n")
            f.write(f"**Date:** {e['date'] or '(unknown)'}\n")
            anchor = e["anchor_text"]
            if len(anchor) > 500:
                anchor_disp = anchor[:500] + "..."
            else:
                anchor_disp = anchor
            f.write(f"**Anchored to:** \"{anchor_disp}\"\n\n")
            f.write("**Comment:**\n\n")
            for line in (e["text"] or "(empty)").splitlines():
                f.write(f"> {line}\n")
            f.write("\n")
            f.write(f"**Classification:** {e['classification']}\n")
            f.write(f"**Note:** {e['one_line']}\n\n")
            f.write("---\n\n")

    print(f"Wrote {OUT_MD}")
    print(f"Total comments: {total}")
    print(f"By class: {by_class}")
    print(f"Top sections: {dict(list(sorted(by_section.items(), key=lambda kv: -kv[1]))[:8])}")


if __name__ == "__main__":
    main()
