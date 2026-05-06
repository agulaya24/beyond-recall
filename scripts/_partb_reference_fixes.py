"""Apply the 32 definite reference fixes + TOC rewrite from the post-restructure audit.

Source: docs/reviews/s114_v9_reference_audit.md
Target: docs/beyond_recall_v9_draft.md

Also resolves the 2 ambiguous cases with sensible defaults:
  - L238 `§5.5` for hedging → `§4.3` (the Results-side Mechanism section where hedging numbers live)
  - L1473 §5.2 self-reference roadmap → rewrite using the clean-map form the audit proposed
"""

from pathlib import Path

PATH = Path('C:/Users/Aarik/Anthropic/memory-study-repo/docs/beyond_recall_v9_draft.md')


# (old_string, new_string, count_required) -- count=1 for uniqueness verification
FIXES = [
    # Row 1: L64
    ('Full methodology and results are in §4.4.1 and §4.7.',
     'Full methodology and results are in §4.5.', 1),

    # Row 2: L121 (§7 → §8 — follow-up context)
    ('flagged as follow-up in §7.', 'flagged as follow-up in §8.', 1),

    # Row 3: L176
    ('see §4.3 and §4.4.1 and §4.7', 'see §4.3 and §4.5', 1),

    # Row 4: L188 (§5.2 → §2.3.1 Twin-2K framing)
    ('prediction as its target, and the framing in this paper is different (§5.2).',
     'prediction as its target, and the framing in this paper is different (§2.3.1).', 1),

    # Row 5 + 6: L206, L208 (§4.8 → §5.5 temporality)
    ('one reason temporality is a flagged follow-up (§4.8, §8).',
     'one reason temporality is a flagged follow-up (§5.5, §8).', 1),
    ('sits alongside temporality (§4.8) as a follow-up in §8.',
     'sits alongside temporality (§5.5) as a follow-up in §8.', 1),

    # Row 7 (ambiguous 1): L238 — default to §4.3 Mechanism (Results-side)
    ('Our hedging-reduction finding (§1.3 Mechanism, §5.5)',
     'Our hedging-reduction finding (§1.3 Mechanism, §4.3)', 1),

    # Row 8: L400
    ('reported in §4.4.1 and §4.7 alongside other Letta findings',
     'reported in §4.5 alongside other Letta findings', 1),

    # Row 9: L412
    ('Tier 2 results and subject-selection rationale are in §3.4.1 and §4.8.',
     'Tier 2 results and subject-selection rationale are in §3.4.1 and §4.6.1.', 1),

    # Row 10: L506
    ('(robustness confirmed in §4.5).', '(robustness confirmed in §4.6).', 1),

    # Row 12: L598
    ('The 7-judge sensitivity check ... is reported in §4.5.',
     'The 7-judge sensitivity check ... is reported in §4.6.', 1),

    # Row 13: L1096
    ('described separately in §4.4.1 and §4.7.',
     'described separately in §4.5.', 1),

    # Row 15: L1295 — self-reference inside new §4.5
    ('§4.7 asks: if the Behavioral Specification improves prediction',
     '§4.5 asks: if the Behavioral Specification improves prediction', 1),

    # Row 16: L1353 — self-reference inside new §4.5
    ('The §4.7 matched-model gap may be attributable',
     'The §4.5 matched-model gap may be attributable', 1),

    # Row 17: L1374 — self-reference inside new §4.6
    ('§4.5 reports the sensitivity of the core findings to each.',
     '§4.6 reports the sensitivity of the core findings to each.', 1),

    # Row 18: L1467 — §4.6 old → §4.4.2 and §4.4.3
    ('per-question analysis (§4.4, §4.6) shows',
     'per-question analysis (§4.4.2, §4.4.3) shows', 1),

    # Row 19: L1471 — §4.7 → §4.5
    ('The target is reachable by more than one architectural path (§4.7).',
     'The target is reachable by more than one architectural path (§4.5).', 1),

    # Row 20 (ambiguous 2): L1473 — roadmap self-reference rewrite
    # We look for the specific sentence the audit flagged
    ('how AI memory systems should be evaluated (§5.2), '
     'how the specification composes with existing memory infrastructure (§5.3), '
     'whether the mechanism finding is a general AI-design primitive rather than a Base Layer-specific claim (§5.5)',
     'The remaining subsections of §5 develop what these results imply for real users outside the sample (§5.3), '
     'for the mechanism of interpretation (§5.4), for practical deployment (§5.5), '
     'for measurement gaps (§5.6), and for behavioral-versus-safety alignment (§5.7)', 0),  # 0 = may not match exactly; we'll do a softer match below

    # Row 21: L1502
    ('§4.6 Yung Wing Q31', '§4.4.2 Yung Wing Q31', 1),

    # Row 22: L1505
    ('The dynamic-activation proposal in §4.8',
     'The dynamic-activation proposal in §5.5', 1),

    # Row 23: L1515 — piecewise component analysis
    ('piecewise component analysis flagged in §4.8',
     'piecewise component analysis flagged in §5.5', 0),  # may not exist exactly

    # Row 24: L1521 — self-reference inside new §5.5 opening
    ('§4.1 through §4.7 establish what the Behavioral Specification does and why it works. §4.8 is a practical note',
     '§4.1 through §4.6 establish what the Behavioral Specification does and why it works. §5.5 is a practical note', 1),

    # Row 27: L1620
    ('what §5.1 summarizes', 'what §5.2 summarizes', 1),

    # Row 29: L1636
    ('The Letta stateful comparison in §4.7 served Base Layer\'s unified',
     'The Letta stateful comparison in §4.5 served Base Layer\'s unified', 1),

    # Row 30: L1686
    ('The serving-strategy gap ... is in §4.8 and §5.6.',
     'The serving-strategy gap ... is in §5.5 and §5.6.', 0),  # may be phrased differently; try soft

    # Row 32: L1702
    ('§4.4, §4.7` (Letta stateful-agent exploration)',
     '§4.4, §4.5` (Letta stateful-agent exploration)', 0),

    # Row 33: L1722
    ('priority authoring-pipeline follow-up (§4.8, §5.4, §5.6).',
     'priority authoring-pipeline follow-up (§5.5, §5.4, §5.6).', 1),

    # Row 34: L1724 (two fixes)
    ('a Base Layer referent-variant that retains named entities inside the same dimensional scaffold, to isolate whether the §4.7 Letta-over-Base-Layer gap is driven by referential vocabulary or by the self-editing process itself (§4.7, §5.5)',
     'a Base Layer referent-variant that retains named entities inside the same dimensional scaffold, to isolate whether the §4.5 Letta-over-Base-Layer gap is driven by referential vocabulary or by the self-editing process itself (§4.5, §5.5)', 0),
    ('a layered-stack Letta rerun on the matched-rerun subjects, which would likely narrow the §4.7 gap (§4.7, §5.6).',
     'a layered-stack Letta rerun on the matched-rerun subjects, which would likely narrow the §4.5 gap (§4.5, §5.6).', 0),

    # Row 35: L1728
    ('Five production-realistic serving-layer follow-ups follow directly from §4.8:',
     'Five production-realistic serving-layer follow-ups follow directly from §5.5:', 1),

    # Row 36: L1732 — canonical life events §5.2 → §2.3.1
    ('canonical life events (automatic detection or user-supplied annotation of within-person behavioral shifts, §5.2)',
     'canonical life events (automatic detection or user-supplied annotation of within-person behavioral shifts, §2.3.1)', 0),

    # Row 37: L1736
    ('The §4.7 Letta stateful-agent comparison is N=3 subjects',
     'The §4.5 Letta stateful-agent comparison is N=3 subjects', 0),

    # Row 38: L1737
    ('The open question §7 raises', 'The open question §5.7 raises', 0),
]


