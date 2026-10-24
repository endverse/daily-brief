#!/usr/bin/env python3
"""Full-archive dedup for issue 034. Drops processed.json items whose URL (normalized)
already appears in any 2026/*.html archive or current briefing.json."""
import json, re, glob, os
from urllib.parse import urlsplit, urlunsplit

def norm(u):
    u = u.replace('&amp;', '&').strip()
    p = urlsplit(u)
    q = '&'.join([x for x in p.query.split('&') if not x.lower().startswith('utm_') and x])
    path = p.path.rstrip('/') if p.path != '/' else p.path
    return urlunsplit((p.scheme, p.netloc.lower(), path, q, ''))

arch = set()
for f in sorted(glob.glob('2026/*.html')):
    raw = open(f, encoding='utf-8').read()
    for h in re.findall(r'href="([^"]+)"', raw):
        if h.startswith('http'):
            arch.add(norm(h))
if os.path.exists('briefing.json'):
    try:
        b = json.load(open('briefing.json'))
        for h in re.findall(r'https?://[^"\s<]+', json.dumps(b, ensure_ascii=False)):
            arch.add(norm(h))
    except Exception:
        pass
print(f'archive unique urls: {len(arch)}')

proc = json.load(open('processed.json'))
kept, dropped = [], []
for it in proc:
    if norm(it['url']) in arch:
        dropped.append(it['title'])
    else:
        kept.append(it)

print(f'processed {len(proc)} -> kept {len(kept)}, dropped {len(dropped)} duplicates')
for t in dropped:
    print('  ⏭️ ', t[:90])
json.dump(kept, open('kept.json', 'w'), ensure_ascii=False, indent=1)
print('wrote kept.json')
