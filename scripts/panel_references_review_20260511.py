"""Focused-references panel review for v11.9.8.

Distinct from the body-paper panel review at panel_review_v11_9_8_20260511.py.
This one ships:
  - The §9 References block in isolation (so the reviewer focuses)
  - The complete list of inline citations extracted from the body
  - The Acknowledgments paragraph (to verify named-but-uncited works)

Each reviewer is asked to assess:
  1. Completeness of §9 (is every body-cited work present?)
  2. Accuracy (right authors, year, title, venue, arXiv ID)
  3. Inline-citation hygiene (every body cite has a §9 home)
  4. Citation-convention compliance (per the §9 preamble)
  5. Orphans in either direction

Providers (same as v11.9.8 body panel):
  - Google Gemini 2.5 Pro
  - OpenAI gpt-5.4 (with gpt-5 / gpt-4o fallback; uses max_completion_tokens for gpt-5.x)
  - Mistral Large
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


def extract_references_block(text: str) -> str:
    """Return the §9 References block, header through next ## or EOF."""
    m = re.search(r"^## 9\. References.*?(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
    return m.group(0).strip() if m else ""


def extract_acknowledgments(text: str) -> str:
    """Return the Acknowledgments paragraph if present."""
    m = re.search(r"\*\*Acknowledgments\.\*\*.*?(?=\n\n\*\*|\n\n##|\Z)", text, flags=re.DOTALL)
    return m.group(0).strip() if m else ""


CITE_PATTERNS = [
    # "Smith et al. (2023)"
    r"\b([A-Z][a-zA-Z]+(?:\s+(?:and|&)\s+[A-Z][a-zA-Z]+)?)\s+et al\.\s*\(?(\d{4})\)?",
    # "(Smith et al., 2023)"
    r"\(([A-Z][a-zA-Z]+)\s+et al\.,?\s*(\d{4})\)",
    # "Smith (2023)" or "Smith 2023"
    r"\b([A-Z][a-zA-Z]+)\s+(?:\()?(\d{4})(?:\))?",
    # "Smith and Jones (2023)"
    r"\b([A-Z][a-zA-Z]+\s+(?:and|&)\s+[A-Z][a-zA-Z]+)\s+\((\d{4})\)",
]

ARXIV_RE = re.compile(r"arXiv\s*:?\s*(\d{4}\.\d{4,5})", re.IGNORECASE)


def extract_inline_citations(text: str, refs_block: str) -> list[dict]:
    """Heuristic citation extractor. Returns a deduplicated list with first-seen line."""
    body = text.replace(refs_block, "")  # strip refs block to avoid self-matches
    lines = body.splitlines()
    seen: dict[str, dict] = {}
    for i, line in enumerate(lines, 1):
        # Skip code blocks (rough)
        if line.startswith("```") or line.startswith("    "):
            continue
        # arXiv IDs
        for m in ARXIV_RE.finditer(line):
            key = f"arXiv:{m.group(1)}"
            if key not in seen:
                seen[key] = {"citation": key, "first_line": i, "context": line.strip()[:240]}
        # Author-year patterns — pick best-fit single match per author phrase
        for pat in CITE_PATTERNS:
            for m in re.finditer(pat, line):
                author = m.group(1).strip()
                year = m.group(2)
                # Filter obvious false positives
                if author.lower() in {"section", "table", "figure", "appendix", "equation", "the", "for", "and", "but", "in"}:
                    continue
                if not (1900 <= int(year) <= 2030):
                    continue
                key = f"{author} {year}"
                if key not in seen:
                    seen[key] = {"citation": key, "first_line": i, "context": line.strip()[:240]}
    # Return sorted by first occurrence
    return sorted(seen.values(), key=lambda d: d["first_line"])


PROMPT = """You are conducting a focused references / citations audit for an arXiv preprint. You are NOT reviewing the body of the paper; another reviewer is doing that in parallel. Your job is the references block and citation hygiene only.

The paper is titled "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization." Author: Aarik Gulaya.

The reference convention at the head of §9 reads:
"Citation conventions: All authors are listed when 3 or fewer; otherwise the first author plus 'et al.' Where a peer-reviewed venue is listed, the citation year is the venue year and the arXiv identifier is included as a durable preprint identifier that may predate the venue year."

You will see three blocks below: the §9 References block, the Acknowledgments paragraph, and a heuristic list of all inline citations extracted from the body. The inline list is a candidate set; some may be false positives (capitalized words followed by year numbers that aren't actually citations).

YOUR JOB — assess across these dimensions and produce structured output:

## Verdict
READY / READY-WITH-MINOR-FIXES / NEEDS-REVISION

## Reference-block accuracy
For each §9 entry, check:
- Author names (correctness, spelling, capitalization)
- Year (matches the cited venue, not a different year)
- Title (exact match to the actual paper)
- Venue (e.g., NeurIPS 2023, ICLR 2025, ACL 2024, arXiv preprint, etc.)
- arXiv ID (well-formed and resolves to the right paper)

For any entry where you doubt accuracy, say so plainly. Don't fabricate confidence.

## Citation-convention compliance
Check each §9 entry against the convention above:
- 3-or-fewer rule applied correctly?
- Year-of-venue (not year-of-arXiv) when both exist?
- arXiv ID format consistent across entries?
- Italics on journal/book titles?
- Capitalization/punctuation consistent?

Flag every deviation.

## Inline-citation completeness
For each inline citation in the heuristic list, judge:
- Is it actually a citation (not a false positive)?
- Does it resolve to an entry in §9?

Flag every real inline citation with NO §9 entry (orphan body citation).

## §9 entries not cited inline
List every §9 entry you can't find a corresponding inline cite for (orphan reference). The Acknowledgments paragraph counts as a valid mention if the entry is in §9.

## Acknowledgments cross-check
The Acknowledgments paragraph names specific researchers. Check that every named work has a §9 entry.

## Missing references (worth adding)
If the paper's prose obviously discusses a concept/finding that should have a citation but doesn't, flag it. Be conservative — only flag if a real, well-known reference should be there.

OUTPUT STRUCTURE (mirror exactly):

## Verdict
[READY / READY-WITH-MINOR-FIXES / NEEDS-REVISION]

## Issues
For each issue:
- Type: [Accuracy / Convention / Orphan-inline / Orphan-§9 / Acknowledgments / Missing-ref]
- Detail: [specific entry / inline citation / paragraph location]
- Severity: [launch-blocker / substantive / nice-to-have]
- Suggested fix: [specific edit]

## Per-entry verification table
| §9 entry | Status | Notes |
|---|---|---|

## What the reference block does well
3-5 short bullets.

---

§9 REFERENCES (verbatim):
{refs}

---

ACKNOWLEDGMENTS PARAGRAPH (verbatim):
{acks}

---

INLINE CITATIONS HEURISTIC LIST (line:citation:context):
{citations}
"""


def review_gemini(refs: str, acks: str, citations: str, key: str) -> tuple[str, str]:
    label = "Gemini 2.5 Pro"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": PROMPT.format(refs=refs, acks=acks, citations=citations)}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 8192},
    }
    try:
        data = post_json(url, payload, {"Content-Type": "application/json"})
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return label, text
    except Exception as e:
        return label, f"ERROR: {e}"


