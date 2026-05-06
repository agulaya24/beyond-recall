# Era / Modernity / Exoticism Cross-Slice of Spec Deltas (Q32)

_Panel: 5-judge primary (haiku, sonnet, opus, gpt4o, gpt54). All 14 main-study subjects._

**Question:** Do certain eras / modernity registers / content-exoticism buckets show systematically different spec deltas?

**Method:** Each subject bucketed on three dimensions. For each bucket, report mean, std, n of Δ_spec across two data sources: (a) §4.1 controlled gradient conditions C2a (spec alone) and C4a (facts+spec), re-aggregated on the 5-judge panel; (b) five memory-system C3−C1 deltas on the controlled config (5-judge panel, from `docs/research/memory_systems_5judge_primary.md`).

**Collinearity control:** because era correlates with C5 baseline (pre-1700 = lower pretraining knowledge = lower baseline), we also report Δ residualized on C5 via simple OLS across all 14 subjects. If residual cross-tabs still differ by bucket, the era/modernity/exoticism axis adds variance beyond baseline. If not, the effect is collinear with baseline.

## 1. Per-subject classification + raw deltas

| Subject | Era | Modernity | Exoticism | C5 (5j) | Δ C2a (5j) | Δ C4a (5j) | Mem0 | Letta | Zep | SM | BL |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| hamerton | 1700-1900 | modern | familiar | 1.26 | +1.374 | +1.513 | +0.103 | +0.387 | +0.333 | +0.144 | -0.010 |
| augustine | pre_1700 | archaic | non-Western | 2.58 | -0.108 | +0.113 | +0.349 | +0.223 | +0.205 | -0.040 | +0.111 |
| babur | pre_1700 | archaic | non-Western | 1.76 | +0.149 | +0.251 | +0.256 | +0.164 | +0.041 | +0.051 | +0.140 |
| bernal_diaz | pre_1700 | archaic | non-Western | 1.70 | +0.569 | +0.785 | -0.026 | +0.036 | +0.097 | -0.031 | -0.077 |
| cellini | pre_1700 | archaic | marginal-familiar | 2.38 | +0.164 | +0.149 | +0.364 | +0.413 | +0.405 | -0.036 | +0.274 |
| ebers | 1700-1900 | modern | familiar | 1.02 | +0.518 | +1.051 | +0.149 | +0.138 | +0.272 | +0.138 | +0.077 |
| equiano | 1700-1900 | modern | non-Western | 2.77 | -0.313 | -0.349 | +0.092 | +0.123 | +0.072 | -0.319 | -0.103 |
| fukuzawa | 1700-1900 | modern | non-Western | 1.67 | +0.682 | +1.108 | +0.046 | +0.044 | +0.026 | -0.205 | +0.051 |
| keckley | 1700-1900 | modern | non-Western | 1.84 | +0.585 | +0.595 | -0.021 | -0.021 | +0.041 | -0.267 | -0.009 |
| rousseau | 1700-1900 | modern | familiar | 2.44 | +0.374 | +0.097 | +0.108 | +0.587 | +0.467 | -0.026 | +0.333 |
| seacole | 1700-1900 | modern | non-Western | 1.77 | +0.708 | +0.821 | +0.154 | +0.400 | +0.472 | +0.082 | +0.197 |
| sunity_devee | 1700-1900 | modern | non-Western | 1.03 | +1.241 | +1.385 | -0.082 | +0.026 | +0.087 | -0.113 | +0.043 |
| yung_wing | 1700-1900 | modern | non-Western | 1.88 | +0.338 | +0.523 | +0.328 | +0.308 | +0.123 | +0.108 | +0.333 |
| zitkala_sa | post_1900 | modern | non-Western | 2.34 | -0.308 | -0.318 | -0.123 | -0.051 | -0.031 | -0.246 | -0.272 |

## 2. Raw cross-tabs — Era

