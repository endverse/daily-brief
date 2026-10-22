#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 032 (2026-10-22) from processed.json (URLs machine-copied)."""
import json

PROC = json.load(open('processed.json'))
BY_URL = {p['url']: p for p in PROC}


def U(*variants):
    """Return the original processed.json URL matching any prefix variant (?query kept)."""
    for v in variants:
        for url in BY_URL:
            if url.split('?')[0].rstrip('/') == v.rstrip('/'):
                return url
    raise SystemExit(f"URL NOT IN processed.json: {variants}")


def S(*variants):
    return BY_URL[U(*variants)]['source']


H = []

H.append({
    "title": "OpenAI 案例：Terminal X 的 Eval Agent 按 54 条 rubric 给投资建议打分，与资深投资人一致率 88.6%",
    "url": U("https://openai.com/index/terminal-x"),
    "summary": "OpenAI 10 月 20 日发布的客户案例里，资管 SaaS 公司 Terminal X 把机构的投资流程、历史决策与内部观点编码成客户自有的 agent（Capital Memory），部署在本地或客户自己的云上。它的 Eval Agent 按 54 条 rubric 逐项判定一段分析——来源准确性、论证连贯性、是否符合基金 mandate——每项只给 pass/fail，失败项附解释与修正文本或更可靠的来源，修正结果再回流成后续工作流的指令与测试用例。在 500 次打分中，跑 GPT-6.1 Sol 的 Eval Agent 与资深投资人一致率 88.6%，次优模型 86.4%（+220 个基点），偏离 mandate 的建议多抓出约 25%，单次查询成本低约 30%。这些数字全部来自厂商自述案例、未经独立审计，OpenAI 与 Terminal X 都把它定位成「工作流控制工具」而不是交易信号。",
    "note": "🔎 新闻要点：54 条 rubric（来源准确性 / 论证连贯 / mandate 对齐）逐项判定；500 次判定与资深评审一致率 88.6%，次优 86.4%；mandate 偏离多抓 25%；单查询成本 -30%；agent 本地或客户云部署；结果为 vendor-reported。",
    "tag": "Agent 落地", "source": S("https://openai.com/index/terminal-x"),
    "detail": [
        {"key": "能做什么", "value": "把「资深投资人的判断」拆成可执行的评分器：54 条 rubric 逐项 pass/fail，失败项自动生成解释与修正文本/更可靠来源，并把修正结果回灌成后续工作流指令与测试用例，形成「评审—修正—再测试」的闭环；agent 部署在本地或客户自有云，数据不出域。"},
        {"key": "解决什么痛点", "value": "资管里合规与投研复核是人力密集且标准难统一的环节：同一条建议不同评审给的结论不一致，mandate 偏离往往在事后才被发现。把 rubric 化评审交给 agent，等于把「一致性与可追溯」做进流程，而不是靠人盯。"},
        {"key": "值不值得", "value": "值得追的是「用 rubric + 失败修正回流做评测」这个模式，而不是 88.6% 这个数——样本 500 次、无独立审计、且是与「资深评审」比一致率而非与真实业绩比。若要复用到自家场景，门槛在 rubric 的编写质量与失败样本的闭环治理；先从一个高频、低风险的复核环节试点。"}
    ]
})

H.append({
    "title": "DeepSeek 开源推理框架 DeepInfer：单集群日吞吐 155 万亿 Token，KVCache 落 3FS 保存 3–7 天",
    "url": U("https://www.infoq.cn/article/NBXP966Bz3eqr6Qidvaf"),
    "summary": "10 月 20 日 DeepSeek 开源大规模云服务推理框架 DeepInfer（已用于 V4.1 Flash 线上推理），同时开源生产级 Token 编解码组件 deepseek-recipe；KVCache 管理与负载均衡因与内部基础设施耦合较深暂未完整开源。架构上把视觉编码器、Prefill、Decode 三段分开部署：Prefill 用常见 8 卡服务器、Decode 用 64–128 卡超节点，MoE 在 Prefill 侧 2–8 路专家并行、Decode 侧扩到 64–128 路 Wide-EP，并按未命中 Token 数与实际计算请求数分别对两侧自动扩缩容。KVCache 被做成集群级共享数据层：以 128 Token 为 Block 分页写入独立 3FS 集群（约 100 PiB SSD），Agent 流量 TTL 3 天、Chatbot 7 天，峰值聚合读 10 TiB/s、写约 850 GiB/s，从而不必做前缀亲和路由。SWA 部分改用 Bounded Replay，缺失时只重算尾部 128 Token，官方称总 Prefill 计算量接近减半；推测解码框架 DSpark 按预测接受率变长验证，比固定验证 5 个 Token 吞吐高 6%。线上单集群日吞吐 155 万亿 Token，按谷价折算每卡每小时 38 美元。",
    "note": "🔎 新闻要点：Prefill(8 卡)/Decode(64–128 卡超节点) 分离 + Wide-EP 64–128 路；KVCache 128 Token/Block 落 3FS，约 100 PiB，TTL Agent 3 天、Chatbot 7 天；3FS 峰值读 10 TiB/s、写 850 GiB/s；SWA Bounded Replay 只重算尾部 128 Token，Prefill 计算量近半；DSpark 变长验证 +6% 吞吐；单集群 155 万亿 Token/天、每卡每小时 38 美元。",
    "tag": "推理引擎", "source": S("https://www.infoq.cn/article/NBXP966Bz3eqr6Qidvaf"), "oss": True,
    "detail": [
        {"key": "能做什么", "value": "一套面向超大规模在线服务的推理系统：PD 分离部署（8 卡 Prefill / 64–128 卡 Decode 超节点）、Wide-EP 大专家并行、集群级 KVCache（3FS 持久化 + 分页 Block + 400G VLAN 拉取）、四类专用负载均衡器（Prefill/Decode/视觉编码/专家并行），以及 CPU-GPU 异步流水调度。附带 deepseek-recipe 做 API 协议到内部 Token 序列的转换（Rust 实现，防特殊 Token 注入）。"},
        {"key": "解决什么痛点", "value": "长上下文与 agent 历史让重复 prefill 成本爆炸；固定容量比例会在流量波动时一边排队一边空转；大 EP 下任一卡故障整实例报废、重启是分钟级。DeepSeek 的解法是「冗余配额 + 请求级重路由 + 缓存与计算解耦」：持久 KVCache 放在独立存储集群，计算节点故障不丢缓存，存储与计算还能分别扩缩。"},
        {"key": "值不值得", "value": "对自建推理平台的选型极有参考价值——尤其「缓存独立成层、不做前缀亲和路由」这个取舍，会直接影响你的 K8s 侧拓扑（是否需要按前缀做 service 亲和）。注意开源版缺 KVCache 管理与负载均衡，抄不到全貌；3FS 与 64–128 卡超节点也不是普通集群能复现的，先读设计取舍再对号入座。"}
    ]
})

SECTIONS = []

# ---------------- 基础设施 ----------------
infra = {"label": "☸️ 基础设施板块", "categories": []}

