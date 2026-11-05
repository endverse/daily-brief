import json
P="processed.json"
items=json.load(open(P))
have={i["url"] for i in items}
gap=[
 {"title":"HAMi v2.11.0：Flexible-MIG、Cluster Autoscaler 与 Remote CUDA",
  "url":"https://github.com/Project-HAMi/HAMi/releases/tag/v2.11.0",
  "summary":"HAMi 2.11.0 的关键能力：Flexible-MIG 及其实时用量监控、支持 Cluster Autoscaler、Remote CUDA 让 vLLM 跑在远端 GPU 上、GPU/CPU NUMA 对齐、PodGroup 与 mutex 调度策略、完整 AMD 支持与昇腾 950。整卡分配不再挂载 hami-core，指标改由 NVML 直出。",
  "published":"2026-11-04T00:00:00+00:00","source":"GitHub Releases","source_cat":"基础设施",
  "extra":{},"board":"基础设施","category":"K8s × AI","oss":True,"hot_score":18,"is_hot":False},
 {"title":"CoreDNS v1.15.0：DNS-over-QUIC 上游、JSON 查询日志，修 7 个 CVE",
  "url":"https://github.com/coredns/coredns/releases/tag/v1.15.0",
  "summary":"CoreDNS 1.15.0 支持 DNS-over-QUIC 上游、可选 JSON 结构化查询日志、RFC 2136 认证动态更新、PROXY protocol v2 元数据；用 Go 1.27.3 构建，覆盖 CVE-2026-56865 等 7 个 CVE。",
  "published":"2026-10-21T00:00:00+00:00","source":"GitHub Releases","source_cat":"基础设施",
  "extra":{},"board":"基础设施","category":"K8s 核心","oss":True,"hot_score":15,"is_hot":False},
 {"title":"etcd v3.7.3：修 MVCC 数据竞争与 MsgApp 逆序导致的性能回退",
  "url":"https://github.com/etcd-io/etcd/releases/tag/v3.7.3",
  "summary":"etcd 3.7.3 修 MVCC store 中 Hash 与 Restore 之间的数据竞争、keys-only RangeStream 的数据竞争，以及 leader 逆序向 follower 发送 MsgApp 造成的性能回退。",
  "published":"2026-10-22T00:00:00+00:00","source":"GitHub Releases","source_cat":"基础设施",
  "extra":{},"board":"基础设施","category":"K8s 核心","oss":True,"hot_score":14,"is_hot":False},
 {"title":"Argo CD v3.6.1：修 UI 侧栏状态与 --rootpath 失效",
  "url":"https://github.com/argoproj/argo-cd/releases/tag/v3.6.1",
  "summary":"Argo CD 3.6.1 修切换侧栏后布局不同步，以及 webpack 压缩 index.html 导致 --rootpath/--basehref 失效的问题。",
  "published":"2026-11-04T00:00:00+00:00","source":"GitHub Releases","source_cat":"基础设施",
  "extra":{},"board":"基础设施","category":"云原生周边","oss":True,"hot_score":12,"is_hot":False},
 {"title":"Kubeflow Trainer v2.4.0-rc.1",
  "url":"https://github.com/kubeflow/trainer/releases/tag/v2.4.0-rc.1",
  "summary":"Kubeflow Trainer 发布 v2.4.0-rc.1，进入 2.4 线的候选版本阶段。",
  "published":"2026-11-04T00:00:00+00:00","source":"GitHub Releases","source_cat":"基础设施",
  "extra":{},"board":"基础设施","category":"K8s × AI","oss":True,"hot_score":11,"is_hot":False},
]
for g in gap:
    if g["url"] not in have:
        items.append(g); have.add(g["url"])
json.dump(items, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("processed.json now", len(items))
