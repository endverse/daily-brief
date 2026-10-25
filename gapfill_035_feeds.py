#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""funnel step 3b: community/blog feeds (kubezilla, CNCF, K8s blog) dedup vs archive."""
import json, re, glob, os, datetime, urllib.request
from urllib.parse import urlsplit, urlunsplit
from email.utils import parsedate_to_datetime

REPO = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"}

def norm(u):
    u = u.replace("&amp;", "&").strip()
    s = urlsplit(u)
    q = "&".join(p for p in s.query.split("&") if p and not p.startswith("utm_"))
    return urlunsplit((s.scheme.lower(), s.netloc.lower(), s.path.rstrip("/"), q, ""))

seen = set()
for f in glob.glob(os.path.join(REPO, "2026", "*.html")):
    for h in re.findall(r'href="([^"]+)"', open(f, encoding="utf-8", errors="ignore").read()):
        seen.add(norm(h))
try:
    prev = json.load(open(os.path.join(REPO, "briefing.json"), encoding="utf-8"))
    def walk(o):
        if isinstance(o, dict):
            if o.get("url"): seen.add(norm(o["url"]))
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(prev)
except Exception:
    pass

FEEDS = {
    "kubezilla": "https://kubezilla.io/feed/",
    "CNCF Blog": "https://www.cncf.io/feed/",
    "K8s Blog": "https://kubernetes.io/feed.xml",
    "InfoQ 云原生": "https://www.infoq.cn/feed/cloud",
}

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")

now = datetime.datetime.now(datetime.timezone.utc)
for name, url in FEEDS.items():
    print(f"\n===== {name} {url}")
    try:
        raw = fetch(url)
    except Exception as e:
        print("  !! fail", e)
        continue
    items = re.findall(r"<item>(.*?)</item>", raw, re.S)
    if not items:
        items = re.findall(r"<entry>(.*?)</entry>", raw, re.S)
    for e in items[:14]:
        t = re.search(r"<title[^>]*>(.*?)</title>", e, re.S)
        l = re.search(r"<link[^>]*>(.*?)</link>", e, re.S) or re.search(r'<link[^>]*href="([^"]+)"', e)
        d = re.search(r"<pubDate>(.*?)</pubDate>", e, re.S)
        dt = None
        if d:
            try: dt = parsedate_to_datetime(d.group(1).strip())
            except Exception: dt = None
        if not dt:
            d2 = re.search(r"<updated>(.*?)</updated>", e, re.S) or re.search(r"<published>(.*?)</published>", e, re.S)
            if d2:
                try: dt = datetime.datetime.fromisoformat(d2.group(1).replace("Z", "+00:00"))
                except Exception: dt = None
        age = (now - dt).days if dt else 999
        title = re.sub(r"<[^>]+>", "", t.group(1)) if t else ""
        title = re.sub(r"\s+", " ", title).strip()
        link = (l.group(1) if l else "").strip()
        flag = "NEW" if norm(link) not in seen else "dup"
        if age <= 30:
            print(f"  {flag} {age:>3}d {dt.date() if dt else '?'} {title[:85]} | {link}")
