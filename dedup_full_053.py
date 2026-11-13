#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full-archive dedup over processed.json for issue 053 (URL + story keywords)."""
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
for f in sorted(glob.glob(os.path.join(REPO, "2026", "*.html"))):
    html = open(f, encoding="utf-8", errors="ignore").read()
    for h in re.findall(r'href="([^"]+)"', html):
        seen_urls.add(norm(h))
    for t in re.findall(r'<[^>]*class="[^"]*item-title[^"]*"[^>]*>(.*?)</', html, re.S):
        arch_titles.append(re.sub(r"<[^>]+>", "", t).strip())
    for t in re.findall(r"<h3[^>]*>(.*?)</h3>", html, re.S):
        arch_titles.append(re.sub(r"<[^>]+>", "", t).strip())

# current briefing.json (prev issue)
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
        dropped.append((it, "URL"))
    else:
        kept.append(it)

# story-level dedup: salient keyword overlap with archive titles
KW = [
    "claude code", "claude 4", "opus 4", "sonnet 4", "gpt-5", "gpt 5", "gemini",
    "kueue", "kserve", "vllm", "llm-d", "daft", "ray", "dynamo", "sglang",
    "e2b", "daytona", "microsandbox", "gvisor", "kata", "firecracker",
    "openclaw", "orca", "codex", "opencode", "copilot", "cursor",
    "kubernetes", "cilium", "calico", "containerd", "envoy", "istio", "kubecon",
    "a2a", "mcp", "agent sandbox", "swe-bench", "alphaver", "alphaproof",
]
at_low = [t.lower() for t in arch_titles if t]
kept2, dropped2 = [], []
for it in kept:
    t = (it.get("title") or "").lower()
    hit = None
    for k in KW:
        if k in t:
            # require a matching archive title that also contains this keyword + strong overlap
            for at in at_low:
                if k in at and len(set(re.findall(r"[a-z0-9]{4,}", t)) & set(re.findall(r"[a-z0-9]{4,}", at))) >= 3:
                    hit = at
                    break
        if hit:
            break
    if hit:
        dropped2.append((it, "STORY:" + hit[:50]))
    else:
        kept2.append(it)

print(f"processed {len(items)} -> afterURL {len(kept)} -> afterStory {len(kept2)}")
print(f"dropped URL={len(dropped)} STORY={len(dropped2)}")
print("--- DROPPED ---")
for it, why in dropped + dropped2:
    print(f"  x [{why[:60]}] {it['title'][:75]} | {it.get('source')}")

json.dump(kept2, open(os.path.join(REPO, "kept.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote kept.json")
