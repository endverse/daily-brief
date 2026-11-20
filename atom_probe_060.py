#!/usr/bin/env python3
import subprocess, re, sys

REPOS = sys.argv[1:]
for r in REPOS:
    try:
        x = subprocess.run(["curl", "-sSL", "--max-time", "20", f"https://github.com/{r}/releases.atom"],
                           capture_output=True, text=True).stdout
    except Exception as e:
        print(f"=== {r} ERR {e}")
        continue
    es = re.findall(r"<entry>(.*?)</entry>", x, re.S)
    print(f"=== {r} ({len(es)} entries)")
    for e in es[:8]:
        t = re.search(r"<title>(.*?)</title>", e, re.S)
        u = re.search(r"<updated>(.*?)</updated>", e, re.S)
        l = re.search(r'<link rel="alternate"[^>]*href="([^"]+)"', e)
        print("  ", (u.group(1)[:10] if u else "?"), (t.group(1).strip() if t else "?")[:60], "|", (l.group(1) if l else "")[-60:])
