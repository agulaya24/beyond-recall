# ebers — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** The Story of My Life — Complete
- **Author:** Georg Ebers
- **Translator:** Mary J. Safford
- **Project Gutenberg release date:** November 15, 2004
- **Project Gutenberg eBook ID:** #5599
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/5599
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 570,047
- **Words:** 96,174
- **Paragraphs:** 1,427
- **SHA-256:** `f3a91b0405bb320350ba2a6a9eca2b508d2d161c12516219f954e20ed8261928`
- **Migrated on:** 2026-05-05T21:43:49.352966+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
