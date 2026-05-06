"""Semantic-similarity duplication analysis for Letta stateful-agent memory blocks.

For each of Hamerton, Ebers, Babur: split the block into sentences, embed them
with all-MiniLM-L6-v2, compute pairwise cosine similarity, and report the
fraction of sentences that have at least one near-duplicate (other than themselves)
at thresholds 0.80 / 0.85 / 0.90 / 0.95.

Companion to the verbatim-sentence-duplication number reported in
beyond_recall_v11_5_draft.md §4.5 / Appendix G (currently 25.4% on Babur, 0% on
Hamerton, 0% on Ebers). The verbatim figure may understate duplication by missing
near-paraphrases the self-editing agent produces when re-summarizing prior content.

Output: docs/research/letta_semantic_duplication_20260501.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

REPO = Path(__file__).resolve().parent.parent
BLOCK_DIR = REPO / "docs" / "research" / "_letta_blocks"
OUT_PATH = REPO / "docs" / "research" / "letta_semantic_duplication_20260501.json"

SUBJECTS = ["hamerton", "ebers", "babur"]
THRESHOLDS = [0.80, 0.85, 0.90, 0.95]
MIN_SENTENCE_CHARS = 20

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> list[str]:
    raw = SENT_SPLIT.split(text)
    out = []
    for s in raw:
        s = s.strip()
        s = re.sub(r"\s+", " ", s)
        if len(s) >= MIN_SENTENCE_CHARS:
            out.append(s)
    return out


def analyze_block(name: str, text: str, model: SentenceTransformer) -> dict:
    sentences = split_sentences(text)
    n = len(sentences)
    print(f"[{name}] {len(text):,} chars, {n:,} sentences (>= {MIN_SENTENCE_CHARS} chars)")
    if n == 0:
        return {"subject": name, "n_sentences": 0}

    print(f"[{name}] embedding...")
    emb = model.encode(sentences, batch_size=64, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)

    print(f"[{name}] computing pairwise cosine on {n}x{n} ...")
    sim = emb @ emb.T  # already L2-normalized
    np.fill_diagonal(sim, -1.0)  # exclude self

    max_sim_per_sent = sim.max(axis=1)

    by_threshold = {}
    for t in THRESHOLDS:
        flagged = (max_sim_per_sent >= t).sum()
        frac = float(flagged) / n
        by_threshold[f"{t:.2f}"] = {
            "fraction_with_near_duplicate": frac,
            "n_flagged": int(flagged),
        }

    examples = {}
    for t in [0.85, 0.90, 0.95]:
        idxs = np.where(max_sim_per_sent >= t)[0]
        sample = []
        for i in idxs[:5]:
            j = int(np.argmax(sim[i]))
            sample.append({
                "score": float(sim[i, j]),
                "sentence_a": sentences[int(i)][:300],
                "sentence_b": sentences[j][:300],
            })
        examples[f"{t:.2f}"] = sample

    return {
        "subject": name,
        "n_chars": len(text),
        "n_sentences": n,
        "min_sentence_chars": MIN_SENTENCE_CHARS,
        "by_threshold": by_threshold,
        "examples": examples,
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    }


def main():
    print(f"loading sentence-transformers model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    results = {"thresholds": THRESHOLDS, "subjects": {}}
    for name in SUBJECTS:
        path = BLOCK_DIR / f"{name}_human_block.txt"
        if not path.exists():
            print(f"[{name}] MISSING: {path}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8")
        results["subjects"][name] = analyze_block(name, text, model)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT_PATH}")

    print("\n===== headline =====")
    for name in SUBJECTS:
        r = results["subjects"].get(name)
        if not r or r.get("n_sentences", 0) == 0:
            continue
        line = f"[{name}] sentences={r['n_sentences']:,}"
        for t in ["0.80", "0.85", "0.90", "0.95"]:
            v = r["by_threshold"][t]
            line += f"  ≥{t}={v['fraction_with_near_duplicate']*100:.1f}%"
        print(line)


if __name__ == "__main__":
    main()
