# equiano — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** The Interesting Narrative of the Life of Olaudah Equiano, Or Gustavus Vassa, The African
- **Author:** Olaudah Equiano
- **Project Gutenberg release date:** March 17, 2005
- **Project Gutenberg eBook ID:** #15399
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/15399
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 479,263
- **Words:** 85,660
- **Paragraphs:** 497
- **SHA-256:** `70a1e2d4e33c9ec46725ee8bb1f8f7de7423f691b02cc7eb29337ab948f1b533`
- **Migrated from:** `C:\Users\Aarik\Anthropic\memory_system\data\corpora\equiano\raw.txt`
- **Migrated on:** 2026-05-05T21:43:49.370504+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
