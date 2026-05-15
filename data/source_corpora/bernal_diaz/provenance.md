# bernal_diaz — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** The Memoirs of the Conquistador Bernal Diaz del Castillo, Vol 1 (of 2)
- **Author:** Bernal Díaz del Castillo
- **Translator:** John Ingram Lockhart
- **Project Gutenberg release date:** May 21, 2010
- **Project Gutenberg eBook ID:** #32474
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/32474
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 1,102,083
- **Words:** 187,315
- **Paragraphs:** 1,772
- **SHA-256:** `416854d7afd5f7f7ee0e15dd7d630d864c2f739288de4bc1083429336f55517e`
- **Migrated on:** 2026-05-05T21:43:49.289484+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
