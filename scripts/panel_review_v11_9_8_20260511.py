"""v11.9.8 pre-submission panel review across 4 external providers.

Differences from `panel_review_v11_9_7_20260510.py`:
  - PAPER_PATH points at v11.9.8
  - OpenAI invocation routes gpt-5.x to `max_completion_tokens` (gpt-5 / gpt-5.4
    rejected `max_tokens` in the v11.9.7 run, returning empty content)
  - Cerebras dropped from the panel (TPM quota exhausted twice in the v11.9.7
    run; Groq fallback returned 403)
  - Output files named with `_20260511` suffix

Providers:
  - Google Gemini 2.5 Pro
  - OpenAI gpt-5.4 (with gpt-5 fallback)
  - Mistral Large
  - Anthropic Claude handled by a separate Claude Code sub-agent, NOT in this
    script.

Author prior (binding): "The paper is in a really good place." Validation
pass, not restructure.
"""
from __future__ import annotations

import json
import re
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
PAPER_PATH = REPO / "docs" / "beyond_recall_v11_9_8_draft.md"
OUT_DIR = REPO / "docs" / "reviews"

REVIEW_PROMPT = """You are a senior peer reviewer for arXiv preprint submission. The paper below is being prepared for upload. The author has explicitly stated: "The paper is in a really good place." Treat this as a final validation pass, not a structural critique. Flag issues at the FACT, PROSE, or STRUCTURE level only if they would materially affect whether the paper holds up under scrutiny.

The paper is: "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"

This is v11.9.8, which incorporated the prior v11.9.7 panel's distillation: number reconciliation (2.44/2.46 paper-wide lock, 23×→~25× compression, +0.71→+0.69 per-subject grain, 47→46 predicate count), headline-prose precision in §1.3 + abstract, Group C section-specific clarifications (§4.1 Franklin C4 footnote, §4.5 Letta column qualifier, §4.6.1 Tier 2 range explainer, §4.3 wrong-Spec pairing footnote, §5.5 Betley inline citation, §9 Betley reference added), broken-reference resolved (`rubric_handling_validity_full.json` regenerated), Mistral's misreads on Jaccard denominator and v1 pairings corrected, and a 5-instance em-dash pass.

Study design: N=14 historical subjects, 5 memory-system configurations (C5 baseline, C4a facts+Spec, C2a Spec only, C3 commercial memory systems, C8 raw corpus), 5-judge primary LLM panel, Haiku 4.5 as main response model with Tier 2 cross-provider replication on Sonnet 4.6 + Gemini 2.5 Pro.

Review across these 7 DIMENSIONS:

1. Argument integrity
2. Prose quality
3. Structure and flow
4. Numerical and factual consistency (especially: have the v11.9.8 reconciliations been applied cleanly? Any residual instances?)
5. Citation and reference handling (especially: §9 Betley entry placement; inline citations consistent)
6. Reproducibility and provenance
7. Tone and positioning

OUTPUT FORMAT (use exactly this structure):

## Verdict
One of: READY / READY-WITH-MINOR-FIXES / NEEDS-MINOR-REVISION / NEEDS-MAJOR-REVISION

## Launch-blocking issues
(Empty list expected.)

## Substantive issues (worth fixing pre-submission)
For each:
- Issue: [specific claim or passage]
- Location: §X.Y or line context
- Why it matters: [1 sentence]
- Suggested fix: [specific edit]

## Stylistic / nice-to-have
Same format. 3-10 items max.

## Did v11.9.8 fixes land cleanly?
Quick verification across the 17 distillation items applied in v11.9.8. Flag any item that did NOT propagate or that left residue.

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

Be direct and specific.

---

PAPER:

{paper}
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


def load_paper() -> str:
    text = PAPER_PATH.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return text.strip()


def post_json(url: str, payload: dict, headers: dict, timeout: int = 900) -> dict:
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
        data = post_json(url, payload, {"Content-Type": "application/json"})
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return label, text
    except Exception as e:
        return label, f"ERROR: {e}"


def review_openai(paper: str, key: str, model_id: str) -> tuple[str, str]:
    label = f"OpenAI {model_id}"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    payload: dict = {
        "model": model_id,
        "messages": [{"role": "user", "content": REVIEW_PROMPT.format(paper=paper)}],
    }
    if needs_new_param(model_id):
        payload["max_completion_tokens"] = 16384
    else:
        payload["max_tokens"] = 8192
        payload["temperature"] = 0.2
    try:
        data = post_json(url, payload, headers)
        choice = data["choices"][0]
        text = (choice.get("message") or {}).get("content") or ""
        if not text.strip():
            return label, f"ERROR: empty content (finish_reason={choice.get('finish_reason')})"
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:600]
        return label, f"ERROR: HTTP {e.code}: {body}"
    except Exception as e:
        return label, f"ERROR: {e}"


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


def save_review(label: str, text: str) -> Path:
    slug = slug_for(label)
    out = OUT_DIR / f"v11_9_8_panel_{slug}_20260511.md"
    body = [
        f"# {label} review — v11.9.8",
        f"Reviewer: {label}",
        "Date: 2026-05-11",
        "Paper: docs/beyond_recall_v11_9_8_draft.md",
        "",
        "---",
        "",
        text.strip(),
    ]
    out.write_text("\n".join(body), encoding="utf-8")
    return out


def main() -> int:
    paper = load_paper()
    print(f"Paper: {len(paper):,} chars\n")

    gemini_key = get_win_env("GEMINI_API_KEY")
    openai_key = get_win_env("OPENAI_API_KEY")
    mistral_key = get_win_env("MISTRAL_API_KEY")
    missing = [k for k, v in [("GEMINI", gemini_key), ("OPENAI", openai_key), ("MISTRAL", mistral_key)] if not v]
    if missing:
        print(f"Missing: {missing}")
        return 1

    results = []

    print("Gemini 2.5 Pro ...")
    label, text = review_gemini(paper, gemini_key)
    out = save_review(label, text)
    print(f"  {'OK' if not text.startswith('ERROR') else 'FAIL'} ({len(text):,} chars) -> {out.name}")
    results.append((label, text.startswith("ERROR"), out))

    # OpenAI: try gpt-5.4 first, fall back to gpt-5
    for model_id in ["gpt-5.4", "gpt-5", "gpt-4o"]:
        print(f"OpenAI {model_id} ...")
        label, text = review_openai(paper, openai_key, model_id)
        if not text.startswith("ERROR"):
            out = save_review(label, text)
            print(f"  OK ({len(text):,} chars) -> {out.name}")
            results.append((label, False, out))
            break
        print(f"  FAIL: {text[:200]}")
    else:
        results.append(("OpenAI (all failed)", True, None))

    print("Mistral Large ...")
    label, text = review_mistral(paper, mistral_key)
    out = save_review(label, text)
    print(f"  {'OK' if not text.startswith('ERROR') else 'FAIL'} ({len(text):,} chars) -> {out.name}")
    results.append((label, text.startswith("ERROR"), out))

    print("\n=== Summary ===")
    for label, failed, out in results:
        print(f"  {label}: {'FAIL' if failed else 'OK'}{f' -> {out.name}' if out else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
