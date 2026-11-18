#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full-archive dedup: drop processed.json items whose URL or story already published."""
import json, re, os, glob, sys, unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))

def norm(u):
    u = u.replace('&amp;', '&').strip()
    u = re.sub(r'[?&]utm_[^&#]*', '', u)
    u = re.sub(r'\?&', '?', u)
    u = u.rstrip('/')
    u = u.split('#')[0]
    return u

# 1) collect archive urls + titles
arch_urls = set()
arch_titles = []
files = sorted(glob.glob(os.path.join(ROOT, '20*', '*.html')))
for f in files:
    raw = open(f, encoding='utf-8', errors='ignore').read()
    for h in re.findall(r'href="([^"]+)"', raw):
        if h.startswith('http'):
            arch_urls.add(norm(h))
    for t in re.findall(r'<h3><a[^>]*>(.*?)</a></h3>', raw, re.S):
        t = re.sub(r'<[^>]+>', '', t)
        t = t.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
        t = re.sub(r'\s+', ' ', t).strip()
        if t:
            arch_titles.append(t)

# also the published briefing.json (should mirror latest page, cheap safety)
try:
    pb = json.load(open(os.path.join(ROOT, 'briefing.json'), encoding='utf-8'))
    def walk(o):
        if isinstance(o, dict):
            if o.get('url'): arch_urls.add(norm(o['url']))
            if o.get('title'): arch_titles.append(o['title'])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(pb)
except Exception as e:
    print('warn: briefing.json', e)

print(f'archives: {len(files)} files, {len(arch_urls)} unique urls, {len(arch_titles)} titles')
assert len(arch_titles) > 200, 'title extraction broken'

# 2) title similarity
def tokens(s):
    s = unicodedata.normalize('NFKC', s).lower()
    return set(re.findall(r'[a-z0-9][a-z0-9\.\-_]{1,}', s))

def cjk3(s):
    s = unicodedata.normalize('NFKC', s)
    chars = re.sub(r'[^\u4e00-\u9fff]', '', s)
    return set(chars[i:i+3] for i in range(len(chars)-2))

def similar(a, b):
    ta, tb = tokens(a), tokens(b)
    if len(ta) >= 3 and len(tb) >= 3:
        inter = ta & tb
        if len(inter) >= 3 and len(inter) / min(len(ta), len(tb)) >= 0.7:
            return True
    ca, cb = cjk3(a), cjk3(b)
    if len(ca) >= 8 and len(cb) >= 8:
        inter = ca & cb
        if len(inter) >= 8 and len(inter) / min(len(ca), len(cb)) >= 0.5:
            return True
    return False

items = json.load(open(os.path.join(ROOT, 'processed.json'), encoding='utf-8'))
kept, dropped = [], []
for it in items:
    u = norm(it.get('url', ''))
    if u in arch_urls:
        dropped.append(('URL', it)); continue
    hit = None
    for at in arch_titles:
        if similar(it.get('title', ''), at):
            hit = at; break
    if hit:
        dropped.append(('STORY:' + hit[:50], it)); continue
    kept.append(it)

print(f'\nkept={len(kept)} dropped={len(dropped)}')
from collections import Counter
print('by category kept:')
print(Counter(i.get('category') for i in kept).most_common())
print('\n--- DROPPED ---')
for r, it in dropped:
    print(f'[{r[:60]}] {it.get("category")} | {it.get("title","")[:80]}')

json.dump(kept, open(os.path.join(ROOT, 'kept.json'), 'w'), ensure_ascii=False, indent=1)
json.dump([i for _, i in dropped], open(os.path.join(ROOT, 'dropped.json'), 'w'), ensure_ascii=False, indent=1)
