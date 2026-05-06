"""OpenAI judge-call utility for the Beyond Recall study.

Single point of entry for every OpenAI judge invocation in the repo.

Why this file exists
--------------------
Two batch failures during v10 review (2026-04-25) traced to one root cause:
the GPT-5.x family rejects the `max_tokens` parameter with HTTP 400; the
correct parameter is `max_completion_tokens`. The bug was duplicated across
multiple ad-hoc judge invocation paths (`scripts/judge_tier2.py`,
`scripts/run_judges.py`, inline scripts under `docs/research/_letta_rerun/`).

This module is the single fixed implementation. New judging code MUST import
from here. Do not hand-roll a new OpenAI judge call.

Public surface
--------------
    call_openai_judge(model, system, user, **kwargs) -> dict
    JudgeAPIError

The return shape is stable across providers (see anthropic_judge_call.py and
gemini_judge_call.py for the parallel modules).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

# ----- Repo paths -----------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = REPO_ROOT / "logs" / "judge_calls"


# ----- Public exception -----------------------------------------------------

class JudgeAPIError(Exception):
    """Raised when an OpenAI judge call cannot be completed.

    The `failure_type` attribute names the structured failure mode and is
    one of:
        BAD_PARAMETER       400 with a parameter-shape complaint
        AUTH_ERROR          401 / 403
        RATE_LIMITED        429 after retries exhausted
        SERVER_ERROR        5xx after retries exhausted
        TIMEOUT             network timeout
        PARSE_FAILURE       could not extract a 1 to 5 score from the response
        UNKNOWN             anything else
    """

    def __init__(self, message: str, failure_type: str = "UNKNOWN", *, raw: str | None = None) -> None:
        super().__init__(message)
        self.failure_type = failure_type
        self.raw = raw


# ----- Model-id routing -----------------------------------------------------

_TOKEN_PARAM_NEW = "max_completion_tokens"
_TOKEN_PARAM_OLD = "max_tokens"

_NEW_PARAM_PREFIXES: tuple[str, ...] = ("o1", "o3", "gpt-5")


def _token_param_for(model: str) -> str:
    """Return the correct max-tokens parameter name for a given OpenAI model id.

    GPT-5.x and the o1/o3 reasoning families require `max_completion_tokens`;
    every other model accepts `max_tokens`. Match is on lower-case prefix so
    `gpt-5.4`, `gpt-5.5`, `gpt-5-mini`, `o1-preview`, etc. all route to the
    new parameter name.
    """
    m = model.lower().strip()
    for p in _NEW_PARAM_PREFIXES:
        if m.startswith(p):
            return _TOKEN_PARAM_NEW
    return _TOKEN_PARAM_OLD


# ----- API key resolution ---------------------------------------------------

def _resolve_api_key() -> str:
    """Resolve OPENAI_API_KEY. Prefer process env, fall back to Windows User env."""
    k = os.environ.get("OPENAI_API_KEY", "").strip()
    if k:
        return k
    # Windows-User-env fallback (matches the pattern in
    # scripts/_rerun_wrong_spec_v2_gpt54_20260425.py)
    try:
        r = subprocess.run(
            ["powershell", "-Command",
             "[System.Environment]::GetEnvironmentVariable('OPENAI_API_KEY','User')"],
            capture_output=True, text=True, timeout=10,
        )
        v = r.stdout.strip()
        if v:
            os.environ["OPENAI_API_KEY"] = v
            return v
    except Exception:  # noqa: BLE001
        pass
    raise JudgeAPIError("OPENAI_API_KEY not set in env or Windows User env",
                        failure_type="AUTH_ERROR")


# ----- Score parser ---------------------------------------------------------

_SCORE_RE = re.compile(r"\b([1-5])\b")


def _parse_score(text: str | None) -> int:
    if not text:
        return 0
    m = _SCORE_RE.search(text.strip())
    return int(m.group(1)) if m else 0


# ----- Logging --------------------------------------------------------------

def _prompt_hash(system: str, user: str) -> str:
    h = hashlib.sha256()
    h.update(b"SYSTEM\n")
    h.update(system.encode("utf-8"))
    h.update(b"\nUSER\n")
    h.update(user.encode("utf-8"))
    return h.hexdigest()


def _log_call(record: dict[str, Any], run_id: str) -> None:
    """Append one JSONL record to logs/judge_calls/<date>_<run_id>.jsonl."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    path = LOG_DIR / f"{today}_{run_id}.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ----- Public entry point ---------------------------------------------------

