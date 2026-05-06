"""Verify canonical in-place GPT-5.4 judgment files are now valid."""
import json
paths = [
    r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237\letta_memory_haiku_judgments_gpt54.json",
    r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_ebers\letta_memory_haiku_judgments_gpt54.json",
    r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_babur\letta_memory_haiku_judgments_gpt54.json",
]
for p in paths:
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    valid = [e for e in d if e.get("score", 0) >= 1 and not e.get("parse_failure")]
    mean = sum(e["score"] for e in valid) / len(valid) if valid else 0
    pf = sum(1 for e in d if e.get("parse_failure"))
    print(f"{p.split(chr(92))[-2]}: n={len(d)} valid={len(valid)} parse_failures={pf} mean={mean:.3f}")
