"""Step 4: Judge full-stack-named BL responses with the 5-judge primary panel:
   haiku, sonnet, opus, gpt4o, gpt54.

Uses the SAME judge prompt as 40_judge_responses.py (scripts/run_baselayer_condition.py).
Resumable: after each question's judgment, atomically overwrites the per-subject-per-judge JSON.
If a single call fails twice, log and continue (no block).

Output: _letta_rerun/fullstack_named/{subject}_fullstack_judgments_{judge}.json
"""
import json
import os
import re
import subprocess
import sys
import time
import httpx

OUT_DIR = r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\fullstack_named"

# Load API keys from user env
for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
    r = subprocess.run(["powershell", "-Command",
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    val = r.stdout.strip()
    if val:
        os.environ[k] = val

API_KEYS = {
    "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
}
for k, v in API_KEYS.items():
    if not v:
        print(f"WARNING: {k} not set", file=sys.stderr)


# Same short-form prompt as 40_judge_responses.py (which matches the main study judge prompt)
def judge_prompt(held_out, response_text):
    return (
        "You are evaluating whether a response about a person PREDICTED "
        "what actually happened.\n\n"
        "=== HELD-OUT GROUND TRUTH ===\n" + held_out + "\n\n"
        "=== RESPONSE ===\n" + response_text[:1500] + "\n\n"
        "Rate 1-5:\n5=Predicts specific outcome\n4=General direction correct\n"
        "3=Right domain wrong outcome\n2=Wrong prediction\n1=Refuses or off-base\n\n"
        "Respond with ONLY a single digit (1-5)."
    )


def parse_score(text):
    if not text:
        return 0
    m = re.search(r"[1-5]", text.strip())
    return int(m.group()) if m else 0


def api_call_anthropic(model, prompt, max_tokens=8, timeout=30):
    resp = httpx.post(
        "https://api.anthropic.com/v1/messages",
        json={"model": model, "max_tokens": max_tokens, "temperature": 0,
              "messages": [{"role": "user", "content": prompt}]},
        headers={"x-api-key": API_KEYS["ANTHROPIC_API_KEY"],
                 "anthropic-version": "2023-06-01", "content-type": "application/json"},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]


def api_call_openai(model, prompt, max_tokens_key="max_tokens", max_tokens=8):
    payload = {"model": model, max_tokens_key: max_tokens, "temperature": 0,
               "messages": [{"role": "user", "content": prompt}]}
    resp = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        json=payload,
        headers={"Authorization": f"Bearer {API_KEYS['OPENAI_API_KEY']}",
                 "Content-Type": "application/json"},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def run_judge_call(judge_name, prompt):
    """Returns (score, raw, parse_failure, error_msg)."""
    try:
        if judge_name == "haiku":
            raw = api_call_anthropic("claude-haiku-4-5-20251001", prompt, timeout=30)
        elif judge_name == "sonnet":
            raw = api_call_anthropic("claude-sonnet-4-6", prompt, timeout=30)
        elif judge_name == "opus":
            raw = api_call_anthropic("claude-opus-4-6", prompt, timeout=60)
        elif judge_name == "gpt4o":
            raw = api_call_openai("gpt-4o", prompt, "max_tokens", 8)
        elif judge_name == "gpt54":
            raw = api_call_openai("gpt-5.4", prompt, "max_completion_tokens", 8)
        else:
            raise ValueError(f"Unknown judge: {judge_name}")
    except Exception as e:
        return 0, "", True, str(e)[:500]
    score = parse_score(raw)
    return score, raw, score == 0, ""


def with_retries(judge_name, prompt, retries=2):
    """Retry once on transient failure; return final result tuple."""
    last = None
    for attempt in range(retries + 1):
        score, raw, pf, err = run_judge_call(judge_name, prompt)
        last = (score, raw, pf, err)
        if not pf and not err:
            return last
        # Retry on obvious transient: rate limit / 5xx
        if err and any(s in err for s in ("429", "529", "503", "502", "500", "ReadTimeout", "ConnectError", "WriteTimeout")):
            time.sleep(2 ** (attempt + 1))
            continue
        # Parse failure but no error => rare; try once more
        if pf and attempt < retries:
            time.sleep(1)
            continue
        break
    return last


def atomic_write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    if os.path.exists(path):
        os.replace(tmp, path)
    else:
        os.rename(tmp, path)


JUDGES = ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]
SUBJECTS = ("hamerton", "ebers", "babur")


def main():
    for subject in SUBJECTS:
        responses_path = os.path.join(OUT_DIR, f"{subject}_bl_c2a_fullstack_responses.json")
        if not os.path.exists(responses_path):
            print(f"[{subject}] responses missing at {responses_path} — skipping.")
            continue
        with open(responses_path, encoding="utf-8") as f:
            resp_data = json.load(f)
        responses = resp_data["results"]
        print(f"\n=== {subject}: judging {len(responses)} responses across {len(JUDGES)} judges ===")

        for judge_name in JUDGES:
            out_path = os.path.join(OUT_DIR, f"{subject}_fullstack_judgments_{judge_name}.json")
            # Resume: load existing, skip qids already valid
            existing_by_qid = {}
            if os.path.exists(out_path):
                with open(out_path, encoding="utf-8") as f:
                    prior = json.load(f)
                for e in prior:
                    qid = e.get("question_id")
                    if qid is not None and e.get("score", 0) >= 1 and not e.get("parse_failure"):
                        existing_by_qid[qid] = e

            print(f"  [{judge_name}] {len(existing_by_qid)}/{len(responses)} cached, judging...")
            out = list(existing_by_qid.values())
            # Pre-write resumable file
            atomic_write_json(out_path, out)

            for r in responses:
                qid = r["question_id"]
                if qid in existing_by_qid:
                    continue
                ho = r.get("held_out_passage") or ""
                rt = r.get("response") or ""
                if not ho or not rt:
                    out.append({"question_id": qid, "condition": f"BL_C2a_fullstack_named_{subject}",
                                "judge": judge_name, "score": 0, "error": "missing held_out or response",
                                "parse_failure": True})
                    atomic_write_json(out_path, out)
                    continue
                prompt = judge_prompt(ho, rt)
                score, raw, pf, err = with_retries(judge_name, prompt, retries=2)
                out.append({
                    "question_id": qid,
                    "condition": f"BL_C2a_fullstack_named_{subject}",
                    "judge": judge_name,
                    "score": score,
                    "raw": (raw or "")[:100],
                    "error": err,
                    "parse_failure": pf,
                })
                atomic_write_json(out_path, out)
                if err:
                    print(f"    Q{qid:02d} FAIL ({judge_name}): {err[:120]}")
                # tiny rate-limit breath
                time.sleep(0.05)

            valid = [x for x in out if x.get("score", 0) >= 1 and not x.get("parse_failure")]
            mean = sum(x["score"] for x in valid) / len(valid) if valid else 0.0
            print(f"  [{judge_name}] done n={len(out)} valid={len(valid)} mean={mean:.3f} -> {out_path}")


if __name__ == "__main__":
    main()
