"""Capitalization pass for v11.9.11 paper draft.

Rules:
1. "specification" / "spec" → "Specification" / "Spec" when referring to the
   Behavioral Specification artifact. Identified by article context.
2. Condition names ("no-context", "all facts", "retrieval only", "facts only")
   → Title Case when used as formal condition references.
3. NEVER modify text inside block quotes (lines starting with >).
4. NEVER modify text inside *"..."* italic quoted spans (model responses).
5. NEVER modify text inside `code spans`.

Reports per-pattern counts of changes made.
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
PAPER = REPO / "docs" / "beyond_recall_v11_9_11_draft.md"


def is_protected_line(line: str) -> bool:
    """Block quotes (model responses excerpted) preserved exactly."""
    return line.lstrip().startswith(">")


def mask_protected_spans(line: str) -> tuple[str, list[tuple[int, str]]]:
    """Mask italic-quoted spans (*"..."*) and code spans (`...`) so they
    are not touched. Returns (masked_line, [(placeholder_index, original)])."""
    placeholders = []
    out = []
    i = 0
    while i < len(line):
        # Italic-quoted span: *"..."*
        if line[i:i+2] == '*"':
            end = line.find('"*', i + 2)
            if end != -1:
                end += 2
                ph = f"\x00MASK{len(placeholders)}\x00"
                placeholders.append((len(placeholders), line[i:end]))
                out.append(ph)
                i = end
                continue
        # Code span: `...`
        if line[i] == "`":
            end = line.find("`", i + 1)
            if end != -1:
                end += 1
                ph = f"\x00MASK{len(placeholders)}\x00"
                placeholders.append((len(placeholders), line[i:end]))
                out.append(ph)
                i = end
                continue
        out.append(line[i])
        i += 1
    return "".join(out), placeholders


def unmask(line: str, placeholders: list[tuple[int, str]]) -> str:
    for idx, original in placeholders:
        line = line.replace(f"\x00MASK{idx}\x00", original)
    return line


# Article patterns that signal we are referring to The Specification (the artifact)
# rather than using "specification" generically.
ARTICLE_PREFIX = r"(?:the|a|each|every|this|that|its|our|their|matched|correct|wrong|served|same|active|inserted|provided|given)"


def cap_specification(line: str, counts: dict) -> str:
    """Apply: (article) specification → (article) Specification.
       Also: (article) spec → (article) Spec.
       Also: behavioral specification → Behavioral Specification.
    """
    # "behavioral specification" first (compound term)
    pattern_behavioral = re.compile(r"\bbehavioral specification\b")
    def repl_behavioral(m):
        counts['behavioral_specification'] += 1
        return "Behavioral Specification"
    line = pattern_behavioral.sub(repl_behavioral, line)

    # "behavioral spec" (compound informal)
    pattern_behavioral_spec = re.compile(r"\bbehavioral spec\b")
    def repl_behavioral_spec(m):
        counts['behavioral_spec'] += 1
        return "Behavioral Spec"
    line = pattern_behavioral_spec.sub(repl_behavioral_spec, line)

    # "(article) specification" → "(article) Specification"
    pattern_spec_article = re.compile(rf"\b({ARTICLE_PREFIX})\s+specification\b", re.IGNORECASE)
    def repl_spec_article(m):
        counts['specification_with_article'] += 1
        # Preserve the article's original case
        return f"{m.group(1)} Specification"
    line = pattern_spec_article.sub(repl_spec_article, line)

    # "(article) spec" → "(article) Spec" — but NOT "respect", "inspect", etc.
    pattern_spec_word = re.compile(rf"\b({ARTICLE_PREFIX})\s+spec\b", re.IGNORECASE)
    def repl_spec_word(m):
        counts['spec_with_article'] += 1
        return f"{m.group(1)} Spec"
    line = pattern_spec_word.sub(repl_spec_word, line)

    return line


# Condition-name patterns — these are formal nouns when referring to the conditions.
# Match "no-context (baseline|prediction|condition|...)" and similar contextual cues.
CONDITION_CONTEXT_WORDS = r"(?:baselines?|predictions?|conditions?|responses?|scores?|cells?|rows?|panels?|aggregates?|runs?|configurations?|setups?|controls?|scorings?|judgments?|refusals?|abstentions?)"


def cap_conditions(line: str, counts: dict) -> str:
    """Capitalize condition-name phrases when used as formal references."""
    # "no-context baseline" / "no-context prediction" / "no-context score" / "no-context condition"
    pat_no_context = re.compile(rf"\bno-context\s+({CONDITION_CONTEXT_WORDS})\b")
    def repl_no_context(m):
        counts['no_context_condition'] += 1
        return f"No-Context {m.group(1).capitalize()}"
    line = pat_no_context.sub(repl_no_context, line)

    # "no-context, Spec," — list-context condition reference
    pat_no_context_list = re.compile(r"\bno-context(?=,\s+Spec)")
    def repl_no_context_list(m):
        counts['no_context_condition'] += 1
        return "No-Context"
    line = pat_no_context_list.sub(repl_no_context_list, line)

    # "all facts (no Spec)" / "all facts condition" / "all facts baseline" etc.
    pat_all_facts = re.compile(rf"\ball facts\b(?=\s+(?:{CONDITION_CONTEXT_WORDS}|\(|,))")
    def repl_all_facts(m):
        counts['all_facts_condition'] += 1
        return "All Facts"
    line = pat_all_facts.sub(repl_all_facts, line)

    # "retrieval only" (C1 condition name)
    pat_retrieval_only = re.compile(r"\bretrieval only\b")
    def repl_retrieval_only(m):
        counts['retrieval_only_condition'] += 1
        return "Retrieval Only"
    line = pat_retrieval_only.sub(repl_retrieval_only, line)

    # "facts only" (C4 condition name)
    pat_facts_only = re.compile(rf"\bfacts only\b(?=\s+(?:{CONDITION_CONTEXT_WORDS}|\(|,|;|\.))")
    def repl_facts_only(m):
        counts['facts_only_condition'] += 1
        return "Facts Only"
    line = pat_facts_only.sub(repl_facts_only, line)

    return line


def main() -> int:
    text = PAPER.read_text(encoding="utf-8")
    lines = text.split("\n")

    counts = {
        'behavioral_specification': 0,
        'behavioral_spec': 0,
        'specification_with_article': 0,
        'spec_with_article': 0,
        'no_context_condition': 0,
        'all_facts_condition': 0,
        'retrieval_only_condition': 0,
        'facts_only_condition': 0,
    }

    new_lines = []
    for line in lines:
        if is_protected_line(line):
            new_lines.append(line)
            continue

        # Mask italic-quoted + code spans
        masked, placeholders = mask_protected_spans(line)

        # Apply transforms
        masked = cap_specification(masked, counts)
        masked = cap_conditions(masked, counts)

        # Unmask
        new_lines.append(unmask(masked, placeholders))

    new_text = "\n".join(new_lines)

    if new_text != text:
        PAPER.write_text(new_text, encoding="utf-8")
        print("Applied changes:")
    else:
        print("No changes (already clean)")

    total = sum(counts.values())
    for label, n in counts.items():
        if n:
            print(f"  {label}: {n}")
    print(f"Total replacements: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
