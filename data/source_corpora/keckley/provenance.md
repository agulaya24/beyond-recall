# keckley — source corpus provenance

**Role in study:** main_study

## Bibliographic record

- **Title:** Behind the Scenes; or, Thirty years a slave, and Four Years in the White House
- **Author:** Elizabeth Keckley
- **Project Gutenberg release date:** March 31, 2008
- **Project Gutenberg eBook ID:** #24968
- **Project Gutenberg URL:** https://www.gutenberg.org/ebooks/24968
- **Language:** English

## Public-domain status

Project Gutenberg eBooks are distributed in the public domain in the United States. Status outside the US varies by jurisdiction (see https://www.gutenberg.org/policy/permission.html). Inclusion in this repository is for academic-archival reproducibility of the Beyond Recall study.

## File integrity

- **File:** `raw.txt`
- **Bytes:** 350,249
- **Words:** 61,831
- **Paragraphs:** 1,043
- **SHA-256:** `609ce1264179bb25c000f828e3322802d638ce2dbb05eaec02aac6d898092022`
- **Migrated from:** `C:\Users\Aarik\Anthropic\memory_system\data\corpora\keckley\raw.txt`
- **Migrated on:** 2026-05-05T21:43:49.469417+00:00

## How this corpus is consumed by the study pipeline

Step 1 (import) ingests `raw.txt` while preserving paragraph boundaries (`\n\n`). Step 2 (extract_facts.py) chunks on paragraph breaks with 500-char overlap and emits AUDN triples constrained to the 46-predicate vocabulary in Appendix A. Step 3 (embed.py) vectorizes facts via `sentence-transformers/all-MiniLM-L6-v2`. Steps 4-5 author and compose the layered specification consumed by §4 conditions.
