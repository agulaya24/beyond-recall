"""Build A/B/C inventories for v11.9.1 walk:
A. band / anchor / slice  — every occurrence with categorical guess at meaning + line context
B. condition labels       — every C5/C4a/etc. + natural-language label, prose vs table, paired or bare
C. em-dashes              — every '—' with surrounding sentence
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "docs" / "beyond_recall_v11_9_1_draft.md"
OUT_DIR = REPO / "docs" / "research"

text = SRC.read_text(encoding="utf-8")
lines = text.splitlines()

# Build line -> section heading map
heading_re = re.compile(r"^(#{1,6})\s+(.*)$")
line_section: list[str] = ["(preamble)"] * (len(lines) + 1)
current = "(preamble)"
for i, ln in enumerate(lines, 1):
    m = heading_re.match(ln)
    if m:
        current = m.group(2).strip()
    line_section[i] = current


def is_table_line(ln: str) -> bool:
    s = ln.strip()
    return s.startswith("|") and s.count("|") >= 2


def is_table_separator(ln: str) -> bool:
    s = ln.strip()
    return bool(re.match(r"^\|[\s\-:|]+\|$", s))


# ------------------------- THEME A: band / anchor / slice -------------------------

A_terms = {
    "band":   re.compile(r"\b(bands?)\b", re.IGNORECASE),
    "anchor": re.compile(r"\b(anchors?)\b", re.IGNORECASE),
    "slice":  re.compile(r"\b(slices?)\b", re.IGNORECASE),
}

# Heuristic categorization buckets per term.
A_buckets = {
    "band": {
        "baseline-cluster":  re.compile(r"\b(baseline|low-baseline|high-baseline|mid-baseline)\s+band|\bband\s+of\s+the\s+baseline|\bin\s+the\s+(low|high|mid)-?baseline\s+band|\bcrosses?\s+into\s+the\s+(low|high|mid)-?baseline\s+band\b", re.IGNORECASE),
        "score-band-on-rubric":  re.compile(r"\b(rubric\s+band|score\s+band|anchor\s+band|band\s+\d|\d\s+band|band\s+1|band\s+2|band\s+3|band\s+4|band\s+5)\b", re.IGNORECASE),
        "score-cluster-numeric": re.compile(r"\bband\s+\d|\bband\s+(low|mid|high)\b|cluster.*band", re.IGNORECASE),
    },
    "anchor": {
        "rubric-anchor":  re.compile(r"\b(rubric\s+anchor|integer\s+anchor|anchor\s+\d|anchor\s+1|anchor\s+2|anchor\s+3|anchor\s+4|anchor\s+5|score\s+anchor)\b", re.IGNORECASE),
        "anchor-crossing": re.compile(r"(cross[a-z\-]*).{0,20}\banchor|\banchor.{0,20}\bcross", re.IGNORECASE),
        "multi-anchor":   re.compile(r"\bmulti[\-\s]?anchor\b|\b(two|three|2|3)[\-\s]?anchor\b", re.IGNORECASE),
        "spec-anchor":    re.compile(r"\b(epistemic\s+anchors?|axiomatic|A\d\s+anchor)\b"),
    },
    "slice": {
        "subject-grouping": re.compile(r"\b(low-baseline|high-baseline|mid-baseline)\s+slice|\b9-?subject\s+slice|\bsubject\s+slice|\bn=\d+\s+slice", re.IGNORECASE),
        "data-pool-slice":  re.compile(r"\b(question|response|paired|condition|paired|14-?subject|13-?subject|8-?subject)\s+slice", re.IGNORECASE),
    },
}

A_records: dict[str, list[dict]] = {"band": [], "anchor": [], "slice": []}
for i, ln in enumerate(lines, 1):
    for term, rx in A_terms.items():
        for m in rx.finditer(ln):
            # Categorize via buckets in order
            bucket = "(uncategorized)"
            for label, brx in A_buckets[term].items():
                if brx.search(ln):
                    bucket = label
                    break
            A_records[term].append({
                "line": i,
                "section": line_section[i],
                "in_table": is_table_line(ln),
                "bucket": bucket,
                "match": m.group(0),
                "snippet": ln.strip(),
            })

# ------------------------- THEME B: condition labels -------------------------

# Condition codes that may appear bare or paired with natural-language.
COND_CODES = ["C5", "C4a", "C4", "C2a", "C2c", "C9", "C8", "C3", "C1"]
COND_RE = re.compile(r"\b(" + "|".join(COND_CODES) + r")\b")

# Natural-language labels we expect to see for those codes.
NL_PHRASES = [
    ("no-context baseline", ["C5"]),
    ("No-Context Baseline", ["C5"]),
    ("Spec only", ["C2a"]),
    ("spec only", ["C2a"]),
    ("Spec alone", ["C2a"]),
    ("spec alone", ["C2a"]),
    ("facts only", ["C4"]),
    ("Facts Only", ["C4"]),
    ("facts + spec", ["C4a"]),
    ("Facts + Spec", ["C4a"]),
    ("full pipeline", ["C4a"]),
    ("corpus + spec", ["C9"]),
    ("Corpus + Spec", ["C9"]),
    ("raw corpus", ["C8"]),
    ("Raw Corpus", ["C8"]),
    ("wrong Spec", ["C2c"]),
    ("Wrong Spec", ["C2c"]),
    ("retrieval alone", ["C1"]),
    ("retrieval + spec", ["C3"]),
    ("Retrieval + Spec", ["C3"]),
]
NL_REGEXES = [(re.compile(r"\b" + re.escape(p) + r"\b"), p, codes) for p, codes in NL_PHRASES]

B_records = []
for i, ln in enumerate(lines, 1):
    is_table = is_table_line(ln) and not is_table_separator(ln)
    code_hits = [(m.group(0), m.start()) for m in COND_RE.finditer(ln)]
    nl_hits = []
    for rx, phrase, codes in NL_REGEXES:
        for m in rx.finditer(ln):
            nl_hits.append((phrase, m.start(), codes))
    if not code_hits and not nl_hits:
        continue
    # Determine pairing pattern
    pairing = "none"
    if code_hits and nl_hits:
        pairing = "paired-on-line"
    elif code_hits and not nl_hits:
        pairing = "code-only"
    elif nl_hits and not code_hits:
        pairing = "nl-only"
    B_records.append({
        "line": i,
        "section": line_section[i],
        "in_table": is_table,
        "pairing": pairing,
        "codes": [h[0] for h in code_hits],
        "nl": [h[0] for h in nl_hits],
        "snippet": ln.strip(),
    })

# ------------------------- THEME C: em-dashes -------------------------

C_records = []
for i, ln in enumerate(lines, 1):
    if "—" not in ln:
        continue
    if is_table_separator(ln):
        continue
    C_records.append({
        "line": i,
        "section": line_section[i],
        "in_table": is_table_line(ln),
        "count": ln.count("—"),
        "snippet": ln.strip(),
    })

# ------------------------- write outputs -------------------------

OUT_DIR.mkdir(parents=True, exist_ok=True)

def write_md(path: Path, title: str, body: list[str]) -> None:
    path.write_text(title + "\n\n" + "\n".join(body), encoding="utf-8")
    print(f"Wrote {path}  ({len(body)} content lines)")

# --- A ---
A_out = OUT_DIR / "v11_9_1_inventory_band_anchor_slice_20260509.md"
A_lines = []
for term in ("band", "anchor", "slice"):
    recs = A_records[term]
    A_lines.append(f"## `{term}` — {len(recs)} occurrence(s)\n")
    bucket_counts: dict[str, int] = {}
    for r in recs:
        bucket_counts[r["bucket"]] = bucket_counts.get(r["bucket"], 0) + 1
    A_lines.append("**Bucket counts:** " + ", ".join(f"{k}={v}" for k, v in sorted(bucket_counts.items(), key=lambda x: -x[1])) + "\n")
    # Group by bucket
    by_bucket: dict[str, list[dict]] = {}
    for r in recs:
        by_bucket.setdefault(r["bucket"], []).append(r)
    for bucket, brecs in by_bucket.items():
        A_lines.append(f"\n### `{term}` — {bucket} ({len(brecs)})\n")
        for r in brecs:
            tbl = " *[in-table]*" if r["in_table"] else ""
            A_lines.append(f"- L{r['line']} *({r['section']})*{tbl}: {r['snippet'][:280]}")
    A_lines.append("")
write_md(A_out, "# v11.9.1 — band / anchor / slice inventory", A_lines)

# --- B ---
B_out = OUT_DIR / "v11_9_1_inventory_condition_labels_20260509.md"
B_lines = []
prose = [r for r in B_records if not r["in_table"]]
table = [r for r in B_records if r["in_table"]]
B_lines.append(f"## Condition mentions: {len(B_records)} lines ({len(prose)} prose, {len(table)} table)\n")

# Pairing pattern counts
def pair_counts(recs):
    out: dict[str, int] = {}
    for r in recs:
        out[r["pairing"]] = out.get(r["pairing"], 0) + 1
    return out

B_lines.append(f"### Prose pairing patterns: {pair_counts(prose)}")
B_lines.append(f"### Table pairing patterns: {pair_counts(table)}\n")

B_lines.append("---\n")
B_lines.append("## Code-only mentions in prose (potential proper-noun-label candidates)\n")
for r in prose:
    if r["pairing"] == "code-only":
        B_lines.append(f"- L{r['line']} *({r['section']})* codes={r['codes']}: {r['snippet'][:280]}")

B_lines.append("\n## Paired-on-line in prose (already labeled)\n")
for r in prose:
    if r["pairing"] == "paired-on-line":
        B_lines.append(f"- L{r['line']} *({r['section']})* codes={r['codes']} nl={r['nl']}: {r['snippet'][:240]}")

B_lines.append("\n## NL-only in prose (no code paired)\n")
for r in prose:
    if r["pairing"] == "nl-only":
        B_lines.append(f"- L{r['line']} *({r['section']})* nl={r['nl']}: {r['snippet'][:240]}")

B_lines.append("\n## Tables containing condition codes/labels\n")
for r in table:
    B_lines.append(f"- L{r['line']} *({r['section']})* pairing={r['pairing']} codes={r['codes']} nl={r['nl']}: {r['snippet'][:200]}")

write_md(B_out, "# v11.9.1 — condition-label inventory", B_lines)

# --- C ---
C_out = OUT_DIR / "v11_9_1_inventory_emdashes_20260509.md"
C_lines = [f"## Em-dash occurrences: {len(C_records)} line(s), {sum(r['count'] for r in C_records)} total dashes\n"]
by_section: dict[str, list[dict]] = {}
for r in C_records:
    by_section.setdefault(r["section"], []).append(r)
for sec, recs in by_section.items():
    C_lines.append(f"\n### {sec} ({len(recs)})\n")
    for r in recs:
        tbl = " *[in-table]*" if r["in_table"] else ""
        C_lines.append(f"- L{r['line']}{tbl} ({r['count']}×): {r['snippet'][:260]}")
write_md(C_out, "# v11.9.1 — em-dash inventory", C_lines)

# Aggregate summary
print("\nSummary:")
print(f"  band:   {len(A_records['band'])} occurrence(s)")
print(f"  anchor: {len(A_records['anchor'])} occurrence(s)")
print(f"  slice:  {len(A_records['slice'])} occurrence(s)")
print(f"  conditions: {len(B_records)} lines (prose {len(prose)}, table {len(table)})")
print(f"  em-dashes: {len(C_records)} lines / {sum(r['count'] for r in C_records)} dashes")
