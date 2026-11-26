#!/usr/bin/env python3
"""Fetch readable text for issue 066 candidate articles."""
import json, re, subprocess, html, sys

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
items = json.load(open('/Users/endverse/code/endverse/daily-brief/processed.dedup.json'))

TARGETS = [99, 100, 98, 93, 95, 82, 90, 94, 89, 50, 10, 25, 69, 22, 48, 70, 87]
for i in TARGETS:
    it = items[i]
    url = it['url']
    print('=' * 90)
    print(f'[{i}] {it["title"]}')
    print(url)
    raw = subprocess.run(['curl', '-sSL', '--max-time', '30', '-A', UA, url],
                         capture_output=True, text=True).stdout
    m = re.findall(r'<article[^>]*>(.*?)</article>', raw, re.S)
    body = m[0] if m else raw
    ps = re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)
    txt = []
    for p in ps:
        t = html.unescape(re.sub(r'<[^>]+>', '', p))
        t = re.sub(r'\s+', ' ', t).strip()
        if len(t) > 25 and not t.startswith('点击查看原文'):
            txt.append(t)
    out = '\n'.join(txt)
    if not out:
        # fallback: meta description / all text
        d = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', raw)
        out = html.unescape(d.group(1)) if d else re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', raw)))[:1500]
    print(out[:2200])
