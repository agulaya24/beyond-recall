# Main BaseLayer Repo -- Updates Needed for Paper Launch

## Current State
README.md is a product-focused document. No mention of the "Beyond Recall" study, the 14-subject validation, or the study repo. Research page link goes to base-layer.ai/research which has older findings.

## Required Changes

### 1. Add Study Section to README
After "Why It Works" section, add a new section:

```markdown
## Research: "Beyond Recall" (April 2026)

We tested the behavioral specification against 4 SOTA memory systems (Mem0, Letta, Supermemory, Zep), 
6 response models, and 7 calibrated judges across 14 subjects from 11 cultures.

**Key findings:**
- The specification improves prediction accuracy for subjects with low pretraining representation (+13% to +168%)
- A 5K-token spec outperforms 33K tokens of raw autobiography
- Adding the spec to every memory system improves it (Letta +45%, Mem0 +22%, Supermemory +12%, Zep +66%)
- A wrong specification is indistinguishable from no specification (content drives improvement, not format)

**Paper:** [Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization](link)
**Study data + code:** [github.com/agulaya24/memory-study-repo](https://github.com/agulaya24/memory-study-repo)
```

### 2. Update Subject Count
- Current: "57+ subjects tested"
- Update to: "60+ subjects modeled" (reflects current count)

### 3. Update "Why It Works" with Study Data
Current bullets are from earlier sessions (S79-era). Update with paper findings:
- Replace "20% of facts is enough" with study-backed compression finding
- Add: "The specification provides for private individuals what pretraining provides for public figures"

### 4. Add Disclosure
Add to README footer or a DISCLOSURE.md:
```
The author of the associated research paper is the founder of this project. 
All study data, code, and evaluation artifacts are released under Apache 2.0.
```

### 5. Update Research Page Link
Current research link goes to base-layer.ai/research. Ensure the website research page references the paper once it's live.

### 6. Add Study Scripts
The main repo has the pipeline code but not the study-specific scripts (battery generation, condition runner, judging, analysis). These live in the study repo. Add a pointer:
```
## Reproducing the Study
See [memory-study-repo](https://github.com/agulaya24/memory-study-repo) for all study data, 
question batteries, judge scores, and reproduction scripts.
```

### 7. Check for Stale Claims
- "57+ subjects" badge -- update count
- "From 101 sessions of experimentation" -- now 110+ sessions
- Pipeline description should match the paper's description exactly
- Any performance claims should be traceable to either the paper or the study repo

### 8. License
- Main repo: Apache 2.0 (already has LICENSE)
- Study repo: needs Apache 2.0 LICENSE file added before going public

## NOT Needed
- Don't merge study repo into main repo -- they serve different purposes
- Don't add raw study data to main repo -- keep it in study repo
- Don't change the CLI/pipeline code -- it's already correct