infra["categories"].append({
    "emoji": "🤖☸️", "title": "K8s × AI", "en": "K8S × AI", "items": [
        {
            "title": "同一 agent 换上下文：K8s 故障 2 分钟内诊断达标率 86% vs 60%，静默故障 326 秒降到 79 秒",
            "url": U("https://www.cncf.io/blog/2026/10/21/before-you-evaluate-an-ai-sre-give-your-existing-agent-context/"),
            "summary": "Radar（Skyhook.io）的 CPO 在 CNCF 博客公布一组对照实验：在 3 节点 EKS 上，用 Claude Code + Claude Sonnet 5（走 Bedrock）跑 Microsoft/UIUC 的 SREGym 的 50 个注入故障，A 组只有 shell 与裸 kubectl，B 组换成只读 MCP 工具（返回当前在失败的对象与最近的变更）并把 kubectl 屏蔽掉。准确率几乎打平（46 vs 45 个正确，judge 均分 0.936 vs 0.905），差距全在时间：有上下文时 86% 的故障在 2 分钟内给出正确诊断，只有 shell 时是 60%，且后者十分之一的故障超过 10 分钟；在最难的 14 个「Pod 全 Ready 但应用已坏」的静默故障上，平均诊断时间从 326 秒降到 79 秒。两组犯了同样 3 个错（mutating webhook 在 admission 时改写 memory limit、PriorityClass 被误设成全局默认触发抢占、一个 DNS 故障被无关配置错误带偏），说明上下文补的是「知道往哪看」，不是判断力。作者的结论是：先给你已有的 agent 只读的失败上下文并测基线，再评估 AI SRE 产品；SREGym 有 Claude Code/Codex/Copilot/Cursor/Gemini CLI/OpenCode 的驱动，Lite 套件 17 题能在 kind（8 vCPU/16GB）上跑，每故障回放也已公开。",
            "tag": "Agent 可观测性", "source": S("https://www.cncf.io/blog/2026/10/21/before-you-evaluate-an-ai-sre-give-your-existing-agent-context/"),
            "detail": [
                {"key": "能做什么", "value": "把「K8s 故障诊断 agent」拆成可测的两件事：模型判断力（换上下文几乎不变）与信息获取（差 4 倍以上）。实验给出可复现的评测装置：SREGym 50 个注入故障 + 只读 MCP 上下文 + judge 模型打分 + 固定时间窗（2/5 分钟），并且给了不给 admin 权限的 kubeconfig 造法（view ClusterRole + 8 小时 token）。"},
                {"key": "解决什么痛点", "value": "agent 排查集群时最贵的不是 token 而是「不知道正在发生什么」：裸 kubectl 要自己拼一堆命令，碰到 Pod 全 Ready 的静默故障就瞎猜。只读、结构化的失败上下文（失败对象 + 最近变更 + 依赖关系）把这部分搜索成本直接砍掉。"},
                {"key": "值不值得", "value": "很值得照着做一次内部基线：成本是 kind 集群 + 一晚上，收益是知道「买 AI SRE 之前自己的 agent 已经能做到什么」。注意作者维护 Radar（MCP 服务端），结论有立场；且两组权限不同（只有 shell 组能写），不能完全归因于上下文类型。"}
            ]
        },
        {
            "title": "GKE Inference Gateway + llm-d：ZenteiQ 批量合成数据吞吐 4.07 倍，每千卡日产 14.7 亿→59.7 亿 Token",
            "url": U("https://cloud.google.com/blog/products/containers-kubernetes/zenteiq-scales-physical-ai-inference-4x-with-gke-and-llm-d/"),
            "summary": "从印度理工（IISc）分拆、入选 IndiaAI Mission 的 ZenteiQ 在 GKE 上跑科学基础模型的批量合成数据流水线：worker pod 准备 prompt，vLLM 在多个加速卡节点池上做生成、评分与护栏，通过的样本打包后喂给 MaxText 预训练。原来用 ClusterIP 轮询做端点负载均衡，出现两个瓶颈——各副本队列不均（吞吐波动大）与重复 prefill。换成 GKE Inference Gateway（由 llm-d 驱动）后，路由按 vLLM 实例的实时队列深度与 KV cache 利用率决策，并把共享同一段科学指令前缀的请求送到该前缀 KV cache 已热的节点（每条 prompt 有 70%–80% 是共享指令上下文），从而跳过重复 prefill 又不压垮单个副本。结果是聚合推理吞吐 4.07 倍、每 1000 张加速卡日产 Token 从 14.7 亿涨到 59.7 亿，下游多机预训练不再等数据、能按计划开跑。",
            "tag": "推理路由", "source": S("https://cloud.google.com/blog/products/containers-kubernetes/zenteiq-scales-physical-ai-inference-4x-with-gke-and-llm-d/"),
            "detail": [
                {"key": "能做什么", "value": "把「批量生成 + 评分 + 护栏」的多模型池收在一个网关后面：请求按实时队列深度与 KV cache 命中路由，而不是 round-robin；同一前缀的请求聚到 KV 已热的副本，跳过重复 prefill。适配的是「共享长前缀、生成内容各异」的批量合成数据负载，官方数据 4.07 倍吞吐。"},
                {"key": "解决什么痛点", "value": "批量数据生成的本质瓶颈是集群利用率而非单卡性能：轮询会让长推导请求堆在某个副本后面，邻居节点却空转；同时固定算力配额下，数据生成慢了就直接占掉预训练时间。"},
                {"key": "值不值得", "value": "如果自建推理集群里存在「一条 prompt 大部分是共享上下文、尾部各不相同」的负载（RAG、批量评测、合成数据），这套 cache-aware 路由就是最直接的降本手段，且 llm-d 是开源的。门槛是 GKE 侧托管省事、自建要自己搭 Gateway API Inference 扩展与 KV 事件通道。"}
            ]
        },
        {
            "title": "SGLang v0.5.22：DeepSeek-V4.1 每卡吞吐 2.3 倍，PD 分离长 prompt p95 TTFT 减半，模型加载快 10 倍",
            "url": U("https://github.com/sgl-project/sglang/releases/tag/v0.5.22"),
            "summary": "SGLang v0.5.22 合并 950 个 PR、245 位贡献者。性能侧：DeepSeek-V4.1 在 H200 上每 GPU 吞吐最高 2.3 倍并支持 AMD MI350X/MI355X，Qwen3.8-Flash-Next 在 B200 解码快 12%，MiMo-V2.6-Pro 在 B300 用 DFlash 解码 1.85 倍；新的 InstantTensor 加载器把模型加载提速 10 倍；PD 分离在长 prompt 负载上吞吐最高 +27%、p95 TTFT 减半；HiSparse 支持 EAGLE 与 MTP，把 KV cache 放到 CPU 内存做长上下文服务；GLM-5.2/5.3 可把 decode 上下文并行与 MTP 组合，GLM-5.3 解码快 2.1 倍。另修了一个重要 bug：投机解码与结构化输出同开时，混合线性模型可能从错误的 mamba 状态恢复。",
            "tag": "推理引擎", "source": S("https://github.com/sgl-project/sglang/releases/tag/v0.5.22"), "oss": True,
            "detail": [
                {"key": "能做什么", "value": "一个版本里同时把单卡效率（DFlash 投机解码、InstantTensor 10 倍加载）、集群侧效率（PD 分离 +27% 吞吐、p95 TTFT 减半）与长上下文（HiSparse 把 KV 放 CPU 内存）推进；新增 Clef、EmbeddingGemma 2、HunyuanImage-3.0 等模型支持，并跑通 Apple Silicon。"},
                {"key": "解决什么痛点", "value": "推理集群的常见病是「模型加载几分钟、长 prompt 第一 token 等很久、KV 显存不够」。这三个数字分别对着冷启动、TTFT 和长上下文成本。"},
                {"key": "值不值得", "value": "自建推理服务的话这是必看的 patch 级升级：升级成本低（镜像 tag 一改），收益是 p95 延迟与加载时间。升级前只需确认自家模型在 changelog 的兼容列表内，并注意那个「投机解码 + 结构化输出」的 mamba 状态 bug 是否命中你的模型。"}
            ]
        },
        {
            "title": "是石科技 TokenFleet：把推理集群调度拆成选点 / 跨机房 / 混合负载三件，宣称首 Token 延迟降 32.4%",
            "url": U("https://www.qbitai.com/2026/10/504421.html"),
            "summary": "第三方算力运营商是石科技（METASTONE）在 2026 CCF 全国高性能计算学术大会上发布 TokenFleet 分布式调度框架，把优化目标定成「成功完成且满足服务等级要求的有效 Token 产出」，而不是单纯的 QPS。三个组件分工：TokenPilot 在同一模型池内选实例（按输入长度档位与 KV cache 命中挑点）、FleetMind 做跨机房容量协同、SLOMax 负责混合负载的准入、队列治理与容量分配；针对短对话、长文档、离线批任务混跑时「部分实例排队、其他容量闲置」以及超时/取消/重复计算白烧算力的问题。官方称首 Token 延迟降低 32.4%，其集群 SLA 99.95%、纳管 2 万 P+ 算力、运营 10 多个智算中心（含 2 个国家级超算中心），此前还发布过单实例优化引擎 Meta-Infer。",
            "tag": "集群调度", "source": S("https://www.qbitai.com/2026/10/504421.html"),
            "detail": [
                {"key": "能做什么", "value": "把「请求分给谁、任务何时进队列、多机房容量怎么协同」统一到一个指标（有效 Token 产出 / 单位成本）下：按长度档位与 KV 命中选点、跨机房容量池化、混合负载准入与配额治理。"},
                {"key": "解决什么痛点", "value": "多模型、多租户、多机房下的推理集群，靠简单分流会同时出现排队与闲置；长请求挤占实时交互，超时与重算又形成沉没成本。"},
                {"key": "值不值得", "value": "方向（调度决定有效吞吐）与 DeepSeek/llm-d 的结论一致，可当作国产推理调度的思路参照。但这是厂商自述产品文、无 benchmark 细节、未开源，32.4% 无法验证；不建议据此做选型，值得记的是「以有效 Token 为单位做成本核算」这个口径。"}
            ]
        },
    ]
})

