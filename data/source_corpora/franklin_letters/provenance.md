# franklin_letters — source corpus provenance

**Role in study:** franklin_obscure_high_baseline

## Bibliographic record

- **Title:** The Complete Works of Benjamin Franklin, Vol. 2
- **Author:** Benjamin Franklin
- **Project Gutenberg eBook ID:** #48137
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/48137
- **Language:** English

## Note on file format

Volume 2 of a 3-volume set (vols 1 + 3 at PG #48136 and #48138). This volume contains Franklin's correspondence and selected writings. Used in the Franklin obscure / high-baseline reference test (§4.1.2) as the lower-coverage complement to the canonical Autobiography (`franklin_autobiography`).

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 901,589
- **Words:** 151,371
- **Paragraphs:** 2,795
- **SHA-256:** `0ca3cf2f48d1869ec1fe289f5c69cbeba3c49c3eadc2bd446a26c1e070a52b36`
- **Migrated on:** 2026-05-05T21:43:49.637923+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
