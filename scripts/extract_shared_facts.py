"""
Extract ~500 neutral declarative facts from Hamerton chapters 1-10.
Uses Haiku to extract simple, system-agnostic facts.
No Base Layer predicates, no tiering — just plain English assertions.
"""

import json
import os
import sys
import hashlib

import anthropic

# NOTE: depends on the separate (private) memory_system repo. Set MEMORY_SYSTEM_ROOT
# to its path; defaults to empty so the missing-path failure is obvious.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
TIER_FILE = os.path.join(MEMORY_SYSTEM_ROOT, "data/experiments/memory_systems/corpus/tiers/tier_02_ch01-10.txt")
OUTPUT_FILE = os.path.join(MEMORY_SYSTEM_ROOT, "data/experiments/memory_systems/shared_facts.json")

# Chunk the text into ~3000 word segments for extraction
def chunk_text(text, max_words=3000, overlap_words=200):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap_words if end < len(words) else end
    return chunks


EXTRACTION_PROMPT = """Extract factual assertions from this autobiography text. Each fact should be:
- A single, self-contained declarative sentence
- About the author (Philip Gilbert Hamerton) or his world
- Stated in plain English, no jargon
- Specific enough to be useful (not "he liked art" but "he began drawing at age 8")
- Include facts about: values, decisions, relationships, habits, beliefs, events, personality traits, skills, preferences, fears, motivations

Extract as many facts as you can find. Return ONLY a JSON array of strings, no other text.

Example output format:
["Hamerton lost his mother when he was very young.", "Hamerton believed intellectual honesty was more important than social approval.", "Hamerton's father was rarely present during his childhood."]

Text to extract from:
---
{text}
---

Return ONLY the JSON array."""


def extract_facts_from_chunk(client, chunk, chunk_idx):
    """Extract facts from a single text chunk using Haiku."""
    print(f"  Extracting from chunk {chunk_idx} ({len(chunk.split())} words)...")

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        temperature=0,
        messages=[{
            "role": "user",
            "content": EXTRACTION_PROMPT.format(text=chunk)
        }]
    )

    text = response.content[0].text.strip()
    # Strip markdown code blocks if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text[:-3].strip()
    # Parse JSON array
    if text.startswith("["):
        try:
            facts = json.loads(text)
            print(f"    -> {len(facts)} facts extracted")
            return facts
        except json.JSONDecodeError:
            # Try to fix common issues
            text = text.replace("'", '"')
            try:
                facts = json.loads(text)
                print(f"    -> {len(facts)} facts extracted (after fix)")
                return facts
            except:
                print(f"    -> JSON parse failed")
                return []
    else:
        print(f"    -> Unexpected format: {text[:100]}")
        return []


def deduplicate_facts(facts, threshold=0.95):
    """Simple deduplication by normalized string similarity."""
    seen = set()
    unique = []
    for fact in facts:
        normalized = fact.lower().strip().rstrip(".")
        if normalized not in seen:
            seen.add(normalized)
            unique.append(fact)
    return unique


def main():
    # Read corpus
    with open(TIER_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"Corpus: {len(text.split())} words")

    # Chunk
    chunks = chunk_text(text)
    print(f"Split into {len(chunks)} chunks")

    # Extract
    client = anthropic.Anthropic()
    all_facts = []

    for i, chunk in enumerate(chunks):
        facts = extract_facts_from_chunk(client, chunk, i + 1)
        all_facts.extend(facts)

    print(f"\nTotal raw facts: {len(all_facts)}")

    # Deduplicate
    unique_facts = deduplicate_facts(all_facts)
    print(f"After dedup: {len(unique_facts)}")

    # Assign IDs and compute checksums
    fact_records = []
    for i, fact in enumerate(unique_facts):
        fact_records.append({
            "id": i + 1,
            "text": fact,
            "checksum": hashlib.sha256(fact.encode()).hexdigest()[:16]
        })

    # Compute corpus checksum
    corpus_checksum = hashlib.sha256(text.encode()).hexdigest()

    output = {
        "metadata": {
            "source": "hamerton_autobiography_chapters_1-10",
            "source_file": TIER_FILE,
            "corpus_checksum": corpus_checksum,
            "total_facts": len(fact_records),
            "extraction_model": "claude-haiku-4-5-20251001",
            "extraction_temperature": 0,
            "chunks_processed": len(chunks),
        },
        "facts": fact_records
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(fact_records)} facts to {OUTPUT_FILE}")
    print(f"Corpus checksum: {corpus_checksum[:16]}...")

    # Show sample
    print("\nSample facts:")
    for fact in fact_records[:10]:
        print(f"  [{fact['id']}] {fact['text']}")


if __name__ == "__main__":
    main()
