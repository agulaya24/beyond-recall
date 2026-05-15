"""
Scan the Beyond Recall v8 paper draft for GTM / marketing / pitch-deck register
and density issues, section by section, using Claude Haiku 4.5.

Output: a single synthesized markdown report under docs/reviews/.
"""
from __future__ import annotations

import os
import re
import sys
import json
import time
from datetime import datetime
from pathlib import Path

import anthropic

PAPER_PATH = Path(__file__).resolve().parents[1] / "docs" / "beyond_recall_v8_draft.md"
REVIEWS_DIR = Path(__file__).resolve().parents[1] / "docs" / "reviews"
MODEL = "claude-haiku-4-5-20251001"

# Split points: we segment on top-level sections and some large subsections to
# keep each call within comfortable token budgets.
# Each tuple: (chunk_label, start_line_1indexed_inclusive, end_line_1indexed_inclusive_or_None_for_eof)
SEGMENTS = [
    ("§1 Introduction (1.1–1.5)", 16, 145),
    ("§2 Related Work", 147, 218),
    ("§3 Study Design", 220, 558),
    ("§4.1 Gradient + 4.1.1 + 4.1.2", 576, 760),
    ("§4.2 Compression + 4.2.1", 761, 872),
    ("§4.3 Mechanism", 873, 1004),
    ("§4.4 Memory-System Composition + 4.4.1", 1005, 1177),
    ("§4.5 Robustness (4.5.1 / 4.5.2 / 4.5.3)", 1178, 1242),
    ("§4.6 Interpretation vs Recall", 1243, None),
]


SCAN_PROMPT = """You are an editor reviewing a research paper for residual marketing / GTM / pitch-deck register. The author wants the prose to read as clean academic writing, not as a funding deck. Your job is to flag every instance of marketing register and suggest plainer alternatives.

For each instance, output one line:
[section §X.Y] "exact phrase" -> suggested replacement | reason

Also flag dense passages:
[dense §X.Y] "first 60 chars of sentence..." -> suggestion for breaking up

At the end, give a register-cleanliness score (1-5) for each section covered in this chunk, with 1 = heavy GTM feel, 5 = clean academic prose.

Focus ONLY on prose. Ignore tables, code blocks, and formatted lists.

Types of GTM/marketing register to catch:
- Marketing verbs: "beats," "crushes," "dominates," "unlocks," "leverages," "transforms," "revolutionizes"
- Pitch-deck superlatives: "cleanest," "strongest," "most robust," "best-in-class"
- Vague-strength descriptors: "significant," "substantial," "meaningful," "impressive," "remarkable," "powerful"
- Oversold framings: "the key to," "at the heart of," "fundamentally changes," "flagship," "load-bearing," "foundational"
- Verb-noun inflation: "mechanism," "dynamic," "machinery," "architecture" used where plain words suffice
- Compound nouns that feel invented: "over-theorization," "hurts-heavy," "count-asymmetric magnitude-symmetric mixture"

Be thorough. Flag every instance. It is easier for the author to reject a false positive than to miss a real one.

Paper text follows:

<<<BEGIN PAPER CHUNK: {label}>>>
{chunk}
<<<END PAPER CHUNK>>>
"""


def extract_segment(lines: list[str], start: int, end: int | None) -> str:
    """Extract a 1-indexed inclusive range from the full file lines."""
    if end is None:
        sub = lines[start - 1 :]
    else:
        sub = lines[start - 1 : end]
    return "".join(sub)


