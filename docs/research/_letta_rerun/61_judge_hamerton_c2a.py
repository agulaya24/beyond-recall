"""Judge Hamerton C2a_full_spec responses (on Letta battery qids)
with sonnet, opus, gpt4o, gpt54 to complete the 5-judge primary panel.
Haiku judgments already exist in analysis/judgments.json.

Reads responses from:
  memory_system/.../run_fullstack_hamerton_20260411_231237/results.json

Writes judgments to:
  _letta_rerun/hamerton_bl_c2a_judgments_{judge}.json
"""
import json, os, subprocess, time, re, httpx

RERUN_DIR = os.path.dirname(os.path.abspath(__file__))

# Load keys
for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
    r = subprocess.run(["powershell", "-Command",
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    v = r.stdout.strip()
    if v:
        os.environ[k] = v

ANT_KEY = os.environ["ANTHROPIC_API_KEY"]
OAI_KEY = os.environ["OPENAI_API_KEY"]

JUDGE_PROMPT = """You are evaluating a behavioral prediction against a verbatim ground truth passage.

Question: {question}

Ground truth (what actually happened): {ground_truth}

Response to score: {response}

Score 1-5 based on prediction accuracy:
5 = Predicts the specific outcome or behavior in the ground truth
4 = Predicts the general direction correctly with some specifics
3 = Captures the right domain but not the specific outcome
2 = Addresses the topic but predicts incorrectly
1 = Refuses to answer or is completely off-base

Respond with only the number 1, 2, 3, 4, or 5."""


def parse_score(text):
    if not text:
        return 0
    m = re.search(r"\b([1-5])\b", text.strip())
    return int(m.group(1)) if m else 0


def anthropic_call(model, prompt, max_tokens=10):
    for attempt in range(6):
        r = httpx.post(
            "https://api.anthropic.com/v1/messages",
            json={"model": model, "max_tokens": max_tokens, "temperature": 0,
                  "messages": [{"role": "user", "content": prompt}]},
            headers={"x-api-key": ANT_KEY, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"},
            timeout=60,
        )
        if r.status_code in (429, 529):
            time.sleep(2 ** (attempt + 2))
            continue
        r.raise_for_status()
        return r.json()["content"][0]["text"]
    raise RuntimeError(f"{model} rate limited")


def openai_call(model, prompt, max_tokens_key="max_tokens", max_tokens=10):
    for attempt in range(5):
        payload = {"model": model, max_tokens_key: max_tokens, "temperature": 0,
                   "messages": [{"role": "user", "content": prompt}]}
        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {OAI_KEY}", "Content-Type": "application/json"},
            timeout=60,
        )
        if r.status_code == 429:
            time.sleep(2 ** (attempt + 2))
            continue
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    raise RuntimeError(f"{model} rate limited")


JUDGES = {
    "sonnet": lambda p: anthropic_call("claude-sonnet-4-6", p),
    "opus": lambda p: anthropic_call("claude-opus-4-6", p),
    "gpt4o": lambda p: openai_call("gpt-4o", p, "max_tokens", 10),
    "gpt54": lambda p: openai_call("gpt-5.4", p, "max_completion_tokens", 10),
}


def atomic_write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    if os.path.exists(path):
        os.replace(tmp, path)
    else:
        os.rename(tmp, path)


# Load Hamerton main results + Letta battery qids
base = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237"
with open(f"{base}\\results.json", encoding="utf-8") as f:
    main = json.load(f)
with open(f"{base}\\letta_memory_haiku_results.json", encoding="utf-8") as f:
    letta = json.load(f)

letta_qids = set(r["question_id"] for r in letta["results"])

items = []
for r in main:
    qid = r["question_id"]
    if qid not in letta_qids:
        continue
    resp = r.get("responses", {}).get("C2a_full_spec")
    if not isinstance(resp, dict) or "text" not in resp:
        continue
    ho = r.get("held_out_passage") or ""
    qt = r.get("question_text", "")
    if not ho:
        continue
    items.append((qid, qt, ho, resp["text"]))

print(f"Hamerton C2a items on Letta battery: {len(items)}")

for judge_name, judge_fn in JUDGES.items():
    out_path = os.path.join(RERUN_DIR, f"hamerton_bl_c2a_judgments_{judge_name}.json")
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            existing = json.load(f)
        valid = sum(1 for e in existing if e.get("score", 0) >= 1 and not e.get("parse_failure"))
        if len(existing) >= len(items) and valid == len(items):
            print(f"  [{judge_name}] complete (n={len(existing)}, valid={valid}), skipping")
            continue

    print(f"  [{judge_name}] scoring {len(items)} Hamerton C2a responses...")
    out = []
    failures = 0
    for qid, qt, ho, rt in items:
        prompt = JUDGE_PROMPT.format(question=qt, ground_truth=ho, response=rt)
        try:
            raw = judge_fn(prompt)
            score = parse_score(raw)
            out.append({
                "question_id": qid, "condition": "C2a_full_spec", "judge": judge_name,
                "score": score, "raw": raw.strip()[:100],
                "parse_failure": score == 0,
            })
            failures = 0
        except Exception as e:
            out.append({
                "question_id": qid, "condition": "C2a_full_spec", "judge": judge_name,
                "score": 0, "error": str(e)[:300], "parse_failure": True,
            })
            failures += 1
            print(f"    ERROR qid={qid}: {e}")
            if failures >= 5:
                break
        time.sleep(0.2)

    valid = [e for e in out if e.get("score", 0) >= 1 and not e.get("parse_failure")]
    mean = sum(e["score"] for e in valid) / len(valid) if valid else 0
    print(f"  [{judge_name}] valid={len(valid)}/{len(out)}, mean={mean:.3f}")
    atomic_write_json(out_path, out)
