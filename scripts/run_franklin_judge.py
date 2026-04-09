"""
Franklin Study — 4-Judge Pipeline
Scores behavioral prediction responses from all conditions.
Supports Haiku (immediate), Sonnet/Opus (Anthropic batch), GPT-4o (OpenAI batch).

Usage:
    python run_franklin_judge.py haiku          # immediate Haiku scoring
    python run_franklin_judge.py submit-sonnet  # submit Sonnet batch
    python run_franklin_judge.py submit-opus    # submit Opus batch
    python run_franklin_judge.py submit-gpt4o   # submit GPT-4o batch
    python run_franklin_judge.py check          # check all batch statuses
    python run_franklin_judge.py process-sonnet # process Sonnet results
    python run_franklin_judge.py process-opus   # process Opus results
    python run_franklin_judge.py process-gpt4o  # process GPT-4o results
    python run_franklin_judge.py summary        # 4-judge comparison table
"""

import json
import os
import sys
import re
import subprocess
import argparse
from collections import defaultdict
from glob import glob

import httpx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Find the Franklin results directory
FRANKLIN_RUNS = sorted(glob(os.path.join(BASE_DIR, "results", "run_franklin_*")))

CONDITIONS = [
    "C1_mem0", "C1_supermemory",
    "C2a_spec_only", "C2c_wrong_spec",
    "C3_mem0", "C3_supermemory",
    "C4_factdump", "C4a_factdump_plus_spec",
    "C5_baseline", "C6_random", "C7_named_baseline",
    "C9_raw_corpus",
]