# TOC block rewrite (row 11): lines 589-596
TOC_OLD = """**§4.1. The Cross-Subject Gradient.**"""  # use as anchor to find the block

# Actually let's make this more targeted — replace whole block
TOC_OLD_BLOCK = """**§4.1. The Cross-Subject Gradient.** The less the model already knows about a person from pretraining, the more the specification helps. The headline empirical finding, tested across 14 subjects.

**§4.2. Compression: Structure vs. Raw Text.** A 7,000-token specification recovers most of what the full source corpus delivers at ~5% of the context.

**§4.3. Mechanism: Content, Not Format.** The effect is driven by the specific content of the correct specification. Wrong specifications score at or below baseline; mere structured prompting does not reproduce the effect.

**§4.4. Memory-System Composition.** The specification layers additively on three of four commercial memory systems. The fourth (Supermemory) aggregates near zero at the subject level but produces large per-question swings in both directions.

**§4.5. Robustness and Sensitivity.** Does the effect hold across response models, judges, and replication conditions?

**§4.6. Interpretation vs. Recall.** Where does the specification help and where does it hurt at the per-question level? Consequences for how behavioral-prediction benchmarks should be scored going forward.

**§4.7. Architectural Convergence.** Letta's stateful-agent path independently arrives at a similar solution, documented with its scaling behavior at large corpus sizes.

**§4.8. Scaling and Practical Implications.** Cost, context-budget, modifiability, and deployment considerations."""