def review_openai(refs: str, acks: str, citations: str, key: str, model_id: str) -> tuple[str, str]:
    label = f"OpenAI {model_id}"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    payload: dict = {
        "model": model_id,
        "messages": [{"role": "user", "content": PROMPT.format(refs=refs, acks=acks, citations=citations)}],
    }
    if needs_new_param(model_id):
        payload["max_completion_tokens"] = 12000
    else:
        payload["max_tokens"] = 6000
        payload["temperature"] = 0.2
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


def review_mistral(refs: str, acks: str, citations: str, key: str) -> tuple[str, str]:
    label = "Mistral Large"
    url = "https://api.mistral.ai/v1/chat/completions"
    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": PROMPT.format(refs=refs, acks=acks, citations=citations)}],
        "temperature": 0.2,
        "max_tokens": 6000,
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
    out = OUT_DIR / f"v11_9_8_references_{slug}_20260511.md"
    body = [
        f"# {label} references review — v11.9.8",
        f"Reviewer: {label}",
        "Date: 2026-05-11",
        "Paper: docs/beyond_recall_v11_9_8_draft.md",
        "Focus: §9 References + inline-citation hygiene only (body paper reviewed separately).",
        "",
        "---",
        "",
        text.strip(),
    ]
    out.write_text("\n".join(body), encoding="utf-8")
    return out


def main() -> int:
    text = PAPER_PATH.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    refs = extract_references_block(text)
    acks = extract_acknowledgments(text)
    citations_list = extract_inline_citations(text, refs)
    citations_str = "\n".join(
        f"L{c['first_line']:4d}: {c['citation']} — {c['context']}"
        for c in citations_list
    )

    print(f"Refs block: {len(refs):,} chars")
    print(f"Acknowledgments: {len(acks):,} chars")
    print(f"Heuristic inline citations: {len(citations_list)}")
    print(f"Total prompt size estimate: ~{(len(refs) + len(acks) + len(citations_str) + len(PROMPT)) // 4} tokens\n")

    gemini_key = get_win_env("GEMINI_API_KEY")
    openai_key = get_win_env("OPENAI_API_KEY")
    mistral_key = get_win_env("MISTRAL_API_KEY")
    missing = [k for k, v in [("GEMINI", gemini_key), ("OPENAI", openai_key), ("MISTRAL", mistral_key)] if not v]
    if missing:
        print(f"Missing: {missing}")
        return 1

    print("Gemini 2.5 Pro ...")
    label, text_out = review_gemini(refs, acks, citations_str, gemini_key)
    out = save_review(label, text_out)
    print(f"  {'OK' if not text_out.startswith('ERROR') else 'FAIL'} ({len(text_out):,} chars) -> {out.name}")

    for model_id in ["gpt-5.4", "gpt-5", "gpt-4o"]:
        print(f"OpenAI {model_id} ...")
        label, text_out = review_openai(refs, acks, citations_str, openai_key, model_id)
        if not text_out.startswith("ERROR"):
            out = save_review(label, text_out)
            print(f"  OK ({len(text_out):,} chars) -> {out.name}")
            break
        print(f"  FAIL: {text_out[:200]}")

    print("Mistral Large ...")
    label, text_out = review_mistral(refs, acks, citations_str, mistral_key)
    out = save_review(label, text_out)
    print(f"  {'OK' if not text_out.startswith('ERROR') else 'FAIL'} ({len(text_out):,} chars) -> {out.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