def load_env():
    for k in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]:
        r = subprocess.run(
            ["powershell", "-Command",
             f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
            capture_output=True, text=True
        )
        val = r.stdout.strip()
        if val:
            os.environ[k] = val


def find_results():
    """Find the Franklin results file."""
    for run_dir in reversed(FRANKLIN_RUNS):
        results_file = os.path.join(run_dir, "results.json")
        if os.path.exists(results_file):
            return results_file, run_dir
        # Check checkpoint
        cp_file = os.path.join(run_dir, "checkpoint.json")
        if os.path.exists(cp_file):
            return cp_file, run_dir
    print("ERROR: No Franklin results found", flush=True)
    sys.exit(1)


def load_results(results_file):
    """Load results, handling both results.json and checkpoint.json format."""
    with open(results_file, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "results" in data:
        return data["results"]  # checkpoint format
    return data  # results.json format


def build_judge_prompt(held_out, response_text):
    return (
        "You are evaluating whether a response about a person PREDICTED "
        "what actually happened, as described in a held-out passage the "
        "response author never saw.\n\n"
        f"=== HELD-OUT GROUND TRUTH ===\n{held_out}\n\n"
        f"=== RESPONSE BEING EVALUATED ===\n{response_text[:1500]}\n\n"
        "Rate the prediction accuracy on this scale:\n"
        "5 = Response predicts the specific outcome/behavior in the ground truth\n"
        "4 = Response predicts the general direction correctly with some specifics\n"
        "3 = Response captures the right domain but not the specific outcome\n"
        "2 = Response addresses the topic but predicts incorrectly\n"
        "1 = Response refuses to answer or is completely off-base\n\n"
        "Respond with ONLY a single digit (1-5)."
    )


def get_pred_items(results):
    """Extract all (qid, condition, held_out, response_text) tuples for behavioral prediction."""
    items = []
    for r in results:
        if r.get("tier") != "behavioral_prediction" or not r.get("held_out_passage"):
            continue
        qid = r["question_id"]
        held_out = r["held_out_passage"]
        for cond in CONDITIONS:
            resp = r.get("responses", {}).get(cond, {})
            resp_text = resp.get("text", "")
            if resp_text and "error" not in resp:
                items.append((qid, cond, held_out, resp_text))
    return items


# === HAIKU JUDGE (immediate) ===

def cmd_haiku():
    load_env()
    api_key = os.environ["ANTHROPIC_API_KEY"]
    results_file, run_dir = find_results()
    results = load_results(results_file)
    items = get_pred_items(results)
    analysis_dir = os.path.join(run_dir, "analysis")
    os.makedirs(analysis_dir, exist_ok=True)

    print(f"Scoring {len(items)} items with Haiku...", flush=True)

    judgments = []
    for i, (qid, cond, held_out, resp_text) in enumerate(items):
        prompt = build_judge_prompt(held_out, resp_text)
        try:
            resp = httpx.post(
                "https://api.anthropic.com/v1/messages",
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": 8,
                    "temperature": 0,
                    "messages": [{"role": "user", "content": prompt}],
                },
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                timeout=30,
            )
            data = resp.json()
            txt = data["content"][0]["text"].strip()
            score = int(txt[0]) if txt and txt[0].isdigit() else 0
        except Exception as e:
            print(f"  ERROR q{qid}_{cond}: {e}", flush=True)
            score = 0

        judgments.append({"question_id": qid, "condition": cond, "haiku_score": score})
        if (i + 1) % 50 == 0:
            print(f"  {i+1}/{len(items)} scored", flush=True)

    # Save
    with open(os.path.join(analysis_dir, "haiku_judgments.json"), "w") as f:
        json.dump(judgments, f, indent=2)

    # Summary
    cond_scores = defaultdict(list)
    for j in judgments:
        if j["haiku_score"] > 0:
            cond_scores[j["condition"]].append(j["haiku_score"])

    summary = {}
    print(f"\n{'Condition':<25} {'Mean':>6} {'n':>4}", flush=True)
    print("=" * 40, flush=True)
    for cond in sorted(cond_scores, key=lambda c: -sum(cond_scores[c])/len(cond_scores[c])):
        scores = cond_scores[cond]
        mean = sum(scores) / len(scores)
        summary[cond] = {"avg_score": round(mean, 2), "n": len(scores),
                         "score_dist": {str(i): scores.count(i) for i in range(1, 6)}}
        print(f"  {cond:<23} {mean:>6.2f} {len(scores):>4}", flush=True)

    with open(os.path.join(analysis_dir, "haiku_prediction_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nSaved to {analysis_dir}", flush=True)


# === BATCH SUBMISSION (Sonnet, Opus, GPT-4o) ===

def cmd_submit_anthropic(model_name, model_id):
    load_env()
    api_key = os.environ["ANTHROPIC_API_KEY"]
    results_file, run_dir = find_results()
    results = load_results(results_file)
    items = get_pred_items(results)
    analysis_dir = os.path.join(run_dir, "analysis")
    os.makedirs(analysis_dir, exist_ok=True)

    # Build JSONL
    batch_file = os.path.join(analysis_dir, f"{model_name}_batch_input.jsonl")
    count = 0
    with open(batch_file, "w", encoding="utf-8") as f:
        for qid, cond, held_out, resp_text in items:
            prompt = build_judge_prompt(held_out, resp_text)
            batch_req = {
                "custom_id": f"q{qid}_{cond}",
                "params": {
                    "model": model_id,
                    "max_tokens": 8,
                    "temperature": 0,
                    "messages": [{"role": "user", "content": prompt}],
                }
            }
            f.write(json.dumps(batch_req, ensure_ascii=False) + "\n")
            count += 1

    print(f"Built {count} requests for {model_name}", flush=True)

    # Submit
    with open(batch_file, "rb") as f:
        resp = httpx.post(
            "https://api.anthropic.com/v1/messages/batches",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "anthropic-beta": "message-batches-2024-09-24",
            },
            files={"file": ("batch.jsonl", f, "application/jsonl")},
            timeout=60,
        )

    if resp.status_code in (200, 201):
        batch_data = resp.json()
        batch_id = batch_data.get("id", "")
        print(f"Submitted: {batch_id}", flush=True)
        with open(os.path.join(analysis_dir, f"{model_name}_batch_id.txt"), "w") as f:
            f.write(batch_id)
    else:
        print(f"Failed: {resp.status_code} — {resp.text[:300]}", flush=True)


def cmd_submit_gpt4o():
    load_env()
    import openai
    client = openai.OpenAI()
    results_file, run_dir = find_results()
    results = load_results(results_file)
    items = get_pred_items(results)
    analysis_dir = os.path.join(run_dir, "analysis")
    os.makedirs(analysis_dir, exist_ok=True)

    # Build JSONL
    batch_file = os.path.join(analysis_dir, "gpt4o_batch_input.jsonl")
    count = 0
    with open(batch_file, "w", encoding="utf-8") as f:
        for qid, cond, held_out, resp_text in items:
            prompt = build_judge_prompt(held_out, resp_text)
            req = {
                "custom_id": f"q{qid}_{cond}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o",
                    "max_tokens": 8,
                    "temperature": 0,
                    "messages": [{"role": "user", "content": prompt}],
                }
            }
            f.write(json.dumps(req) + "\n")
            count += 1

    print(f"Built {count} requests for GPT-4o", flush=True)

    # Submit in chunks (OpenAI has token limits)
    chunk_size = 50
    batch_ids = []
    lines = open(batch_file).readlines()

    for i in range(0, len(lines), chunk_size):
        chunk = lines[i:i+chunk_size]
        chunk_file = os.path.join(analysis_dir, f"gpt4o_chunk_{i//chunk_size}.jsonl")
        with open(chunk_file, "w") as f:
            f.writelines(chunk)

        with open(chunk_file, "rb") as f:
            uploaded = client.files.create(file=f, purpose="batch")
        batch = client.batches.create(
            input_file_id=uploaded.id,
            endpoint="/v1/chat/completions",
            completion_window="24h"
        )
        batch_ids.append(batch.id)
        print(f"  Chunk {i//chunk_size}: {batch.id} ({batch.status})", flush=True)

    with open(os.path.join(analysis_dir, "gpt4o_batch_ids.json"), "w") as f:
        json.dump(batch_ids, f, indent=2)
    print(f"Submitted {len(batch_ids)} chunks", flush=True)


