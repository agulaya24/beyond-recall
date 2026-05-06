"""
Vision-based figure review for the 'Beyond Recall' paper.

Sends each figure (PNG) to Claude Opus, GPT-5.4, and Groq Llama 4 Scout (vision)
and collects structured publication-readiness reviews.

Usage: python scripts/review_figures.py
Output: docs/reviews/figure_review_<timestamp>.md
"""
import base64
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIG_DIR = REPO / 'figures'
OUT_DIR = REPO / 'docs' / 'reviews'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Figure catalog: filename -> (caption, section, status)
FIGURE_CATALOG = {
    # V8-active figures (publication critical)
    'fig_4_1_gradient_scatter.png': {
        'caption': 'Figure 4.1: Cross-Subject Gradient. Delta_C4a (facts+spec vs C5 baseline) on y-axis vs C5 baseline on x-axis. Points colored by band (low-baseline green, mid-baseline orange, Franklin red as high-baseline reference). Regression line with 95% CI band. N=14 main subjects + Franklin control. Slope -0.96, R^2 0.82.',
        'section': 'Section 4.1 Cross-Subject Gradient (PUBLICATION-CRITICAL)',
        'status': 'v8-active',
    },
    'fig_4_2_compression.png': {
        'caption': 'Figure 4.2: Compression curve. Score (5-judge primary, 1-5 rubric) vs context size in tokens (log scale). Per-subject lines for all low-baseline subjects. Highlights that the spec+facts region (1-7.10K tokens) produces steep initial slope followed by a long plateau. Shows ~5K-token spec beats 34K-token raw corpus.',
        'section': 'Section 4.2 Compression: Structure vs Raw Text (PUBLICATION-CRITICAL)',
        'status': 'v8-active',
    },
    'fig_4_2_1_question_improvement_rates.png': {
        'caption': 'Figure 4.2.1: Per-question outcome distribution by condition. Stacked bars for C2a (spec only), C4 (facts only), C8 (raw corpus), C4a (facts+spec) showing share improved/tied/worsened vs C5 baseline across 351 questions (9 low-baseline subjects x 39 questions). Median delta when improved = +1.00 points; median delta when worsened = -0.40 points.',
        'section': 'Section 4.2.1 Question-Improvement Rate (PUBLICATION-CRITICAL)',
        'status': 'v8-active',
    },
    # V6 legacy figures (may be cut or regenerated)
    'fig1_global_gradient.png': {
        'caption': 'Figure 1 (v6): Per-subject baseline (C5) vs spec+facts score across all 14 subjects. Visualizes the gradient result: spec helps most where baseline is low. Labeled: Hamerton, Sunity Devee, Ebers, Equiano, Zitkala-Sa.',
        'section': 'V6-legacy - possibly orphaned in v8',
        'status': 'v6-legacy',
    },
    'fig2_compression_curve.png': {
        'caption': 'Figure 2 (v6): Log-tokens vs judge score. Labeled conditions: C5 Baseline, Memory alone, C2a Spec, Memory+Spec, C3 Letta+Spec, C4 All Facts, C9 Raw. Shows ~5K-token spec beats raw corpus.',
        'section': 'V6-legacy - superseded by fig_4_2_compression',
        'status': 'v6-legacy',
    },
    'fig3_retrieval_disagreement.png': {
        'caption': 'Figure 3 (v6): Top-k retrieval disagreement rate across Mem0/Letta/Supermemory at k=1,3,5,10. Bars showing 68%/39%/22%/11%. NOTE: paper prose states 93% at top-1 and 53% at top-10 - possible data mismatch.',
        'section': 'V6-legacy - possible data mismatch with v8 prose',
        'status': 'v6-legacy',
    },
    'fig4_hedging_reduction.png': {
        'caption': 'Figure 4 (v6): Two-bar chart showing hedging language 51% (without spec) vs 31% (with spec), labeled "39% reduction". NOTE: paper describes 3 conditions (C5/C2a/C4a) with two classifier rules, but the figure shows only 2 bars - possible data/structure mismatch.',
        'section': 'V6-legacy - structural mismatch',
        'status': 'v6-legacy',
    },
    'fig5_condition_effects.png': {
        'caption': 'Figure 5 (v6): Two-panel figure. Panel A: per-subject trajectories across Baseline/Spec/Wrong Spec/Facts/Facts+Spec. Panel B: box plots of score distributions by condition.',
        'section': 'V6-legacy',
        'status': 'v6-legacy',
    },
    'fig6_wrong_spec_control.png': {
        'caption': 'Figure 6 (v6): Per-subject dot plot showing Baseline (gray), Wrong spec (orange), Correct spec (blue) for 14 subjects. Shows wrong-spec lands near or below baseline.',
        'section': 'V6-legacy',
        'status': 'v6-legacy',
    },
    'fig7_memory_systems.png': {
        'caption': 'Figure 7 (v6): Grouped bar chart showing memory systems (Letta, Mem0, Supermemory, Zep) with spec vs without spec. Delta percentages: Letta +45%, Mem0 +22%, Supermemory +12%, Zep +66%.',
        'section': 'V6-legacy',
        'status': 'v6-legacy',
    },
    'fig8_judge_agreement.png': {
        'caption': 'Figure 8 (v6): 7x7 heatmap of Spearman rho inter-judge agreement between Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gem Flash, Gem Pro. NOTE: v8 uses 5-judge primary panel, this figure is 7-judge.',
        'section': 'V6-legacy - 7-judge, v8 uses 5-judge',
        'status': 'v6-legacy',
    },
    'fig9_cultural_baseline.png': {
        'caption': 'Figure 9 (v6): Horizontal bar chart of baseline recognizability by cultural region (West African, North African, Italian, French, Native American, ..., Indian). Orange bars = spec did not improve; blue bars = spec improved. Threshold line at ~2.4.',
        'section': 'V6-legacy',
        'status': 'v6-legacy',
    },
    'fig10_letta_scaling.png': {
        'caption': 'Figure 10 (v6): Two-panel. Left: Letta block size vs Base Layer spec size as source corpus grows (Hamerton, Ebers, Babur); Letta API ceiling 333,000 chars. Right: Verbatim sentence duplication (0%, 0%, 25.4% for Babur).',
        'section': 'V6-legacy - supports Letta scaling ceiling narrative',
        'status': 'v6-legacy',
    },
    'fig11_tier2_replication.png': {
        'caption': 'Figure 11 (v6): Tier-2 cross-provider replication. Grouped bars showing spec effect delta for Sonnet (blue) and Gemini Pro (green) response models on Ebers, Yung Wing, Zitkala-Sa. 5 of 6 cells positive (+1.48, +1.07, +1.91, +1.27, +1.40, -0.55).',
        'section': 'V6-legacy - cross-provider robustness',
        'status': 'v6-legacy',
    },
}

