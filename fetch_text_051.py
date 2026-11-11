#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch article body text for candidate URLs (issue 051)."""
import re, sys, subprocess, os, html

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"


def strip(s):
    s = re.sub(r"(?is)<(script|style|nav|footer|header|svg)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def get(url):
    p = "/tmp/dbf_%d.html" % abs(hash(url))
    subprocess.run(["curl", "-sSL", "-m", "45", "-A", UA, url, "-o", p], check=False)
    try:
        raw = open(p, encoding="utf-8", errors="ignore").read()
    except Exception as e:
        return "ERR %s" % e
    os.unlink(p)
    # InfoQ: article body paragraphs
    arts = re.findall(r"<article[^>]*>(.*?)</article>", raw, re.S)
    if arts:
        ps = re.findall(r"<p[^>]*>(.*?)</p>", arts[0], re.S)
        txt = "\n".join(strip(x) for x in ps if strip(x))
        if len(txt) > 200:
            return txt
    m = re.search(r"(?is)<main[^>]*>(.*?)</main>", raw)
    body = m.group(1) if m else raw
    return strip(body)


for u in sys.argv[1:]:
    t = get(u)
    print("\n" + "=" * 90)
    print("URL:", u, "| len", len(t))
    print(t[:3200])
