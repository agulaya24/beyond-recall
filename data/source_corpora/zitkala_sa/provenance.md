# zitkala_sa — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** American Indian Stories
- **Author:** Zitkala-Sa
- **Project Gutenberg release date:** December 1, 2003
- **Project Gutenberg eBook ID:** #10376
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/10376
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 201,900
- **Words:** 35,328
- **Paragraphs:** 670
- **SHA-256:** `e802c1a2ed4553bf128dad265cf5ce0277aeba26a9c33a295563f62eacc34459`
- **Migrated on:** 2026-05-05T21:43:49.584827+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
