#!/usr/bin/env python3
"""Append funnel step-3 gap-fill items (068) to processed.json."""
import json, urllib.request, ssl, os

BASE = os.path.dirname(os.path.abspath(__file__))
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

NEW = [
    dict(title="Crush v0.103.0: client/server mode ships as experimental, terminals can resume a session via OSC 7577",
         url="https://github.com/charmbracelet/crush/releases/tag/v0.103.0",
         source="GitHub Releases", source_cat="AI-官方", board="AI 板块", category="Agent 工具链", oss=True, hot_score=12),
    dict(title="Orca v1.4.280: drops agy-based quota meter, avatars and commit messages to match Antigravity's integration guidance",
         url="https://github.com/stablyai/orca/releases/tag/v1.4.280",
         source="GitHub Releases", source_cat="AI-官方", board="AI 板块", category="Agent 工具链", oss=True, hot_score=11),
    dict(title="Models Can Communicate via Inference Servers Despite Being Sandboxed",
         url="https://www.lesswrong.com/posts/7wzWuLP3HhyBLmKfo/models-can-communicate-via-inference-servers-despite-being-sandboxed",
         source="LessWrong", source_cat="社区", board="AI 板块", category="沙箱与运行时", oss=False, hot_score=14),
    dict(title="brickie: run durable agent sandboxes in your own Kubernetes cluster on top of agent-sandbox",
         url="https://github.com/hatchet-dev/brickie",
         source="GitHub", source_cat="AI-官方", board="AI 板块", category="沙箱与运行时", oss=True, hot_score=13),
    dict(title="Kubernetes v1.38 Sneak Peek",
         url="https://kubernetes.io/blog/2026/11/23/kubernetes-v1-38-sneak-peek/",
         source="Kubernetes Blog", source_cat="云原生", board="基础设施", category="K8s × AI", oss=True, hot_score=13),
]

items = json.load(open(os.path.join(BASE, "processed.json"), encoding="utf-8"))
have = {it["url"] for it in items}
added = 0
for n in NEW:
    try:
        req = urllib.request.Request(n["url"], headers={"User-Agent": UA})
        st = urllib.request.urlopen(req, timeout=20, context=ctx).status
    except Exception as e:
        st = str(e)[:40]
    print(f"{st} {n['url']}")
    if st != 200:
        print("  SKIP (not 200)")
        continue
    if n["url"] in have:
        print("  already present")
        continue
    n.update(published="2026-11-27T00:00:00+00:00", summary="", extra={}, is_hot=False)
    items.append(n); have.add(n["url"]); added += 1

json.dump(items, open(os.path.join(BASE, "processed.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"\nappended {added}; total {len(items)}")
