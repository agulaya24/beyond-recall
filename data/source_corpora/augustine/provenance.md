# augustine — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** The Confessions of St. Augustine
- **Author:** Saint of Hippo Augustine
- **Translator:** E. B. Pusey
- **Project Gutenberg release date:** June 1, 2002
- **Project Gutenberg eBook ID:** #3296
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/3296
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 632,170
- **Words:** 114,873
- **Paragraphs:** 541
- **SHA-256:** `20f5b0791e2307186e3db1f80a90f2083ace32a00c5074011dd47d1cb3bb6e00`
- **Migrated on:** 2026-05-05T21:43:49.139581+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
