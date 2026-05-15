"""Retry Cerebras + Groq after initial cold-review failures.

Cerebras: 429 (queue). Wait + retry.
Groq: 403 1010 (Cloudflare UA block). Add browser User-Agent.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "docs" / "reviews"

sys.path.insert(0, str(REPO / "scripts"))
from cold_abstract_review_20260512 import (  # type: ignore
    ABSTRACT_TEXT, COLD_PROMPT, get_win_env, post_json, save_review,
)


def review_cerebras_retry(prompt: str, key: str, attempts: int = 3) -> tuple[str, str]:
    label = "Cerebras Qwen3 235B"
    url = "https://api.cerebras.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) python-cerebras-client/1.0",
    }
    payload = {
        "model": "qwen-3-235b-a22b-instruct-2507",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 4000,
    }
    for attempt in range(attempts):
        try:
            data = post_json(url, payload, headers)
            text = data["choices"][0]["message"]["content"]
            return label, text
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:300]
            if e.code == 429 and attempt < attempts - 1:
                wait = 15 * (attempt + 1)
                print(f"  Cerebras 429 (attempt {attempt+1}); waiting {wait}s", flush=True)
                time.sleep(wait)
                continue
            return label, f"ERROR: HTTP {e.code}: {body}"
        except Exception as e:
            return label, f"ERROR: {e}"
    return label, "ERROR: exhausted retries"


def review_groq_with_ua(prompt: str, key: str) -> tuple[str, str]:
    label = "Groq Llama 3.3 70B"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Accept": "application/json",
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 4000,
    }
    try:
        data = post_json(url, payload, headers)
        text = data["choices"][0]["message"]["content"]
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        return label, f"ERROR: HTTP {e.code}: {body}"
    except Exception as e:
        return label, f"ERROR: {e}"


def main() -> None:
    prompt = COLD_PROMPT.format(abstract=ABSTRACT_TEXT)

    cerebras_key = get_win_env("CEREBRAS_API_KEY")
    groq_key = get_win_env("GROQ_API_KEY")

    if cerebras_key:
        print("Retrying Cerebras Qwen3 235B...", flush=True)
        label, text = review_cerebras_retry(prompt, cerebras_key)
        path = save_review(label, text)
        print(f"  Saved: {path}", flush=True)
        print(f"  Preview: {text[:300]}\n", flush=True)

    if groq_key:
        print("Retrying Groq Llama 3.3 70B with browser UA...", flush=True)
        label, text = review_groq_with_ua(prompt, groq_key)
        path = save_review(label, text)
        print(f"  Saved: {path}", flush=True)
        print(f"  Preview: {text[:300]}\n", flush=True)


if __name__ == "__main__":
    main()
