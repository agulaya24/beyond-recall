# seacole — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** Wonderful Adventures of Mrs. Seacole in Many Lands
- **Author:** Mary Seacole
- **Editor:** W. J. S.
- **Project Gutenberg release date:** October 14, 2007
- **Project Gutenberg eBook ID:** #23031
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/23031
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 363,626
- **Words:** 62,467
- **Paragraphs:** 627
- **SHA-256:** `3f69bc831c77410f514bf20a532216c9406f375a925f97619c3e393a78477d73`
- **Migrated from:** `C:\Users\Aarik\Anthropic\memory_system\data\corpora\seacole\raw.txt`
- **Migrated on:** 2026-05-05T21:43:49.544109+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
