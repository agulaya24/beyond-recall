"""
Memory Systems Study — Complete Runner (all 14 conditions)
Query-only — assumes all systems already have data loaded.

Conditions:
  C1_mem0, C1_letta, C1_supermemory, C1_zep  — memory system retrieval
  C2a_spec_only                                — behavioral spec, no facts
  C3_mem0, C3_letta, C3_supermemory, C3_zep   — spec + memory system facts
  C4_factdump                                  — all 462 facts in context
  C5_baseline                                  — no facts, no spec
  C6_random                                    — random fact sample

Usage:
    python run_full_study.py --test          # 5 test questions
    python run_full_study.py --full          # 80 questions
    python run_full_study.py --resume RUN_ID # resume interrupted run
"""

import json
import os
import sys
import time
import random
import argparse
import hashlib
import concurrent.futures
from datetime import datetime, timezone

import anthropic

API_TIMEOUT = 30  # seconds — kill any API call that hangs longer than this


def with_timeout(fn, timeout=API_TIMEOUT):
    """Run fn() with a timeout. Returns result or raises TimeoutError."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(fn)
        return future.result(timeout=timeout)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACTS_FILE = os.path.join(BASE_DIR, "shared_facts.json")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
SPEC_FILE = os.path.normpath(os.path.join(
    BASE_DIR, "..", "..", "..", "..",
    "hamerton_memory", "data", "identity_layers", "brief_v5_clean.md"
))
# Wrong spec control — Franklin's spec applied to Hamerton's questions
WRONG_SPEC_FILE = os.path.normpath(os.path.join(
    BASE_DIR, "..", "..", "..", "..",
    "subjects", "franklin_memory", "data", "identity_layers", "brief_v5_clean.md"
))

RESPONSE_MODEL = "claude-haiku-4-5-20251001"
RESPONSE_TEMPERATURE = 0
RESPONSE_MAX_TOKENS = 1024


def load_env():
    """Load API keys from Windows User environment variables."""
    import subprocess
    loaded = {}
    for key_name in ["ZEP_KEY", "SUPERMEMORY_KEY", "LETTA_KEY", "MEM0_KEY",
                     "ANTHROPIC_API_KEY", "OPENAI_API_KEY"]:
        result = subprocess.run(
            ["powershell", "-Command",
             f"[System.Environment]::GetEnvironmentVariable('{key_name}','User')"],
            capture_output=True, text=True
        )
        val = result.stdout.strip()
        if val:
            os.environ[key_name] = val
            loaded[key_name] = f"SET ({len(val)}c)"
        else:
            loaded[key_name] = "NOT SET"
    return loaded


def load_config():
    """Load per-system config."""
    with open(CONFIG_FILE) as f:
        return json.load(f)


def load_spec():
    """Load the Hamerton behavioral spec."""
    with open(SPEC_FILE, encoding="utf-8") as f:
        return f.read()


def load_wrong_spec():
    """Load a mismatched spec (Franklin) for control condition C2c."""
    if not os.path.exists(WRONG_SPEC_FILE):
        return None
    with open(WRONG_SPEC_FILE, encoding="utf-8") as f:
        return f.read()


# === Retrieval Adapters (query-only, no ingestion) ===

class Mem0Retriever:
    name = "mem0"

    def __init__(self, config):
        from mem0 import MemoryClient
        self.client = MemoryClient(api_key=os.environ["MEM0_KEY"])
        self.user_id = config.get("mem0", {}).get("user_id", "hamerton_study")
        self.search_params = config.get("mem0", {}).get("search_params", {})

    def search(self, query, top_k=10):
        results = self.client.search(
            query,
            filters={"user_id": self.user_id},
            limit=self.search_params.get("top_k", top_k),
        )
        if isinstance(results, dict):
            results = results.get("results", results.get("memories", []))
        return [{
            "text": r.get("memory", r.get("text", "")) if isinstance(r, dict) else str(r),
            "score": r.get("score", 0) if isinstance(r, dict) else 0,
        } for r in results[:top_k]]


class LettaRetriever:
    name = "letta"

    def __init__(self, config):
        from letta_client import Letta
        self.client = Letta(api_key=os.environ["LETTA_KEY"])
        self.agent_id = None
        agents = list(self.client.agents.list())
        for a in agents:
            if "hamerton" in (a.name or "").lower():
                self.agent_id = a.id
                break
        if not self.agent_id:
            raise RuntimeError("No hamerton agent found in Letta.")

    def search(self, query, top_k=10):
        response = self.client.agents.passages.search(
            agent_id=self.agent_id, query=query, top_k=top_k
        )
        results = response.results if hasattr(response, 'results') else []
        return [{
            "text": r.content if hasattr(r, 'content') else str(r),
            "score": r.score if hasattr(r, 'score') else 0,
        } for r in results[:top_k]]


class SupermemoryRetriever:
    name = "supermemory"

    def __init__(self, config):
        from supermemory import Supermemory
        self.client = Supermemory(api_key=os.environ["SUPERMEMORY_KEY"])
        sm_cfg = config.get("supermemory", {})
        self.container_tag = sm_cfg.get("container_tag", "hamerton_v2")
        self.search_params = sm_cfg.get("search_params", {})

    def search(self, query, top_k=10):
        kwargs = {
            "q": query,
            "limit": self.search_params.get("limit", top_k),
        }
        if self.container_tag:
            kwargs["container_tag"] = self.container_tag
        results = self.client.search.memories(**kwargs)
        memories = results.results if hasattr(results, 'results') else []
        return [{
            "text": m.memory if hasattr(m, 'memory') and m.memory else str(m),
            "score": m.similarity if hasattr(m, 'similarity') else 0,
        } for m in (memories or [])[:top_k]]


class ZepRetriever:
    name = "zep"

    def __init__(self, config):
        from zep_cloud.client import Zep
        self.client = Zep(api_key=os.environ["ZEP_KEY"])
        self.user_id = None
        try:
            users = list(self.client.user.list_ordered(page_size=50))
            for u in users:
                uid = u.user_id if hasattr(u, 'user_id') else str(u)
                if "hamerton" in uid.lower():
                    self.user_id = uid
                    break
        except Exception:
            pass
        if not self.user_id:
            raise RuntimeError("No hamerton user found in Zep.")

    def search(self, query, top_k=10):
        results = self.client.graph.search(
            user_id=self.user_id, query=query, limit=top_k
        )
        edges = results.edges if hasattr(results, 'edges') and results.edges else []
        return [{
            "text": e.fact if hasattr(e, 'fact') else str(e),
            "score": e.score if hasattr(e, 'score') else 0,
        } for e in edges[:top_k]]


# === Response Generation ===

def build_system_prompt(context_type, context_content, spec_text=None):
    """Build system prompt for a given condition.

    Design principle: the user question is always delivered identically.
    Only the system context differs. No condition gets special instructions
    like "say so if you don't know" — that would be a confound. The model
    sees context + question, nothing else.
    """
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

    if context_type == "baseline":
        return "Answer the following question."

    return "Answer the following question."


def generate_response(client, question, system_prompt):
    """Generate a single response."""
    response = client.messages.create(
        model=RESPONSE_MODEL,
        max_tokens=RESPONSE_MAX_TOKENS,
        temperature=RESPONSE_TEMPERATURE,
        system=system_prompt,
        messages=[{"role": "user", "content": question}],
    )
    return {
        "text": response.content[0].text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "model": RESPONSE_MODEL,
    }


# === Checkpointing ===

def load_checkpoint(output_dir):
    """Load completed question IDs from checkpoint."""
    cp_file = os.path.join(output_dir, "checkpoint.json")
    if os.path.exists(cp_file):
        with open(cp_file, encoding="utf-8") as f:
            return json.load(f)
    return {"completed_ids": [], "results": []}


def save_checkpoint(output_dir, checkpoint):
    """Save checkpoint after each question."""
    cp_file = os.path.join(output_dir, "checkpoint.json")
    with open(cp_file, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=2, ensure_ascii=False)


# === Main Study Runner ===

def run_study(questions, facts, fact_texts, retrievers, spec_text, output_dir,
              checkpoint=None, wrong_spec_text=None):
    """Run all conditions for all questions."""
    anthropic_client = anthropic.Anthropic()
    random.seed(42)

    if checkpoint is None:
        checkpoint = {"completed_ids": [], "results": []}

    completed = set(checkpoint["completed_ids"])
    total = len(questions)
    skipped = 0

    # Condition list for manifest
    all_conditions = [
        "C1_mem0", "C1_letta", "C1_supermemory", "C1_zep",
        "C2a_spec_only", "C2c_wrong_spec",
        "C3_mem0", "C3_letta", "C3_supermemory", "C3_zep",
        "C4_factdump", "C5_baseline", "C6_random",
    ]

    # Token counters
    total_input_tokens = 0
    total_output_tokens = 0

    for q_idx, question in enumerate(questions):
        q_id = question["id"]
        q_text = question["text"]
        q_tier = question["tier"]
        q_cat = question.get("category", "")

        if q_id in completed:
            skipped += 1
            continue

        progress = f"[{q_idx + 1}/{total}]"
        print(f"\n{'=' * 70}")
        print(f"{progress} Q{q_id} ({q_tier}/{q_cat}): {q_text[:65]}...")
        print(f"{'=' * 70}")

        q_result = {
            "question_id": q_id,
            "question_text": q_text,
            "tier": q_tier,
            "category": q_cat,
            "held_out_passage": question.get("held_out_passage"),
            "held_out_chapter": question.get("held_out_chapter"),
            "retrieval": {},
            "responses": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # --- Step 1: Retrieve from all memory systems ---
        for name, retriever in retrievers.items():
            try:
                t0 = time.time()
                retrieved = with_timeout(
                    lambda r=retriever: r.search(q_text, top_k=10)
                )
                elapsed = time.time() - t0
                q_result["retrieval"][name] = {
                    "facts": [r["text"] for r in retrieved],
                    "scores": [r["score"] for r in retrieved],
                    "count": len(retrieved),
                    "latency_ms": round(elapsed * 1000),
                }
                print(f"  {name:15s} retrieved {len(retrieved):2d} facts ({elapsed:.1f}s)")
            except concurrent.futures.TimeoutError:
                print(f"  {name:15s} TIMEOUT ({API_TIMEOUT}s)")
                q_result["retrieval"][name] = {
                    "error": f"timeout after {API_TIMEOUT}s", "facts": [], "count": 0
                }
            except Exception as e:
                print(f"  {name:15s} FAILED: {e}")
                q_result["retrieval"][name] = {
                    "error": str(e), "facts": [], "count": 0
                }

        # --- Step 2: Generate responses for all conditions ---

        def run_condition(cond_name, system_prompt):
            """Run a single condition and record result."""
            nonlocal total_input_tokens, total_output_tokens
            try:
                t0 = time.time()
                resp = with_timeout(
                    lambda: generate_response(anthropic_client, q_text, system_prompt),
                    timeout=60  # response generation gets longer timeout
                )
                elapsed = time.time() - t0
                resp["latency_ms"] = round(elapsed * 1000)
                q_result["responses"][cond_name] = resp
                total_input_tokens += resp["input_tokens"]
                total_output_tokens += resp["output_tokens"]
                print(f"  {cond_name:20s} {resp['output_tokens']:4d}t  ({elapsed:.1f}s)")
            except concurrent.futures.TimeoutError:
                print(f"  {cond_name:20s} TIMEOUT (60s)")
                q_result["responses"][cond_name] = {"error": "timeout after 60s"}
            except Exception as e:
                print(f"  {cond_name:20s} FAILED: {e}")
                q_result["responses"][cond_name] = {"error": str(e)}

        # C1: Memory system retrieval (4 conditions)
        for name in retrievers:
            ret_facts = q_result["retrieval"].get(name, {}).get("facts", [])
            if ret_facts:
                prompt = build_system_prompt("facts", ret_facts)
                run_condition(f"C1_{name}", prompt)

        # C2a: Spec only (correct spec)
        prompt = build_system_prompt("spec_only", None, spec_text=spec_text)
        run_condition("C2a_spec_only", prompt)

        # C2c: Wrong spec (Franklin's spec on Hamerton's questions)
        if wrong_spec_text:
            prompt = build_system_prompt("spec_only", None, spec_text=wrong_spec_text)
            run_condition("C2c_wrong_spec", prompt)

        # C3: Spec + each memory system's facts (4 conditions)
        for name in retrievers:
            ret_facts = q_result["retrieval"].get(name, {}).get("facts", [])
            if ret_facts:
                prompt = build_system_prompt(
                    "spec_plus_facts", ret_facts, spec_text=spec_text
                )
                run_condition(f"C3_{name}", prompt)

        # C4: Fact dump (all facts)
        prompt = build_system_prompt("all_facts", fact_texts)
        run_condition("C4_factdump", prompt)

        # C5: Baseline (no context)
        prompt = build_system_prompt("baseline", None)
        run_condition("C5_baseline", prompt)

        # C6: Random facts (same count as median retrieval = 10)
        rand_facts = random.sample(fact_texts, min(10, len(fact_texts)))
        prompt = build_system_prompt("facts", rand_facts)
        q_result["C6_random_facts"] = rand_facts  # log which facts were selected
        run_condition("C6_random", prompt)

        # Save to checkpoint
        checkpoint["results"].append(q_result)
        checkpoint["completed_ids"].append(q_id)
        save_checkpoint(output_dir, checkpoint)
        sys.stdout.flush()

    if skipped:
        print(f"\nSkipped {skipped} already-completed questions.")

    # Cost estimate
    input_cost = total_input_tokens * 0.80 / 1_000_000
    output_cost = total_output_tokens * 4.00 / 1_000_000
    total_cost = input_cost + output_cost

    print(f"\n{'=' * 70}")
    print(f"TOKENS: {total_input_tokens:,} input + {total_output_tokens:,} output")
    print(f"COST:   ${total_cost:.2f} (${input_cost:.2f} input + ${output_cost:.2f} output)")
    print(f"{'=' * 70}")

    return checkpoint["results"], all_conditions, total_cost


def save_results(output_dir, results, all_conditions, questions_file, facts_data,
                 spec_text, retrievers, cost, wrong_spec_text=None):
    """Save final results + manifest."""
    os.makedirs(output_dir, exist_ok=True)

    # Compute spec checksum
    spec_hash = hashlib.sha256(spec_text.encode()).hexdigest()[:16]

    manifest = {
        "run_id": os.path.basename(output_dir),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "questions_file": os.path.basename(questions_file),
        "total_questions": len(results),
        "total_facts": len(facts_data["facts"]),
        "facts_checksum": facts_data.get("metadata", {}).get("corpus_checksum", ""),
        "spec_file": SPEC_FILE,
        "spec_checksum": spec_hash,
        "spec_tokens": len(spec_text.split()),
        "wrong_spec_file": WRONG_SPEC_FILE if wrong_spec_text else None,
        "wrong_spec_subject": "Benjamin Franklin" if wrong_spec_text else None,
        "response_model": RESPONSE_MODEL,
        "response_temperature": RESPONSE_TEMPERATURE,
        "response_max_tokens": RESPONSE_MAX_TOKENS,
        "systems": list(retrievers.keys()),
        "conditions": all_conditions,
        "estimated_cost_usd": round(cost, 2),
    }

    with open(os.path.join(output_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Remove checkpoint after successful save
    cp_file = os.path.join(output_dir, "checkpoint.json")
    if os.path.exists(cp_file):
        os.remove(cp_file)

    print(f"\nResults saved: {output_dir}")
    print(f"  manifest.json  — run metadata")
    print(f"  results.json   — all {len(results)} questions × {len(all_conditions)} conditions")


def print_overlap_summary(results, retrievers):
    """Print retrieval overlap summary (string-based, for quick sanity check)."""
    print("\n--- Retrieval Overlap (string Jaccard, sanity check only) ---")
    names = list(retrievers.keys())
    for i, s1 in enumerate(names):
        for s2 in names[i + 1:]:
            overlaps = []
            for r in results:
                f1 = set(r["retrieval"].get(s1, {}).get("facts", []))
                f2 = set(r["retrieval"].get(s2, {}).get("facts", []))
                if f1 and f2:
                    overlaps.append(len(f1 & f2) / max(len(f1 | f2), 1))
            if overlaps:
                avg = sum(overlaps) / len(overlaps)
                print(f"  {s1} vs {s2}: {avg:.1%}")
    print("(Use LLM-as-judge for real overlap — run_judge.py)")


def main():
    parser = argparse.ArgumentParser(description="Memory Systems Study — Full Runner")
    parser.add_argument("--test", action="store_true", help="5 test questions")
    parser.add_argument("--full", action="store_true", help="80 questions")
    parser.add_argument("--resume", type=str, help="Resume run by ID (e.g. run_20260409_120000)")
    args = parser.parse_args()

    # Load environment
    print("=== Environment ===")
    keys = load_env()
    for k, v in keys.items():
        print(f"  {k}: {v}")

    # Load config
    config = load_config()

    # Determine questions file
    if args.test or (not args.full and not args.resume):
        q_file = os.path.join(BASE_DIR, "battery", "test_questions.json")
    else:
        q_file = os.path.join(BASE_DIR, "battery", "questions_80.json")

    with open(q_file, encoding="utf-8") as f:
        battery = json.load(f)
    questions = battery["questions"]

    # Load facts
    with open(FACTS_FILE, encoding="utf-8") as f:
        facts_data = json.load(f)
    facts = facts_data["facts"]
    fact_texts = [f["text"] for f in facts]

    # Load specs
    spec_text = load_spec()
    wrong_spec_text = load_wrong_spec()

    print(f"\n=== Study Config ===")
    print(f"  Questions:  {len(questions)} ({os.path.basename(q_file)})")
    print(f"  Facts:      {len(facts)}")
    print(f"  Spec:       {len(spec_text.split())} words")
    print(f"  Wrong spec: {'Franklin (' + str(len(wrong_spec_text.split())) + ' words)' if wrong_spec_text else 'NOT FOUND'}")
    print(f"  Model:      {RESPONSE_MODEL}")
    print(f"  Temp:       {RESPONSE_TEMPERATURE}")

    # Initialize retrievers
    print(f"\n=== Initializing Retrievers ===")
    retrievers = {}
    # Letta and Zep excluded — run standalone (Letta hangs on init after ~50 queries,
    # Zep user_id mismatch). Their results merged from standalone runs.
    retriever_classes = [
        Mem0Retriever, SupermemoryRetriever,
    ]
    for RetClass in retriever_classes:
        try:
            ret = with_timeout(lambda RC=RetClass: RC(config), timeout=30)
            retrievers[ret.name] = ret
            print(f"  {ret.name:15s} OK")
            sys.stdout.flush()
        except concurrent.futures.TimeoutError:
            print(f"  {RetClass.name:15s} TIMEOUT (init)")
            sys.stdout.flush()
        except Exception as e:
            print(f"  {RetClass.name:15s} FAILED — {e}")
            sys.stdout.flush()

    if not retrievers:
        print("\nERROR: No retrievers initialized. Check API keys.")
        sys.exit(1)

    # Output dir + checkpoint
    if args.resume:
        run_id = args.resume
        output_dir = os.path.join(BASE_DIR, "results", run_id)
        if not os.path.exists(output_dir):
            print(f"ERROR: Run directory not found: {output_dir}")
            sys.exit(1)
        checkpoint = load_checkpoint(output_dir)
        remaining = len(questions) - len(checkpoint["completed_ids"])
        print(f"\n=== Resuming {run_id} ({len(checkpoint['completed_ids'])} done, {remaining} remaining) ===")
    else:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        run_id = f"run_{timestamp}"
        output_dir = os.path.join(BASE_DIR, "results", run_id)
        os.makedirs(output_dir, exist_ok=True)
        checkpoint = None

    print(f"  Output: {output_dir}")

    # Estimate
    n_conditions = 4 + 1 + len(retrievers) + 3  # C1 + C2a + C3 + C4/C5/C6
    n_questions = len(questions) - len(checkpoint["completed_ids"] if checkpoint else [])
    est_calls = n_questions * n_conditions
    print(f"\n=== Starting ({n_questions} questions × {n_conditions} conditions = {est_calls} API calls) ===")

    # Run
    results, all_conditions, cost = run_study(
        questions, facts, fact_texts, retrievers, spec_text, output_dir,
        checkpoint=checkpoint, wrong_spec_text=wrong_spec_text,
    )

    # Save
    save_results(output_dir, results, all_conditions, q_file, facts_data,
                 spec_text, retrievers, cost, wrong_spec_text=wrong_spec_text)

    # Quick overlap
    print_overlap_summary(results, retrievers)

    print(f"\n{'=' * 70}")
    print(f"COMPLETE — {len(results)} questions, {len(all_conditions)} conditions")
    print(f"Next: python run_judge.py --run {run_id}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
