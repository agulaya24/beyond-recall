"""Part B restructure on v9 — one-shot execution.

Four moves:
  1. §4.8 Scaling → §5.5 Practical Implications (delete from §4, replace old §5.5 Arch convergence)
  2. §5 rebuild: delete §5.2 (moves to §2.3.1), add new §5.1 Anti-Pattern, rename old §5.1 → §5.2
  3. §7 Behavioral alignment → §5.7
  4. Move §5.2 content to new §2.3.1 subsection
"""

from pathlib import Path

PATH = Path('C:/Users/Aarik/Anthropic/memory-study-repo/docs/beyond_recall_v9_draft.md')

# New §5.1 Anti-Pattern content
NEW_51 = """### 5.1 The Anti-Pattern: What Behavioral Specification Is Not

Before summarizing what this study demonstrates, this discussion first defines the anti-pattern: what the Behavioral Specification is explicitly not trying to be. Naming the anti-pattern clarifies the scope of every positive claim that follows and marks the boundaries the paper does not overstep.

**It is not memory recall.** Memory-recall benchmarks (LOCOMO, LongMemEval, discussed in §2.3) measure whether a system can retrieve a specific fact it previously ingested. A system that scores 95% on recall can still score at the rubric floor on representational accuracy: the ability to anticipate a person's reasoning in a situation no stored fact covers. §4.1 and §4.4 separate these two axes empirically.

**It is not persona fidelity.** Persona benchmarks (PersonaGym, §2.3) measure whether a model maintains a described character consistently during conversation. A system that maintains persona perfectly can still be representationally inaccurate: the persona itself can be a surface portrayal that does not carry the interpretive patterns the person actually reasons with. Representational accuracy is measured against a specific person's held-out behavior, not against self-consistency of portrayal.

**It is not preference alignment.** Preference-tuning benchmarks (AlpsBench, §2.3) measure whether a system produces responses a user rates higher on preference or emotional-resonance scales. Preference alignment optimizes what the user likes receiving; representational accuracy measures how well the system anticipates what the user would do next. The Behavioral Specification targets the second and is ambivalent about the first.

**It is not survey-response prediction.** Twin-2K (§2.3) predicts a participant's next answer on a structured survey from their other answers on the same survey. The task shape constrains both the representation (survey history) and the target (Likert-scale response interpolation). Representational accuracy is a broader test: predicting open-ended behavior in situations the representation has not seen, drawn from a different modality than the source material.

**It is not a psychometric profile.** Psychometric profiles compress a person to scores on a fixed dimension set (Big Five, MBTI, Enneagram). Those dimensions are legible and portable but lossy by construction: the axes are chosen in advance by the test designer, not derived from the subject's own reasoning patterns. The Behavioral Specification's anchors are surfaced from the subject's corpus rather than projected onto a fixed axis set.

The positive target is narrower than any of the above. We want a representation that lets a response model act as this specific person would, on situations the model has never seen, grounded in the person's documented reasoning patterns rather than in surface-level similarity, psychometric dimensions, or preference signals. What follows (§5.2 through §5.7) develops what the study shows about this target and where it falls short.

---

"""


