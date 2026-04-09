"""
Franklin Replication Study — Raw HTTP runner (no SDK init hangs).
Known-figure test with C7 named baseline and C4a (all facts + spec).

Conditions (11 from this runner, Letta/Zep run standalone):
  C1_mem0, C1_supermemory              — memory system retrieval (facts only)
  C2a_spec_only                        — behavioral spec, no facts
  C2c_wrong_spec                       — Hamerton's spec on Franklin's questions
  C3_mem0, C3_supermemory              — spec + memory system facts
  C4_factdump                          — all facts, no spec
  C4a_factdump_plus_spec               — all facts + spec
  C5_baseline                          — nothing (anonymous)
  C6_random                            — 10 random facts
  C7_named_baseline                    — "This is Benjamin Franklin"
"""

import json
import os
import sys
import time
import random
import hashlib
import subprocess
from datetime import datetime, timezone

import requests
import httpx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACTS_FILE = os.path.join(BASE_DIR, "franklin_shared_facts.json")

# Franklin spec = correct spec
SPEC_FILE = os.path.normpath(os.path.join(
    BASE_DIR, "..", "..", "..", "..",
    "subjects", "franklin_memory", "data", "identity_layers", "brief_v5_clean.md"
))
# Hamerton spec = wrong spec (role reversal)
WRONG_SPEC_FILE = os.path.normpath(os.path.join(
    BASE_DIR, "..", "..", "..", "..",
    "hamerton_memory", "data", "identity_layers", "brief_v5_clean.md"
))

RESPONSE_MODEL = "claude-haiku-4-5-20251001"
RESPONSE_TEMPERATURE = 0
RESPONSE_MAX_TOKENS = 1024


