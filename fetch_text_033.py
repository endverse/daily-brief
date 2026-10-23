#!/usr/bin/env python3
"""Fetch article body text for a list of URLs (InfoQ/量子位/cloud blogs). Prints first N paragraphs."""
import sys, re, html, urllib.request, ssl
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}

def text(u):
    raw = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30, context=ctx).read().decode('utf-8', 'ignore')
    raw = re.sub(r'<(script|style|nav|footer)[^>]*>.*?</\1>', '', raw, flags=re.S)
    art = re.findall(r'<article[^>]*>(.*?)</article>', raw, re.S)
    seg = art[0] if art else raw
    ps = re.findall(r'<p[^>]*>(.*?)</p>', seg, re.S)
    out = []
    for p in ps:
        t = html.unescape(re.sub(r'<[^>]+>', '', p)).strip()
        if len(t) > 45 and 'Enable JavaScript' not in t:
            out.append(t)
    return out

for u in sys.argv[1:]:
    print('=' * 80); print(u)
    try:
        ps = text(u)
        print(f'[{len(ps)} paras]')
        print('\n\n'.join(ps[:14])[:3200])
    except Exception as e:
        print('ERR', str(e)[:120])
