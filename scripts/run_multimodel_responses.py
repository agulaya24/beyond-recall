"""
Multi-model response generation — run key conditions with GPT-4.1, Gemini Flash, and Sonnet.
Uses full layer stack spec. Reuses existing retrieval data.

Usage:
    python run_multimodel_responses.py --model gpt41 --subject hamerton
    python run_multimodel_responses.py --model gemini --subject all
    python run_multimodel_responses.py --model sonnet --subject all
"""
import json, os, sys, time, subprocess, random, argparse, httpx, pathlib
from datetime import datetime, timezone
from collections import defaultdict
from glob import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# NOTE: the subject memory environments (hamerton_memory, franklin_clean_memory,
# subjects/franklin_memory) live outside this repo. Set ANTHROPIC_ROOT to the
# directory that contains them; defaults to empty so a missing path is obvious.
ANTHROPIC_ROOT = os.environ.get("ANTHROPIC_ROOT", "")

# Load env
for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GEMINI_API_KEY']:
    r = subprocess.run(['powershell', '-Command',
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    val = r.stdout.strip()
    if val: os.environ[k] = val


def load_full_spec(layers_dir):
    layers_dir = pathlib.Path(layers_dir)
    sections = []
    for layer_name, filename in [
        ("ANCHORS", "anchors_v4.md"), ("CORE", "core_v4.md"),
        ("PREDICTIONS", "predictions_v4.md"),
    ]:
        filepath = layers_dir / filename
        if not filepath.exists(): continue
        content = filepath.read_text(encoding="utf-8")
        marker = "## Injectable Block"
        idx = content.find(marker)
        block = content[idx + len(marker):].strip() if idx >= 0 else content.strip()
        sections.append(f"## {layer_name}\n\n{block}")
    brief_file = layers_dir / "brief_v5_clean.md"
    if brief_file.exists():
        content = brief_file.read_text(encoding="utf-8")
        marker = "## Injectable Block"
        idx = content.find(marker)
        block = content[idx + len(marker):].strip() if idx >= 0 else content.strip()
        sections.append(f"## UNIFIED BRIEF\n\n{block}")
    return "\n\n".join(sections)


# Model adapters
def gen_sonnet(question, system_prompt):
    resp = httpx.post("https://api.anthropic.com/v1/messages",
        json={"model": "claude-sonnet-4-6", "max_tokens": 1024, "temperature": 0,
              "system": system_prompt,
              "messages": [{"role": "user", "content": question}]},
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                 "anthropic-version": "2023-06-01", "content-type": "application/json"},
        timeout=60)
    resp.raise_for_status()
    d = resp.json()
    return {"text": d["content"][0]["text"],
            "input_tokens": d["usage"]["input_tokens"],
            "output_tokens": d["usage"]["output_tokens"],
            "model": "claude-sonnet-4-6"}


def gen_gpt41(question, system_prompt):
    resp = httpx.post("https://api.openai.com/v1/chat/completions",
        json={"model": "gpt-4.1", "max_tokens": 1024, "temperature": 0,
              "messages": [
                  {"role": "system", "content": system_prompt},
                  {"role": "user", "content": question}
              ]},
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                 "Content-Type": "application/json"},
        timeout=60)
    resp.raise_for_status()
    d = resp.json()
    return {"text": d["choices"][0]["message"]["content"],
            "input_tokens": d["usage"]["prompt_tokens"],
            "output_tokens": d["usage"]["completion_tokens"],
            "model": "gpt-4.1"}


def gen_gemini(question, system_prompt):
    gemini_key = os.environ["GEMINI_API_KEY"]
    # Gemini doesn't have system prompt — prepend to user content
    full_prompt = f"System instructions:\n{system_prompt}\n\nUser question:\n{question}"
    resp = httpx.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}",
        json={"contents": [{"parts": [{"text": full_prompt}]}]},
        timeout=60)
    if resp.status_code == 429:
        time.sleep(15)
        resp = httpx.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}",
            json={"contents": [{"parts": [{"text": full_prompt}]}]},
            timeout=60)
    resp.raise_for_status()
    d = resp.json()
    text = d["candidates"][0]["content"]["parts"][0]["text"]
    usage = d.get("usageMetadata", {})
    return {"text": text,
            "input_tokens": usage.get("promptTokenCount", 0),
            "output_tokens": usage.get("candidatesTokenCount", 0),
            "model": "gemini-2.5-flash"}


MODELS = {
    "sonnet": gen_sonnet,
    "gpt41": gen_gpt41,
    "gemini": gen_gemini,
}

SUBJECTS = {
    "hamerton": {
        "questions": os.path.join(BASE_DIR, "battery", "questions_80.json"),
        "facts": os.path.join(BASE_DIR, "shared_facts.json"),
        "spec_layers_dir": os.path.join(ANTHROPIC_ROOT, "hamerton_memory/data/identity_layers"),
        "mem0_user": "hamerton_study",
    },
    "franklin": {
        "questions": os.path.join(BASE_DIR, "battery", "questions_80_franklin.json"),
        "facts": os.path.join(BASE_DIR, "franklin_shared_facts.json"),
        "spec_layers_dir": os.path.join(ANTHROPIC_ROOT, "franklin_clean_memory/data/identity_layers"),
        "mem0_user": "franklin_study_v1",
    },
    "franklin_obscure": {
        "questions": os.path.join(BASE_DIR, "battery", "questions_80_franklin_obscure.json"),
        "facts": os.path.join(BASE_DIR, "franklin_obscure_shared_facts.json"),
        "spec_layers_dir": os.path.join(ANTHROPIC_ROOT, "subjects/franklin_memory/data/identity_layers"),
        "mem0_user": None,
    },
}


