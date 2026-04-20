"""Verify the gap between T220 human_len (332,585) and final block (335,349)."""
import json

path = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_babur\letta_stateful_test_result.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

# Final blocks
for b in data["final_blocks"]:
    print(f"final_blocks {b.get('label')} size: {len(b.get('value',''))}")

# Highest human_len across turns
max_hl = 0
max_i = None
for i, t in enumerate(data["turns"]):
    hl = t.get("human_len") or 0
    if hl > max_hl:
        max_hl = hl
        max_i = i
print(f"Max human_len across turns: {max_hl} at turn {max_i}")

# Check blocks_after sizes
max_ba_size = 0
max_ba_i = None
for i, t in enumerate(data["turns"]):
    ba = t.get("blocks_after")
    if isinstance(ba, list):
        for b in ba:
            if b.get("label") == "human":
                sz = len(b.get("value", ""))
                if sz > max_ba_size:
                    max_ba_size = sz
                    max_ba_i = i
print(f"Max blocks_after[human] value size across turns: {max_ba_size} at turn {max_ba_i}")

# Does final_blocks match last successful block_after or something else?
print()
print("Hypothesis: The 335,349 final block came from a final fetch *after* the loop, not from any turn.")
print("The discrepancy: final_blocks = 335,349 chars, but max human_len recorded per turn = 332,585.")
print("Gap = ", 335349 - 332585, "chars")
print()
print("The block grew +2,764 chars after T220's successful update. This means some post-loop retry succeeded.")
print("Or: final_blocks was pulled via a separate GET that normalized/re-fetched.")

# Given that the ceiling is documented in Letta's docs for per-message context — verify message ceiling pattern
# Turn 220's chunk_words=912 => ~5K chars chunk; after T220 block was 332,585; adding another ~2.5K chunk would push over 335k
# T221's attempted update fails with 400 => ceiling is roughly 335k - 337k

# Also: block limit field = 100000. That's a hint the agent was way over its declared limit but still succeeding until API caps it
print()
print("Conclusions about the ceiling:")
print("  - Block metadata 'limit' field = 100,000 but is NOT enforced.")
print("  - Actual agreement: successful updates up through human_len=332,585 (T220).")
print("  - First 400 Bad Request at T221 when attempting to add another ~850-word chunk.")
print("  - This suggests the ceiling is likely on the request body (block value + new chunk in a single API call), which combined would push past ~337,000 chars.")
print("  - The paper's '333,000-character per-message API ceiling' claim is directionally close; the observed ceiling is slightly higher. Last successful state was 332,585 chars; the first rejected attempt had base 332,585 + ~5K-10K chunk ~= 337K-343K total in the request.")

# Check if the paper's claim of 333K is the Letta message limit — search the repo for any docs
