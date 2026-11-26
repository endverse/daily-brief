#!/usr/bin/env python3
"""Issue 066: full-archive URL + event dedup."""
import json, re, glob, os, html, unicodedata

REPO = os.path.dirname(os.path.abspath(__file__))

def norm(u):
    u = html.unescape(u or "").strip()
    u = re.sub(r'[?&]utm_[^&]*', '', u)
    u = re.sub(r'\?&', '?', u)
    u = re.sub(r'[?&]$', '', u)
    u = u.rstrip('/')
    return u.lower()

arch_urls = set()
arch_titles = []
for f in sorted(glob.glob(os.path.join(REPO, '2026', '*.html'))):
    raw = open(f, encoding='utf-8').read()
    for h in re.findall(r'href="([^"]+)"', raw):
        if h.startswith('http'):
            arch_urls.add(norm(h))
    for t in re.findall(r'<h3><a [^>]*>(.*?)</a></h3>', raw, re.S):
        t = re.sub(r'<[^>]+>', '', t)
        t = html.unescape(t).strip()
        if t:
            arch_titles.append((t, os.path.basename(f)))

# also current briefing.json (previous issue source)
if os.path.exists(os.path.join(REPO, 'briefing.json')):
    try:
        bj = json.load(open(os.path.join(REPO, 'briefing.json'), encoding='utf-8'))
        for sec in bj.get('sections', []):
            for cat in sec.get('categories', []):
                for it in cat.get('items', []):
                    if it.get('url'):
                        arch_urls.add(norm(it['url']))
                    if it.get('title'):
                        arch_titles.append((it['title'], 'briefing.json'))
        for it in bj.get('highlights', []) + bj.get('flash', []):
            if it.get('url'):
                arch_urls.add(norm(it['url']))
            if it.get('title'):
                arch_titles.append((it['title'], 'briefing.json'))
    except Exception as e:
        print('briefing.json read err', e)

print(f'archive urls={len(arch_urls)} titles={len(arch_titles)}')

def tokens(s):
    s = unicodedata.normalize('NFKC', s or '').lower()
    return set(re.findall(r'[a-z0-9][a-z0-9.+#_-]{1,}', s))

def cjk3(s):
    s = re.sub(r'[^\u4e00-\u9fff]', '', unicodedata.normalize('NFKC', s or ''))
    return set(s[i:i+3] for i in range(max(0, len(s)-2)))

def jac(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

arch_tok = [(tokens(t), cjk3(t), t, src) for t, src in arch_titles]
arch_tok = [x for x in arch_tok if x[0] or x[1]]

items = json.load(open(os.path.join(REPO, 'processed.json'), encoding='utf-8'))
kept, dropped = [], []
for it in items:
    u = it.get('url', '')
    if norm(u) in arch_urls:
        dropped.append((it, 'URL-in-archive'))
        continue
    t = it.get('title', '') or ''
    tk, ck = tokens(t), cjk3(t)
    hit = None
    for atk, ack, at, src in arch_tok:
        score = max(jac(tk, atk), jac(ck, ack))
        if score >= 0.62 and (len(tk & atk) >= 3 or len(ck & ack) >= 4):
            hit = (at, src, round(score, 2))
            break
    if hit:
        dropped.append((it, f'event-dup:{hit[2]} vs {hit[0][:60]!r} @{hit[1]}'))
    else:
        kept.append(it)

print(f'kept={len(kept)} dropped={len(dropped)}')
for it, why in dropped:
    print('  DROP', why[:110], '|', (it.get('title') or '')[:70], '|', it.get('category'))

json.dump(kept, open(os.path.join(REPO, 'processed.dedup.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{**it, 'drop_reason': why} for it, why in dropped], open(os.path.join(REPO, 'dropped.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

from collections import Counter
c = Counter((it['board'], it['category']) for it in kept)
print('\n--- kept by category ---')
for k, v in c.most_common():
    print(f'{k[0]} / {k[1]}: {v}')
