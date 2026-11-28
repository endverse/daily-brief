#!/usr/bin/env python3
"""Full-archive dedup: drop processed.json items whose URL or story already appeared."""
import json, re, glob, os, html, sys
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

BASE = os.path.dirname(os.path.abspath(__file__))

def norm(u):
    if not u: return ""
    u = html.unescape(u).strip()
    s = urlsplit(u)
    q = [(k, v) for k, v in parse_qsl(s.query, keep_blank_values=True)
         if not k.lower().startswith("utm_") and k.lower() not in ("spm", "from", "ref", "source")]
    path = s.path.rstrip("/")
    return urlunsplit((s.scheme.lower(), s.netloc.lower().replace("www.", ""), path, urlencode(q), ""))

arch_urls = set()
arch_titles = []
files = sorted(glob.glob(os.path.join(BASE, "2026", "*.html")))
for f in files:
    raw = open(f, encoding="utf-8", errors="ignore").read()
    for h in re.findall(r'href=["\'](https?://[^"\']+)["\']', raw):
        arch_urls.add(norm(h))
    # story titles: <h3><a href="...">TITLE</a></h3>
    for t in re.findall(r'<h3><a [^>]*>(.*?)</a></h3>', raw, re.S):
        t = re.sub(r"<[^>]+>", "", t)
        arch_titles.append(html.unescape(t).strip())

print(f"archives={len(files)} arch_urls={len(arch_urls)} arch_titles={len(arch_titles)}")

def tokens(s):
    s = s.lower()
    en = re.findall(r"[a-z0-9][a-z0-9.+#-]{1,}", s)
    cjk = re.findall(r"[\u4e00-\u9fff]", s)
    grams = set()
    for i in range(len(cjk) - 2):
        grams.add("".join(cjk[i:i+3]))
    return set(en), grams

arch_tok = [tokens(t) for t in arch_titles]

STOP = {"the","and","for","with","from","that","this","are","was","how","why","new",
        "you","your","can","not","but","its","has","have","will","into","out","all",
        "via","use","using","about","after","over","more","than","one","two"}

def is_dup_story(title):
    en, cg = tokens(title)
    en = {w for w in en if w not in STOP and len(w) > 2}
    if not en and not cg:
        return False
    for aen, acg in arch_tok:
        aen2 = {w for w in aen if w not in STOP and len(w) > 2}
        if en and aen2:
            inter = en & aen2
            if len(inter) >= 3 and len(inter) / min(len(en), len(aen2)) >= 0.45:
                return True
        if len(cg) >= 6 and len(acg) >= 6:
            inter = cg & acg
            if len(inter) / min(len(cg), len(acg)) >= 0.5:
                return True
    return False

items = json.load(open(os.path.join(BASE, "processed.json"), encoding="utf-8"))
kept, dropped = [], []
for it in items:
    if norm(it["url"]) in arch_urls:
        dropped.append((it, "URL"))
    elif is_dup_story(it.get("title") or ""):
        dropped.append((it, "STORY"))
    else:
        kept.append(it)

print(f"\nDROPPED {len(dropped)} / KEPT {len(kept)}")
for it, why in dropped:
    print(f"  [{why}] ({it.get('category')}) {it['title'][:70]}")

json.dump(kept, open(os.path.join(BASE, "processed.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

from collections import Counter
print("\nREMAINING by category:")
for k, v in Counter((it["board"], it["category"]) for it in kept).most_common():
    print(" ", k, v)