# === SUMMARY ===

def cmd_summary():
    """Print 4-judge comparison table from all available judge results."""
    results_file, run_dir = find_results()
    analysis_dir = os.path.join(run_dir, "analysis")

    judges = {}

    # Load each judge's results
    for judge_name, filename in [
        ("Haiku", "haiku_judgments.json"),
        ("Sonnet", "sonnet_judgments.json"),
        ("Opus", "opus_judgments.json"),
        ("GPT-4o", "gpt4o_judgments.json"),
    ]:
        path = os.path.join(analysis_dir, filename)
        if os.path.exists(path):
            data = json.load(open(path))
            cond_scores = defaultdict(list)
            score_key = [k for k in data[0].keys() if "score" in k and k != "haiku_score"][0] if len(data[0]) > 3 else f"{judge_name.lower()}_score"

            for j in data:
                # Find the score key for this judge
                score = 0
                for k, v in j.items():
                    if "score" in k and isinstance(v, int) and v > 0:
                        score = v
                        break
                if score > 0:
                    cond_scores[j["condition"]].append(score)

            judges[judge_name] = {c: sum(s)/len(s) for c, s in cond_scores.items() if s}

    if not judges:
        print("No judge results found yet.", flush=True)
        return

    print(f"\nFranklin Study — Judge Comparison", flush=True)
    print(f"{'Condition':<25}", end="", flush=True)
    for j in judges:
        print(f" {j:>7}", end="", flush=True)
    if len(judges) > 1:
        print(f" {'Avg':>7}", end="", flush=True)
    print(flush=True)
    print("=" * (25 + 8 * (len(judges) + (1 if len(judges) > 1 else 0))), flush=True)

    rows = []
    all_conds = set()
    for j_scores in judges.values():
        all_conds.update(j_scores.keys())

    for cond in sorted(all_conds):
        vals = [judges[j].get(cond) for j in judges if cond in judges[j]]
        avg = sum(vals) / len(vals) if vals else 0
        rows.append((cond, vals, avg))

    rows.sort(key=lambda r: -r[2])

    for cond, vals, avg in rows:
        print(f"  {cond:<23}", end="", flush=True)
        for j in judges:
            v = judges[j].get(cond)
            print(f" {v:>7.2f}" if v else f" {'—':>7}", end="", flush=True)
        if len(judges) > 1:
            print(f" {avg:>7.2f}", end="", flush=True)
        print(flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=[
        "haiku", "submit-sonnet", "submit-opus", "submit-gpt4o",
        "check", "process-sonnet", "process-opus", "process-gpt4o",
        "summary"
    ])
    args = parser.parse_args()

    if args.command == "haiku":
        cmd_haiku()
    elif args.command == "submit-sonnet":
        cmd_submit_anthropic("sonnet", "claude-sonnet-4-6")
    elif args.command == "submit-opus":
        cmd_submit_anthropic("opus", "claude-opus-4-6")
    elif args.command == "submit-gpt4o":
        cmd_submit_gpt4o()
    elif args.command == "summary":
        cmd_summary()
    else:
        print(f"TODO: {args.command} not yet implemented", flush=True)


if __name__ == "__main__":
    main()