REVIEW_PROMPT_TEMPLATE = """You are reviewing a figure from a research paper on behavioral specifications for AI personalization. The figure is being evaluated for publication readiness.

Paper context: the paper measures whether a compact behavioral specification can improve AI prediction of how a specific person would respond in novel situations. The target venue is machine-learning / AI / personalization research (arXiv / NeurIPS / ICML / ICLR-adjacent).

Figure caption and claim it supports:
{caption}

Paper section: {section}

Please review for:
1. Clarity: can a reader understand what is being shown without reading the caption at length?
2. Style: does it match academic publication conventions (clean axes, minimal chart junk, readable labels, legible at print size)?
3. Color use: is the palette professional, colorblind-safe, print-friendly? Any confusing color choices?
4. Labels / legend / annotations: are there enough? too many? typography consistent?
5. Data-ink ratio (Tufte): is there chart junk that could be removed? information that could be added?
6. Axis scales: appropriate? any misleading truncations or non-zero baselines?
7. Comparability to the genre: how does this figure compare to conventions in ML/AI papers for similar data (gradient plots, per-condition comparisons, per-subject tables, etc.)?

Respond with:
(a) Overall grade A/B/C/D/F for publication readiness (be direct; no hedging).
(b) Specific issues in priority order with suggested fixes.
(c) Any strengths worth preserving.
(d) If you recommend regeneration, one-sentence description of what the ideal version looks like.

Keep your response concise: aim for 250-450 words total."""


def encode_image(path: Path) -> str:
    with open(path, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('ascii')


def review_claude(image_path: Path, caption: str, section: str) -> dict:
    import anthropic
    client = anthropic.Anthropic()
    b64 = encode_image(image_path)
    prompt = REVIEW_PROMPT_TEMPLATE.format(caption=caption, section=section)
    t0 = time.time()
    try:
        resp = client.messages.create(
            model='claude-opus-4-5',
            max_tokens=1500,
            temperature=0.2,
            messages=[{
                'role': 'user',
                'content': [
                    {'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/png', 'data': b64}},
                    {'type': 'text', 'text': prompt},
                ],
            }],
        )
        text = resp.content[0].text
        return {'provider': 'claude-opus-4-5', 'text': text, 'elapsed': time.time() - t0, 'error': None}
    except Exception as e:
        return {'provider': 'claude-opus-4-5', 'text': None, 'elapsed': time.time() - t0, 'error': str(e)}


