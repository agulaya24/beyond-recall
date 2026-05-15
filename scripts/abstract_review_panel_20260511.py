"""Focused abstract-review panel for the v11.9.9 abstract.

Sends only:
  - The new abstract (223 words)
  - §1.1 opener (alignment context)
  - §5.8 closing remarks (alignment context)
  - The §1.3 headline findings (for completeness check)
  - 8 peer-paper abstracts (Twin-2K, PersonaGym, Persona Vectors, Mem0,
    MemGPT, LongMemEval, Zep, LoCoMo) for stylistic calibration

Reviewers asked: (1) does the abstract land? (2) is each sentence pulling
weight? (3) are major findings represented qualitatively? (4) compare to
peer abstracts. (5) name specific edits.

Providers (same as v11.9.8 panel): Gemini 2.5 Pro, OpenAI gpt-5.4 (with
gpt-5/gpt-4o fallback), Mistral Large. Anthropic Claude handled separately
by sub-agent.
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
PAPER_PATH = REPO / "docs" / "beyond_recall_v11_9_9_draft.md"
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


def extract_section_body(text: str, anchor: str, stop_anchor: str) -> str:
    m = re.search(re.escape(anchor) + r".*?" + re.escape(stop_anchor), text, flags=re.DOTALL)
    return m.group(0)[:len(anchor)+1500].strip() if m else ""


ABSTRACT_TEXT = """AI is moving from a tool a person uses to an agent that acts on a person's behalf, and that shift changes what memory must do for a specific individual. State of the art AI memory has been optimizing for recall: whether the system retrieves the right facts. Recall does not capture how accurately a system represents the way a specific person reasons. **Representational accuracy** is the AI-side property: how faithfully a system's internal model of a person captures that person's interpretive patterns. A **Behavioral Specification** operationalizes it as a static document encoding those patterns, served to a frontier model as context. Across public-domain autobiographies, scored on held-out passages by a calibrated LLM-judge panel, the matched Specification produces a categorical shift in the model's answers. The lift is largest where pretraining covers the subject least. The Specification recovers most of the predictive performance of the full source corpus at a fraction of the context cost. A different person's Specification served in place degrades accuracy below baseline; matched content does the work, not the structure of the prompt. Given identical input, leading memory systems disagree on which facts are most relevant to the same question. As AI shifts from tool to agent, representational accuracy of a specific person becomes the structural primitive for behavioral alignment. Pipeline source and study repository at `github.com/agulaya24/BaseLayer` and `github.com/agulaya24/beyond-recall`."""

HEADLINE_FINDINGS = """The paper's §1.3 lists six headline findings:
1. **Gradient.** Every low-baseline subject improved with the Spec; per-subject mean lift +0.89 points on 1-5 rubric; 78.6% of questions improve.
2. **Per-question interpretive lift.** The Spec moves 55% of low-baseline questions across at least one rubric anchor upward; 18% cross two or more; 5.9% cross three or more.
3. **Compression.** The Spec recovers 76% of what the corpus delivers at ~25× less context.
4. **Content specificity.** Wrong Spec drops accuracy below baseline (Δ=-0.25); correct Spec lifts above (Δ=+0.35); random-derangement Δ=+0.15.
5. **Memory-system layering.** Spec lifts 3 of 4 commercial systems on aggregate (Mem0, Letta, Zep positive; Supermemory not). Per-question anchor crossings 20-36% across systems.
6. **Hedging reduction.** Spec collapses baseline hedging from 41.2% to 0.4%. Wrong-Spec keeps hedging at 60.6%."""

S1_1_OPENER = """§1.1 opens: "AI is moving from a tool a person uses to an agent that acts on a person's behalf, and that shift changes what 'memory' must do for a specific individual. State of the art AI memory has been optimizing for recall as the success metric. The four leading systems (Zep, Letta, Mem0, and Supermemory) compete on standard recall benchmarks such as LOCOMO and LongMemEval, reporting accuracies in roughly the 70% to 93% range. Optimizing further on recall leaves something more fundamental unmeasured. This paper examines how recall is one part of memory, and how the function of memory is dictated by how an individual processes the facts and experiences of their life." """

S5_8_CLOSING = """§5.8 closes: "What the paper has done is operationalize a representational-accuracy measure of an interpretive layer, and demonstrate that a representation of this kind can be built within the resources and constraints of today's frontier AI systems. The result is a measurable proxy for whether an AI knows enough about a specific person to act in alignment with how that person actually reasons. The forward-looking commitment is that the future of human-AI alignment, particularly as agents take on a larger share of the actions individuals delegate to AI, requires this kind of representation as a structural primitive. An AI agent acting on behalf of someone cannot align with that person's reasoning without representing it. As AI integrates into more of everyday life through agents, accurate individual representation is the structural problem that needs to be addressed, not a feature that gets added later." """

