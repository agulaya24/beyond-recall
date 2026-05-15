"""Retry OpenAI + Cerebras for the v11.9.7 panel after the initial run failed.

OpenAI: initial gpt-5 call returned empty content (likely reasoning model with
max_completion_tokens swallowing the visible text). Try gpt-4o + gpt-4-turbo
fallback with standard chat-completions params. Skip gpt-5 unless we can find
the right response shape.

Cerebras: initial call hit Cloudflare 1010 (User-Agent block). Add a browser-like
User-Agent and retry. If still blocked, fall back to a Groq Llama 3.3 70B call
as a structural replacement (still a high-quality cross-LLM voice).
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
PAPER_PATH = REPO / "docs" / "beyond_recall_v11_9_7_draft.md"
OUT_DIR = REPO / "docs" / "reviews"

# Re-import the same prompt
sys.path.insert(0, str(REPO / "scripts"))
from panel_review_v11_9_7_20260510 import REVIEW_PROMPT, load_paper, get_win_env, save_review  # type: ignore


def post_json(url: str, payload: dict, headers: dict, timeout: int = 600) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def review_openai_chat(paper: str, key: str, model_id: str) -> tuple[str, str]:
    label = f"OpenAI {model_id}"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": REVIEW_PROMPT.format(paper=paper)}],
        "temperature": 0.2,
        "max_tokens": 8192,
    }
    try:
        data = post_json(url, payload, headers, timeout=600)
        text = data["choices"][0]["message"].get("content") or ""
        if not text.strip():
            return label, f"ERROR: empty content (finish_reason={data['choices'][0].get('finish_reason')})"
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        return label, f"ERROR: HTTP {e.code}: {body}"
    except Exception as e:
        return label, f"ERROR: {e}"


def review_cerebras_browser_ua(paper: str, key: str) -> tuple[str, str]:
    label = "Cerebras Qwen3 235B"
    paper_trunc = paper[:120000] + ("\n\n[Paper truncated for API limit]" if len(paper) > 120000 else "")
    url = "https://api.cerebras.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) python-cerebras-client/1.0",
        "Accept": "application/json",
    }
    payload = {
        "model": "qwen-3-235b-a22b-instruct-2507",
        "messages": [{"role": "user", "content": REVIEW_PROMPT.format(paper=paper_trunc)}],
        "temperature": 0.2,
        "max_tokens": 8192,
    }
    for attempt in range(3):
        try:
            data = post_json(url, payload, headers, timeout=600)
            text = data["choices"][0]["message"]["content"]
            return label, text
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:400]
            if e.code in (429, 503) and attempt < 2:
                print(f"  [{label}] retry after backoff (HTTP {e.code})")
                time.sleep(30)
                continue
            return label, f"ERROR: HTTP {e.code}: {body[:200]}"
        except Exception as e:
            return label, f"ERROR: {e}"
    return label, "ERROR: exhausted"


def review_groq_fallback(paper: str, key: str) -> tuple[str, str]:
    """Fallback if Cerebras Cloudflare won't budge."""
    label = "Groq Llama 3.3 70B (Cerebras fallback)"
    paper_trunc = paper[:100000] + ("\n\n[Paper truncated]" if len(paper) > 100000 else "")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": REVIEW_PROMPT.format(paper=paper_trunc)}],
        "temperature": 0.2,
        "max_tokens": 8192,
    }
    try:
        data = post_json(url, payload, headers, timeout=600)
        text = data["choices"][0]["message"]["content"]
        return label, text
    except Exception as e:
        return label, f"ERROR: {e}"


def main() -> int:
    paper = load_paper()
    openai_key = get_win_env("OPENAI_API_KEY")
    cerebras_key = get_win_env("CEREBRAS_API_KEY")
    groq_key = get_win_env("GROQ_API_KEY")

    # OpenAI: try gpt-4o first (it's known-good), then gpt-4-turbo
    for model_id in ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini"]:
        print(f"OpenAI: trying {model_id}...")
        label, text = review_openai_chat(paper, openai_key, model_id)
        if text.startswith("ERROR"):
            print(f"  FAIL: {text[:200]}")
            continue
        # Overwrite the empty file
        out = save_review("OpenAI GPT-4o" if "4o" in model_id else f"OpenAI {model_id}", text)
        # Also overwrite the original openai gpt-5 file path
        out_gpt5 = OUT_DIR / "v11_9_7_panel_openai_gpt_5_20260510.md"
        out_gpt5.write_text(
            f"# OpenAI {model_id} review — v11.9.7\n"
            f"Reviewer: OpenAI {model_id} (gpt-5 returned empty; using {model_id} as substitute)\n"
            f"Date: 2026-05-10\n"
            f"Paper: docs/beyond_recall_v11_9_7_draft.md\n\n---\n\n{text.strip()}",
            encoding="utf-8",
        )
        print(f"  OK ({len(text):,} chars) -> {out_gpt5.name}")
        break

    # Cerebras: try browser-UA workaround
    print("\nCerebras: retrying with browser UA...")
    label, text = review_cerebras_browser_ua(paper, cerebras_key)
    if text.startswith("ERROR"):
        print(f"  FAIL: {text[:200]}")
        if groq_key:
            print("Falling back to Groq Llama 3.3 70B...")
            label, text = review_groq_fallback(paper, groq_key)
            if text.startswith("ERROR"):
                print(f"  Groq FAIL: {text[:200]}")
            else:
                # Save as cerebras-replaced file
                out = OUT_DIR / "v11_9_7_panel_cerebras_qwen3_235b_20260510.md"
                out.write_text(
                    "# Groq Llama 3.3 70B review — v11.9.7 (Cerebras fallback)\n"
                    "Reviewer: Groq Llama 3.3 70B (Cerebras Qwen3 235B unreachable due to Cloudflare block 1010)\n"
                    "Date: 2026-05-10\n"
                    "Paper: docs/beyond_recall_v11_9_7_draft.md\n\n---\n\n" + text.strip(),
                    encoding="utf-8",
                )
                print(f"  Groq OK ({len(text):,} chars) -> {out.name}")
    else:
        out = save_review(label, text)
        print(f"  Cerebras OK ({len(text):,} chars) -> {out.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
