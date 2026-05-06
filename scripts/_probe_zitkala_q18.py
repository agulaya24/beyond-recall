"""One-shot probe: does Zitkala-Sa Q18 produce a spec-induced C3 refusal
under the broad rule, across any of the 5 memory systems? The author's
motivating question was Q18 ventriloquism; Zitkala-Sa is outside the low-
baseline cutoff that P0-5 used (C5=2.34), so she is absent from the 81-case set.
This probe confirms whether rerunning the audit with her included would
surface Q18.
"""
import json
import re
from pathlib import Path

RESULTS = Path(__file__).resolve().parent.parent / "results"
REFUSAL_PATTERNS = [
    r"\bI (?:cannot|can't|don't|do not) (?:know|predict|have|be sure)",
    r"\bI (?:have )?no (?:information|data|knowledge|facts)\b",
    r"\bwithout (?:more|additional|the) (?:information|context|facts)\b",
    r"\bThe retrieved facts (?:do not|don't) (?:contain|include|provide|mention|specify)",
    r"\bI must acknowledge\b",
    r"\bcannot determine\b",
    r"\bunable to (?:determine|predict|specify)\b",
    r"\bno specific (?:information|details)\b",
]
REFUSAL_RE = re.compile("|".join(REFUSAL_PATTERNS), re.IGNORECASE)

SYSTEMS = ["mem0", "letta", "supermemory", "zep", "baselayer"]
zdir = RESULTS / "global_zitkala_sa"

summary = []
for system in SYSTEMS:
    if system == "baselayer":
        p = zdir / "baselayer_results.json"
        c1n, c3n = "C1_baselayer", "C3_baselayer"
    else:
        p_fp = zdir / f"{system}_fullpipeline_results.json"
        p_alt = zdir / f"{system}_results.json"
        if p_fp.exists():
            p = p_fp
            c1n, c3n = f"C1_{system}_fp", f"C3_{system}_fp"
        else:
            p = p_alt
            c1n, c3n = f"C1_{system}", f"C3_{system}"
    if not p.exists():
        print(f"[SKIP] {system}: {p} missing")
        continue
    data = json.load(p.open(encoding="utf-8"))
    for rec in data:
        if str(rec.get("question_id")) != "18":
            continue
        resp = rec.get("responses") or {}

        def text_of(key):
            v = resp.get(key)
            if isinstance(v, dict):
                return v.get("text") or v.get("response") or ""
            return str(v or "")

        t1 = text_of(c1n)
        t3 = text_of(c3n)
        c1_ref = bool(REFUSAL_RE.search(t1))
        c3_ref = bool(REFUSAL_RE.search(t3))
        spec_induced = c3_ref and not c1_ref
        summary.append({
            "system": system,
            "c1_refusal": c1_ref,
            "c3_refusal": c3_ref,
            "spec_induced": spec_induced,
            "question_text": rec.get("question_text", ""),
            "held_out": (rec.get("held_out_passage") or "")[:300],
            "c3_response_head": t3[:500],
        })

print(f"\nZitkala-Sa Q18 question: {summary[0]['question_text'] if summary else 'N/A'}")
print(f"Held-out: {summary[0]['held_out'] if summary else 'N/A'}\n")
print("| system | c1_refusal | c3_refusal | spec_induced |")
print("|---|---|---|---|")
for r in summary:
    print(f"| {r['system']} | {r['c1_refusal']} | {r['c3_refusal']} | {r['spec_induced']} |")
print()
for r in summary:
    if r["spec_induced"]:
        print(f"--- {r['system']} C3 (SPEC-INDUCED REFUSAL) ---")
        print(r["c3_response_head"])
        print()