infra["categories"].append({
    "emoji": "☸️", "title": "K8s 核心技术", "en": "KUBERNETES CORE", "items": [
        {
            "title": "Volcano v1.16.0：NamespaceQueue + fairshare 插件，HyperNode 控制器独立可复用，Unschedulable Job Cache 上线",
            "url": U("https://github.com/volcano-sh/volcano/releases/tag/v1.16.0"),
            "summary": "Volcano v1.16.0 引入 NamespaceQueue 与 fairshare 插件：租户可在自己命名空间内管理队列层级与配额（资源池由管理员授权），当 namespace 隔离的租户共享同一队列时，fairshare 用 Slurm 式历史用量衰减改善长期公平性。HyperNode 的拓扑发现与超节点管理被抽成可独立部署的控制器与 API，其他调度器也能复用；新增 PodGroup 拓扑反亲和，把工作负载实例分散到不同拓扑域。性能侧加入 Unschedulable Job Cache（按插件事件提示决定何时重评，默认 5 分钟看门狗）、节点评分共享遍历、缓存更新与队列查找降开销；另支持 Kubernetes 1.36、DRA 打分、按 nodegroup 的队列配额与加速器增强。",
            "tag": "批调度", "source": S("https://github.com/volcano-sh/volcano/releases/tag/v1.16.0"), "oss": True,
            "detail": [
                {"key": "能做什么", "value": "多租户批调度三件套：namespace 内自助建队列与配额、Slurm 式 fairshare 历史衰减、PodGroup 拓扑反亲和；大规模 pending 积压时用 Unschedulable Job Cache 跳过重复的准入检查（记录拒绝原因 + 事件驱动唤醒 + gang 需求仍可见）。"},
                {"key": "解决什么痛点", "value": "AI/批任务的集群里 pending backlog 很大时，每轮调度都为同一批不可调度的 Job 重复算一遍，调度器自己成了瓶颈；跨团队共享队列时又缺长期公平性度量。"},
                {"key": "值不值得", "value": "自建 K8s 跑训练/批推理的话，这一版同时解决「调度器吞吐」与「多租户公平」两个实际痛点，且 HyperNode 抽成独立控制器后，混用 Kueue/其他调度器的集群也能接入拓扑感知。升级主要风险在 CRD 与队列层级迁移，先在测试集群验证 gang 调度与抢占行为。"}
            ]
        },
        {
            "title": "containerd 2.4.2：3 个安全通告，日志软链 / 镜像引用 .. 路径 / 默认 seccomp socket 域三重加固",
            "url": U("https://github.com/containerd/containerd/releases/tag/v2.4.2"),
            "summary": "containerd 2.4.2 是 2.4 线第二个补丁版，含 3 个安全修复（CVE-2026-95839、GHSA-8647-2jxj-p2rc、GHSA-hc94-p972-ch66）。CRI 侧改为不跟随容器日志文件的符号链接；镜像分发侧修掉「registry 下载速度快于内容写入时的内存暴涨」，并拒绝带 .. 路径分量的镜像引用；运行时把默认 seccomp 配置收紧为 socket 域白名单。同批还发了 2.3.7 / 2.2.10 / 2.0.14。",
            "tag": "容器运行时", "source": S("https://github.com/containerd/containerd/releases/tag/v2.4.2"), "oss": True,
            "detail": [
                {"key": "能做什么", "value": "一个补丁版同时堵三类入口：日志路径的符号链接逃逸、镜像引用里的路径穿越、以及默认 seccomp 允许的 socket 域过宽；另修拉镜像时内容写入跟不上导致的内存暴涨。"},
                {"key": "解决什么痛点", "value": "容器运行时是节点上的最高权限组件之一，这类「软链 + 路径 + 系统调用面」的小洞在生产里往往被镜像拉取与日志采集这两条高频路径放大。"},
                {"key": "值不值得", "value": "属于「该排进下一次节点滚动升级」的补丁：影响面是节点组件而非业务，但节点重启要按批次做。升级前确认 containerd 版本线（2.4/2.3/2.2/2.0 都有对应补丁）与 CRI 配置兼容。"}
            ]
        },
    ]
})

