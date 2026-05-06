"""Smoke tests for the Beyond Recall study MCP tools.

Tests the tool functions directly (no MCP wire protocol). Goal: confirm the
underlying queries and aggregations work against the real study data on disk.

Run:
    python test_smoke.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import tools  # noqa: E402
import resources  # noqa: E402


def _ok(label: str) -> None:
    print(f"  PASS  {label}")


def _fail(label: str, detail: str) -> None:
    print(f"  FAIL  {label}: {detail}")
    sys.exit(1)


def test_list_subjects() -> None:
    rows = tools.list_subjects()
    if len(rows) != 14:
        _fail("list_subjects returns 14 rows", f"got {len(rows)}")
    if rows[0]["subject"] != "ebers":
        _fail("first subject is ebers (lowest C5)", f"got {rows[0]['subject']}")
    needed = {"subject", "results_dir", "data_dir", "c5_baseline", "c4a_facts_plus_spec", "delta_spec", "low_baseline"}
    if not needed.issubset(rows[0].keys()):
        _fail("list_subjects schema", f"missing {needed - set(rows[0].keys())}")
    _ok(f"list_subjects: {len(rows)} subjects, first {rows[0]['subject']}")


def test_get_subject_score_seacole_c4a() -> None:
    res = tools.get_subject_score("seacole", "C4a")
    if "error" in res:
        _fail("get_subject_score seacole C4a", res["error"])
    if res["mean"] is None:
        _fail("get_subject_score mean", "mean is None")
    # Per DATA_REFERENCE §1, seacole C4a 5-judge primary = 2.59 (within rounding tolerance)
    if not (2.30 <= res["mean"] <= 2.85):
        _fail("seacole C4a in expected range", f"mean={res['mean']}")
    if len(res["per_judge"]) < 4:
        _fail("seacole C4a per-judge coverage", f"only {len(res['per_judge'])} judges")
    _ok(
        f"get_subject_score(seacole, C4a) = {res['mean']:.3f} "
        f"across {len(res['per_judge'])} judges over {res['n_questions']} qids"
    )
    print(f"        per_judge keys: {list(res['per_judge'].keys())}")
    print(f"        condition variant: {res['condition_variant_used']}")


def test_get_subject_score_short_form_disambiguation() -> None:
    # Unknown subject should return error with alternatives.
    res_bad = tools.get_subject_score("not_a_subject_xyz", "C4a")
    if "error" not in res_bad:
        _fail("unknown subject should error", "no error returned")
    if not res_bad.get("alternatives"):
        _fail("unknown subject should provide alternatives", str(res_bad))
    # Hamerton C5 should work via direct directory name.
    res2 = tools.get_subject_score("hamerton", "C5")
    if "error" in res2:
        _fail("hamerton C5", res2["error"])
    _ok(f"get_subject_score(hamerton, C5) = {res2['mean']}")


def test_search_study() -> None:
    # Use FTS5-friendly query (no hyphens, no operators).
    res = tools.search_study("Wilcoxon gradient", mode="fts", limit=5)
    valid = [r for r in res if "error" not in r]
    if not valid:
        _fail("search_study fts wilcoxon", str(res[:1]))
    if not any(r.get("filename") for r in valid):
        _fail("search_study returns filenames", f"first={valid[0]}")
    _ok(f"search_study fts: {len(valid)} hits, first={valid[0].get('filename')}")


def test_get_provenance() -> None:
    res = tools.get_provenance("Wilcoxon p value gradient", limit=5)
    if not res:
        _fail("get_provenance returns rows", "empty")
    valid = [r for r in res if "error" not in r]
    if not valid:
        _fail("get_provenance has non-error rows", str(res[:2]))
    fnames = {r.get("filename") for r in valid}
    if not fnames & {"PROVENANCE_INDEX.md", "DATA_REFERENCE.md"}:
        _fail("get_provenance hits target files", f"got {fnames}")
    _ok(f"get_provenance: {len(valid)} target rows, files={fnames}")


def test_list_anchor_crossings() -> None:
    res = tools.list_anchor_crossings("C5_to_C4a", min_jump=2, limit=10)
    if not res or "error" in res[0]:
        _fail("list_anchor_crossings C5_to_C4a", str(res[:1]))
    needed = {"subject", "qid", "jump", "pre_band", "post_band"}
    if not needed.issubset(res[0].keys()):
        _fail("list_anchor_crossings schema", f"missing {needed - set(res[0].keys())}")
    enriched = [r for r in res if r.get("question_text")]
    _ok(
        f"list_anchor_crossings: {len(res)} rows, "
        f"{len(enriched)} enriched with held-out text"
    )


def test_paper_resources() -> None:
    secs = tools.list_paper_sections()
    if not secs:
        _fail("list_paper_sections", "empty")
    target = next((s for s in secs if s["id"] == "3.6.2"), None)
    if not target:
        # fallback if paper structure shifts; just take first numeric id
        target = next((s for s in secs if s["id"][0].isdigit()), None)
    if not target:
        _fail("paper section index", "no numeric-id sections found")
    res = tools.get_paper_section(target["id"])
    if "error" in res or not res.get("text"):
        _fail("get_paper_section", str(res)[:200])
    rsrc = resources.read_resource(resources.section_uri(target["id"]))
    if rsrc.startswith("Error:"):
        _fail("resources.read_resource", rsrc)
    _ok(
        f"paper sections: {len(secs)} indexed; section {target['id']} "
        f"({target['title'][:50]!r}) has {len(res['text'])} chars"
    )


def main() -> None:
    print("Beyond Recall study MCP smoke tests")
    print("=" * 60)
    test_list_subjects()
    test_get_subject_score_seacole_c4a()
    test_get_subject_score_short_form_disambiguation()
    test_search_study()
    test_get_provenance()
    test_list_anchor_crossings()
    test_paper_resources()
    print("=" * 60)
    print("ALL SMOKE TESTS PASSED")


if __name__ == "__main__":
    main()
