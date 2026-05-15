"""Download arXiv PDFs for every §9 reference of beyond_recall_v11_8_draft.md.

Pulls each PDF into docs/references/<surname>_<year>_<arxiv_id>.pdf.
Writes docs/references/MANIFEST.md recording source URLs, fetch timestamps,
and SHA-256 hashes for archival integrity.

Bartlett 1932 is not on arXiv (book); a stub note is written instead.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "references"
OUT.mkdir(parents=True, exist_ok=True)

# (surname, year, arxiv_id, paper_title_short) — extracted from §9 of v11.8
REFERENCES = [
    ("Chen",      2025, "2507.21509", "Persona vectors"),
    ("Chhikara",  2025, "2504.19413", "Mem0"),
    ("Hinton",    2015, "1503.02531", "Distilling the knowledge in a neural network"),
    ("Jain",      2025, "2509.12517", "Interaction context sycophancy"),
    ("Jiang",     2025, "2504.14225", "Know me respond to me"),
    ("Lu",        2026, "2601.10387", "The Assistant Axis"),
    ("Maharana",  2024, "2402.17753", "Very long-term conversational memory"),
    ("Packer",    2023, "2310.08560", "MemGPT"),
    ("Perez",     2022, "2212.09251", "Discovering language model behaviors"),
    ("Rasmussen", 2025, "2501.13956", "Zep"),
    ("Samuel",    2025, "2407.18416", "PersonaGym"),
    ("Sharma",    2023, "2310.13548", "Towards understanding sycophancy"),
    ("Toubia",    2025, "2505.17479", "Twin-2K-500"),
    ("Verga",     2024, "2404.18796", "Replacing judges with juries"),
    ("Wu",        2025, "2410.10813", "LongMemEval"),
    ("Xiao",      2026, "2603.26680", "AlpsBench"),
    ("Zheng",     2023, "2306.05685", "Judging LLM-as-a-judge / MT-Bench"),
]


def fetch(url: str, dest: Path, timeout: int = 60) -> dict:
    """Download URL to dest. Return manifest entry."""
    started = datetime.now(timezone.utc).isoformat()
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "memory-study-repo/1.0 (academic archival; Aarik Gulaya)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            content = r.read()
            content_type = r.headers.get("Content-Type", "")
        dest.write_bytes(content)
        sha = hashlib.sha256(content).hexdigest()
        return {
            "url": url,
            "dest": str(dest.relative_to(REPO)),
            "fetched_utc": started,
            "size_bytes": len(content),
            "content_type": content_type,
            "sha256": sha,
            "status": "OK",
        }
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        return {
            "url": url,
            "dest": str(dest.relative_to(REPO)),
            "fetched_utc": started,
            "status": f"FAIL: {type(e).__name__}: {e}",
        }


def main() -> int:
    manifest = []

    for surname, year, arxiv_id, short in REFERENCES:
        # Slug-safe title fragment
        slug = short.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
        pdf_name = f"{surname.lower()}_{year}_{arxiv_id}_{slug}.pdf"
        dest = OUT / pdf_name
        url = f"https://arxiv.org/pdf/{arxiv_id}"
        if dest.exists():
            sha = hashlib.sha256(dest.read_bytes()).hexdigest()
            entry = {
                "url": url,
                "dest": str(dest.relative_to(REPO)),
                "fetched_utc": "preexisting",
                "size_bytes": dest.stat().st_size,
                "sha256": sha,
                "status": "EXISTS",
            }
        else:
            print(f"Fetching {surname} {year} ({arxiv_id})...", flush=True)
            entry = fetch(url, dest)
            time.sleep(2)  # be polite to arXiv
        entry.update({"surname": surname, "year": year, "arxiv_id": arxiv_id, "title": short})
        manifest.append(entry)
        print(f"  -> {entry.get('status')} ({entry.get('size_bytes', 0):,} bytes)", flush=True)

    # Bartlett 1932 stub
    bartlett_note = OUT / "bartlett_1932_NOTE.md"
    bartlett_note.write_text(
        "# Bartlett 1932 — *Remembering: A Study in Experimental and Social Psychology*\n\n"
        "Cambridge University Press, 1932. Not on arXiv (predates arXiv).\n\n"
        "Cited in §1.2 footnote 2 of `beyond_recall_v11_8_draft.md` as the foundational "
        "schema-theoretic framing for memory: recall as reconstruction shaped by prior "
        "structure rather than verbatim retrieval.\n\n"
        "**Canonical record (per Cambridge UP catalog, Library of Congress, OCLC WorldCat):**\n\n"
        "- Author: Sir Frederic Charles Bartlett (1886-1969)\n"
        "- Title: *Remembering: A Study in Experimental and Social Psychology*\n"
        "- Publisher: Cambridge University Press\n"
        "- First published: 1932\n"
        "- 1995 reprint with introduction by W. Kintsch: ISBN 978-0-521-48356-8\n"
        "- 50 pages of plates + xxiv + 317 pages\n\n"
        "PDF not included in this repo. Public-domain status varies by jurisdiction; "
        "current reprint is in copyright. Reproductions are widely available via "
        "academic libraries and archive.org.\n",
        encoding="utf-8",
    )
    manifest.append({
        "url": "https://www.cambridge.org/core/books/remembering",
        "dest": str(bartlett_note.relative_to(REPO)),
        "fetched_utc": datetime.now(timezone.utc).isoformat(),
        "status": "MANUAL_NOTE (book, no arXiv equivalent)",
        "surname": "Bartlett",
        "year": 1932,
        "arxiv_id": None,
        "title": "Remembering",
    })

    # Write MANIFEST.md
    manifest_path = OUT / "MANIFEST.md"
    lines = [
        "# References — Beyond Recall v11.8 §9",
        "",
        f"Manifest generated {datetime.now(timezone.utc).isoformat()}.",
        "",
        "Every reference cited in §9 of `docs/beyond_recall_v11_8_draft.md`.",
        "PDFs fetched from arXiv abstract page redirects (`https://arxiv.org/pdf/<ID>`).",
        "Bartlett 1932 is a book (Cambridge UP, predates arXiv); a canonical-record note is included instead.",
        "",
        "## Manifest",
        "",
        "| Author (year) | arXiv ID | File | Size (KB) | SHA-256 (first 12) | Status |",
        "|---|---|---|---:|---|---|",
    ]
    for e in manifest:
        sha = e.get("sha256", "")
        sha_short = sha[:12] if sha else "—"
        size_kb = round((e.get("size_bytes", 0) or 0) / 1024)
        size_str = f"{size_kb:,}" if size_kb else "—"
        arxiv = e.get("arxiv_id") or "—"
        fname = Path(e["dest"]).name
        lines.append(
            f"| {e['surname']} ({e['year']}) | {arxiv} | `{fname}` | {size_str} | `{sha_short}` | {e['status']} |"
        )
    lines += [
        "",
        "## Reproducibility",
        "",
        "Re-run: `python scripts/fetch_references.py`. Existing PDFs are not redownloaded.",
        "",
        "Each PDF's SHA-256 is recorded above for integrity verification.",
        "",
        "## License notes",
        "",
        "arXiv PDFs are distributed under their respective license terms (typically arXiv "
        "non-exclusive license to arXiv.org or a CC-BY variant chosen by the authors). "
        "Inclusion in this repository is for academic-archival reference only and does not "
        "extend or modify those terms.",
        "",
    ]
    manifest_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWROTE {manifest_path}")
    print(f"WROTE {bartlett_note}")

    # Also persist as JSON for programmatic use
    json_path = OUT / "manifest.json"
    json_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"WROTE {json_path}")

    n_ok = sum(1 for e in manifest if e["status"] in ("OK", "EXISTS"))
    n_fail = sum(1 for e in manifest if e["status"].startswith("FAIL"))
    print(f"\nDone. {n_ok} OK, {n_fail} failed, {len(manifest) - n_ok - n_fail} manual notes.")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
