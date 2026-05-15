"""
Figure 4.2 v3: Hamerton compression — publication polish.

Changes from v2:
1. Shared typography (14/12/10 via _figure_style.py).
2. Shared palette (baseline gray, spec blue, facts orange, facts+spec green, corpus red,
   corpus+spec purple). No color-concept collisions with other figures.
3. Guide callout "spec alone (7K tok) outscores raw corpus (34K tok)" now rides the
   arc arrow between the two points it references, not floating far to the left.
4. Leader-line offsets tuned so callouts no longer cross.
5. Wider figsize (10.5 x 5.8) to accommodate 14pt fonts without crowding.
6. dpi=300.

Mechanical link (2026-05-13): the Hamerton condition scores and the spec / corpus
token counts are now loaded from docs/research/v11_emit/4_2_compression.json
(produced by scripts/_v11_emit_4_2_compression.py from primary results/ judgment
data) instead of hardcoded Python literals. The previously-hardcoded scores were
stale: they predated the 5-judge primary aggregation and disagreed with the §4.2
Table 4.2 in the paper by up to 0.45 points. The corrected scores now match that
table. C4 (facts only) and C4a (facts + spec) token counts are not yet emitted by
the emit scaffold and remain as a small local manifest below, clearly flagged;
adding them to the emit output is the follow-up that fully closes the link.
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _figure_style import (
    apply_style,
    COLOR_BASELINE, COLOR_MEAN_DELTA,
    SIZE_ANNOTATION_SMALL, SIZE_LEGEND,
)

REPO = Path(__file__).resolve().parent.parent
FIG_DIR = REPO / 'figures'
DATA_PATH = REPO / 'docs' / 'research' / 'v11_emit' / '4_2_compression.json'

apply_style()

# Per-condition plot encoding (marker + color). The paper uses a distinct
# marker/color per condition; this is presentation, not data.
CONDITION_STYLE = {
    'C5':  ('C5 (baseline)',    'X', COLOR_BASELINE, 'No context'),
    'C2a': ('C2a (spec alone)', 'o', '#2E86AB',      'Spec alone'),
    'C4':  ('C4 (facts alone)', 'D', '#F18F01',      'Facts alone'),
    'C4a': ('C4a (facts+spec)', '^', '#2F9E44',      'Facts + spec'),
    'C8':  ('C8 (raw corpus)',  's', '#C44E52',      'Raw corpus'),
    'C9':  ('C9 (corpus+spec)', 'P', '#6A4C93',      'Corpus + spec'),
}

# C5 is a nominal no-context anchor (no real context served); C4 facts-only and
# C4a facts+spec token counts are not yet emitted by
# scripts/_v11_emit_4_2_compression.py. They are kept here as a small local
# manifest pending a follow-up that adds them to the emit output. The
# load-bearing token counts (C2a spec, C8 corpus, and C9 = corpus + spec) are
# loaded from the emit JSON below.
LOCAL_TOKEN_MANIFEST = {
    'C5':  40,
    'C4':  7723,
    'C4a': 16874,
}


def load_points():
    """Build the 6 (label, tokens, score, marker, color, family) plot points.

    Scores and the spec / corpus token counts come from the v11 emit JSON;
    C5/C4/C4a token positions come from LOCAL_TOKEN_MANIFEST (see note above).
    """
    data = json.load(open(DATA_PATH, encoding='utf-8'))
    claims = data['claims']

    def score(cond):
        return claims[f'4_2_hamerton_{cond}']['value']

    spec_tokens = claims['4_2_hamerton_spec_tokens']['value']
    corpus_tokens = claims['4_2_hamerton_corpus_tokens']['value']
    tokens = {
        'C5':  LOCAL_TOKEN_MANIFEST['C5'],
        'C2a': spec_tokens,
        'C4':  LOCAL_TOKEN_MANIFEST['C4'],
        'C4a': LOCAL_TOKEN_MANIFEST['C4a'],
        'C8':  corpus_tokens,
        'C9':  corpus_tokens + spec_tokens,
    }

    points = []
    for cond in ('C5', 'C2a', 'C4', 'C4a', 'C8', 'C9'):
        label, marker, color, family = CONDITION_STYLE[cond]
        points.append((label, tokens[cond], round(score(cond), 2),
                        marker, color, family))
    return points


POINTS = load_points()
C5_SCORE = POINTS[0][2]


def main():
    fig, ax = plt.subplots(figsize=(10.5, 6.4))

    ax.axhline(C5_SCORE, color='#BBBBBB', linestyle=':', linewidth=1.1, zorder=1,
               label=f'C5 baseline ({C5_SCORE:.2f}, no context)')

    for label, toks, score, marker, color, family in POINTS:
        ax.scatter(toks, score, marker=marker, s=230, color=color,
                   edgecolors='black', linewidths=0.9, zorder=5,
                   label=f'{label} = {score:.2f}')

    # Leader-line offsets. Arrow-less labels placed closer to points; arrowed ones
    # pulled further to avoid overlap in the dense 7-17K token band.
    offset_map = {
        # (dx, dy, arrow)
        'C5 (baseline)':    (  60,  16, True),
        'C2a (spec alone)': ( -95,  48, True),
        'C4 (facts alone)': ( -90, -46, True),
        'C4a (facts+spec)': (   0,  42, False),
        'C8 (raw corpus)':  (   0, -38, False),
        'C9 (corpus+spec)': (  50,  30, True),
    }
    for label, toks, score, marker, color, family in POINTS:
        dx, dy, arrow = offset_map[label]
        tok_str = f'~{toks/1000:.1f}K tok' if toks >= 1000 else f'~{toks} tok'
        ann = f'{label}\n{tok_str}, score {score:.2f}'
        ax.annotate(
            ann, (toks, score), xytext=(dx, dy), textcoords='offset points',
            ha='center', fontsize=SIZE_ANNOTATION_SMALL, color='#222',
            bbox=dict(boxstyle='round,pad=0.32', facecolor='white',
                      edgecolor='#BBBBBB', linewidth=0.7, alpha=0.97),
            arrowprops=dict(arrowstyle='-', color='#999', linewidth=0.8) if arrow else None,
        )

    # Guide arrow + callout: spec alone outscores raw corpus despite less context.
    # Arc arrow above points (rad positive) from C8 point to C2a point.
    pt = {label.split()[0]: (toks, score) for label, toks, score, *_ in POINTS}
    c2a_tok, c2a_score = pt['C2a']
    c8_tok, c8_score = pt['C8']
    ax.annotate('',
                xy=(c2a_tok, c2a_score), xycoords='data',
                xytext=(c8_tok, c8_score), textcoords='data',
                arrowprops=dict(arrowstyle='->', color='#777777', linewidth=1.2,
                                linestyle='--', connectionstyle='arc3,rad=0.45'),
                zorder=2)
    # Callout text placed above the arc, between C2a and C8 horizontally.
    callout_x = (c2a_tok * c8_tok) ** 0.5  # geometric mean (log x-axis)
    callout_y = max(c2a_score, c8_score) + 0.85
    ax.text(callout_x, callout_y,
            f'spec alone (~{c2a_tok/1000:.0f}K tok) outscores raw corpus (~{c8_tok/1000:.0f}K tok)',
            fontsize=SIZE_ANNOTATION_SMALL, color='#444', fontstyle='italic', ha='center',
            bbox=dict(boxstyle='round,pad=0.28', facecolor='#FFFEF5',
                      edgecolor='#D8C88A', linewidth=0.7, alpha=0.96))

    ax.set_xscale('log')
    ax.set_xlabel('Context size served to the response model (tokens, log scale)')
    ax.set_ylabel('5-judge primary score (1-5 rubric)')
    ax.set_title('Figure 4.2: Hamerton score vs. context size across 5 context strategies + baseline')
    ax.grid(True, alpha=0.3, linewidth=0.5, which='both')
    ax.set_ylim(0.5, 4.3)
    ax.set_xlim(20, 200000)

    ax.legend(loc='lower right', fontsize=SIZE_LEGEND - 1, framealpha=0.96,
              edgecolor='#CCCCCC', ncol=1, title='Condition (score)')

    plt.tight_layout()
    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig_4_2_compression_v3.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