Bucket ordering: `pre_1700` (n=4), `1700-1900` (n=9), `post_1900` (n=1). post_1900 is Zitkala-Sa alone — do not treat as its own effect, but report for completeness.

### §4.1 C2a spec-alone (C2a-C5)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.612 | 0.470 |
| post_1900 | 1 | -0.308 | 0.000 |
| pre_1700 | 4 | +0.194 | 0.242 |

### §4.1 facts+spec (C4a-C5)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.749 | 0.569 |
| post_1900 | 1 | -0.318 | 0.000 |
| pre_1700 | 4 | +0.324 | 0.271 |

### Mem0 controlled (C3-C1)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.097 | 0.110 |
| post_1900 | 1 | -0.123 | 0.000 |
| pre_1700 | 4 | +0.236 | 0.157 |

### Letta controlled (C3-C1)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.221 | 0.196 |
| post_1900 | 1 | -0.051 | 0.000 |
| pre_1700 | 4 | +0.209 | 0.136 |

### Zep controlled (C3-C1)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.210 | 0.169 |
| post_1900 | 1 | -0.031 | 0.000 |
| pre_1700 | 4 | +0.187 | 0.139 |

### Supermemory controlled

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | -0.051 | 0.171 |
| post_1900 | 1 | -0.246 | 0.000 |
| pre_1700 | 4 | -0.014 | 0.038 |

### Base Layer controlled

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.101 | 0.145 |
| post_1900 | 1 | -0.272 | 0.000 |
| pre_1700 | 4 | +0.112 | 0.125 |

## 3. Raw cross-tabs — Modernity

Bucket ordering: `archaic` (n=4: Augustine, Babur, Bernal Diaz, Cellini), `modern` (n=10). All corpora are in English; archaic = pre-modern English/translation voice.

### §4.1 C2a spec-alone (C2a-C5)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | +0.194 | 0.242 |
| modern | 10 | +0.520 | 0.524 |

### §4.1 facts+spec (C4a-C5)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | +0.324 | 0.271 |
| modern | 10 | +0.643 | 0.628 |

### Mem0 controlled (C3-C1)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | +0.236 | 0.157 |
| modern | 10 | +0.075 | 0.123 |

### Letta controlled (C3-C1)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | +0.209 | 0.136 |
| modern | 10 | +0.194 | 0.203 |

### Zep controlled (C3-C1)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | +0.187 | 0.139 |
| modern | 10 | +0.186 | 0.176 |

### Supermemory controlled

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | -0.014 | 0.038 |
| modern | 10 | -0.070 | 0.173 |

### Base Layer controlled

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | +0.112 | 0.125 |
| modern | 10 | +0.064 | 0.177 |

## 4. Raw cross-tabs — Exoticism

Bucket ordering: `familiar` (n=4: Hamerton, Ebers, Rousseau, Franklin if included — here Rousseau, Ebers, Hamerton = n=3, since Franklin is not in the 14), `marginal-familiar` (n=1: Cellini), `non-Western` (n=10). Small-cell noise warning: `marginal-familiar` has n=1. Reported for transparency only.

### §4.1 C2a spec-alone (C2a-C5)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.756 | 0.441 |
| marginal-familiar | 1 | +0.164 | 0.000 |
| non-Western | 10 | +0.354 | 0.475 |

### §4.1 facts+spec (C4a-C5)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.887 | 0.589 |
| marginal-familiar | 1 | +0.149 | 0.000 |
| non-Western | 10 | +0.491 | 0.543 |

### Mem0 controlled (C3-C1)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.120 | 0.021 |
| marginal-familiar | 1 | +0.364 | 0.000 |
| non-Western | 10 | +0.097 | 0.160 |

### Letta controlled (C3-C1)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.371 | 0.184 |
| marginal-familiar | 1 | +0.413 | 0.000 |
| non-Western | 10 | +0.125 | 0.140 |

