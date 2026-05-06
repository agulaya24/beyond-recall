"""Build v8 draft: v7 §1+§2 (locked) merged with v6 §3-end, with 85% claim sweep.

v8 structure:
- Front matter + §1 + §2 from v7 (locked content from this session's review)
- §3 through appendices from v6 (unreviewed content, 85% claim swept)

The 85% claim sweep replaces blanket "four systems score 85%+ on recall benchmarks"
type statements with the contested-landscape framing established in §2.1 and KEY_FINDINGS m21.

No abstract is carried over (v6 abstract needs a full rewrite based on §1 locked content;
will be handled in the abstract-review pass later).
"""

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
V7 = REPO / "docs" / "beyond_recall_v7_draft.md"
V6 = REPO / "docs" / "beyond_recall_v6_draft.md"
V8 = REPO / "docs" / "beyond_recall_v8_draft.md"

# Sweep: (old_substring, new_substring). Order matters — longer/specific patterns first.
SWEEP_PAIRS = [
    # §5.7 L1134 type statement
    (
        "This study is, to our knowledge, the first head-to-head evaluation of the major memory-for-agents providers (Mem0, Letta, Supermemory, Zep) against a non-recall criterion. Recall benchmarks (LOCOMO, LongMemEval, LME-S) measure whether the system returns the right chunk; all four providers score 85%+ on those.",
        "This study is, to our knowledge, the first head-to-head evaluation of the major memory-for-agents providers (Mem0, Letta, Supermemory, Zep) against a non-recall criterion. Recall benchmarks (LOCOMO, LongMemEval, LME-S) measure whether the system returns the right chunk; all four providers publish recall-benchmark scores in roughly the 68–85% range (see §2.1 for the contested benchmark methodology discussion).",
    ),
    # §4.3 retrieval-variance framing
    (
        "The four systems all pass recall benchmarks at 85%+",
        "The four systems all publish recall-benchmark scores in the 68–85% range (methodology disputed, see §2.1)",
    ),
    # §8 Conclusion / closing
    (
        "Four systems that all pass recall benchmarks at 85%+",
        "Four systems that publish recall-benchmark scores in the 68–85% range (methodology disputed, see §2.1)",
    ),
    # §8 closing / key takeaways
    (
        "Four memory systems score 85%+ on recall",
        "Four memory systems publish recall-benchmark scores in the 68–85% range",
    ),
    # §5 misc mentions
    (
        "four funded systems score 85%+ on LOCOMO/LongMemEval",
        "four funded systems publish LOCOMO/LongMemEval scores in the 68–85% range",
    ),
    # §4.3 key finding phrasing
    (
        "Systems that all pass recall benchmarks at 85%+",
        "Systems that publish recall-benchmark scores in the 68–85% range",
    ),
    (
        "all pass recall benchmarks at 85%+",
        "publish recall-benchmark scores in the 68–85% range",
    ),
    # §5.8 / §1.6 misc
    (
        "Memory systems that pass recall at 85%+",
        "Memory systems that publish recall-benchmark scores in the 68–85% range",
    ),
    # §4.3.2 Supermemory strengths - keep specific 81.6/85.2 since that's a supported number
    # No change needed there.
]


def apply_sweep(text):
    applied = 0
    for old, new in SWEEP_PAIRS:
        if old in text:
            text = text.replace(old, new)
            applied += 1
    return text, applied


def build():
    v7 = V7.read_text(encoding="utf-8")
    v6 = V6.read_text(encoding="utf-8")

    # Strip v7's trailing navigation hint if present
    v7_lines = v7.split("\n")
    # Drop trailing lines that look like "*§2 Related Work complete. Next: §3..."
    while v7_lines and (v7_lines[-1].strip().startswith("*") or v7_lines[-1].strip() == "" or v7_lines[-1].strip() == "---"):
        v7_lines.pop()
    v7_clean = "\n".join(v7_lines).rstrip() + "\n"

    # Locate "## 3. Study Design" in v6
    v6_lines = v6.split("\n")
    s3_idx = None
    for i, line in enumerate(v6_lines):
        if line.startswith("## 3. Study Design"):
            s3_idx = i
            break
    if s3_idx is None:
        raise RuntimeError("Could not find §3 start in v6")

    v6_tail = "\n".join(v6_lines[s3_idx:])

    # Apply sweep on v6 tail only (v7 §1+§2 already correct)
    v6_tail_swept, applied = apply_sweep(v6_tail)

    v8 = v7_clean + "\n\n" + v6_tail_swept

    V8.write_text(v8, encoding="utf-8")

    print(f"v8 written: {V8}")
    print(f"v7 kept: front matter + §1 + §2 ({len(v7_clean.splitlines())} lines)")
    print(f"v6 tail appended: §3 onwards ({len(v6_tail_swept.splitlines())} lines)")
    print(f"85% sweep replacements applied: {applied}")
    print(f"v8 total: {len(v8.splitlines())} lines")


if __name__ == "__main__":
    build()
