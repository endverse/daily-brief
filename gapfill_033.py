#!/usr/bin/env python3
"""Issue 033 gap-fill: append curated release items (funnel step 3) into processed.json
so verify_links.py accepts them as fetched sources."""
import json, datetime

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
add = [
    dict(title="Dynamo v1.6.0", url="https://github.com/ai-dynamo/dynamo/releases/tag/v1.6.0",
         summary="Dynamo v1.6.0: 654 PRs from 148 contributors, pluggable router flow control, LPX on Kubernetes, runtime GPU budget reconfiguration.",
         source="GitHub Releases", source_cat="K8s×AI 开源", board="基础设施", category="K8s × AI", oss=True),
    dict(title="kueue v0.20.3", url="https://github.com/kubernetes-sigs/kueue/releases/tag/v0.20.3",
         summary="Kueue v0.20.3: MultiKueue RayService in-tree autoscaling with elastic workload slices, faster classical preemption, ConcurrentAdmission fix.",
         source="GitHub Releases", source_cat="K8s×AI 开源", board="基础设施", category="K8s × AI", oss=True),
    dict(title="Istio 1.31.3", url="https://github.com/istio/istio/releases/tag/1.31.3",
         summary="Istio 1.31.3 security release (ISTIO-SECURITY-2026-008), ambient node-untaint can wait for ztunnel, istiod renews expired self-signed CA.",
         source="GitHub Releases", source_cat="K8s 核心", board="基础设施", category="K8s 核心", oss=True),
    dict(title="Kyverno v1.19.2", url="https://github.com/kyverno/kyverno/releases/tag/v1.19.2",
         summary="Kyverno v1.19.2: CEL admission builds request activation once per request, cheaper engine context checkpoint copy, imageExtractors filter field.",
         source="GitHub Releases", source_cat="K8s 核心", board="基础设施", category="K8s 核心", oss=True),
    dict(title="open-webui v0.12.3", url="https://github.com/open-webui/open-webui/releases/tag/v0.12.3",
         summary="Open WebUI v0.12.3: MLS end-to-end encrypted chats, lighter Redis streaming, skill read limits, live collaborators.",
         source="GitHub Releases", source_cat="AI 开源", board="AI 板块", category="AI 工程落地", oss=True),
    dict(title="Envoy v1.38.8", url="https://github.com/envoyproxy/envoy/releases/tag/v1.38.8",
         summary="Envoy v1.38.8 security patch: drops compromised eMudhra intermediate CAs from docker images, Envoy Mobile root bundle and Hickory DNS resolver.",
         source="GitHub Releases", source_cat="云原生", board="基础设施", category="云原生周边", oss=True),
    dict(title="Argo CD v3.3.18", url="https://github.com/argoproj/argo-cd/releases/tag/v3.3.18",
         summary="Argo CD v3.3.18 security patch (eMudhra CA certs compromise) for the 3.3 line.",
         source="GitHub Releases", source_cat="云原生", board="基础设施", category="云原生周边", oss=True),
]
proc = json.load(open('processed.json'))
have = {it['url'] for it in proc}
added = 0
for a in add:
    if a['url'] in have:
        continue
    a.setdefault('published', now)
    a.setdefault('extra', {})
    a.setdefault('hot_score', 8)
    a.setdefault('is_hot', False)
    proc.append(a); added += 1
json.dump(proc, open('processed.json', 'w'), ensure_ascii=False, indent=1)
print(f'appended {added}, processed now {len(proc)}')
