#!/usr/bin/env python3
"""Full-archive URL dedup: drop processed.json items already published in any 2026/*.html."""
import json, re, glob, os, sys
from urllib.parse import urlsplit, urlunsplit

def norm(u):
    u = u.replace('&amp;', '&').strip()
    s = urlsplit(u)
    q = [p for p in s.query.split('&') if p and not p.split('=')[0].lower().startswith('utm_')]
    return urlunsplit((s.scheme, s.netloc.lower().replace('www.', ''), s.path.rstrip('/'), '&'.join(q), ''))

seen = {}
for f in sorted(glob.glob('2026/*.html')):
    raw = open(f, encoding='utf-8').read()
    for h in re.findall(r'href="([^"]+)"', raw):
        if h.startswith('http'):
            seen.setdefault(norm(h), os.path.basename(f))
# also current briefing.json (last issue)
try:
    bj = json.load(open('briefing.json'))
    def walk(o):
        if isinstance(o, dict):
            if o.get('url'): seen.setdefault(norm(o['url']), 'briefing.json')
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(bj)
except Exception as e:
    print('briefing.json skip', e)

items = json.load(open('processed.json'))
kept, dropped = [], []
for it in items:
    n = norm(it.get('url', ''))
    if n in seen:
        dropped.append((it.get('title', '')[:60], it.get('source'), seen[n]))
    else:
        kept.append(it)

json.dump(kept, open('kept.json', 'w'), ensure_ascii=False, indent=1)
print(f'archive urls={len(seen)}  processed={len(items)}  kept={len(kept)}  dropped={len(dropped)}')
print('--- dropped ---')
for t, s, f in dropped:
    print(f'  [{s}] {t}  ({f})')
from collections import Counter
c = Counter((i['board'], i['category']) for i in kept)
print('--- kept distribution ---')
for k, v in c.most_common():
    print(f'  {k[0]} / {k[1]}: {v}')
