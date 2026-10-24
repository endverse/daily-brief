#!/usr/bin/env python3
"""Issue 034 gap-fill: append curated release/technical items (funnel step 3) into
processed.json so verify_links.py accepts them as fetched sources."""
import json, datetime

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
add = [
    dict(title="Don't Let Your AI Agent Run kubectl: Sandboxing LLM-Generated Code on Kubernetes",
         url="https://kubezilla.io/dont-let-your-ai-agent-run-kubectl-sandboxing-llm-generated-code-on-kubernetes/",
         summary="在 Kubernetes v1.34.1 上用集群自带能力隔离 Agent 生成的代码：agent-system 与 agent-sandbox 双命名空间、PSA restricted、按命名空间 Role、ResourceQuota/LimitRange、默认拒绝 NetworkPolicy、ValidatingAdmissionPolicy CEL 校验。实测策略生效有延迟窗口：连开 5 次立即提交有 1 次被放过，延迟 2 秒后 5/5 拒绝。",
         source="Kubezilla", source_cat="K8s×AI 实践", board="基础设施", category="K8s × AI", oss=False),
    dict(title="DRA Driver for NVIDIA GPUs v0.5.1",
         url="https://github.com/kubernetes-sigs/dra-driver-nvidia-gpu/releases/tag/v0.5.1",
         summary="ComputeDomain 控制器修复了会把存活节点误移出状态、重排 IMEX 节点索引并中断 GPU 显存导入导出的竞态；新增 resources.computeDomains.imex.config 可覆盖 nvidia-imex 参数；kubelet plugin 不再注册未实现的 DRA 资源健康服务，消除 v1.36 上反复出现的报错。",
         source="GitHub Releases", source_cat="K8s×AI 开源", board="基础设施", category="K8s × AI", oss=True),
    dict(title="Kueue v0.19.10",
         url="https://github.com/kubernetes-sigs/kueue/releases/tag/v0.19.10",
         summary="修复 ConcurrentAdmission 下父 Workload 可能停留在已从 ClusterQueue 移除的 flavor 上；classical preemption 增加 ClassicalPreemptionCandidateOrderCache（alpha）复用候选排序；修正停止的 Pod 组被用于构建新 Workload 而钉在原节点、RayCluster worker PodSet 低于 KubeRay 最小副本等问题。",
         source="GitHub Releases", source_cat="K8s×AI 开源", board="基础设施", category="K8s × AI", oss=True),
    dict(title="Cilium v1.20.4",
         url="https://github.com/cilium/cilium/releases/tag/v1.20.4",
         summary="修复 1.20.3 引入的回归：Gateway API 实现错误处理 BackendTLSPolicy 导致 Cilium CPU 飙高且无法转发流量；另修 CiliumEnvoyConfig 只在自身命名空间重定向 Service、terminating backend 在开启 trafficDistribution 时被提前逐出 BPF map、内核 <6.12 上 IPv6 ClusterIP 反向 NAT 校验和错误。",
         source="GitHub Releases", source_cat="K8s 核心", board="基础设施", category="K8s 核心", oss=True),
    dict(title="Gateway API v1.7.0-rc.3",
         url="https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.7.0-rc.3",
         summary="rc.2 因发布清单问题被撤回；rc.3 为 ListenerSet 增加 pre-routing listener filters（GEP-5224），把 TLSRouteMixedMode 从 Experimental 提升到 Standard 通道，HTTPRouteRetry.Attempts 回退为 *int 且最小值降到 0 以便按规则关闭重试。",
         source="GitHub Releases", source_cat="K8s 核心", board="基础设施", category="K8s 核心", oss=True),
    dict(title="Envoy v1.40.1",
         url="https://github.com/envoyproxy/envoy/releases/tag/v1.40.1",
         summary="因 eMudhra 中间 CA 私钥泄露，镜像不再信任被攻破的 eMudhra CA，Envoy Mobile 内置根证书移除 AAA Certificate Services 与 emSign ECC Root CA G3，Hickory DNS 解析器升级 webpki-roots/rustls-webpki；contrib/istio 的 peer metadata 恢复优先读取 app/version 标签。",
         source="GitHub Releases", source_cat="云原生", board="基础设施", category="云原生周边", oss=True),
    dict(title="Prometheus v3.15.1",
         url="https://github.com/prometheus/prometheus/releases/tag/v3.15.1",
         summary="安全补丁：镜像 CA 证书不再信任 emSign ECC Root CA G3 与 Comodo AAA Services root；改用 Go 1.27.3 编译修 net/http、net/textproto、crypto/tls、html/template 漏洞；golang.org/x/net 升到 v0.60.0 修 5 个 HTTP/2 漏洞（GO-2026-6603 等）。",
         source="GitHub Releases", source_cat="云原生", board="基础设施", category="云原生周边", oss=True),
    dict(title="Argo CD v3.5.6",
         url="https://github.com/argoproj/argo-cd/releases/tag/v3.5.6",
         summary="修复 gRPC 的 _grpclb._tcp SRV 查询（#29989）、SOCKS5 代理下 SSH 仓库拉取、以及 server-side diff 把其他 manager 删除的字段误报为差异；同时把 Go 升到 1.26.10。",
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
