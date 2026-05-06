"""
Mechanical section-pointer audit for beyond_recall_v11_8_draft.md.

Builds a map of actual section headings, scans every §X(.Y(.Z)?) reference in
the paper, and reports for each reference: does the target section exist, what
is its current title, and the line/context of the reference.

Output: docs/reviews/section_pointer_audit_v11_8_<ts>.md

Mechanical pass only. Does not judge whether the cross-ref is semantically
correct (e.g. "§5.7 catalogues open questions" -- the section may exist but
contain different content). That requires manual review against the report.
"""
import re
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER = REPO_ROOT / 'docs' / 'beyond_recall_v11_8_draft.md'
OUT_DIR = REPO_ROOT / 'docs' / 'reviews'
OUT_DIR.mkdir(exist_ok=True)

HEADING_RE = re.compile(r'^(#{2,4})\s+(\d+(?:\.\d+)*)\.?\s+(.+?)\s*$')
REF_RE = re.compile(r'§\s*(\d+(?:\.\d+){0,3})')


def parse_headings(lines):
    """Return dict: '5.7' -> {'title': 'Privacy', 'line': 1579, 'level': 3}."""
    headings = {}
    for i, line in enumerate(lines, start=1):
        m = HEADING_RE.match(line)
        if not m:
            continue
        hashes, num, title = m.groups()
        headings[num] = {
            'title': title.strip(),
            'line': i,
            'level': len(hashes),
            'raw': line.rstrip(),
        }
    return headings


def find_refs(lines):
    """Yield (line_number, section_ref, surrounding_context)."""
    for i, line in enumerate(lines, start=1):
        for m in REF_RE.finditer(line):
            ref = m.group(1)
            start = max(0, m.start() - 60)
            end = min(len(line), m.end() + 60)
            ctx = line[start:end].strip()
            yield i, ref, ctx


def main():
    text = PAPER.read_text(encoding='utf-8')
    lines = text.splitlines()
    headings = parse_headings(lines)

    print(f'Parsed {len(headings)} headings.')

    refs = list(find_refs(lines))
    print(f'Found {len(refs)} §X references.')

    rows = []
    for line_no, ref, ctx in refs:
        if ref in headings:
            h = headings[ref]
            status = 'OK'
            target_title = h['title']
            target_line = h['line']
        else:
            status = 'MISSING'
            target_title = '(no such section)'
            target_line = ''
        rows.append({
            'status': status,
            'ref_line': line_no,
            'ref': ref,
            'target_title': target_title,
            'target_line': target_line,
            'context': ctx,
        })

    missing = [r for r in rows if r['status'] == 'MISSING']
    ok = [r for r in rows if r['status'] == 'OK']

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out = OUT_DIR / f'section_pointer_audit_v11_8_{ts}.md'

    body = []
    body.append(f'# v11.8 Section-Pointer Audit -- mechanical')
    body.append(f'_Generated: {ts}_')
    body.append(f'_Paper: `{PAPER.name}`_')
    body.append('')
    body.append(f'- Total headings parsed: **{len(headings)}**')
    body.append(f'- Total §X refs found: **{len(refs)}**')
    body.append(f'- OK (target exists): **{len(ok)}**')
    body.append(f'- MISSING (target does not exist): **{len(missing)}**')
    body.append('')

    body.append('## Heading map')
    body.append('')
    body.append('| § | Title | Line |')
    body.append('|---|---|---:|')
    for num in sorted(headings.keys(), key=lambda s: tuple(int(x) for x in s.split('.'))):
        h = headings[num]
        body.append(f'| §{num} | {h["title"]} | {h["line"]} |')
    body.append('')

    body.append('## MISSING references (target section does not exist)')
    body.append('')
    if missing:
        body.append('| Ref line | §Ref | Context |')
        body.append('|---:|---|---|')
        for r in missing:
            ctx = r['context'].replace('|', '\\|')
            body.append(f'| {r["ref_line"]} | §{r["ref"]} | {ctx} |')
    else:
        body.append('_None._')
    body.append('')

    body.append('## All references with current target')
    body.append('')
    body.append('| Ref line | §Ref | Status | Target title | Target line | Context |')
    body.append('|---:|---|---|---|---:|---|')
    for r in rows:
        ctx = r['context'].replace('|', '\\|')
        title = r['target_title'].replace('|', '\\|')
        body.append(
            f'| {r["ref_line"]} | §{r["ref"]} | {r["status"]} | {title} | '
            f'{r["target_line"]} | {ctx} |'
        )
    body.append('')

    out.write_text('\n'.join(body), encoding='utf-8')
    print(f'Saved: {out}')
    print(f'  OK: {len(ok)}, MISSING: {len(missing)}')


if __name__ == '__main__':
    main()
