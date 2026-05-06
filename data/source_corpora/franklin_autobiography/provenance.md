# franklin_autobiography — source corpus provenance

**Role in study:** franklin_high_baseline_reference

## Bibliographic record

- **Title:** Autobiography of Benjamin Franklin
- **Author:** Benjamin Franklin
- **Editor:** Frank Woodworth Pine
- **Project Gutenberg release date:** December 28, 2006
- **Project Gutenberg eBook ID:** #20203
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/20203
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 467,473
- **Words:** 79,259
- **Paragraphs:** 986
- **SHA-256:** `a788e84346327fa709f3866a3246bef7949eb04b3f43108a4b632461d49d5f59`
- **Migrated from:** `C:\Users\Aarik\Anthropic\memory_system\data\corpora\franklin_autobiography\franklin_raw.txt`
- **Migrated on:** 2026-05-05T21:43:49.602865+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
