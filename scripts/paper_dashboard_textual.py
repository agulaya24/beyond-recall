"""Textual TUI dashboard for Beyond Recall paper launch.

Run: python paper_dashboard_textual.py

Shows: paper status, experiments, judging coverage, analyses, outreach.
Auto-refreshes every 30 seconds from disk state.
"""
import json, os, sys
from datetime import datetime
from pathlib import Path

try:
    from textual.app import App, ComposeResult
    from textual.containers import Horizontal, Vertical, ScrollableContainer
    from textual.widgets import Header, Footer, Static, DataTable, TabbedContent, TabPane
    from textual.reactive import reactive
except ImportError:
    print('Installing textual...'); os.system(f'"{sys.executable}" -m pip install textual')
    from textual.app import App, ComposeResult
    from textual.containers import Horizontal, Vertical, ScrollableContainer
    from textual.widgets import Header, Footer, Static, DataTable, TabbedContent, TabPane
    from textual.reactive import reactive

REPO = Path(__file__).parent.parent
# NOTE: depends on the separate (private) memory_system repo. Set MEMORY_SYSTEM_ROOT
# to its path; defaults to empty so the missing-path failure is obvious.
MS = Path(os.environ.get("MEMORY_SYSTEM_ROOT", "")) / 'data' / 'experiments' / 'memory_systems'

SUBJECTS = ['zitkala_sa','hamerton','keckley','yung_wing','seacole','sunity_devee',
            'equiano','augustine','ebers','fukuzawa','cellini','bernal_diaz','rousseau','babur']
JUDGES = ['haiku','sonnet','opus','gpt4o','gpt54','gemini_flash','gemini_pro']


def _subject_dir(s):
    if s == 'hamerton':
        return MS / 'results' / 'run_fullstack_hamerton_20260411_231237'
    return MS / 'results' / f'global_{s}'


def _valid_count(jpath):
    try:
        d = json.loads(jpath.read_text(encoding='utf-8'))
        return sum(1 for e in d if e.get('score',0)>0 and not e.get('parse_failure'))
    except: return 0


def collect_paper_state():
    """Read paper checklist + dashboard status."""
    draft = REPO / 'docs' / 'beyond_recall_v6_draft.md'
    dash = REPO / 'docs' / 'PAPER_DASHBOARD.md'
    out = {'draft_exists': draft.exists(),
           'draft_size': draft.stat().st_size if draft.exists() else 0,
           'draft_modified': datetime.fromtimestamp(draft.stat().st_mtime).strftime('%H:%M:%S') if draft.exists() else '—',
           'dashboard_exists': dash.exists(),
           'results_s113': (MS/'results'/'RESULTS_S113.json').exists(),
           'analysis_plan_locked': (REPO/'docs'/'ANALYSIS_PLAN_LOCK.md').exists()}
    if draft.exists():
        text = draft.read_text(encoding='utf-8')
        out['placeholders'] = text.count('PLACEHOLDER')
        out['word_count'] = len(text.split())
    return out


def collect_judging_coverage():
    """Matrix of judge coverage across experiments."""
    rows = []
    # Main study per-subject
    main_total = 14
    main_done = 0
    for s in SUBJECTS:
        p = _subject_dir(s) / ('judgments_v2.json' if s!='hamerton' else 'analysis/judgments.json')
        if p.exists() and p.stat().st_size > 1000:
            main_done += 1
    rows.append(('Main study (14 subjects)', f'{main_done}/{main_total}', '5 cond × 6-7 judges'))

    # Base Layer
    bl_done = 0
    for s in SUBJECTS:
        p = _subject_dir(s) / 'baselayer_judgments_merged.json'
        if p.exists(): bl_done += 1
    rows.append(('Base Layer (5th system)', f'{bl_done}/14', '3-6 judges/subject'))

    # Tier 2
    t2_cells = 0
    t2_valid = 0
    for s in ['ebers','yung_wing','zitkala_sa']:
        for m in ['sonnet','gemini_pro']:
            for j in JUDGES:
                p = _subject_dir(s) / f'tier2_{m}_judgments_{j}.json'
                if p.exists():
                    t2_cells += 1
                    if _valid_count(p) > 100: t2_valid += 1
    rows.append(('Tier 2 circularity', f'{t2_valid}/{t2_cells}', '3 subj × 2 resp × 7 judges'))

    # Wrong-spec v2
    ws2_cells = 0; ws2_valid = 0
    for s in SUBJECTS:
        for j in JUDGES:
            p = _subject_dir(s) / f'wrong_spec_v2_judgments_{j}.json'
            if p.exists():
                ws2_cells += 1
                if _valid_count(p) > 30: ws2_valid += 1
    rows.append(('Wrong-spec v2', f'{ws2_valid}/{ws2_cells}', '14 subj × 7 judges'))
    return rows