def load_env():
    keys = {}
    for k in ["MEM0_KEY", "SUPERMEMORY_KEY", "ANTHROPIC_API_KEY"]:
        r = subprocess.run(
            ["powershell", "-Command",
             f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
            capture_output=True, text=True
        )
        val = r.stdout.strip()
        if val:
            os.environ[k] = val
            keys[k] = f"SET ({len(val)}c)"
        else:
            keys[k] = "NOT SET"
    return keys


# === Raw HTTP retrievers ===

def mem0_search(query, top_k=10):
    resp = requests.post(
        "https://api.mem0.ai/v1/memories/search/",
        json={"query": query, "user_id": "franklin_study_v1", "limit": top_k},
        headers={"Authorization": f"Token {os.environ['MEM0_KEY']}"},
        timeout=15,
    )
    if resp.status_code != 200:
        return []
    data = resp.json()
    if isinstance(data, list):
        return [{"text": r.get("memory", ""), "score": r.get("score", 0)} for r in data[:top_k]]
    results = data.get("results", data.get("memories", []))
    return [{"text": r.get("memory", r.get("text", "")), "score": r.get("score", 0)} for r in results[:top_k]]


def supermemory_search(query, top_k=10):
    resp = requests.post(
        "https://api.supermemory.ai/v3/search",
        json={"q": query, "limit": top_k, "containerTags": ["franklin_study_v1"]},
        headers={
            "Authorization": f"Bearer {os.environ['SUPERMEMORY_KEY']}",
            "Content-Type": "application/json",
        },
        timeout=15,
    )
    if resp.status_code != 200:
        return []
    data = resp.json()
    results = data.get("results", [])
    out = []
    for r in results[:top_k]:
        chunks = r.get("chunks", [])
        if chunks:
            best = chunks[0]
            out.append({"text": best.get("content", ""), "score": best.get("score", 0)})
        else:
            out.append({"text": r.get("memory", r.get("content", "")), "score": r.get("similarity", 0)})
    return out


RETRIEVERS = {
    "mem0": mem0_search,
    "supermemory": supermemory_search,
}


# === Response generation ===

def build_system_prompt(context_type, context_content, spec_text=None):
    if context_type == "spec_only":
        return (
            "The following is a behavioral specification describing your user — "
            "how they think, decide, and act.\n\n"
            f"=== BEHAVIORAL SPECIFICATION ===\n{spec_text}"
        )
    if context_type == "spec_plus_facts":
        facts_text = "\n".join(f"- {f}" for f in context_content)
        return (
            "The following is a behavioral specification describing your user — "
            "how they think, decide, and act. You also have a set of retrieved "
            "facts about this person.\n\n"
            f"=== BEHAVIORAL SPECIFICATION ===\n{spec_text}\n\n"
            f"=== RETRIEVED FACTS ===\n{facts_text}"
        )
    if context_type == "facts":
        facts_text = "\n".join(f"- {f}" for f in context_content)
        return (
            "The following facts are available about the person this question "
            f"concerns.\n\n=== FACTS ===\n{facts_text}"
        )
    if context_type == "all_facts":
        facts_text = "\n".join(f"- {f}" for f in context_content)
        return (
            "The following is a complete set of known facts about the person "
            f"this question concerns.\n\n=== FACTS ===\n{facts_text}"
        )
    if context_type == "all_facts_plus_spec":
        facts_text = "\n".join(f"- {f}" for f in context_content)
        return (
            "The following is a behavioral specification describing your user — "
            "how they think, decide, and act. You also have the complete set of "
            "known facts about this person.\n\n"
            f"=== BEHAVIORAL SPECIFICATION ===\n{spec_text}\n\n"
            f"=== ALL KNOWN FACTS ===\n{facts_text}"
        )
    if context_type == "raw_corpus":
        return (
            "The following is the full text of an autobiography. Use it to "
            "answer the question that follows.\n\n"
            f"=== AUTOBIOGRAPHY TEXT ===\n{context_content}"
        )
    if context_type == "named_baseline":
        return (
            "The following question is about Benjamin Franklin, "
            "the American statesman, inventor, writer, and polymath (1706-1790). "
            "Answer using your knowledge of Franklin."
        )
    if context_type == "baseline":
        return "Answer the following question."
    return "Answer the following question."


def generate_response(api_key, question, system_prompt):
    resp = httpx.post(
        "https://api.anthropic.com/v1/messages",
        json={
            "model": RESPONSE_MODEL,
            "max_tokens": RESPONSE_MAX_TOKENS,
            "temperature": RESPONSE_TEMPERATURE,
            "system": system_prompt,
            "messages": [{"role": "user", "content": question}],
        },
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        "text": data["content"][0]["text"],
        "input_tokens": data["usage"]["input_tokens"],
        "output_tokens": data["usage"]["output_tokens"],
        "model": RESPONSE_MODEL,
    }


def main():
    print("=== Franklin Replication Study ===", flush=True)
    keys = load_env()
    for k, v in keys.items():
        print(f"  {k}: {v}", flush=True)

    # Load data
    with open(os.path.join(BASE_DIR, "battery", "questions_80_franklin.json"), encoding="utf-8") as f:
        questions = json.load(f)["questions"]
    with open(FACTS_FILE, encoding="utf-8") as f:
        facts_data = json.load(f)
    fact_texts = [f["text"] for f in facts_data["facts"]]
    with open(SPEC_FILE, encoding="utf-8") as f:
        spec_text = f.read()
    with open(WRONG_SPEC_FILE, encoding="utf-8") as f:
        wrong_spec_text = f.read()

    # Load raw training corpus for C9
    corpus_file = os.path.join(BASE_DIR, "corpus", "tiers", "tier_02_franklin_ch00-10.txt")
    with open(corpus_file, encoding="utf-8") as f:
        raw_corpus = f.read()

    print(f"\n  Questions: {len(questions)}", flush=True)
    print(f"  Facts: {len(fact_texts)}", flush=True)
    print(f"  Spec: {len(spec_text.split())}w (Franklin)", flush=True)
    print(f"  Wrong spec: {len(wrong_spec_text.split())}w (Hamerton)", flush=True)
    print(f"  Raw corpus: {len(raw_corpus.split())}w", flush=True)

    # Test retrievers
    print("\n=== Testing Retrievers ===", flush=True)
    active = {}
    for name, fn in RETRIEVERS.items():
        try:
            r = fn("test query", top_k=2)
            print(f"  {name}: OK ({len(r)} results)", flush=True)
            active[name] = fn
        except Exception as e:
            print(f"  {name}: FAILED — {e}", flush=True)

    # Output dir
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_id = f"run_franklin_{timestamp}"
    output_dir = os.path.join(BASE_DIR, "results", run_id)
    os.makedirs(output_dir, exist_ok=True)
    cp_file = os.path.join(output_dir, "checkpoint.json")

    if os.path.exists(cp_file):
        with open(cp_file, encoding="utf-8") as f:
            checkpoint = json.load(f)
        completed = set(checkpoint["completed_ids"])
        print(f"  Resuming: {len(completed)} done", flush=True)
    else:
        checkpoint = {"completed_ids": [], "results": []}
        completed = set()

    api_key = os.environ["ANTHROPIC_API_KEY"]
    random.seed(42)
    total_input = 0
    total_output = 0

    print(f"\n=== Running {len(questions)} questions ===", flush=True)
    print(f"  Output: {output_dir}", flush=True)

    for q_idx, q in enumerate(questions):
        q_id = q["id"]
        if q_id in completed:
            continue

        q_text = q["text"]
        print(f"\n{'='*60}", flush=True)
        print(f"[{q_idx+1}/{len(questions)}] Q{q_id} ({q['tier']}/{q.get('category','')})", flush=True)
        print(f"  {q_text[:70]}...", flush=True)

        q_result = {
            "question_id": q_id,
            "question_text": q_text,
            "tier": q["tier"],
            "category": q.get("category", ""),
            "held_out_passage": q.get("held_out_passage"),
            "held_out_chapter": q.get("held_out_chapter"),
            "retrieval": {},
            "responses": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Retrieval
        for name, fn in active.items():
            try:
                t0 = time.time()
                retrieved = fn(q_text, top_k=10)
                elapsed = time.time() - t0
                q_result["retrieval"][name] = {
                    "facts": [r["text"] for r in retrieved],
                    "scores": [r["score"] for r in retrieved],
                    "count": len(retrieved),
                    "latency_ms": round(elapsed * 1000),
                }
                print(f"  {name:15s} {len(retrieved):2d} facts ({elapsed:.1f}s)", flush=True)
            except Exception as e:
                print(f"  {name:15s} FAILED: {e}", flush=True)
                q_result["retrieval"][name] = {"error": str(e), "facts": [], "count": 0}

        def run_cond(cond_name, prompt):
            nonlocal total_input, total_output
            try:
                t0 = time.time()
                resp = generate_response(api_key, q_text, prompt)
                elapsed = time.time() - t0
                resp["latency_ms"] = round(elapsed * 1000)
                q_result["responses"][cond_name] = resp
                total_input += resp["input_tokens"]
                total_output += resp["output_tokens"]
                print(f"  {cond_name:25s} {resp['output_tokens']:4d}t ({elapsed:.1f}s)", flush=True)
            except Exception as e:
                print(f"  {cond_name:25s} FAILED: {e}", flush=True)
                q_result["responses"][cond_name] = {"error": str(e)}

        # C1: Memory system facts only
        for name in active:
            facts = q_result["retrieval"].get(name, {}).get("facts", [])
            if facts:
                run_cond(f"C1_{name}", build_system_prompt("facts", facts))

        # C2a: Spec only (Franklin)
        run_cond("C2a_spec_only", build_system_prompt("spec_only", None, spec_text=spec_text))

        # C2c: Wrong spec (Hamerton on Franklin)
        run_cond("C2c_wrong_spec", build_system_prompt("spec_only", None, spec_text=wrong_spec_text))

        # C3: Spec + retrieved facts
        for name in active:
            facts = q_result["retrieval"].get(name, {}).get("facts", [])
            if facts:
                run_cond(f"C3_{name}", build_system_prompt("spec_plus_facts", facts, spec_text=spec_text))

        # C4: All facts, no spec
        run_cond("C4_factdump", build_system_prompt("all_facts", fact_texts))

        # C4a: All facts + spec
        run_cond("C4a_factdump_plus_spec", build_system_prompt("all_facts_plus_spec", fact_texts, spec_text=spec_text))

        # C5: Baseline (anonymous)
        run_cond("C5_baseline", build_system_prompt("baseline", None))

        # C6: Random facts
        rand_facts = random.sample(fact_texts, min(10, len(fact_texts)))
        q_result["C6_random_facts"] = rand_facts
        run_cond("C6_random", build_system_prompt("facts", rand_facts))

        # C7: Named baseline
        run_cond("C7_named_baseline", build_system_prompt("named_baseline", None))

        # C9: Raw corpus in context (full training text, no extraction)
        run_cond("C9_raw_corpus", build_system_prompt("raw_corpus", raw_corpus))

        # Checkpoint
        checkpoint["results"].append(q_result)
        checkpoint["completed_ids"].append(q_id)
        with open(cp_file, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)

    # Final
    input_cost = total_input * 0.80 / 1_000_000
    output_cost = total_output * 4.00 / 1_000_000
    total_cost = input_cost + output_cost

    print(f"\n{'='*60}", flush=True)
    print(f"COMPLETE — {len(checkpoint['results'])} questions", flush=True)
    print(f"TOKENS: {total_input:,} input + {total_output:,} output", flush=True)
    print(f"COST: ${total_cost:.2f}", flush=True)

    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(checkpoint["results"], f, indent=2, ensure_ascii=False)

    manifest = {
        "run_id": run_id,
        "subject": "Benjamin Franklin",
        "study_type": "franklin_replication",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_questions": len(checkpoint["results"]),
        "total_facts": len(fact_texts),
        "spec_file": SPEC_FILE,
        "wrong_spec_file": WRONG_SPEC_FILE,
        "wrong_spec_subject": "Philip Gilbert Hamerton",
        "response_model": RESPONSE_MODEL,
        "conditions": [
            "C1_mem0", "C1_supermemory",
            "C2a_spec_only", "C2c_wrong_spec",
            "C3_mem0", "C3_supermemory",
            "C4_factdump", "C4a_factdump_plus_spec",
            "C5_baseline", "C6_random", "C7_named_baseline",
            "C9_raw_corpus",
        ],
        "estimated_cost_usd": round(total_cost, 2),
    }
    with open(os.path.join(output_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    if os.path.exists(cp_file):
        os.remove(cp_file)
    print(f"\nSaved to {output_dir}", flush=True)


if __name__ == "__main__":
    main()
