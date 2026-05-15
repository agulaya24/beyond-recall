"""Rerun missing GPT-4o and GPT-5.4 judges on Franklin C4 + Bernal Diaz C9.

Fills two known partial-panel cells caught by v11.9.11 review:

  - Franklin C4 (facts only) was scored by 4 legacy judges (Haiku, Sonnet,
    Opus, Gemini) but never by GPT-4o or GPT-5.4. This run brings Franklin's
    C4 to a 6-judge complete set (4 legacy + GPT-4o + GPT-5.4 = 5-of-5
    primary + Gemini sensitivity).

  - Bernal Diaz C9 (raw corpus + Spec) was scored by Haiku, Sonnet, Opus
    cleanly, but the GPT-4o and GPT-5.4 batches 429-errored across all 39
    questions (parse_failure=True, score=0). This run reruns the 78 missing
    judge calls so the 5-judge primary aggregate is complete.

Output: appends to existing per-judge JSON files; idempotent on
(question_id, condition) pairs already present.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import httpx

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent

JUDGES = {
    "gpt4o":  {"provider": "openai", "model": "gpt-4o-2024-08-06"},
    "gpt54":  {"provider": "openai", "model": "gpt-5.4"},
}

# Each target: (response_file, condition_to_judge, output_file_template, response_in_responses_dict_under_key)
TARGETS = [
    {
        "name": "Franklin C4 (gpt4o + gpt54)",
        "response_file": REPO / "results" / "franklin_legacy_20260411" / "results.json",
        "condition": "C4_factdump",
        "out_dir": REPO / "results" / "franklin_legacy_20260411" / "analysis",
        "out_filename_template": "{judge}_judgments.json",  # existing files; append
        "score_field_template": "{judge}_score",  # legacy schema: 'haiku_score', 'gpt4o_score', etc.
        "use_wide_schema": True,
    },
    {
        "name": "Bernal Diaz C9 (gpt4o + gpt54 rerun)",
        "response_file": REPO / "results" / "global_bernal_diaz" / "c8_c9_results.json",
        "condition": "C9_raw_corpus_plus_spec",
        "out_dir": REPO / "results" / "global_bernal_diaz",
        "out_filename_template": "c8_c9_judgments_{judge}.json",
        "score_field_template": "score",  # current schema: 'score'
        "use_wide_schema": False,
    },
]


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def load_env() -> None:
    for k in ["OPENAI_API_KEY"]:
        r = subprocess.run(
            ["powershell", "-Command",
             f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
            capture_output=True, text=True,
        )
        v = r.stdout.strip()
        if v:
            os.environ[k] = v


def judge_prompt(held_out: str, response_text: str) -> str:
    return ("You are evaluating whether a response about a person PREDICTED "
            "what actually happened.\n\n"
            "=== HELD-OUT GROUND TRUTH ===\n" + held_out + "\n\n"
            "=== RESPONSE ===\n" + response_text[:1500] + "\n\n"
            "Rate 1-5:\n"
            "5=Predicts specific outcome\n"
            "4=General direction correct\n"
            "3=Right domain wrong outcome\n"
            "2=Wrong prediction\n"
            "1=Refuses or off-base\n\n"
            "Respond with ONLY a single digit (1-5).")


def parse_score(text: str) -> int:
    if not text:
        return 0
    m = re.search(r"[1-5]", text.strip())
    return int(m.group()) if m else 0


def call_openai(api_key: str, model: str, prompt: str, max_tokens: int = 16) -> str:
    backoff = [2, 5, 15, 30, 60]
    last_err = None
    for attempt, wait in enumerate(backoff):
        try:
            r = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": model,
                    "max_completion_tokens": max_tokens,
                    "temperature": 0,
                    "messages": [{"role": "user", "content": prompt}],
                },
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                timeout=90,
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            last_err = e
            code = e.response.status_code if e.response else None
            if code == 429:
                log(f"  429 rate limit, backoff {wait}s (attempt {attempt+1}/{len(backoff)})")
                time.sleep(wait)
                continue
            raise
        except Exception as e:
            last_err = e
            time.sleep(wait)
    raise last_err  # type: ignore[misc]


def atomic_write(path: Path, data) -> None:
    tmp = str(path) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def extract_response_text(responses_dict, condition):
    """Get the 'text' field from a response dict, handling string-or-dict cases."""
    r = responses_dict.get(condition)
    if r is None:
        return None
    if isinstance(r, str):
        return r
    if isinstance(r, dict):
        return r.get("text") or r.get("response")
    return str(r)


def run_target(target, openai_key: str) -> dict:
    name = target["name"]
    response_file = target["response_file"]
    condition = target["condition"]
    out_dir = target["out_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    log(f"=== {name} ===")
    log(f"Response file: {response_file}")
    questions = json.load(open(response_file, encoding="utf-8"))
    valid = [q for q in questions
             if q.get("held_out_passage")
             and extract_response_text(q.get("responses", {}), condition)]
    log(f"  {len(valid)} questions with held-out + response for {condition}")

    summary = {}
    for judge_name in JUDGES:
        out_path = out_dir / target["out_filename_template"].format(judge=judge_name)
        rows = []
        if out_path.exists():
            try:
                rows = json.load(open(out_path, encoding="utf-8"))
                log(f"  [{judge_name}] resuming, {len(rows)} existing rows")
            except Exception:
                rows = []

        # Index existing rows
        score_field = target["score_field_template"].format(judge=judge_name)
        if target["use_wide_schema"]:
            done = {(r["question_id"], r["condition"]) for r in rows
                    if r.get(score_field) is not None and (r.get("parse_failure") is not True)}
        else:
            done = {(r["question_id"], r["condition"]) for r in rows
                    if r.get("score") is not None and r.get("score") > 0
                    and (r.get("parse_failure") is not True)}

        # Replace existing parse-failure rows for this condition+judge
        rows = [r for r in rows if not (r.get("condition") == condition and r.get("parse_failure") is True)]
        new_calls = 0
        for q in valid:
            qid = q["question_id"]
            if (qid, condition) in done:
                continue
            ho = q["held_out_passage"]
            resp_text = extract_response_text(q.get("responses", {}), condition)
            if not resp_text:
                continue
            prompt = judge_prompt(ho, resp_text)
            try:
                raw = call_openai(openai_key, JUDGES[judge_name]["model"], prompt)
                score = parse_score(raw)
            except Exception as e:
                log(f"  [{judge_name}] q={qid} ERROR: {str(e)[:120]}")
                score = 0
                raw = f"ERROR: {e}"

            if target["use_wide_schema"]:
                row = {
                    "question_id": qid,
                    "condition": condition,
                    score_field: score if score > 0 else None,
                    "raw_response": raw[:200] if isinstance(raw, str) else str(raw)[:200],
                    "parse_failure": score == 0,
                }
            else:
                row = {
                    "question_id": qid,
                    "condition": condition,
                    "judge": judge_name,
                    "score": score if score > 0 else None,
                    "raw_response": raw[:200] if isinstance(raw, str) else str(raw)[:200],
                    "parse_failure": score == 0,
                }
            rows.append(row)
            new_calls += 1
            if new_calls % 10 == 0:
                atomic_write(out_path, rows)
                log(f"  [{judge_name}] {new_calls} new calls done")

        atomic_write(out_path, rows)
        success = sum(1 for r in rows
                      if r.get("condition") == condition
                      and (r.get("parse_failure") is not True))
        log(f"  [{judge_name}] DONE: {new_calls} new calls, {success} successful for {condition}, output: {out_path.name}")
        summary[judge_name] = {"new_calls": new_calls, "successful_for_condition": success}

    return {"target": name, "by_judge": summary}


def main() -> int:
    load_env()
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        log("FATAL: OPENAI_API_KEY not set")
        return 1

    all_summary = []
    for target in TARGETS:
        s = run_target(target, openai_key)
        all_summary.append(s)

    log("")
    log("=== RUN SUMMARY ===")
    for s in all_summary:
        log(f"  {s['target']}: {s['by_judge']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
