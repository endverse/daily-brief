#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append step-③ gap-fill items into processed.json for issue 049."""
import json, subprocess

ADD = [
    dict(title="Introducing Kinference: An Open Source Inference Control Plane for vLLM and Kubernetes",
         url="https://vllm.ai/blog/2026-11-04-introducing-kinference",
         summary="Buoyant 开源 Kinference：vLLM 之上的推理控制面，提供 KV-cache 感知负载均衡、token 限流、租户成本核算与 CRD 形式的 InferencePolicy 路由策略。基准中对标准 kube-proxy Service，TTFT 中位数降 95%，共享前缀 goodput 7.4 倍。",
         source="vLLM Blog", board="基础设施", category="K8s × AI", oss=True),
    dict(title="Migrating vLLM to the LibTorch Stable ABI",
         url="https://vllm.ai/blog/2026-11-06-stable-abi-cuda",
         summary="vLLM v0.33.0 起发布 LibTorch ABI Stable 的 CUDA wheel：升级 PyTorch 不再需要重编 vLLM，靠 stable C shim + torch_call_dispatcher 覆盖未稳定 API。迁移覆盖 175 个 .cpp/.cu 文件与 120+ 头文件，分块迁到独立 stable 库。",
         source="vLLM Blog", board="AI 板块", category="AI 工程落地", oss=True),
    dict(title="Kubernetes v1.36.6",
         url="https://github.com/kubernetes/kubernetes/releases/tag/v1.36.6",
         summary="补丁版本，修 Pod status.resourceClaimStatuses 在多 claim 时来回抖动、同名重建 Job 继承旧 Pod expectations 导致不收敛、kube-scheduler 对负操作符 namespaceSelector 的误判，以及 kube-proxy 在无权限改 sysctl 时反复尝试设置 nf_conntrack_max 的 1.36 回归。",
         source="GitHub Releases", board="基础设施", category="K8s 核心技术"),
    dict(title="Istio 1.30.8",
         url="https://github.com/istio/istio/releases/tag/1.30.8",
         summary="安全补丁版，修复 7 个 CVE：ambient 模式端口级策略运算符优先级错误导致明文绕过 mTLS（CVSS 8.2）、istiod 被畸形 xDS 资源名打崩（7.7）、4 元组复用绕过 sidecar conntrack（7.4）、多集群 SDS 可冒领他集群 secret 等。",
         source="GitHub Releases", board="基础设施", category="K8s 核心技术"),
    dict(title="Agent Sandbox v1.0.10",
         url="https://github.com/kubernetes-sigs/agent-sandbox/releases/tag/v1.0.10",
         summary="K8s SIG 的 agent 沙箱项目发布 v1.0.10：sandbox-router 支持 gRPC-Web 转码、sandboxd 增加单次执行超时与 mkdir/move/copy/tar 等文件操作、镜像进 registry.k8s.io；NetworkPolicy 改为只允许带 sandbox-name-hash 标签的 Pod 出网，属破坏性变更。",
         source="GitHub Releases", board="基础设施", category="K8s × AI", oss=True),
    dict(title="OpenTelemetry Collector v0.165.0",
         url="https://github.com/open-telemetry/opentelemetry-collector/releases/tag/v0.165.0",
         summary="移除 confighttp 中 IdleConnTimeout/MaxIdleConns/DisableKeepAlives 等废弃字段（破坏性），memory_limiter 新增 garbage_collector.enabled 可关掉强制 GC，queue_batch 处理器升到 traces/metrics/logs beta，pdata Map 读写减少分配。",
         source="GitHub Releases", board="基础设施", category="云原生周边", oss=True),
    dict(title="vLLM Delivers Day-0 Support for Kimi K3.1 Pro",
         url="https://vllm.ai/blog/2026-11-04-kimi-k31-pro",
         summary="vLLM 在 Kimi K3.1 Pro 发布当天提供支持：KDA 混合注意力上的稀疏 attention、FP8/NVFP4 packed KV cache，配套并行策略与 kernel 改动。",
         source="vLLM Blog", board="AI 板块", category="AI 工程落地", oss=True),
]

p = "processed.json"
items = json.load(open(p, encoding="utf-8"))
have = {i["url"] for i in items}
for a in ADD:
    st = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "-L",
                         "--max-time", "25", "-A", "Mozilla/5.0", a["url"]],
                        capture_output=True, text=True).stdout.strip()
    print(st, a["url"])
    if st not in ("200", "403"):
        print("  !! skip (status)", st)
        continue
    if a["url"] in have:
        print("  already present")
        continue
    items.append({
        "title": a["title"], "url": a["url"], "summary": a["summary"],
        "published": "2026-11-08T00:00:00+00:00", "source": a["source"],
        "source_cat": "补搜", "extra": {}, "board": a["board"],
        "category": a["category"], "oss": a.get("oss", False),
        "hot_score": 0, "is_hot": False,
    })
json.dump(items, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("processed.json now", len(items))