def call_openai_judge(
    model: str,
    system: str,
    user: str,
    *,
    max_output_tokens: int = 10,
    temperature: float = 0.0,
    timeout_s: float = 60.0,
    max_retries_429: int = 5,
    max_retries_5xx: int = 3,
    run_id: str = "ad_hoc",
    log: bool = True,
) -> dict[str, Any]:
    """Invoke an OpenAI chat completion as a 1-to-5 score judge.

    Parameters
    ----------
    model : OpenAI model id, e.g. ``gpt-5.4`` or ``gpt-4o``.
    system : System prompt string. Pass empty string if not used.
    user : User-content prompt string. Must contain the rubric and inputs.
    max_output_tokens : Output token cap. The parameter name is selected
        automatically based on `model`.
    temperature : Sampling temperature. Defaults to 0 for judge use.
    timeout_s : Per-attempt HTTP timeout in seconds.
    max_retries_429 : Number of exponential-backoff retries for HTTP 429.
    max_retries_5xx : Number of exponential-backoff retries for HTTP 5xx.
    run_id : Stable identifier for the calling job, used in log filename.
    log : If True, append a JSONL record to ``logs/judge_calls/``.

    Returns
    -------
    dict with keys ``score`` (int 0 to 5; 0 indicates parse failure),
    ``raw_text`` (string), ``tokens`` ({prompt, completion, total}),
    ``latency_ms`` (int), ``error_type`` (None on success or a JudgeAPIError
    failure-type string on a non-fatal degraded return), ``model``,
    ``param_used`` (which token-cap parameter was sent), ``prompt_hash``.

    Raises
    ------
    JudgeAPIError if the call cannot be completed. The exception's
    ``failure_type`` attribute names the failure mode.
    """
    api_key = _resolve_api_key()
    param_name = _token_param_for(model)
    prompt_hash = _prompt_hash(system, user)

    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    body: dict[str, Any] = {
        "model": model,
        param_name: max_output_tokens,
        "temperature": temperature,
        "messages": messages,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    url = "https://api.openai.com/v1/chat/completions"

    started = time.time()
    last_err: Exception | None = None
    raw_text: str = ""
    tokens = {"prompt": 0, "completion": 0, "total": 0}

    attempts_429 = 0
    attempts_5xx = 0

    while True:
        try:
            r = httpx.post(url, json=body, headers=headers, timeout=timeout_s)
        except httpx.TimeoutException as e:
            last_err = e
            if attempts_5xx < max_retries_5xx:
                attempts_5xx += 1
                time.sleep(2 ** attempts_5xx)
                continue
            err = JudgeAPIError(f"Timeout after {attempts_5xx} retries: {e}",
                                failure_type="TIMEOUT")
            _record_outcome(log, run_id, model, param_name, prompt_hash,
                            started, raw_text, tokens, err)
            raise err
        except Exception as e:  # noqa: BLE001
            last_err = e
            err = JudgeAPIError(f"Network error: {e}", failure_type="UNKNOWN")
            _record_outcome(log, run_id, model, param_name, prompt_hash,
                            started, raw_text, tokens, err)
            raise err

        # Handle status codes.
        if r.status_code == 200:
            payload = r.json()
            try:
                raw_text = payload["choices"][0]["message"]["content"] or ""
            except (KeyError, IndexError, TypeError) as e:
                err = JudgeAPIError(f"Malformed 200 response: {e}",
                                    failure_type="UNKNOWN", raw=r.text[:300])
                _record_outcome(log, run_id, model, param_name, prompt_hash,
                                started, raw_text, tokens, err)
                raise err
            usage = payload.get("usage") or {}
            tokens = {
                "prompt": int(usage.get("prompt_tokens", 0) or 0),
                "completion": int(usage.get("completion_tokens", 0) or 0),
                "total": int(usage.get("total_tokens", 0) or 0),
            }
            score = _parse_score(raw_text)
            error_type = None if score >= 1 else "PARSE_FAILURE"
            latency_ms = int((time.time() - started) * 1000)
            result = {
                "score": score,
                "raw_text": raw_text.strip()[:500],
                "tokens": tokens,
                "latency_ms": latency_ms,
                "error_type": error_type,
                "model": model,
                "param_used": param_name,
                "prompt_hash": prompt_hash,
            }
            if log:
                _log_call({
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "run_id": run_id,
                    "provider": "openai",
                    **result,
                    "ok": error_type is None,
                }, run_id)
            return result

        if r.status_code == 429:
            attempts_429 += 1
            if attempts_429 > max_retries_429:
                err = JudgeAPIError(
                    f"Rate limited after {attempts_429 - 1} retries",
                    failure_type="RATE_LIMITED", raw=r.text[:300],
                )
                _record_outcome(log, run_id, model, param_name, prompt_hash,
                                started, raw_text, tokens, err)
                raise err
            wait = min(60, 2 ** (attempts_429 + 1))
            time.sleep(wait)
            continue

        if 500 <= r.status_code < 600:
            attempts_5xx += 1
            if attempts_5xx > max_retries_5xx:
                err = JudgeAPIError(
                    f"Server error {r.status_code} after {attempts_5xx - 1} retries",
                    failure_type="SERVER_ERROR", raw=r.text[:300],
                )
                _record_outcome(log, run_id, model, param_name, prompt_hash,
                                started, raw_text, tokens, err)
                raise err
            time.sleep(2 ** attempts_5xx)
            continue

        if r.status_code in (401, 403):
            err = JudgeAPIError(f"Auth error {r.status_code}: {r.text[:300]}",
                                failure_type="AUTH_ERROR", raw=r.text[:300])
            _record_outcome(log, run_id, model, param_name, prompt_hash,
                            started, raw_text, tokens, err)
            raise err

        if r.status_code == 400:
            # Inspect the body. The historical bug surfaces as a body that
            # explicitly mentions the disallowed parameter name. Surface a
            # named failure type so downstream code can react.
            body_txt = r.text or ""
            failure_type = "BAD_PARAMETER"
            if "max_tokens" in body_txt and "max_completion_tokens" in body_txt:
                # The model is rejecting `max_tokens` and pointing at
                # `max_completion_tokens`. This is the historical bug.
                pass
            err = JudgeAPIError(
                f"HTTP 400 from OpenAI: {body_txt[:300]}",
                failure_type=failure_type, raw=body_txt[:500],
            )
            _record_outcome(log, run_id, model, param_name, prompt_hash,
                            started, raw_text, tokens, err)
            raise err

        # Anything else.
        err = JudgeAPIError(
            f"Unexpected HTTP {r.status_code}: {r.text[:300]}",
            failure_type="UNKNOWN", raw=r.text[:500],
        )
        _record_outcome(log, run_id, model, param_name, prompt_hash,
                        started, raw_text, tokens, err)
        raise err


def _record_outcome(log: bool, run_id: str, model: str, param_name: str,
                    prompt_hash: str, started: float, raw_text: str,
                    tokens: dict[str, int], err: JudgeAPIError) -> None:
    if not log:
        return
    _log_call({
        "ts": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "provider": "openai",
        "model": model,
        "param_used": param_name,
        "prompt_hash": prompt_hash,
        "raw_text": raw_text[:200],
        "tokens": tokens,
        "latency_ms": int((time.time() - started) * 1000),
        "error_type": err.failure_type,
        "error_message": str(err)[:300],
        "ok": False,
    }, run_id)


# Convenience for callers that only have a single combined prompt (most of
# the existing scripts pass everything through user content):
def call_openai_judge_user_only(model: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
    """Single-prompt convenience wrapper. Routes through `call_openai_judge`."""
    return call_openai_judge(model=model, system="", user=prompt, **kwargs)


__all__ = [
    "JudgeAPIError",
    "call_openai_judge",
    "call_openai_judge_user_only",
]
