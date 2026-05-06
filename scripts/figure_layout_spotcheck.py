"""Vision-only layout/collision spot-check on all 14 paper figures.

Uses Claude Opus via Anthropic SDK. Single pass, fast. Writes one-line result
per figure to docs/reviews/figure_layout_spotcheck_20260423.md.
"""

import base64
import os
import sys
from datetime import datetime
from pathlib import Path

from anthropic import Anthropic

FIGURES_DIR = Path(r"C:/Users/Aarik/Anthropic/memory-study-repo/figures")
OUTPUT_FILE = Path(
    r"C:/Users/Aarik/Anthropic/memory-study-repo/docs/reviews/figure_layout_spotcheck_20260423.md"
)

FIGURE_NAMES = [
    "fig1_global_gradient",
    "fig2_compression_curve",
    "fig3_retrieval_disagreement",
    "fig4_hedging_reduction",
    "fig5_condition_effects",
    "fig6_wrong_spec_control",
    "fig7_memory_systems",
    "fig8_judge_agreement",
    "fig9_cultural_baseline",
    "fig10_letta_scaling",
    "fig11_tier2_replication",
    "fig_4_1_gradient_scatter",
    "fig_4_2_compression",
    "fig_4_2_1_question_improvement_rates",
]

PROMPT = (
    "Quick layout check. Is this figure publication-ready from a formatting "
    "standpoint? Flag only: (a) overlapping text/labels, (b) legend covering "
    "data, (c) clipped or cut-off elements, (d) tick labels overlapping each "
    "other, (e) unreadably small text, (f) anything else a print reviewer "
    "would flag as a layout bug. Do NOT critique content, color, or style "
    "choices — just layout/collision issues. Respond in one of two forms:\n"
    "- \"CLEAN\" if no layout issues\n"
    "- \"ISSUES: [brief bullet list]\" if anything needs fixing"
)

# Try a few model IDs in case the exact name varies
MODEL_CANDIDATES = [
    "claude-opus-4-5",
    "claude-opus-4-5-20250101",
    "claude-opus-4-6",
    "claude-opus-4-7",
]


def encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def pick_model(client: Anthropic) -> str:
    """Ping each candidate with a trivial call; return the first that works."""
    for m in MODEL_CANDIDATES:
        try:
            client.messages.create(
                model=m,
                max_tokens=8,
                messages=[{"role": "user", "content": "ok"}],
            )
            return m
        except Exception as e:
            print(f"[model probe] {m} -> {type(e).__name__}: {str(e)[:100]}")
    raise RuntimeError("No candidate model worked")


def check_figure(client: Anthropic, model: str, path: Path) -> str:
    img_b64 = encode_image(path)
    resp = client.messages.create(
        model=model,
        max_tokens=200,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_b64,
                        },
                    },
                    {"type": "text", "text": PROMPT},
                ],
            }
        ],
    )
    return resp.content[0].text.strip()


def main() -> int:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 1

    client = Anthropic(api_key=api_key)
    model = pick_model(client)
    print(f"[info] using model: {model}")

    results = []
    for name in FIGURE_NAMES:
        png = FIGURES_DIR / f"{name}.png"
        if not png.exists():
            results.append((name, "MISSING FILE"))
            print(f"[{name}] MISSING FILE")
            continue
        try:
            verdict = check_figure(client, model, png)
        except Exception as e:
            verdict = f"ERROR: {type(e).__name__}: {str(e)[:150]}"
        one_line = verdict.replace("\n", " ").strip()
        results.append((name, one_line))
        print(f"[{name}] {one_line[:180]}")

    # Write report
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    clean = sum(1 for _, v in results if v.startswith("CLEAN"))
    issues = [(n, v) for n, v in results if not v.startswith("CLEAN")]

    lines = [
        "# Figure Layout Spot-Check (2026-04-23)",
        "",
        f"- Run: {ts}",
        f"- Model: {model}",
        f"- Scope: layout/collision only (no content/color/style critique)",
        f"- Figures checked: {len(results)}",
        f"- CLEAN: {clean}",
        f"- FLAGGED: {len(issues)}",
        "",
        "## Per-figure verdicts",
        "",
    ]
    for name, verdict in results:
        lines.append(f"- **{name}**: {verdict}")
    lines.append("")
    if issues:
        lines.append("## Flagged figures")
        lines.append("")
        for name, verdict in issues:
            lines.append(f"### {name}")
            lines.append("")
            lines.append(verdict)
            lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[info] wrote report -> {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
