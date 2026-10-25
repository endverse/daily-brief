#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full-archive dedup over processed.json for issue 035."""
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
for f in glob.glob(os.path.join(REPO, "2026", "*.html")):
    html = open(f, encoding="utf-8", errors="ignore").read()
    for h in re.findall(r'href="([^"]+)"', html):
        seen_urls.add(norm(h))

# current briefing.json (prev issue leftovers)
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
    print("prev briefing skip", e)

items = json.load(open(os.path.join(REPO, "processed.json"), encoding="utf-8"))
kept, dropped = [], []
for it in items:
    if norm(it.get("url")) in seen_urls:
        dropped.append(it)
    else:
        kept.append(it)

print(f"processed {len(items)} -> kept {len(kept)}, dropped {len(dropped)}")
print("--- DROPPED titles ---")
for it in dropped:
    print("  x", it["title"][:80], "|", it.get("source"))

json.dump(kept, open(os.path.join(REPO, "kept.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote kept.json")
