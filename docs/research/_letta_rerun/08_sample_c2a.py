"""Sample C2a response texts to confirm the run used the named or anonymized spec."""
import json
import os

for subject in ("ebers", "babur"):
    print(f"\n========== {subject} ==========")
    path = os.path.join(r"C:\Users\Aarik\Anthropic\memory-study-repo\results", f"global_{subject}", "results_v2.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # Show first 3 C2a responses (just first 400 chars each)
    name = {"ebers": "Ebers", "babur": "Babur"}[subject]
    for i, q in enumerate(data[:5]):
        qid = q.get("question_id")
        qt = q.get("question_text", "").encode("ascii", errors="replace").decode("ascii")
        c2a_resp = q.get("responses", {}).get("C2a_full_spec", "")
        c5_resp = q.get("responses", {}).get("C5_baseline", "")
        if isinstance(c2a_resp, dict):
            c2a_resp = c2a_resp.get("text", "") or str(c2a_resp)
        if isinstance(c5_resp, dict):
            c5_resp = c5_resp.get("text", "") or str(c5_resp)
        c2a_preview = c2a_resp[:400].encode("ascii", errors="replace").decode("ascii").replace("\n", " ")
        print(f"\n  Q{qid}: {qt[:120]}")
        print(f"    C2a response (first 400): {c2a_preview}")
        # Check if the response names the subject or refuses
        if "don't have information" in c2a_resp or "don't have reliable" in c2a_resp or "I don't know" in c2a_resp:
            print(f"    !!! REFUSAL DETECTED !!!")
        name_count = c2a_resp.count(name)
        this_person = c2a_resp.count("this person") + c2a_resp.count("the person") + c2a_resp.count("they ")
        print(f"    named '{name}' count: {name_count} | anonymized pronouns: {this_person}")
