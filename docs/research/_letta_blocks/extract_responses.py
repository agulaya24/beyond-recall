import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

# For each subject and target qid, pull the Letta stateful + Haiku response and BL C2a + Haiku response

def get_letta_response(subj_dir, qid):
    p = subj_dir + 'letta_memory_haiku_results.json'
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for r in d['results']:
        if r['question_id'] == qid:
            return r
    return None

def get_bl_response_hamerton(qid):
    p = 'C:/Users/Aarik/Anthropic/memory-study-repo/results/hamerton/fullstack_haiku.json'
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for r in d:
        if r['question_id'] == qid:
            return r
    return None

def get_bl_response_v2(subj_dir_name, qid):
    p = f'C:/Users/Aarik/Anthropic/memory-study-repo/results/{subj_dir_name}/results_v2.json'
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for r in d:
        if r['question_id'] == qid:
            return r
    return None

def get_individual_judge_scores(subj_dir, qid, pattern):
    """Pull per-judge scores for a qid from a pattern."""
    judges = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro']
    scores = {}
    for j in judges:
        p = subj_dir + pattern.format(judge=j)
        if not os.path.exists(p): continue
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        if isinstance(d, list):
            for item in d:
                if item.get('question_id') == qid and not item.get('parse_failure'):
                    scores[j] = item.get('score')
    return scores

def get_bl_judge_scores_hamerton(qid, cond='C2a_full_spec'):
    """Pull Hamerton per-judge scores for a qid."""
    scores = {}
    # judgments.json has haiku + gemini
    p = 'C:/Users/Aarik/Anthropic/memory-study-repo/results/hamerton/judgments.json'
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for item in d:
        if item.get('question_id') == qid and item.get('condition') == cond:
            if item.get('haiku_score') is not None:
                scores['haiku'] = item['haiku_score']
            if item.get('gemini_score') is not None:
                scores['gemini_flash'] = item['gemini_score']
    # other judge files
    for j in ['gemini_pro', 'gpt54']:
        p = f'C:/Users/Aarik/Anthropic/memory-study-repo/results/hamerton/{j}_judgments.json'
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                d = json.load(f)
            for item in d:
                if item.get('question_id') == qid and item.get('condition') == cond and not item.get('parse_failure'):
                    scores[j] = item.get('score')
    return scores

def get_bl_judge_scores_v2(subj_dir_name, qid, cond='C2a_full_spec'):
    """Pull Ebers/Babur per-judge scores for a qid."""
    scores = {}
    p = f'C:/Users/Aarik/Anthropic/memory-study-repo/results/{subj_dir_name}/judgments_v2.json'
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for item in d:
        if item.get('question_id') == qid and item.get('condition') == cond and not item.get('parse_failure'):
            judge = item.get('judge')
            if judge:
                scores[judge] = item.get('score')
    return scores

# ===================
# TARGETS
# ===================

# Hamerton — big Letta > BL: Q55, Q22, Q31, Q54
# Hamerton — big BL > Letta: Q51, Q27, Q29
hamerton_qids = [55, 22, 31, 54, 51, 27, 29]
# Ebers — big Letta > BL: Q19, Q10, Q14, Q29, Q21, Q1
# Ebers — no big BL > Letta (only small deltas)
ebers_qids = [19, 10, 14, 29, 21, 1, 37, 6]
# Babur — big Letta > BL: Q27, Q33, Q5
# Babur — big BL > Letta: Q22, Q3, Q9
babur_qids = [27, 33, 5, 22, 3, 9]

def process(subj_name, subj_dir_name, qids, hamerton_style=False):
    print(f'\n\n============== {subj_name.upper()} ===============')
    letta_dir = 'C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/' + (
        'run_fullstack_hamerton_20260411_231237/' if subj_name == 'hamerton' else f'{subj_dir_name}/'
    )
    for qid in qids:
        letta_r = get_letta_response(letta_dir, qid)
        if hamerton_style:
            bl_r = get_bl_response_hamerton(qid)
        else:
            bl_r = get_bl_response_v2(subj_dir_name, qid)
        if letta_r is None or bl_r is None:
            print(f'Q{qid}: missing (letta={letta_r is not None}, bl={bl_r is not None})')
            continue
        print(f'\n--- Q{qid} ---')
        print(f'QUESTION: {letta_r["question_text"]}')
        held = letta_r.get('held_out_passage', '')
        print(f'HELD-OUT: {held[:400]}')
        # Letta stateful+Haiku response
        resp = letta_r['response']
        if isinstance(resp, dict):
            letta_text = resp.get('text', '')
        else:
            letta_text = str(resp)
        print(f'\nLETTA STATEFUL + HAIKU:')
        print(letta_text[:2500])
        # BL C2a + Haiku response
        bl_text = ''
        if 'responses' in bl_r:
            resp = bl_r['responses']
            if isinstance(resp, dict):
                if 'C2a_full_spec' in resp:
                    bl_text = resp['C2a_full_spec'].get('text', '')
        print(f'\nBL C2a + HAIKU:')
        print(bl_text[:2500])
        # Judge scores
        letta_scores = get_individual_judge_scores(letta_dir, qid, 'letta_memory_haiku_judgments_{judge}.json')
        if hamerton_style:
            bl_scores = get_bl_judge_scores_hamerton(qid)
        else:
            bl_scores = get_bl_judge_scores_v2(subj_dir_name, qid)
        print(f'\nJUDGE SCORES:')
        print(f'  Letta stateful+Haiku: {letta_scores}')
        print(f'  BL C2a+Haiku: {bl_scores}')

process('hamerton', 'hamerton', hamerton_qids, hamerton_style=True)
process('ebers', 'global_ebers', ebers_qids, hamerton_style=False)
process('babur', 'global_babur', babur_qids, hamerton_style=False)
