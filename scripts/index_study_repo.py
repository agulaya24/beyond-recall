"""Index every study-related file in memory-study-repo + experiment results dir.

Builds a focused SQLite + ChromaDB knowledge store for semantic search over
the entire study output. Designed to run once overnight and produce a
queryable index for the post-launch review.

Usage:
    python index_study_repo.py            # Build/refresh index
    python index_study_repo.py --search "Letta scaling"   # Query

Outputs:
    workspace/study_knowledge.db    SQLite (file metadata + chunk text + FTS)
    workspace/study_vectors/        ChromaDB collection
"""
import os, sys, json, sqlite3, argparse, time, hashlib, re
from pathlib import Path
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

REPO = Path('C:/Users/Aarik/Anthropic/memory-study-repo')
RESULTS = Path('C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results')
WORKSPACE = REPO / 'workspace'
WORKSPACE.mkdir(exist_ok=True)
DB_PATH = WORKSPACE / 'study_knowledge.db'
VEC_PATH = WORKSPACE / 'study_vectors'

# File scopes to index
INDEX_SCOPES = {
    'paper': [REPO / 'docs' / 'beyond_recall_v6_draft.md',
              REPO / 'docs' / 'KEY_FINDINGS.md',
              REPO / 'docs' / 'DATA_REFERENCE.md',
              REPO / 'docs' / 'METHODOLOGY.md',
              REPO / 'docs' / 'PROVENANCE_INDEX.md',
              REPO / 'docs' / 'ANALYSIS_PLAN_LOCK.md',
              REPO / 'docs' / 'PAPER_CORRECTIONS.md',
              REPO / 'docs' / 'REFERENCE_TABLE.md',
              REPO / 'README.md',
              REPO / 'agents' / 'study-guide.md',
              REPO / 'agents' / 'STUDY_MEMORY.md'],
    'reviews': sorted((REPO / 'docs' / 'reviews').glob('*.md')) if (REPO / 'docs' / 'reviews').exists() else [],
    'blog': [REPO / 'docs' / 'blog_post_v2.md'],
    'data_specs': sorted(REPO.glob('data/**/spec*.md')) + sorted(REPO.glob('data/**/brief*.md')) + sorted(REPO.glob('data/**/*_v4.md')),
    'data_facts': sorted(REPO.glob('data/**/facts*.json'))[:20],  # cap to avoid bloat
    'results_summary': sorted(RESULTS.glob('RESULTS_*.json')) + sorted(RESULTS.glob('summary*.json')),
    'results_judgments': sorted(RESULTS.glob('**/letta_memory_haiku_judgments_*.json')) +
                         sorted(RESULTS.glob('**/letta_stateful_judgments_*.json'))[:30],
    'results_letta_blocks': sorted(RESULTS.glob('**/letta_stateful_test_result.json')),
    'results_responses': sorted(RESULTS.glob('**/letta_memory_haiku_results.json')),
    'analysis_scripts': sorted(REPO.glob('scripts/*.py'))[:20] +
                        sorted(Path('C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems').glob('run_*.py'))[:15] +
                        sorted(Path('C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems').glob('judge_*.py'))[:10] +
                        [Path('C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/string_match_disagreement.py')],
}


def init_db():
    c = sqlite3.connect(DB_PATH)
    c.execute('''CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scope TEXT, path TEXT UNIQUE, filename TEXT,
        size_bytes INTEGER, indexed_at TEXT, content_hash TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER, scope TEXT, chunk_idx INTEGER,
        chunk_kind TEXT, label TEXT, text TEXT,
        char_start INTEGER, char_end INTEGER,
        FOREIGN KEY(file_id) REFERENCES files(id))''')
    c.execute('CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(text, content="chunks", content_rowid="id")')
    c.commit()
    return c


def chunk_markdown(text, label_prefix=''):
    """Split markdown by H2/H3 headings."""
    lines = text.split('\n')
    chunks, current_label, current_text, char_start = [], label_prefix or 'intro', [], 0
    char_pos = 0
    for line in lines:
        m = re.match(r'^#{2,3}\s+(.+)$', line)
        if m and current_text:
            chunks.append((current_label, '\n'.join(current_text), char_start, char_pos))
            current_text = [line]
            current_label = m.group(1)[:120]
            char_start = char_pos
        else:
            current_text.append(line)
        char_pos += len(line) + 1
    if current_text:
        chunks.append((current_label, '\n'.join(current_text), char_start, char_pos))
    return [(l, t.strip(), s, e) for l, t, s, e in chunks if len(t.strip()) > 30]


def chunk_json(data, path, label_prefix=''):
    """Flatten JSON into chunks. For lists, one chunk per item up to a cap."""
    chunks = []
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (list, dict)) and len(json.dumps(v, default=str)) > 200:
                chunks.extend(chunk_json(v, f'{path}.{k}', f'{label_prefix}{k}'))
            else:
                txt = f'{k}: {json.dumps(v, default=str, ensure_ascii=False)[:600]}'
                chunks.append((f'{label_prefix}{k}'[:120], txt, 0, len(txt)))
    elif isinstance(data, list):
        for i, item in enumerate(data[:50]):
            txt = json.dumps(item, default=str, ensure_ascii=False)[:1500]
            chunks.append((f'{label_prefix}[{i}]'[:120], txt, 0, len(txt)))
    return chunks


