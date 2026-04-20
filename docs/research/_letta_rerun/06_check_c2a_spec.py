"""Determine which spec was used in the paper's C2a run for Ebers and Babur.
Look at results.json or results_v2.json for the 'system_prompt' field,
or compare with the spec.md files available.
"""
import json
import os

RESULTS = r"C:\Users\Aarik\Anthropic\memory-study-repo\results"

for subject in ("ebers", "babur"):
    print(f"\n=== {subject} ===")
    # results_v2.json is where v2 results land
    for name in ("results_v2.json", "results.json"):
        path = os.path.join(RESULTS, f"global_{subject}", name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        print(f"\n  {name} top keys:", list(data.keys()) if isinstance(data, dict) else f"list len={len(data)}")
        if isinstance(data, dict):
            # Check conditions
            if "conditions" in data:
                print(f"   conditions: {list(data['conditions'].keys()) if isinstance(data['conditions'], dict) else data['conditions']}")
                # C2a system prompt
                if isinstance(data["conditions"], dict) and "C2a" in data["conditions"]:
                    c2a = data["conditions"]["C2a"]
                    print(f"   C2a type:", type(c2a).__name__)
                    if isinstance(c2a, dict):
                        print(f"   C2a keys:", list(c2a.keys()))
                        # system_prompt
                        for k in ("system_prompt", "spec", "prompt"):
                            if k in c2a:
                                v = c2a[k]
                                if isinstance(v, str):
                                    print(f"   C2a.{k} preview (first 300):", v[:300])
                                    break
                        # Look at one response for system prompt
                        if "responses" in c2a:
                            rs = c2a["responses"]
                            print(f"   C2a.responses type:", type(rs).__name__, "len:", len(rs) if hasattr(rs, '__len__') else "?")
                            if isinstance(rs, list) and rs:
                                print(f"   responses[0] keys:", list(rs[0].keys()) if isinstance(rs[0], dict) else "not dict")
                                # Is there prompt/spec in the response?
                                if isinstance(rs[0], dict):
                                    for k, v in rs[0].items():
                                        if isinstance(v, str) and len(v) > 500:
                                            print(f"     {k} preview (first 400):", v[:400])
            # Structure may be different — list of responses
            if "responses" in data:
                rs = data["responses"]
                if isinstance(rs, list) and rs:
                    print(f"  responses[0] keys:", list(rs[0].keys()) if isinstance(rs[0], dict) else "not dict")
                    if isinstance(rs[0], dict):
                        for k, v in rs[0].items():
                            if isinstance(v, str) and len(v) > 500:
                                print(f"    {k} (len={len(v)}) preview (first 300):", v[:300].replace('\n', ' '))
                            elif isinstance(v, str):
                                print(f"    {k} (str len={len(v)}):", v[:100])
                            else:
                                print(f"    {k}: {v!r}"[:100])

    # Also check spec.md in the study repo
    spec_path = os.path.join(RESULTS, f"global_{subject}", "spec.md")
    if os.path.exists(spec_path):
        with open(spec_path, encoding="utf-8") as f:
            content = f.read()
        print(f"\n  spec.md size: {len(content)} chars")
        # Does it name the subject?
        name_check = {"ebers": "Ebers", "babur": "Babur"}[subject]
        name_count = content.lower().count(name_check.lower())
        this_person_count = content.lower().count("this person") + content.lower().count("the person") + content.lower().count("they ")
        print(f"  '{name_check}' mentions: {name_count}")
        print(f"  anonymized pronoun ('this person'/'the person'/'they '): {this_person_count}")
        # First 500 chars
        print(f"  preview (first 500 chars):\n  {content[:500]}")
