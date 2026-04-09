import subprocess, httpx, time, json

# Get API key from Windows environment
r = subprocess.run(
    ['powershell', '-Command', "[System.Environment]::GetEnvironmentVariable('GEMINI_API_KEY','User')"],
    capture_output=True, text=True
)
key = r.stdout.strip()
if not key:
    print("ERROR: No GEMINI_API_KEY found in Windows user environment")
    exit(1)
print(f"API key loaded ({len(key)} chars)")

# Read the paper
with open(r'C:\Users\Aarik\Anthropic\memory-study-repo\docs\beyond_recall_arxiv_draft.md', 'r', encoding='utf-8') as f:
    paper = f.read()
print(f"Paper loaded ({len(paper)} chars)")

prompt = """You are a senior AI researcher reviewing an ArXiv preprint titled 'Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization.' This is a corrected draft where all numbers have been verified against raw data files. Please provide:

1. OVERALL GRADE (A-F) for ArXiv readiness
2. STRONGEST ELEMENTS — what would impress a reviewer
3. CRITICAL ISSUES — anything that must be fixed before publication
4. FRAMING CHECK — the paper argues that (a) recall is part of memory but interpretation is what makes it actionable, (b) facts don't carry their own significance — only the person can dictate what a fact means to them, (c) prediction is the TEST of representational accuracy, not the end goal. Does the paper consistently maintain this framing throughout, or does it slip into older 'prediction as the product' language anywhere?
5. METHODOLOGICAL CONCERNS — any issues with study design, statistics, or evaluation
6. NUMBER CONSISTENCY — flag any numbers that seem inconsistent or suspicious
7. MISSING ELEMENTS — what's absent that a top venue would expect?
8. ONE PARAGRAPH summary for a colleague

Be brutally honest. Direct feedback is valued over diplomatic hedging.

Here is the paper:

""" + paper

payload = {
    'contents': [{'parts': [{'text': prompt}]}],
    'generationConfig': {'maxOutputTokens': 8192}
}

# Try multiple model variants
models = [
    'gemini-2.5-pro',
    'gemini-2.5-pro-preview-05-06',
    'gemini-2.0-pro',
    'gemini-2.5-flash',
]

review_text = None
for model in models:
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}'
    for attempt in range(5):
        print(f"[{model}] Attempt {attempt+1}...")
        try:
            resp = httpx.post(url, json=payload, timeout=300)
            print(f"  Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                review_text = data['candidates'][0]['content']['parts'][0]['text']
                print(f"  Review received ({len(review_text)} chars)")
                break
            elif resp.status_code == 503:
                wait = 45 * (attempt + 1)
                print(f"  503 overloaded, waiting {wait}s...")
                time.sleep(wait)
            elif resp.status_code == 429:
                print("  Rate limited, waiting 60s...")
                time.sleep(60)
            elif resp.status_code == 404:
                print(f"  Model {model} not found, trying next...")
                break
            else:
                print(f"  Error: {resp.text[:500]}")
                time.sleep(30)
        except Exception as e:
            print(f"  Exception: {e}")
            time.sleep(30)
    if review_text:
        actual_model = model
        break

if review_text:
    output_path = r'C:\Users\Aarik\Anthropic\memory-study-repo\docs\gemini_pro_paper_review_v2.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Gemini 2.5 Pro Paper Review (v2) — Beyond Recall\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Model:** {actual_model}\n")
        f.write(f"**Paper:** beyond_recall_arxiv_draft.md (corrected draft)\n\n")
        f.write("---\n\n")
        f.write(review_text)
    print(f"\nReview saved to {output_path}")
else:
    print("ERROR: Failed to get review after all attempts")
