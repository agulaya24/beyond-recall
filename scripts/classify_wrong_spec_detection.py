"""Classify wrong-spec responses by detection behavior.

For each C2c_wrong_spec response across global subjects (v2 derangement) and
Hamerton (v1 Franklin), classify into:
  1) explicit  - response explicitly flags that the spec does not describe the
                 subject, refuses to apply it, or names the mismatch
  2) implicit  - response hedges, acknowledges uncertainty, or notes a poor fit
                 without explicitly naming a mismatch
  3) misapply  - response attempts to apply the spec as if it were the subject's,
                 producing a low-quality or confabulated prediction
  4) ambiguous - cannot be cleanly classified

Uses Haiku with structured output. Saves per-response labels plus a summary.
"""
import json
import os
import sys
from pathlib import Path
import anthropic

SUBJECTS_V2 = [
    "global_augustine", "global_babur", "global_bernal_diaz", "global_cellini",
    "global_ebers", "global_equiano", "global_fukuzawa", "global_keckley",
    "global_rousseau", "global_seacole", "global_sunity_devee", "global_yung_wing",
    "global_zitkala_sa",
]
HAMERTON_V1 = "hamerton"  # has C2c_full_wrong_spec (Franklin's spec)

RESULTS_ROOT = Path("C:/Users/Aarik/Anthropic/memory-study-repo/results")
OUT_PATH = Path("C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/wrong_spec_detection_raw.json")

JUDGE_PROMPT = """You are classifying a language model's response to a knowledge probe.
The model was shown a BEHAVIORAL SPECIFICATION that describes some person's patterns of decision-making, values, risk tolerance, etc., and was then asked a question about a DIFFERENT named historical subject. The spec does NOT describe the subject in the question. This is a mismatch condition.

Classify the response into exactly one of these categories based on how it handles the mismatch:

1. explicit
   The response explicitly flags that the specification does not describe the subject of the question, OR explicitly refuses to apply it, OR states the spec describes someone different. Phrases like "the specification describes someone fundamentally different," "this does not contain information about [subject]," "I need to flag that," "the profile does not match," "I cannot apply this to [subject]" count as explicit.

2. implicit
   The response hedges, acknowledges uncertainty, or notes the spec is a poor fit WITHOUT explicitly saying the spec describes someone else or refusing. Phrases like "does not map cleanly," "the spec is limited here," "based on what the spec supports..." with substantial hedging.

3. misapply
   The response attempts to apply the spec as if it DID describe the subject, producing a prediction that maps spec patterns onto the named subject. No clear flag of mismatch. The response may still be wrong, but it does not surface the mismatch to the reader.

4. ambiguous
   Cannot be cleanly classified (e.g. partial flag + partial application, or the response is too short to judge).

Return JSON only, with this exact shape:
{"category": "explicit" | "implicit" | "misapply" | "ambiguous", "evidence_quote": "<up to 200 chars quoted verbatim from the response>"}

Do not add commentary. Do not add markdown fences."""


def classify(client, subject_name, question_text, response_text):
    user_msg = (
        f"Subject of the question: {subject_name}\n"
        f"Question: {question_text}\n\n"
        f"Model response (begins below):\n---\n{response_text[:6000]}\n---"
    )
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=JUDGE_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        text = resp.content[0].text.strip()
        # Strip potential markdown fencing
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        obj = json.loads(text)
        cat = obj.get("category", "ambiguous")
        if cat not in ("explicit", "implicit", "misapply", "ambiguous"):
            cat = "ambiguous"
        quote = obj.get("evidence_quote", "")[:240]
        return cat, quote, None
    except Exception as e:
        return "ambiguous", "", str(e)


def subject_display_name(sub_key):
    # Derive a best-effort display name for the question subject
    mapping = {
        "global_augustine": "Augustine",
        "global_babur": "Babur",
        "global_bernal_diaz": "Bernal Diaz",
        "global_cellini": "Cellini",
        "global_ebers": "Ebers",
        "global_equiano": "Equiano",
        "global_fukuzawa": "Fukuzawa",
        "global_keckley": "Keckley",
        "global_rousseau": "Rousseau",
        "global_seacole": "Mary Seacole",
        "global_sunity_devee": "Sunity Devee",
        "global_yung_wing": "Yung Wing",
        "global_zitkala_sa": "Zitkala-Sa",
        "hamerton": "Hamerton",
    }
    return mapping.get(sub_key, sub_key)


def load_wrong_spec_responses():
    rows = []
    # v2: global subjects
    for sub in SUBJECTS_V2:
        path = RESULTS_ROOT / sub / "results_v2.json"
        if not path.exists():
            print(f"MISSING: {path}")
            continue
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        for q in d:
            r = q.get("responses", {}).get("C2c_wrong_spec")
            if r and r.get("text"):
                rows.append({
                    "subject_key": sub,
                    "subject_name": subject_display_name(sub),
                    "variant": "v2_derangement",
                    "question_id": q.get("question_id"),
                    "question_text": q.get("question_text", ""),
                    "response_text": r["text"],
                })
    # v1: Hamerton
    path = RESULTS_ROOT / HAMERTON_V1 / "results.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        for q in d:
            resp = q.get("responses", {})
            r = resp.get("C2c_full_wrong_spec") or resp.get("C2c_wrong_spec")
            if r and r.get("text"):
                rows.append({
                    "subject_key": HAMERTON_V1,
                    "subject_name": subject_display_name(HAMERTON_V1),
                    "variant": "v1_franklin",
                    "question_id": q.get("question_id"),
                    "question_text": q.get("question_text", ""),
                    "response_text": r["text"],
                })
    return rows


def main():
    rows = load_wrong_spec_responses()
    print(f"Loaded {len(rows)} wrong-spec responses to classify")
    client = anthropic.Anthropic()
    results = []
    from collections import Counter
    counts = Counter()
    for i, row in enumerate(rows, 1):
        cat, quote, err = classify(
            client,
            row["subject_name"],
            row["question_text"],
            row["response_text"],
        )
        counts[cat] += 1
        results.append({
            "subject_key": row["subject_key"],
            "subject_name": row["subject_name"],
            "variant": row["variant"],
            "question_id": row["question_id"],
            "question_text": row["question_text"],
            "response_preview": row["response_text"][:500],
            "response_full": row["response_text"],
            "category": cat,
            "evidence_quote": quote,
            "error": err,
        })
        if i % 20 == 0 or i == len(rows):
            print(f"  [{i}/{len(rows)}] running counts: {dict(counts)}")
            # Checkpoint save
            OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(OUT_PATH, "w", encoding="utf-8") as f:
                json.dump({"counts": dict(counts), "total": len(results), "rows": results}, f, indent=2)
    print("FINAL counts:", dict(counts))
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