def main():
    text = PATH.read_text(encoding='utf-8')

    # ----- Locate key anchors -----
    s48_heading = '### 4.8 Scaling and Practical Implications'
    s55_arch_heading = '### 5.5 Architectural convergence'
    s56_heading = '### 5.6 What the study does not settle'
    s52_heading = "### 5.2 Recall, prediction, persona: what we measure and what it isn't"
    s53_heading = '### 5.3 The population of relevance'
    s7_heading = '## 7. Behavioral alignment and safety alignment'
    discussion_heading = '## 5. Discussion'
    appendix_a_heading = '## Appendix A.'

    assert text.count(s48_heading) == 1, 'missing §4.8'
    assert text.count(s55_arch_heading) == 1, 'missing §5.5 Arch convergence'
    assert text.count(s56_heading) == 1, 'missing §5.6 heading'
    assert text.count(s52_heading) == 1, 'missing §5.2 heading'
    assert text.count(s7_heading) == 1, 'missing §7 heading'

    # ----- Extract §4.8 body (to move to §5.5) -----
    s48_idx = text.find(s48_heading)
    s5_idx = text.find(discussion_heading, s48_idx)
    s48_block_full = text[s48_idx:s5_idx]
    s48_body = s48_block_full.replace(s48_heading + '\n\n', '', 1).rstrip()
    if s48_body.endswith('---'):
        s48_body = s48_body[:-3].rstrip()

    # ----- Extract §5.2 body (to move to new §2.3.1) -----
    s52_idx = text.find(s52_heading)
    s53_idx = text.find(s53_heading, s52_idx)
    s52_block_full = text[s52_idx:s53_idx]
    s52_body = s52_block_full.replace(s52_heading + '\n\n', '', 1).rstrip()
    if s52_body.endswith('---'):
        s52_body = s52_body[:-3].rstrip()

    # Build the §2.3.1 insertion block
    s231_block = (
        '### 2.3.1 What Existing Benchmarks Measure vs What Representational Accuracy Tests\n\n'
        + s52_body
        + '\n\n---\n\n'
    )

    # ----- Locate §2.4 (end of §2.3) -----
    s23_idx = text.find('### 2.3 Memory and personalization benchmarks')
    if s23_idx == -1:
        raise RuntimeError('cannot find §2.3 heading')
    s24_idx = text.find('### 2.4', s23_idx)
    if s24_idx == -1:
        s24_idx = text.find('## 3.', s23_idx)
    assert s24_idx > s23_idx

    # ----- Phase 1: insert §2.3.1 content into §2 -----
    text = text[:s24_idx] + s231_block + text[s24_idx:]

    # ----- Phase 2: delete §4.8 block from §4 -----
    s48_idx = text.find(s48_heading)
    s5_idx = text.find(discussion_heading, s48_idx)
    text = text[:s48_idx] + text[s5_idx:]

    # ----- Phase 3: delete §5.2 (moved content already inserted into §2.3.1) -----
    s52_idx = text.find(s52_heading)
    s53_idx = text.find(s53_heading, s52_idx)
    text = text[:s52_idx] + text[s53_idx:]

    # ----- Phase 4: replace old §5.5 Arch convergence with new §5.5 Practical Implications -----
    s55_idx = text.find(s55_arch_heading)
    s56_idx = text.find(s56_heading, s55_idx)
    new_s55 = (
        '### 5.5 Practical Implications\n\n'
        + s48_body.rstrip()
        + '\n\n---\n\n'
    )
    text = text[:s55_idx] + new_s55 + text[s56_idx:]

    # ----- Phase 5: fold §7 into §5 as §5.7 -----
    s7_idx = text.find(s7_heading)
    appendix_idx = text.find(appendix_a_heading, s7_idx)
    assert appendix_idx > s7_idx
    s7_block = text[s7_idx:appendix_idx]
    s7_as_sub = s7_block.replace(
        s7_heading,
        '### 5.7 Behavioral Alignment and Safety Alignment',
        1,
    )

    # Delete old §7 block from its position; insert before appendix
    text = text[:s7_idx] + text[appendix_idx:]
    appendix_idx = text.find(appendix_a_heading)
    text = text[:appendix_idx] + s7_as_sub.rstrip() + '\n\n---\n\n' + text[appendix_idx:]

    # ----- Phase 6: rename old §5.1 → §5.2; insert new §5.1 Anti-Pattern at top of §5 -----
    text = text.replace(
        '### 5.1 What the study demonstrates',
        '### 5.2 What the study demonstrates',
        1,
    )

    # Insert new §5.1 just after "## 5. Discussion\n\n"
    disc_idx = text.find(discussion_heading)
    after_disc = disc_idx + len(discussion_heading)
    while text[after_disc] == '\n':
        after_disc += 1
    text = text[:after_disc] + NEW_51 + text[after_disc:]

    # ----- Sanity checks -----
    assert '### 5.1 The Anti-Pattern' in text
    assert '### 5.2 What the study demonstrates' in text
    assert '### 5.5 Practical Implications' in text
    assert '### 5.7 Behavioral Alignment and Safety Alignment' in text
    assert s7_heading not in text
    assert s48_heading not in text
    assert s55_arch_heading not in text
    assert '### 5.2 Recall, prediction, persona' not in text
    assert '### 2.3.1 What Existing Benchmarks Measure' in text

    PATH.write_text(text, encoding='utf-8')

    import re
    headings = [m.group(0) for m in re.finditer(r'^(##|###) \d.*$', text, re.MULTILINE)]
    print('Final structure:')
    for h in headings:
        print(f'  {h}')


if __name__ == '__main__':
    main()
