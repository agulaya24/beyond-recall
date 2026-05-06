# fukuzawa — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** The Autobiography of Fukuzawa Yukichi
- **Author:** Fukuzawa Yukichi (1835–1901)
- **Translator:** Eiichi Kiyooka
- **Source URL:** https://archive.org/details/in.ernet.dli.2015.186693
- **Language:** English

## Note on file format

Downloaded as the archive.org 'Full text' HTML page (the only readily-available text format for the Digital Library of India scan), not from Project Gutenberg. HTML preamble + chrome inflate raw byte/word counts; the pipeline strips chrome before extraction. Paper-cited corpus sizes reflect the cleaned ingestion text.

## Public-domain status

Public-domain status of the Japanese original (1899) and the Kiyooka translation varies by jurisdiction. The Digital Library of India / archive.org host this scan as a public-access resource.

Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 907,497
- **Words:** 139,088
- **Paragraphs:** 4,605
- **SHA-256:** `2b5cc85787df10cb08c333174e297ac2ef62465dd89135e87927c125ff5e52b1`
- **Migrated from:** `C:\Users\Aarik\Anthropic\memory_system\data\corpora\fukuzawa\raw.txt`
- **Migrated on:** 2026-05-05T21:43:49.408091+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
