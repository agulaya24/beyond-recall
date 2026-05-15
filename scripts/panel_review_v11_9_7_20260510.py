"""v11.9.7 pre-submission panel review across 4 external providers.

Providers:
  - Google Gemini 2.5 Pro
  - OpenAI GPT-5 (with gpt-4o fallback)
  - Mistral Large
  - Cerebras Qwen3 235B Instruct

Anthropic Claude review is handled by a separate Claude Code sub-agent and is
NOT in this script.

Per-provider review is written to a single markdown file at
  docs/reviews/v11_9_7_panel_<provider>_20260510.md

Reviewers are instructed to assess 7 dimensions and produce specific,
actionable feedback in a fixed format that downstream distillation can parse.

The author's prior is binding context: "The paper is in a really good place.
Don't imagine there'll be any major changes." This is a validation pass.
"""
from __future__ import annotations

import json
import re
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
OUT_DIR.mkdir(exist_ok=True)


REVIEW_PROMPT = """You are a senior peer reviewer for arXiv preprint submission. The paper below is being prepared for upload. The author has explicitly stated: "The paper is in a really good place. Don't imagine there'll be any major changes." Treat this as a final validation pass, not a structural critique. Flag issues at the FACT, PROSE, or STRUCTURE level only if they would materially affect whether the paper holds up under scrutiny.

The paper is: "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"

Study design: N=14 historical subjects, 5 memory-system configurations (C5 baseline, C4a facts+Spec, C2a Spec only, C3 commercial memory systems, C1 full corpus), 5-judge primary LLM panel, Haiku 4.5 as main response model with Tier 2 cross-provider replication on Sonnet 4.6 + Gemini 2.5 Pro.

Review across these 7 DIMENSIONS:

1. Argument integrity: Does each major claim follow from the evidence? Logical gaps, unsupported leaps, framing/data mismatches?
2. Prose quality: Run-on sentences, semicolons/colons piling up, em-dash use (author hates em-dashes), unclear referents, awkward transitions.
3. Structure and flow: Sections in the right order? Does §1 land the thesis? Does §5 give discussion rather than metric recap? Are §6/§7 honest about limitations?
4. Numerical and factual consistency: Cross-check numbers between abstract, §1.3 callout, §4 body, §5 synthesis, tables. Flag any inconsistency.
5. Citation and reference handling: External references (NLA, Chen persona vectors, Letta, Mem0, etc.) cited where they should be? Uncited claims needing attribution?
6. Reproducibility and provenance: Scripts/data paths plausible? Does §8 give enough to redo the experiments?
7. Tone and positioning: Agentic-future framing landing? "Interpretive layer" / "Spec" / "Representational Accuracy" terminology consistent? Commercial/GTM language slipping into the science prose?

OUTPUT FORMAT (use exactly this structure):

## Verdict
One of: READY / READY-WITH-MINOR-FIXES / NEEDS-MINOR-REVISION / NEEDS-MAJOR-REVISION

## Launch-blocking issues
(Empty list expected given author prior. If you flag any, justify why this is launch-blocking rather than substantive.)

## Substantive issues (worth fixing pre-submission)
For each:
- Issue: [specific claim or passage]
- Location: §X.Y or paragraph context
- Why it matters: [1 sentence]
- Suggested fix: [specific edit, not vague guidance]

## Stylistic / nice-to-have
Same format. Keep to 3-10 items max.

## What the paper does well
3-5 brief bullets.

## Dimension scores (1-10)
Argument integrity:
Prose quality:
Structure and flow:
Numerical/factual consistency:
Citation/reference handling:
Reproducibility/provenance:
Tone and positioning:
Overall:

Be direct and specific. "Section 5 needs work" is useless; "§5.3 paragraph 2 conflates retrieval-overlap divergence with retrieval-grounding divergence" is useful.

---

PAPER:

{paper}
"""


def get_win_env(key: str) -> str:
    r = subprocess.run(
        ["powershell", "-Command", f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True,
    )
    return r.stdout.strip()


def load_paper() -> str:
    text = PAPER_PATH.read_text(encoding="utf-8")
    # Strip HTML comments (internal review notes)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return text.strip()


def post_json(url: str, payload: dict, headers: dict, timeout: int = 300) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def review_gemini(paper: str, key: str) -> tuple[str, str]:
    label = "Gemini 2.5 Pro"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": REVIEW_PROMPT.format(paper=paper)}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 8192},
    }
    try:
        data = post_json(url, payload, {"Content-Type": "application/json"}, timeout=600)
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return label, text
    except Exception as e:
        return label, f"ERROR: {e}"


