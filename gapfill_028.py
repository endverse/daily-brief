#!/usr/bin/env python3
"""Append funnel-step-3 gap-fill items into processed.json (so verify_links accepts them)."""
import json

GAP = [
    dict(title="Agent Sandbox v1.0.7", url="https://github.com/kubernetes-sigs/agent-sandbox/releases/tag/v1.0.7",
         summary="Kubernetes Agent Sandbox v1.0.7 release", published="2026-10-15T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s×AI", extra={}, board="基础设施板块",
         category="K8s × AI", oss=True, hot_score=12, is_hot=False),
    dict(title="kagent v1.0.0-alpha14", url="https://github.com/kagent-dev/kagent/releases/tag/v1.0.0-alpha14",
         summary="kagent release v1.0.0-alpha14", published="2026-10-16T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s×AI", extra={}, board="基础设施板块",
         category="K8s × AI", oss=True, hot_score=10, is_hot=False),
    dict(title="GPU Sharing on Kubernetes: What HAMi Showed at KubeCon China 2026",
         url="https://kubezilla.io/hami-gpu-sharing-kubecon-china-2026/",
         summary="HAMi at KubeCon China 2026: dynamic MIG, schedule-first partition-second",
         published="2026-10-02T00:00:00+00:00", source="kubezilla", source_cat="K8s×AI", extra={},
         board="基础设施板块", category="K8s × AI", oss=False, hot_score=8, is_hot=False),
    dict(title="Karpenter v1.15.0", url="https://github.com/kubernetes-sigs/karpenter/releases/tag/v1.15.0",
         summary="Karpenter v1.15.0 release notes", published="2026-10-10T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s核心", extra={}, board="基础设施板块",
         category="K8s 核心技术", oss=True, hot_score=9, is_hot=False),
    dict(title="Karpenter v1.14.2", url="https://github.com/kubernetes-sigs/karpenter/releases/tag/v1.14.2",
         summary="Karpenter v1.14.2 patch", published="2026-10-16T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s核心", extra={}, board="基础设施板块",
         category="K8s 核心技术", oss=True, hot_score=5, is_hot=False),
    dict(title="Cluster API v1.14.3", url="https://github.com/kubernetes-sigs/cluster-api/releases/tag/v1.14.3",
         summary="Cluster API v1.14.3 release notes", published="2026-10-07T00:00:00+00:00",
         source="GitHub Releases", source_cat="社区项目", extra={}, board="基础设施板块",
         category="社区与项目", oss=True, hot_score=7, is_hot=False),
    dict(title="Argo CD v3.5.5", url="https://github.com/argoproj/argo-cd/releases/tag/v3.5.5",
         summary="Argo CD v3.5.5 patch release", published="2026-10-12T00:00:00+00:00",
         source="GitHub Releases", source_cat="社区项目", extra={}, board="基础设施板块",
         category="社区与项目", oss=True, hot_score=6, is_hot=False),
    dict(title="OpenTelemetry Collector v0.163.0",
         url="https://github.com/open-telemetry/opentelemetry-collector/releases/tag/v0.163.0",
         summary="OpenTelemetry Collector v0.163.0 release notes", published="2026-10-14T00:00:00+00:00",
         source="GitHub Releases", source_cat="社区项目", extra={}, board="基础设施板块",
         category="社区与项目", oss=True, hot_score=6, is_hot=False),
    dict(title="vLLM v0.32.0", url="https://github.com/vllm-project/vllm/releases/tag/v0.32.0",
         summary="vLLM v0.32.0", published="2026-10-17T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s×AI", extra={}, board="基础设施板块",
         category="K8s × AI", oss=True, hot_score=6, is_hot=False),
    dict(title="SGLang v0.5.22", url="https://github.com/sgl-project/sglang/releases/tag/v0.5.22",
         summary="SGLang v0.5.22", published="2026-10-15T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s×AI", extra={}, board="基础设施板块",
         category="K8s × AI", oss=True, hot_score=6, is_hot=False),
    dict(title="GPU Operator v26.7.2", url="https://github.com/NVIDIA/gpu-operator/releases/tag/v26.7.2",
         summary="NVIDIA GPU Operator 26.7.2", published="2026-10-14T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s×AI", extra={}, board="基础设施板块",
         category="K8s × AI", oss=True, hot_score=6, is_hot=False),
    dict(title="llm-d v1.0.0-rc.1", url="https://github.com/llm-d/llm-d/releases/tag/v1.0.0-rc.1",
         summary="llm-d v1.0.0 release candidate 1", published="2026-10-14T00:00:00+00:00",
         source="GitHub Releases", source_cat="K8s×AI", extra={}, board="基础设施板块",
         category="K8s × AI", oss=True, hot_score=6, is_hot=False),
]

items = json.load(open("processed.json"))
have = {it["url"] for it in items}
added = 0
for g in GAP:
    if g["url"] not in have:
        items.append(g); added += 1
json.dump(items, open("processed.json", "w"), ensure_ascii=False, indent=1)
print(f"processed.json: {len(items)} items (+{added} gap-fill)")
