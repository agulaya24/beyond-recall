#!/usr/bin/env python3
"""Make every plain-text section pointer (e.g. "§4.4", "§3.3.6") a clickable
\\hyperref in beyond_recall_body.tex.

Pandoc renders most cross-references as literal "§X.Y" text. This pass builds
a section-number -> label map from the headings in body.tex itself (not by
predicting pandoc's slug rules -- those are unreliable, see fix_body_anchors.py),
then wraps each plain "§X.Y" in \\hyperref[label]{§X.Y}.

Rules:
  - Build the map by scanning every \\(sub)*section{NUMBER TITLE}\\label{SLUG}.
  - Replace longest-number-first so "§4.4.1" matches before "§4.4".
  - Never touch a "§..." already inside \\hyperref{ } or \\hyperlink{ }.
  - Any "§X.Y" whose number is not in the map is LEFT AS PLAIN TEXT and
    reported -- no invented targets, no dead links.
  - Idempotent: a "§X.Y" already wrapped is skipped.
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

BODY = Path(__file__).resolve().parents[1] / "build" / "beyond_recall_body.tex"


def build_number_to_label(text: str) -> dict[str, str]:
    """Map section-number string -> \\label slug, parsed from headings."""
    num_to_label: dict[str, str] = {}
    # Heading: \section{ ... }\label{slug}  (title text may span newlines)
    pat = re.compile(
        r"\\(?:sub)*section\{(?P<title>.*?)\}\s*\\label\{(?P<slug>[^}]+)\}",
        re.DOTALL,
    )
    for m in pat.finditer(text):
        title = re.sub(r"\s+", " ", m.group("title")).strip()
        slug = m.group("slug")
        # Leading number token: "1.", "1.3", "4.4.1", "Appendix A." etc.
        nm = re.match(r"(?P<num>\d+(?:\.\d+)*)\.?\s", title)
        if nm:
            num = nm.group("num")
            num_to_label.setdefault(num, slug)
        # Appendix headings: "Appendix A. ..." / "Appendix B.3 ..."
        am = re.match(r"Appendix\s+(?P<ap>[A-Z](?:\.\d+)*)", title)
        if am:
            num_to_label.setdefault("Appendix " + am.group("ap"), slug)
    return num_to_label


def wrap_section_refs(text: str, num_to_label: dict[str, str]) -> tuple[str, int, set[str]]:
    """Wrap plain §X.Y refs. Returns (new_text, n_wrapped, unmatched_numbers)."""
    unmatched: set[str] = set()
    n_wrapped = 0

    # Match "§" + a dotted number, NOT already preceded by an open hyperref/
    # hyperlink brace context. We approximate "already linked" by checking the
    # 12 chars before the match for "hyperref[" or "hyperlink{".
    ref_pat = re.compile(r"§(\d+(?:\.\d+)*)")

    # Detect "§ sits inside a macro's optional [...] argument" (e.g.
    # \caption[ ... §X.Y ... ]{...}). A \hyperref[label]{...} placed inside
    # such an optional arg closes it prematurely -- see the Figure 4.1
    # caption bug. Heuristic: scan backward from the match to the nearest
    # paragraph break; if we see an unbalanced "\word[" (an open optional
    # arg with no matching "]" before the match), the § is inside it.
    opt_arg_pat = re.compile(r"\\[A-Za-z@]+\[")

    def inside_optional_arg(idx: int) -> bool:
        seg = text[max(0, idx - 600):idx]
        # Trim to the current paragraph so we do not scan across blank lines.
        para_break = seg.rfind("\n\n")
        if para_break != -1:
            seg = seg[para_break + 2:]
        depth = 0
        i = len(seg) - 1
        while i >= 0:
            ch = seg[i]
            if ch == "]":
                depth += 1
            elif ch == "[":
                if depth > 0:
                    depth -= 1
                else:
                    # Unbalanced "["; is it a macro's optional-arg opener?
                    if opt_arg_pat.search(seg, max(0, i - 40), i + 1):
                        return True
            i -= 1
        return False

    out: list[str] = []
    last = 0
    for m in ref_pat.finditer(text):
        start, end = m.span()
        num = m.group(1)
        pre = text[max(0, start - 14):start]
        # Skip if this § sits inside an existing link target/label or is the
        # visible text of an existing \hyperref[...]{§...}.
        if "hyperref[" in pre or "hyperlink{" in pre or pre.endswith("{"):
            continue
        # Skip if this § sits inside a macro's optional [...] argument.
        if inside_optional_arg(start):
            continue
        label = num_to_label.get(num)
        if not label:
            unmatched.add(num)
            continue
        out.append(text[last:start])
        out.append(r"\hyperref[" + label + r"]{§" + num + "}")
        last = end
        n_wrapped += 1
    out.append(text[last:])
    return "".join(out), n_wrapped, unmatched


def main() -> int:
    text = BODY.read_text(encoding="utf-8")
    num_to_label = build_number_to_label(text)
    print(f"Section-number -> label map: {len(num_to_label)} entries")

    new_text, n_wrapped, unmatched = wrap_section_refs(text, num_to_label)
    print(f"Wrapped {n_wrapped} plain section pointers in \\hyperref.")

    if unmatched:
        print(f"\nUNMATCHED ({len(unmatched)}) -- left as plain text, no target found:")
        for num in sorted(unmatched, key=lambda s: [int(x) for x in s.split(".")]):
            print(f"  §{num}")
    else:
        print("All section pointers matched a heading label.")

    BODY.write_text(new_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
