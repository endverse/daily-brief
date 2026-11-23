#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full-archive dedup for issue 062: URL-normalized + story similarity (EN tokens / CJK 3-gram).
Improved over 061: token rule requires >=3 shared tokens so generic single-word titles
("Agent 上岗…") don't get dropped by min-length normalization; prints matched archive title.
"""
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

seen_urls = {}
arch_titles = []
files = sorted(glob.glob(os.path.join(REPO, "2026", "*.html")))
for f in files:
    html = open(f, encoding="utf-8", errors="ignore").read()
    for h in re.findall(r'href="([^"]+)"', html):
        seen_urls[norm(h)] = os.path.basename(f)
    for t in re.findall(r"<h3[^>]*>(.*?)</h3>", html, re.S):
        t = re.sub(r"<[^>]+>", "", t).strip()
        if t:
            arch_titles.append(t)

try:
    prev = json.load(open(os.path.join(REPO, "briefing.json"), encoding="utf-8"))
    def walk(o):
        if isinstance(o, dict):
            if o.get("url"):
                seen_urls.setdefault(norm(o["url"]), "briefing.json")
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

AT = [(t, toks(t), grams(t)) for t in arch_titles]

def similar(a):
    ta, ga = toks(a), grams(a)
    best, who = 0.0, ""
    for bt, bto, bgr in AT:
        if ta and bto:
            inter = len(ta & bto)
            if inter >= 3:
                sc = inter / max(1, min(len(ta), len(bto)))
                if sc > best:
                    best, who = sc, bt
        if ga and bgr:
            inter = len(ga & bgr)
            if inter >= 4:
                sc = inter / max(1, min(len(ga), len(bgr)))
                if sc > best:
                    best, who = sc, bt
    return best, who

items = json.load(open(os.path.join(REPO, "processed.json"), encoding="utf-8"))
kept, dropped = [], []
for it in items:
    n = norm(it.get("url"))
    if n in seen_urls:
        dropped.append((it, f"URL({seen_urls[n]})", ""))
        continue
    s, who = similar(it.get("title") or "")
    if s >= 0.72:
        dropped.append((it, f"STORY({s:.2f})", who))
        continue
    kept.append(it)

print(f"processed {len(items)} -> kept {len(kept)} | dropped {len(dropped)}")
print("--- DROPPED ---")
for it, why, who in dropped:
    print(f"  x [{why}] {it['title'][:70]} | {it.get('source')} | match={who[:60]}")

json.dump(kept, open(os.path.join(REPO, "kept.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

from collections import Counter
print("--- KEPT BY CAT ---")
print(Counter(k.get("category") for k in kept).most_common())
