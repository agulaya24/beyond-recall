# babur — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** The Bābur-nāma in English (Memoirs of Bābur)
- **Author:** Emperor of Hindustan Babur
- **Translator:** Annette Susannah Beveridge
- **Project Gutenberg release date:** January 7, 2014
- **Project Gutenberg eBook ID:** #44608
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/44608
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 2,786,879
- **Words:** 422,769
- **Paragraphs:** 9,822
- **SHA-256:** `47c48eec416898cc7da98e3a999e1db39639daf45314752d6ddbac902e3ece92`
- **Migrated on:** 2026-05-05T21:43:49.242810+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
