# sunity_devee — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** The Autobiography of an Indian Princess
- **Author:** Maharani of Cooch Behar Sunity Devee
- **Project Gutenberg release date:** May 17, 2018
- **Project Gutenberg eBook ID:** #57175
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/57175
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 387,921
- **Words:** 67,378
- **Paragraphs:** 1,171
- **SHA-256:** `7935b6d8f3acfe69d7ddaf68a8d60aa80bd9bc9da1133d256b629fd200734351`
- **Migrated from:** `C:\Users\Aarik\Anthropic\memory_system\data\corpora\sunity_devee\raw.txt`
- **Migrated on:** 2026-05-05T21:43:49.559278+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
