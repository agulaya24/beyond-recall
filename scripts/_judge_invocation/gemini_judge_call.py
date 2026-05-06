"""Gemini judge-call utility for the Beyond Recall study.

Parallel API to ``openai_judge_call.call_openai_judge`` for Google Gemini
models (Flash, Pro). Same structured return shape; raises ``JudgeAPIError``
on unrecoverable failure.

Public surface
--------------
    call_gemini_judge(model, system, user, **kwargs) -> dict
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

from .openai_judge_call import JudgeAPIError

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = REPO_ROOT / "logs" / "judge_calls"


def _resolve_api_key() -> str:
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if k:
        return k
    try:
        r = subprocess.run(
            ["powershell", "-Command",
             "[System.Environment]::GetEnvironmentVariable('GEMINI_API_KEY','User')"],
            capture_output=True, text=True, timeout=10,
        )
        v = r.stdout.strip()
        if v:
            os.environ["GEMINI_API_KEY"] = v
            return v
    except Exception:  # noqa: BLE001
        pass
    raise JudgeAPIError("GEMINI_API_KEY not set", failure_type="AUTH_ERROR")


_SCORE_RE = re.compile(r"\b([1-5])\b")


def _parse_score(text: str | None) -> int:
    if not text:
        return 0
    m = _SCORE_RE.search(text.strip())
    return int(m.group(1)) if m else 0


def _prompt_hash(system: str, user: str) -> str:
    h = hashlib.sha256()
    h.update(b"SYSTEM\n")
    h.update(system.encode("utf-8"))
    h.update(b"\nUSER\n")
    h.update(user.encode("utf-8"))
    return h.hexdigest()


def _log_call(record: dict[str, Any], run_id: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    path = LOG_DIR / f"{today}_{run_id}.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def call_gemini_judge(
    model: str,
    system: str,
    user: str,
    *,
    max_output_tokens: int = 16,
    temperature: float = 0.0,
    timeout_s: float = 60.0,
    max_retries_429: int = 5,
    max_retries_5xx: int = 3,
    run_id: str = "ad_hoc",
    log: bool = True,
) -> dict[str, Any]:
    """Invoke a Gemini model as a 1-to-5 score judge.

    Uses the public ``generativelanguage.googleapis.com`` REST endpoint.
    Returns the same structured dict shape as ``call_openai_judge``.
    """
    api_key = _resolve_api_key()
    prompt_hash = _prompt_hash(system, user)

    body: dict[str, Any] = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {
            "maxOutputTokens": max_output_tokens,
            "temperature": temperature,
        },
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    headers = {"Content-Type": "application/json"}

    started = time.time()
    attempts_429 = 0
    attempts_5xx = 0

    while True:
        try:
            r = httpx.post(url, json=body, headers=headers, timeout=timeout_s)
        except httpx.TimeoutException as e:
            raise JudgeAPIError(f"Timeout: {e}", failure_type="TIMEOUT")

        if r.status_code == 200:
            payload = r.json()
            cands = payload.get("candidates") or []
            raw_text = ""
            if cands:
                parts = (cands[0].get("content") or {}).get("parts") or []
                raw_text = "".join(p.get("text", "") for p in parts)
            usage = payload.get("usageMetadata") or {}
            tokens = {
                "prompt": int(usage.get("promptTokenCount", 0) or 0),
                "completion": int(usage.get("candidatesTokenCount", 0) or 0),
                "total": int(usage.get("totalTokenCount", 0) or 0),
            }
            score = _parse_score(raw_text)
            error_type = None if score >= 1 else "PARSE_FAILURE"
            result = {
                "score": score,
                "raw_text": raw_text.strip()[:500],
                "tokens": tokens,
                "latency_ms": int((time.time() - started) * 1000),
                "error_type": error_type,
                "model": model,
                "param_used": "maxOutputTokens",
                "prompt_hash": prompt_hash,
            }
            if log:
                _log_call({
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "run_id": run_id, "provider": "gemini",
                    **result, "ok": error_type is None,
                }, run_id)
            return result

        if r.status_code == 429:
            attempts_429 += 1
            if attempts_429 > max_retries_429:
                raise JudgeAPIError(f"Rate limited: {r.text[:300]}",
                                    failure_type="RATE_LIMITED")
            time.sleep(min(60, 2 ** (attempts_429 + 1)))
            continue

        if 500 <= r.status_code < 600:
            attempts_5xx += 1
            if attempts_5xx > max_retries_5xx:
                raise JudgeAPIError(f"Server error: {r.text[:300]}",
                                    failure_type="SERVER_ERROR")
            time.sleep(2 ** attempts_5xx)
            continue

        if r.status_code in (401, 403):
            raise JudgeAPIError(f"Auth error {r.status_code}",
                                failure_type="AUTH_ERROR")

        raise JudgeAPIError(f"HTTP {r.status_code}: {r.text[:300]}",
                            failure_type="UNKNOWN", raw=r.text[:500])


__all__ = ["call_gemini_judge", "JudgeAPIError"]