infra["categories"].append({
    "emoji": "☁️", "title": "公有云动态", "en": "PUBLIC CLOUD", "items": [
        {
            "title": "AWS 空隔区 ECR 建设方法：仓库创建模板 + Terraform，把加密 / 不可变标签 / 扫描做成默认",
            "url": U("https://aws.amazon.com/blogs/containers/automating-secure-container-registry-management-for-air-gapped-aws-workloads"),
            "summary": "AWS 面向没有 internet 网关与 NAT 的 VPC（金融、医疗、政务、国防常见）给出把数十到数百个 Helm chart 与镜像搬进私有 ECR 的做法。真正的难点不是单个仓库，而是在持续增长的仓库集合上保持一致的防护姿态：用 ECR repository creation templates 把 CMEK 加密、不可变镜像标签、增强扫描与生命周期规则固化成新仓库的默认值，再配合 Terraform 与迁移工具，让「安全默认」成为最省力的路径。文中以一家受强监管的欧洲金融机构为例。",
            "tag": "离线集群", "source": S("https://aws.amazon.com/blogs/containers/automating-secure-container-registry-management-for-air-gapped-aws-workloads"),
            "detail": [
                {"key": "能做什么", "value": "用仓库创建模板（creation template）+ IaC 把「每个新 ECR 仓库都必须 CMEK 加密、标签不可变、开增强扫描、有生命周期规则」变成结构性默认，而不是靠 checklist 逐个人工配置；迁移工具负责把公共/私有源的 chart 与镜像批量搬进边界内。"},
                {"key": "解决什么痛点", "value": "空隔区集群上线前必须把全部依赖搬进边界内，仓库数量多且持续增长时，配置漂移会让某个仓库悄悄少了扫描或用了可变标签——这类问题在审计时才暴露。"},
                {"key": "值不值得", "value": "做金融/受监管环境的私有镜像仓库时值得照抄这个结构：模板化 + IaC 才是可持续的，脚本一次性搬完迟早漂移。注意这是 AWS ECR 特性绑定的做法，Harbor/其他 registry 要自己找等价物（项目级策略、复制规则、不可变 tag 策略）。"}
            ]
        },
        {
            "title": "Confidential G4 正式可用：G4 实例上的 NVIDIA Blackwell 机密计算 GA，覆盖 agent 处理敏感数据的场景",
            "url": U("https://cloud.google.com/blog/topics/ai-infrastructure/confidential-g4-gpus-are-ga/"),
            "summary": "Google Cloud 宣布 G4 实例上基于 NVIDIA RTX PRO 6000 Blackwell 的机密计算正式可用（GA）。官方给出的场景是把自主 agent 放进生产后要同时处理敏感数据与模型权重、prompt 与输出，需要在计算过程中也保持数据受保护；机密 GPU 让这些内容在推理时仍处于加密隔离的信任域内，而不是只保护静态存储与传输。",
            "tag": "机密计算", "source": S("https://cloud.google.com/blog/topics/ai-infrastructure/confidential-g4-gpus-are-ga/"),
            "detail": [
                {"key": "能做什么", "value": "把机密计算的边界从 CPU 扩到 GPU：G4 + RTX PRO 6000 Blackwell 上的推理负载，权重与 prompt 在计算中保持受保护，可对「数据不能出信任域」的合规要求给出技术答案。"},
                {"key": "解决什么痛点", "value": "金融/医疗把模型托管到公有云时，最大的阻力是「跑起来的那一刻数据是明文」；纯传输与静态加密过不了内部安全评审。"},
                {"key": "值不值得", "value": "做受监管行业上云评估时，这是公有云 GPU 方案里少数能直接回应「计算中数据保护」的选项；但机密 GPU 会带来吞吐损耗与机型/区域限制，且信任链还包含 attestation 与密钥管理，需要端到端验证而不是只看 GA 标签。"}
            ]
        },
    ]
})

SECTIONS.append(infra)

# ---------------- AI 板块 ----------------
ai = {"label": "🤖 AI 板块", "categories": []}

