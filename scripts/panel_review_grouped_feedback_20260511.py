"""Send the v11.9.10 grouped feedback document to 3 LLM providers for review.

The grouped feedback doc consolidates 142 docx comments into 10 categories
with effort estimates and a recommended sequencing. The panel reviews this
*meta-feedback* document, not the paper itself. Useful for validating the
grouping, flagging missed themes, and stress-testing the sequencing.

Prompt is intentionally generic: "Please review this feedback-grouping
document. Tell me what you'd prioritize, what's mis-grouped, what's missing,
and where the sequencing could be improved."

Outputs: docs/reviews/v11_9_10_panel_grouped_feedback_<provider>_20260511.md
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
GROUPED_FEEDBACK_PATH = REPO / "docs" / "reviews" / "v11_9_10_comments_review_grouped_20260511.md"
RAW_COMMENTS_PATH = REPO / "docs" / "reviews" / "v11_9_10_comments_extracted_20260511.md"
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


PROMPT_HEADER = """Below is a grouped-feedback document an author created after extracting 142 comments from their academic paper draft (a preprint titled "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"). The 142 comments were the author's own annotations on the draft. The grouped-feedback document organizes them into 10 categories and proposes three sequencing options.

I want your review of THIS GROUPING DOCUMENT, not the paper itself.

Your job:
1. Is the grouping coherent? Are any items mis-categorized?
2. Are any patterns or themes missed?
3. Is the effort estimation reasonable?
4. Is the recommended sequencing (Options 1/2/3) sound? Would you propose a different order?
5. What single change to the grouping or sequencing would have the highest leverage?
6. Flag any items the author should reconsider — places where you suspect the comment is wrong, the grouping is wrong, or the recommended fix is misguided.

The raw 142-comment extraction is also included below for reference, so you can sanity-check the grouping against the original comments.

Be specific. Cite group letters (A, B, C, etc.) and comment numbers. Be honest about disagreement.

---

# GROUPED FEEDBACK DOCUMENT

"""


def review_gemini(payload_text: str, key: str) -> tuple[str, str]:
    label = "Gemini 2.5 Pro"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": payload_text}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 16384},
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
        payload["temperature"] = 0.3
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
        "temperature": 0.3,
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


def save_review(label: str, text: str, payload_chars: int) -> Path:
    slug = slug_for(label)
    out = OUT_DIR / f"v11_9_10_panel_grouped_feedback_{slug}_20260511.md"
    body = [
        f"# {label} review of grouped feedback — v11.9.10",
        f"Reviewer: {label}",
        "Date: 2026-05-11",
        "Reviewed: docs/reviews/v11_9_10_comments_review_grouped_20260511.md",
        f"Payload size: {payload_chars:,} chars (~{payload_chars//4:,} tokens)",
        "Prompt: Generic review of the grouping document + 142 raw comments for context",
        "",
        "---",
        "",
        text.strip(),
    ]
    out.write_text("\n".join(body), encoding="utf-8")
    return out


def main() -> int:
    grouped_text = GROUPED_FEEDBACK_PATH.read_text(encoding="utf-8")
    raw_text = RAW_COMMENTS_PATH.read_text(encoding="utf-8")
    payload_text = PROMPT_HEADER + grouped_text + "\n\n---\n\n# RAW 142-COMMENT EXTRACTION (for reference)\n\n" + raw_text
    payload_chars = len(payload_text)

    print(f"Payload size: {payload_chars:,} chars (~{payload_chars//4:,} tokens)\n")

    gemini_key = get_win_env("GEMINI_API_KEY")
    openai_key = get_win_env("OPENAI_API_KEY")
    mistral_key = get_win_env("MISTRAL_API_KEY")
    missing = [k for k, v in [("GEMINI", gemini_key), ("OPENAI", openai_key), ("MISTRAL", mistral_key)] if not v]
    if missing:
        print(f"Missing: {missing}")
        return 1

    print("Gemini 2.5 Pro ...")
    label, t = review_gemini(payload_text, gemini_key)
    out = save_review(label, t, payload_chars)
    print(f"  {'OK' if not t.startswith('ERROR') else 'FAIL'} ({len(t):,} chars) -> {out.name}")

    for model_id in ["gpt-5.4", "gpt-5", "gpt-4o"]:
        print(f"OpenAI {model_id} ...")
        label, t = review_openai(payload_text, openai_key, model_id)
        if not t.startswith("ERROR"):
            out = save_review(label, t, payload_chars)
            print(f"  OK ({len(t):,} chars) -> {out.name}")
            break
        print(f"  FAIL: {t[:200]}")

    print("Mistral Large ...")
    label, t = review_mistral(payload_text, mistral_key)
    out = save_review(label, t, payload_chars)
    print(f"  {'OK' if not t.startswith('ERROR') else 'FAIL'} ({len(t):,} chars) -> {out.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
