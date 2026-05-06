"""Audit script: re-derive subset share-zero / share-le-1 stats for v11.8 §4.4.1 footnote."""

import json
import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path

REPO = Path("C:/Users/Aarik/Anthropic/memory-study-repo")
RESULTS = REPO / "results"
DATA = REPO / "data"

CONTROLLED_SYSTEMS = ["baselayer", "mem0", "letta", "supermemory", "zep"]
COMMERCIAL_SYSTEMS = ["mem0", "letta", "supermemory", "zep"]
SUBJECTS_14 = [
    "hamerton", "global_augustine", "global_babur", "global_bernal_diaz",
    "global_cellini", "global_ebers", "global_equiano", "global_fukuzawa",
    "global_keckley", "global_rousseau", "global_seacole", "global_sunity_devee",
    "global_yung_wing", "global_zitkala_sa",
]
SUBJECTS_13_GLOBALS = [s for s in SUBJECTS_14 if s != "hamerton"]

ZEP_METADATA_KEYS = {"communities", "context", "episodes", "nodes", "sagas", "themes"}
ZEP_FACT_PATTERN = re.compile(r"\bfact=('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")")


def normalize(s):
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s.rstrip(".;").strip()


def load_battery_qids(subject):
    if subject == "hamerton":
        bp = DATA / "hamerton" / "battery.json"
    else:
        bp = RESULTS / subject / "battery_v2.json"
    bat = json.loads(bp.read_text(encoding="utf-8"))
    qs = bat.get("questions", []) if isinstance(bat, dict) else bat
    bp_qids = []
    for q in qs:
        if q.get("tier") == "behavioral_prediction":
            qid = q.get("question_id") or q.get("id") or q.get("qid")
            bp_qids.append(qid)
    return set(bp_qids)


def load_retrieval(subject, system):
    if subject == "hamerton":
        rp = RESULTS / "hamerton" / f"{system}_retrieval.json"
    else:
        rp = RESULTS / subject / f"{system}_retrieval.json"
    if not rp.exists():
        return {}
    raw = json.loads(rp.read_text(encoding="utf-8"))
    out = {}
    if isinstance(raw, list):
        entries = raw
    else:
        entries = list(raw.values())
    for entry in entries:
        qid = entry.get("question_id") or entry.get("qid") or entry.get("id")
        results = entry.get("fact_texts") or entry.get("results", entry.get("retrieved", []))
        facts = []
        for r in results:
            if isinstance(r, dict):
                t = r.get("text") or r.get("fact") or r.get("content") or ""
            else:
                t = str(r)
            if not t:
                continue
            if system == "zep":
                # extract fact='...' patterns
                matches = ZEP_FACT_PATTERN.findall(t)
                for m in matches:
                    fact = m[1:-1]
                    facts.append(fact)
            else:
                facts.append(t)
        out[qid] = facts
    return out


def main():
    cuts = {
        "all_14_all_pairs": (SUBJECTS_14, list(combinations(CONTROLLED_SYSTEMS, 2))),
        "13_globals_all_pairs": (SUBJECTS_13_GLOBALS, list(combinations(CONTROLLED_SYSTEMS, 2))),
        "all_14_commercial": (SUBJECTS_14, list(combinations(COMMERCIAL_SYSTEMS, 2))),
        "13_globals_commercial": (SUBJECTS_13_GLOBALS, list(combinations(COMMERCIAL_SYSTEMS, 2))),
    }

    for cut_name, (subjects, pairs) in cuts.items():
        n_total = 0
        n_zero = 0
        n_le1 = 0
        for subject in subjects:
            try:
                bp_qids = load_battery_qids(subject)
            except Exception as e:
                print(f"FAIL {subject}: {e}")
                continue
            sys_facts = {}
            for sys in CONTROLLED_SYSTEMS:
                sys_facts[sys] = load_retrieval(subject, sys)
            for sys_a, sys_b in pairs:
                fa = sys_facts.get(sys_a, {})
                fb = sys_facts.get(sys_b, {})
                # Need to use common qids across all 5 systems for this subject (matching analyze_retrieval_overlap.py logic)
                common_qids = bp_qids
                for sys in CONTROLLED_SYSTEMS:
                    common_qids = common_qids & set(sys_facts.get(sys, {}).keys())
                for qid in common_qids:
                    a = set(fa.get(qid, []))  # RAW, not normalized (matches canonical)
                    b = set(fb.get(qid, []))
                    n_total += 1
                    intersect_size = len(a & b)
                    if intersect_size == 0:
                        n_zero += 1
                    if intersect_size <= 1:
                        n_le1 += 1
        print(f"{cut_name}: n={n_total}, share_zero={n_zero/n_total*100:.2f}%, share_le1={n_le1/n_total*100:.2f}%")


if __name__ == "__main__":
    main()
