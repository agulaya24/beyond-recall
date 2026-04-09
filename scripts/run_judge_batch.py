"""
Memory Systems Study — Sonnet 4.6 Judge via Batch API
Submits all 505 prediction accuracy judgments as a single batch.
50% cost discount, no rate limit concerns.

Usage:
    python run_judge_batch.py submit   # create and submit batch
    python run_judge_batch.py check    # check batch status
    python run_judge_batch.py process  # process completed batch results
"""

import json
import os
import sys
import subprocess
import time
import argparse
from collections import defaultdict

import httpx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(BASE_DIR, "results", "run_20260409_182743", "results_merged.json")
ANALYSIS_DIR = os.path.join(BASE_DIR, "results", "run_20260409_182743", "analysis")
BATCH_FILE = os.path.join(ANALYSIS_DIR, "sonnet_batch_input.jsonl")
BATCH_ID_FILE = os.path.join(ANALYSIS_DIR, "sonnet_batch_id.txt")

JUDGE_MODEL = "claude-sonnet-4-6"


def load_env():
    for k in ["ANTHROPIC_API_KEY"]:
        r = subprocess.run(
            ["powershell", "-Command",
             f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
            capture_output=True, text=True
        )
        val = r.stdout.strip()
        if val:
            os.environ[k] = val


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


CONDITIONS = [
    "C1_mem0", "C1_letta", "C1_supermemory", "C1_zep",
    "C2a_spec_only", "C2c_wrong_spec",
    "C3_mem0", "C3_letta", "C3_supermemory", "C3_zep",
    "C4_factdump", "C5_baseline", "C6_random",
]


def cmd_submit():
    """Build JSONL and submit batch."""
    load_env()
    api_key = os.environ["ANTHROPIC_API_KEY"]

    with open(RESULTS_FILE, encoding="utf-8") as f:
        results = json.load(f)

    pred_qs = [r for r in results
               if r.get("held_out_passage") and r["tier"] == "behavioral_prediction"]

    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    # Build JSONL
    count = 0
    with open(BATCH_FILE, "w", encoding="utf-8") as f:
        for r in pred_qs:
            qid = r["question_id"]
            held_out = r["held_out_passage"]
            for cond in CONDITIONS:
                resp = r.get("responses", {}).get(cond, {})
                resp_text = resp.get("text", "")
                if not resp_text:
                    continue

                custom_id = f"q{qid}_{cond}"
                prompt = build_judge_prompt(held_out, resp_text)

                batch_req = {
                    "custom_id": custom_id,
                    "params": {
                        "model": JUDGE_MODEL,
                        "max_tokens": 8,
                        "temperature": 0,
                        "messages": [{"role": "user", "content": prompt}],
                    }
                }
                f.write(json.dumps(batch_req, ensure_ascii=False) + "\n")
                count += 1

    print(f"Built {count} requests in {BATCH_FILE}", flush=True)

    # Submit batch
    with open(BATCH_FILE, "rb") as f:
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
        print(f"Batch submitted: {batch_id}", flush=True)
        print(f"Status: {batch_data.get('processing_status', '')}", flush=True)
        with open(BATCH_ID_FILE, "w") as f:
            f.write(batch_id)
    else:
        print(f"Submit failed: {resp.status_code}", flush=True)
        print(resp.text[:500], flush=True)


def cmd_check():
    """Check batch status."""
    load_env()
    api_key = os.environ["ANTHROPIC_API_KEY"]

    with open(BATCH_ID_FILE) as f:
        batch_id = f.read().strip()

    resp = httpx.get(
        f"https://api.anthropic.com/v1/messages/batches/{batch_id}",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "message-batches-2024-09-24",
        },
        timeout=30,
    )
    data = resp.json()
    print(f"Batch: {batch_id}", flush=True)
    print(f"Status: {data.get('processing_status', 'unknown')}", flush=True)
    counts = data.get("request_counts", {})
    print(f"Processing: {counts.get('processing', 0)}", flush=True)
    print(f"Succeeded: {counts.get('succeeded', 0)}", flush=True)
    print(f"Errored: {counts.get('errored', 0)}", flush=True)
    return data.get("processing_status", "")


