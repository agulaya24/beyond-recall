"""Blind language-model review of the v11.9.10 paper.

Field-reader simulation: send the FULL paper to each provider with a single
minimal, generic prompt ("Please provide honest feedback on this paper").
No paper-specific framing, no rubric, no structured output spec. This
captures what each LLM spontaneously surfaces when no direction is provided,
mimicking the natural-use case where someone pastes the paper into an LLM
and asks for thoughts.

Providers: Gemini 2.5 Pro, OpenAI gpt-5.4 (fallback gpt-5 then gpt-4o),
Mistral Large. Anthropic Claude handled separately by a sub-agent.

Outputs: docs/reviews/v11_9_10_blind_review_<provider>_20260511.md
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
PAPER_PATH = REPO / "docs" / "beyond_recall_v11_9_10_draft.md"
OUT_DIR = REPO / "docs" / "reviews"

GPT5_PREFIXES = ("o1", "o3", "gpt-5")


def needs_new_param(model: str) -> bool:
    m = model.lower().strip()
    return any(m.startswith(p) for p in GPT5_PREFIXES)


def get_win_env(key: str) -> str:
    r = subprocess.run(
        ["powershell", "-Command", f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True,
    )
    return r.stdout.strip()


def post_json(url: str, payload: dict, headers: dict, timeout: int = 900) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


PROMPT_HEADER = "Please provide honest feedback on this paper.\n\n---\n\n"


def review_gemini(payload_text: str, key: str) -> tuple[str, str]:
    label = "Gemini 2.5 Pro"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": payload_text}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 16384},
    }
    try:
        data = post_json(url, payload, {"Content-Type": "application/json"})
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return label, text
    except Exception as e:
        return label, f"ERROR: {e}"


def review_openai(payload_text: str, key: str, model_id: str) -> tuple[str, str]:
    label = f"OpenAI {model_id}"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    payload: dict = {
        "model": model_id,
        "messages": [{"role": "user", "content": payload_text}],
    }
    if needs_new_param(model_id):
        payload["max_completion_tokens"] = 16000
    else:
        payload["max_tokens"] = 8000
        payload["temperature"] = 0.4
    try:
        data = post_json(url, payload, headers)
        choice = data["choices"][0]
        text = (choice.get("message") or {}).get("content") or ""
        if not text.strip():
            return label, f"ERROR: empty content (finish_reason={choice.get('finish_reason')})"
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        return label, f"ERROR: HTTP {e.code}: {body}"
    except Exception as e:
        return label, f"ERROR: {e}"


def review_mistral(payload_text: str, key: str) -> tuple[str, str]:
    label = "Mistral Large"
    url = "https://api.mistral.ai/v1/chat/completions"
    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": payload_text}],
        "temperature": 0.4,
        "max_tokens": 8000,
    }
    try:
        data = post_json(url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
        text = data["choices"][0]["message"]["content"]
        return label, text
    except Exception as e:
        return label, f"ERROR: {e}"


def slug_for(label: str) -> str:
    if label.startswith("OpenAI"):
        return "openai_" + label.split()[-1].replace(".", "_").replace("-", "_").lower()
    if label.startswith("Gemini"):
        return "gemini_2_5_pro"
    if label.startswith("Mistral"):
        return "mistral_large"
    return label.lower().replace(" ", "_")


def save_review(label: str, text: str, paper_chars: int) -> Path:
    slug = slug_for(label)
    out = OUT_DIR / f"v11_9_10_blind_review_{slug}_20260511.md"
    body = [
        f"# {label} blind review — v11.9.10",
        f"Reviewer: {label}",
        "Date: 2026-05-11",
        "Paper: docs/beyond_recall_v11_9_10_draft.md",
        "Prompt: \"Please provide honest feedback on this paper.\" (only — no rubric, no framing)",
        f"Paper size sent: {paper_chars:,} chars (~{paper_chars//4:,} tokens)",
        "",
        "---",
        "",
        text.strip(),
    ]
    out.write_text("\n".join(body), encoding="utf-8")
    return out


def main() -> int:
    paper_text = PAPER_PATH.read_text(encoding="utf-8")
    payload_text = PROMPT_HEADER + paper_text
    paper_chars = len(paper_text)

    print(f"Paper size: {paper_chars:,} chars (~{paper_chars//4:,} tokens)")
    print(f"Total payload: {len(payload_text):,} chars\n")

    gemini_key = get_win_env("GEMINI_API_KEY")
    openai_key = get_win_env("OPENAI_API_KEY")
    mistral_key = get_win_env("MISTRAL_API_KEY")
    missing = [k for k, v in [("GEMINI", gemini_key), ("OPENAI", openai_key), ("MISTRAL", mistral_key)] if not v]
    if missing:
        print(f"Missing: {missing}")
        return 1

    print("Gemini 2.5 Pro ...")
    label, t = review_gemini(payload_text, gemini_key)
    out = save_review(label, t, paper_chars)
    print(f"  {'OK' if not t.startswith('ERROR') else 'FAIL'} ({len(t):,} chars) -> {out.name}")

    for model_id in ["gpt-5.4", "gpt-5", "gpt-4o"]:
        print(f"OpenAI {model_id} ...")
        label, t = review_openai(payload_text, openai_key, model_id)
        if not t.startswith("ERROR"):
            out = save_review(label, t, paper_chars)
            print(f"  OK ({len(t):,} chars) -> {out.name}")
            break
        print(f"  FAIL: {t[:200]}")

    print("Mistral Large ...")
    label, t = review_mistral(payload_text, mistral_key)
    out = save_review(label, t, paper_chars)
    print(f"  {'OK' if not t.startswith('ERROR') else 'FAIL'} ({len(t):,} chars) -> {out.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