ai["categories"].append({
    "emoji": "🧩", "title": "Agent & Skill", "en": "AGENT & SKILL", "items": [
        {
            "title": "Cloudflare 开源 Clef 决策模型：27B 一次前向输出各选项概率，9B 版中位延迟 38.8ms",
            "url": U("https://www.infoq.cn/article/iqCrZLLizNkRTpfo2Jrb"),
            "summary": "Cloudflare 在「生日周」发布 Clef——一组开源权重的决策模型，不做自由生成，而是在预设选项之间做选择。270 亿参数的多模态版本接收「状态 + 带类型问题的 Schema」，可吃文本、JSON、图像或视频，一次前向推理就返回每个问题所有可选项的概率；9B 的 Clef-Flash 面向延迟敏感场景，官方基准中位延迟 38.8ms（27B 为 209.3ms）。与 Typesafe 的 Jev System Once 相比，Clef 多了视觉编码器、上下文 64k（Jev 32k）。模型托管在 Cloudflare 边缘 GPU 上，可通过 Workers AI 调用，权重在 Hugging Face 可下载，另提供用客户自有数据微调的服务。HN 上的争议集中在两点：这是否算新范式，以及公开基准是否可信（有人指出更该测「它知不知道什么时候该放弃判断」）。",
            "tag": "决策模型", "source": S("https://www.infoq.cn/article/iqCrZLLizNkRTpfo2Jrb"), "oss": True,
            "detail": [
                {"key": "能做什么", "value": "把 agent 循环里的「分类/路由/是否升级人工」从生成任务变成分类任务：输入状态 + 类型化 Schema，输出每选项概率，无需解析自由文本；9B 版 38.8ms 中位延迟足以放进同步决策路径，并可与 Workers AI 上的 LLM 串起来做后续动作。"},
                {"key": "解决什么痛点", "value": "用通用 LLM 做路由/分单，成本高、延迟高、输出还要解析和纠错；决策模型把这一步变成结构化概率输出，便于阈值化与降级。"},
                {"key": "值不值得", "value": "如果 agent 里有大量「选一个」的环节（工单分级、工具选择、是否转人工），这一类小模型比再调一次大模型划算得多，且有开源权重可自托管。风险在基准可信度与校准——上线前必须测「该弃权时是否弃权」，而不是只看准确率。"}
            ]
        },
        {
            "title": "HarnessAdapt-RL：训练时连 harness 一起进化，9B 模型 SWE-bench Verified 比 GRPO 高 9.8 个点",
            "url": U("https://huggingface.co/papers/2610.28069"),
            "summary": "这篇论文指出训练 coding agent 时的常见做法是「策略更新、harness 冻结」，但训练轨迹里暴露的失败修复策略与交互问题会随策略变化而漂移。HarnessAdapt-RL 让两者一起演化：对修复策略问题，用冻结的教师模型生成任务级、机制级的 skill；对跨任务复现的交互问题，用另一个教师模型演化工具与 hook，只有观测到的 pass rate 或 trainable rate 提升且互不拉低才保留改动；策略在新 harness 下训练，新轨迹再驱动下一轮适配。9B 基座上，SWE-bench Verified / Multilingual / Pro 上比 GRPO 分别高 9.8、12.6、6.4 个点，也优于用人工设计的 OpenHands harness 的 GRPO；机制级 skill 在评测时移除后增益仍保留，而把演化出的工具与 hook 在部署时移除会掉最多 7.7 个点。",
            "tag": "Agent 训练", "source": S("https://huggingface.co/papers/2610.28069"),
            "detail": [
                {"key": "能做什么", "value": "把「模型 + harness」作为一个整体来优化：教师模型按失败类型分别产出机制级 skill（对修复策略）与工具/hook 改动（对交互问题），改动以观测到的通过率为准入条件，策略与新 harness 交替迭代。"},
                {"key": "解决什么痛点", "value": "冻结 harness 训练出的策略会把 harness 的缺陷学进权重；而手工改 harness 又靠人猜。这条路线把 harness 演进变成可度量的优化步骤。"},
                {"key": "值不值得", "value": "做 agent 训练/微调的话，结论很实用：技能可以在部署时剥离（增益保留），但演化出的工具与 hook 必须一起带走——否则掉 7.7 个点。对只做 harness 工程不训练模型的团队，也有借鉴：把「工具演进」的准入条件写成 pass rate 不下降。"}
            ]
        },
        {
            "title": "TEAL：无标注下让 coding agent 自建工具库，10–15 步预算内 Sonnet-5 在 LakeQA 涨 21.7 个点",
            "url": U("https://huggingface.co/papers/2610.27327"),
            "summary": "数据湖分析类问题没有标准答案标签（要专家先做一遍），所以这篇工作在无监督设定下做工具演进：TEAL 为给定的 Worker agent 演化一套工具库与使用技能，两个 agent 从互补证据提改动——Explorer 从数据湖本身提，Critic 从 Worker 的历史轨迹提；只有当 Worker 重跑时无需额外步骤就采纳该工具、且被改动过的答案有轨迹证据支撑，这项改动才被保留。在 KramaBench 与 LakeQA 上、四个 Worker 模型、严格步数预算下评测：10 或 15 步的紧预算里每个 Worker 都提升，Sonnet-5 在 15 步时 KramaBench +9.3、LakeQA +21.7；在 20 步演化的库拿到 30 步部署，LakeQA 得 68.3，高于基线 59.6 与直接在 30 步演化的 64.2。用合成问题演化的库与真实问题演化的效果相当（TEAL-Q）。",
            "tag": "工具进化", "source": S("https://huggingface.co/papers/2610.27327"),
            "detail": [
                {"key": "能做什么", "value": "让 agent 把每次问答里做过的发现、清洗、join 沉淀成可复用工具，且不需要标签：以「Worker 是否主动采纳」和「答案变化是否有轨迹证据」作为双重准入，避免把偶发结果固化成工具。"},
                {"key": "解决什么痛点", "value": "coding/data agent 每次任务都从头探索同一批表，重复劳动；而有监督的工具学习在真实数据湖里没有 ground truth 可用。"},
                {"key": "值不值得", "value": "对内部数据平台做 agent 的场景很直接：先把「工具库」当成一等资产，用步数预算做压力测试（紧预算下增益更大，说明工具是真复用不是补上下文）。落地门槛是轨迹证据的采集质量，也就是可观测性要先到位。"}
            ]
        },
        {
            "title": "Sage-A1.5：35B MoE 长程 agent 模型，子 agent 隔离上下文 + 过程验证，转向开放式科研",
            "url": U("https://arxiv.org/abs/2610.28578v1"),
            "summary": "Sage-A1.5 是 35B 的 MoE agent 模型，在 A1 基础上把「解单个任务」推进到「组织工作并在执行中修正方法」，三个改动：agentic orchestration 用子 agent 委派与并行协作（各自隔离上下文）来拆解复杂任务、减少并发子 agent 之间的干扰；agentic verification 用进度检查、证据校验与反思式策略修正来提升长程可靠性，让 agent 识别走不通的搜索路径并换路；open scientific discovery 把能力从回答既定问题扩到探索式研究，产出可检查的研究工件。论文以多学科科研任务做展示，定位是给社区一个可及的开源科研 agent 基座。",
            "tag": "长程 agent", "source": S("https://arxiv.org/abs/2610.28578v1"),
            "detail": [
                {"key": "能做什么", "value": "一个 35B MoE 的 agent 模型把编排（子 agent 并行、上下文隔离）、验证（证据校验 + 反思换路）与科研探索（可检查的中间产物）做进同一个模型，而不是外部 harness 拼出来。"},
                {"key": "解决什么痛点", "value": "长程任务的失败多数不是单步能力不够，而是「错了不回头」和「子任务互相污染上下文」；验证与隔离是这类系统的两个结构性缺口。"},
                {"key": "值不值得", "value": "35B 规模意味着单机多卡可部署，适合评估「自托管 agent 模型能不能替代一部分闭源调用」。但论文以展示性任务为主、缺少与主流闭源模型的系统对比，先看它在你自己任务集上的可靠性再谈替换。"}
            ]
        },
        {
            "title": "Épi：跨会话持续的自我改进科研 agent，产出 120 项纪录，算法解题比 Codex 高 5.4% 而成本仅 64%",
            "url": U("https://huggingface.co/papers/2610.24944"),
            "summary": "Épi 是一个能跨模型会话持续同一项研究的自主 agent，靠持久研究历史、分层记忆、分支与独立评审来保持连续性并从实验里学习方法。它的实验跨会话运行、由固定 verifier 评判，共产出 120 项纪录：12 个族的 20 个数值界纪录与 8 个族的 100 个构造纪录，包括 n-queens 常数区间收窄约 84 倍、四次 Feigenbaum 吸引子维数的严格区间收窄超过 360 万倍；还给出 Tuza 猜想在一类 split graph 上的计算机辅助证明。同一套流程的轻量版 Épi-turbo 在 30 个 FrontierOR 任务上比 Codex 总分高 5.4%，只用 64% 的模型成本（同模型、同推理强度）。",
            "tag": "自主研究", "source": S("https://huggingface.co/papers/2610.24944"),
            "detail": [
                {"key": "能做什么", "value": "把「研究」做成有状态的长期进程：记忆 + 分支探索 + 独立评审 + 固定 verifier，让 agent 在多次会话之间接着上次的实验往下做，并能解释自己用的方法与论证。"},
                {"key": "解决什么痛点", "value": "现有 agent 一次会话结束就遗忘，长任务变成反复重启；科研/优化类任务的收益恰恰来自「试错历史」的积累。"},
                {"key": "值不值得", "value": "数字很硬（360 万倍区间收窄、120 项纪录），说明「持久状态 + 验证器」在可验证任务上是真增益；但适用边界是可形式化验证的问题。工程上的可迁移点是 Épi-turbo 的成本结构：同模型下靠流程编排省 36% 成本还更高分。"}
            ]
        },
        {
            "title": "Voxtral 3：Mistral 的语音 agent SDK，50+ 语言实时转写 + 情绪 TTS + 深度工具调用，可自部署",
            "url": U("https://mistral.ai/news/voxtral-3/"),
            "summary": "Mistral 发布 Voxtral 3，定位是「语音 agent SDK」而不是单个语音模型：覆盖 50 多种语言的实时转写、带情绪的 TTS，以及语音链路中的工具调用；部署上可选 EU 托管或完全自部署。它把语音 agent 需要的三段（听、说、调工具）放进一套 SDK，意图是让语音交互能直接接进已有 agent 循环。",
            "tag": "语音 agent", "source": S("https://mistral.ai/news/voxtral-3/"),
            "detail": [
                {"key": "能做什么", "value": "一套 SDK 覆盖实时 ASR、情绪化 TTS 与语音场景下的工具调用，50+ 语言，支持 EU 托管或自部署（对数据主权敏感的行业有意义）。"},
                {"key": "解决什么痛点", "value": "做语音 agent 通常要拼三家供应商（ASR、LLM、TTS）并自己处理打断、时延与工具调用，链路上每段都要单独治理。"},
                {"key": "值不值得", "value": "如果业务里有电话/客服/语音录入类场景且要求数据不出境，自部署的整套语音栈是可评估项；但要先确认中文与方言的实际识别质量，以及自部署所需的 GPU 规格——这两项官方材料里给得最少。"}
            ]
        },
    ]
})

