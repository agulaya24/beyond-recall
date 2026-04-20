"""Extract block size progression across Babur turns to pinpoint the ceiling."""
import json

path = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_babur\letta_stateful_test_result.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
turns = data["turns"]

print(f"Total turns: {len(turns)}")
print(f"Format: turn | kind | error? | human_len | total_chars | chunk_words")
print()
# Print last successful + first failed
last_success_idx = None
for i, t in enumerate(turns):
    if not t.get("error") and i > 0:
        last_success_idx = i

# Print 215 through end
for i in range(215, len(turns)):
    t = turns[i]
    err = "ERR" if t.get("error") else "ok "
    hl = t.get("human_len", "?")
    tc = t.get("total_chars", "?")
    cw = t.get("chunk_words", "?")
    print(f"T{i:3d} | {t.get('kind')} | {err} | human_len={hl} | total_chars={tc} | chunk_words={cw}")

# Find the last turn where human_len exists and progression
print("\n--- First occurrences of human_len >= 300k ---")
for i, t in enumerate(turns):
    hl = t.get("human_len")
    if hl is not None and hl >= 300000:
        err = "ERR" if t.get("error") else "ok"
        print(f"T{i}: human_len={hl} total_chars={t.get('total_chars')} chunk_words={t.get('chunk_words')} {err}")
        if i > 10 and all(turns[j].get("error") for j in range(i, min(i+5, len(turns)))):
            break

# Find final successful update
print("\n--- Last turn with successful update (no error, has human_len) ---")
last_ok = None
for i, t in enumerate(turns):
    if not t.get("error"):
        if t.get("human_len") is not None:
            last_ok = i
print(f"Last successful turn index: {last_ok}")
if last_ok is not None:
    t = turns[last_ok]
    print(f"  turn={last_ok} human_len={t.get('human_len')} total_chars={t.get('total_chars')}")

# Find first error turn
print("\n--- First error turn details ---")
first_err_i = None
for i, t in enumerate(turns):
    if t.get("error"):
        first_err_i = i
        break
print(f"First error at turn {first_err_i}")
if first_err_i:
    t = turns[first_err_i]
    print(f"  turn={first_err_i} kind={t.get('kind')} human_len={t.get('human_len')} total_chars={t.get('total_chars')}")
    # The turn preceding
    if first_err_i > 0:
        prev = turns[first_err_i - 1]
        print(f"  prev turn {first_err_i-1}: human_len={prev.get('human_len')} total_chars={prev.get('total_chars')}")

# First persistent 400 error
print("\n--- First 400 error ---")
first_400 = None
for i, t in enumerate(turns):
    if t.get("error") and "400" in t["error"]:
        first_400 = i
        break
print(f"First 400 error at turn {first_400}")
if first_400 and first_400 > 0:
    # Check preceding successful turns' block size
    for j in range(max(0, first_400 - 3), first_400 + 2):
        t = turns[j]
        err = "ERR" if t.get("error") else "ok"
        print(f"  T{j}: human_len={t.get('human_len')} total_chars={t.get('total_chars')} chunk_words={t.get('chunk_words')} {err}")

# blocks_after — what's in it?
print("\n--- Sample blocks_after ---")
for i in (0, 50, 100, 200, 220):
    if i < len(turns):
        ba = turns[i].get("blocks_after")
        if ba:
            print(f"T{i} blocks_after keys/sample:", type(ba).__name__, str(ba)[:200] if isinstance(ba, (str, int)) else [{k: (v if not isinstance(v, str) or len(v) < 40 else f"<str len={len(v)}>") for k, v in b.items()} for b in ba] if isinstance(ba, list) else ba)
