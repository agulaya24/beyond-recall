"""Pull a stratified random sample of 30 classified responses for human spot-check."""
import json, random
random.seed(17)

d = json.load(open("C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/wrong_spec_detection_raw.json", encoding="utf-8"))
rows = d["rows"]
# Stratify by category
by_cat = {}
for r in rows:
    by_cat.setdefault(r["category"], []).append(r)

# Sample 10 from explicit, 10 from misapply, 5 from implicit (if available), 5 ambiguous (if available)
sample = []
quota = {"explicit": 10, "misapply": 10, "implicit": 5, "ambiguous": 5}
for cat, n in quota.items():
    pool = by_cat.get(cat, [])
    if pool:
        sample.extend(random.sample(pool, min(n, len(pool))))

out = []
for r in sample:
    out.append({
        "subject_key": r["subject_key"],
        "subject_name": r["subject_name"],
        "question_id": r["question_id"],
        "question_text": r["question_text"],
        "category_predicted": r["category"],
        "evidence_quote": r["evidence_quote"],
        "response_first_1200": r["response_full"][:1200],
    })

with open("C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/wrong_spec_validation_sample.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(out)} validation samples")
