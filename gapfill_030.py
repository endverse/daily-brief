#!/usr/bin/env python3
"""Append funnel-step-3 gap-fill items into processed.json (issue 030, 2026-10-20)."""
import json

GAP = [
    dict(title="Don't Let Your AI Agent Run kubectl: Sandboxing LLM-Generated Code on Kubernetes",
         url="https://kubezilla.io/dont-let-your-ai-agent-run-kubectl-sandboxing-llm-generated-code-on-kubernetes/",
         summary="kubezilla 用内置能力在 K8s v1.34.1 上搭 agent 沙箱：双 namespace + PSA restricted",
         published="2026-10-13T15:55:00+00:00",
         source="kubezilla", source_cat="K8s×AI", extra={}, board="基础设施板块",
         category="K8s × AI", oss=False, hot_score=12, is_hot=False),
    dict(title="Extending Kubernetes policy enforcement to runtime security for AI workloads",
         url="https://www.cncf.io/blog/2026/10/15/extending-kubernetes-policy-enforcement-to-runtime-security-for-ai-workloads/",
         summary="Kyverno 生态推出 Runtime for Kyverno：eBPF + LSM 把策略从准入推进到运行时",
         published="2026-10-15T11:00:00+00:00",
         source="CNCF Blog", source_cat="K8s×AI", extra={}, board="基础设施板块",
         category="K8s × AI", oss=False, hot_score=11, is_hot=False),
    dict(title="Carbon as a first-class signal: Bringing software carbon intensity to OpenTelemetry",
         url="https://www.cncf.io/blog/2026/10/15/carbon-as-a-first-class-signal-bringing-software-carbon-intensity-to-opentelemetry/",
         summary="Observability Summit EU 主题演讲：把 SCI 做成 OTel 语义约定的候选信号",
         published="2026-10-15T22:21:00+00:00",
         source="CNCF Blog", source_cat="云原生", extra={}, board="基础设施板块",
         category="云原生周边", oss=False, hot_score=6, is_hot=False),
    dict(title="Week Ending October 11, 2026 (Last Week in Kubernetes Development)",
         url="https://lwkd.info/2026/20261015",
         summary="LWKD 周刊：十月 patch release 推迟到 10/20，SIG Autoscaling 新增 model-serving-signals 子项目",
         published="2026-10-15T00:00:00+00:00",
         source="LWKD", source_cat="社区", extra={}, board="基础设施板块",
         category="社区与项目", oss=False, hot_score=7, is_hot=False),
    dict(title="KEP-5945: DRA Optional Node Operations",
         url="https://github.com/kubernetes/enhancements/issues/5945",
         summary="KEP-5945 给 ResourceSlice 加 skipNodeOperations，kubelet 可跳过 Prepare/Unprepare gRPC",
         published="2026-09-28T00:00:00+00:00",
         source="Kubernetes Enhancements", source_cat="K8s核心", extra={}, board="基础设施板块",
         category="K8s 核心技术", oss=True, hot_score=10, is_hot=False),
    dict(title="Kubernetes PR 142913: granular Job failure condition reasons for PodFailurePolicy",
         url="https://github.com/kubernetes/kubernetes/pull/142913",
         summary="Job 的 PodFailurePolicy 支持给规则命名，失败条件能指到具体规则而不是统一原因",
         published="2026-10-10T00:00:00+00:00",
         source="Kubernetes PR", source_cat="K8s核心", extra={}, board="基础设施板块",
         category="K8s 核心技术", oss=True, hot_score=8, is_hot=False),
    dict(title="Kubernetes PR 142897: WebSocket streaming metrics graduate to BETA",
         url="https://github.com/kubernetes/kubernetes/pull/142897",
         summary="KEP-4006 的 WebSocket 流式指标在 apiserver 与 kubelet 升到 Beta，配套无 SPDY 回退的 e2e",
         published="2026-10-10T00:00:00+00:00",
         source="Kubernetes PR", source_cat="K8s核心", extra={}, board="基础设施板块",
         category="K8s 核心技术", oss=True, hot_score=8, is_hot=False),
]

items = json.load(open("processed.json", encoding="utf-8"))
have = {it["url"] for it in items}
added = 0
for g in GAP:
    if g["url"] in have:
        continue
    items.append(g)
    have.add(g["url"])
    added += 1
json.dump(items, open("processed.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"processed.json: +{added} gap-fill items -> {len(items)} total")
for g in GAP:
    print(" ", g["category"], "|", g["title"][:70])
