"""Build a section-by-section technicality map for v11.9.1.

For each H2/H3, score the section on a 0-5 technical-density scale based on:
  - statistical jargon: Wilcoxon, Spearman, Krippendorff, R², ρ, α, p =, CI, slope, regression
  - Greek symbols: ρ, α, β, Δ
  - variable names: Δ_C4a, Δ_spec, Δ, n=, N=
  - code refs / file paths: scripts/, results/, .json, .py
  - condition codes density: C5, C2a, C4a, etc per 100 words
  - method-internal vocabulary: anchor, rubric, panel, judge, abstention, derangement
  - equations / formulas

Output: ordered list of sections with score + rationale + primary lever for laymanization.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "docs" / "beyond_recall_v11_9_1_draft.md"
OUT = REPO / "docs" / "research" / "v11_9_1_section_technicality_map_20260509.md"

text = SRC.read_text(encoding="utf-8")
lines = text.splitlines()

heading_re = re.compile(r"^(##+)\s+(.*)$")

# Walk: collect sections. Section = lines from a heading until next heading at same-or-higher level.
sections = []
current = None
for i, ln in enumerate(lines, 1):
    m = heading_re.match(ln)
    if m:
        # Close prior
        if current is not None:
            current["end"] = i - 1
            sections.append(current)
        level = len(m.group(1))
        title = m.group(2).strip()
        current = {"level": level, "title": title, "start": i, "end": len(lines), "body": []}
        continue
    if current is not None:
        current["body"].append(ln)
if current is not None:
    sections.append(current)

# Restrict to H2/H3 only (## or ###) to keep map digestible
sections = [s for s in sections if s["level"] in (2, 3)]

# Skip walk-progress + appendix-deep utility sections from foreground attention
SKIP_PREFIXES = ("§4 Walk Progress",)

# Patterns
P_STATS = re.compile(r"\b(Wilcoxon|Spearman|Krippendorff|regression|slope|R²|R\^2|95% CI|p\s*=\s*0\.|p\s*<\s*0\.|bootstrap|permutation|Pearson|standard error|standard deviation|null distribution|reshuffles|effect size|Cohen)\b", re.IGNORECASE)
P_GREEK = re.compile(r"[ραβΔπσμ]")
P_VAR = re.compile(r"\bΔ[_\w]*|\b[Nn]\s*=\s*\d|\bn=\s*\d|\b[Kk]\s*=\s*\d|\bα\s*=|\bρ\s*=|\bp\s*=")
P_CODE = re.compile(r"`[^`]*\.(py|json|md|csv|sh|yaml)`|`scripts/|`results/|`docs/")
P_CONDITION = re.compile(r"\b(C[1-9]a?c?)\b")
P_METHOD = re.compile(r"\b(anchor|rubric|panel|judge|abstention|derangement|aggregation|interquartile|cosine|jaccard|embedding|tokenizer)\b", re.IGNORECASE)


def word_count(blob: str) -> int:
    return len(re.findall(r"\b\w+\b", blob))

records = []
for s in sections:
    if any(s["title"].startswith(p) for p in SKIP_PREFIXES):
        continue
    blob = "\n".join(s["body"])
    wc = word_count(blob) or 1
    n_stats   = len(P_STATS.findall(blob))
    n_greek   = len(P_GREEK.findall(blob))
    n_var     = len(P_VAR.findall(blob))
    n_code    = len(P_CODE.findall(blob))
    n_cond    = len(P_CONDITION.findall(blob))
    n_method  = len(P_METHOD.findall(blob))

    # Density per 1000 words
    def per_kw(n: int) -> float:
        return 1000.0 * n / wc

    score_components = {
        "stats": min(per_kw(n_stats) / 5.0, 5.0),
        "greek": min(per_kw(n_greek) / 8.0, 5.0),
        "var":   min(per_kw(n_var)   / 6.0, 5.0),
        "code":  min(per_kw(n_code)  / 3.0, 5.0),
        "cond":  min(per_kw(n_cond)  / 8.0, 5.0),
        "method":min(per_kw(n_method)/ 12.0, 5.0),
    }
    raw_score = sum(score_components.values())  # 0-30
    score_5 = round(raw_score / 30.0 * 5.0, 1)

    # Primary lever: which component is highest -> what to laymanize
    top_component = max(score_components, key=lambda k: score_components[k])

    records.append({
        "level": s["level"],
        "title": s["title"],
        "wc": wc,
        "score": score_5,
        "components": score_components,
        "top_component": top_component,
        "n_stats": n_stats,
        "n_greek": n_greek,
        "n_var": n_var,
        "n_code": n_code,
        "n_cond": n_cond,
        "n_method": n_method,
    })

# Sort by section order (already in document order)

# Build output
out_lines = ["# v11.9.1 — section technicality map", ""]
out_lines.append(f"Sections ranked on a 0-5 technical-density scale (higher = denser jargon/stats/codes per 1000 words). Higher scores = more aggressive laymanization opportunity in audience-facing prose; appendix-style scores ≥ 4 are usually appropriate as-is.")
out_lines.append("")
out_lines.append("**Components (0-5 each, capped):**")
out_lines.append("- `stats` = Wilcoxon/Spearman/Krippendorff/R²/p=/regression/permutation density")
out_lines.append("- `greek` = ρ α β Δ π σ μ density")
out_lines.append("- `var` = Δ_C4a, n=, k=, α=, ρ=, p= variable density")
out_lines.append("- `code` = backticked file paths (.py / .json / scripts/ / results/)")
out_lines.append("- `cond` = condition-code (C1, C2a, C4a, ...) density")
out_lines.append("- `method` = anchor / rubric / panel / judge / abstention / derangement / cosine / jaccard density")
out_lines.append("")
out_lines.append("**Score-5 → laymanization band:**")
out_lines.append("- 0.0–1.0 — already layman; touch only if a specific term lands wrong")
out_lines.append("- 1.0–2.0 — mostly layman; a few terms need parenthetical glosses or a 1-line setup")
out_lines.append("- 2.0–3.0 — mixed; needs a layman opener + technical body OK to follow")
out_lines.append("- 3.0–4.0 — technical-by-design; appropriate if it's a methods/sensitivity section, but the section opener should be a layman summary if it's audience-facing")
out_lines.append("- 4.0–5.0 — fully technical; appropriate for §3.3 internals, §4.6, appendices; not appropriate for §1, §5, abstract")
out_lines.append("")
out_lines.append("---")
out_lines.append("")
out_lines.append("| § | Title | wc | Score | Top driver | stats / greek / var / code / cond / method |")
out_lines.append("|---|---|---:|---:|---|---|")
for r in records:
    indent = "&nbsp;&nbsp;" * (r["level"] - 2)
    title_cell = f"{indent}{r['title']}"
    counts = f"{r['n_stats']} / {r['n_greek']} / {r['n_var']} / {r['n_code']} / {r['n_cond']} / {r['n_method']}"
    out_lines.append(f"| H{r['level']} | {title_cell} | {r['wc']} | {r['score']:.1f} | {r['top_component']} | {counts} |")

OUT.write_text("\n".join(out_lines), encoding="utf-8")
print(f"Wrote {OUT}  ({len(records)} sections)")
print(f"\nTop-10 highest-density sections:")
for r in sorted(records, key=lambda x: -x["score"])[:10]:
    print(f"  {r['score']:.1f}  H{r['level']}  {r['title'][:60]} (top: {r['top_component']})")
print(f"\nLowest-10 (most layman) sections:")
for r in sorted(records, key=lambda x: x["score"])[:10]:
    print(f"  {r['score']:.1f}  H{r['level']}  {r['title'][:60]}")