def review_openai(paper: str, key: str) -> tuple[str, str]:
    label = "OpenAI GPT-5"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    for model_id in ["gpt-5", "gpt-4o-2024-11-20", "gpt-4o"]:
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": REVIEW_PROMPT.format(paper=paper)}],
            "temperature": 0.2,
            "max_tokens": 8192,
        }
        # GPT-5 family doesn't take temperature on all variants; retry without if needed
        for attempt in range(2):
            try:
                data = post_json(url, payload, headers, timeout=600)
                text = data["choices"][0]["message"]["content"]
                return f"OpenAI {model_id}", text
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="replace")[:400]
                # Some new models reject `temperature` or `max_tokens` — strip and retry
                if attempt == 0 and ("temperature" in body or "max_tokens" in body or "unsupported" in body.lower()):
                    payload.pop("temperature", None)
                    payload.pop("max_tokens", None)
                    payload["max_completion_tokens"] = 8192
                    continue
                print(f"  [{label} {model_id}] HTTP {e.code}: {body[:200]}")
                break
            except Exception as e:
                print(f"  [{label} {model_id}] ERROR: {e}")
                break
    return label, "ERROR: all OpenAI models failed"


def review_mistral(paper: str, key: str) -> tuple[str, str]:
    label = "Mistral Large"
    url = "https://api.mistral.ai/v1/chat/completions"
    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": REVIEW_PROMPT.format(paper=paper)}],
        "temperature": 0.2,
        "max_tokens": 8192,
    }
    try:
        data = post_json(url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}, timeout=600)
        text = data["choices"][0]["message"]["content"]
        return label, text
    except Exception as e:
        return label, f"ERROR: {e}"


def review_cerebras(paper: str, key: str) -> tuple[str, str]:
    label = "Cerebras Qwen3 235B"
    # Cerebras context window for this model is ~131k; v11.9.7 paper is well within
    paper_trunc = paper[:120000] + ("\n\n[Paper truncated for API limit]" if len(paper) > 120000 else "")
    url = "https://api.cerebras.ai/v1/chat/completions"
    payload = {
        "model": "qwen-3-235b-a22b-instruct-2507",
        "messages": [{"role": "user", "content": REVIEW_PROMPT.format(paper=paper_trunc)}],
        "temperature": 0.2,
        "max_tokens": 8192,
    }
    for attempt in range(3):
        try:
            data = post_json(url, payload, {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}, timeout=600)
            text = data["choices"][0]["message"]["content"]
            return label, text
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                print(f"  [{label}] rate limited, waiting 45s...")
                time.sleep(45)
                continue
            return label, f"ERROR: HTTP {e.code}: {e.read().decode()[:200]}"
        except Exception as e:
            return label, f"ERROR: {e}"
    return label, "ERROR: all attempts exhausted"


PROVIDER_SLUGS = {
    "Gemini 2.5 Pro": "gemini_2_5_pro",
    "Mistral Large": "mistral_large",
    "Cerebras Qwen3 235B": "cerebras_qwen3_235b",
}


def slug_for(label: str) -> str:
    if label.startswith("OpenAI"):
        return "openai_" + label.split()[-1].replace("-", "_").replace(".", "_")
    return PROVIDER_SLUGS.get(label, label.lower().replace(" ", "_"))


def save_review(label: str, text: str) -> Path:
    slug = slug_for(label)
    out = OUT_DIR / f"v11_9_7_panel_{slug}_20260510.md"
    body = [
        f"# {label} review — v11.9.7",
        f"Reviewer: {label}",
        "Date: 2026-05-10",
        "Paper: docs/beyond_recall_v11_9_7_draft.md",
        "",
        "---",
        "",
        text.strip(),
    ]
    out.write_text("\n".join(body), encoding="utf-8")
    return out


def main() -> int:
    print("Loading API keys...")
    gemini_key = get_win_env("GEMINI_API_KEY")
    openai_key = get_win_env("OPENAI_API_KEY")
    mistral_key = get_win_env("MISTRAL_API_KEY")
    cerebras_key = get_win_env("CEREBRAS_API_KEY")
    missing = [k for k, v in [("GEMINI", gemini_key), ("OPENAI", openai_key), ("MISTRAL", mistral_key), ("CEREBRAS", cerebras_key)] if not v]
    if missing:
        print(f"Missing: {missing}")
        return 1

    print(f"Loading {PAPER_PATH.name}...")
    paper = load_paper()
    print(f"Paper: {len(paper):,} chars, ~{len(paper)//4:,} tokens\n")

    results: list[tuple[str, str, Path]] = []
    for name, fn, key in [
        ("Gemini", review_gemini, gemini_key),
        ("OpenAI", review_openai, openai_key),
        ("Mistral", review_mistral, mistral_key),
        ("Cerebras", review_cerebras, cerebras_key),
    ]:
        print(f"Sending to {name}...")
        label, text = fn(paper, key)
        out = save_review(label, text)
        marker = "OK" if not text.startswith("ERROR") else "FAIL"
        print(f"  [{label}] {marker} ({len(text):,} chars) -> {out.name}")
        results.append((label, text[:200] if text.startswith("ERROR") else "OK", out))

    print("\n=== Summary ===")
    for label, status, out in results:
        print(f"  {label}: {status}")
        print(f"    {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
