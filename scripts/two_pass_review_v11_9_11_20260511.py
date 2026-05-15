"""Two-pass external review on v11.9.11 (cold + reviewer-framed).

Two parallel passes against the same paper, run on the same provider panel.
Each pass uses a different prompt so we get two distinct lenses:

  PASS A (cold): minimal prompting; simulates a real-world reader's first
  encounter. Just the paper plus a one-line ask. Surfaces what actually
  lands without scaffolding, including what confuses or pushes the reader
  away.

  PASS B (reviewer-framed): explicit peer-reviewer prompt with structured
  output. Surfaces fixable issues at fact/prose/structure level.

Together: Pass A tells us how the paper reads; Pass B tells us what to fix.

Providers (mirroring the v11.9.7 / v11.9.8 / v11.9.10 panels):
  - Google Gemini 2.5 Pro
  - OpenAI gpt-5.4 (fallback chain: gpt-5, gpt-4o)
  - Mistral Large
  - (Anthropic Claude handled separately by sub-agent; not in this script.)

Output: 6 review files (3 providers × 2 passes) at:
  docs/reviews/v11_9_11_panel_cold_<slug>_20260511.md
  docs/reviews/v11_9_11_panel_review_<slug>_20260511.md
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
PAPER_PATH = REPO / "docs" / "beyond_recall_v11_9_11_draft.md"
OUT_DIR = REPO / "docs" / "reviews"

GPT5_PREFIXES = ("o1", "o3", "gpt-5")

# ---------- PASS A: Cold read ----------

COLD_PROMPT = """Please read the paper below and give me your honest first reaction.

What stood out, what landed, what confused you, what you'd push back on. Write the kind of response you would give a colleague who handed you a paper and asked "what do you think." Use whatever structure feels natural for that.

PAPER:

{paper}
"""

# ---------- PASS B: Reviewer-framed ----------

REVIEW_PROMPT = """You are a senior peer reviewer for arXiv preprint submission. The paper below is being prepared for upload. The author has stated: "The paper is in a really good place." Treat this as a final validation pass, not a structural critique. Flag issues at the FACT, PROSE, or STRUCTURE level only if they would materially affect whether the paper holds up under scrutiny.

The paper is: "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"

This is v11.9.11. Forked through v11.9.7 → v11.9.8 → v11.9.9 → v11.9.10 → v11.9.11. v11.9.11 specifically applied:
  - Pass 5 voice polish (3 edits)
  - Franklin/Hamerton precision audit (corrected: paper had said Franklin C4 scored by "2-judge legacy panel"; actual data has 4 judges)
  - Pass 6 cross-reference cleanup (7 Group F edits incl. floor/engaged subject naming, anchor-list comma consistency)
  - Pass 7 table column widths (14 tables, OOXML)
  - Pass 8 Group E content strengthening (all 3 §4.1 worked-example reframes; abstract bridge sentence on interpretation-heavy questions; Templo Mayor setup; Jaccard calibration anchor; Letta unique-fact note; Pattern 1 internal-bar dynamic)

Headline numbers and structural arguments are unchanged across v11.9.7 → v11.9.11.

Study design: N=14 historical subjects, 5 memory-system configurations (C5 baseline, C4a facts+Spec, C2a Spec only, C3 commercial memory systems, C8 raw corpus), 5-judge primary LLM panel, Haiku 4.5 main response model with Tier 2 cross-provider replication on Sonnet 4.6 + Gemini 2.5 Pro.

Review across these 7 DIMENSIONS:

1. Argument integrity
2. Prose quality
3. Structure and flow
4. Numerical and factual consistency (do v11.9.11 fixes land? Especially the Franklin C4 4-judge correction in §3.4.1 / §4.1 / §4.1.2)
5. Citation and reference handling
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

## Did the v11.9.11 changes land cleanly?
Verification across the Pass 5/6/7/8 + Franklin C4 fix. Flag any item that did NOT propagate or that left residue.

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


def review_openai(prompt: str, key: str, model_id: str) -> tuple[str, str]:
    label = f"OpenAI {model_id}"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    payload: dict = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
    }
    if needs_new_param(model_id):
        payload["max_completion_tokens"] = 16384
    else:
        payload["max_tokens"] = 8192
        payload["temperature"] = 0.4
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


def review_mistral(prompt: str, key: str) -> tuple[str, str]:
    label = "Mistral Large"
    url = "https://api.mistral.ai/v1/chat/completions"
    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
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


def save_review(pass_tag: str, label: str, text: str) -> Path:
    """pass_tag in {"cold", "review"}."""
    slug = slug_for(label)
    out = OUT_DIR / f"v11_9_11_panel_{pass_tag}_{slug}_20260511.md"
    body = [
        f"# {label} {pass_tag} pass — v11.9.11",
        f"Reviewer: {label}",
        f"Pass: {pass_tag}",
        "Date: 2026-05-11",
        "Paper: docs/beyond_recall_v11_9_11_draft.md",
        "",
        "---",
        "",
        text.strip(),
    ]
    out.write_text("\n".join(body), encoding="utf-8")
    return out


def run_pass(pass_tag: str, prompt_template: str, paper: str,
             gemini_key: str, openai_key: str, mistral_key: str) -> list[tuple[str, bool, Path | None]]:
    prompt = prompt_template.format(paper=paper)
    results: list[tuple[str, bool, Path | None]] = []
    print(f"\n=== PASS: {pass_tag} ===")

    print("Gemini 2.5 Pro ...")
    label, text = review_gemini(prompt, gemini_key)
    out = save_review(pass_tag, label, text)
    print(f"  {'OK' if not text.startswith('ERROR') else 'FAIL'} ({len(text):,} chars) -> {out.name}")
    results.append((label, text.startswith("ERROR"), out))

    for model_id in ["gpt-5.4", "gpt-5", "gpt-4o"]:
        print(f"OpenAI {model_id} ...")
        label, text = review_openai(prompt, openai_key, model_id)
        if not text.startswith("ERROR"):
            out = save_review(pass_tag, label, text)
            print(f"  OK ({len(text):,} chars) -> {out.name}")
            results.append((label, False, out))
            break
        print(f"  FAIL: {text[:200]}")
    else:
        results.append(("OpenAI (all failed)", True, None))

    print("Mistral Large ...")
    label, text = review_mistral(prompt, mistral_key)
    out = save_review(pass_tag, label, text)
    print(f"  {'OK' if not text.startswith('ERROR') else 'FAIL'} ({len(text):,} chars) -> {out.name}")
    results.append((label, text.startswith("ERROR"), out))

    return results


def main() -> int:
    paper = load_paper()
    print(f"Paper: {len(paper):,} chars")

    gemini_key = get_win_env("GEMINI_API_KEY")
    openai_key = get_win_env("OPENAI_API_KEY")
    mistral_key = get_win_env("MISTRAL_API_KEY")
    missing = [k for k, v in [("GEMINI", gemini_key), ("OPENAI", openai_key), ("MISTRAL", mistral_key)] if not v]
    if missing:
        print(f"Missing: {missing}")
        return 1

    all_results: dict[str, list] = {}
    for pass_tag, prompt_template in [("cold", COLD_PROMPT), ("review", REVIEW_PROMPT)]:
        all_results[pass_tag] = run_pass(pass_tag, prompt_template, paper, gemini_key, openai_key, mistral_key)

    print("\n=== Summary ===")
    for pass_tag in ("cold", "review"):
        print(f"\n[{pass_tag}]")
        for label, failed, out in all_results[pass_tag]:
            print(f"  {label}: {'FAIL' if failed else 'OK'}{f' -> {out.name}' if out else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
