"""Term-consistency audit for v11.8 paper. Per-section counts."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = 'C:/Users/Aarik/Anthropic/memory-study-repo/docs/beyond_recall_v11_8_draft.md'
with open(PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Build per-line section ownership
section_map = {}
current_top = "TITLE"
for i, line in enumerate(lines):
    m = re.match(r'^(##+)\s+(.+)$', line)
    if m:
        title = m.group(2).strip()
        nm = re.match(r'^(\d+)', title)
        if nm:
            current_top = f"§{nm.group(1)}"
        elif title.startswith('Appendix'):
            ap = re.match(r'^Appendix\s+([A-Z])', title)
            if ap:
                current_top = f"App {ap.group(1)}"
            else:
                current_top = title
        else:
            current_top = title
    section_map[i+1] = current_top

patterns = {
    'BS_cap':       re.compile(r'\bBehavioral Specification\b'),
    'BS_cap_pl':    re.compile(r'\bBehavioral Specifications\b'),
    'bs_lc':        re.compile(r'\bbehavioral specification\b'),
    'bs_lc_pl':     re.compile(r'\bbehavioral specifications\b'),
    'the_spec':     re.compile(r'\bthe spec\b'),
    'the_Spec':     re.compile(r'\bthe Spec\b'),
    'the_specification': re.compile(r'\bthe specification\b'),
    'interp_layer': re.compile(r'\binterpretive layer\b'),
    'the_layer':    re.compile(r'\bthe layer\b'),
    'rubric_anchor': re.compile(r'\brubric anchor[s]?\b'),
    'rubric_band':  re.compile(r'\brubric band[s]?\b'),
    'integer_rubric_band': re.compile(r'\binteger rubric band[s]?\b'),
    'integer_anchor': re.compile(r'\binteger anchor[s]?\b'),
    'integer_band': re.compile(r'\binteger band[s]?\b'),
    'baseline_band': re.compile(r'\bbaseline band\b'),
    'anchor_band': re.compile(r'\banchor band[s]?\b'),
    'substrate':    re.compile(r'\bsubstrate\b'),
    'framework':    re.compile(r'\bframework\b'),
    'frameworks':   re.compile(r'\bframeworks\b'),
    'Benjamin_Franklin': re.compile(r'\bBenjamin Franklin\b'),
    'Franklin':     re.compile(r'\bFranklin\b'),
    'wins':         re.compile(r'\bwins\b'),
    'won':          re.compile(r'\bwon\b'),
}

per_section = {}
hits = {pn: [] for pn in patterns}
for pat_name, pat in patterns.items():
    for i, line in enumerate(lines, start=1):
        for m in pat.finditer(line):
            sec = section_map.get(i, "TITLE")
            per_section.setdefault(sec, {}).setdefault(pat_name, 0)
            per_section[sec][pat_name] += 1
            hits[pat_name].append((i, sec, line.rstrip()))

# Order sections
sec_order = ["TITLE", "§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9",
             "App A", "App B", "App C", "App D", "App E", "App F", "App G", "App H"]
sec_seen = set(per_section.keys())
extras = sorted(s for s in sec_seen if s not in sec_order)
sec_final = [s for s in sec_order if s in sec_seen] + extras

print("=== TERM COUNT TABLE ===")
print()
header = ["Section", "BS(cap)", "bs(lc)", "the spec", "interp.layer", "the layer", "rubric anchor", "rubric band", "substrate", "framework(+s)", "Franklin", "wins/won"]
print(" | ".join(header))
print(" | ".join(["---"] * len(header)))
for sec in sec_final:
    c = per_section.get(sec, {})
    bs = c.get('BS_cap', 0) + c.get('BS_cap_pl', 0)
    bsl = c.get('bs_lc', 0) + c.get('bs_lc_pl', 0)
    sp = c.get('the_spec', 0) + c.get('the_Spec', 0)
    il = c.get('interp_layer', 0)
    lay = c.get('the_layer', 0)
    ra = c.get('rubric_anchor', 0)
    rb = c.get('rubric_band', 0)
    sub = c.get('substrate', 0)
    fw = c.get('framework', 0) + c.get('frameworks', 0)
    fr = c.get('Franklin', 0)
    w = c.get('wins', 0) + c.get('won', 0)
    print(f"{sec} | {bs} | {bsl} | {sp} | {il} | {lay} | {ra} | {rb} | {sub} | {fw} | {fr} | {w}")

print()
print("=== TOTAL HITS ===")
for pn in sorted(patterns):
    total = sum(per_section.get(s, {}).get(pn, 0) for s in sec_final)
    print(f"  {pn}: {total}")

print()
print("=== ALL HITS DETAIL ===")
for pn in ['bs_lc', 'bs_lc_pl', 'BS_cap_pl', 'the_layer', 'interp_layer',
           'rubric_band', 'integer_rubric_band', 'integer_band', 'anchor_band',
           'substrate', 'wins', 'won']:
    print(f"\n--- {pn} ({len(hits[pn])} hits) ---")
    for ln, sec, text in hits[pn]:
        print(f"  L{ln} [{sec}] {text[:200]}")