ai["categories"].append({
    "emoji": "🛠️", "title": "AI 工程落地", "en": "AI ENGINEERING", "items": [
        {
            "title": "COBOL 迁移评测：GPT-6.1 Sol 逐字节一致率 97.9%，MultiLangBench 20 语言平均 87.4%",
            "url": U("https://www.infoq.cn/article/LZsVYHAH1jyOtLg6Yiwk"),
            "summary": "OpenAI 10 月 19 日发布低资源编程语言研究。COBOL 迁移评测要求把现有 COBOL 程序迁到 C++/Java/Kotlin/Python/Rust 并保持行为一致，判据不是「能编译」而是隐藏测试下可观察输出逐字节相同：上一代 GPT-5.6 Sol 在低推理强度下只有 5.4%，GPT-6.1 Sol 同强度 86.6%（估算 API 成本还降 39%），提高推理强度到 97.9%。另一项 MultiLangBench 要求用 20 种语言从零实现兼容 SQLite 的数据库引擎（以数据库文件为统一接口比对），GPT-6 Astra 平均通过率 87.4%，上一代 26.8%；OCaml 25.6%→85.8%、Fortran 21.4%→83.5%、Visual Basic 27.5%→89.4%，而 COBOL 仍是最难的一门（72.1%）。难点被点得很准：COBOL 的定点数舍入语义、缺失记录处理、异常输入响应这些行为往往没写进文档，只藏在代码里。",
            "tag": "代码迁移", "source": S("https://www.infoq.cn/article/LZsVYHAH1jyOtLg6Yiwk"),
            "detail": [
                {"key": "能做什么", "value": "在受控评测里做「行为等价」的跨语言迁移：以输出逐字节一致为成功标准，而不是语法正确；MultiLangBench 还公开了评测代码与测试套件，可用同一套 SQLite 兼容性测试横向比 20 种语言的实现能力。"},
                {"key": "解决什么痛点", "value": "遗留系统迁移的真正成本在语义：COBOL 定点数截断、记录缺失处理这类规则迁移后不报错但算错账，人工评审几乎无法穷举。"},
                {"key": "值不值得", "value": "对金融/量化系统的代码现代化是最值得跟的一条线，但 97.9% 是「评测任务上的逐字节一致率」，不等于大型机核心系统可直接交给 AI——样本由 OpenAI 构造、且是短程序级任务。可行路径是先拿非核心的批处理/对账模块做影子比对（新旧并行跑、比输出），再谈扩大范围。"}
            ]
        },
        {
            "title": "Cache Engineering：让 agent 直接操作 KV cache（drop / repos），成本降 27.7%、吞吐 1.2 倍",
            "url": U("https://arxiv.org/abs/2610.28577v1"),
            "summary": "论文指出 agent 轨迹变长后，KV cache 的 I/O 与存储成为主要成本，而现有做法（裁剪或摘要历史）会改动前缀、使后续缓存失效并触发昂贵的重新 prefill，留太少上下文又掉准确率。它提出 cache engineering：agent 主动用 drop 把选定缓存排除出后续 attention、用 repos 调整保留 key 的位置编码，全程不改轨迹、不重新 prefill。由此暴露服务侧难题——相同 token 序列在不同 cache 操作序列下状态不同，前缀匹配不足以正确复用，于是他们配套设计了 AKV 引擎（对外无状态接口，内部管理有状态复用/驱逐/恢复）。实验里「工具响应滚动丢弃」策略比阈值触发的摘要平均涨 1.7 分、成本降 27.7%；AKV 上输出吞吐最高 1.2 倍、P95 延迟 1.5 倍加速，缓存策略递归自改进再省 7.1%。",
            "tag": "推理优化", "source": S("https://arxiv.org/abs/2610.28577v1"),
            "detail": [
                {"key": "能做什么", "value": "把上下文管理从「改文本」下沉到「改缓存」：drop 掉不再需要的工具输出、repos 调整位置编码，保持前缀不变因而不触发重算；配套 AKV 引擎负责有状态缓存复用与驱逐。"},
                {"key": "解决什么痛点", "value": "agent 长轨迹的成本大头是重复 prefill；trim/summarize 省了 token 却让整个前缀缓存失效，省下的和浪费的经常抵不过。"},
                {"key": "值不值得", "value": "自建推理服务+长轨迹 agent 的话，这是少见的「同时降成本、提吞吐」的机制，且暴露成无状态接口意味着业务侧改动很小。门槛是要改推理引擎（vLLM/SGLang 未必支持 drop/repos 语义），先评估你的引擎是否有对应 hook。"}
            ]
        },
        {
            "title": "Token-Energy Law：用「活跃字节 × 实际耗时」预测每 token 焦耳数，覆盖架构与部署参数",
            "url": U("https://arxiv.org/abs/2610.28576v1"),
            "summary": "论文提出 Token-Energy Law：一个紧凑、可解释的模型，用来预测稠密、全历史解码时 GPU 板级每输出 token 的能耗，把模型架构、硬件与 serving 参数（批大小、并行方式）一起纳入，而不是只看参数量。核心量是每 token 的「活跃字节」与「实际耗时」——即这一 token 解码真正从显存搬了多少权重与 KV、以及这些搬运在多少时间里发生。它的用途是给容量规划与能耗核算一个可算的公式，而不必为每个配置实测功率。",
            "tag": "能耗建模", "source": S("https://arxiv.org/abs/2610.28576v1"),
            "detail": [
                {"key": "能做什么", "value": "在只给定架构与 serving 配置时估算 J/token，并把「批大小、并行切分、KV 长度」对能耗的影响显式化；对有能耗/成本 KPI 的推理平台，可作为选型与配额设计的解析工具。"},
                {"key": "解决什么痛点", "value": "能耗与成本评估现在依赖实测功率，换一个模型或批大小就得重测；PUE、碳排与机柜供电预算却需要在部署前给出数字。"},
                {"key": "值不值得", "value": "做容量规划、机柜供电与单位 token 成本核算时值得一读：它把「省电」落到可改的参数上（活跃字节与时间）。但它只覆盖稠密全历史解码，MoE、投机解码、PD 分离都需另行校准。"}
            ]
        },
    ]
})

