#!/usr/bin/env python3
"""Full-archive URL dedup: drop processed.json items whose URL (normalized)
already appears in ANY 2026/*.html archive or in the current briefing.json."""
import json, re, glob, html, os

BASE = os.path.dirname(os.path.abspath(__file__))

def norm(u):
    if not u:
        return ""
    u = html.unescape(u.strip())
    u = re.sub(r'[?&]utm_[^&]+', '', u)
    u = re.sub(r'[?&]$', '', u)
    u = u.rstrip('/')
    return u.lower()

# collect archive URLs
arch_urls = set()
for f in glob.glob(os.path.join(BASE, '2026', '*.html')):
    txt = open(f, encoding='utf-8', errors='ignore').read()
    for m in re.findall(r'href="([^"]+)"', txt):
        arch_urls.add(norm(m))
# current briefing.json (last issue) URLs
if os.path.exists(os.path.join(BASE, 'briefing.json')):
    bj = json.load(open(os.path.join(BASE, 'briefing.json'), encoding='utf-8'))
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ('url',) and isinstance(v, str):
                    arch_urls.add(norm(v))
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(bj)

print(f"archive normalized URLs: {len(arch_urls)}")

items = json.load(open(os.path.join(BASE, 'processed.json'), encoding='utf-8'))
kept, dropped = [], []
for it in items:
    if norm(it.get('url')) in arch_urls:
        dropped.append(it)
    else:
        kept.append(it)

print(f"processed: {len(items)} -> kept {len(kept)}, dropped {len(dropped)} repeats")
json.dump(kept, open(os.path.join(BASE, 'kept.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print("\n=== DROPPED (already published) ===")
for it in dropped:
    print(f"  x [{it['category']}] {it['title'][:70]} | {it['source']}")

print("\n=== KEPT by category ===")
from collections import defaultdict
g = defaultdict(list)
for it in kept:
    g[(it['board'], it['category'])].append(it)
for k in sorted(g):
    print(f"\n## {k[0]} / {k[1]}  ({len(g[k])})")
    for it in g[k]:
        print(f"  [{it.get('hot_score')}] {it['title'][:78]} | {it['source']}")
