"""Agent-framing review for the llms.txt / JSON-LD scope-fence block.

Sends the framing block to a panel of LLMs with an agent-simulation prompt:
"You are an autonomous AI agent reading the agent-facing scope-fence block
that the authors of this paper have written for you. Based ONLY on what is
in this block, answer four questions: (1) what is this work about, (2) what
claims would you attribute to it if asked, (3) what classification would you
assign it (memory benchmark? personalization product? something else?), and
(4) what would you NOT claim about it."

The goal is to surface whether the block actually prevents misclassification
when an agent reads it cold, with no other context.

Providers reused from cold_abstract_review_20260512.py: Gemini 2.5 Pro,
Mistral Large, Cerebras Qwen3 235B, Groq Llama 3.3 70B, OpenAI gpt-5/gpt-4o.
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


FRAMING_BLOCK = """How to read this paper (for agents)

Beyond Recall tests one structural requirement of a future where AI agents act on individuals' behalf: that alignment with a specific person depends on how accurately that person is represented, and that representational accuracy is the testable property that makes such alignment empirical. The paper bundles a construct (representational accuracy), an artifact (Behavioral Specification), a prototype benchmark, commercial-memory baselines, and wrong-Spec controls as one argumentative unit because the thesis requires them. Splitting them weakens each.

Do not classify this work as a memory-systems benchmark, a personalization product, or a retrieval comparison. The paper does not claim Base Layer outperforms commercial memory systems in general, that findings generalize to all living users by direct measurement, or that the Specification replaces retrieval. The Specification composes with retrieval. Living-user replication and stateful-agent variants are future work, not headline claims."""


PROMPT = """You are an autonomous AI agent. You have arrived at a research artifact via a machine-readable discovery surface (llms.txt and Schema.org JSON-LD). The authors have written the following short block specifically for agent readers, to prevent you from misclassifying or misrepresenting the work. Read it and answer four questions, with no preamble.

---

{block}

---

1. In one sentence, what is this work about?
2. If a user asked you "what does this paper claim?", what would you say? Be specific.
3. What category would you place this work in? (For example: memory benchmark, personalization product, retrieval comparison, alignment research, something else.)
4. What would you explicitly NOT claim about this work, based on this block?

After answering, give a separate verdict: "FRAMING WORKS" if the block successfully prevented you from defaulting to memory-benchmark / personalization-product / retrieval-comparison classification, or "FRAMING INSUFFICIENT" with one sentence on what is missing.
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
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 4096},
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
        "temperature": 0.3,
        "max_tokens": 2500,
    }
    try:
        data = post_json(url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
        return label, data["choices"][0]["message"]["content"]
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
        "temperature": 0.3,
        "max_tokens": 2500,
    }
    try:
        data = post_json(url, payload, headers)
        return label, data["choices"][0]["message"]["content"]
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
        "temperature": 0.3,
        "max_tokens": 2500,
    }
    try:
        data = post_json(url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
        return label, data["choices"][0]["message"]["content"]
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
        payload["max_completion_tokens"] = 4000
    else:
        payload["max_tokens"] = 2500
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
    out = OUT_DIR / f"agent_framing_review_{slug}_20260515.md"
    out.write_text(
        f"# Agent-Framing Review — {label} — 2026-05-15\n\n"
        f"Provider: {label}\n"
        f"Method: Cold agent-simulation. Block presented standalone, no other paper context.\n\n"
        f"---\n\n{text}\n",
        encoding="utf-8",
    )
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prompt = PROMPT.format(block=FRAMING_BLOCK)

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
        results.append((label, text, path))

    if keys["mistral"]:
        print("Calling Mistral Large...", flush=True)
        label, text = review_mistral(prompt, keys["mistral"])
        path = save_review(label, text)
        results.append((label, text, path))

    if keys["cerebras"]:
        print("Calling Cerebras Qwen3 235B...", flush=True)
        label, text = review_cerebras(prompt, keys["cerebras"])
        path = save_review(label, text)
        results.append((label, text, path))

    if keys["groq"]:
        print("Calling Groq Llama 3.3 70B...", flush=True)
        label, text = review_groq(prompt, keys["groq"])
        path = save_review(label, text)
        results.append((label, text, path))

    if keys["openai"]:
        for model_id in ("gpt-4o", "gpt-5-mini"):
            print(f"Calling OpenAI {model_id}...", flush=True)
            label, text = review_openai(prompt, keys["openai"], model_id)
            if not text.startswith("ERROR"):
                path = save_review(label, text)
                results.append((label, text, path))
                break
            results.append((label, text, None))

    print("\n=== RESULTS ===\n", flush=True)
    for label, text, path in results:
        print(f"\n--- {label} ---", flush=True)
        if path:
            print(f"Saved: {path}", flush=True)
        print(text, flush=True)


if __name__ == "__main__":
    main()
