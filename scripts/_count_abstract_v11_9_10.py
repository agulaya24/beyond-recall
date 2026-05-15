import re
from pathlib import Path

text = Path("docs/beyond_recall_v11_9_10_draft.md").read_text(encoding="utf-8")
m = re.search(r"## Abstract\s*\n\s*\n(.+?)\n\s*\n", text, re.DOTALL)
abs_text = m.group(1).strip()
plain = re.sub(r"\*\*([^*]+)\*\*", r"\1", abs_text)
words = plain.split()
print(f"Abstract word count: {len(words)}")
sentences = re.split(r"(?<=[.!?])\s+", plain)
print(f"Sentence count: {len(sentences)}")
for i, s in enumerate(sentences, 1):
    print(f"S{i} ({len(s.split())}w): {s[:120]}{'...' if len(s)>120 else ''}")
