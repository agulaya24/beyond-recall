"""Apply Supermemory §4.4.1 updates from update block."""
from pathlib import Path

p = Path('C:/Users/Aarik/Anthropic/memory-study-repo/docs/beyond_recall_v9_draft.md')
text = p.read_text(encoding='utf-8')

fixes = [
    (
        '| Supermemory* | −0.07 | 3/10 | −0.03 | 3/7 |',
        '| Supermemory | −0.01 | 6/14 | −0.03 | 4/9 |',
    ),
    (
        'Wilcoxon: **Zep native p = 0.0015, Mem0 native p = 0.0088**, both robust. Letta native and Supermemory native are not significant.',
        'Wilcoxon: **Zep native p = 0.0015, Mem0 native p = 0.0088**, both robust. Letta native and Supermemory native are not significant (Supermemory native W = 48.0, p = 0.8077 on the paid-tier-complete n = 14 sample).',
    ),
    (
        '\\* Supermemory native has four ingestion failures on the free-tier API (Bernal Diaz, Babur, Cellini, Rousseau), so the native n drops to 10 full / 7 low-baseline. Base Layer has no separate "native" condition because Base Layer\'s authored pipeline is already the main-study ingestion for the controlled configuration; there is no separate native ingestion path to compare against.',
        'Supermemory native data: four subjects (Bernal Diaz, Babur, Cellini, Rousseau) initially encountered ingestion failures on the free-tier Supermemory API. A paid-tier rerun completed 2026-04-23 indexed all 199 chunks (0 failures) and retrieved 4.3-5.0 facts per question across these four subjects, with the 5-judge primary panel re-run on the resulting responses; the native Supermemory aggregate reported above reflects the paid-tier rerun, with all 14 main-study subjects (Hamerton + 13 globals) included. Base Layer has no separate "native" condition because Base Layer\'s authored pipeline is already the main-study ingestion for the controlled configuration; there is no separate native ingestion path to compare against.',
    ),
]

applied = 0
for old, new in fixes:
    if old in text:
        text = text.replace(old, new, 1)
        applied += 1
    else:
        print(f'NOT FOUND: {old[:100]!r}')

p.write_text(text, encoding='utf-8')
print(f'Applied: {applied}/3')
