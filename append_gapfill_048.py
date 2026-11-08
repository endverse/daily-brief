import json
P = "processed.json"
items = json.load(open(P))
have = {i["url"] for i in items}
gap = [
 {"title": "Kubernetes 存储分层拆解：Volume、PV、PVC、StorageClass、CSI 各管哪一段",
  "url": "https://kubezilla.io/kubernetes-storage-explained-volumes-pv-pvc-storageclass-csi/",
  "summary": "文章把 K8s 存储拆成五层讲：Volume 是 Pod 内可挂载的目录（emptyDir 随 Pod 生命周期消失，configMap/secret 做注入）；PV 是集群级存储资源、PVC 是用户侧的申领，两者经 StorageClass 的动态供应绑定；实际读写由 CSI 驱动落到后端存储。作者强调分层的目的——把「申领意图」「供应策略」「驱动实现」解耦，换成一条 hands-on 示例走完 PVC→PV→挂载。",
  "published": "2026-11-06T07:19:54+00:00", "source": "kubezilla.io", "source_cat": "基础设施",
  "extra": {}, "board": "基础设施", "category": "K8s 核心技术", "oss": False, "hot_score": 8, "is_hot": False},
 {"title": "Kubernetes 版本节奏、支持窗口与 version skew：升级前要对的几张表",
  "url": "https://kubezilla.io/kubernetes-release-cycle-upgrades-version-skew-explained/",
  "summary": "把 K8s 的 x.y.z 语义、三个 minor/年的发布节奏、每个 minor 约 14 个月的支持窗口、组件间允许的 version skew（kubelet 可比 apiserver 落后若干 minor、kube-proxy/controller-manager 的约束各不相同）和 API 弃用流程收在一处，末尾给 kubeadm 官方升级流程与一份可复用的升级 checklist（含托管集群）。",
  "published": "2026-11-05T07:29:30+00:00", "source": "kubezilla.io", "source_cat": "基础设施",
  "extra": {}, "board": "基础设施", "category": "K8s 核心技术", "oss": False, "hot_score": 8, "is_hot": False},
 {"title": "用 Backstage + Crossplane 搭 IDP：CNCF 平台白皮书的「薄平台」口径",
  "url": "https://kubezilla.io/platform-engineering-kubernetes-backstage-crossplane-idp/",
  "summary": "按 CNCF TAG App Delivery 的平台白皮书解释 IDP：平台是一组围绕使用者需求整合的能力，可以薄到只覆盖「每个团队都要重复解决的那几件事」（数据库、CI/CD、仪表盘、安全基线）。文章把 Backstage 定位为开发者入口与软件目录、Crossplane 定位为用 K8s API 声明式供应云资源，两者拼成「自助 + 受控」的平台骨架，而不是再造一套 PaaS。",
  "published": "2026-11-04T07:23:44+00:00", "source": "kubezilla.io", "source_cat": "基础设施",
  "extra": {}, "board": "基础设施", "category": "云原生周边", "oss": False, "hot_score": 7, "is_hot": False},
 {"title": "Kueue v0.19.12：ConcurrentAdmission 配额泄漏与 MultiKueue 重复执行修掉了",
  "url": "https://github.com/kubernetes-sigs/kueue/releases/tag/v0.19.12",
  "summary": "0.19 线补丁版：ConcurrentAdmission 删掉 concurrentAdmissionPolicy 后残留的 parent/variant Workload 会永久占着配额，此版清理；变体生成时改父 Workload 元数据、覆盖兄弟变体 flavor 注解的问题一并修掉。MultiKueue 侧修了 worker 集群被移出配置后 Workload 已驱逐但 Job 仍在跑、导致同一 Job 跑两遍的 bug。可观测性上把 job reconciler 的逐 Job 日志降到 verbosity 3、错误只记一次，日志 key 改名（oldQueueName/newQueueName → prevLocalQueue/localQueue），依赖日志的看板要同步改。",
  "published": "2026-11-05T00:00:00+00:00", "source": "GitHub Releases", "source_cat": "基础设施",
  "extra": {}, "board": "基础设施", "category": "K8s × AI", "oss": True, "hot_score": 13, "is_hot": False},
]
for g in gap:
    if g["url"] not in have:
        items.append(g)
        have.add(g["url"])
json.dump(items, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("processed.json now", len(items))
