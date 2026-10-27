#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gap-fill: pull releases.atom for K8s x AI + K8s core repos, list entries in last 16 days."""
import subprocess, re, datetime, json, sys

REPOS = [
    # K8s x AI
    "llm-d/llm-d", "kubernetes-sigs/kueue", "kserve/kserve", "vllm-project/vllm",
    "NVIDIA/KAI-Scheduler", "volcano-sh/volcano", "Project-HAMi/HAMi",
    "koordinator-sh/koordinator", "NVIDIA/k8s-dra-driver-gpu",
    "ai-dynamo/dynamo", "sgl-project/sglang", "kubeflow/kubeflow",
    "kubernetes-sigs/gateway-api-inference-extension", "ray-project/kuberay",
    # K8s core / cloud native
    "kubernetes/kubernetes", "cilium/cilium", "projectcalico/calico",
    "containerd/containerd", "kubernetes-sigs/lws", "moby/buildkit",
    "envoyproxy/envoy", "istio/istio", "argoproj/argo-cd", "prometheus/prometheus",
    "kubernetes-sigs/gateway-api", "open-telemetry/opentelemetry-collector",
]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=16)

out = []
for repo in REPOS:
    url = f"https://github.com/{repo}/releases.atom"
    try:
        r = subprocess.run(["curl", "-sSL", "-A", UA, "--max-time", "25", url],
                           capture_output=True, text=True, timeout=30)
        raw = r.stdout
    except Exception as e:
        print(f"!! {repo}: {e}", file=sys.stderr)
        continue
    entries = re.findall(r"<entry>(.*?)</entry>", raw, re.S)
    fresh = []
    for e in entries:
        m = re.search(r"<updated>(.*?)</updated>", e)
        t = re.search(r"<title>(.*?)</title>", e, re.S)
        l = re.search(r'<link[^>]*href="([^"]+)"', e)
        if not (m and t and l):
            continue
        try:
            dt = datetime.datetime.fromisoformat(m.group(1).replace("Z", "+00:00"))
        except Exception:
            continue
        if dt >= cutoff:
            fresh.append({"tag": t.group(1).strip(), "date": dt.strftime("%Y-%m-%d"),
                          "url": l.group(1), "repo": repo})
    if fresh:
        print(f"== {repo}: {len(fresh)} fresh (of {len(entries)})")
        for f in fresh:
            print("   ", f["date"], f["tag"], f["url"])
        out.extend(fresh)
    else:
        print(f"== {repo}: 0 fresh (of {len(entries)})")

json.dump(out, open("/Users/endverse/code/endverse/daily-brief/atom_candidates.json", "w"),
          ensure_ascii=False, indent=1)
print(f"\nTOTAL fresh: {len(out)}")
