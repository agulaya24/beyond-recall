"""Step 1: Generate named full-stack specs (~40K chars) for Hamerton, Ebers, Babur.

- Ebers, Babur: read spec_production.md, replace "this person" -> Surname
  (case-insensitive; handle possessive variants). Preserve pronouns (they/them/their).
- Hamerton: concat anchors_v4 + core_v4 + predictions_v4 + brief_v5_clean with a
  prepended named header. Do not convert pronouns.

Outputs: _letta_rerun/fullstack_named/{subject}_spec_fullstack_named.md
"""
import os
import re

REPO = r"C:\Users\Aarik\Anthropic\memory-study-repo"
OUT_DIR = os.path.join(REPO, r"docs\research\_letta_rerun\fullstack_named")
os.makedirs(OUT_DIR, exist_ok=True)


def name_substitute(text: str, surname: str) -> str:
    """Replace 'this person' and 'this person's' variants with surname / surname's.

    Preserves capitalization at sentence start (e.g. "This person" at start of
    sentence -> "Surname") and handles curly/straight apostrophes.
    """
    # Possessive forms first so they don't collide with bare form replacement.
    # Handle both straight (') and curly ('’') apostrophes.
    patterns = [
        (r"\bthis person’s\b", f"{surname}’s"),
        (r"\bThis person’s\b", f"{surname}’s"),
        (r"\bthis person's\b",      f"{surname}'s"),
        (r"\bThis person's\b",      f"{surname}'s"),
        (r"\bthis person\b",        surname),
        (r"\bThis person\b",        surname),
    ]
    for pat, repl in patterns:
        text = re.sub(pat, repl, text)
    return text


def make_ebers_babur_spec(subject: str, surname: str) -> str:
    src = os.path.join(REPO, "data", "global_subjects", subject, "spec_production.md")
    with open(src, encoding="utf-8") as f:
        text = f.read()
    text = name_substitute(text, surname)
    header = f"# BEHAVIORAL SPECIFICATION: {surname.upper()}\n\n"
    # The spec_production file begins with '# ANCHORS' header for the first layer.
    # We keep that structure and just prepend the subject header.
    return header + text


def make_hamerton_spec() -> str:
    """Concat 4 layer files with a named header. Pronouns preserved (they/them/their)."""
    base = os.path.join(REPO, "data", "hamerton", "spec")
    layers = [
        ("anchors_v4.md",       "# ANCHORS LAYER\n\n"),
        ("core_v4.md",          "# CORE LAYER\n\n"),
        ("predictions_v4.md",   "# PREDICTIONS LAYER\n\n"),
        ("brief_v5_clean.md",   "# UNIFIED BRIEF\n\n"),
    ]
    parts = ["# BEHAVIORAL SPECIFICATION: PHILIP GILBERT HAMERTON\n\n"]
    for fname, section_header in layers:
        with open(os.path.join(base, fname), encoding="utf-8") as f:
            parts.append(section_header)
            parts.append(f.read().rstrip())
            parts.append("\n\n---\n\n")
    return "".join(parts).rstrip() + "\n"


def main():
    # Hamerton
    ham = make_hamerton_spec()
    out = os.path.join(OUT_DIR, "hamerton_spec_fullstack_named.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(ham)
    print(f"hamerton : {len(ham):,} chars -> {out}")

    # Ebers
    eb = make_ebers_babur_spec("ebers", "Ebers")
    out = os.path.join(OUT_DIR, "ebers_spec_fullstack_named.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(eb)
    print(f"ebers    : {len(eb):,} chars -> {out}")

    # Babur
    bb = make_ebers_babur_spec("babur", "Babur")
    out = os.path.join(OUT_DIR, "babur_spec_fullstack_named.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(bb)
    print(f"babur    : {len(bb):,} chars -> {out}")

    # Quick post-check: count residual 'this person' substrings (should be 0).
    for subj in ("hamerton", "ebers", "babur"):
        p = os.path.join(OUT_DIR, f"{subj}_spec_fullstack_named.md")
        with open(p, encoding="utf-8") as f:
            t = f.read()
        n = len(re.findall(r"this person", t, re.I))
        print(f"  {subj}: residual 'this person' matches = {n}")


if __name__ == "__main__":
    main()