PEER_ABSTRACTS = """Peer-paper abstracts for stylistic calibration:

**Twin-2K (Toubia et al. 2025, arXiv:2505.17479, ~210 words):**
"LLM-based digital twin simulation, where large language models are used to emulate individual human behavior, holds great promise for research in AI, social science, and digital experimentation. However, progress in this area has been hindered by the scarcity of real, individual-level datasets that are both large and publicly available. This lack of high-quality ground truth limits both the development and validation of digital twin methodologies. To address this gap, we introduce a large-scale, public dataset designed to capture a rich and holistic view of individual human behavior. We survey a representative sample of N=2,058 participants across four waves with 500 questions in total, covering a comprehensive battery of demographic, psychological, economic, personality, and cognitive measures, as well as replications of behavioral economics experiments and a pricing survey. The final wave repeats tasks from earlier waves to establish a test-retest accuracy baseline. Initial analyses suggest the data are of high quality and show promise for constructing digital twins that predict human behavior well at the individual and aggregate levels. By making the full dataset publicly available, we aim to establish a valuable testbed for the development and benchmarking of LLM-based persona simulations."

**Persona Vectors (Chen et al. 2025, arXiv:2507.21509, ~155 words):**
"Large language models interact with users through a simulated 'Assistant' persona. While the Assistant is typically trained to be helpful, harmless, and honest, it sometimes deviates from these ideals. In this paper, we identify directions in the model's activation space-persona vectors-underlying several traits, such as evil, sycophancy, and propensity to hallucinate. We confirm that these vectors can be used to monitor fluctuations in the Assistant's personality at deployment time. We then apply persona vectors to predict and control personality shifts that occur during training. We find that both intended and unintended personality changes after finetuning are strongly correlated with shifts along the relevant persona vectors. These shifts can be mitigated through post-hoc intervention, or avoided in the first place with a new preventative steering method. Our method for extracting persona vectors is automated and can be applied to any personality trait of interest, given only a natural-language description."

**PersonaGym (Samuel et al. 2025, arXiv:2407.18416, ~130 words):**
"Persona agents, which are LLM agents conditioned to act according to an assigned persona, enable contextually rich and user aligned interactions across domains like education and healthcare. However, evaluating how faithfully these agents adhere to their personas remains a significant challenge, particularly in free-form settings that demand consistency across diverse, persona-relevant environments. We introduce PersonaGym, the first dynamic evaluation framework for persona agents, and PersonaScore, a human-aligned automatic metric grounded in decision theory that enables comprehensive large-scale evaluation. Our evaluation of 10 leading LLMs across 200 personas and 10,000 questions reveals significant advancement opportunities. Importantly, increased model size and complexity do not necessarily enhance persona agent capabilities, underscoring the need for algorithmic and architectural innovation toward faithful, performant persona agents."

**Mem0 (Chhikara et al. 2025, arXiv:2504.19413, ~245 words; DENSE example):**
"Large Language Models (LLMs) have demonstrated remarkable prowess in generating contextually coherent responses, yet their fixed context windows pose fundamental challenges for maintaining consistency over prolonged multi-session dialogues. We introduce Mem0, a scalable memory-centric architecture that addresses this issue by dynamically extracting, consolidating, and retrieving salient information from ongoing conversations. Building on this foundation, we further propose an enhanced variant that leverages graph-based memory representations to capture complex relational structures among conversational elements. Through comprehensive evaluations on LOCOMO benchmark, we systematically compare our approaches against six baseline categories. Empirical results show that our methods consistently outperform all existing memory systems. Notably, Mem0 achieves 26% relative improvements in the LLM-as-a-Judge metric over OpenAI, while Mem0 with graph memory achieves around 2% higher overall score than the base configuration. Beyond accuracy gains, we also markedly reduce computational overhead. In particular, Mem0 attains a 91% lower p95 latency and saves more than 90% token cost, offering a compelling balance between advanced reasoning capabilities and practical deployment constraints."

**MemGPT/Letta (Packer et al. 2023, arXiv:2310.08560, ~155 words):**
"Large language models (LLMs) have revolutionized AI, but are constrained by limited context windows, hindering their utility in tasks like extended conversations and document analysis. To enable using context beyond limited context windows, we propose virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems that provide the appearance of large memory resources through data movement between fast and slow memory. Using this technique, we introduce MemGPT, a system that intelligently manages different memory tiers in order to effectively provide extended context within the LLM's limited context window. We evaluate our OS-inspired design in two domains where the limited context windows of modern LLMs severely handicaps their performance: document analysis and multi-session chat. We release MemGPT code and data for our experiments at https://memgpt.ai." """

