"""Step 3: Run Haiku 4.5 C2a responses over the full-stack named spec for each subject.

Mirrors 20_run_c2a_named.py exactly:
  system prompt = "The following is a behavioral specification describing your user.\n\n"
                  "=== BEHAVIORAL SPECIFICATION ===\n" + spec
  model  = claude-haiku-4-5-20251001
  temp   = 0
  max_tokens = 1024

Resumable: saves after every question (atomic). Skips any qid already present.
"""
import json
import os
import subprocess
import sys
import time
import httpx

OUT_DIR = r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\fullstack_named"
PARENT_DIR = r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun"

# Load ANTHROPIC_API_KEY from user env
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
    for attempt in range(3):
        try:
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
                timeout=180,
            )
            if resp.status_code in (429, 529):
                time.sleep(2 ** (attempt + 2))
                continue
            resp.raise_for_status()
            d = resp.json()
            return {
                "text": d["content"][0]["text"],
                "input_tokens": d["usage"]["input_tokens"],
                "output_tokens": d["usage"]["output_tokens"],
            }
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue
            raise


def atomic_write_json(path: str, data: dict):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    if os.path.exists(path):
        os.replace(tmp, path)
    else:
        os.rename(tmp, path)


SUBJECTS = ("hamerton", "ebers", "babur")


def run_subject(subject: str):
    spec_path = os.path.join(OUT_DIR, f"{subject}_spec_fullstack_named.md")
    # Hamerton's battery lives in fullstack_named/; Ebers/Babur batteries live in the parent _letta_rerun/.
    if subject == "hamerton":
        battery_path = os.path.join(OUT_DIR, f"{subject}_letta_battery.json")
    else:
        battery_path = os.path.join(PARENT_DIR, f"{subject}_letta_battery.json")
    out_path = os.path.join(OUT_DIR, f"{subject}_bl_c2a_fullstack_responses.json")

    with open(spec_path, encoding="utf-8") as f:
        spec = f.read()
    with open(battery_path, encoding="utf-8") as f:
        battery = json.load(f)

    system_prompt = (
        "The following is a behavioral specification describing your user.\n\n"
        "=== BEHAVIORAL SPECIFICATION ===\n" + spec
    )

    # Resume: load any existing results
    existing_by_qid = {}
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            prior = json.load(f)
        for r in prior.get("results", []):
            if r.get("response") and not r.get("error"):
                existing_by_qid[r["question_id"]] = r

    results = list(existing_by_qid.values())
    print(f"\n[{subject}] spec={len(spec):,} chars | battery={len(battery['questions'])} qs | resuming with {len(results)} cached")

    payload = {
        "subject": subject,
        "source_spec": os.path.basename(spec_path),
        "source_battery": os.path.basename(battery_path),
        "response_model": "claude-haiku-4-5-20251001",
        "condition": "BL-C2a-fullstack-named (full layered spec + Haiku, no retrieval, no facts) on Letta stateful battery",
        "total": len(battery["questions"]),
        "results": results,
    }

    done = 0
    for i, q in enumerate(battery["questions"]):
        qid = q["question_id"]
        if qid in existing_by_qid:
            continue
        qt = q["question_text"]
        try:
            r = gen_response(qt, system_prompt)
            entry = {
                "question_id": qid,
                "question_text": qt,
                "held_out_passage": q.get("held_out_passage", ""),
                "response": r["text"],
                "input_tokens": r["input_tokens"],
                "output_tokens": r["output_tokens"],
            }
            results.append(entry)
            preview = r["text"][:80].encode("ascii", errors="replace").decode("ascii").replace("\n", " ")
            print(f"  Q{qid:02d} ok ({r['input_tokens']}t in, {r['output_tokens']}t out): {preview}")
        except Exception as e:
            entry = {
                "question_id": qid,
                "question_text": qt,
                "held_out_passage": q.get("held_out_passage", ""),
                "response": "",
                "error": str(e)[:500],
            }
            results.append(entry)
            print(f"  Q{qid:02d} ERROR: {e}")

        # Save after every question (atomic, resumable)
        payload["results"] = results
        atomic_write_json(out_path, payload)
        done += 1
        # Light rate limit safety every 10
        if done % 10 == 0:
            time.sleep(0.5)

    # Sort by qid for cleanliness
    results.sort(key=lambda x: x["question_id"])
    payload["results"] = results
    atomic_write_json(out_path, payload)
    print(f"[{subject}] wrote {out_path} (n={len(results)})")


def main():
    for s in SUBJECTS:
        run_subject(s)


if __name__ == "__main__":
    main()