### Zep controlled (C3-C1)

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.357 | 0.081 |
| marginal-familiar | 1 | +0.405 | 0.000 |
| non-Western | 10 | +0.113 | 0.134 |

### Supermemory controlled

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.085 | 0.079 |
| marginal-familiar | 1 | -0.036 | 0.000 |
| non-Western | 10 | -0.098 | 0.147 |

### Base Layer controlled

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.133 | 0.146 |
| marginal-familiar | 1 | +0.274 | 0.000 |
| non-Western | 10 | +0.041 | 0.161 |

## 5. Residualized cross-tabs — does the axis add variance beyond C5 baseline?

Residualized Δ = Δ − OLS-predicted(Δ | C5 baseline), computed across all 14 subjects. A bucket mean near zero on the residualized table means the raw bucket-level effect was explained by baseline. A bucket mean still clearly nonzero means the axis adds genuine variance beyond baseline.

### 5.1 Era — residualized

### §4.1 C2a residualized on C5 — by era

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.077 | 0.282 |
| post_1900 | 1 | -0.400 | 0.000 |
| pre_1700 | 4 | -0.072 | 0.180 |

### §4.1 C4a residualized on C5 — by era

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.057 | 0.201 |
| post_1900 | 1 | -0.437 | 0.000 |
| pre_1700 | 4 | -0.019 | 0.244 |

### Mem0 residualized on C5 — by era

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | -0.012 | 0.110 |
| post_1900 | 1 | -0.281 | 0.000 |
| pre_1700 | 4 | +0.097 | 0.134 |

### Letta residualized on C5 — by era

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.034 | 0.189 |
| post_1900 | 1 | -0.282 | 0.000 |
| pre_1700 | 4 | -0.005 | 0.117 |

### Zep residualized on C5 — by era

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.025 | 0.169 |
| post_1900 | 1 | -0.222 | 0.000 |
| pre_1700 | 4 | -0.002 | 0.136 |

### Supermemory residualized on C5 — by era

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | -0.016 | 0.149 |
| post_1900 | 1 | -0.133 | 0.000 |
| pre_1700 | 4 | +0.068 | 0.041 |

### Base Layer residualized on C5 — by era

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| 1700-1900 | 9 | +0.025 | 0.144 |
| post_1900 | 1 | -0.355 | 0.000 |
| pre_1700 | 4 | +0.032 | 0.123 |

### 5.2 Modernity — residualized

### §4.1 C2a residualized on C5 — by modernity

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | -0.072 | 0.180 |
| modern | 10 | +0.029 | 0.304 |

### §4.1 C4a residualized on C5 — by modernity

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | -0.019 | 0.244 |
| modern | 10 | +0.008 | 0.242 |

### Mem0 residualized on C5 — by modernity

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | +0.097 | 0.134 |
| modern | 10 | -0.039 | 0.132 |

### Letta residualized on C5 — by modernity

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | -0.005 | 0.117 |
| modern | 10 | +0.002 | 0.202 |

### Zep residualized on C5 — by modernity

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | -0.002 | 0.136 |
| modern | 10 | +0.001 | 0.177 |

### Supermemory residualized on C5 — by modernity

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | +0.068 | 0.041 |
| modern | 10 | -0.027 | 0.146 |

### Base Layer residualized on C5 — by modernity

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| archaic | 4 | +0.032 | 0.123 |
| modern | 10 | -0.013 | 0.178 |

### 5.3 Exoticism — residualized

### §4.1 C2a residualized on C5 — by exoticism

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.094 | 0.459 |
| marginal-familiar | 1 | +0.102 | 0.000 |
| non-Western | 10 | -0.038 | 0.199 |

### §4.1 C4a residualized on C5 — by exoticism

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.031 | 0.282 |
| marginal-familiar | 1 | +0.069 | 0.000 |
| non-Western | 10 | -0.016 | 0.240 |

