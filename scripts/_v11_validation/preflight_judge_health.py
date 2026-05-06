"""Pre-flight health check for the judge panel.

Sends one canonical-format judge prompt to each model in the panel and
verifies the model returns a numeric score in [1, 5] within timeout. Used
as a hard gate BEFORE any large-batch judging job (>50 calls).

Run::

    python scripts/_v11_validation/preflight_judge_health.py

Exit code 0 if every required judge passes; 1 if any fails.

Required judges by default are the 5-judge primary panel
(haiku, sonnet, opus, gpt4o, gpt54). The two Gemini sensitivity judges
are tested as well but are non-blocking by default; pass ``--require-gemini``
to make their failure also gate the run.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Module path bootstrap: when run as a script, scripts/ is not on sys.path.
# This MUST happen before the _judge_invocation import below.
REPO = Path(__file__).resolve().parent.parent.parent
LOG_DIR = REPO / "logs" / "judge_calls"
sys.path.insert(0, str(REPO / "scripts"))

from _judge_invocation import JudgeAPIError, call_judge  # noqa: E402

# Canonical 1-line judge probe. The expected behavior is "return 5".
PROBE_PROMPT = """You are evaluating a behavioral prediction against a verbatim ground truth passage.

Question: What did the subject do when faced with adversity in childhood?

Ground truth (what actually happened): The subject ran away from home at age twelve and worked as a printer's apprentice.

Response to score: The subject ran away from home at age twelve and worked as a printer's apprentice.

Score 1-5 based on prediction accuracy:
5 = Predicts the specific outcome or behavior in the ground truth
4 = Predicts the general direction correctly with some specifics
3 = Captures the right domain but not the specific outcome
2 = Addresses the topic but predicts incorrectly
1 = Refuses to answer or is completely off-base

Respond with only the number 1, 2, 3, 4, or 5."""

EXPECTED_LOW = 4   # an exact-match response should score 4 or 5
EXPECTED_HIGH = 5

# (slug, provider, model_id, required)
JUDGE_PANEL: list[tuple[str, str, str, bool]] = [
    ("haiku",        "anthropic", "claude-haiku-4-5",  True),
    ("sonnet",       "anthropic", "claude-sonnet-4-6", True),
    ("opus",         "anthropic", "claude-opus-4-6",   True),
    ("gpt4o",        "openai",    "gpt-4o",            True),
    ("gpt54",        "openai",    "gpt-5.4",           True),
    ("gemini_flash", "gemini",    "gemini-2.5-flash",  False),
    ("gemini_pro",   "gemini",    "gemini-2.5-pro",    False),
]


def _run_one(slug: str, provider: str, model: str, run_id: str,
             timeout_s: float) -> dict[str, object]:
    started = time.time()
    try:
        result = call_judge(
            provider, model, system="", user=PROBE_PROMPT,
            max_output_tokens=10, temperature=0.0,
            timeout_s=timeout_s, run_id=run_id, log=True,
        )
        elapsed_ms = int((time.time() - started) * 1000)
        score = int(result.get("score", 0) or 0)
        ok = EXPECTED_LOW <= score <= EXPECTED_HIGH
        return {
            "slug": slug, "provider": provider, "model": model,
            "ok": ok, "score": score, "raw": result.get("raw_text", "")[:80],
            "param_used": result.get("param_used"),
            "elapsed_ms": elapsed_ms, "error": None,
        }
    except JudgeAPIError as e:
        elapsed_ms = int((time.time() - started) * 1000)
        return {
            "slug": slug, "provider": provider, "model": model,
            "ok": False, "score": 0, "raw": "",
            "param_used": None,
            "elapsed_ms": elapsed_ms,
            "error": f"{e.failure_type}: {e}",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Judge-panel health pre-flight")
    parser.add_argument("--require-gemini", action="store_true",
                        help="Make Gemini failures gate the exit code.")
    parser.add_argument("--timeout-s", type=float, default=60.0)
    parser.add_argument("--run-id", type=str,
                        default=f"preflight_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    args = parser.parse_args()

    print("Judge-panel health pre-flight")
    print(f"  Run ID  : {args.run_id}")
    print(f"  Timeout : {args.timeout_s}s")
    print(f"  Require Gemini: {args.require_gemini}")
    print()

    results: list[dict[str, object]] = []
    for slug, provider, model, required in JUDGE_PANEL:
        if not required and not args.require_gemini:
            tag = "(sensitivity)"
        else:
            tag = ""
        print(f"  -> {slug:<14} {provider:<10} {model:<24} {tag}", flush=True)
        r = _run_one(slug, provider, model, args.run_id, args.timeout_s)
        r["required"] = required or args.require_gemini
        status = "OK" if r["ok"] else "FAIL"
        print(f"     {status:<5} score={r['score']} param={r.get('param_used')!s:<25} "
              f"elapsed={r['elapsed_ms']}ms err={r['error']}")
        results.append(r)

    print()
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = LOG_DIR / f"preflight_{args.run_id}.json"
    summary_path.write_text(
        json.dumps({"run_id": args.run_id, "results": results}, indent=2),
        encoding="utf-8",
    )
    print(f"Summary written: {summary_path.relative_to(REPO).as_posix()}")

    failed_required = [r for r in results if r["required"] and not r["ok"]]
    if failed_required:
        print(f"FAIL: {len(failed_required)} required judges failed.")
        for r in failed_required:
            print(f"  {r['slug']:<14} {r['error']}")
        return 1
    print("PASS: all required judges healthy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
