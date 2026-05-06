"""Confirm that full-stack input token counts are significantly larger than unified-brief."""
import json

with open(r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\ebers_bl_c2a_named_responses.json", encoding="utf-8") as f:
    old_eb = json.load(f)
with open(r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\fullstack_named\ebers_bl_c2a_fullstack_responses.json", encoding="utf-8") as f:
    new_eb = json.load(f)
with open(r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\babur_bl_c2a_named_responses.json", encoding="utf-8") as f:
    old_ba = json.load(f)
with open(r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\fullstack_named\babur_bl_c2a_fullstack_responses.json", encoding="utf-8") as f:
    new_ba = json.load(f)
with open(r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\fullstack_named\hamerton_bl_c2a_fullstack_responses.json", encoding="utf-8") as f:
    new_ha = json.load(f)


def avg_tok(results):
    vals = [r["input_tokens"] for r in results if r.get("input_tokens")]
    return sum(vals) / len(vals) if vals else 0


print(f"Ebers:   old unified mean in_tokens = {avg_tok(old_eb['results']):.0f}  |  new full-stack mean = {avg_tok(new_eb['results']):.0f}")
print(f"Babur:   old unified mean in_tokens = {avg_tok(old_ba['results']):.0f}  |  new full-stack mean = {avg_tok(new_ba['results']):.0f}")
print(f"Hamerton: new full-stack mean = {avg_tok(new_ha['results']):.0f}  (no old unified baseline here; see diag scripts)")
