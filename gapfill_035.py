#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""funnel step 3: gap-fill infra from releases.atom + blog feeds, dedup vs archive."""
import json, re, glob, os, sys, datetime, urllib.request
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
    html = open(f, encoding="utf-8", errors="ignore").read()
    for h in re.findall(r'href="([^"]+)"', html):
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

REPOS = [
    "kubernetes-sigs/kueue", "llm-d/llm-d", "kserve/kserve", "vllm-project/vllm",
    "kubernetes/kubernetes", "kubernetes-sigs/gateway-api", "NVIDIA/KAI-Scheduler",
    "volcano-sh/volcano", "Project-HAMi/HAMi", "koordinator-sh/koordinator",
    "NVIDIA/k8s-dra-driver-gpu", "ai-dynamo/dynamo", "sgl-project/sglang",
    "cilium/cilium", "projectcalico/calico", "containerd/containerd",
    "kubernetes-sigs/lws", "moby/buildkit", "envoyproxy/envoy", "istio/istio",
    "ray-project/kuberay", "kubernetes-sigs/jobset", "kubernetes-sigs/kubeflow",
]

def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")

now = datetime.datetime.now(datetime.timezone.utc)
print("now", now.isoformat())
out = []
for repo in REPOS:
    url = f"https://github.com/{repo}/releases.atom"
    try:
        raw = fetch(url)
    except Exception as e:
        print(f"!! {repo} fetch fail {e}")
        continue
    entries = re.findall(r"<entry>(.*?)</entry>", raw, re.S)
    print(f"\n## {repo}  entries={len(entries)}")
    for e in entries[:6]:
        t = re.search(r"<title>(.*?)</title>", e, re.S)
        u = re.search(r'<link[^>]*href="([^"]+)"', e)
        d = re.search(r"<updated>(.*?)</updated>", e)
        if not (t and u and d):
            continue
        try:
            dt = datetime.datetime.fromisoformat(d.group(1).replace("Z", "+00:00"))
        except Exception:
            continue
        age = (now - dt).days
        title = re.sub(r"\s+", " ", t.group(1)).strip()
        link = u.group(1).strip()
        flag = "NEW " if norm(link) not in seen else "dup "
        print(f"  {flag}{age:>3}d  {dt.date()}  {title[:70]}  {link}")
        if norm(link) in seen:
            continue
        if age <= 21:
            out.append({"repo": repo, "tag": title, "url": link,
                        "date": dt.date().isoformat(), "age": age})

json.dump(out, open(os.path.join(REPO, "gapfill_035.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"\n=== NEW candidates (<=21d): {len(out)} ===")
for c in out:
    print(c["age"], c["repo"], c["tag"], c["url"])