def review_openai(image_path: Path, caption: str, section: str) -> dict:
    import openai
    client = openai.OpenAI()
    b64 = encode_image(image_path)
    prompt = REVIEW_PROMPT_TEMPLATE.format(caption=caption, section=section)
    t0 = time.time()
    # Try GPT-5.4 first, fall back to gpt-4o
    for model_id in ['gpt-5.4', 'gpt-4o']:
        try:
            resp = client.chat.completions.create(
                model=model_id,
                temperature=0.2,
                max_tokens=1500,
                messages=[{
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': prompt},
                        {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{b64}'}},
                    ],
                }],
            )
            return {'provider': model_id, 'text': resp.choices[0].message.content, 'elapsed': time.time() - t0, 'error': None}
        except Exception as e:
            last_err = str(e)
            continue
    return {'provider': 'openai', 'text': None, 'elapsed': time.time() - t0, 'error': last_err}


def review_groq(image_path: Path, caption: str, section: str) -> dict:
    import groq
    client = groq.Groq()
    b64 = encode_image(image_path)
    prompt = REVIEW_PROMPT_TEMPLATE.format(caption=caption, section=section)
    t0 = time.time()
    try:
        resp = client.chat.completions.create(
            model='meta-llama/llama-4-scout-17b-16e-instruct',
            temperature=0.2,
            max_tokens=1500,
            messages=[{
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt},
                    {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{b64}'}},
                ],
            }],
        )
        return {'provider': 'llama-4-scout-vision', 'text': resp.choices[0].message.content, 'elapsed': time.time() - t0, 'error': None}
    except Exception as e:
        return {'provider': 'llama-4-scout-vision', 'text': None, 'elapsed': time.time() - t0, 'error': str(e)}


def review_one(fig_name: str, meta: dict, providers: list) -> dict:
    path = FIG_DIR / fig_name
    result = {'figure': fig_name, 'caption': meta['caption'], 'section': meta['section'],
              'status': meta['status'], 'reviews': {}}
    for provider_fn in providers:
        r = provider_fn(path, meta['caption'], meta['section'])
        result['reviews'][r['provider']] = r
    return result


def main():
    # V8-active figures get all 3 providers; v6-legacy figures get just Claude (cheaper)
    v8_active = {k: v for k, v in FIGURE_CATALOG.items() if v['status'] == 'v8-active'}
    v6_legacy = {k: v for k, v in FIGURE_CATALOG.items() if v['status'] == 'v6-legacy'}

    all_results = []

    # V8-active: full panel (Claude + OpenAI + Groq)
    print(f'Reviewing {len(v8_active)} v8-active figures with Claude + OpenAI + Groq...', flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(review_one, name, meta, [review_claude, review_openai, review_groq]): name
                   for name, meta in v8_active.items()}
        for fut in as_completed(futures):
            r = fut.result()
            all_results.append(r)
            print(f'  done: {r["figure"]}', flush=True)

    # V6-legacy: Claude + Groq (skip OpenAI to save budget)
    print(f'Reviewing {len(v6_legacy)} v6-legacy figures with Claude + Groq...', flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(review_one, name, meta, [review_claude, review_groq]): name
                   for name, meta in v6_legacy.items()}
        for fut in as_completed(futures):
            r = fut.result()
            all_results.append(r)
            print(f'  done: {r["figure"]}', flush=True)

    # Save raw JSON
    ts = time.strftime('%Y%m%d_%H%M%S')
    json_path = OUT_DIR / f'figure_review_raw_{ts}.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    print(f'Raw results: {json_path}', flush=True)

    # Write markdown report
    md_path = OUT_DIR / f'figure_review_{ts}.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f'# Figure Review - Beyond Recall v8\n\nGenerated: {ts}\n\n')
        f.write('Providers: Claude Opus 4.5, GPT-5.4 (with gpt-4o fallback), Groq Llama 4 Scout Vision.\n\n')
        f.write('V8-active figures received all three reviewers; v6-legacy figures received Claude + Groq.\n\n')

        # Sort: v8-active first, then v6-legacy
        order = {'v8-active': 0, 'v6-legacy': 1}
        all_results.sort(key=lambda r: (order.get(r['status'], 9), r['figure']))

        for r in all_results:
            f.write(f'---\n\n## {r["figure"]}\n\n')
            f.write(f'**Status:** {r["status"]}\n\n')
            f.write(f'**Section:** {r["section"]}\n\n')
            f.write(f'**Caption:** {r["caption"]}\n\n')
            for prov, rev in r['reviews'].items():
                f.write(f'### {prov}\n\n')
                if rev['error']:
                    f.write(f'ERROR: `{rev["error"]}`\n\n')
                else:
                    f.write(f'{rev["text"]}\n\n')
                    f.write(f'*({rev["elapsed"]:.1f}s)*\n\n')

    print(f'Report: {md_path}', flush=True)
    return md_path


if __name__ == '__main__':
    main()
