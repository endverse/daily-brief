#!/usr/bin/env python3
"""Full-archive URL + story dedup against every published issue."""
import json, re, glob, os, sys, html
from urllib.parse import urlsplit, parse_qsl, urlencode

BASE = os.path.dirname(os.path.abspath(__file__))

def norm(u):
    if not u:
        return ""
    u = html.unescape(u).strip()
    s = urlsplit(u)
    q = [(k, v) for k, v in parse_qsl(s.query, keep_blank_values=True)
         if not k.lower().startswith("utm_")]
    path = s.path.rstrip("/") or "/"
    return f"{s.scheme.lower()}://{s.netloc.lower()}{path}" + (("?" + urlencode(q)) if q else "")

# 1) collect all archived hrefs
arch_urls = {}
for f in sorted(glob.glob(os.path.join(BASE, "2026", "*.html"))):
    raw = open(f, encoding="utf-8", errors="ignore").read()
    for h in re.findall(r'href="([^"]+)"', raw):
        if h.startswith("#") or h.startswith("mailto:"):
            continue
        n = norm(h)
        if n:
            arch_urls.setdefault(n, os.path.basename(f))

# 2) current briefing.json urls too (if exists from an aborted run)
if os.path.exists(os.path.join(BASE, "briefing.json")):
    try:
        b = json.load(open(os.path.join(BASE, "briefing.json")))
        for it in b.get("highlights", []):
            if it.get("url"): arch_urls.setdefault(norm(it["url"]), "briefing.json")
        for sec in b.get("sections", []):
            for c in sec.get("categories", []):
                for it in c.get("items", []):
                    if it.get("url"): arch_urls.setdefault(norm(it["url"]), "briefing.json")
    except Exception as e:
        print("warn briefing.json:", e)

print(f"归档 URL 总数(归一化): {len(arch_urls)}")

items = json.load(open(os.path.join(BASE, "processed.json"), encoding="utf-8"))
print(f"processed.json: {len(items)} 条")

kept, dropped = [], []
for it in items:
    n = norm(it.get("url", ""))
    if n in arch_urls:
        dropped.append((it, arch_urls[n]))
    else:
        kept.append(it)

# story-level dedup: token sets from archived titles
arch_raw_titles = []
for f in sorted(glob.glob(os.path.join(BASE, "2026", "*.html"))):
    raw = open(f, encoding="utf-8", errors="ignore").read()
    arch_raw_titles += re.findall(r'<h3><a [^>]*>(.*?)</a></h3>', raw, re.S)
arch_raw_titles = [re.sub(r"<[^>]+>", "", t).strip() for t in arch_raw_titles]

STOP = set("the a an of to in on for with and or is are new how what why this that from at by as it its be will can now your you we our not 2026 vs into over after first more than about s".split())

def toks(s):
    return {w for w in re.findall(r"[a-z0-9][a-z0-9\.\-]{1,}", (s or "").lower()) if w not in STOP}

arch_tok = [(t, toks(t)) for t in arch_raw_titles if t]
story_dups = []
final = []
for it in kept:
    tt = toks(it.get("title", ""))
    hit = None
    for at, aset in arch_tok:
        if not tt or not aset:
            continue
        inter = tt & aset
        # require a distinctive overlap: >=3 shared tokens and >=60% of the shorter title
        if len(inter) >= 3 and len(inter) >= 0.6 * min(len(tt), len(aset)):
            hit = at
            break
    if hit:
        story_dups.append((it, hit))
    else:
        final.append(it)

print(f"\nURL 重复剔除: {len(dropped)} 条")
for it, src in dropped:
    print(f"  ✗ [{src}] {it.get('title','')[:80]}")

print(f"\n同事件(title token)剔除: {len(story_dups)} 条")
for it, hit in story_dups:
    print(f"  ✗ vs「{hit[:60]}」← {it.get('title','')[:70]}")

print(f"\n剩余: {len(final)} 条")

json.dump(final, open(os.path.join(BASE, "processed.dedup.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

from collections import Counter
c = Counter(i.get("category", "?") for i in final)
print("\n剩余分类分布:")
for k, v in c.most_common():
    print(f"  {k}: {v}")
