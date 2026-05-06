"""Figure review script — sends each figure to Claude Opus + OpenAI GPT-5.4,
collects verbatim reviews, writes incrementally to markdown report."""
import base64
import os
import sys
import time
from pathlib import Path

import anthropic
from openai import OpenAI

FIG_DIR = Path(r"C:\Users\Aarik\Anthropic\memory-study-repo\figures")
REPORT = Path(r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\reviews\figure_review_20260422.md")

# (filename, caption, supported-claim) — from figures/README.md
FIGURES = [
    (
        "fig1_global_gradient.png",
        "Per-subject baseline (C5) vs. spec+facts score across all 14 subjects, ordered by baseline. Visualizes the gradient result (spec helps most where baseline is low).",
        "§1.3 Finding 1, §4.1-4.2 (the gradient table and Wilcoxon p=0.006, slope -0.98)",
    ),
    (
        "fig2_compression_curve.png",
        "Log-tokens vs. normalized prediction score. Shows that ~5K-token spec beats 34K-token raw corpus.",
        "Figure 2: Compression curve; supports §4.5 (Hamerton C2a 3.04 vs C8 2.32)",
    ),
    (
        "fig3_retrieval_disagreement.png",
        "Top-k retrieval disagreement rate across the three embedding-based memory systems (Mem0, Letta, Supermemory) at k=1, 3, 5, 10.",
        "§1 abstract and §4 memory-systems discussion (93% disagreement at top-1, 53% at top-10)",
    ),
    (
        "fig4_hedging_reduction.png",
        "Hedging/refusal rate across C5 -> C2a -> C4a conditions, reported under two classifier rules. Narrow rule: 28.8% -> 1.4% -> 0.0%. Broader rule: 41.2% -> 7.9% -> 0.4%.",
        "§1.3 Finding 4, §5 hedging analysis",
    ),
    (
        "fig5_condition_effects.png",
        "Condition-by-condition mean deltas across subjects. Multi-panel summary of the core conditions (C1, C2a, C2c, C3, C4, C4a, C5, C6, C7, C8, C9).",
        "§4 core results tables; orientation figure for readers scanning the condition space",
    ),
    (
        "fig6_wrong_spec_control.png",
        "Correct-spec score vs. wrong-spec (random derangement) score per subject. Shows wrong-spec lands near baseline.",
        "§1.3 Finding 3 and §4.4 (content, not format)",
    ),
    (
        "fig7_memory_systems.png",
        "Per-system spec delta (C3 minus C1) for Mem0, Letta, Supermemory, Zep, and Base Layer on the 9 low-baseline subjects.",
        "§1.3 Finding 2 and §4.3 (spec is additive to every commercial system)",
    ),
    (
        "fig8_judge_agreement.png",
        "Inter-judge agreement across the 6-judge panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash). Correlations / alpha across subjects.",
        "§3.6 judge calibration and §5 inter-judge reliability discussion",
    ),
    (
        "fig9_cultural_baseline.png",
        "Baseline score by subject culture / origin. Shows baseline is correlated with Western-canon pretraining exposure, not subject quality.",
        "§4 gradient discussion; addresses reviewer concern that the gradient might be confounded by corpus difficulty",
    ),
    (
        "fig10_letta_scaling.png",
        "Letta stateful-agent scaling behavior across the subject set.",
        "§4 memory-systems discussion — Letta scaling ceiling",
    ),
    (
        "fig11_tier2_replication.png",
        "Tier-2 replication: robustness of the gradient finding on an alternate subject tier.",
        "§4 replication discussion",
    ),
    (
        "fig_4_1_gradient_scatter.png",
        "Scatter: baseline vs spec+facts score, per subject, with regression slope.",
        "§4.1 gradient scatter (canonical v8 figure)",
    ),
    (
        "fig_4_2_compression.png",
        "Compression curve (v8 canonical): log-tokens vs normalized score.",
        "§4.2 compression (canonical v8 figure)",
    ),
    (
        "fig_4_2_1_question_improvement_rates.png",
        "Stacked-bar per-question outcome distribution (Improved / Tied / Worsened) for C2a, C4, C8, C4a vs C5 baseline. Spec alone improves 70.9% of questions at ~1/10th the context of raw corpus (78.3%).",
        "§4.2.1 Question-Improvement Rate — candidate secondary reporting metric",
    ),
]

PROMPT_TEMPLATE = """You are reviewing a figure from an AI/ML research paper on behavioral specifications for AI personalization. Target venue is arXiv / NeurIPS / ICML.

Figure caption: {caption}
What it supports: {claim}

Review for:
1. Clarity. Can a reader understand what is being shown without a long caption?
2. Style. Does it match academic publication conventions (clean axes, minimal chart junk, legible at print size)?
3. Color. Professional, colorblind-safe, print-friendly?
4. Labels / legend. Enough? Too many? Typography consistent?
5. Axes. Appropriate scale? Misleading baselines or truncations?

Respond in exactly this structure, no preamble:
- GRADE: A | B | C | D | F
- TOP 3 ISSUES (priority order, each one line):
  1. [issue] -> [specific fix]
  2. [issue] -> [specific fix]
  3. [issue] -> [specific fix]
- STRENGTHS: [one line]
- IDEAL VERSION: [one sentence description of what the improved figure should look like]"""


def b64(path: Path) -> str:
    return base64.standard_b64encode(path.read_bytes()).decode("utf-8")


def review_opus(client, img_b64: str, prompt: str) -> str:
    try:
        resp = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=500,
            temperature=0.2,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                    {"type": "text", "text": prompt},
                ],
            }],
        )
        return resp.content[0].text
    except Exception as e:
        # Try fallback model name
        try:
            resp = client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=500,
                temperature=0.2,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                        {"type": "text", "text": prompt},
                    ],
                }],
            )
            return resp.content[0].text
        except Exception as e2:
            return f"ERROR: {e} / fallback: {e2}"


