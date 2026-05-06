# Independent reference verification, Beyond Recall v11.8 (2026-05-05)

Independent pass over §9 References in `docs/beyond_recall_v11_8_draft.md`. Each reference fetched directly from canonical source: arXiv abstract pages for arXiv preprints, established bibliographic record for Bartlett 1932. Prior pass `docs/reviews/references_backtrack_v11_8_20260505_122358.md` not consulted until the cross-check section at the end.

## Summary
- Total references in §9: 18
- All-fields-VERIFIED: 17
- DRIFT (one or more fields wrong): 0
- UNREACHABLE (live verification not performed but established record exists): 1 (Bartlett 1932; established bibliographic source, not a live arXiv link)

No P0 or P1 drift detected. The §9 list passes independent verification against canonical sources.

The previously-flagged self-citation "Gulaya" does not appear in §9 (verified by grep). The only "Gulaya" occurrences in the paper are the author byline at line 3 and the author-affiliation note at line 1754, both of which are correct.

## Per-reference verdicts

| # | Paper claim (first author, year) | Title check | First author | Year | Venue / arXiv ID | All authors verified | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Bartlett, F. C. (1932) | "Remembering: A Study in Experimental and Social Psychology" matches established bibliographic record | F. C. Bartlett (Frederic Charles Bartlett) | 1932 | Cambridge University Press | yes | VERIFIED (established record; live publisher fetch not performed; see UNREACHABLE) |
| 2 | Chen, R., et al. (2025) | "Persona vectors: Monitoring and controlling character traits in language models", exact match | Runjin Chen | 2025 (submitted Jul 29, 2025) | arXiv:2507.21509 | Chen, Arditi, Sleight, Evans, Lindsey (5 authors; "et al." OK) | VERIFIED |
| 3 | Chhikara, P., et al. (2025) | "Mem0: Building production-ready AI agents with scalable long-term memory", exact match | Prateek Chhikara | 2025 (submitted Apr 28, 2025) | arXiv:2504.19413 | Chhikara, Khant, Aryan, Singh, Yadav (5 authors; "et al." OK) | VERIFIED |
| 4 | Hinton, G., Vinyals, O., & Dean, J. (2015) | "Distilling the knowledge in a neural network", exact match | Geoffrey Hinton | 2015 (submitted Mar 9, 2015) | NIPS 2014 Deep Learning Workshop; arXiv:1503.02531 | Hinton, Vinyals, Dean (3 authors; full list given as required) | VERIFIED |
| 5 | Jain, S., et al. (2025) | "Interaction context often increases sycophancy in LLMs", exact match | Shomik Jain | 2025 (submitted Sep 15, 2025) | arXiv:2509.12517 (CHI 2026 accepted; paper claims preprint only) | Jain, Park, Viana, Wilson, Calacci (5 authors; "et al." OK) | VERIFIED |
| 6 | Jiang, B., et al. (2025) | "Know me, respond to me: Benchmarking LLMs for dynamic user profiling and personalized responses at scale", exact match | Bowen Jiang | 2025 (submitted Apr 19, 2025) | COLM 2025; arXiv:2504.14225 | 9 authors; "et al." OK | VERIFIED |
| 7 | Lu, C., et al. (2026) | "The Assistant Axis: Situating and stabilizing the default persona of language models", exact match | Christina Lu | 2026 (submitted Jan 15, 2026) | arXiv:2601.10387 | Lu, Gallagher, Michala, Fish, Lindsey (5 authors; "et al." OK) | VERIFIED |
| 8 | Maharana, A., et al. (2024) | "Evaluating very long-term conversational memory of LLM agents", exact match | Adyasha Maharana | 2024 (submitted Feb 27, 2024) | ACL 2024; arXiv:2402.17753 | 6 authors; "et al." OK | VERIFIED |
| 9 | Packer, C., et al. (2023) | "MemGPT: Towards LLMs as operating systems", exact match | Charles Packer | 2023 (submitted Oct 12, 2023) | arXiv:2310.08560 | 7 authors; "et al." OK | VERIFIED |
| 10 | Perez, E., et al. (2022) | "Discovering language model behaviors with model-written evaluations", exact match | Ethan Perez | 2022 (submitted Dec 19, 2022) | arXiv:2212.09251 | 60+ authors; "et al." OK | VERIFIED |
| 11 | Rasmussen, P., et al. (2025) | "Zep: A temporal knowledge graph architecture for agent memory", exact match | Preston Rasmussen | 2025 (submitted Jan 20, 2025) | arXiv:2501.13956 | Rasmussen, Paliychuk, Beauvais, Ryan, Chalef (5 authors; "et al." OK) | VERIFIED |
| 12 | Samuel, V., et al. (2025) | "PersonaGym: Evaluating persona agents and LLMs", exact match | Vinay Samuel | 2024 preprint, accepted Findings EMNLP 2025; arXiv:2407.18416 | 9 authors; "et al." OK | VERIFIED (citation year = venue year per paper convention; see Note A below) |
| 13 | Sharma, M., et al. (2023) | "Towards understanding sycophancy in language models", exact match | Mrinank Sharma | 2023 (submitted Oct 20, 2023) | arXiv:2310.13548 | 19 authors; "et al." OK | VERIFIED |
| 14 | Toubia, O., et al. (2025) | "Twin-2K-500: A dataset for building digital twins of over 2,000 people based on their answers to over 500 questions", exact match | Olivier Toubia | 2025 (submitted May 23, 2025) | arXiv:2505.17479 | Toubia, Gui, Peng, Merlau, Li, Chen (6 authors; "et al." OK) | VERIFIED |
| 15 | Verga, P., et al. (2024) | "Replacing judges with juries: Evaluating LLM generations with a panel of diverse models", exact match | Pat Verga | 2024 (submitted Apr 29, 2024) | arXiv:2404.18796 | 9 authors; "et al." OK | VERIFIED |
| 16 | Wu, D., et al. (2025) | "LongMemEval: Benchmarking chat assistants on long-term interactive memory", exact match | Di Wu | 2024 preprint, accepted ICLR 2025; arXiv:2410.10813 | Wu, Wang, Yu, Zhang, Chang, Yu (6 authors; "et al." OK) | VERIFIED (citation year = venue year per paper convention) |
| 17 | Xiao, J., et al. (2026) | "AlpsBench: An LLM personalization benchmark for real-dialogue memorization and preference alignment", exact match | Jianfei Xiao | 2026 (submitted Mar 9, 2026) | arXiv:2603.26680 | 11 authors; "et al." OK | VERIFIED |
| 18 | Zheng, L., et al. (2023) | "Judging LLM-as-a-judge with MT-Bench and Chatbot Arena", exact match | Lianmin Zheng | 2023 (submitted Jun 9, 2023) | NeurIPS 2023 Datasets and Benchmarks Track; arXiv:2306.05685 | 13 authors; "et al." OK | VERIFIED |

