"""
Shared typography + palette for Beyond Recall main-body v3 figures.

Documented in docs/research/_figure_palette.md.
"""

import matplotlib
import matplotlib.pyplot as plt


FONT_FAMILY = 'DejaVu Sans'

# --- Type sizes ---
SIZE_TITLE = 14
SIZE_AXIS_LABEL = 12
SIZE_TICK = 10
SIZE_ANNOTATION = 10
SIZE_ANNOTATION_SMALL = 9
SIZE_LEGEND = 10
SIZE_FOOTER = 9

# --- Semantic colors (identical meaning across figures) ---
COLOR_IMPROVED = '#2F9E44'   # Delta > 0 (green)
COLOR_WORSENED = '#C44E52'   # Delta < 0 (red)
COLOR_TIE      = '#8A8A8A'   # Delta = 0 (gray)
COLOR_ZERO_LINE = '#C44E52'  # Delta = 0 reference line (matches WORSENED)
COLOR_MEAN_DELTA = '#2E86AB' # Mean Delta trend (blue — distinct from green/red)
COLOR_BASELINE = '#7A7A7A'   # C5 baseline markers / reference
COLOR_NEUTRAL_BAND = '#FAFAFA'

# --- Baseline bands (Fig 4.1) ---
BAND_LOW      = '#2E86AB'
BAND_MID      = '#F18F01'
BAND_FRANKLIN = '#A23B72'

# --- Memory-system colors (Fig 7) ---
SYSTEM_COLOR = {
    'Mem0':             '#2E86AB',
    'Letta (archival)': '#2F9E44',
    'Supermemory':      '#6A4C93',
    'Zep':              '#F18F01',
}


def apply_style():
    """Set rcParams to the shared Beyond Recall typography."""
    plt.rcParams.update({
        'font.family': FONT_FAMILY,
        'font.size': SIZE_ANNOTATION,
        'axes.titlesize': SIZE_TITLE,
        'axes.titleweight': 'bold',
        'axes.labelsize': SIZE_AXIS_LABEL,
        'axes.labelweight': 'regular',
        'legend.fontsize': SIZE_LEGEND,
        'xtick.labelsize': SIZE_TICK,
        'ytick.labelsize': SIZE_TICK,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linestyle': '--',
        'grid.linewidth': 0.5,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.edgecolor': '#666666',
        'figure.dpi': 100,
        'savefig.dpi': 300,
    })


def darker(hex_color, amount=0.22):
    """Return a darker variant of a hex color, for mean / aggregate bars."""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = max(0, int(r * (1 - amount)))
    g = max(0, int(g * (1 - amount)))
    b = max(0, int(b * (1 - amount)))
    return f'#{r:02X}{g:02X}{b:02X}'
