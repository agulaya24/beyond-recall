"""
Full Layer Stack Re-Run — Uses anchors + core + predictions + brief as the spec.
Runs only spec-dependent conditions: C2a_full, C2c_full, C3_full, C4a_full, C8_raw+full_spec.
Reuses existing retrieval data from prior runs.

Usage:
    python run_full_spec_rerun.py --subject hamerton
    python run_full_spec_rerun.py --subject franklin
    python run_full_spec_rerun.py --subject franklin_obscure
    python run_full_spec_rerun.py --subject all
"""
import json, os, sys, time, subprocess, random, hashlib, httpx, pathlib, argparse
from datetime import datetime, timezone
from collections import defaultdict
from glob import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# NOTE: the subject memory environments (hamerton_memory, franklin_clean_memory,
# subjects/franklin_memory) live outside this repo. Set ANTHROPIC_ROOT to the
# directory that contains them; defaults to empty so a missing path is obvious.
ANTHROPIC_ROOT = os.environ.get("ANTHROPIC_ROOT", "")

# Load env
for k in ['MEM0_KEY', 'SUPERMEMORY_KEY', 'ANTHROPIC_API_KEY']:
    r = subprocess.run(['powershell', '-Command',
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    val = r.stdout.strip()
    if val: os.environ[k] = val

RESPONSE_MODEL = "claude-haiku-4-5-20251001"


def load_full_spec(layers_dir):
    """Load full layer stack (anchors + core + predictions + brief) matching serving engine."""
    layers_dir = pathlib.Path(layers_dir)
    sections = []
    for layer_name, filename in [
        ("ANCHORS", "anchors_v4.md"),
        ("CORE", "core_v4.md"),
        ("PREDICTIONS", "predictions_v4.md"),
    ]:
        filepath = layers_dir / filename
        if not filepath.exists():
            print(f"  WARNING: {filename} not found at {filepath}", flush=True)
            continue
        content = filepath.read_text(encoding="utf-8")
        marker = "## Injectable Block"
        idx = content.find(marker)
        if idx >= 0:
            block = content[idx + len(marker):].strip()
        else:
            sep = content.find("\n---\n")
            block = content[sep + 5:].strip() if sep >= 0 else content.strip()
        sections.append(f"## {layer_name}\n\n{block}")

    # Add brief
    brief_file = layers_dir / "brief_v5_clean.md"
    if brief_file.exists():
        content = brief_file.read_text(encoding="utf-8")
        marker = "## Injectable Block"
        idx = content.find(marker)
        if idx >= 0:
            block = content[idx + len(marker):].strip()
        else:
            sep = content.find("\n---\n")
            block = content[sep + 5:].strip() if sep >= 0 else content.strip()
        sections.append(f"## UNIFIED BRIEF\n\n{block}")
    else:
        print(f"  WARNING: brief_v5_clean.md not found", flush=True)

    return "\n\n".join(sections)


def gen(api_key, question, system_prompt):
    resp = httpx.post("https://api.anthropic.com/v1/messages",
        json={"model": RESPONSE_MODEL, "max_tokens": 1024, "temperature": 0,
              "system": system_prompt,
              "messages": [{"role": "user", "content": question}]},
        headers={"x-api-key": api_key, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        timeout=60)
    resp.raise_for_status()
    d = resp.json()
    return {"text": d["content"][0]["text"],
            "input_tokens": d["usage"]["input_tokens"],
            "output_tokens": d["usage"]["output_tokens"],
            "model": RESPONSE_MODEL}


def mem0_search(query, user_id):
    resp = httpx.post("https://api.mem0.ai/v1/memories/search/",
        json={"query": query, "user_id": user_id, "limit": 10},
        headers={"Authorization": f"Token {os.environ['MEM0_KEY']}"}, timeout=15)
    if resp.status_code != 200: return []
    data = resp.json()
    if isinstance(data, list):
        return [r.get("memory", "") for r in data[:10]]
    results = data.get("results", data.get("memories", []))
    return [r.get("memory", r.get("text", "")) for r in results[:10]]


def supermemory_search(query, container_tag):
    resp = httpx.post("https://api.supermemory.ai/v3/search",
        json={"q": query, "limit": 10, "containerTags": [container_tag]},
        headers={"Authorization": f"Bearer {os.environ['SUPERMEMORY_KEY']}",
                 "Content-Type": "application/json"},
        timeout=15, follow_redirects=True)
    if resp.status_code != 200: return []
    results = resp.json().get("results", [])
    out = []
    for r in results[:10]:
        chunks = r.get("chunks", [])
        if chunks: out.append(chunks[0].get("content", ""))
        else: out.append(r.get("memory", r.get("content", "")))
    return out


SUBJECTS = {
    "hamerton": {
        "questions": os.path.join(BASE_DIR, "battery", "questions_80.json"),
        "facts": os.path.join(BASE_DIR, "shared_facts.json"),
        "spec_layers_dir": os.path.join(ANTHROPIC_ROOT, "hamerton_memory/data/identity_layers"),
        "wrong_spec_layers_dir": os.path.join(ANTHROPIC_ROOT, "subjects/franklin_memory/data/identity_layers"),
        "mem0_user": "hamerton_study",
        "sm_container": "hamerton_v2",
    },
    "franklin": {
        "questions": os.path.join(BASE_DIR, "battery", "questions_80_franklin.json"),
        "facts": os.path.join(BASE_DIR, "franklin_shared_facts.json"),
        "spec_layers_dir": os.path.join(ANTHROPIC_ROOT, "franklin_clean_memory/data/identity_layers"),
        "wrong_spec_layers_dir": os.path.join(ANTHROPIC_ROOT, "hamerton_memory/data/identity_layers"),
        "mem0_user": "franklin_study_v1",
        "sm_container": "franklin_study_v1",
    },
    "franklin_obscure": {
        "questions": os.path.join(BASE_DIR, "battery", "questions_80_franklin_obscure.json"),
        "facts": os.path.join(BASE_DIR, "franklin_obscure_shared_facts.json"),
        "spec_layers_dir": os.path.join(ANTHROPIC_ROOT, "subjects/franklin_memory/data/identity_layers"),
        "wrong_spec_layers_dir": os.path.join(ANTHROPIC_ROOT, "hamerton_memory/data/identity_layers"),
        "mem0_user": None,
        "sm_container": None,
    },
}


def run_subject(subject_name, cfg):
    api_key = os.environ["ANTHROPIC_API_KEY"]

    questions = json.load(open(cfg["questions"], encoding="utf-8"))["questions"]
    facts_data = json.load(open(cfg["facts"], encoding="utf-8"))
    fact_texts = [f["text"] for f in facts_data["facts"]]

    # Load full spec (layers + brief)
    spec = load_full_spec(cfg["spec_layers_dir"])
    wrong_spec = load_full_spec(cfg["wrong_spec_layers_dir"])

    print(f"\n{'='*60}", flush=True)
    print(f"Subject: {subject_name}", flush=True)
    print(f"  Questions: {len(questions)}", flush=True)
    print(f"  Facts: {len(fact_texts)}", flush=True)
    print(f"  Full spec: {len(spec.split())} words", flush=True)
    print(f"  Wrong spec: {len(wrong_spec.split())} words", flush=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_id = f"run_fullstack_{subject_name}_{timestamp}"
    output_dir = os.path.join(BASE_DIR, "results", run_id)
    os.makedirs(output_dir, exist_ok=True)
    cp_file = os.path.join(output_dir, "checkpoint.json")

    checkpoint = {"completed_ids": [], "results": []}
    random.seed(42)
    total_in = 0
    total_out = 0
    ft_all = "\n".join(f"- {f}" for f in fact_texts)

    print(f"  Output: {output_dir}", flush=True)

    for q_idx, q in enumerate(questions):
        qid = q["id"]
        if qid in set(checkpoint["completed_ids"]): continue
        q_text = q["text"]

        q_result = {
            "question_id": qid, "question_text": q_text, "tier": q["tier"],
            "category": q.get("category", ""),
            "held_out_passage": q.get("held_out_passage"),
            "retrieval": {}, "responses": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        def run_cond(name, prompt):
            nonlocal total_in, total_out
            try:
                t0 = time.time()
                resp = gen(api_key, q_text, prompt)
                elapsed = time.time() - t0
                resp["latency_ms"] = round(elapsed * 1000)
                q_result["responses"][name] = resp
                total_in += resp["input_tokens"]
                total_out += resp["output_tokens"]
                print(f"  {name:30s} {resp['output_tokens']:4d}t ({elapsed:.1f}s)", flush=True)
            except Exception as e:
                q_result["responses"][name] = {"error": str(e)}
                print(f"  {name:30s} FAILED: {e}", flush=True)

        print(f"[{q_idx+1}/{len(questions)}] Q{qid} ({q['tier']})", flush=True)

        # C2a_full: Full spec only
        run_cond("C2a_full_spec",
            "The following is a behavioral specification describing your user — "
            "how they think, decide, and act.\n\n"
            "=== BEHAVIORAL SPECIFICATION ===\n" + spec)

        # C2c_full: Wrong full spec
        run_cond("C2c_full_wrong_spec",
            "The following is a behavioral specification describing your user — "
            "how they think, decide, and act.\n\n"
            "=== BEHAVIORAL SPECIFICATION ===\n" + wrong_spec)

        # C3_full: Full spec + retrieved facts (Mem0)
        if cfg["mem0_user"]:
            try:
                mem0_facts = mem0_search(q_text, cfg["mem0_user"])
                q_result["retrieval"]["mem0"] = {"facts": mem0_facts, "count": len(mem0_facts)}
            except:
                mem0_facts = []
            if mem0_facts:
                ft = "\n".join(f"- {f}" for f in mem0_facts)
                run_cond("C3_full_mem0",
                    "The following is a behavioral specification describing your user — "
                    "how they think, decide, and act. You also have retrieved facts.\n\n"
                    "=== BEHAVIORAL SPECIFICATION ===\n" + spec + "\n\n"
                    "=== RETRIEVED FACTS ===\n" + ft)

        # C3_full: Full spec + Supermemory facts
        if cfg["sm_container"]:
            try:
                sm_facts = supermemory_search(q_text, cfg["sm_container"])
                q_result["retrieval"]["supermemory"] = {"facts": sm_facts, "count": len(sm_facts)}
            except:
                sm_facts = []
            if sm_facts:
                ft = "\n".join(f"- {f}" for f in sm_facts)
                run_cond("C3_full_supermemory",
                    "The following is a behavioral specification describing your user — "
                    "how they think, decide, and act. You also have retrieved facts.\n\n"
                    "=== BEHAVIORAL SPECIFICATION ===\n" + spec + "\n\n"
                    "=== RETRIEVED FACTS ===\n" + ft)

        # C4a_full: All facts + full spec
        run_cond("C4a_full_all_facts_plus_spec",
            "The following is a behavioral specification describing your user — "
            "how they think, decide, and act. You also have the complete set of "
            "known facts about this person.\n\n"
            "=== BEHAVIORAL SPECIFICATION ===\n" + spec + "\n\n"
            "=== ALL KNOWN FACTS ===\n" + ft_all)

        # Checkpoint
        checkpoint["results"].append(q_result)
        checkpoint["completed_ids"].append(qid)
        with open(cp_file, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)

    # Final
    cost = (total_in * 0.80 + total_out * 4.00) / 1_000_000
    print(f"\nCOMPLETE — {len(checkpoint['results'])} questions", flush=True)
    print(f"COST: ${cost:.2f}", flush=True)

    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(checkpoint["results"], f, indent=2, ensure_ascii=False)
    if os.path.exists(cp_file): os.remove(cp_file)

    manifest = {
        "run_id": run_id, "subject": subject_name,
        "spec_type": "full_layer_stack (anchors + core + predictions + brief)",
        "spec_words": len(spec.split()),
        "wrong_spec_words": len(wrong_spec.split()),
        "total_questions": len(checkpoint["results"]),
        "total_facts": len(fact_texts),
        "conditions": ["C2a_full_spec", "C2c_full_wrong_spec",
                       "C3_full_mem0", "C3_full_supermemory",
                       "C4a_full_all_facts_plus_spec"],
        "response_model": RESPONSE_MODEL,
        "estimated_cost_usd": round(cost, 2),
    }
    with open(os.path.join(output_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Saved to {output_dir}", flush=True)
    return output_dir


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", choices=["hamerton", "franklin", "franklin_obscure", "all"],
                       default="hamerton")
    args = parser.parse_args()

    subjects = (["hamerton", "franklin", "franklin_obscure"] if args.subject == "all"
                else [args.subject])

    print("=== Full Layer Stack Re-Run ===", flush=True)
    print(f"Subjects: {subjects}", flush=True)

    for subject in subjects:
        if subject not in SUBJECTS:
            print(f"Unknown subject: {subject}", flush=True)
            continue

        cfg = SUBJECTS[subject]

        # Check if spec layers exist
        layers_dir = pathlib.Path(cfg["spec_layers_dir"])
        if not (layers_dir / "anchors_v4.md").exists():
            print(f"\n{subject}: Spec layers not ready at {layers_dir}. Skipping.", flush=True)
            continue

        run_subject(subject, cfg)


if __name__ == "__main__":
    main()
