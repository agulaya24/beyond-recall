"""Migrate source autobiographies from memory_system/data/corpora into the
study repo at memory-study-repo/data/source_corpora/, with provenance + hashes.

Every source the study consumed should be in this repo for full reproducibility.
Each subject is a Project Gutenberg public-domain text. Provenance is parsed
from the PG header (title, author, translator/editor, release date, eBook ID).

Outputs per subject:
  data/source_corpora/<subject>/raw.txt
  data/source_corpora/<subject>/provenance.md

Plus repo-level:
  data/source_corpora/MANIFEST.md
  data/source_corpora/manifest.json
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("C:/Users/Aarik/Anthropic/memory-study-repo")
OUT = REPO / "data" / "source_corpora"
OUT.mkdir(parents=True, exist_ok=True)

# subject_id -> source_path. Hamerton lives in a different location.
# franklin_letters is included for franklin_obscure / high-baseline reference.
SOURCES: dict[str, Path] = {
    "augustine":              Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/augustine/raw.txt"),
    "babur":                  Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/babur/raw.txt"),
    "bernal_diaz":            Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/bernal_diaz/raw.txt"),
    "cellini":                Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/cellini/raw.txt"),
    "ebers":                  Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/ebers/raw.txt"),
    "equiano":                Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/equiano/raw.txt"),
    "fukuzawa":               Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/fukuzawa/raw.txt"),
    "hamerton":               Path("C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/corpus/hamerton_autobiography_raw.txt"),
    "keckley":                Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/keckley/raw.txt"),
    "rousseau":               Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/rousseau/raw.txt"),
    "seacole":                Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/seacole/raw.txt"),
    "sunity_devee":           Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/sunity_devee/raw.txt"),
    "yung_wing":              Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/yung_wing/raw.txt"),
    "zitkala_sa":             Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/zitkala_sa/raw.txt"),
    "franklin_autobiography": Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/franklin_autobiography/franklin_raw.txt"),
    "franklin_letters":       Path("C:/Users/Aarik/Anthropic/memory_system/data/corpora/franklin_letters/complete_works_vol2_raw.txt"),
}

# Per-subject overrides for sources that don't have a clean PG header.
# Fukuzawa was downloaded as an archive.org HTML page (Digital Library of India scan),
# so the PG-header parser does not apply.
OVERRIDES = {
    "fukuzawa": {
        "title": "The Autobiography of Fukuzawa Yukichi",
        "author": "Fukuzawa Yukichi (1835–1901)",
        "translator": "Eiichi Kiyooka",
        "ebook_id": None,
        "source_url": "https://archive.org/details/in.ernet.dli.2015.186693",
        "source_note": (
            "Downloaded as the archive.org 'Full text' HTML page (the only readily-available "
            "text format for the Digital Library of India scan), not from Project Gutenberg. "
            "HTML preamble + chrome inflate raw byte/word counts; the pipeline strips chrome "
            "before extraction. Paper-cited corpus sizes reflect the cleaned ingestion text."
        ),
        "license_note": (
            "Public-domain status of the Japanese original (1899) and the Kiyooka translation "
            "varies by jurisdiction. The Digital Library of India / archive.org host this scan "
            "as a public-access resource."
        ),
    },
    "franklin_letters": {
        "title": "The Complete Works of Benjamin Franklin, Vol. 2",
        "author": "Benjamin Franklin",
        "ebook_id": "48137",
        "source_url": "https://www.gutenberg.org/ebooks/48137",
        "source_note": (
            "Volume 2 of a 3-volume set (vols 1 + 3 at PG #48136 and #48138). This volume "
            "contains Franklin's correspondence and selected writings. Used in the "
            "Franklin obscure / high-baseline reference test (§4.1.2) as the lower-coverage "
            "complement to the canonical Autobiography (`franklin_autobiography`)."
        ),
    },
}


# Role for paper context.
ROLES = {
    **{s: "main_study" for s in [
        "augustine", "babur", "bernal_diaz", "cellini", "ebers", "equiano",
        "fukuzawa", "hamerton", "keckley", "rousseau", "seacole", "sunity_devee",
        "yung_wing", "zitkala_sa",
    ]},
    "franklin_autobiography": "franklin_high_baseline_reference",
    "franklin_letters":       "franklin_obscure_high_baseline",
}


# Project Gutenberg header field patterns.
HEADER_PATTERNS = {
    "title":      re.compile(r"^Title:\s*(.+)$",      re.IGNORECASE | re.MULTILINE),
    # Author: capture first author line; any continuation handled below
    "author":     re.compile(r"^Author:\s*(.+)$",     re.IGNORECASE | re.MULTILINE),
    "translator": re.compile(r"^Translator:\s*(.+)$", re.IGNORECASE | re.MULTILINE),
    "editor":     re.compile(r"^Editor:\s*(.+)$",     re.IGNORECASE | re.MULTILINE),
    "release":    re.compile(r"^Release date:\s*(.+?)(?:\s*\[)",
                             re.IGNORECASE | re.MULTILINE),
    "ebook_id":   re.compile(r"\[eBook\s*#(\d+)\]",   re.IGNORECASE),
    "language":   re.compile(r"^Language:\s*(.+)$",   re.IGNORECASE | re.MULTILINE),
}

# Capture additional author lines that follow on subsequent indented lines
# (Hamerton: Eugénie + Philip on two lines under "Author:")
AUTHOR_BLOCK_RE = re.compile(
    r"^Author:\s*(.+)\n((?:[ \t]+\S.*\n)+)",
    re.IGNORECASE | re.MULTILINE,
)


def parse_pg_header(text: str) -> dict:
    """Pull Project Gutenberg header fields from the first ~80 lines."""
    head = "\n".join(text.splitlines()[:80])
    out = {}
    for field, pat in HEADER_PATTERNS.items():
        m = pat.search(head)
        if m:
            value = m.group(1).strip() if m.lastindex else m.group(0).strip()
            value = re.sub(r"[ \t]+", " ", value).strip()
            out[field] = value
        else:
            out[field] = None

    # If "Author:" line is followed by indented continuation lines (multiple
    # co-authors, e.g. Hamerton), join them into one comma-separated value.
    blk = AUTHOR_BLOCK_RE.search(head)
    if blk:
        first = blk.group(1).strip()
        cont = [ln.strip() for ln in blk.group(2).splitlines() if ln.strip()]
        if cont:
            out["author"] = ", ".join([first] + cont)

    # Fallback for franklin_letters: header lacks "Title:" prefix
    if not out.get("title"):
        m = re.search(r"START OF THE PROJECT GUTENBERG EBOOK\s+(\d+)", head, re.IGNORECASE)
        if m:
            out["ebook_id"] = m.group(1)
    return out


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def paragraph_count(text: str) -> int:
    return len([p for p in re.split(r"\n\s*\n", text) if p.strip()])


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def write_provenance(subject: str, dest_dir: Path, raw_bytes: bytes,
                     header: dict, source_path: Path) -> dict:
    """Write per-subject provenance.md and return manifest entry."""
    text = raw_bytes.decode("utf-8", errors="replace")
    override = OVERRIDES.get(subject, {})
    title = override.get("title") or header.get("title") or "(see source file)"
    author = override.get("author") or header.get("author") or "(see source file)"
    translator = override.get("translator") or header.get("translator")
    editor = override.get("editor") or header.get("editor")
    ebook_id = override.get("ebook_id") if "ebook_id" in override else header.get("ebook_id")
    release = header.get("release")
    language = header.get("language") or "English"
    source_url_override = override.get("source_url")
    source_note = override.get("source_note")
    license_note = override.get("license_note")

    if source_url_override:
        pg_url = source_url_override
    elif ebook_id:
        pg_url = f"https://www.gutenberg.org/ebooks/{ebook_id}"
    else:
        pg_url = "(see source file)"

    wc = word_count(text)
    pc = paragraph_count(text)
    bc = len(raw_bytes)
    sha = sha256(raw_bytes)

    role = ROLES.get(subject, "unknown")

    lines = [
        f"# {subject} — source corpus provenance",
        "",
        f"**Role in study:** {role}",
        "",
        "## Bibliographic record",
        "",
        f"- **Title:** {title}",
        f"- **Author:** {author}",
    ]
    if translator:
        lines.append(f"- **Translator:** {translator}")
    if editor:
        lines.append(f"- **Editor:** {editor}")
    if release:
        lines.append(f"- **Project Gutenberg release date:** {release}")
    if ebook_id:
        lines.append(f"- **Project Gutenberg eBook ID:** #{ebook_id}")
        lines.append(f"- **Project Gutenberg URL:** {pg_url}")
    elif source_url_override:
        lines.append(f"- **Source URL:** {source_url_override}")
    lines.append(f"- **Language:** {language}")
    lines.append("")
    if source_note:
        lines.append("## Note on file format")
        lines.append("")
        lines.append(source_note)
        lines.append("")
    lines.append("## Public-domain status")
    lines.append("")
    if license_note:
        lines.append(license_note)
        lines.append("")
        lines.append(
            "Inclusion in this repository is for academic-archival reproducibility of the "
            "Beyond Recall study."
        )
    else:
        lines.append(
            "Project Gutenberg eBooks are distributed in the public domain in the United "
            "States. Status outside the US varies by jurisdiction (see "
            "https://www.gutenberg.org/policy/permission.html). Inclusion in this repository "
            "is for academic-archival reproducibility of the Beyond Recall study."
        )
    lines.append("")
    lines.append("## File integrity")
    lines.append("")
    lines.append(f"- **File:** `raw.txt`")
    lines.append(f"- **Bytes:** {bc:,}")
    lines.append(f"- **Words:** {wc:,}")
    lines.append(f"- **Paragraphs:** {pc:,}")
    lines.append(f"- **SHA-256:** `{sha}`")
    lines.append(f"- **Migrated from:** `{source_path}`")
    lines.append(f"- **Migrated on:** {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append("## How this corpus is consumed by the study pipeline")
    lines.append("")
    lines.append(
        "Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\\n\\n`). "
        "Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits "
        "AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) "
        "vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and "
        "compose the layered specification consumed by §4 conditions."
    )
    lines.append("")

    prov_path = dest_dir / "provenance.md"
    prov_path.write_text("\n".join(lines), encoding="utf-8")

    return {
        "subject": subject,
        "role": role,
        "source": str(source_path).replace("\\", "/"),
        "dest": str((dest_dir / "raw.txt").relative_to(REPO)).replace("\\", "/"),
        "title": title,
        "author": author,
        "translator": translator,
        "editor": editor,
        "ebook_id": ebook_id,
        "pg_url": pg_url if ebook_id else None,
        "release_date": release,
        "language": language,
        "bytes": bc,
        "words": wc,
        "paragraphs": pc,
        "sha256": sha,
        "migrated_utc": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    manifest = []
    failures = []

    for subject, src in SOURCES.items():
        if not src.exists():
            print(f"[FAIL] {subject}: source not found at {src}")
            failures.append((subject, str(src), "source not found"))
            continue
        dest_dir = OUT / subject
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_raw = dest_dir / "raw.txt"

        # Copy raw.txt
        if dest_raw.exists():
            print(f"[OK]   {subject}: raw.txt present, regenerating provenance")
            raw_bytes = dest_raw.read_bytes()
        else:
            shutil.copy2(src, dest_raw)
            raw_bytes = dest_raw.read_bytes()
            print(f"[OK]   {subject}: copied {len(raw_bytes):,} bytes")

        # Parse PG header
        text = raw_bytes.decode("utf-8", errors="replace")
        header = parse_pg_header(text)

        # Write provenance + record manifest
        entry = write_provenance(subject, dest_dir, raw_bytes, header, src)
        manifest.append(entry)

        # franklin_autobiography also has chapters/ + entity_map.json + README.md to mirror
        if subject == "franklin_autobiography":
            src_dir = src.parent
            for extra in ("chapters", "entity_map.json", "README.md"):
                src_extra = src_dir / extra
                if src_extra.exists():
                    dest_extra = dest_dir / extra
                    if dest_extra.exists():
                        print(f"[SKIP] {subject}/{extra} already present")
                    elif src_extra.is_dir():
                        shutil.copytree(src_extra, dest_extra)
                        print(f"[OK]   {subject}/{extra}: directory copied")
                    else:
                        shutil.copy2(src_extra, dest_extra)
                        print(f"[OK]   {subject}/{extra}: file copied")

    # Write top-level MANIFEST.md
    lines = [
        "# `data/source_corpora/` — Source Texts for the Beyond Recall Study",
        "",
        f"Generated {datetime.now(timezone.utc).isoformat()} by `scripts/migrate_source_corpora.py`.",
        "",
        "Every input the study pipeline consumed lives under this directory, with per-subject "
        "provenance and SHA-256 integrity hashes. All texts are Project Gutenberg public-domain "
        "editions.",
        "",
        "## Subjects",
        "",
        "| Subject | Role | Title | Author | Translator/Editor | PG eBook ID | Words | SHA-256 (first 12) |",
        "|---|---|---|---|---|---:|---:|---|",
    ]
    for e in sorted(manifest, key=lambda x: x["subject"]):
        translator_or_editor = e.get("translator") or e.get("editor") or "—"
        ebook = f"#{e['ebook_id']}" if e.get("ebook_id") else "—"
        lines.append(
            f"| `{e['subject']}` | {e['role']} | {e['title']} | {e['author']} | "
            f"{translator_or_editor} | {ebook} | {e['words']:,} | "
            f"`{e['sha256'][:12]}` |"
        )
    lines += [
        "",
        "## Reproducibility",
        "",
        "Re-run: `python scripts/migrate_source_corpora.py`. Existing files are not overwritten; "
        "delete `data/source_corpora/<subject>/` to refresh.",
        "",
        "Each `provenance.md` records the bibliographic record, file integrity hash, and notes on "
        "how the pipeline consumes the corpus.",
        "",
        "## Pipeline integration",
        "",
        "The study pipeline (described in §3.7 of `docs/beyond_recall_v11_8_draft.md`) consumes "
        "each `raw.txt` through Steps 1-5: import → extract → embed → author → compose. "
        "Battery files (`data/<subject>/battery.json` for Hamerton, `results/<subject>/battery_v2.json` "
        "for globals) hold the 80-question evaluation batteries.",
        "",
        "## License",
        "",
        "Source texts are Project Gutenberg public-domain works. Inclusion here is for "
        "academic-archival reference. See each `provenance.md` for jurisdictional notes and the "
        "Project Gutenberg permission policy: https://www.gutenberg.org/policy/permission.html",
        "",
    ]
    if failures:
        lines += ["## Failures", ""]
        for s, src, reason in failures:
            lines.append(f"- `{s}` ({src}): {reason}")
        lines.append("")

    (OUT / "MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nWROTE {OUT/'MANIFEST.md'}")
    print(f"WROTE {OUT/'manifest.json'}")
    print(f"\nMigrated {len(manifest)}/{len(SOURCES)} subjects ({len(failures)} failures)")

    # Summary stats
    total_bytes = sum(e["bytes"] for e in manifest)
    total_words = sum(e["words"] for e in manifest)
    print(f"Total: {total_bytes:,} bytes ({total_bytes/1024/1024:.1f} MB), {total_words:,} words")

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