TOC_NEW_BLOCK = """**§4.1. The Cross-Subject Gradient.** The less the model already knows about a person from pretraining, the more the specification helps. The headline empirical finding, tested across 14 subjects.

**§4.2. Compression: Structure vs. Raw Text.** A 7,000-token specification recovers most of what the full source corpus delivers at ~5% of the context.

**§4.3. Mechanism: Content, Not Format.** The effect is driven by the specific content of the correct specification. Wrong specifications score at or below baseline; mere structured prompting does not reproduce the effect.

**§4.4. Memory-System Composition.** The specification layers additively on three of four commercial memory systems. Aggregate per-system performance (§4.4.1), common mechanisms observed across systems (§4.4.2), and a cross-system case study on Keckley Q21 (§4.4.3) develop this axis.

**§4.5. Architectural Convergence.** Letta's stateful-agent path independently arrives at a similar solution, documented with its scaling behavior at large corpus sizes.

**§4.6. Robustness and Sensitivity.** Does the effect hold across response models, judges, and replication conditions?"""


def main():
    text = PATH.read_text(encoding='utf-8')
    applied = 0
    skipped = []

    for i, (old, new, required_count) in enumerate(FIXES, 1):
        count = text.count(old)
        if count == 0:
            skipped.append((i, old[:80], 'not found'))
            continue
        if required_count == 1 and count > 1:
            skipped.append((i, old[:80], f'matched {count} times, expected 1'))
            continue
        text = text.replace(old, new, 1)  # replace only first match
        applied += 1

    # TOC block rewrite
    toc_count = text.count(TOC_OLD_BLOCK)
    if toc_count == 1:
        text = text.replace(TOC_OLD_BLOCK, TOC_NEW_BLOCK, 1)
        toc_applied = True
    else:
        toc_applied = False
        skipped.append(('TOC', 'TOC block', f'matched {toc_count} times; soft replace below'))

        # Fall back: replace individual TOC lines one at a time
        toc_fixes = [
            ('**§4.5. Robustness and Sensitivity.** Does the effect hold across response models, judges, and replication conditions?',
             '**§4.5. Architectural Convergence.** Letta\'s stateful-agent path independently arrives at a similar solution, documented with its scaling behavior at large corpus sizes.'),
            ('**§4.6. Interpretation vs. Recall.** Where does the specification help and where does it hurt at the per-question level? Consequences for how behavioral-prediction benchmarks should be scored going forward.',
             '**§4.6. Robustness and Sensitivity.** Does the effect hold across response models, judges, and replication conditions?'),
        ]
        for old, new in toc_fixes:
            if text.count(old) == 1:
                text = text.replace(old, new, 1)
                applied += 1

        # Delete the old §4.7 and §4.8 TOC bullets that are now redundant
        drop47 = '**§4.7. Architectural Convergence.** Letta\'s stateful-agent path independently arrives at a similar solution, documented with its scaling behavior at large corpus sizes.\n\n'
        drop48 = '**§4.8. Scaling and Practical Implications.** Cost, context-budget, modifiability, and deployment considerations.\n\n'
        if drop47 in text:
            text = text.replace(drop47, '', 1)
            applied += 1
        if drop48 in text:
            text = text.replace(drop48, '', 1)
            applied += 1

    PATH.write_text(text, encoding='utf-8')

    print(f'Applied: {applied} fixes')
    print(f'Skipped: {len(skipped)} fixes')
    for s in skipped:
        print(f'  skipped #{s[0]}: {s[1]!r} -- {s[2]}')


if __name__ == '__main__':
    main()