def review_gpt(client, img_b64: str, prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model="gpt-5.4",
            max_completion_tokens=500,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                ],
            }],
        )
        return resp.choices[0].message.content
    except Exception as e:
        # Fallback to gpt-4o which we know supports vision
        try:
            resp = client.chat.completions.create(
                model="gpt-4o",
                max_tokens=500,
                temperature=0.2,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                    ],
                }],
            )
            return f"(Note: gpt-5.4 unavailable; using gpt-4o fallback)\n\n{resp.choices[0].message.content}"
        except Exception as e2:
            return f"ERROR: gpt-5.4: {e} / gpt-4o fallback: {e2}"


def write_header(grades: dict):
    """Write header + partial summary table + details already collected."""
    lines = []
    lines.append("# Figure Quality Review (2026-04-22)")
    lines.append("")
    lines.append("Vision providers: Claude Opus 4.5, OpenAI GPT-5.4 (with gpt-4o fallback if unavailable). Figures reviewed: 14.")
    lines.append("")
    lines.append("## Summary table")
    lines.append("")
    lines.append("| Figure | Opus grade | GPT-5.4 grade | Consensus priority |")
    lines.append("|---|---|---|---|")
    for fn, _, _ in FIGURES:
        stem = fn.replace(".png", "")
        g = grades.get(fn, {})
        lines.append(f"| {stem} | {g.get('opus','-')} | {g.get('gpt','-')} | {g.get('priority','-')} |")
    return "\n".join(lines) + "\n\n"


def extract_grade(text: str) -> str:
    if not text or text.startswith("ERROR"):
        return "ERR"
    # Look for "GRADE: X"
    import re
    m = re.search(r"GRADE:\s*([A-F])", text)
    return m.group(1) if m else "?"


def consensus_priority(opus_grade: str, gpt_grade: str) -> str:
    order = {"A": 5, "B": 4, "C": 3, "D": 2, "F": 1, "?": 3, "ERR": 3}
    lo = min(order.get(opus_grade, 3), order.get(gpt_grade, 3))
    if lo <= 2:
        return "Critical"
    if lo == 3:
        return "High"
    if lo == 4:
        return "Low"
    return "Low"


def main():
    anth = anthropic.Anthropic()
    oai = OpenAI()

    grades = {}
    details = []  # list of (filename, opus_text, gpt_text)

    # Initial write — header only
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(write_header(grades) + "## Per-figure details\n\n", encoding="utf-8")

    for i, (fn, caption, claim) in enumerate(FIGURES, 1):
        fpath = FIG_DIR / fn
        print(f"[{i}/{len(FIGURES)}] {fn}", flush=True)
        if not fpath.exists():
            print(f"  MISSING: {fpath}", flush=True)
            grades[fn] = {"opus": "MISS", "gpt": "MISS", "priority": "-"}
            details.append((fn, "MISSING FILE", "MISSING FILE"))
            continue

        img_b64 = b64(fpath)
        prompt = PROMPT_TEMPLATE.format(caption=caption, claim=claim)

        t0 = time.time()
        opus_text = review_opus(anth, img_b64, prompt)
        t1 = time.time()
        gpt_text = review_gpt(oai, img_b64, prompt)
        t2 = time.time()
        print(f"  opus {t1-t0:.1f}s, gpt {t2-t1:.1f}s", flush=True)

        og = extract_grade(opus_text)
        gg = extract_grade(gpt_text)
        pri = consensus_priority(og, gg)
        grades[fn] = {"opus": og, "gpt": gg, "priority": pri}
        details.append((fn, opus_text, gpt_text))

        # Rewrite report incrementally
        body = write_header(grades) + "## Per-figure details\n\n"
        for d_fn, d_op, d_gp in details:
            body += f"### {d_fn}\n\n"
            body += f"**Claude Opus:**\n\n{d_op}\n\n"
            body += f"**GPT-5.4:**\n\n{d_gp}\n\n"
            body += "---\n\n"
        REPORT.write_text(body, encoding="utf-8")

    # Write final sections placeholder — will be filled by agent
    body = write_header(grades) + "## Per-figure details\n\n"
    for d_fn, d_op, d_gp in details:
        body += f"### {d_fn}\n\n"
        body += f"**Claude Opus:**\n\n{d_op}\n\n"
        body += f"**GPT-5.4:**\n\n{d_gp}\n\n"
        body += "---\n\n"
    body += "## Cross-cutting observations\n\n_TBD — agent synthesis_\n\n"
    body += "## Prioritized fix list\n\n_TBD — agent synthesis_\n\n"
    body += "## Overall verdict\n\n_TBD — agent synthesis_\n"
    REPORT.write_text(body, encoding="utf-8")
    print("DONE. Report at", REPORT, flush=True)


if __name__ == "__main__":
    main()