ai["categories"].append({
    "emoji": "🧠", "title": "模型与研究", "en": "MODELS & RESEARCH", "items": [
        {
            "title": "首个 token 就决定对错：16 个开源模型里，喂对第一个 token 能纠正 1/5 到 1/2 的错误",
            "url": U("https://huggingface.co/papers/2610.23400"),
            "summary": "这篇论文把闭卷问答的错误重新归类：很多不是「不知道」，而是首个 token 的召回失败——模型锁定了错误的第一个 token，一旦给它正确的起始 token 就能补完答案并认出它是对的。作者用 First-Token Cueing 探测（把标准答案的第一个 token 预填进响应）：模型的不确定性在第一个答案 token 处最高，且此时已能预测自己会不会答对；在所有长度的标准前缀里，第一个 token 单独贡献了最多的错误修复。16 个开源模型上，一个 token 就能纠正英文多 token 答案错误的两成到五成，并在多语言基准的 7 种语言上全部提升。被纠正的错误多数也能被模型自己的采样推理解决，说明知识确实编码在里面。",
            "tag": "机制研究", "source": S("https://huggingface.co/papers/2610.23400"),
            "detail": [
                {"key": "能做什么", "value": "定位了一类可恢复的事实错误发生在「第一个解码步」，并给出行为学探针（首个 token 提示）与判据（模型对正确起始的置信度高于同类型同先验的错误起始）。这为推理时的纠错提供了极低成本的切入点。"},
                {"key": "解决什么痛点", "value": "闭卷错误通常被当成知识缺失去做 RAG/微调，成本高；如果相当一部分只是起始 token 选错，那么在第一步做重采样或验证就够了。"},
                {"key": "值不值得", "value": "对做推理时优化/评测的人很有价值：一个前向就能拿到「首 token 处的正确性信号」，可用于提前终止、重采样或路由到检索。但它只解释闭卷事实召回，不解决推理链错误；且需标准答案做探针，线上只能用其自监督版本。"}
            ]
        },
        {
            "title": "Muse Glimmer 30B：4bit 量化跑单卡消费级硬件的 agent 模型，Apache 2.0 开源",
            "url": U("https://huggingface.co/papers/2610.24628"),
            "summary": "Muse Glimmer 是 30B 参数、带感知编码器的因果语言模型，专为消费级硬件上的自主 agent 任务设计：把多步推理、可靠工具调用与失败恢复放进一个模型，本地运行、不需要云。它接受文本与图像输入、训练数据覆盖上百种语言，量化到约 4bit 以在单 GPU 上推理；同尺寸对比中（Gemma4-31B、Qwen3.6-27B）在工具使用、多步规划与 agent 任务完成上取得 SOTA，并以 Apache 2.0 发布权重。",
            "tag": "端侧模型", "source": S("https://huggingface.co/papers/2610.24628"), "oss": True,
            "detail": [
                {"key": "能做什么", "value": "在单张消费级 GPU 上本地跑多步 agent 循环（含工具调用与失败重试），4bit 量化 + 文本/图像输入，Apache 2.0 权重可用于商业部署。"},
                {"key": "解决什么痛点", "value": "agent 落地时常卡在「数据不能出内网」与「云端调用成本」；端侧 30B 是这两者之间的现实折中，尤其适合做本地工具编排层。"},
                {"key": "值不值得", "value": "想给团队做本地 agent 试验台的可以拿来测：30B/4bit 的显存需求在单卡可承受范围，许可也宽松。但要清楚 30B 与前沿闭源模型在长程任务上的差距，适合做工具路由、简单自动化而非复杂推理。"}
            ]
        },
        {
            "title": "Lafa：8B 连续流语言模型，块内双向异步流 + 前缀因果注意力，走并行生成路线",
            "url": U("https://arxiv.org/abs/2610.28559v1"),
            "summary": "连续流语言模型能并行生成、并具备离散扩散没有的控制与加速工具，但如何做到十亿参数规模一直不清楚。论文提出 Lafa（Large flow language model），以数据高效的方式把流语言模型做到 8B：采用分块（blockwise）流结构，块内用双向、异步的 flow，前缀用因果注意力；在此基础上给出可控与加速手段。这是对「自回归之外」的并行生成路线在 8B 量级的一次实证。",
            "tag": "模型架构", "source": S("https://arxiv.org/abs/2610.28559v1"),
            "detail": [
                {"key": "能做什么", "value": "把流（flow）式语言模型做到 8B 并保持数据高效：块内双向异步流 + 前缀因果注意力，允许块内并行生成，同时保留前缀的因果正确性。"},
                {"key": "解决什么痛点", "value": "自回归解码逐 token 串行，吞吐上限受延迟约束；扩散式并行生成在语言上质量与规模都还没走通，流模型是第三条路。"},
                {"key": "值不值得", "value": "属于架构层研究，短期不会改变推理栈选型；但「并行生成」若成立会直接冲击现有 PD 分离与 KV 优化的假设，值得保持关注。当前缺与同规模自回归模型的系统对比，不宜据此做技术押注。"}
            ]
        },
    ]
})

ai["categories"].append({
    "emoji": "📊", "title": "产品与商业", "en": "PRODUCT & BUSINESS", "items": [
        {
            "title": "Anthropic 上线 Claude Duet：主动式 agent 应用进研究预览，Opus 5.5 驱动、接 6000+ 连接器",
            "url": U("https://claude.com/product/claude-duet"),
            "summary": "Anthropic 推出 Claude Duet，定位是「主动式 agent」：它自己判断什么需要你注意，任务在你离开时继续跑，关键决策处等你确认；官方描述是每天早上给你一份简报、起草下一步，然后安静到有事找你。由 Opus 5.5 驱动，可用 6000 多个 connector 与 plugin，复用 Claude app 里已有的记忆、skills 与应用。美国 Pro/Max 计划先行、需排队，属研究预览。HN 上该条目 297 分、254 条评论。",
            "tag": "产品发布", "source": S("https://claude.com/product/claude-duet"),
            "detail": [
                {"key": "能做什么", "value": "把 agent 从「你问它答」变成「它主动推进」：定时简报、后台继续执行、关键动作前向人确认，并继承已有记忆与 skills，接 6000+ 连接器读真实业务数据。"},
                {"key": "解决什么痛点", "value": "现有 chat 形态要求人一直在线驱动；真正的工作是「等你回来时它已经做完了需要判断的那一步」。"},
                {"key": "值不值得", "value": "值得看的是产品形态而非功能清单：它把「主动性 + 审批点」做成了默认交互，这也是企业 agent 落地的关键设计。限制很明确——仅美国 Pro/Max、研究预览，且主动性意味着权限与审计必须同步到位。"}
            ]
        },
        {
            "title": "Google Cloud 把 OpenAI 模型上架 Model Garden，成为唯一同时供 Gemini 与 OpenAI 模型的超大规模云",
            "url": U("https://cloud.google.com/blog/products/ai-machine-learning/google-cloud-brings-openai-models-to-customers/"),
            "summary": "Google Cloud 宣布在 Model Garden 上线 OpenAI 模型，官方说法是成为唯一同时提供 OpenAI 模型与自家前沿模型的超大规模云厂商，卖点是让 agentic workload 按成本/能力/性能在模型间切换，并沿用既有的企业治理与配额体系。这条与同日的 GTC Berlin 公告（Google Cloud × NVIDIA 扩大联合工程、Confidential G4 GA）一起，构成了「模型可选 + 机密算力」的组合叙事。",
            "tag": "模型接入", "source": S("https://cloud.google.com/blog/products/ai-machine-learning/google-cloud-brings-openai-models-to-customers/"),
            "detail": [
                {"key": "能做什么", "value": "在同一个云账户与治理边界内调用 OpenAI 模型与 Gemini，按任务在模型间切换，避免为多模型分别建采购与合规流程。"},
                {"key": "解决什么痛点", "value": "企业做多模型策略时，最麻烦的是一套模型一个供应商、一套计费与审计；模型集中到一个 model garden 后，路由与成本核算才做得起来。"},
                {"key": "值不值得", "value": "对多云中立性有要求的团队是加分项，但注意「同一账号里能调」不等于「同一套 SLA 与数据条款」，区域可用性与配额仍受各自限制；如果已在 GCP 上，值得做一次跨模型路由的成本对比。"}
            ]
        },
        {
            "title": "Meshy Edit：圈选区域 + 一句话改 3D 模型局部，约一分钟出结果、未选中部分保持不变",
            "url": U("https://www.qbitai.com/2026/10/504415.html"),
            "summary": "Meshy 推出 Meshy Edit，基于自研模型做 3D 模型的局部编辑：用户圈选要改的区域，用一句话描述改动，约一分钟生成新模型，且未选中区域保持原样。它解决的是 3D 生成里「改一处就得整模重生成」的老问题。",
            "tag": "3D 生成", "source": S("https://www.qbitai.com/2026/10/504415.html"),
            "detail": [
                {"key": "能做什么", "value": "局部可编辑的 3D 生成：区域圈选 + 文本指令，约一分钟出结果，非编辑区保持不变，把 3D 资产从「一次性生成」变成「可迭代修改」。"},
                {"key": "解决什么痛点", "value": "整模重生成会破坏已确认的细节，返工成本高；游戏/电商资产的迭代主要卡在局部修改上。"},
                {"key": "值不值得", "value": "与他的 K8s/AI 基建主线关系不大，除非涉及 3D 资产流水线；要看的是「局部编辑的一致性」是否稳定，官方未给量化指标。"}
            ]
        },
    ]
})

