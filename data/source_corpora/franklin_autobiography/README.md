# Franklin Autobiography — Base Layer Case Study

## Source
Project Gutenberg EBook #20203 — *Autobiography of Benjamin Franklin*
Edited by Frank Woodworth Pine (Henry Holt, 1916)
Public domain.

## Corpus Stats
- 21 chapter files (Introduction + 19 chapters + Appendix)
- 75,383 words total
- Cleaned: Gutenberg header/footer stripped, [Illustration] tags removed

## To Run Pipeline

```bash
# Set environment for isolated Franklin data
export MEMORY_SYSTEM_ROOT=./franklin_memory

# Initialize
baselayer init

# Copy entity_map.json to franklin_memory/data/
cp data/corpora/franklin_autobiography/entity_map.json $MEMORY_SYSTEM_ROOT/data/entity_map.json

# Import all chapters (each becomes one "conversation")
baselayer import --text data/corpora/franklin_autobiography/chapters/

# Run full pipeline
baselayer extract
baselayer process
baselayer checkpoint extraction
baselayer checkpoint scoring
baselayer checkpoint classification

# If checkpoints pass:
baselayer author --agent-pipeline
```

## Expected Yield
- ~190-210 raw facts (10-15 per chapter at current cap)
- ~150-180 active facts after consolidation
- Estimated API cost: ~$3.10

## Purpose
1. Public domain case study for README and HN launch
2. Tests pipeline on pre-curated biographical text (vs raw conversations)
3. Ground truth available — Franklin's documented decisions, values, behavioral patterns
4. Answers: does the pipeline add value over just reading the biography?
