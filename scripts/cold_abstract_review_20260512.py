"""Cold panel review for the locked v11.9.11 abstract.

Sends only the abstract text (with placeholder URLs) to a panel of LLM
providers with no direction, no rubric, no structure. Just a one-line
prompt asking for review. The intent is to surface unsolicited feedback
that we have not primed for, so reviewers volunteer what they see.

Providers: Gemini 2.5 Pro, Mistral Large, Cerebras Qwen3 235B, Groq
Llama 3.3 70B, OpenAI (gpt-5/gpt-4o fallback). Anthropic Claude handled
separately in-conversation.

Aarik instruction: "send this to all the language model providers ...
don't include actual links just include placeholders for the links and
just have them give a sort of a cold review on this don't give them any
direction."
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
OUT_DIR = REPO / "docs" / "reviews"


ABSTRACT_TEXT = """If an AI agent plays a larger role in everyday human decisions, those decisions must align with its user. We introduce **representational accuracy** to measure how faithfully a system has captured a person's interpretive structure. An **interpretive layer** is operationalized as a **Behavioral Specification**. Our reference implementation aggressively compresses a person's data into interpretive patterns, served as context to a language model. We evaluate the Specification on a prototype benchmark of held-out behavioral predictions scored by a calibrated 5-judge LLM panel. We test it independently and in composition with a range of context conditions: full raw corpus, full extracted facts, and four commercial memory systems (Mem0, Letta, Supermemory, Zep).

Across 14 public-domain autobiographical corpora, the Specification lifts representational accuracy in aggregate and nearly eliminates model hedging. It recovers most of what the raw corpus delivers, at a fraction of the context cost. Lift grows as the model's pretraining coverage of the subject decreases, suggesting the population of relevance is anyone not adequately represented in pretraining. Lift is greatest on interpretation-required questions, where providing an interpretive layer enables model behavior that extracted facts or raw corpus do not. Conversely, on recall-required questions, this layer can interfere rather than help.

We conclude that representational accuracy is distinct from recall and that human-AI alignment is bounded by how accurately the user is represented. Representational accuracy makes that alignment testable.

Study repository: [STUDY_REPO_URL]
Pipeline source: [PIPELINE_REPO_URL]"""


COLD_PROMPT = """Please review the following arXiv preprint abstract. Provide your honest feedback.

---

{abstract}
"""


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


def post_json(url: str, payload: dict, headers: dict, timeout: int = 600) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def review_gemini(prompt: str, key: str) -> tuple[str, str]:
    label = "Gemini 2.5 Pro"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 8192},
    }
    try:
        data = post_json(url, payload, {"Content-Type": "application/json"})
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return label, text
    except Exception as e:
        return label, f"ERROR: {e}"


def review_mistral(prompt: str, key: str) -> tuple[str, str]:
    label = "Mistral Large"
    url = "https://api.mistral.ai/v1/chat/completions"
    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 4000,
    }
    try:
        data = post_json(url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
        text = data["choices"][0]["message"]["content"]
        return label, text
    except Exception as e:
        return label, f"ERROR: {e}"


def review_cerebras(prompt: str, key: str) -> tuple[str, str]:
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
    try:
        data = post_json(url, payload, headers)
        text = data["choices"][0]["message"]["content"]
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        return label, f"ERROR: HTTP {e.code}: {body}"
    except Exception as e:
        return label, f"ERROR: {e}"


def review_groq(prompt: str, key: str) -> tuple[str, str]:
    label = "Groq Llama 3.3 70B"
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 4000,
    }
    try:
        data = post_json(url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
        text = data["choices"][0]["message"]["content"]
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        return label, f"ERROR: HTTP {e.code}: {body}"
    except Exception as e:
        return label, f"ERROR: {e}"


def review_openai(prompt: str, key: str, model_id: str) -> tuple[str, str]:
    label = f"OpenAI {model_id}"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    payload: dict = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
    }
    if needs_new_param(model_id):
        payload["max_completion_tokens"] = 8000
    else:
        payload["max_tokens"] = 4000
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


def slug_for(label: str) -> str:
    if label.startswith("OpenAI"):
        return "openai_" + label.split()[-1].replace(".", "_").replace("-", "_").lower()
    if label.startswith("Gemini"):
        return "gemini_2_5_pro"
    if label.startswith("Mistral"):
        return "mistral_large"
    if label.startswith("Cerebras"):
        return "cerebras_qwen3_235b"
    if label.startswith("Groq"):
        return "groq_llama_3_3_70b"
    return label.lower().replace(" ", "_")


def save_review(label: str, text: str) -> Path:
    slug = slug_for(label)
    out = OUT_DIR / f"cold_abstract_review_{slug}_20260512.md"
    out.write_text(
        f"# Cold Abstract Review — {label} — 2026-05-12\n\n"
        f"Provider: {label}\n"
        f"Method: Single-shot review of locked v11.9.11 abstract. No rubric, no direction, no peer abstracts. Placeholder URLs.\n\n"
        f"---\n\n{text}\n",
        encoding="utf-8",
    )
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prompt = COLD_PROMPT.format(abstract=ABSTRACT_TEXT)

    keys = {
        "gemini": get_win_env("GEMINI_API_KEY"),
        "mistral": get_win_env("MISTRAL_API_KEY"),
        "cerebras": get_win_env("CEREBRAS_API_KEY"),
        "groq": get_win_env("GROQ_API_KEY"),
        "openai": get_win_env("OPENAI_API_KEY"),
    }

    results: list[tuple[str, str, Path | None]] = []

    if keys["gemini"]:
        print("Calling Gemini 2.5 Pro...", flush=True)
        label, text = review_gemini(prompt, keys["gemini"])
        path = save_review(label, text)
        results.append((label, text[:200] + "...", path))

    if keys["mistral"]:
        print("Calling Mistral Large...", flush=True)
        label, text = review_mistral(prompt, keys["mistral"])
        path = save_review(label, text)
        results.append((label, text[:200] + "...", path))

    if keys["cerebras"]:
        print("Calling Cerebras Qwen3 235B...", flush=True)
        label, text = review_cerebras(prompt, keys["cerebras"])
        path = save_review(label, text)
        results.append((label, text[:200] + "...", path))

    if keys["groq"]:
        print("Calling Groq Llama 3.3 70B...", flush=True)
        label, text = review_groq(prompt, keys["groq"])
        path = save_review(label, text)
        results.append((label, text[:200] + "...", path))

    if keys["openai"]:
        for model_id in ("gpt-4o", "gpt-5-mini"):
            print(f"Calling OpenAI {model_id}...", flush=True)
            label, text = review_openai(prompt, keys["openai"], model_id)
            if not text.startswith("ERROR"):
                path = save_review(label, text)
                results.append((label, text[:200] + "...", path))
                break
            else:
                print(f"  {label}: {text[:200]}", flush=True)

    print("\n--- Summary ---", flush=True)
    for label, preview, path in results:
        print(f"{label}: saved to {path}", flush=True)
        print(f"  Preview: {preview}\n", flush=True)


if __name__ == "__main__":
    main()
