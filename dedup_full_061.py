#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full-archive dedup for issue 061: URL-normalized + story similarity (EN tokens / CJK 3-gram)."""
import json, re, glob, os
from urllib.parse import urlsplit, urlunsplit

REPO = os.path.dirname(os.path.abspath(__file__))

def norm(u):
    if not u:
        return ""
    u = u.replace("&amp;", "&").strip()
    s = urlsplit(u)
    q = "&".join(p for p in s.query.split("&") if p and not p.startswith("utm_"))
    path = s.path.rstrip("/")
    return urlunsplit((s.scheme, s.netloc.lower(), path, q, ""))

seen_urls = set()
arch_titles = []
files = sorted(glob.glob(os.path.join(REPO, "2026", "*.html")))
for f in files:
    html = open(f, encoding="utf-8", errors="ignore").read()
    for h in re.findall(r'href="([^"]+)"', html):
        seen_urls.add(norm(h))
    for t in re.findall(r"<h3[^>]*>(.*?)</h3>", html, re.S):
        t = re.sub(r"<[^>]+>", "", t).strip()
        if t:
            arch_titles.append(t)
    for t in re.findall(r'class="[^"]*item-title[^"]*"[^>]*>(.*?)</', html, re.S):
        t = re.sub(r"<[^>]+>", "", t).strip()
        if t:
            arch_titles.append(t)

# previous briefing.json URLs
try:
    prev = json.load(open(os.path.join(REPO, "briefing.json"), encoding="utf-8"))
    def walk(o):
        if isinstance(o, dict):
            if o.get("url"):
                seen_urls.add(norm(o["url"]))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(prev)
except Exception as e:
    print("prev briefing skip:", e)

print(f"archive files={len(files)} archive titles={len(arch_titles)} archive urls={len(seen_urls)}")

def toks(s):
    return set(re.findall(r"[a-z0-9]{3,}", s.lower()))

def grams(s):
    cjk = "".join(re.findall(r"[\u4e00-\u9fff]", s))
    return {cjk[i:i+3] for i in range(len(cjk) - 2)} if len(cjk) >= 3 else set()

AT = [(t, toks(t), grams(t), t.lower()) for t in arch_titles]

def similar(a, b):
    ta, ga = toks(a), grams(a)
    best = 0.0
    for bt, bto, bgr, bl in [(x[0], x[1], x[2], x[3]) for x in AT]:
        sc = 0.0
        if ta and bto:
            sc = max(sc, len(ta & bto) / max(1, min(len(ta), len(bto))))
        if ga and bgr:
            sc = max(sc, len(ga & bgr) / max(1, min(len(ga), len(bgr))))
        if sc > best:
            best = sc
    return best

items = json.load(open(os.path.join(REPO, "processed.json"), encoding="utf-8"))
kept, dropped = [], []
for it in items:
    if norm(it.get("url")) in seen_urls:
        dropped.append((it, "URL", ""))
        continue
    s = similar(it.get("title") or "", "")
    if s >= 0.72:
        dropped.append((it, f"STORY({s:.2f})", ""))
        continue
    kept.append(it)

print(f"processed {len(items)} -> kept {len(kept)} | dropped {len(dropped)}")
print("--- DROPPED ---")
for it, why, _ in dropped:
    print(f"  x [{why}] {it['title'][:80]} | {it.get('source')}")

json.dump(kept, open(os.path.join(REPO, "kept.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

from collections import Counter
print("--- KEPT BY CAT ---")
print(Counter(k.get("category") for k in kept).most_common())