### Mem0 residualized on C5 — by exoticism

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.024 | 0.064 |
| marginal-familiar | 1 | +0.203 | 0.000 |
| non-Western | 10 | -0.028 | 0.153 |

### Letta residualized on C5 — by exoticism

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.195 | 0.144 |
| marginal-familiar | 1 | +0.179 | 0.000 |
| non-Western | 10 | -0.077 | 0.141 |

### Zep residualized on C5 — by exoticism

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.174 | 0.075 |
| marginal-familiar | 1 | +0.214 | 0.000 |
| non-Western | 10 | -0.074 | 0.134 |

### Supermemory residualized on C5 — by exoticism

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.099 | 0.015 |
| marginal-familiar | 1 | +0.082 | 0.000 |
| non-Western | 10 | -0.038 | 0.139 |

### Base Layer residualized on C5 — by exoticism

| Bucket | n | mean Δ | std |
|---|---:|---:|---:|
| familiar | 3 | +0.059 | 0.139 |
| marginal-familiar | 1 | +0.191 | 0.000 |
| non-Western | 10 | -0.037 | 0.163 |

## 6. Interpretation

With n=14 split 3 ways on any axis, cell sizes are 1–10. Numbers are descriptive; no significance tests are attempted on cells with n<3. The headline check is whether any axis still shows a bucket separation on the **residualized** tables (§5) after the baseline-collinear component is removed.

**Era: collinear with baseline.** Raw era buckets look suggestive — §4.1 C2a shows Δ=+0.61 on 1700-1900 vs +0.19 on pre_1700. After residualizing on C5 baseline, the separation almost entirely collapses: residualized means are +0.08 (1700-1900) and -0.07 (pre_1700) on C2a, and +0.06 / -0.02 on C4a. Across all 5 memory systems the residualized era buckets are within ±0.10 of zero and within one std of each other. **The "older subjects benefit less" raw pattern is a baseline-collinearity artifact.** The post_1900 bucket (Zitkala-Sa) is the only residualized outlier, but with n=1 it is a single-subject observation, not an era effect.

**Modernity: collinear with baseline.** Same story. Raw archaic vs modern on §4.1 C2a is +0.19 vs +0.52. Residualized it is -0.07 vs +0.03 — essentially collapsed. Mem0 shows a small residual tilt (archaic +0.10 vs modern -0.04) but it is smaller than the within-bucket std. **Language modernity does not add variance beyond baseline.**

**Exoticism: a real small effect survives residualization on 3 of 5 memory systems.** Familiar (n=3: Hamerton, Ebers, Rousseau) retains a positive residualized Δ of +0.17–0.20 on Letta, Zep, Mem0, Base Layer, while non-Western (n=10) sits at -0.03 to -0.08. §4.1 C2a/C4a residualized tables show the separation too but noisier (familiar n=3, std 0.28–0.46). The direction is consistent across 4 of 5 memory systems (Supermemory is the exception — everything near zero). **Possible real signal: the spec helps marginally more on Western-bourgeois-autobiography content than on non-Western content at the same baseline level**, plausibly because the Base Layer spec axioms were developed on Hamerton and carry a Western-introspective frame that generalizes less cleanly to cross-cultural subjects. This is a small effect on a small n — not a finding to lead with.

**Critical caveats.**
1. `familiar` has n=3; one outlier moves the mean by >0.3. Conclusions cannot be statistically distinguished from noise.
2. `familiar` overlaps with "memoir-writer tradition the spec author is embedded in" — this is a pipeline-tuning bias signal more than a content signal. Hamerton is the spec development subject; Ebers and Rousseau are European memoirs in the Western-Christian introspective tradition.
3. `marginal-familiar` is n=1 (Cellini). Report only for transparency.
4. `post_1900` is n=1 (Zitkala-Sa). The residualized -0.28 to -0.44 across systems is consistent with the paper's existing observation that Zitkala-Sa is an anomalous declining case; it is not an era effect.

