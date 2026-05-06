# `docs/research/_letta_blocks/` — Letta human-memory-block analysis

**What's in this folder:** Everything produced for the Letta stateful-agent analysis where Letta's "human" memory block is treated as a compressed spec-like artifact. This backs paper §4.7.

Letta is a memory system (formerly called MemGPT) that self-edits a persistent memory block during multi-turn conversations. The question this folder answers is: does that block, on its own, reach the same predictive accuracy as a Base Layer behavioral specification?

## Contents

- `hamerton_human_block.txt`, `ebers_human_block.txt`, `babur_human_block.txt`: The final `human` memory blocks Letta produced for each of the three tested subjects after 30-turn ingestion of training text.
- `archival_pairs.txt`, `response_pairs.txt`: Paired data used for the comparison (Letta archival path vs Letta stateful path, and response-level pairings).
- `paired_scores.json`: Computed paired scores for the Letta vs Base Layer C2a comparison.
- `archival_scan.py`: Scans Letta archival outputs for the paired extract.
- `archival_pair_extract.py`: Extracts the archival-pair set.
- `extract_responses.py`: Pulls response pairs.
- `compute_paired.py`: Computes paired-score comparison.
- `check_babur_alignment.py`, `check_ebers_hamerton_alignment.py`: Sanity checks that the Letta test battery aligns with the Base Layer C2a battery for a clean comparison.

## How naming works here

The three subjects tested (Hamerton, Ebers, Babur) each have one `<subject>_human_block.txt`. All computation scripts are plain `.py`. Pair and paired-score files are JSON or plain text. This folder is fully flat.

## Where these files come from / go to

Inputs: Letta run outputs and response batteries generated elsewhere in the repo. Outputs feed into paper §4.7 (Letta architectural convergence) and the memo at `docs/research/letta_stateful_deep_read.md`.

## Caveats worth knowing

- Babur's final memory block reached 335,349 characters. Letta began rejecting further ingestion at ~332,585 characters (22 failed attempts). The scaling-ceiling discussion in the paper rests on this.
- Letta's stateful-agent path is architecturally different from the archival-retrieval path tested in §4.3. Do not conflate the two when reading these outputs.
- Tested on three subjects only. Generalization is listed as future work.