PROMPT = """You are reviewing the abstract of an arXiv preprint. The author's binding direction:
- Qualitative-focused (no specific numbers like "14 subjects" or "Jaccard 0.08")
- Declarative voice; no filler ("rather than a marginal nudge," "we find that," "showing that")
- Each sentence must be curated and pulling weight
- Include code link in close (MemGPT pattern)
- Major headline findings adapted, not all six

The paper's title: "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"

Below: (A) the current abstract, (B) §1.1 opener for alignment check, (C) §5.8 closing for alignment check, (D) the six headline findings, (E) peer-paper abstracts for stylistic calibration.

YOUR JOB — produce structured feedback:

## Verdict
[READY / READY-WITH-MINOR-FIXES / NEEDS-REVISION]

## Per-sentence audit
For each sentence of the abstract:
- Sentence number + brief label (e.g., "S1 — agentic-future opener")
- Pulling weight? [YES / WEAK / FILLER]
- If WEAK or FILLER: specific edit

## Coverage of major findings
For each of the six §1.3 findings, mark whether the abstract represents it adequately:
- Gradient: [present / partial / absent]
- Per-question interpretive lift: [present / partial / absent]
- Compression: [present / partial / absent]
- Content specificity (wrong-Spec): [present / partial / absent]
- Memory-system layering: [present / partial / absent]
- Hedging reduction: [present / partial / absent]
Flag any "absent" finding that you think should be added.

## Stylistic comparison to peers
- Length vs peers (currently ~223 words; Persona Vectors 155w, PersonaGym 130w, Twin-2K 210w, MemGPT 155w, Mem0 245w)
- Where does the abstract sit on the dense ↔ compact axis?
- Specific peer abstract whose style most resembles what this should aim for?

## Alignment check
- Does the abstract's opening mirror §1.1 voice well?
- Does the abstract's close mirror §5.8 thesis well?

## Top 3 specific edits
The single most-impactful one-sentence rewrites or cuts that would tighten the abstract.

## What the abstract does well
3-5 brief bullets.

Be specific. Quote sentences when you flag them.

---

## A. CURRENT ABSTRACT (~223 words)

{abstract}

---

## B. §1.1 OPENER

{s11}

---

## C. §5.8 CLOSING

{s58}

---

## D. SIX HEADLINE FINDINGS FROM §1.3

{findings}

---

## E. PEER-PAPER ABSTRACTS

{peers}
"""


def review_gemini(payload_text: str, key: str) -> tuple[str, str]:
    label = "Gemini 2.5 Pro"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": payload_text}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 8192},
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


def review_mistral(payload_text: str, key: str) -> tuple[str, str]:
    label = "Mistral Large"
    url = "https://api.mistral.ai/v1/chat/completions"
    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": payload_text}],
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
    out = OUT_DIR / f"v11_9_9_abstract_{slug}_20260511.md"
    body = [
        f"# {label} abstract review — v11.9.9",
        f"Reviewer: {label}",
        "Date: 2026-05-11",
        "Paper: docs/beyond_recall_v11_9_9_draft.md",
        "Focus: abstract only (per-sentence audit + headline-finding coverage + peer-stylistic comparison)",
        "",
        "---",
        "",
        text.strip(),
    ]
    out.write_text("\n".join(body), encoding="utf-8")
    return out


def main() -> int:
    payload_text = PROMPT.format(
        abstract=ABSTRACT_TEXT,
        s11=S1_1_OPENER,
        s58=S5_8_CLOSING,
        findings=HEADLINE_FINDINGS,
        peers=PEER_ABSTRACTS,
    )

    print(f"Prompt size: ~{len(payload_text)//4} tokens, {len(payload_text):,} chars\n")

    gemini_key = get_win_env("GEMINI_API_KEY")
    openai_key = get_win_env("OPENAI_API_KEY")
    mistral_key = get_win_env("MISTRAL_API_KEY")
    missing = [k for k, v in [("GEMINI", gemini_key), ("OPENAI", openai_key), ("MISTRAL", mistral_key)] if not v]
    if missing:
        print(f"Missing: {missing}")
        return 1

    print("Gemini 2.5 Pro ...")
    label, t = review_gemini(payload_text, gemini_key)
    out = save_review(label, t)
    print(f"  {'OK' if not t.startswith('ERROR') else 'FAIL'} ({len(t):,} chars) -> {out.name}")

    for model_id in ["gpt-5.4", "gpt-5", "gpt-4o"]:
        print(f"OpenAI {model_id} ...")
        label, t = review_openai(payload_text, openai_key, model_id)
        if not t.startswith("ERROR"):
            out = save_review(label, t)
            print(f"  OK ({len(t):,} chars) -> {out.name}")
            break
        print(f"  FAIL: {t[:200]}")

    print("Mistral Large ...")
    label, t = review_mistral(payload_text, mistral_key)
    out = save_review(label, t)
    print(f"  {'OK' if not t.startswith('ERROR') else 'FAIL'} ({len(t):,} chars) -> {out.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
