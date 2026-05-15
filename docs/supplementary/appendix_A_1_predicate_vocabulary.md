# Appendix A.1 — The 46 Constrained Predicates (full vocabulary)

*Mirrored from beyond_recall_v11.9.1. The paper retains a one-paragraph overview in Appendix A.1 and an architectural reference in §3.7.*

---

### A.1 The 46 Constrained Predicates

The extraction step (Step 2 of the pipeline, §3.7) instructs the extraction model to emit triples of the form `(subject, predicate, object)` using only the 46 predicates listed below. Predicates outside this list are either normalized by `normalize_predicate()` into the canonical form or routed to the `unknown` catch-all (which is filterable downstream, not silently dropped). The vocabulary is frozen for the study; it was curated and validated across roughly 50 pilot subjects before being locked. The canonical source is `memory_system/src/baselayer/config.py` lines 613-639 (`CONSTRAINED_PREDICATES`).

The predicates group into seven behavioral dimensions. The groupings below are analytical; the predicate list itself is flat in code.

**Behavioral patterns (activities and engagement).** These are the most load-bearing predicates for interpretive representation. They describe what the subject repeatedly does or refuses to do, which is what anchors the authored layers in §3.7.

| Predicate | Definition | Example usage |
|---|---|---|
| `practices` | Repeated deliberate activity, skill-building, or routine. | (subject) `practices` daily writing |
| `avoids` | Consistent pattern of not engaging with a thing or situation. | (subject) `avoids` hierarchical social settings |
| `prefers` | Systematic choice of one option over another when both available. | (subject) `prefers` solitary work over committees |
| `follows` | Active tracking of a person, domain, or source. | (subject) `follows` developments in French art theory |
| `monitors` | Active observation, narrower than `follows`. | (subject) `monitors` his guardian's health |
| `plays` | Games, sports, musical instruments. | (subject) `plays` chess |
| `studies` | Deliberate intellectual engagement with a topic or body of work. | (subject) `studies` Renaissance painters |
| `builds` | Creation of things, relationships, or institutions. | (subject) `builds` a private library over decades |
| `manages` | Ongoing oversight or administration. | (subject) `manages` the household finances |

**Values, beliefs, and self-view.** These populate the core layer (§3.7) and describe the stable commitments a subject carries across situations.

| Predicate | Definition | Example usage |
|---|---|---|
| `values` | What the subject holds as important or worthy. | (subject) `values` intellectual honesty over social standing |
| `believes` | Propositional commitment, often theological or ideological. | (subject) `believes` scripture is not divinely infallible |
| `prioritizes` | Revealed-preference ranking under constraint. | (subject) `prioritizes` proximity to family over career advancement |
| `identifies_as` | How the subject labels or categorizes the self. | (subject) `identifies_as` an independent artist, not a teacher |
| `aspires_to` | Directional aspiration toward a goal or state. | (subject) `aspires_to` mastery of French prose |
| `wants_to` | Narrower than `aspires_to`; immediate desire. | (subject) `wants_to` visit the ancestral homes |

**Emotions and dispositions.** These describe affective responses, which often provide the clearest behavioral signal in autobiographical text.

| Predicate | Definition | Example usage |
|---|---|---|
| `fears` | Things, situations, or outcomes the subject avoids or guards against. | (subject) `fears` religious hypocrisy more than social ostracism |
| `loves` | Strong positive emotion, stronger than `enjoys`. | (subject) `loves` the moors near Burnley |
| `hates` | Strong negative emotion, stronger than `dislikes`. | (subject) `hates` formal balls |
| `enjoys` | Mild positive engagement. | (subject) `enjoys` long walks |
| `dislikes` | Mild negative response. | (subject) `dislikes` urban environments |
| `admires` | Respect or admiration, often toward a specific person. | (subject) `admires` Ruskin's early prose |
| `struggles_with` | Recurring difficulty or area of known weakness. | (subject) `struggles_with` time management |
| `excels_at` | Recurring demonstrated strength. | (subject) `excels_at` verbal persuasion in small groups |

**Experiences, decisions, and learning.** Transitive episodic events and the inferences drawn from them.

| Predicate | Definition | Example usage |
|---|---|---|
| `experienced` | An episodic event the subject underwent. | (subject) `experienced` his guardian's death in 1857 |
| `learned` | A concrete skill, fact, or lesson derived from experience. | (subject) `learned` that shame is more effective than instruction in driving mastery |
| `decided` | A specific documented decision or resolution. | (subject) `decided` not to pursue a political career |
| `lost` | A thing, relationship, or role no longer held. | (subject) `lost` his fortune in the poetry-book failure |
| `founded` | Institutions or groups the subject created. | (subject) `founded` a French-language art journal |

**Relationships (Session 55 expansion).** A targeted set of relationship predicates, added to raise relationship-fact extraction from 0.8% to the 3 to 5% range.

| Predicate | Definition | Example usage |
|---|---|---|
| `married_to` | Marriage relationship. | (subject) `married_to` Eugenie Gindriez |
| `parents` | The subject's parents (subject is the child). | (subject) `parents` are John and Mary Hamerton |
| `raised_by` | Parental or guardian relationship from the child's perspective. | (subject) `raised_by` his aunt after his father's death |
| `mentored_by` | Directional mentor relationship; subject was mentored. | (subject) `mentored_by` his guardian's circle |
| `friends_with` | Friendship. | (subject) `friends_with` a Doncaster schoolfellow |
| `collaborates_with` | Professional or creative collaboration. | (subject) `collaborates_with` the editor of the *Saturday Review* |
| `reports_to` | Organizational hierarchy. | (subject) `reports_to` the regimental commander |
| `relates_to` | Generic relationship fallback when the specific type is unclear. | (subject) `relates_to` the Breadalbane family as distant hosts |
| `conflicts_with` | Recurring tension or disagreement. | (subject) `conflicts_with` the Anglican social consensus |
| `maintains` | Ongoing relationship, practice, or commitment. | (subject) `maintains` correspondence with French friends |

**Biographical context.** Stable factual biographical attributes. These are not the most predictive class but are needed for disambiguation and for the anchors layer's detection conditions.

| Predicate | Definition | Example usage |
|---|---|---|
| `owns` | Property or possessions. | (subject) `owns` a house on Loch Awe |
| `works_at` | Current or past workplace. | (subject) `works_at` the *Portfolio* magazine |
| `lives_in` | Current or past residence. | (subject) `lives_in` a Scottish island |
| `raised_in` | Place where the subject grew up. | (subject) `raised_in` Lancashire |
| `attended` | Attendance at an institution (may or may not include graduation). | (subject) `attended` Doncaster Grammar School |
| `graduated_from` | Specifically graduated (distinct from `attended`). | (subject) `graduated_from` no university |
| `interested_in` | Passive interest, weaker than `follows` or `studies`. | (subject) `interested_in` heraldry |

**Fallback.**

| Predicate | Definition | Example usage |
|---|---|---|
| `unknown` | Catch-all for extracted claims that do not map cleanly to any of the 45 above. Filterable, never silently dropped. | (subject) `unknown` [unmapped extracted claim] |

