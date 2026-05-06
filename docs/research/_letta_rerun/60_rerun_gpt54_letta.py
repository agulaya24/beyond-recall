"""Re-run GPT-5.4 on Letta stateful responses for Hamerton, Ebers, Babur.

Root-cause fix: the original judge_tier2.py used `max_tokens` which GPT-5.x rejects
with HTTP 400 -- must use `max_completion_tokens` instead.

Outputs:
  - Authoritative: overwrites
      memory_system/.../results/global_{ebers,babur}/letta_memory_haiku_judgments_gpt54.json
      memory_system/.../results/run_fullstack_hamerton_20260411_231237/letta_memory_haiku_judgments_gpt54.json
  - Copy for traceability:
      docs/research/_letta_rerun/letta_{subject}_judgments_gpt54.json   (new name, does NOT clash with BL-side file)
"""
import json, os, subprocess, time, re, httpx

RERUN_DIR = os.path.dirname(os.path.abspath(__file__))

# Load API keys from user env
for k in ("OPENAI_API_KEY",):
    r = subprocess.run(["powershell", "-Command",
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    v = r.stdout.strip()
    if v:
        os.environ[k] = v

OPENAI_KEY = os.environ["OPENAI_API_KEY"]

# Same prompt template as judge_tier2.JUDGE_PROMPT (what was used in original Letta scoring)
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


def call_gpt54(prompt):
    """FIXED: uses max_completion_tokens instead of max_tokens."""
    for attempt in range(5):
        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": "gpt-5.4",
                "max_completion_tokens": 10,  # FIX: was max_tokens=10 which GPT-5.x rejects
                "temperature": 0,
                "messages": [{"role": "user", "content": prompt}],
            },
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}",
                "Content-Type": "application/json",
            },
            timeout=60,
        )
        if r.status_code == 429:
            time.sleep(2 ** (attempt + 2))
            continue
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    raise RuntimeError("gpt54 rate limited")


# (subject, results_json_path, canonical_out_path, copy_out_path, condition_label, qt_override?)
SOURCES = [
    ("hamerton",
     r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237\letta_memory_haiku_results.json",
     r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237\letta_memory_haiku_judgments_gpt54.json",
     os.path.join(RERUN_DIR, "letta_hamerton_judgments_gpt54.json"),
     "C_letta_memory_haiku"),
    ("ebers",
     r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_ebers\letta_memory_haiku_results.json",
     r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_ebers\letta_memory_haiku_judgments_gpt54.json",
     os.path.join(RERUN_DIR, "letta_ebers_judgments_gpt54.json"),
     "C_letta_memory_haiku_ebers"),
    ("babur",
     r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_babur\letta_memory_haiku_results.json",
     r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_babur\letta_memory_haiku_judgments_gpt54.json",
     os.path.join(RERUN_DIR, "letta_babur_judgments_gpt54.json"),
     "C_letta_memory_haiku_babur"),
]


def atomic_write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    if os.path.exists(path):
        os.replace(tmp, path)
    else:
        os.rename(tmp, path)


for subject, src_path, out_canon, out_copy, condition in SOURCES:
    with open(src_path, encoding="utf-8") as f:
        data = json.load(f)
    results = data["results"]
    print(f"\n=== {subject}: rescoring {len(results)} Letta responses with GPT-5.4 (fixed) ===")

    out = []
    failures = 0
    for r in results:
        qid = r["question_id"]
        qt = r.get("question_text", "")
        ho = r.get("held_out_passage") or ""
        resp = r.get("response", {})
        if not isinstance(resp, dict) or "text" not in resp or "error" in resp:
            out.append({
                "question_id": qid, "condition": condition, "judge": "gpt54",
                "score": 0, "error": "missing response text", "parse_failure": True,
            })
            continue
        if not ho:
            out.append({
                "question_id": qid, "condition": condition, "judge": "gpt54",
                "score": 0, "error": "missing held_out", "parse_failure": True,
            })
            continue

        prompt = JUDGE_PROMPT.format(question=qt, ground_truth=ho, response=resp["text"])
        try:
            raw = call_gpt54(prompt)
            score = parse_score(raw)
            out.append({
                "question_id": qid, "condition": condition, "judge": "gpt54",
                "score": score, "raw": raw.strip()[:100],
                "parse_failure": score == 0,
            })
            failures = 0
        except Exception as e:
            out.append({
                "question_id": qid, "condition": condition, "judge": "gpt54",
                "score": 0, "error": str(e)[:300], "parse_failure": True,
            })
            failures += 1
            print(f"  ERROR qid={qid}: {e}")
            if failures >= 5:
                print("  5 consecutive failures, aborting")
                break
        time.sleep(0.2)

    valid = [e for e in out if e.get("score", 0) >= 1 and not e.get("parse_failure")]
    mean = sum(e["score"] for e in valid) / len(valid) if valid else 0
    print(f"  valid={len(valid)}/{len(out)}, mean={mean:.3f}")

    atomic_write_json(out_canon, out)
    atomic_write_json(out_copy, out)
    print(f"  wrote: {out_canon}")
    print(f"  copy:  {out_copy}")