def index_file(c, scope, path):
    if not path.exists() or path.is_dir():
        return 0
    try:
        content = path.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f'  skip {path.name}: {e}')
        return 0
    h = hashlib.sha1(content.encode('utf-8', errors='ignore')).hexdigest()[:16]
    existing = c.execute('SELECT id, content_hash FROM files WHERE path=?', (str(path),)).fetchone()
    if existing and existing[1] == h:
        return 0
    if existing:
        c.execute('DELETE FROM chunks WHERE file_id=?', (existing[0],))
        c.execute('UPDATE files SET indexed_at=?, content_hash=?, size_bytes=? WHERE id=?',
                  (datetime.now(timezone.utc).isoformat(), h, len(content), existing[0]))
        file_id = existing[0]
    else:
        cur = c.execute('INSERT INTO files (scope, path, filename, size_bytes, indexed_at, content_hash) VALUES (?,?,?,?,?,?)',
                        (scope, str(path), path.name, len(content), datetime.now(timezone.utc).isoformat(), h))
        file_id = cur.lastrowid
    if path.suffix == '.md':
        chunks = chunk_markdown(content, label_prefix='')
        kind = 'section'
    elif path.suffix == '.json':
        try:
            data = json.loads(content)
            chunks = chunk_json(data, path.name)
            kind = 'json_record'
        except Exception:
            chunks = [(path.name, content[:2000], 0, min(2000, len(content)))]
            kind = 'raw'
    elif path.suffix == '.py':
        # Chunk python by top-level def/class
        chunks = []
        cur_label, cur_text, char_start, char_pos = 'module', [], 0, 0
        for line in content.split('\n'):
            m = re.match(r'^(?:def|class)\s+(\w+)', line)
            if m and cur_text:
                chunks.append((cur_label, '\n'.join(cur_text), char_start, char_pos))
                cur_text = [line]
                cur_label = m.group(1)[:120]
                char_start = char_pos
            else:
                cur_text.append(line)
            char_pos += len(line) + 1
        if cur_text:
            chunks.append((cur_label, '\n'.join(cur_text), char_start, char_pos))
        kind = 'pyfn'
    else:
        chunks = [(path.name, content[:2000], 0, min(2000, len(content)))]
        kind = 'raw'
    n_chunks = 0
    for i, (label, text, cs, ce) in enumerate(chunks):
        if len(text.strip()) < 20: continue
        cur = c.execute('INSERT INTO chunks (file_id, scope, chunk_idx, chunk_kind, label, text, char_start, char_end) VALUES (?,?,?,?,?,?,?,?)',
                        (file_id, scope, i, kind, label[:120], text[:8000], cs, ce))
        c.execute('INSERT INTO chunks_fts (rowid, text) VALUES (?, ?)', (cur.lastrowid, text[:8000]))
        n_chunks += 1
    return n_chunks


def build_index():
    c = init_db()
    total_files = total_chunks = 0
    for scope, paths in INDEX_SCOPES.items():
        print(f'Scope: {scope} ({len(paths)} candidate paths)')
        scope_chunks = scope_files = 0
        for p in paths:
            if not isinstance(p, Path): continue
            n = index_file(c, scope, p)
            if n > 0:
                scope_chunks += n
                scope_files += 1
        c.commit()
        print(f'  {scope}: {scope_files} files, {scope_chunks} chunks')
        total_files += scope_files
        total_chunks += scope_chunks
    print(f'\\nTotal: {total_files} files, {total_chunks} chunks indexed')

    # Build vector index now (separate step using MiniLM)
    print('\\nBuilding vector index...')
    try:
        from sentence_transformers import SentenceTransformer
        import chromadb
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        client = chromadb.PersistentClient(path=str(VEC_PATH))
        try: client.delete_collection('study')
        except: pass
        col = client.create_collection('study')
        rows = c.execute('SELECT id, scope, label, text FROM chunks').fetchall()
        BATCH = 64
        for i in range(0, len(rows), BATCH):
            batch = rows[i:i+BATCH]
            ids = [str(r[0]) for r in batch]
            docs = [r[3] for r in batch]
            embs = model.encode(docs, show_progress_bar=False).tolist()
            metas = [{'scope': r[1], 'label': r[2]} for r in batch]
            col.add(ids=ids, documents=docs, embeddings=embs, metadatas=metas)
            if (i // BATCH) % 10 == 0:
                print(f'  embedded {i+len(batch)}/{len(rows)}')
        print(f'  done: {len(rows)} chunks embedded')
    except ImportError as e:
        print(f'  skipped vector index: {e} (FTS available via SQLite)')

    c.close()


def search(query, n=10):
    c = sqlite3.connect(DB_PATH)
    print(f'\\nFTS search for: {query!r}')
    rows = c.execute("""SELECT chunks.scope, chunks.label, snippet(chunks_fts, 0, '[', ']', '...', 32), files.filename
        FROM chunks_fts JOIN chunks ON chunks.id=chunks_fts.rowid JOIN files ON chunks.file_id=files.id
        WHERE chunks_fts MATCH ? ORDER BY rank LIMIT ?""", (query, n)).fetchall()
    for scope, label, snip, fn in rows:
        print(f'  [{scope}] {fn} > {label}')
        print(f'    {snip[:200]}')

    # Semantic search if vectors available
    try:
        from sentence_transformers import SentenceTransformer
        import chromadb
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        client = chromadb.PersistentClient(path=str(VEC_PATH))
        col = client.get_collection('study')
        emb = model.encode([query]).tolist()
        res = col.query(query_embeddings=emb, n_results=n)
        print(f'\\nSemantic search for: {query!r}')
        for i in range(len(res['ids'][0])):
            meta = res['metadatas'][0][i]
            doc = res['documents'][0][i][:200]
            print(f"  [{meta['scope']}] {meta['label']}")
            print(f'    {doc}')
    except Exception as e:
        print(f'\\n(vector search unavailable: {e})')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--search', help='Search query (FTS + semantic)')
    p.add_argument('--n', type=int, default=10)
    a = p.parse_args()
    if a.search:
        search(a.search, a.n)
    else:
        build_index()


if __name__ == '__main__':
    main()