ai["categories"].append({
    "emoji": "🛡️", "title": "安全与治理", "en": "SECURITY & GOVERNANCE", "items": [
        {
            "title": "Patch the Planet：Codex + 安全工程师在 19 个开源项目里挖出数百个问题、合并数十个补丁",
            "url": U("https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities"),
            "summary": "OpenAI 公布 Daybreak 计划下的 Patch the Planet 进展：与 Trail of Bits 合作，把前沿模型（含 GPT-5.5-Cyber）与 Codex Security 交给全职安全工程师，在 19 个开源项目上做「发现—验证—定级—补丁—测试—协调披露」的完整闭环，参与项目包括 cURL、NATS Server、pyca/cryptography、Sigstore、aiohttp、Go、freenginx、Python。官方称已识别数百个安全问题、合并数十个补丁，其余仍在协调披露中；副产物是一批可复用基础设施：fuzzing harness、历史 CVE 分析流水线、差分测试系统、威胁模型、去重与误报过滤、严重性校正与补丁生成流程。HackerOne 与 Calif 参与分流与披露协调。",
            "tag": "漏洞治理", "source": S("https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities"),
            "detail": [
                {"key": "能做什么", "value": "把 AI 挖洞从「批量提交报告」改成有验证与补丁的闭环：模型做发现与初筛，安全工程师做验证/定级/写补丁/跑测试，再走协调披露；同时沉淀 fuzzing、差分测试、去重与误报过滤等可复用工具链。"},
                {"key": "解决什么痛点", "value": "维护者最怕的不是漏洞被报告，而是大量未经验证的 AI 生成报告淹没邮件列表；「发现加速了但修复没加速」是当前开源安全的真实瓶颈。"},
                {"key": "值不值得", "value": "对自建供应链安全流程的团队有两点可借：一是准入必须包含验证与补丁，二是去重/误报过滤要当成基础设施做。注意这是厂商自述进展、具体漏洞细节待披露，且项目选择由 OpenAI 与伙伴决定，不代表普遍覆盖。"}
            ]
        },
    ]
})

ai["categories"].append({
    "emoji": "💡", "title": "观点与好文", "en": "ESSAYS", "items": [
        {
            "title": "Andy Pavlo：Agent 删库不是新问题，是数据库护栏被绕过——向量库退潮、自动驾驶 DBA 的十年",
            "url": U("https://www.infoq.cn/article/2Z056Q54wWa6vAIQKsqJ"),
            "summary": "InfoQ 整理的 The MAD Podcast 访谈里，CMU 教授、ClickHouse 数据库研究副总裁 Andy Pavlo 谈 Agent 时代数据库的四重变化：向量数据库的退潮、Agent 删库的护栏问题、AI 能否从零构建数据库、以及「自动驾驶数据库」十年的进展。他的核心判断是：Agent 删库不是新问题，权限与管控手段几十年前就有（触发器、只读副本、审批流），只是大家急着让 agent「能干活」，忘了先问「它干错了怎么办」。",
            "tag": "工程观点", "source": S("https://www.infoq.cn/article/2Z056Q54wWa6vAIQKsqJ"),
            "detail": [
                {"key": "能做什么", "value": "用数据库领域几十年的既有机制（权限分层、只读副本、审批/回滚、审计日志）重新框定 agent 安全问题，而不是把「AI 危险」当成新命题。"},
                {"key": "解决什么痛点", "value": "给 agent 生产库的写权限，本质是把「不可撤销的操作」交给了概率系统；而行业已经有成熟的防呆设计，只是没被接进 agent 的工具链。"},
                {"key": "值不值得", "value": "做 agent 落地时的必读视角：先把权限与回滚设计好，再谈自主性。分歧点在于他对向量库的判断较激进，需自己判断；但「护栏是工程问题不是模型问题」这条结论很硬。"}
            ]
        },
        {
            "title": "Simon Willison：用 Claude 做出一款能玩的 RTS（Battle Drones），多人同步靠音频传状态",
            "url": U("https://simonwillison.net/2026/Oct/20/battledrones/"),
            "summary": "Simon Willison 记录了他最新的 vibe coding 实验 Battle Drones——一款 Command & Conquer 风格的即时战略游戏，他说这是自己多个实验里第一个「真的好玩」的，方法是对 Claude 说「让它好玩得多」。游戏还支持附近设备之间的多人对战，同步方式是用音频传游戏状态。文章写了他怎么搭、以及过程中学到的几件事。",
            "tag": "构建", "source": S("https://simonwillison.net/2026/Oct/20/battledrones/"),
            "detail": [
                {"key": "能做什么", "value": "一个可玩的完整作品：RTS 玩法 + 近场多人 + 用音频信道同步状态（不走网络栈），全部由 AI 辅助写成。价值在于展示 agent 在「有反馈循环的交互系统」上能做到的完成度。"},
                {"key": "解决什么痛点", "value": "多数 AI 编码演示停在脚本与页面；真正难的是循环调参（手感、难度、平衡）——这类体验无法规格化，靠的是快速迭代。"},
                {"key": "值不值得", "value": "读它是为了看方法：把「好玩」这种模糊目标当成可迭代的验收标准，而不是写规格。对基础设施工作没有直接迁移，但作为「AI 协作开发的上限样本」值得一看。"}
            ]
        },
    ]
})

SECTIONS.insert(0, ai)

FLASH = []
for t, u in [
    ("supabase/supabase", "https://github.com/supabase/supabase"),
    ("twentyhq/twenty", "https://github.com/twentyhq/twenty"),
    ("Comfy-Org/ComfyUI", "https://github.com/Comfy-Org/ComfyUI"),
    ("shiyu-coder/Kronos", "https://github.com/shiyu-coder/Kronos"),
]:
    try:
        FLASH.append({"title": BY_URL[U(u)]['title'], "url": U(u)})
    except SystemExit:
        print("skip flash", u)

brief = {
    "brand": "AI & 基础设施早报",
    "date_label": "2026 年 10 月 22 日 · 星期四",
    "issue": 32,
    "kicker": "DAILY",
    "hint": "👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
    "lead": "今天两条主线都指向同一件事：把「判断」做成可度量的东西。DeepSeek 开源 DeepInfer，把推理系统的成本压到架构层——Prefill 用 8 卡机、Decode 用 64–128 卡超节点，KVCache 从显存搬进独立 3FS 集群（约 100 PiB）保存 3–7 天，于是不必再做前缀亲和路由，单集群日吞吐 155 万亿 Token。另一条是评测：CNCF 用 SREGym 的 50 个注入故障证明，同一个 agent 换成只读 MCP 上下文后，2 分钟内诊断达标率从 60% 升到 86%、静默故障从 326 秒降到 79 秒，而判断力本身没变；OpenAI 的 Terminal X 案例则把投资复核拆成 54 条 rubric，与资深评审一致率 88.6%。基础设施侧 Volcano 1.16 把多租户公平与调度吞吐一起改，containerd 2.4.2 是必须排期的安全补丁。",
    "highlights": H,
    "sections": SECTIONS,
    "flash": FLASH,
    "footer": "由 Hermes 自动汇编 · 每日 09:00 更新",
}

# ---- assertions ----
def walk(o):
    if isinstance(o, dict):
        if 'url' in o:
            assert o.get('title'), f"missing title for {o['url']}"
            assert o['url'] in BY_URL, f"URL not from processed.json: {o['url']}"
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)

walk(brief)
n_items = len(brief['highlights']) + sum(len(c['items']) for s in brief['sections'] for c in s['categories']) + len(brief['flash'])
json.dump(brief, open('briefing.json', 'w'), ensure_ascii=False, indent=1)
print("items:", n_items, "| sections:", [(s['label'], [(c['title'], len(c['items'])) for c in s['categories']]) for s in brief['sections']])
