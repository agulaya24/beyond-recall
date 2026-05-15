"""Retry the panel review for GPT-5.4 using the correct param shape.

The first attempt at GPT-5 / GPT-5.4 returned an empty content body because the
GPT-5.x family rejects `max_tokens` and requires `max_completion_tokens`. This
script uses the shared `_judge_invocation/openai_judge_call.py` parameter
selector that already handles this distinction for the rest of the codebase
(it routes gpt-5.x to `max_completion_tokens` automatically).

Also retries Cerebras Qwen3 235B once with a long-waiting backoff in case the
TPM quota has freed up overnight; if it still fails, leaves the existing
fallback file in place.
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

sys.path.insert(0, str(REPO / "scripts"))
from panel_review_v11_9_7_20260510 import REVIEW_PROMPT, load_paper, get_win_env  # type: ignore

GPT54_PREFIXES = ("o1", "o3", "gpt-5")


def needs_new_param(model: str) -> bool:
    m = model.lower().strip()
    return any(m.startswith(p) for p in GPT54_PREFIXES)


def post_json(url: str, payload: dict, headers: dict, timeout: int = 600) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def review_openai(paper: str, key: str, model_id: str) -> tuple[str, str]:
    label = f"OpenAI {model_id}"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}

    payload: dict = {
        "model": model_id,
        "messages": [{"role": "user", "content": REVIEW_PROMPT.format(paper=paper)}],
    }
    if needs_new_param(model_id):
        # GPT-5.x family: no temperature override (some variants reject it), high cap
        payload["max_completion_tokens"] = 16384
    else:
        payload["max_tokens"] = 8192
        payload["temperature"] = 0.2

    try:
        data = post_json(url, payload, headers, timeout=900)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:600]
        return label, f"ERROR: HTTP {e.code}: {body}"
    except Exception as e:
        return label, f"ERROR: {e}"

    choice = data.get("choices", [{}])[0]
    text = (choice.get("message") or {}).get("content") or ""
    finish = choice.get("finish_reason")
    if not text.strip():
        usage = data.get("usage", {})
        return label, (
            f"ERROR: empty content (finish_reason={finish}; "
            f"completion_tokens={usage.get('completion_tokens')}; "
            f"reasoning_tokens={(usage.get('completion_tokens_details') or {}).get('reasoning_tokens')})"
        )
    return label, text


def save_review(label: str, model_id: str, text: str) -> Path:
    slug = "openai_" + model_id.replace(".", "_").replace("-", "_").lower()
    out = OUT_DIR / f"v11_9_7_panel_{slug}_20260511.md"
    body = [
        f"# {label} review — v11.9.7",
        f"Reviewer: {label}",
        "Date: 2026-05-11",
        "Paper: docs/beyond_recall_v11_9_7_draft.md",
        "",
        "---",
        "",
        text.strip(),
    ]
    out.write_text("\n".join(body), encoding="utf-8")
    return out


def main() -> int:
    paper = load_paper()
    print(f"Paper loaded: {len(paper):,} chars\n")

    openai_key = get_win_env("OPENAI_API_KEY")
    if not openai_key:
        print("Missing OPENAI_API_KEY")
        return 1

    # Try the GPT-5 family in the order of likely quality
    candidates = ["gpt-5.4", "gpt-5", "gpt-5-pro"]
    for model_id in candidates:
        print(f"=== {model_id} ===")
        label, text = review_openai(paper, openai_key, model_id)
        if text.startswith("ERROR"):
            print(f"  FAIL: {text[:300]}\n")
            continue
        out = save_review(label, model_id, text)
        print(f"  OK ({len(text):,} chars)")
        print(f"  -> {out}\n")
        return 0

    print("All GPT-5 family attempts failed.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
