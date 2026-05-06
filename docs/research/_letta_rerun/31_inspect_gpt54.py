"""Inspect the gpt54 judgment file structure."""
import json
import os

path = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_ebers\letta_memory_haiku_judgments_gpt54.json"
with open(path, encoding="utf-8") as f:
    d = json.load(f)

if isinstance(d, list):
    print(f"list len={len(d)}")
    if d:
        print(f"item 0 keys: {list(d[0].keys()) if isinstance(d[0], dict) else type(d[0]).__name__}")
        print(f"item 0: {d[0]}")
        print(f"item 1: {d[1]}")
