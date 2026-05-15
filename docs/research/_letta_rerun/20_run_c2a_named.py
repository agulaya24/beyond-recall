"""Part 4: Run BL C2a (named spec + Haiku 4.5) on the Letta stateful battery.
No retrieval, no facts — just the spec + question.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path
import httpx

REPO = Path(__file__).resolve().parents[3]
OUT_DIR = str(REPO / "docs" / "research" / "_letta_rerun")

# Load ANTHROPIC_API_KEY from user env via powershell
for k in ["ANTHROPIC_API_KEY"]:
    r = subprocess.run(["powershell", "-Command",
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    val = r.stdout.strip()
    if val:
        os.environ[k] = val

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("ERROR: ANTHROPIC_API_KEY not found", file=sys.stderr)
    sys.exit(1)

def gen_response(question: str, system_prompt: str) -> dict:
    resp = httpx.post(
        "https://api.anthropic.com/v1/messages",
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 1024,
            "temperature": 0,
            "system": system_prompt,
            "messages": [{"role": "user", "content": question}],
        },
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        timeout=120,
    )
    resp.raise_for_status()
    d = resp.json()
    return {
        "text": d["content"][0]["text"],
        "input_tokens": d["usage"]["input_tokens"],
        "output_tokens": d["usage"]["output_tokens"],
    }

for subject in ("ebers", "babur"):
    spec_path = os.path.join(OUT_DIR, f"{subject}_spec_named.md")
    battery_path = os.path.join(OUT_DIR, f"{subject}_letta_battery.json")
    out_path = os.path.join(OUT_DIR, f"{subject}_bl_c2a_named_responses.json")

    # Skip if already done
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            existing = json.load(f)
        if len(existing.get("results", [])) >= 40:
            print(f"[{subject}] Already complete ({len(existing['results'])} responses). Skipping.")
            continue

    with open(spec_path, encoding="utf-8") as f:
        spec = f.read()
    with open(battery_path, encoding="utf-8") as f:
        battery = json.load(f)

    system_prompt = (
        "The following is a behavioral specification describing your user.\n\n"
        "=== BEHAVIORAL SPECIFICATION ===\n" + spec
    )

    results = []
    print(f"\n[{subject}] spec size: {len(spec)} chars | {len(battery['questions'])} questions")
    for i, q in enumerate(battery["questions"]):
        qid = q["question_id"]
        qt = q["question_text"]
        try:
            r = gen_response(qt, system_prompt)
            results.append({
                "question_id": qid,
                "question_text": qt,
                "held_out_passage": q["held_out_passage"],
                "response": r["text"],
                "input_tokens": r["input_tokens"],
                "output_tokens": r["output_tokens"],
            })
            # Simple progress printout without emitting non-ascii
            preview = r["text"][:80].encode("ascii", errors="replace").decode("ascii").replace("\n", " ")
            print(f"  Q{qid:02d} ok ({r['input_tokens']}t in, {r['output_tokens']}t out): {preview}")
        except Exception as e:
            print(f"  Q{qid:02d} ERROR: {e}")
            results.append({
                "question_id": qid,
                "question_text": qt,
                "held_out_passage": q["held_out_passage"],
                "response": "",
                "error": str(e),
            })
        # Light rate limit safety
        if (i + 1) % 10 == 0:
            time.sleep(0.5)

    payload = {
        "subject": subject,
        "source_spec": os.path.basename(spec_path),
        "source_battery": os.path.basename(battery_path),
        "response_model": "claude-haiku-4-5-20251001",
        "condition": "BL-C2a-named (named spec + Haiku, no retrieval, no facts) on Letta stateful battery",
        "total": len(results),
        "results": results,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"[{subject}] Wrote {out_path} ({len(results)} responses)")