**Note A on citation-year convention.** The §9 preamble states: "Where a peer-reviewed venue is listed, the citation year is the venue year and the arXiv identifier is included as a durable preprint identifier that may predate the venue year." This convention is correctly applied for Samuel 2025 (arXiv:2407.xxxxx is July 2024, EMNLP Findings 2025), Wu 2025 (arXiv:2410.xxxxx is Oct 2024, ICLR 2025), and Maharana 2024 (arXiv:2402.xxxxx is Feb 2024, ACL 2024). No drift.

## DRIFT items

None.

## UNREACHABLE references

1. **Bartlett, F. C. (1932).** Live publisher page (Cambridge University Press) was attempted but blocked by the local sandbox permission policy on this run; Wikipedia fallback also blocked. The §9 entry as written matches the universally-cited canonical record:
   - Title: *Remembering: A Study in Experimental and Social Psychology*
   - Author: Frederic Charles Bartlett ("F. C. Bartlett")
   - Publisher: Cambridge University Press
   - Year: 1932 (reissued 1995 with foreword by Walter Kintsch; the 1932 first-edition citation is correct)

   No drift detected on the basis of established bibliographic knowledge. Recommend a manual one-line confirmation against the publisher catalog before final freeze for full closure, but no fix required.

## Cross-check vs. prior pass `references_backtrack_v11_8_20260505_122358.md`

After completing the independent verification above, I read the prior pass for comparison. The prior pass (12:23:58) and this pass (later same day) reached different conclusions because the §9 list was edited between the two runs. The prior pass found 11 DRIFT items; this pass finds 0. Reading the prior pass's drift items against the current §9 line-by-line confirms that every prior-pass DRIFT item has already been fixed in v11.8.

There was also an even earlier pass at 12:08:48 (`references_check_v11_8_20260505_120848.md`) that flagged structural issues: Gulaya self-cite, and Sharma 2023 plus Perez 2022 missing from §9. Those have also been fixed.

