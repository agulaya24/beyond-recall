"""Reproduce the GPT-5.4 HTTP 400 on a Letta stateful response."""
import json
import os
import subprocess
import httpx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load keys
for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"):
    r = subprocess.run(["powershell", "-Command",
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    v = r.stdout.strip()
    if v:
        os.environ[k] = v

OPENAI_KEY = os.environ["OPENAI_API_KEY"]


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


# Load one Ebers Letta response
with open(r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_ebers\letta_memory_haiku_results.json", encoding="utf-8") as f:
    data = json.load(f)

r = data["results"][0]
resp_text = r["response"]["text"]
ho = r["held_out_passage"]
qt = r["question_text"]

prompt = JUDGE_PROMPT.format(question=qt, ground_truth=ho, response=resp_text)
print(f"prompt len chars: {len(prompt)}")
print(f"resp_text len chars: {len(resp_text)}")

# ATTEMPT 1: Exactly how judge_tier2.py called it
print("\n--- ATTEMPT 1: max_tokens=10 (original) ---")
try:
    r1 = httpx.post("https://api.openai.com/v1/chat/completions",
        json={"model": "gpt-5.4", "max_tokens": 10, "temperature": 0,
              "messages": [{"role": "user", "content": prompt}]},
        headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
        timeout=60)
    print(f"status: {r1.status_code}")
    print(f"body: {r1.text[:500]}")
except Exception as e:
    print(f"EXC: {e}")

# ATTEMPT 2: Same but with max_completion_tokens
print("\n--- ATTEMPT 2: max_completion_tokens=10 ---")
try:
    r2 = httpx.post("https://api.openai.com/v1/chat/completions",
        json={"model": "gpt-5.4", "max_completion_tokens": 10, "temperature": 0,
              "messages": [{"role": "user", "content": prompt}]},
        headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
        timeout=60)
    print(f"status: {r2.status_code}")
    print(f"body: {r2.text[:500]}")
except Exception as e:
    print(f"EXC: {e}")

# ATTEMPT 3: larger max_completion_tokens
print("\n--- ATTEMPT 3: max_completion_tokens=64 ---")
try:
    r3 = httpx.post("https://api.openai.com/v1/chat/completions",
        json={"model": "gpt-5.4", "max_completion_tokens": 64, "temperature": 0,
              "messages": [{"role": "user", "content": prompt}]},
        headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
        timeout=60)
    print(f"status: {r3.status_code}")
    print(f"body: {r3.text[:500]}")
except Exception as e:
    print(f"EXC: {e}")
