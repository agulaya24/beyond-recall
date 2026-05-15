"""Numeric similarity threshold for the §6.3 pipeline-variance probe.

§6.3 currently states roughly 45% of rerun text is verbatim-identical and
the remaining 55% covers the same predicates with different surface phrasing
(assessed by side-by-side reading). C213 asks for a numeric similarity figure
on the non-verbatim 55%.

Approach: for each of the three probe subjects (Augustine, Sunity Devee,
Yung Wing), load the 3 reruns of the brief (`brief_v5_clean.md`), the most
holistic single-artifact representation of the spec. Compute:
  - Pairwise sentence-level alignment with verbatim-match flagging
  - On non-verbatim sentences, pairwise cosine similarity via sentence-transformers
  - Percentile distribution of non-verbatim similarity scores

Output: per-subject + pooled mean / median / IQR cosine on non-verbatim
sentence pairs, and verbatim-share recompute.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
SUBJECTS = ["augustine", "sunity_devee", "yung_wing"]
OUT_JSON = REPO / "docs" / "research" / "v11_9_6_pipeline_variance_similarity_20260510.json"
OUT_MD = REPO / "docs" / "research" / "v11_9_6_pipeline_variance_similarity_20260510.md"


def load_brief(subject: str, run: int) -> str:
    p = REPO / "data" / "global_subjects" / subject / "_variance_runs" / f"run_{run}" / "brief_v5_clean.md"
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def sentence_split(text: str) -> list[str]:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[\^[^\]]+\]:?", "", text)
    parts: list[str] = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("|"):
            continue
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(\[*])", line):
            s = s.strip()
            if len(s) > 25 and re.search(r"[A-Za-z]{4,}", s):
                parts.append(s)
    return parts


def normalize(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip().lower()
    s = re.sub(r"[‘’]", "'", s)
    s = re.sub(r"[“”]", '"', s)
    return s


def main() -> int:
    print("Loading sentence-transformers...")
    from sentence_transformers import SentenceTransformer
    import numpy as np

    model = SentenceTransformer("all-MiniLM-L6-v2")

    per_subject = {}
    pool_nonverbatim_cosines: list[float] = []
    pool_verbatim_count = 0
    pool_total_count = 0

    for subj in SUBJECTS:
        briefs = [load_brief(subj, r) for r in (1, 2, 3)]
        if not all(briefs):
            print(f"  WARN: {subj} missing one or more reruns")
            continue

        sentence_lists = [sentence_split(b) for b in briefs]
        print(f"\n{subj}: run sentence counts = {[len(s) for s in sentence_lists]}")

        # Pairwise (run_i, run_j) on the alignable portion: encode all unique sentences
        all_sents = list({normalize(s): s for sl in sentence_lists for s in sl}.values())
        embeds = model.encode(all_sents, show_progress_bar=False, normalize_embeddings=True)
        norm_to_idx = {normalize(s): i for i, s in enumerate(all_sents)}

        pair_results = []
        for i in range(len(sentence_lists)):
            for j in range(i + 1, len(sentence_lists)):
                sl_i = sentence_lists[i]
                sl_j = sentence_lists[j]
                norm_set_i = {normalize(s) for s in sl_i}
                norm_set_j = {normalize(s) for s in sl_j}
                verbatim = norm_set_i & norm_set_j
                # For each sentence in run_i that is NOT verbatim in run_j, find its best cosine match in run_j
                nonverbatim_cosines = []
                i_only = [s for s in sl_i if normalize(s) not in verbatim]
                j_emb_idxs = [norm_to_idx[normalize(s)] for s in sl_j]
                j_embeds = embeds[j_emb_idxs]
                for s in i_only:
                    s_emb = embeds[norm_to_idx[normalize(s)]]
                    sims = j_embeds @ s_emb
                    nonverbatim_cosines.append(float(sims.max()))
                # Also symmetric direction (j_only -> best in i)
                j_only = [s for s in sl_j if normalize(s) not in verbatim]
                i_emb_idxs = [norm_to_idx[normalize(s)] for s in sl_i]
                i_embeds = embeds[i_emb_idxs]
                for s in j_only:
                    s_emb = embeds[norm_to_idx[normalize(s)]]
                    sims = i_embeds @ s_emb
                    nonverbatim_cosines.append(float(sims.max()))

                total_pairs = len(sl_i) + len(sl_j)
                verbatim_pairs = 2 * len(verbatim)  # counted from both directions
                pool_verbatim_count += verbatim_pairs
                pool_total_count += total_pairs
                pool_nonverbatim_cosines.extend(nonverbatim_cosines)

                pair_results.append({
                    "pair": (i + 1, j + 1),
                    "verbatim_count": len(verbatim),
                    "verbatim_share_run_i": len(verbatim) / max(len(sl_i), 1),
                    "verbatim_share_run_j": len(verbatim) / max(len(sl_j), 1),
                    "nonverbatim_cosines_n": len(nonverbatim_cosines),
                    "nonverbatim_cosine_mean": float(np.mean(nonverbatim_cosines)) if nonverbatim_cosines else None,
                    "nonverbatim_cosine_median": float(np.median(nonverbatim_cosines)) if nonverbatim_cosines else None,
                    "nonverbatim_cosine_iqr": [
                        float(np.percentile(nonverbatim_cosines, 25)) if nonverbatim_cosines else None,
                        float(np.percentile(nonverbatim_cosines, 75)) if nonverbatim_cosines else None,
                    ],
                    "share_cosine_ge_080": float(np.mean(np.array(nonverbatim_cosines) >= 0.80)) if nonverbatim_cosines else None,
                    "share_cosine_ge_085": float(np.mean(np.array(nonverbatim_cosines) >= 0.85)) if nonverbatim_cosines else None,
                    "share_cosine_ge_090": float(np.mean(np.array(nonverbatim_cosines) >= 0.90)) if nonverbatim_cosines else None,
                })

        per_subject[subj] = {
            "run_sentence_counts": [len(s) for s in sentence_lists],
            "pair_results": pair_results,
        }

    import numpy as np
    pool_summary = {
        "pool_nonverbatim_n": len(pool_nonverbatim_cosines),
        "pool_verbatim_share": pool_verbatim_count / pool_total_count if pool_total_count else None,
        "pool_nonverbatim_cosine_mean": float(np.mean(pool_nonverbatim_cosines)) if pool_nonverbatim_cosines else None,
        "pool_nonverbatim_cosine_median": float(np.median(pool_nonverbatim_cosines)) if pool_nonverbatim_cosines else None,
        "pool_nonverbatim_cosine_iqr": [
            float(np.percentile(pool_nonverbatim_cosines, 25)) if pool_nonverbatim_cosines else None,
            float(np.percentile(pool_nonverbatim_cosines, 75)) if pool_nonverbatim_cosines else None,
        ],
        "pool_share_cosine_ge_080": float(np.mean(np.array(pool_nonverbatim_cosines) >= 0.80)) if pool_nonverbatim_cosines else None,
        "pool_share_cosine_ge_085": float(np.mean(np.array(pool_nonverbatim_cosines) >= 0.85)) if pool_nonverbatim_cosines else None,
        "pool_share_cosine_ge_090": float(np.mean(np.array(pool_nonverbatim_cosines) >= 0.90)) if pool_nonverbatim_cosines else None,
    }

    output = {"per_subject": per_subject, "pool_summary": pool_summary}
    OUT_JSON.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    print()
    print("=== Pool summary ===")
    for k, v in pool_summary.items():
        print(f"  {k}: {v}")

    # Markdown report
    md = [
        "# v11.9.6 — pipeline-variance numeric similarity probe\n",
        "Per-rerun brief comparison across three probe subjects (Augustine, Sunity Devee, Yung Wing).",
        "For each pair of reruns within a subject, sentences are classified as verbatim-identical or non-verbatim.",
        "On non-verbatim sentences, best-match cosine similarity (MiniLM-L6-v2 sentence embeddings, normalized) is",
        "reported against the other run's sentence pool. This puts a numeric figure on the §6.3 claim that the",
        "non-verbatim share covers the same predicates and behavioral patterns with different surface phrasing.\n",
        "## Pool summary (Augustine + Sunity Devee + Yung Wing combined)\n",
        f"- Non-verbatim sentence pairs evaluated: **{pool_summary['pool_nonverbatim_n']:,}**",
        f"- Verbatim share across the three subjects (pairwise): **{pool_summary['pool_verbatim_share']:.1%}**",
        f"- Non-verbatim best-match cosine, mean: **{pool_summary['pool_nonverbatim_cosine_mean']:.3f}**",
        f"- Non-verbatim best-match cosine, median: **{pool_summary['pool_nonverbatim_cosine_median']:.3f}**",
        f"- Non-verbatim best-match cosine, IQR: **[{pool_summary['pool_nonverbatim_cosine_iqr'][0]:.3f}, {pool_summary['pool_nonverbatim_cosine_iqr'][1]:.3f}]**",
        f"- Share of non-verbatim sentences with best-match cosine ≥ 0.80: **{pool_summary['pool_share_cosine_ge_080']:.1%}**",
        f"- Share of non-verbatim sentences with best-match cosine ≥ 0.85: **{pool_summary['pool_share_cosine_ge_085']:.1%}**",
        f"- Share of non-verbatim sentences with best-match cosine ≥ 0.90: **{pool_summary['pool_share_cosine_ge_090']:.1%}**",
        "",
        "## Per-subject pairwise detail\n",
    ]
    for subj, data in per_subject.items():
        md.append(f"### {subj}\n")
        md.append(f"Run sentence counts: {data['run_sentence_counts']}")
        md.append("")
        for pr in data["pair_results"]:
            md.append(f"- **Run {pr['pair'][0]} vs Run {pr['pair'][1]}**: verbatim={pr['verbatim_count']} sentences (share_i={pr['verbatim_share_run_i']:.1%}, share_j={pr['verbatim_share_run_j']:.1%}). Non-verbatim best-match cosine: mean={pr['nonverbatim_cosine_mean']:.3f}, median={pr['nonverbatim_cosine_median']:.3f}, IQR=[{pr['nonverbatim_cosine_iqr'][0]:.3f}, {pr['nonverbatim_cosine_iqr'][1]:.3f}]; ≥0.80={pr['share_cosine_ge_080']:.1%}, ≥0.85={pr['share_cosine_ge_085']:.1%}, ≥0.90={pr['share_cosine_ge_090']:.1%}.")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