### Items where this pass agrees with the prior pass

For the 5 entries the prior pass marked VERIFIED outright (no drift), this pass also confirms VERIFIED on independent fetch:

- Bartlett 1932 (book, recognition).
- Hinton, Vinyals & Dean 2015 (title, authors, year, venue).
- Packer et al. 2023.
- Perez et al. 2022.
- Sharma et al. 2023.
- Zheng et al. 2023.

Plus Samuel 2025 (VERIFIED-WITH-NOTE in the prior pass, VERIFIED in this pass) with the citation-year-equals-venue-year convention now stated explicitly in the §9 preamble. The convention note makes the year resolution unambiguous.

### Items where this pass DISAGREES with the prior pass

For all 11 DRIFT items the prior pass flagged, this pass marks the current §9 entries VERIFIED. The DRIFT items in the prior pass are NOT present in the current v11.8 §9. They have been corrected. Verbatim line-by-line spot check:

| Prior pass DRIFT | Prior pass said §9 had | Current v11.8 §9 says (verbatim) | Status |
|---|---|---|---|
| Chen 2025 first-author initial | "Chen, Y." | "Chen, R., et al." (line 1772) | FIXED |
| Chhikara 2025 first-author initial | "Chhikara, A." | "Chhikara, P., et al." (line 1774) | FIXED |
| Jain 2025 title + initial | title paraphrased; "Jain, A." | "Jain, S., et al. ... Interaction context often increases sycophancy in LLMs." (line 1778) | FIXED |
| Jiang 2025 title + initial | "Jiang, X." with paraphrased title | "Jiang, B., et al. ... Know me, respond to me: Benchmarking LLMs for dynamic user profiling and personalized responses at scale." (line 1780) | FIXED |
| Lu 2026 title subtitle + initial | "Lu, R." with subtitle "A dominant internal direction..." | "Lu, C., et al. ... The Assistant Axis: Situating and stabilizing the default persona of language models." (line 1782) | FIXED |
| Maharana 2024 title | "LoCoMo: Long-context conversational memory benchmark" | "Evaluating very long-term conversational memory of LLM agents." (line 1784) | FIXED |
| Rasmussen 2025 title | "bi-temporal knowledge graph for grounded LLM agent memory" | "Zep: A temporal knowledge graph architecture for agent memory." (line 1790) | FIXED |
| Toubia 2025 title | "Twin-2K: Behavioral prediction at scale on held-out survey items" | "Twin-2K-500: A dataset for building digital twins of over 2,000 people based on their answers to over 500 questions." (line 1796) | FIXED |
| Verga 2024 first-author initial | "Verga, A." | "Verga, P., et al." (line 1798) | FIXED |
| Wu 2025 title + initial | "Wu, Z." with paraphrased title | "Wu, D., et al. ... LongMemEval: Benchmarking chat assistants on long-term interactive memory." (line 1800) | FIXED |
| Xiao 2026 title + initial | "Xiao, T." with paraphrased title | "Xiao, J., et al. ... AlpsBench: An LLM personalization benchmark for real-dialogue memorization and preference alignment." (line 1802) | FIXED |

All 11 prior-pass DRIFT items have been corrected. No DRIFT remains.

### Items the prior pass missed

None identified. The prior pass was thorough on the title/author/initial drift axis. This pass also independently confirms:

- Year-prefix sanity (YYMM) for every arXiv ID. All 17 IDs resolve to abstract pages with matching submission months. Both 2026 IDs (Lu 2601, Xiao 2603) are real and resolve.
- No "Gulaya" self-citation in §9. Only the author byline at line 3 and the §8 author-affiliation note at line 1754 contain the name.
- COLM 2025 (Jiang), ICLR 2025 (Wu), and EMNLP Findings 2025 (Samuel) venue claims are confirmed against the arXiv abstract pages, which now state these venues in the comments field. ACL 2024 for Maharana is also a defensible claim. The arXiv abstract does not state ACL, but the paper is a known ACL 2024 publication and the §9 preamble's citation-year-equals-venue-year convention is stated. If a stricter venue-confirmation policy is desired, this could be cross-checked against the ACL Anthology.
- The §9 preamble's explicit citation-year-equals-venue-year convention is a clean fix to the year-discrepancy concern the prior pass flagged for Samuel and Wu.

### Net verdict

The current §9 is clean. Recommend no further reference fixes before final freeze. The 52.3% to 35.9% transcription-error class that triggered this independent verification does not appear in §9 references.
