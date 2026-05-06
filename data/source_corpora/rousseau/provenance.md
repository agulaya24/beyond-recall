# rousseau — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** The Confessions of Jean Jacques Rousseau — Complete
- **Author:** Jean-Jacques Rousseau
- **Project Gutenberg release date:** August 15, 2004
- **Project Gutenberg eBook ID:** #3913
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/3913
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 1,585,959
- **Words:** 278,120
- **Paragraphs:** 1,586
- **SHA-256:** `3ab4d68f81e2da40c94418a8f6beb30aac82eafd8faaf546cdeeaf0d16d61b8a`
- **Migrated from:** `C:\Users\Aarik\Anthropic\memory_system\data\corpora\rousseau\raw.txt`
- **Migrated on:** 2026-05-05T21:43:49.530571+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
