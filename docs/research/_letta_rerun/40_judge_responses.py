"""Part 5: Judge the BL-C2a-named responses with 7 judges:
   haiku, sonnet, opus, gpt4o, gpt54, gemini_flash, gemini_pro.
Same judge prompt as paper (see scripts/run_baselayer_condition.py).
"""
import json
import os
import re
import sys
import subprocess
import time
import httpx

OUT_DIR = r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun"

# Load API keys from user env
for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"):
    r = subprocess.run(["powershell", "-Command",
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    val = r.stdout.strip()
    if val:
        os.environ[k] = val

API_KEYS = {
    "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
    "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
}
for k, v in API_KEYS.items():
    if not v:
        print(f"WARNING: {k} not set")


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


def api_call_openai(model, prompt, max_tokens=8):
    resp = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        json={"model": model, "max_completion_tokens": max_tokens, "temperature": 0,
              "messages": [{"role": "user", "content": prompt}]},
        headers={"Authorization": f"Bearer {API_KEYS['OPENAI_API_KEY']}",
                 "Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def api_call_gemini(model, prompt):
    for attempt in range(3):
        try:
            resp = httpx.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEYS['GEMINI_API_KEY']}",
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=60,
            )
            if resp.status_code == 429:
                time.sleep(2 ** (attempt + 2))
                continue
            resp.raise_for_status()
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


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


def run_judge(judge_name, prompt):
    """Returns (score, raw, parse_failure, error_msg)."""
    try:
        if judge_name == "haiku":
            raw = api_call_anthropic("claude-haiku-4-5-20251001", prompt, timeout=30)
        elif judge_name == "sonnet":
            raw = api_call_anthropic("claude-sonnet-4-6", prompt, timeout=30)
        elif judge_name == "opus":
            raw = api_call_anthropic("claude-opus-4-6", prompt, timeout=60)
        elif judge_name == "gpt4o":
            raw = api_call_openai("gpt-4o", prompt)
        elif judge_name == "gpt54":
            raw = api_call_openai("gpt-5.4", prompt)
        elif judge_name == "gemini_flash":
            raw = api_call_gemini("gemini-2.5-flash", prompt)
        elif judge_name == "gemini_pro":
            raw = api_call_gemini("gemini-2.5-pro", prompt)
        else:
            raise ValueError(f"Unknown judge: {judge_name}")
    except Exception as e:
        return 0, "", True, str(e)
    score = parse_score(raw)
    return score, raw, score == 0, ""


JUDGES = ["haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"]


for subject in ("ebers", "babur"):
    responses_path = os.path.join(OUT_DIR, f"{subject}_bl_c2a_named_responses.json")
    with open(responses_path, encoding="utf-8") as f:
        resp_data = json.load(f)
    responses = resp_data["results"]
    print(f"\n=== {subject}: judging {len(responses)} responses across {len(JUDGES)} judges ===")

    for judge_name in JUDGES:
        out_path = os.path.join(OUT_DIR, f"{subject}_judgments_{judge_name}.json")
        if os.path.exists(out_path):
            with open(out_path, encoding="utf-8") as f:
                existing = json.load(f)
            if len(existing) >= len(responses):
                non_zero = sum(1 for r in existing if r.get("score", 0) >= 1)
                print(f"  [{judge_name}] already complete (n={len(existing)}, non-zero={non_zero}). Skipping.")
                continue

        print(f"  [{judge_name}] judging...")
        out = []
        for r in responses:
            qid = r["question_id"]
            ho = r["held_out_passage"] or ""
            rt = r["response"] or ""
            if not ho or not rt:
                out.append({"question_id": qid, "score": 0, "error": "missing held_out or response", "parse_failure": True})
                continue
            prompt = judge_prompt(ho, rt)
            score, raw, pf, err = run_judge(judge_name, prompt)
            out.append({
                "question_id": qid,
                "condition": f"BL_C2a_named_{subject}",
                "judge": judge_name,
                "score": score,
                "raw": raw,
                "error": err,
                "parse_failure": pf,
            })
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        non_zero = sum(1 for x in out if x["score"] >= 1)
        mean = sum(x["score"] for x in out if x["score"] >= 1) / max(non_zero, 1)
        print(f"  [{judge_name}] n={len(out)} valid={non_zero} mean={mean:.3f} -> {out_path}")
