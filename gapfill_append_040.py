#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append gap-fill items (K8s x AI / K8s core / cloud native) for issue 040."""
import json

p = 'processed.json'
d = json.load(open(p))
have = {i['url'] for i in d}

add = [
    {
        "title": "Agent Sandbox v1.0.9：router 原生 gRPC 代理、挂起/恢复延迟指标，修掉暖池重复建沙箱",
        "url": "https://github.com/kubernetes-sigs/agent-sandbox/releases/tag/v1.0.9",
        "summary": "Kubernetes SIG 的 agent-sandbox 于 10 月 29 日发布 v1.0.9：sandbox-router 现在原生代理 gRPC（含 sandboxd 的 ProcessService，unary 与 streaming），8080 端口同时接受 h2c，v1.0.7 起坏掉的 WebSocket 恢复。新增 sandbox 生命周期指标（suspend_total / resume_total / suspend_latency_ms / resume_latency_ms，按 namespace、sandbox_template、owned_by 打标）。修掉两个暖池竞态：状态写 409 冲突被丢弃导致 SandboxClaim 卡在 Ready=False，以及从陈旧缓存 reconcile 冷建出第二个 Sandbox 并保留到 claim 删除。Suspend 不再上报 Finished=True，避免 ttlSecondsAfterFinished=0 时 claim 被误过期连 PVC 一起删。",
        "published": "2026-10-29T00:00:00+00:00",
        "source": "Agent Sandbox Releases",
        "source_cat": "K8s",
        "extra": {},
        "board": "基础设施",
        "category": "K8s × AI",
        "oss": True,
        "hot_score": 14,
        "is_hot": False,
    },
    {
        "title": "Kueue v0.20.4：DRA 设备额度按陈旧 ResourceSlice 误算导致占额，ElasticJobs 就绪判定修复",
        "url": "https://github.com/kubernetes-sigs/kueue/releases/tag/v0.20.4",
        "summary": "Kueue 10 月 29 日发 v0.20.4（v0.19.11 同步）：DRA 的 CEL 设备可用性检查会把陈旧或不完整 ResourceSlice 池里的设备算进来，Workload 可能为 DRA 分配器根本用不了的设备占住额度；device request 来自 LimitRange 默认值的 Workload 在匹配 DeviceClass 建好后仍停在 Pending。另修 ElasticJobsViaWorkloadSlices 下 WaitForPodsReady 把已准入的弹性 Job 误判为未就绪、以及 PodsReadyTimeout 误驱逐刚扩容的 slice。",
        "published": "2026-10-29T00:00:00+00:00",
        "source": "Kueue Releases",
        "source_cat": "K8s",
        "extra": {},
        "board": "基础设施",
        "category": "K8s × AI",
        "oss": True,
        "hot_score": 11,
        "is_hot": False,
    },
    {
        "title": "Gateway API v1.7.0 正式发布：HTTPRoute retry 晋升 Standard，新增预路由过滤器与 XTelemetryPolicy",
        "url": "https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.7.0",
        "summary": "Gateway API v1.7.0 于 10 月 29 日发布，是 v1.6.3 之后首个正式版。HTTPRoute 的 retry（codes / attempts / backoff）晋升 Standard 通道，并新增 HTTPRouteRetryCodes 与 HTTPRouteRetryConnectionError 一致性特性，旧的 HTTPRouteRetry、HTTPRouteRetryBackendTimeout 特性被移除。实验通道新增 GatewayListenerFilters（在路由决策前执行 listener 过滤器，用于外部鉴权、payload 处理）、XTelemetryPolicy（基于 OpenTelemetry 语义约定的标准属性字典）、把会话保持迁到 XBackend 资源、BackendTLSPolicy 可用 caCertificateRefs 引用 ClusterTrustBundle，以及按 Gateway 地址表达 routability。破坏性变更集中在实验 API：sessionName 改为 cookie.name / header.name，cookieConfig 改名 cookie，XBackend 的 spec.port.port 改为 number。",
        "published": "2026-10-29T00:00:00+00:00",
        "source": "Gateway API Releases",
        "source_cat": "K8s",
        "extra": {},
        "board": "基础设施",
        "category": "K8s 核心技术",
        "oss": True,
        "hot_score": 15,
        "is_hot": False,
    },
    {
        "title": "Cilium 1.20.4 修 1.20.3 的 Gateway API BackendTLSPolicy 回归：CPU 飙高且无法转发",
        "url": "https://github.com/cilium/cilium/releases/tag/1.20.4",
        "summary": "Cilium 10 月 23 日发 1.20.4（1.19.10、1.18.16 同步）。CHANGELOG 首条重要修复针对 1.20.3 引入的回归：Gateway API 实现对 BackendTLSPolicy 处理错误，导致 Cilium CPU 占用飙高并无法转发流量。另修 NAT46x64 网关前缀转换 panic、6.12 以下内核 IPv6 ClusterIP 反向 NAT 的 L4 校验和错误、CiliumEnvoyConfig 会把别的 namespace 的 Service 也重定向、以及启动瞬间 Pod 查询 DNS 出现 SERVFAIL/REFUSED。",
        "published": "2026-10-23T00:00:00+00:00",
        "source": "Cilium Releases",
        "source_cat": "CloudNative",
        "extra": {},
        "board": "基础设施",
        "category": "云原生周边",
        "oss": True,
        "hot_score": 9,
        "is_hot": False,
    },
]

n = 0
for a in add:
    if a['url'] not in have:
        d.append(a)
        have.add(a['url'])
        n += 1
json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1)
print('appended', n, 'total', len(d))
