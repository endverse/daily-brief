#!/usr/bin/env python3
"""Append funnel-step-3 gap-fill items into processed.json (so verify_links accepts them)."""
import json

GAP = [
    dict(title="KAI-Scheduler v0.18.6", url="https://github.com/kai-scheduler/KAI-Scheduler/releases/tag/v0.18.6",
         summary="KAI-Scheduler v0.18.6: per-worker score maps removed; bind request handling fixes",
         published="2026-10-15T15:53:08+00:00",
         source="GitHub Releases", source_cat="K8s×AI", extra={}, board="基础设施板块",
         category="K8s × AI", oss=True, hot_score=12, is_hot=False),
    dict(title="Istio 1.30.6", url="https://github.com/istio/istio/releases/tag/1.30.6",
         summary="Istio 1.30.6 security patch: HTTP/2 method-case AuthZ bypass, istiod ambient crash",
         published="2026-10-15T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s核心", extra={}, board="基础设施板块",
         category="K8s 核心技术", oss=True, hot_score=10, is_hot=False),
    dict(title="containerd 2.2.10", url="https://github.com/containerd/containerd/releases/tag/v2.2.10",
         summary="containerd 2.2.10: four security advisories, log symlink and image ref hardening",
         published="2026-10-13T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s核心", extra={}, board="基础设施板块",
         category="K8s 核心技术", oss=True, hot_score=9, is_hot=False),
    dict(title="Envoy v1.39.4", url="https://github.com/envoyproxy/envoy/releases/tag/v1.39.4",
         summary="Envoy v1.39.4: RDS route-config race fixes, Prometheus native histogram index fix",
         published="2026-10-12T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s核心", extra={}, board="基础设施板块",
         category="K8s 核心技术", oss=True, hot_score=7, is_hot=False),
    dict(title="Cilium 1.19.9", url="https://github.com/cilium/cilium/releases/tag/1.19.9",
         summary="Cilium 1.19.9: selector cache data race panic, endpoint GC ID reuse fixes",
         published="2026-10-15T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s核心", extra={}, board="基础设施板块",
         category="K8s 核心技术", oss=True, hot_score=7, is_hot=False),
    dict(title="Cluster API v1.13.7", url="https://github.com/kubernetes-sigs/cluster-api/releases/tag/v1.13.7",
         summary="Cluster API v1.13.7: KCP learner deletion and proxy DialContext race fixes",
         published="2026-10-07T00:00:00+00:00",
         source="GitHub Releases", source_cat="社区项目", extra={}, board="基础设施板块",
         category="社区与项目", oss=True, hot_score=6, is_hot=False),
    dict(title="Cloudflare Containers 跨租户数据泄露：修复 skip_block_zeroing，清理全部运行中容器磁盘",
         url="https://www.infoq.cn/article/YmllSwKbZXY0bcVjjw70?utm_source=rss&utm_medium=article",
         summary="Cloudflare Containers dm-thin skip_block_zeroing cross-tenant block leak",
         published="2026-10-17T00:00:00+00:00",
         source="InfoQ中国", source_cat="云原生", extra={}, board="基础设施板块",
         category="云原生周边", oss=False, hot_score=13, is_hot=False),
    dict(title="KAI-Scheduler v0.16.12", url="https://github.com/kai-scheduler/KAI-Scheduler/releases/tag/v0.16.12",
         summary="KAI-Scheduler v0.16.12 maintenance release", published="2026-10-18T09:31:39+00:00",
         source="GitHub Releases", source_cat="K8s×AI", extra={}, board="基础设施板块",
         category="K8s × AI", oss=True, hot_score=4, is_hot=False),
    dict(title="Argo Workflows v4.1.5", url="https://github.com/argoproj/argo-workflows/releases/tag/v4.1.5",
         summary="Argo Workflows v4.1.5 patch release", published="2026-10-09T00:00:00+00:00",
         source="GitHub Releases", source_cat="社区项目", extra={}, board="基础设施板块",
         category="社区与项目", oss=True, hot_score=4, is_hot=False),
    dict(title="CNCF Landscape Explained: How Projects Move from Sandbox to Incubating to Graduated",
         url="https://kubezilla.io/cncf-landscape-explained-sandbox-incubating-graduated/",
         summary="CNCF maturity levels and TOC admission criteria explained", published="2026-10-18T07:26:34+00:00",
         source="kubezilla", source_cat="社区", extra={}, board="基础设施板块",
         category="社区与项目", oss=False, hot_score=4, is_hot=False),
]

items = json.load(open("processed.json"))
have = {it["url"] for it in items}
added = 0
for g in GAP:
    if g["url"] not in have:
        items.append(g); added += 1
json.dump(items, open("processed.json", "w"), ensure_ascii=False, indent=1)
print(f"processed.json: {len(items)} items (+{added} gap-fill)")
