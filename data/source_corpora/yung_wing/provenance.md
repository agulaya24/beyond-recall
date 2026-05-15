# yung_wing — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** My Life in China and America
- **Author:** Wing Yung
- **Project Gutenberg release date:** April 30, 2017
- **Project Gutenberg eBook ID:** #54635
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/54635
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 392,202
- **Words:** 66,459
- **Paragraphs:** 937
- **SHA-256:** `5d67fdb3d1c107d1bd75fcea1447d15bb8df06957a87a9cb15b2e661a4508b7c`
- **Migrated on:** 2026-05-05T21:43:49.575812+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
