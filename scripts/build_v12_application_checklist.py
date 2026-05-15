"""Build a status checklist of every v12 Aarik comment for mechanical tracking.

Reads the verbatim extract at docs/reviews/v12_aarik_comments_20260513.md and
emits a per-comment row with status, section, anchored text, and the tag
assigned in the tagged review.

Status legend:
  PENDING       — not yet addressed
  APPLIED       — edit made; record what file/section
  DEFERRED      — flagged for after-launch
  N/A           — empty comment or sympathetic note (no action)
  NEEDS-DECISION — requires Aarik input

This file is the source of truth for completeness. Rebuild after each batch.
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
SRC = REPO / "docs" / "reviews" / "v12_aarik_comments_20260513.md"
OUT = REPO / "docs" / "reviews" / "v12_application_checklist_20260513.md"

# Tag assignments by comment number (from tagged review file).
# Multiple tags per comment allowed; first is primary.
TAGS: dict[int, list[str]] = {
    1:  ["TABLE-CLEANUP", "BOLD-LESS"],
    2:  ["ABSTRACT-ALIGN"],
    3:  ["TERM-CAP"],
    4:  ["REPHRASE"],
    5:  ["ABSTRACT-ALIGN"],
    6:  ["HYP-PROVENANCE"],
    7:  ["REPHRASE"],
    8:  ["TERM-CAP", "GLOBAL"],
    9:  ["LABEL-FACTS", "GLOBAL"],
    10: ["ABSTENTION-FRAME", "RUBRIC-LANG"],
    11: ["RUBRIC-LANG"],
    12: ["RUBRIC-LANG"],
    13: ["LABEL-COND", "GLOBAL"],
    14: ["TABLE-CLEANUP", "STRUCTURE-LIST"],
    15: ["CUT-FILLER"],
    16: ["REPHRASE"],
    17: ["REPHRASE", "ABSTRACT-ALIGN"],
    18: ["REPHRASE"],
    19: ["ABSTRACT-ALIGN"],
    20: ["§1.3-DENSE"],
    21: ["§1.3-DENSE", "BOLD-LESS"],
    22: ["TERM-CAP"],
    23: ["STATS-CLARIFY"],
    24: ["BOLD-LESS"],
    25: ["CUT-FILLER"],
    26: ["TERM-DEF"],
    27: ["N/A"],
    28: ["LABEL-FACTS", "TERM-CAP"],
    29: ["TERM-CAP"],
    30: ["TERM-CAP"],
    31: ["TERM-CAP"],
    32: ["REPHRASE"],
    33: ["REPHRASE"],
    34: ["TERM-DEF"],
    35: ["TERM-CAP"],
    36: ["LABEL-FACTS"],
    37: ["TERM-DEF"],
    38: ["N/A"],
    39: ["TERM-DEF"],
    40: ["REPHRASE"],
    41: ["REPHRASE", "§1.4-LEAD"],
    42: ["WORD-CHOICE"],
    43: ["LABEL-COND"],
    44: ["CUT-FILLER"],
    45: ["CUT-FILLER"],
    46: ["TERM-DEF"],
    47: ["§1.4-LEAD", "ABSTRACT-ALIGN"],
    48: ["§1.4-LEAD", "ABSTRACT-ALIGN"],
    49: ["REPHRASE"],
    50: ["CUT-FILLER"],
    51: ["CUT-PARENTHETICAL"],
    52: ["REPHRASE"],
    53: ["N/A"],
    54: ["CUT-FILLER"],
    55: ["REPHRASE"],
    56: ["N/A"],
    57: ["REPHRASE"],
    58: ["REPHRASE"],
    59: ["N/A"],
    60: ["REPHRASE"],
    61: ["CUT-FILLER"],
    62: ["FUTURE-RESEARCH"],
    63: ["N/A"],
    64: ["REPHRASE"],
    65: ["FOOTNOTE-CLASH"],
    66: ["REPHRASE"],
    67: ["MOVE-APPENDIX"],
    68: ["MOVE-APPENDIX"],
    69: ["REPHRASE"],
    70: ["TABLE-CLEANUP"],
    71: ["MOVE-APPENDIX"],
    72: ["REPHRASE"],
    73: ["REPHRASE"],
    74: ["REPHRASE"],
    75: ["CUT-FILLER"],
    76: ["REPHRASE"],
    77: ["N/A"],
    78: ["REPHRASE"],
    79: ["REPHRASE"],
    80: ["REPHRASE"],
    81: ["REPHRASE"],
    82: ["REPHRASE"],
    83: ["STATS-CLARIFY"],
    84: ["N/A"],
    85: ["TERM-CAP", "LABEL-COND"],
    86: ["REPHRASE"],
    87: ["REPHRASE"],
    88: ["TABLE-WIDTH"],
    89: ["CASE-COND"],
    90: ["TABLE-WIDTH"],
    91: ["FUTURE-RESEARCH"],
    92: ["REPHRASE"],
    93: ["TABLE-CLEANUP"],
    94: ["REPHRASE"],
    95: ["LINK-REF"],
    96: ["LINK-REF"],
    97: ["RUBRIC-DEFINE"],
    98: ["RUBRIC-LANG"],
    99: ["RUBRIC-DEFINE"],
    100: ["CUT-FILLER"],
    101: ["WORD-CHOICE"],
    102: ["WORD-CHOICE"],
    103: ["ABSTENTION-FRAME"],
    104: ["REPHRASE"],
    105: ["STATS-CLARIFY"],
    106: ["STATS-CLARIFY"],
    107: ["MOVE-APPENDIX"],
    108: ["REPHRASE"],
    109: ["TABLE-CLEANUP"],
    110: ["REPHRASE"],
    111: ["LABEL-FACTS"],
    112: ["LABEL-COND"],
    113: ["STATS-CLARIFY"],
    114: ["STATS-CLARIFY"],
    115: ["RUBRIC-DEFINE"],
    116: ["RUBRIC-LANG"],
    117: ["TABLE-WIDTH"],
    118: ["REPHRASE"],
    119: ["N/A"],
    120: ["REPHRASE"],
    121: ["BOLD-LESS"],
    122: ["FUTURE-RESEARCH"],
    123: ["CUT-FILLER"],
    124: ["STATS-CLARIFY"],
    125: ["MOVE-APPENDIX"],
    126: ["CUT-FILLER"],
    127: ["REPHRASE"],
    128: ["CUT-FILLER"],
    129: ["BOLD-LESS"],
    130: ["N/A"],
    131: ["N/A"],
    132: ["BOLD-LESS"],
    133: ["REPHRASE"],
    134: ["N/A"],
    135: ["LINK-REF"],
    136: ["REPHRASE"],
    137: ["REPHRASE"],
    138: ["BOLD-LESS"],
    139: ["REPHRASE"],
    140: ["STRUCTURE-LIST"],
    141: ["TABLE-CLEANUP", "STRUCTURE-LIST"],
    142: ["FOOTNOTE-CLASH"],
    143: ["FIGURE-PLACEMENT"],
    144: ["FIGURE-PLACEMENT"],
    145: ["BOLD-MORE"],
    146: ["BOLD-MORE"],
    147: ["REPHRASE"],
    148: ["REPHRASE"],
    149: ["TABLE-CLEANUP", "LABEL-COND"],
    150: ["CITATION"],
    151: ["REPHRASE"],
    152: ["WORD-CHOICE"],
    153: ["N/A"],
    154: ["REPHRASE"],
    155: ["STRUCTURE-LIST"],
    156: ["ABSTENTION-FRAME"],
    157: ["WORD-CHOICE"],
    158: ["TABLE-CLEANUP", "STRUCTURE-LIST"],
    159: ["WORD-CHOICE"],
    160: ["WORD-CHOICE"],
    161: ["WORD-CHOICE"],
    162: ["CUT-FILLER"],
    163: ["REPHRASE"],
    164: ["CUT-FILLER"],
    165: ["WORD-CHOICE"],
    166: ["N/A"],
    167: ["TABLE-WIDTH"],
    168: ["N/A"],
    169: ["REPHRASE"],
    170: ["TABLE-CLEANUP"],
    171: ["BOLD-LESS"],
    172: ["TABLE-CLEANUP"],
    173: ["REPHRASE"],
    174: ["TABLE-CLEANUP"],
    175: ["TABLE-WIDTH"],
    176: ["CITATION"],
    177: ["N/A"],
    178: ["TABLE-WIDTH"],
    179: ["BOLD-LESS"],
    180: ["STRUCTURE-LIST"],
    181: ["BOLD-LESS", "REPHRASE"],
    182: ["REPHRASE"],
    183: ["TABLE-WIDTH"],
    184: ["REPHRASE"],
    185: ["FUTURE-RESEARCH", "LETTA-EMPHASIS"],
    186: ["BOLD-LESS"],
    187: ["CUT-PARENTHETICAL"],
    188: ["STATS-CLARIFY"],
    189: ["BOLD-LESS"],
    190: ["BOLD-LESS"],
    191: ["EVIDENTIARY-BAR"],
    192: ["REPHRASE"],
    193: ["BOLD-LESS", "EVIDENTIARY-BAR"],
    194: ["EVIDENTIARY-BAR", "FUTURE-RESEARCH"],
    195: ["STATS-CLARIFY", "LABEL-FACTS"],
    196: ["EVIDENTIARY-BAR"],
    197: ["APPENDIX-CLEANUP"],
    198: ["APPENDIX-CLEANUP"],
    199: ["APPENDIX-CLEANUP"],
    200: ["APPENDIX-CLEANUP"],
    201: ["WORD-CHOICE"],
    202: ["APPENDIX-CLEANUP"],
    203: ["TABLE-WIDTH"],
    204: ["TABLE-WIDTH"],
    205: ["TABLE-WIDTH"],
    206: ["TABLE-WIDTH"],
    207: ["FORMAT-LANDSCAPE"],
    208: ["APPENDIX-CLEANUP"],
    209: ["APPENDIX-CLEANUP"],
    210: ["LETTA-EMPHASIS"],
    211: ["GLOSSARY-REVIEW"],
}


def main() -> int:
    text = SRC.read_text(encoding="utf-8")
    # Parse the verbatim file into per-comment records
    blocks = re.split(r"^---\s*$", text, flags=re.M)
    records = []
    for blk in blocks:
        m_num = re.search(r"^## C(\d{3})\s+\(comment-id\s+(\d+)\)", blk, flags=re.M)
        if not m_num:
            continue
        cnum = int(m_num.group(1))
        cid = m_num.group(2)
        m_sect = re.search(r"^\*\*Section:\*\*\s*(.+)$", blk, flags=re.M)
        section = m_sect.group(1) if m_sect else ""
        m_anc = re.search(r"^\*\*Anchored text:\*\*\s*(.+)$", blk, flags=re.M)
        anchored = m_anc.group(1) if m_anc else ""
        m_com = re.search(r"^\*\*Comment:\*\*\s*(.*)$", blk, flags=re.M | re.S)
        comment = m_com.group(1).strip() if m_com else ""
        records.append({
            "num": cnum,
            "cid": cid,
            "section": section,
            "anchored": anchored[:120],
            "comment": comment[:200].replace("\n", " "),
            "tags": TAGS.get(cnum, ["UNTAGGED"]),
        })
    records.sort(key=lambda r: r["num"])

    # Emit checklist
    lines = []
    lines.append("# v12 Application Checklist")
    lines.append("")
    lines.append(f"Total comments: {len(records)}. Source verbatim: `v12_aarik_comments_20260513.md`.")
    lines.append("")
    lines.append("Status legend: `PENDING` `APPLIED` `DEFERRED` `N/A` `NEEDS-DECISION`")
    lines.append("")
    lines.append("Update the Status column in place as each comment is addressed.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("| C# | Status | Tags | Section | Anchor / Comment |")
    lines.append("|---|---|---|---|---|")
    for r in records:
        status = "N/A" if "N/A" in r["tags"] else "PENDING"
        tags = ", ".join(r["tags"])
        # Strip the title prefix from section for compact display
        sect = r["section"]
        sect = re.sub(r"^Beyond Recall:[^›]+›\s*", "", sect)
        anch = r["anchored"][:60].replace("|", "\\|")
        com = r["comment"][:120].replace("|", "\\|")
        if anch and anch.strip():
            display = f"_{anch}_ — {com}"
        else:
            display = com
        lines.append(f"| C{r['num']:03d} | {status} | {tags} | {sect[:80]} | {display} |")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(records)} rows to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