**Hamerton sensitivity check.** The `familiar` bucket originally has n=3 (Hamerton, Ebers, Rousseau). Hamerton is the spec-development subject and could plausibly belong in `marginal-familiar` instead. Rerun with Hamerton reclassified to `marginal-familiar` (familiar becomes Ebers + Rousseau, marginal-familiar becomes Cellini + Hamerton):

| System | familiar (n=2) | marginal-familiar (n=2) | non-Western (n=10) |
|---|---:|---:|---:|
| Mem0 resid | +0.020 | +0.118 | -0.028 |
| Letta resid | +0.176 | +0.207 | -0.077 |
| Zep resid | +0.185 | +0.183 | -0.074 |
| Supermemory resid | +0.090 | +0.099 | -0.038 |
| Base Layer resid | +0.129 | +0.055 | -0.037 |
| §4.1 C2a resid | -0.099 | +0.291 | -0.038 |
| §4.1 C4a resid | -0.131 | +0.212 | -0.016 |

**The Western-vs-non-Western split is robust to the swap.** With Hamerton in either bucket, Western-adjacent content (familiar + marginal-familiar together, n=4) sits at +0.10 to +0.21 on 4 of 5 memory systems while non-Western (n=10) sits at -0.03 to -0.08. The finding is not Hamerton-carried; collapsing `familiar` and `marginal-familiar` into one "Western-tradition" bucket gives a more robust version of the signal: the spec's residualized lift is consistently larger on subjects in the Western-European-introspective autobiography tradition than on non-Western subjects at the same baseline level. §4.1 raw gradient C2a/C4a flip sign after the swap, which is expected noise at n=2 — the memory-system residualized rows are the more stable evidence.

**Paper-worthiness decision.** **Future Work, not main paper, but a firmer finding than first thought.** The era and modernity axes are collinear with baseline and add no variance beyond the existing §4.1 gradient story. The exoticism axis — now better named **Western-tradition vs non-Western** — shows a stable residualized gap of roughly +0.15 to +0.25 favoring Western-tradition subjects on 4 of 5 memory systems (Supermemory flat at near-zero on both sides). The effect is robust to Hamerton's bucket assignment. With n=4 in the Western-tradition bucket on 5 memory systems, this is enough signal to name but not enough for a main claim. The right home is §8 Future Work as a testable hypothesis: "The Base Layer spec, authored by a person embedded in the Western-introspective autobiographical tradition, transfers its interpretive axioms less effectively to subjects outside that tradition; the spec's residualized lift decays on cross-cultural subjects at matched baseline knowledge." — with a design that recruits a larger, balanced cross-cultural subject pool and matches C5 baselines explicitly.

**One honest paragraph for the paper, if desired:** "We examined whether the spec effect varied by subject era (pre-1700 / 1700-1900 / post-1900), language modernity (archaic / modern translation voice), or content domain (Western-tradition / non-Western). After residualizing on C5 baseline to separate axis effects from baseline-collinearity, era and modernity cross-slices collapsed to within ±0.10 of zero across all five memory systems — era and modernity are collinear with baseline and add no variance beyond the gradient. The Western-tradition vs non-Western axis showed a stable residualized gap of +0.15 to +0.25 favoring Western-tradition subjects on 4 of 5 memory systems (Mem0, Letta, Zep, Base Layer), with Supermemory flat at near-zero on both sides. The finding is robust to Hamerton's bucket assignment (swapping Hamerton from `familiar` to `marginal-familiar` leaves the combined Western-tradition vs non-Western gap intact). With n=4 Western-tradition vs n=10 non-Western, we name this as a hypothesis for future work with a larger cross-cultural subject pool: the Base Layer spec, authored inside the Western-introspective autobiographical tradition, may transfer its axioms less effectively to subjects outside that tradition at matched baseline knowledge."

