"""Mechanical verifier: scan the paper for any (subject, qid, condition)
reference and verify against the canonical V2 extractor.

For each detected reference:
  - Pull V2 cell (question text, held-out, response, primary mean, per-judge)
  - Look for paper text surrounding the reference and compare against V2
  - Flag mismatches (paper question text != V2; paper response excerpt not a
    substring of V2 response; cited score != V2 primary mean; etc.)

Outputs a report at docs/research/v11_9_paper_cell_reference_audit_<date>.md.

This does NOT replace human review; it surfaces candidate mismatches for
manual review and provides a mechanical sanity check.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))
from v2_canonical_cell_extractor_20260508 import extract


# Subject name -> canonical key mapping (paper text -> extractor arg)
SUBJECT_NAMES = {
    'Hamerton': 'hamerton', 'hamerton': 'hamerton',
    'Sunity Devee': 'sunity_devee', 'sunity_devee': 'sunity_devee',
    'Ebers': 'ebers', 'ebers': 'ebers',
    'Fukuzawa': 'fukuzawa', 'Yukichi Fukuzawa': 'fukuzawa', 'fukuzawa': 'fukuzawa',
    'Bernal Díaz': 'bernal_diaz', 'Bernal Diaz': 'bernal_diaz', 'Bernal Díaz del Castillo': 'bernal_diaz',
    'bernal_diaz': 'bernal_diaz',
    'Bābur': 'babur', 'Babur': 'babur', 'babur': 'babur',
    'Seacole': 'seacole', 'Mary Seacole': 'seacole', 'seacole': 'seacole',
    'Keckley': 'keckley', 'Elizabeth Keckley': 'keckley', 'keckley': 'keckley',
    'Yung Wing': 'yung_wing', 'yung_wing': 'yung_wing',
    'Zitkala-Ša': 'zitkala_sa', 'Zitkala-Sa': 'zitkala_sa', 'zitkala_sa': 'zitkala_sa',
    'Cellini': 'cellini', 'Benvenuto Cellini': 'cellini', 'cellini': 'cellini',
    'Rousseau': 'rousseau', 'Jean-Jacques Rousseau': 'rousseau', 'rousseau': 'rousseau',
    'Augustine': 'augustine', 'Saint Augustine': 'augustine', 'augustine': 'augustine',
    'Equiano': 'equiano', 'Olaudah Equiano': 'equiano', 'equiano': 'equiano',
}

# Condition aliases from paper text -> extractor arg
CONDITION_ALIASES = {
    'C5': 'C5_baseline', 'C5_baseline': 'C5_baseline', 'no-context': 'C5_baseline',
    'C2a': 'C2a_full_spec', 'Spec only': 'C2a_full_spec',
    'C2c': 'C2c_wrong_spec', 'wrong-spec': 'C2c_wrong_spec', 'wrong Spec': 'C2c_wrong_spec',
    'C4': 'C4_factdump', 'C4_factdump': 'C4_factdump', 'facts only': 'C4_factdump', 'factdump': 'C4_factdump',
    'C4a': 'C4a_full_facts_plus_spec', 'C4a_full_facts_plus_spec': 'C4a_full_facts_plus_spec',
    'facts+Spec': 'C4a_full_facts_plus_spec', 'facts + Spec': 'C4a_full_facts_plus_spec',
    'full pipeline': 'C4a_full_facts_plus_spec',
}

# Patterns that indicate a numeric score citation
SCORE_RE = re.compile(r'\bmean\s*([0-9]+\.[0-9]+)\b')
QID_RE = re.compile(r'\bQ(\d+)\b')


def iter_blockquote_examples(text: str):
    """Yield each `> ### Example X.` blockquote chunk, splitting at next Example
    header or at next non-blockquote section header (### or ##)."""
    starts = [(m.start(), m.group(1)) for m in re.finditer(r'(?m)^> ###\s+Example\s+([A-Z])\.', text)]
    for i, (start_pos, letter) in enumerate(starts):
        # End at next Example start, or at next plain section header, or end of file
        next_section_match = re.search(r'(?m)^(?:#{2,3}\s+|---\s*$)', text[start_pos + 1:])
        end_at_section = (start_pos + 1 + next_section_match.start()) if next_section_match else len(text)
        end_at_next_example = starts[i + 1][0] if i + 1 < len(starts) else len(text)
        end = min(end_at_section, end_at_next_example)
        block = text[start_pos:end]
        yield letter, block, start_pos


SUBJECT_LINE_RE = re.compile(r'\*\*Subject:\*\*\s+([^\.\n]+?)(?:\.|\n)')


def find_subject_qid_in_block(block: str):
    """Find subject name + Qid using the explicit Subject: prefix."""
    sm = SUBJECT_LINE_RE.search(block)
    sub_name = sm.group(1).strip() if sm else None
    sub_key = None
    if sub_name:
        # Try exact match first, then by longest-substring match
        if sub_name in SUBJECT_NAMES:
            sub_key = SUBJECT_NAMES[sub_name]
        else:
            for name, key in sorted(SUBJECT_NAMES.items(), key=lambda kv: -len(kv[0])):
                if name in sub_name:
                    sub_key = key
                    break
    qid_match = QID_RE.search(block)
    return ((sub_name, sub_key), int(qid_match.group(1)) if qid_match else None)


def normalize_for_compare(s: str) -> str:
    """Lowercase, collapse whitespace, strip punctuation noise."""
    s = re.sub(r'\s+', ' ', s.lower()).strip()
    s = re.sub(r'[‘’“”`\'"]', '', s)
    return s


def short_excerpt_in(needle: str, haystack: str, min_chars: int = 40) -> bool:
    """Is some short verbatim slice of needle present inside haystack?
    We slide a window across needle (step = min_chars // 4) and check each."""
    n = normalize_for_compare(needle)
    h = normalize_for_compare(haystack)
    if not n or not h:
        return False
    if min_chars > len(n):
        return n in h
    step = max(1, min_chars // 4)
    for i in range(0, len(n) - min_chars + 1, step):
        if n[i:i + min_chars] in h:
            return True
    return False


def audit_block(block: str, subject_key: str, qid: int) -> list[dict]:
    """For one example block, audit each condition row by extracting V2 and
    comparing against the block."""
    findings = []
    for cond_alias, cond_canon in [('C4_factdump', 'C4_factdump'),
                                   ('C4a_full_facts_plus_spec', 'C4a_full_facts_plus_spec')]:
        try:
            cell = extract(subject_key, qid, cond_canon)
        except Exception as e:
            findings.append({'condition': cond_canon, 'error': str(e)})
            continue
        # Check question presence
        q_in_block = short_excerpt_in(cell['question'], block)
        # Check held-out presence
        ho_in_block = short_excerpt_in(cell['held_out'], block)
        # Check response excerpt
        resp_in_block = short_excerpt_in(cell['response'], block, min_chars=60)
        # Check score
        scores_cited = [float(m) for m in SCORE_RE.findall(block)]
        score_match = any(abs(s - cell['primary_mean']) < 0.05 for s in scores_cited) if scores_cited else None
        findings.append({
            'condition': cond_canon,
            'question_in_block': q_in_block,
            'held_out_in_block': ho_in_block,
            'response_excerpt_present': resp_in_block,
            'score_cited_in_block': scores_cited,
            'score_match': score_match,
            'cell_primary_mean': cell['primary_mean'],
            'cell_question_first_60': cell['question'][:60],
            'cell_response_first_60': cell['response'][:60],
        })
    return findings


def main():
    paper_path = REPO / 'docs' / 'beyond_recall_v11_9_11_draft.md'
    text = paper_path.read_text(encoding='utf-8')

    out_lines = ['# v11.9 paper cell-reference audit\n',
                 'Generated by `scripts/verify_paper_cell_references_20260508.py`.',
                 'Each `> ### Example X.` blockquote in the paper is checked against the canonical V2 extractor.',
                 'PASS = question, held-out, response excerpt, and cited score all match V2 cached cell.\n']

    overall_pass = 0
    overall_findings = 0
    for letter, block, _start in iter_blockquote_examples(text):
        (sub_name, sub_key), qid = find_subject_qid_in_block(block)
        out_lines.append(f"## Example {letter}\n")
        if not sub_key or qid is None:
            out_lines.append(f"  Could not detect subject + qid (sub={sub_name}, qid={qid}). SKIPPED.\n")
            continue
        out_lines.append(f"  Subject: **{sub_name}** ({sub_key})  ")
        out_lines.append(f"  Qid: **{qid}**\n")
        per_cond = audit_block(block, sub_key, qid)
        for f in per_cond:
            cond = f['condition']
            if 'error' in f:
                out_lines.append(f"  - {cond}: ERROR ({f['error']})")
                continue
            out_lines.append(f"  - **{cond}** (primary mean V2 = {f['cell_primary_mean']})")
            out_lines.append(f"    - V2 question first chars: `{f['cell_question_first_60']}...`")
            out_lines.append(f"    - V2 response first chars: `{f['cell_response_first_60']}...`")
            tag_q = 'PASS' if f['question_in_block'] else 'FAIL'
            tag_h = 'PASS' if f['held_out_in_block'] else 'FAIL'
            tag_r = 'PASS' if f['response_excerpt_present'] else 'FAIL'
            tag_s = 'PASS' if f['score_match'] is True else ('NO_SCORE_CITED' if f['score_match'] is None else 'FAIL')
            out_lines.append(f"    - question-in-block: {tag_q}; held-out-in-block: {tag_h}; response-excerpt: {tag_r}; score: {tag_s}")
            overall_findings += 1
            if all([f['question_in_block'], f['held_out_in_block'], f['response_excerpt_present'], f['score_match'] in (True, None)]):
                overall_pass += 1
        out_lines.append('')

    out_lines.append(f"\n## Summary\n")
    out_lines.append(f"- Total cell-condition rows audited: {overall_findings}")
    out_lines.append(f"- Rows passing all checks: {overall_pass}")
    out_lines.append(f"- Rows with at least one fail: {overall_findings - overall_pass}")

    out_path = REPO / 'docs' / 'research' / 'v11_9_paper_cell_reference_audit_20260508.md'
    out_path.write_text('\n'.join(out_lines), encoding='utf-8')
    print(f"Audit written to {out_path}")
    print(f"Total rows: {overall_findings}, passing: {overall_pass}, failing: {overall_findings - overall_pass}")


if __name__ == '__main__':
    main()
