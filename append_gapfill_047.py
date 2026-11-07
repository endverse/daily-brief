import json
P="processed.json"
items=json.load(open(P))
have={i["url"] for i in items}
gap=[
 {"title":"Kubeflow Trainer v2.4.0：TrainJob 支持 DRA，工作负载感知调度进 Phase 1",
  "url":"https://github.com/kubeflow/trainer/releases/tag/v2.4.0",
  "summary":"Kubeflow Trainer v2.4.0 正式发布，TrainJob 接入 DRA（KEP-2782）、工作负载感知调度进 Phase 1（KEP-3015）、OptimizationJob 控制器以 alpha 门控上线，并支持按 TrainJob 覆盖 schedulerName、多切片 TPU 的 Job Replicas、TrainJob 终结时清理 Volcano PodGroup。破坏性变更：MPI 插件改用 PRTE_MCA_* 环境变量，升级前创建的挂起 TrainJob 无法恢复；ReplicatedJob 名字限 20 字符。",
  "published":"2026-11-06T00:00:00+00:00","source":"GitHub Releases","source_cat":"基础设施",
  "extra":{},"board":"基础设施","category":"K8s × AI","oss":True,"hot_score":17,"is_hot":False},
 {"title":"Kubernetes v1.38.0-beta.0：seccomp 配置可从 OCI registry 拉取，DRA Device Binding 转 GA",
  "url":"https://github.com/kubernetes/kubernetes/releases/tag/v1.38.0-beta.0",
  "summary":"v1.38.0-beta.0 带来 alpha 的 SecurityProfileOCI（Pod 可用 seccompProfile.type=OCI 从 registry 按 digest 拉 seccomp 配置）、DRA Device Binding Conditions 转 GA、CompositePodGroup 升到 scheduling.k8s.io/v1beta1、StatefulSet Recreate 更新策略转 beta，并移除 RecoverVolumeExpansionFailure 与 SupplementalGroupsPolicy 两个 GA 门控。",
  "published":"2026-11-06T00:00:00+00:00","source":"GitHub Releases","source_cat":"基础设施",
  "extra":{},"board":"基础设施","category":"K8s 核心","oss":True,"hot_score":16,"is_hot":False},
 {"title":"Istio 1.31.4：security release，ambient 模式 mTLS 可被绕过（CVSS 8.2）",
  "url":"https://github.com/istio/istio/releases/tag/1.31.4",
  "summary":"Istio 1.31.4 为纯安全版本，含 5 个 CVE：ambient 模式下端口级 STRICT PeerAuthentication 因运算符优先级错误被跳过，明文流量可打到要求 mTLS 的端口（8.2）；任意持有 mesh 身份的负载发 istio.io/debug xDS 请求可打崩 istiod（7.7）；复用 4-tuple 的新连接可命中陈旧 conntrack 绕过 sidecar（7.4）；空 to/from 的 AuthorizationPolicy 让 istiod 崩溃循环（6.3）。",
  "published":"2026-11-06T00:00:00+00:00","source":"GitHub Releases","source_cat":"基础设施",
  "extra":{},"board":"基础设施","category":"K8s 核心","oss":True,"hot_score":15,"is_hot":False},
]
for g in gap:
    if g["url"] not in have:
        items.append(g); have.add(g["url"])
json.dump(items, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("processed.json now", len(items))
