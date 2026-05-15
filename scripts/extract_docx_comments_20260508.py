"""Extract comments + the surrounding paragraph text they anchor to from a .docx.

Walks the document body, finds every w:commentRangeStart / w:commentRangeEnd
pair, captures the commented text span and the surrounding paragraph context,
then matches each comment id back to its w:comment record (author + text).

Output: Markdown with one section per comment, ordered by document order, each
showing: comment id, author, comment text, anchored span, surrounding paragraph.

Usage: python extract_docx_comments_20260508.py <input.docx> <output.md>
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def get_xml(z, name):
    if name not in z.namelist():
        return None
    with z.open(name) as f:
        return ET.parse(f).getroot()


def text_of(el):
    """Concatenate w:t descendants."""
    return ''.join((t.text or '') for t in el.iter(W + 't'))


def main(input_path: Path, output_path: Path) -> int:
    with zipfile.ZipFile(input_path) as z:
        comments_root = get_xml(z, 'word/comments.xml')
        document_root = get_xml(z, 'word/document.xml')

    if comments_root is None or document_root is None:
        print('No comments.xml or document.xml found.')
        return 1

    # Map id -> {author, text}
    comment_meta = {}
    for c in comments_root.findall(W + 'comment'):
        cid = c.get(W + 'id')
        author = c.get(W + 'author', '')
        text = text_of(c).strip()
        comment_meta[cid] = {'author': author, 'text': text}

    # Walk document body in order, build (paragraph_text, comments_in_para)
    body = document_root.find(W + 'body')
    paragraphs = []
    open_comments = {}  # id -> [span tokens collected]

    for p in body.findall(W + 'p'):
        para_text_parts = []
        para_comment_ids = set()
        cursor = 0
        for el in p.iter():
            tag = el.tag
            if tag == W + 'commentRangeStart':
                cid = el.get(W + 'id')
                open_comments[cid] = []
                para_comment_ids.add(cid)
            elif tag == W + 'commentRangeEnd':
                cid = el.get(W + 'id')
                open_comments.pop(cid, None)
            elif tag == W + 't':
                txt = el.text or ''
                para_text_parts.append(txt)
                for cid in list(open_comments.keys()):
                    open_comments[cid].append(txt)
        para_text = ''.join(para_text_parts)
        paragraphs.append((para_text, para_comment_ids))

    # Build comment -> {anchored_span, surrounding_paragraphs}
    comment_locations = {}
    for cid in comment_meta:
        comment_locations[cid] = {'anchor_span': '', 'paragraphs': []}

    # Re-walk to capture anchor_span per comment id (concatenate spans across multi-paragraph anchors)
    open_spans = {}
    for p in body.findall(W + 'p'):
        for el in p.iter():
            tag = el.tag
            if tag == W + 'commentRangeStart':
                cid = el.get(W + 'id')
                open_spans[cid] = []
            elif tag == W + 'commentRangeEnd':
                cid = el.get(W + 'id')
                if cid in open_spans:
                    comment_locations[cid]['anchor_span'] = ''.join(open_spans[cid]).strip()
                    open_spans.pop(cid, None)
            elif tag == W + 't':
                for cid in open_spans:
                    open_spans[cid].append(el.text or '')

    # Surrounding paragraph: capture each paragraph that contains a comment range
    for idx, (para_text, ids) in enumerate(paragraphs):
        for cid in ids:
            comment_locations[cid]['paragraphs'].append((idx, para_text))

    # Order comments by first appearance in the body
    first_appearance = {}
    for idx, (para_text, ids) in enumerate(paragraphs):
        for cid in ids:
            first_appearance.setdefault(cid, idx)
    ordered_ids = sorted(comment_meta.keys(), key=lambda c: first_appearance.get(c, 10**9))

    # Output
    out = ['# Aarik\'s feedback on `beyond_recall_v11_8_draft_with_figures.docx`\n']
    out.append(f"Total comments: {len(comment_meta)}\n")
    out.append(f"Source: {input_path.name}\n")
    out.append('---\n')

    for cid in ordered_ids:
        meta = comment_meta[cid]
        loc = comment_locations[cid]
        anchor = loc['anchor_span'] or '(no anchor span captured)'
        para_idx = first_appearance.get(cid, '?')
        para_preview = ''
        if loc['paragraphs']:
            para_preview = loc['paragraphs'][0][1][:600]
            if len(loc['paragraphs'][0][1]) > 600:
                para_preview += '...'
        out.append(f"## Comment {cid} — {meta['author'] or 'unknown'} (paragraph #{para_idx})\n")
        out.append(f"**Anchored span:** {anchor!r}\n")
        out.append(f"**Comment text:** {meta['text']}\n")
        out.append(f"**Surrounding paragraph:**\n> {para_preview}\n")
        out.append('---\n')

    output_path.write_text('\n'.join(out), encoding='utf-8')
    print(f"Wrote {len(ordered_ids)} comments to {output_path}")
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input.docx> <output.md>")
        sys.exit(2)
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