def mem0_search(query, user_id):
    resp = httpx.post("https://api.mem0.ai/v1/memories/search/",
        json={"query": query, "user_id": user_id, "limit": 10},
        headers={"Authorization": f"Token {os.environ.get('MEM0_KEY', '')}"}, timeout=15)
    if resp.status_code != 200: return []
    data = resp.json()
    if isinstance(data, list):
        return [r.get("memory", "") for r in data[:10]]
    return [r.get("memory", r.get("text", "")) for r in data.get("results", data.get("memories", []))[:10]]


def run_subject(model_name, gen_fn, subject_name, cfg):
    questions = json.load(open(cfg["questions"], encoding="utf-8"))["questions"]
    facts_data = json.load(open(cfg["facts"], encoding="utf-8"))
    fact_texts = [f["text"] for f in facts_data["facts"]]
    spec = load_full_spec(cfg["spec_layers_dir"])
    ft_all = "\n".join(f"- {f}" for f in fact_texts)

    print(f"\n{'='*60}", flush=True)
    print(f"{model_name} / {subject_name}", flush=True)
    print(f"  Questions: {len(questions)}, Facts: {len(fact_texts)}, Spec: {len(spec.split())}w", flush=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_id = f"run_{model_name}_{subject_name}_{timestamp}"
    output_dir = os.path.join(BASE_DIR, "results", run_id)
    os.makedirs(output_dir, exist_ok=True)
    cp_file = os.path.join(output_dir, "checkpoint.json")

    if os.path.exists(cp_file):
        checkpoint = json.load(open(cp_file))
        completed = set(checkpoint["completed_ids"])
    else:
        checkpoint = {"completed_ids": [], "results": []}
        completed = set()

    random.seed(42)
    total_in = total_out = 0

    for q_idx, q in enumerate(questions):
        qid = q["id"]
        if qid in completed: continue
        q_text = q["text"]

        q_result = {"question_id": qid, "question_text": q_text, "tier": q["tier"],
                    "category": q.get("category", ""),
                    "held_out_passage": q.get("held_out_passage"),
                    "responses": {}, "timestamp": datetime.now(timezone.utc).isoformat()}

        def run_cond(name, prompt):
            nonlocal total_in, total_out
            try:
                t0 = time.time()
                resp = gen_fn(q_text, prompt)
                elapsed = time.time() - t0
                resp["latency_ms"] = round(elapsed * 1000)
                q_result["responses"][name] = resp
                total_in += resp["input_tokens"]
                total_out += resp["output_tokens"]
                print(f"  {name:30s} {resp['output_tokens']:4d}t ({elapsed:.1f}s)", flush=True)
            except Exception as e:
                q_result["responses"][name] = {"error": str(e)}
                print(f"  {name:30s} FAILED: {e}", flush=True)

        print(f"[{q_idx+1}/{len(questions)}] Q{qid}", flush=True)

        # C2a: Full spec only
        run_cond("C2a_full_spec",
            "The following is a behavioral specification describing your user.\n\n"
            "=== BEHAVIORAL SPECIFICATION ===\n" + spec)

        # C3: Full spec + Mem0 facts
        if cfg["mem0_user"]:
            try:
                facts = mem0_search(q_text, cfg["mem0_user"])
            except:
                facts = []
            if facts:
                ft = "\n".join(f"- {f}" for f in facts)
                run_cond("C3_full_mem0",
                    "The following is a behavioral specification describing your user. "
                    "You also have retrieved facts.\n\n"
                    "=== BEHAVIORAL SPECIFICATION ===\n" + spec + "\n\n"
                    "=== RETRIEVED FACTS ===\n" + ft)

        # C4a: All facts + full spec
        run_cond("C4a_full_all_facts_plus_spec",
            "The following is a behavioral specification describing your user. "
            "You also have the complete set of known facts.\n\n"
            "=== BEHAVIORAL SPECIFICATION ===\n" + spec + "\n\n"
            "=== ALL KNOWN FACTS ===\n" + ft_all)

        # C5: Baseline
        run_cond("C5_baseline", "Answer the following question.")

        # Checkpoint
        checkpoint["results"].append(q_result)
        checkpoint["completed_ids"].append(qid)
        with open(cp_file, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)

        if model_name == "gemini":
            time.sleep(1)  # Rate limit

    # Save
    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(checkpoint["results"], f, indent=2, ensure_ascii=False)
    if os.path.exists(cp_file): os.remove(cp_file)

    manifest = {"run_id": run_id, "response_model": model_name, "subject": subject_name,
                "spec_type": "full_layer_stack", "total_questions": len(checkpoint["results"]),
                "conditions": ["C2a_full_spec", "C3_full_mem0", "C4a_full_all_facts_plus_spec", "C5_baseline"]}
    with open(os.path.join(output_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nDONE — {len(checkpoint['results'])} questions, ${(total_in*2+total_out*10)/1e6:.2f} est", flush=True)
    print(f"Saved to {output_dir}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["sonnet", "gpt41", "gemini"], required=True)
    parser.add_argument("--subject", choices=["hamerton", "franklin", "franklin_obscure", "all"],
                       default="hamerton")
    args = parser.parse_args()

    subjects = ["hamerton", "franklin", "franklin_obscure"] if args.subject == "all" else [args.subject]
    gen_fn = MODELS[args.model]

    print(f"=== Multi-Model Response Generation ===", flush=True)
    print(f"Model: {args.model}, Subjects: {subjects}", flush=True)

    for subject in subjects:
        cfg = SUBJECTS[subject]
        run_subject(args.model, gen_fn, subject, cfg)


if __name__ == "__main__":
    main()