def cmd_process():
    """Download and process batch results."""
    load_env()
    api_key = os.environ["ANTHROPIC_API_KEY"]

    with open(BATCH_ID_FILE) as f:
        batch_id = f.read().strip()

    # Download results
    resp = httpx.get(
        f"https://api.anthropic.com/v1/messages/batches/{batch_id}/results",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "message-batches-2024-09-24",
        },
        timeout=120,
    )

    if resp.status_code != 200:
        print(f"Download failed: {resp.status_code} — {resp.text[:300]}", flush=True)
        return

    # Parse JSONL results
    lines = resp.text.strip().split("\n")
    print(f"Downloaded {len(lines)} results", flush=True)

    # Load Haiku scores for comparison
    haiku_file = os.path.join(ANALYSIS_DIR, "prediction_judgments.json")
    with open(haiku_file, encoding="utf-8") as f:
        haiku_j = json.load(f)
    haiku_lookup = {(j["question_id"], j["condition"]): j["score"] for j in haiku_j}

    # Parse results
    all_judgments = []
    for line in lines:
        data = json.loads(line)
        custom_id = data.get("custom_id", "")
        result = data.get("result", {})

        # Parse custom_id: q21_C1_mem0
        parts = custom_id.split("_", 1)
        qid = int(parts[0][1:])  # strip 'q'
        cond = parts[1]

        # Extract score
        score = 0
        if result.get("type") == "succeeded":
            msg = result.get("message", {})
            content = msg.get("content", [{}])
            if content:
                txt = content[0].get("text", "").strip()
                if txt and txt[0].isdigit():
                    score = int(txt[0])

        h_score = haiku_lookup.get((qid, cond), 0)
        all_judgments.append({
            "question_id": qid,
            "condition": cond,
            "sonnet_score": score,
            "haiku_score": h_score,
        })

    # Analysis
    valid = [j for j in all_judgments if j["sonnet_score"] > 0 and j["haiku_score"] > 0]
    exact = sum(1 for j in valid if j["sonnet_score"] == j["haiku_score"])
    within1 = sum(1 for j in valid if abs(j["sonnet_score"] - j["haiku_score"]) <= 1)

    print(f"\n=== INTER-RATER RELIABILITY (Haiku vs Sonnet 4.6) ===", flush=True)
    print(f"Valid pairs: {len(valid)}/{len(all_judgments)}", flush=True)
    print(f"Exact agreement: {exact}/{len(valid)} ({exact/len(valid)*100:.1f}%)", flush=True)
    print(f"Within 1 point:  {within1}/{len(valid)} ({within1/len(valid)*100:.1f}%)", flush=True)

    # Per-condition averages
    s_by_c = defaultdict(list)
    h_by_c = defaultdict(list)
    for j in valid:
        s_by_c[j["condition"]].append(j["sonnet_score"])
        h_by_c[j["condition"]].append(j["haiku_score"])

    print(f"\n{'':20s} {'Haiku':>7s} {'Sonnet':>7s} {'Diff':>6s}", flush=True)
    for c in CONDITIONS:
        if s_by_c[c] and h_by_c[c]:
            h = sum(h_by_c[c]) / len(h_by_c[c])
            s = sum(s_by_c[c]) / len(s_by_c[c])
            print(f"  {c:18s} {h:7.2f} {s:7.2f} {s-h:+6.2f}", flush=True)

    # Rank correlation
    h_avgs = {c: sum(h_by_c[c]) / len(h_by_c[c]) for c in CONDITIONS if h_by_c[c]}
    s_avgs = {c: sum(s_by_c[c]) / len(s_by_c[c]) for c in CONDITIONS if s_by_c[c]}
    common = sorted(set(h_avgs) & set(s_avgs))
    h_ranked = sorted(common, key=lambda c: h_avgs[c], reverse=True)
    s_ranked = sorted(common, key=lambda c: s_avgs[c], reverse=True)
    h_rank = {c: i + 1 for i, c in enumerate(h_ranked)}
    s_rank = {c: i + 1 for i, c in enumerate(s_ranked)}
    n = len(common)
    d_sq = sum((h_rank[c] - s_rank[c]) ** 2 for c in common)
    rho = 1 - (6 * d_sq) / (n * (n ** 2 - 1))
    print(f"\nSpearman rank correlation: rho={rho:.3f} (n={n})", flush=True)

    print(f"\nRank comparison:", flush=True)
    print(f"  {'':20s} {'H_rank':>7s} {'S_rank':>7s}", flush=True)
    for c in h_ranked:
        print(f"  {c:20s} {h_rank[c]:7d} {s_rank[c]:7d}", flush=True)

    # Save
    with open(os.path.join(ANALYSIS_DIR, "sonnet_judgments.json"), "w", encoding="utf-8") as f:
        json.dump(all_judgments, f, indent=2, ensure_ascii=False)

    sonnet_summary = {}
    for c in CONDITIONS:
        scores = s_by_c.get(c, [])
        if scores:
            sonnet_summary[c] = {
                "avg_score": round(sum(scores) / len(scores), 2),
                "n": len(scores),
                "score_dist": {str(i): scores.count(i) for i in range(1, 6)},
            }
    with open(os.path.join(ANALYSIS_DIR, "sonnet_prediction_summary.json"), "w", encoding="utf-8") as f:
        json.dump(sonnet_summary, f, indent=2)

    print(f"\nSaved to {ANALYSIS_DIR}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["submit", "check", "process"])
    args = parser.parse_args()

    if args.command == "submit":
        cmd_submit()
    elif args.command == "check":
        cmd_check()
    elif args.command == "process":
        cmd_process()


if __name__ == "__main__":
    main()