def call_haiku(client: anthropic.Anthropic, label: str, chunk: str) -> str:
    prompt = SCAN_PROMPT.format(label=label, chunk=chunk)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    # Concatenate any text blocks
    return "\n".join(b.text for b in resp.content if hasattr(b, "text"))


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 1
    if not PAPER_PATH.exists():
        print(f"ERROR: paper not found at {PAPER_PATH}", file=sys.stderr)
        return 1

    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)

    with open(PAPER_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    client = anthropic.Anthropic()
    per_chunk_outputs: list[tuple[str, str]] = []

    for label, start, end in SEGMENTS:
        chunk = extract_segment(lines, start, end)
        char_count = len(chunk)
        print(f"[scan] {label}  lines {start}..{end or 'EOF'}  {char_count} chars", flush=True)
        tries = 0
        while True:
            try:
                out = call_haiku(client, label, chunk)
                break
            except Exception as e:
                tries += 1
                print(f"  error on try {tries}: {e!r}", flush=True)
                if tries >= 3:
                    out = f"[ERROR calling Haiku on {label}: {e!r}]"
                    break
                time.sleep(2 * tries)
        per_chunk_outputs.append((label, out))

    # Synthesize single report
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REVIEWS_DIR / f"gtm_jargon_scan_{ts}.md"
    raw_path = REVIEWS_DIR / f"gtm_jargon_scan_{ts}_raw_haiku.md"

    # Save raw Haiku outputs first (durable intermediate)
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(f"# GTM/Jargon Scan Raw Haiku Outputs ({ts})\n\n")
        f.write(f"Model: `{MODEL}`  |  temperature 0.2  |  max_tokens 8000\n\n")
        f.write(f"Paper: `{PAPER_PATH}`\n\n---\n\n")
        for label, out in per_chunk_outputs:
            f.write(f"## Chunk: {label}\n\n")
            f.write(out.strip() + "\n\n---\n\n")
    print(f"[scan] raw outputs saved to {raw_path}", flush=True)

    # Now build the structured synthesis report
    # Parse each chunk output for:
    #   - "[section §X.Y]" GTM flag lines
    #   - "[dense §X.Y]"   density flag lines
    #   - section cleanliness scores (flexible match)
    gtm_lines: list[tuple[str, str]] = []   # (chunk_label, line)
    dense_lines: list[tuple[str, str]] = []
    score_entries: list[tuple[str, str]] = []  # (chunk_label, score block)

    score_block_re = re.compile(
        r"(?:register[- ]cleanliness|cleanliness)\s*(?:score[s]?)?[^\n]*",
        re.IGNORECASE,
    )

    for label, out in per_chunk_outputs:
        for line in out.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            low = stripped.lower()
            if low.startswith("[section") or low.startswith("[§") or low.startswith("[gtm"):
                gtm_lines.append((label, stripped))
            elif low.startswith("[dense"):
                dense_lines.append((label, stripped))

        # Extract trailing score summary (last ~20 non-empty lines heuristically)
        tail = [ln for ln in out.splitlines() if ln.strip()][-40:]
        # Keep any lines that look score-like
        for ln in tail:
            if re.search(r"§?\d+\.\d+.*[:\-]\s*[1-5]\b", ln) or re.search(
                r"^\s*§?\d+\.\d+\s*[:\-]\s*[1-5]\b", ln
            ):
                score_entries.append((label, ln.strip()))

    # Write synthesized report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# GTM / Jargon / Density Scan — Beyond Recall v8\n\n")
        f.write(f"Generated: {ts}\n\n")
        f.write(f"Model: `{MODEL}`  |  temperature 0.2  |  max_tokens 8000 per chunk\n\n")
        f.write(f"Paper: `{PAPER_PATH}`\n\n")
        f.write(f"Raw per-chunk Haiku outputs: `{raw_path.name}`\n\n")
        f.write("---\n\n")

        # 1. Per-section cleanliness scores
        f.write("## 1. Per-Section Cleanliness Scores\n\n")
        f.write("Scale: 1 = heavy GTM feel, 5 = clean academic prose. Scores extracted from Haiku's chunk-level summaries.\n\n")
        if score_entries:
            f.write("| Chunk | Raw score line from Haiku |\n|---|---|\n")
            for chunk_label, line in score_entries:
                safe_line = line.replace("|", "\\|")
                f.write(f"| {chunk_label} | {safe_line} |\n")
            f.write("\n")
        else:
            f.write("_No score lines parsed automatically. See raw outputs._\n\n")

        # 2. All flagged GTM instances, grouped by chunk
        f.write("## 2. Flagged GTM / Marketing Register Instances\n\n")
        f.write(f"Total flagged lines: **{len(gtm_lines)}**\n\n")
        current = None
        for chunk_label, line in gtm_lines:
            if chunk_label != current:
                f.write(f"\n### {chunk_label}\n\n")
                current = chunk_label
            f.write(f"- {line}\n")
        if not gtm_lines:
            f.write("_No GTM instances parsed. Check raw outputs._\n")
        f.write("\n")

        # 3. All flagged dense passages, grouped by chunk
        f.write("## 3. Flagged Dense Passages\n\n")
        f.write(f"Total flagged lines: **{len(dense_lines)}**\n\n")
        current = None
        for chunk_label, line in dense_lines:
            if chunk_label != current:
                f.write(f"\n### {chunk_label}\n\n")
                current = chunk_label
            f.write(f"- {line}\n")
        if not dense_lines:
            f.write("_No density issues parsed. Check raw outputs._\n")
        f.write("\n")

        # 4. Raw per-chunk summaries (trailing summaries from each chunk for
        # readers who want Haiku's own prioritization)
        f.write("## 4. Per-Chunk Trailing Summaries (from Haiku)\n\n")
        f.write("Each chunk's final summary/priority statements as emitted by Haiku, in order.\n\n")
        for label, out in per_chunk_outputs:
            tail_nonempty = [ln for ln in out.splitlines() if ln.strip()]
            # Take everything from the first line that looks like "cleanliness"
            tail_start = 0
            for i, ln in enumerate(tail_nonempty):
                if score_block_re.search(ln):
                    tail_start = i
                    break
            summary_block = "\n".join(tail_nonempty[tail_start:]) if tail_start else "\n".join(tail_nonempty[-15:])
            f.write(f"### {label}\n\n")
            f.write("```\n" + summary_block.strip() + "\n```\n\n")

        f.write("---\n\n")
        f.write("_End of scan report._\n")

    print(f"[scan] synthesized report saved to {report_path}", flush=True)
    print(json.dumps({
        "report": str(report_path),
        "raw": str(raw_path),
        "gtm_flags": len(gtm_lines),
        "density_flags": len(dense_lines),
        "score_entries": len(score_entries),
        "chunks": len(per_chunk_outputs),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
