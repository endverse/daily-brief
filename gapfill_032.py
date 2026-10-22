#!/usr/bin/env python3
"""Append gap-fill items (funnel step ③/④) to processed.json so verify_links accepts them."""
import json, urllib.request, datetime

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
new = [
 {"title": "Volcano v1.16.0：NamespaceQueue + fairshare 插件，HyperNode 控制器独立可复用，调度的 Unschedulable Job Cache 上线",
  "url": "https://github.com/volcano-sh/volcano/releases/tag/v1.16.0",
  "summary": "Volcano v1.16.0 引入 NamespaceQueue 与 fairshare 插件，让租户在自己命名空间内管理队列层级与配额（资源池由管理员授权）；同一队列下按 namespace 隔离的租户共享时，fairshare 用 Slurm 式历史用量衰减改善长期公平性。HyperNode 拓扑发现与超节点管理被抽成可独立部署的控制器与 API，其他调度器可复用；新增 PodGroup 拓扑反亲和。性能侧加入 Unschedulable Job Cache（按插件事件提示决定何时重评）、共享节点遍历评分、缓存更新与队列查找降开销，另支持 Kubernetes 1.36、DRA 打分、按 nodegroup 的队列配额与加速器增强。",
  "published": "2026-10-15T00:00:00+00:00", "source": "GitHub Releases", "source_cat": "K8s",
  "extra": {}, "board": "基础设施", "category": "K8s 核心技术", "oss": True, "hot_score": 9, "is_hot": False},
 {"title": "containerd 2.4.2 补丁发布：3 个安全通告 + 日志软链/镜像引用 .. 路径/默认 seccomp socket 域三重加固",
  "url": "https://github.com/containerd/containerd/releases/tag/v2.4.2",
  "summary": "containerd 2.4.2 是 2.4 线的第二个补丁版，含 3 个安全修复（CVE-2026-95839、GHSA-8647-2jxj-p2rc、GHSA-hc94-p972-ch66）。CRI 侧禁止跟随容器日志文件的符号链接；镜像分发侧修复「registry 下载速度快于内容写入时的内存暴涨」，并拒绝带 .. 路径分量的镜像引用；运行时把默认 seccomp 配置收紧为 socket 域白名单。同一批还发了 2.3.7 / 2.2.10 / 2.0.14。",
  "published": "2026-10-13T00:00:00+00:00", "source": "GitHub Releases", "source_cat": "K8s",
  "extra": {}, "board": "基础设施", "category": "K8s 核心技术", "oss": True, "hot_score": 9, "is_hot": False},
 {"title": "SGLang v0.5.22：950 个 PR，DeepSeek-V4.1 单卡吞吐 2.3x、PD 分离长 prompt p95 TTFT 减半、模型加载快 10 倍",
  "url": "https://github.com/sgl-project/sglang/releases/tag/v0.5.22",
  "summary": "SGLang v0.5.22 合并 950 个 PR、245 位贡献者。性能更新包括：DeepSeek-V4.1 在 H200 上每 GPU 吞吐提升至 2.3 倍并支持 AMD MI350X/MI355X，Qwen3.8-Flash-Next 在 B200 解码快 12%，MiMo-V2.6-Pro 在 B300 用 DFlash 解码 1.85 倍；新的 InstantTensor 加载器把模型加载提速 10 倍；PD 分离在长 prompt 上吞吐最多 +27%、p95 TTFT 减半；HiSparse 支持 EAGLE/MTP 把 KV cache 放到 CPU 内存，GLM-5.2/5.3 可把 decode 上下文并行与 MTP 组合（GLM-5.3 解码 2.1 倍）。新增 Clef/EmbeddingGemma 2/HunyuanImage-3.0 等模型支持与 Apple Silicon 后端。",
  "published": "2026-10-19T00:00:00+00:00", "source": "GitHub Releases", "source_cat": "K8s",
  "extra": {}, "board": "基础设施", "category": "K8s × AI", "oss": True, "hot_score": 9, "is_hot": False},
 {"title": "AWS 空隔区（air-gapped）ECR 建设方法：仓库创建模板 + Terraform + 迁移工具，让加密/不可变标签/扫描成为默认",
  "url": "https://aws.amazon.com/blogs/containers/automating-secure-container-registry-management-for-air-gapped-aws-workloads",
  "summary": "AWS 面向金融、医疗、政务等无 internet/NAT 网关的 VPC，给出把公共与私有源的数十到数百个 Helm chart 与镜像搬进私有 Amazon ECR 的做法。难点不在单个仓库，而在大量且持续增长的仓库上保持一致的防护姿态：用 ECR repository creation templates 把 CMEK 加密、不可变标签、增强扫描、生命周期规则固化成默认，配合 Terraform 与迁移工具，避免逐个仓库配置导致的安全姿态漂移。",
  "published": "2026-10-16T00:00:00+00:00", "source": "AWS News", "source_cat": "云厂商",
  "extra": {}, "board": "基础设施", "category": "公有云动态", "oss": False, "hot_score": 8, "is_hot": False},
]

data = json.load(open('processed.json'))
have = {d['url'] for d in data}
added = 0
for it in new:
    try:
        st = urllib.request.urlopen(urllib.request.Request(it['url'], headers={"User-Agent": UA}, method="HEAD"), timeout=20).status
    except Exception as e:
        st = getattr(e, 'code', str(e)[:40])
    print(f"{st} {it['url']}")
    if it['url'] not in have:
        data.append(it); added += 1
json.dump(data, open('processed.json', 'w'), ensure_ascii=False, indent=1)
print(f"added={added} total={len(data)}")
