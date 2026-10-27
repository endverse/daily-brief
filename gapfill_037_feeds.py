#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pull K8s / cloud-native / AI-infra feeds, list items from the last 4 days."""
import subprocess, re, datetime, email.utils, sys

FEEDS = {
    "k8s-blog": "https://kubernetes.io/feed.xml",
    "cncf": "https://www.cncf.io/feed/",
    "kubezilla": "https://kubezilla.io/feed/",
    "gcloud-containers": "https://cloudblog.withgoogle.com/topics/containers/rss/",
    "gcloud-ai": "https://cloudblog.withgoogle.com/topics/ai-machine-learning/rss/",
    "nvidia-blog": "https://blogs.nvidia.com/feed/",
    "infoq-ai": "https://www.infoq.cn/feed",
}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=4)

for name, url in FEEDS.items():
    try:
        r = subprocess.run(["curl", "-sSL", "-A", UA, "--max-time", "25", url],
                           capture_output=True, text=True, timeout=30)
        raw = r.stdout
    except Exception as e:
        print(f"!! {name}: {e}")
        continue
    items = re.findall(r"<item>(.*?)</item>", raw, re.S)
    print(f"\n===== {name}: {len(items)} items =====")
    n = 0
    for it in items[:25]:
        t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S)
        l = re.search(r"<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>", it, re.S)
        d = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
        if not (t and l):
            continue
        dt = None
        if d:
            try:
                dt = email.utils.parsedate_to_datetime(d.group(1).strip())
            except Exception:
                dt = None
        if dt and dt < cutoff:
            continue
        n += 1
        print("  ", dt.strftime("%Y-%m-%d") if dt else "??", "|", t.group(1).strip()[:95])
        print("      ", l.group(1).strip()[:130])
    if n == 0:
        print("   (no recent items)")
