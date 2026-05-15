# v11.9.6 — pipeline-variance numeric similarity probe

Per-rerun brief comparison across three probe subjects (Augustine, Sunity Devee, Yung Wing).
For each pair of reruns within a subject, sentences are classified as verbatim-identical or non-verbatim.
On non-verbatim sentences, best-match cosine similarity (MiniLM-L6-v2 sentence embeddings, normalized) is
reported against the other run's sentence pool. This puts a numeric figure on the §6.3 claim that the
non-verbatim share covers the same predicates and behavioral patterns with different surface phrasing.

## Pool summary (Augustine + Sunity Devee + Yung Wing combined)

- Non-verbatim sentence pairs evaluated: **1,304**
- Verbatim share across the three subjects (pairwise): **0.0%**
- Non-verbatim best-match cosine, mean: **0.551**
- Non-verbatim best-match cosine, median: **0.539**
- Non-verbatim best-match cosine, IQR: **[0.473, 0.612]**
- Share of non-verbatim sentences with best-match cosine ≥ 0.80: **3.1%**
- Share of non-verbatim sentences with best-match cosine ≥ 0.85: **2.3%**
- Share of non-verbatim sentences with best-match cosine ≥ 0.90: **1.7%**

## Per-subject pairwise detail

### augustine

Run sentence counts: [77, 81, 63]

- **Run 1 vs Run 2**: verbatim=0 sentences (share_i=0.0%, share_j=0.0%). Non-verbatim best-match cosine: mean=0.545, median=0.538, IQR=[0.475, 0.612]; ≥0.80=1.3%, ≥0.85=1.3%, ≥0.90=1.3%.
- **Run 1 vs Run 3**: verbatim=0 sentences (share_i=0.0%, share_j=0.0%). Non-verbatim best-match cosine: mean=0.553, median=0.540, IQR=[0.476, 0.605]; ≥0.80=4.3%, ≥0.85=4.3%, ≥0.90=2.9%.
- **Run 2 vs Run 3**: verbatim=0 sentences (share_i=0.0%, share_j=0.0%). Non-verbatim best-match cosine: mean=0.548, median=0.529, IQR=[0.473, 0.608]; ≥0.80=4.2%, ≥0.85=1.4%, ≥0.90=1.4%.

### sunity_devee

Run sentence counts: [66, 72, 78]

- **Run 1 vs Run 2**: verbatim=0 sentences (share_i=0.0%, share_j=0.0%). Non-verbatim best-match cosine: mean=0.554, median=0.553, IQR=[0.470, 0.632]; ≥0.80=2.9%, ≥0.85=2.9%, ≥0.90=1.4%.
- **Run 1 vs Run 3**: verbatim=0 sentences (share_i=0.0%, share_j=0.0%). Non-verbatim best-match cosine: mean=0.564, median=0.562, IQR=[0.475, 0.627]; ≥0.80=1.4%, ≥0.85=1.4%, ≥0.90=1.4%.
- **Run 2 vs Run 3**: verbatim=0 sentences (share_i=0.0%, share_j=0.0%). Non-verbatim best-match cosine: mean=0.573, median=0.576, IQR=[0.502, 0.632]; ≥0.80=2.7%, ≥0.85=1.3%, ≥0.90=1.3%.

### yung_wing

Run sentence counts: [74, 77, 64]

- **Run 1 vs Run 2**: verbatim=0 sentences (share_i=0.0%, share_j=0.0%). Non-verbatim best-match cosine: mean=0.549, median=0.532, IQR=[0.477, 0.606]; ≥0.80=5.3%, ≥0.85=5.3%, ≥0.90=2.6%.
- **Run 1 vs Run 3**: verbatim=0 sentences (share_i=0.0%, share_j=0.0%). Non-verbatim best-match cosine: mean=0.542, median=0.527, IQR=[0.458, 0.612]; ≥0.80=4.3%, ≥0.85=1.4%, ≥0.90=1.4%.
- **Run 2 vs Run 3**: verbatim=0 sentences (share_i=0.0%, share_j=0.0%). Non-verbatim best-match cosine: mean=0.532, median=0.516, IQR=[0.462, 0.557]; ≥0.80=1.4%, ≥0.85=1.4%, ≥0.90=1.4%.
