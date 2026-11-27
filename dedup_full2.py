#!/usr/bin/env python3
"""Full-archive dedup: URL (normalized) + story-level title matching against ALL archives."""
import json, re, glob, html, os, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))

def norm(u):
    if not u:
        return ""
    u = html.unescape(u.strip())
    u = re.sub(r'[?&](utm_[^&]+|ref=[^&]+|source=[^&]+)', '', u)
    u = re.sub(r'[?&]$', '', u)
    return u.split('#')[0].rstrip('/').lower()

arch_files = sorted(glob.glob(os.path.join(BASE, '20*', '*.html')))
arch_urls, arch_titles = set(), []
for f in arch_files:
    txt = open(f, encoding='utf-8', errors='ignore').read()
    for m in re.findall(r'href="([^"]+)"', txt):
        if m.startswith('http'):
            arch_urls.add(norm(m))
    for t in re.findall(r'<h3><a [^>]*>(.*?)</a></h3>', txt, re.S):
        arch_titles.append(re.sub(r'<[^>]+>', '', t).strip())

if os.path.exists(os.path.join(BASE, 'briefing.json')):
    bj = json.load(open(os.path.join(BASE, 'briefing.json'), encoding='utf-8'))
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'url' and isinstance(v, str):
                    arch_urls.add(norm(v))
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(bj)

def toks(t):
    t = unicodedata.normalize('NFKC', t or '').lower()
    return set(re.findall(r'[a-z0-9][a-z0-9\.\-]{1,}', t))

def cjk3(t):
    t = re.sub(r'[^\u4e00-\u9fff]', '', t or '')
    return set(t[i:i+3] for i in range(len(t)-2))

arch_en = [toks(t) for t in arch_titles]
arch_cjk = [cjk3(t) for t in arch_titles]
print(f"archives={len(arch_files)} arch_urls={len(arch_urls)} arch_titles={len(arch_titles)}")

def dup_title(title):
    if not title:
        return False
    te, tc = toks(title), cjk3(title)
    for i, at in enumerate(arch_titles):
        ae, ac = arch_en[i], arch_cjk[i]
        if te and ae:
            inter = len(te & ae)
            if inter >= 3 and inter / min(len(te), len(ae)) >= 0.55:
                return at
        if tc and ac:
            inter = len(tc & ac)
            if inter >= 4 and inter / min(len(tc), len(ac)) >= 0.55:
                return at
    return False

items = json.load(open(os.path.join(BASE, 'processed.json'), encoding='utf-8'))
kept, dropped_url, dropped_story = [], [], []
for it in items:
    if norm(it.get('url')) in arch_urls:
        dropped_url.append(it)
        continue
    s = dup_title(it.get('title'))
    if s:
        dropped_story.append((it, s))
        continue
    kept.append(it)

print(f"processed: {len(items)} -> kept {len(kept)} | dropped_url {len(dropped_url)} | dropped_story {len(dropped_story)}")
json.dump(kept, open(os.path.join(BASE, 'kept.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print("\n=== DROPPED URL ===")
for it in dropped_url:
    print(f"  U [{it['category']}] {(it.get('title') or '')[:70]} | {it.get('source')}")

print("\n=== DROPPED STORY ===")
for it, s in dropped_story:
    print(f"  S [{it['category']}] {(it.get('title') or '')[:62]} || {s[:48]}")

print("\n=== KEPT by category ===")
from collections import defaultdict
g = defaultdict(list)
for it in kept:
    g[(it['board'], it['category'])].append(it)
for k in sorted(g):
    print(f"\n## {k[0]} / {k[1]}  ({len(g[k])})")
    for it in g[k]:
        print(f"  [{it.get('hot_score')}] {(it.get('title') or '')[:78]} | {it.get('source')}")
