# `data/source_corpora/` — Source Texts for the Beyond Recall Study

Generated 2026-05-05T21:43:49.637923+00:00 by `scripts/migrate_source_corpora.py`.

Every input the study pipeline consumed lives under this directory, with per-subject provenance and SHA-256 integrity hashes. All texts are Project Gutenberg public-domain editions.

## Subjects

| Subject | Role | Title | Author | Translator/Editor | PG eBook ID | Words | SHA-256 (first 12) |
|---|---|---|---|---|---:|---:|---|
| `augustine` | main_study | The Confessions of St. Augustine | Saint of Hippo Augustine | E. B. Pusey | #3296 | 114,873 | `20f5b0791e23` |
| `babur` | main_study | The Bābur-nāma in English (Memoirs of Bābur) | Emperor of Hindustan Babur | Annette Susannah Beveridge | #44608 | 422,769 | `47c48eec4168` |
| `bernal_diaz` | main_study | The Memoirs of the Conquistador Bernal Diaz del Castillo, Vol 1 (of 2) | Bernal Díaz del Castillo | John Ingram Lockhart | #32474 | 187,315 | `416854d7afd5` |
| `cellini` | main_study | The Autobiography of Benvenuto Cellini | Benvenuto Cellini | John Addington Symonds | #4028 | 190,389 | `f8ca08da8c99` |
| `ebers` | main_study | The Story of My Life — Complete | Georg Ebers | Mary J. Safford | #5599 | 96,174 | `f3a91b0405bb` |
| `equiano` | main_study | The Interesting Narrative of the Life of Olaudah Equiano, Or Gustavus Vassa, The African | Olaudah Equiano | — | #15399 | 85,660 | `70a1e2d4e33c` |
| `franklin_autobiography` | franklin_high_baseline_reference | Autobiography of Benjamin Franklin | Benjamin Franklin | Frank Woodworth Pine | #20203 | 79,259 | `a788e8434632` |
| `franklin_letters` | franklin_obscure_high_baseline | The Complete Works of Benjamin Franklin, Vol. 2 | Benjamin Franklin | — | #48137 | 151,371 | `0ca3cf2f48d1` |
| `fukuzawa` | main_study | The Autobiography of Fukuzawa Yukichi | Fukuzawa Yukichi (1835–1901) | Eiichi Kiyooka | — | 139,088 | `2b5cc85787df` |
| `hamerton` | main_study | Philip Gilbert Hamerton | Eugénie Hamerton, Philip Gilbert Hamerton | — | #8536 | 213,266 | `17e2a6c9c82e` |
| `keckley` | main_study | Behind the Scenes; or, Thirty years a slave, and Four Years in the White House | Elizabeth Keckley | — | #24968 | 61,831 | `609ce1264179` |
| `rousseau` | main_study | The Confessions of Jean Jacques Rousseau — Complete | Jean-Jacques Rousseau | — | #3913 | 278,120 | `3ab4d68f81e2` |
| `seacole` | main_study | Wonderful Adventures of Mrs. Seacole in Many Lands | Mary Seacole | W. J. S. | #23031 | 62,467 | `3f69bc831c77` |
| `sunity_devee` | main_study | The Autobiography of an Indian Princess | Maharani of Cooch Behar Sunity Devee | — | #57175 | 67,378 | `7935b6d8f3ac` |
| `yung_wing` | main_study | My Life in China and America | Wing Yung | — | #54635 | 66,459 | `5d67fdb3d1c1` |
| `zitkala_sa` | main_study | American Indian Stories | Zitkala-Sa | — | #10376 | 35,328 | `e802c1a2ed45` |

## Reproducibility

Re-run: `python scripts/migrate_source_corpora.py`. Existing files are not overwritten; delete `data/source_corpora/<subject>/` to refresh.

Each `provenance.md` records the bibliographic record, file integrity hash, and notes on how the pipeline consumes the corpus.

## Pipeline integration

The study pipeline (described in §3.7 of `docs/beyond_recall_v11_8_draft.md`) consumes each `raw.txt` through Steps 1-5: import → extract → embed → author → compose. Battery files (`data/<subject>/battery.json` for Hamerton, `results/<subject>/battery_v2.json` for globals) hold the 80-question evaluation batteries.

## License

Source texts are Project Gutenberg public-domain works. Inclusion here is for academic-archival reference. See each `provenance.md` for jurisdictional notes and the Project Gutenberg permission policy: https://www.gutenberg.org/policy/permission.html
