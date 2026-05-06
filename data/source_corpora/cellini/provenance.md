# cellini — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** The Autobiography of Benvenuto Cellini
- **Author:** Benvenuto Cellini
- **Translator:** John Addington Symonds
- **Project Gutenberg release date:** May 1, 2003
- **Project Gutenberg eBook ID:** #4028
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/4028
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 1,054,021
- **Words:** 190,389
- **Paragraphs:** 1,515
- **SHA-256:** `f8ca08da8c99f5993ae76a0232586e410c912526d02da634b2ec1a56cced6b25`
- **Migrated from:** `C:\Users\Aarik\Anthropic\memory_system\data\corpora\cellini\raw.txt`
- **Migrated on:** 2026-05-05T21:43:49.330407+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