def collect_backfill_progress():
    """Background backfill job progress."""
    logs = [
        ('OpenAI backfill v2', MS / 'backfill_openai_v2.log'),
        ('Gemini Flash (key 1)', MS / 'backfill_gemini.log'),
        ('Semantic overlap', MS / 'results' / 'semantic_overlap_analysis.json'),
        ('Letta agent-loop (hamerton)', MS / 'letta_loop_hamerton_v2.log'),
    ]
    rows = []
    for label, p in logs:
        if p.exists():
            if p.suffix == '.json':
                rows.append((label, '✅ done', datetime.fromtimestamp(p.stat().st_mtime).strftime('%H:%M:%S')))
            else:
                try:
                    tail = p.read_text(encoding='utf-8', errors='replace').splitlines()[-3:]
                    last = tail[-1][:60] if tail else '—'
                    rows.append((label, last, datetime.fromtimestamp(p.stat().st_mtime).strftime('%H:%M:%S')))
                except: rows.append((label, 'read error', '—'))
        else:
            rows.append((label, '— not started —', '—'))
    return rows


def collect_outreach_state():
    """Hardcoded outreach checklist (static for now)."""
    return [
        ('Repo: agulaya24/memory-study-repo public', '⬜ still private'),
        ('arXiv endorsement ask to Packer', '⬜'),
        ('Blog post v2 voice pass', '🟡 drafted, needs Aarik'),
        ('Email templates (memory founders)', '⬜'),
        ('Email templates (agent builders)', '⬜'),
        ('Twitter/X thread draft', '⬜'),
        ('LinkedIn article draft', '⬜'),
        ('Reddit r/MachineLearning draft', '⬜'),
        ('Reddit r/LocalLLaMA draft', '⬜'),
        ('AI Grant application', '⬜'),
        ('Emergent Ventures application', '⬜'),
    ]


def collect_follow_ups():
    return [
        ('Living-subject study (Aarik N=1)', '⬜ future'),
        ('Letta agent-loop diff test', '⬜ deferred (rate limits)'),
        ('Independent pretraining proxy', '⬜ future'),
        ('Layer ablation (anchors/core/predictions)', '⬜ future'),
        ('Human judge validation', '⬜ future'),
        ('Cross-family generation pipeline', '⬜ future'),
    ]


class Dashboard(App):
    CSS = """
    DataTable { margin: 1; }
    Static.header { background: $primary; color: $text; padding: 1; text-align: center; text-style: bold; }
    .status { color: $accent; padding: 1; }
    """
    BINDINGS = [('r', 'refresh', 'Refresh'), ('q', 'quit', 'Quit')]

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial='paper'):
            with TabPane('Paper', id='paper'):
                yield Static('', id='paper-status', classes='status')
            with TabPane('Judging', id='judging'):
                yield DataTable(id='judging-table')
            with TabPane('Backfill', id='backfill'):
                yield DataTable(id='backfill-table')
            with TabPane('Outreach', id='outreach'):
                yield DataTable(id='outreach-table')
            with TabPane('Follow-up', id='followup'):
                yield DataTable(id='followup-table')
        yield Footer()

    def on_mount(self):
        self.populate()
        self.set_interval(30.0, self.populate)

    def action_refresh(self):
        self.populate()

    def populate(self):
        # Paper status
        p = collect_paper_state()
        paper_text = f"""📄 Beyond Recall — Paper Status
{'─' * 60}
Draft:              {'EXISTS' if p['draft_exists'] else 'MISSING'} — {p.get('word_count', 0):,} words
Last modified:      {p.get('draft_modified', '—')}
Placeholders:       {p.get('placeholders', '—')}
Dashboard doc:      {'✓' if p['dashboard_exists'] else '✗'}
Results JSON:       {'✓' if p['results_s113'] else '✗'}
Analysis plan lock: {'✓' if p['analysis_plan_locked'] else '✗'}

Launch target: Tuesday 2026-04-21
Commits to date: {self._git_commits()}
"""
        self.query_one('#paper-status', Static).update(paper_text)

        # Judging table
        tbl = self.query_one('#judging-table', DataTable)
        tbl.clear(columns=True)
        tbl.add_columns('Experiment', 'Coverage', 'Note')
        for row in collect_judging_coverage():
            tbl.add_row(*row)

        # Backfill
        tbl = self.query_one('#backfill-table', DataTable)
        tbl.clear(columns=True)
        tbl.add_columns('Job', 'Status', 'Last update')
        for row in collect_backfill_progress():
            tbl.add_row(*row)

        # Outreach
        tbl = self.query_one('#outreach-table', DataTable)
        tbl.clear(columns=True)
        tbl.add_columns('Item', 'Status')
        for row in collect_outreach_state():
            tbl.add_row(*row)

        # Follow-up
        tbl = self.query_one('#followup-table', DataTable)
        tbl.clear(columns=True)
        tbl.add_columns('Item', 'Status')
        for row in collect_follow_ups():
            tbl.add_row(*row)

    def _git_commits(self):
        try:
            import subprocess
            r = subprocess.run(['git','-C',str(REPO),'rev-list','--count','HEAD'],
                capture_output=True, text=True, timeout=5)
            return r.stdout.strip()
        except: return '—'


if __name__ == '__main__':
    Dashboard().run()
