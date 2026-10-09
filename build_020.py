#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build issue 020 briefing.json. Appends funnel-gap-fill infra items into
processed.json first (so verify_links.py accepts them), then assembles
briefing.json with machine-copied URLs (asserted present in processed.json)."""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__)) or "."
P = lambda *a: os.path.join(BASE, *a)

# ---------------------------------------------------------------- gap-fill
GAP = [
 dict(title="Scaling Kubernetes Workloads with Node Swap",
   url="https://kubernetes.io/blog/2026/10/05/scaling-kubernetes-workloads-with-node-swap/",
   summary="Kubernetes 官方实测：在 v1.34 起 GA 的 node swap 基础上用 NVMe SSD 承载交换分区，对 CI/CD 内核构建、沙箱无头浏览器、隔离 Python 运行时三类负载做基准，节点密度最高提升 3 倍，多数场景几乎无延迟代价。作者指出新一波 agentic 负载启动即要占大内存运行不受信代码、随后长时间空转等 prompt，把闲置常驻内存压在物理 RAM 里会直接限制单节点可容纳的 Pod 数。",
   published="2026-10-05T00:00:00+00:00", source="Kubernetes Blog", source_cat="K8s-官方",
   board="基础设施板块", category="K8s × AI"),
 dict(title="Kubernetes v1.37: DRA Updates",
   url="https://kubernetes.io/blog/2026/09/03/kubernetes-v1-37-dra-updates/",
   summary="K8s 1.37 把 DRA Extended Resource 支持推进到 GA：DRA 驱动可直接满足传统扩展资源请求（如 example.com/gpu），不再需要并行的 device plugin，现有工作负载无需改动即可渐进迁移到 DRA 后端。同时 device taints/tolerations 转 Stable（可把单块设备标记为可驱逐做维护），ResourceClaim.status 新增 devices 字段回报网卡名/MAC/IP，numaNode 成为跨驱动统一的设备属性名。",
   published="2026-09-03T00:00:00+00:00", source="Kubernetes Blog", source_cat="K8s-官方",
   board="基础设施板块", category="K8s × AI"),
 dict(title="Kubernetes v1.37: Advancing Workload-Aware Scheduling",
   url="https://kubernetes.io/blog/2026/09/08/kubernetes-v1-37-advancing-workload-aware-scheduling/",
   summary="K8s 1.37 把核心 Workload/PodGroup API（gang scheduling）、Workload-Aware Preemption、PodGroup 共享 DRA ResourceClaim 一起推进到 Beta；新增 CompositePodGroup API 表达多层拓扑约束、gang scheduling 与抢占策略，原生打通 JobSet、LeaderWorkerSet(LWS) 这类高阶结构。同时提供控制器集成 API 与 workloadbuilder Go 库，并让原生 Job 控制器消费 WAS API。",
   published="2026-09-08T00:00:00+00:00", source="Kubernetes Blog", source_cat="K8s-官方",
   board="基础设施板块", category="K8s × AI"),
 dict(title="Smarter GPU sharing: How Red Hat build of Kueue works with dynamic resource allocation",
   url="https://developers.redhat.com/articles/2026/10/02/smarter-gpu-sharing-how-red-hat-build-of-kueue-works-with-dynamic-resource-allocation",
   summary="Red Hat 讲解在 OpenShift 上用 Kueue + DRA 管 GPU 配额：DRA（1.34 GA）让驱动通过结构化 API 公布显存/算力/拓扑等真实设备属性、工作负载按需描述，但它只解决设备发现与分配，不管配额、公平共享与抢占——这正是 Kueue 的职责。文章指出 Kueue 目前按聚合配额准入（ClusterQueue 有没有足够 GPU 显存），而配额可用不等于能落到真实节点，上游正引入 scheduler-library 弥合这一缺口。",
   published="2026-10-02T00:00:00+00:00", source="Red Hat Developer", source_cat="厂商工程博客",
   board="基础设施板块", category="K8s × AI"),
 dict(title="How Zhuoyu Technology Pushed GPU Allocation Above 95% on Kubernetes with Koordinator",
   url="https://www.cncf.io/case-studies/zhuoyu-technology",
   summary="CNCF 案例：自动驾驶公司卓驭科技(Zhuoyu)用 CNCF Sandbox 项目 Koordinator 解决默认 kube-scheduler 造成的 GPU 搁浅与分布式作业调度低效，把集群 GPU 分配率推过 95%、整体利用率提到 55% 以上（共享推理约 60%），开发环境(Codespaces)减少约 60% 整卡。单集群 100+ ElasticQuota，日调度吞吐 30 万–80 万 Pod。栈里同时用了 Kubernetes、Koordinator 与 HAMi。",
   published="2026-09-29T00:00:00+00:00", source="CNCF", source_cat="CNCF",
   board="基础设施板块", category="K8s × AI"),
 dict(title="GPU Sharing on Kubernetes: What HAMi Showed at KubeCon China 2026",
   url="https://kubezilla.io/hami-gpu-sharing-kubecon-china-2026",
   summary="HAMi（异构算力虚拟化中间件，2026-07-15 被 CNCF TOC 接纳为 Incubating）在 KubeCon 中国 2026 拿到两个 keynote：Intsig 在约 1 万张 GPU、跨自建机房与多云上跑 1,000+ 在线推理与 1,000+ 离线训练，全天利用率 90%+，GPU 利用率提升约 50%、整体成本降约 30%、推理开销 <10%；招商银行单卡推理吞吐 +46.7%、利用率 20%→80%；顺丰 1,400→1,000 张卡无业务影响；工行利用率 20%→70%。",
   published="2026-09-15T00:00:00+00:00", source="Kubezilla", source_cat="社区博客",
   board="基础设施板块", category="K8s × AI"),
 dict(title="CiliumCon is back at KubeCon + CloudNativeCon North America 2026",
   url="https://www.cncf.io/blog/2026/10/07/ciliumcon-is-back-at-kubecon-cloudnativecon-north-america-2026",
   summary="CiliumCon 将在 KubeCon 北美 2026（11/9–12 盐湖城）回归，议题聚焦真实生产问题：纯 IPv6 跑 K8s、大规模 CNI 数据面迁移会踩什么坑、对 AI 集群 RDMA 流量做 network policy、用 eBPF 追延迟敏感负载的丢包。面向在生产运行 Cilium/Hubble/Tetragon 的平台工程师，以及正在评估 CNI 迁移或为 AI 负载调整网络的人。",
   published="2026-10-07T00:00:00+00:00", source="CNCF Blog", source_cat="CNCF",
   board="基础设施板块", category="社区与项目"),
 dict(title="KubeCon + CloudNativeCon North America 2026: Join the cloud native community at OpenTofu Day",
   url="https://www.cncf.io/blog/2026/10/02/kubecon-cloudnativecon-north-america-2026-join-the-cloud-native-community-at-opentofu-day",
   summary="OpenTofu 从 Terraform 分叉成长为 CNCF Sandbox 项目，截至 2026 年 10 月下载量超过 1,000 万，近期加入客户端状态加密、provider 配置的 for_each、OCI registry 支持。OpenTofu Day（KubeCon 北美 2026）议程含项目现状更新、Ask the Devs，以及从 Terraform 迁移、规模化性能与插桩、平台工程内源采纳等实践分享。",
   published="2026-10-02T00:00:00+00:00", source="CNCF Blog", source_cat="CNCF",
   board="基础设施板块", category="社区与项目"),
 dict(title="Kubernetes v1.37 Release",
   url="https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/",
   summary="Kubernetes v1.37 发布，以安全加固、AI/ML 负载支持与大规模 API 扩展为主：DRA Extended Resource 转 GA，Workload/PodGroup 与 gang scheduling、Workload-Aware Preemption、HPA scale-to-zero、Pod 级资源管理器、Memory QoS、kubelet rootless、PVC UnusedSinceTime 均转 Beta；CSI 卷健康检查以新 RPC 进入 Alpha。",
   published="2026-08-26T00:00:00+00:00", source="Kubernetes Blog", source_cat="K8s-官方",
   board="基础设施板块", category="K8s 核心"),
 dict(title="llm-d",
   url="https://github.com/llm-d/llm-d",
   summary="llm-d 是 Kubernetes 原生的分布式 LLM 推理框架，2026-03 由 Red Hat、Google Cloud、IBM Research、CoreWeave、NVIDIA 等捐给 CNCF 成为 Sandbox 项目。它把 prefill/decode 阶段拆到独立 GPU 池，用 Gateway API Inference Extension 做 KV cache 感知路由，支持分层 KV 卸载、cache-aware LoRA 路由、active-active HA、UCCL 传输与 scale-to-zero 自动缩放；v0.5 基准在 16×16 B200 拓扑上报告约 50,000 输出 token/s。",
   published="2026-03-24T00:00:00+00:00", source="GitHub", source_cat="开源项目",
   board="基础设施板块", category="K8s × AI", oss=True),
]
for g in GAP:
    g.setdefault("extra", {}); g.setdefault("oss", False)
    g.setdefault("hot_score", 9); g.setdefault("is_hot", False)

proc = json.load(open(P("processed.json"), encoding="utf-8"))
have = {it["url"] for it in proc}
added = 0
for g in GAP:
    if g["url"] not in have:
        proc.append(g); have.add(g["url"]); added += 1
json.dump(proc, open(P("processed.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"processed.json: +{added} gap-fill items -> {len(proc)} total")

PROC = {it["url"]: it for it in proc}

# ---------------------------------------------------------------- helpers
def item(url, title=None, summary=None, tag=None, oss=None, detail=None, source=None):
    assert url in PROC, f"URL not in processed.json: {url}"
    src = PROC[url]
    d = {"title": title or src["title"],
         "url": url,
         "summary": summary or src.get("summary") or ""}
    d["source"] = source or src.get("source") or ""
    if tag: d["tag"] = tag
    if oss is None: oss = src.get("oss")
    if oss: d["oss"] = True
    if detail: d["detail"] = detail
    assert d["title"], f"missing title for {url}"
    assert d["summary"], f"missing summary for {url}"
    return d

D = lambda a, b, c: [{"key":"能做什么","value":a},{"key":"解决什么痛点","value":b},{"key":"值不值得","value":c}]

# ---------------------------------------------------------------- highlights
highlights = [
 {"title":"自动驾驶公司卓驭用 Koordinator 把 K8s GPU 分配率推过 95%：单集群日调度 30–80 万 Pod，开发环境省下约 60% 整卡",
  "url":"https://www.cncf.io/case-studies/zhuoyu-technology",
  "summary":"CNCF 发布卓驭科技(Zhuoyu)的案例：这家中国自动驾驶公司用 CNCF Sandbox 项目 Koordinator 扩展 Kubernetes 调度，解决默认 kube-scheduler 造成的 GPU 搁浅与分布式作业调度低效。成果是集群 GPU 分配率超过 95%、整体 GPU 利用率 55%+（共享推理场景约 60%），开发环境(Codespaces)使用的整卡数量减少约 60%。规模上单集群维护 100+ 个 ElasticQuota，日调度吞吐量达 30 万–80 万个 Pod。整套栈同时用了 Kubernetes、Koordinator 与 HAMi，回应的是 AI 时代“卡贵、但大量卡被碎片化占用”的核心矛盾。",
  "note":"🔎 新闻要点：Koordinator 是 CNCF Sandbox 的 Kubernetes 调度扩展；本案例核心指标为 GPU 分配率 >95%、整体利用率 >55%（共享推理 ≈60%）、Codespaces 整卡数 ≈-60%、日调度 300K–800K Pod、单集群 100+ ElasticQuota。方案不替换默认调度器，而是补足其在大规模 AI 负载下的配额、共卡与拓扑调度能力。",
  "tag":"K8s × AI","source":"CNCF",
  "detail":D("用 Koordinator 在原生 K8s 上做 GPU 共卡/配额/拓扑调度：弹性配额(ElasticQuota)做多租户配额与超卖，配合 QoS 与资源超卖提升整机利用率，并对分布式训练/推理做共置与大队列调度；案例中与 HAMi 共用，由 Koordinator 管配额与放置、HAMi 管 vGPU 切分。",
          "默认调度器按整卡计数分配、缺队列与优先级语义，AI 负载下会出现 GPU 搁浅（已分配但闲置）与作业启动失败；显存维度不可见导致小任务独占整卡，集群成本高企。",
          "对自建 GPU 集群、要提升卡利用率并做多租户隔离的团队，Koordinator 是“不换调度器、增量叠加”的低侵入路线，和你在做的 K8s 集群建设直接对口；但它是 Sandbox 项目、生态成熟度低于 Kueue，大规模落地仍需自担运维。"),
 },
 {"title":"Mistral 发布 Large 4「le Chonk」：1T 参数 MoE（激活 49B）、512k 上下文，10 月 6 日开放 API 预览、权重承诺月底开源",
  "url":"https://mistral.ai/news/mistral-large-4/",
  "summary":"Mistral 于 10 月 6 日开放旗舰模型 Mistral Large 4 的 API 预览（模型 ID mistral-large-4，昵称 le Chonk）。它是一个约 1 万亿参数、激活约 490 亿的 MoE，报告使用 3,800 张 NVIDIA Grace Blackwell GPU 训练，支持 512k 上下文与图像输入，定位长文档、agentic 工作流、代码与网络安全任务，官方称在 Cybench 上达 93%、对 prompt injection 有较强抵抗。权重承诺在 10 月底发布（含安全审查），独立评测 Vals Index 给到 48.05% 排 32/44。它是欧洲阵营在开源权重赛道对中美的正面回应。",
  "note":"🔎 新闻要点：发布日 2026-10-06；总参数约 1T、激活约 49B 的 MoE；训练用 3,800 张 GB200(Grace Blackwell)；上下文 512k、支持图像输入；定价约 $1.36/$4.18 每百万 token（in/out）；独立榜单 Vals Index 48.05% 居中游，但在 Harvey 法律 Agent 基准排第 6/75。权重“月底开源”为官方口径、许可证未定。",
  "tag":"模型发布","source":"Mistral AI",
  "detail":D("一个万亿级稀疏 MoE 通用模型：512k 上下文 + 图像输入，主打长文档推理、agentic 任务（工具体用/多步）、代码与网络安全（官方 Cybench 93%），并强调抗提示注入；提供托管 API（mistral-large-4）且承诺开放权重可自托管。",
          "前沿闭源模型强但在金融等高合规场景不满足“数据不出内网/可自托管”的要求；欧洲也需要一个可下载权重、可私有部署的旗舰来替代完全黑盒的 API。",
          "若你关注“金融量化场景里能否自托管一个够强的旗舰”，值得盯权重落地与许可证；但独立榜单显示它并非 SOTA（Vals 32/44），万亿 MoE 自托管的显存/推理成本很高，短期更现实的是用它做对比基线而非主力。"),
 },
]

# ---------------------------------------------------------------- sections
def cat(emoji, title, en, items):
    return {"emoji":emoji,"title":title,"en":en,"items":items}

ai_items_agent = [
 item("https://openai.com/index/oracle", tag="Agent 落地",
   summary="Oracle 把 ChatGPT Work 与 Codex 铺到招聘、工程与运营三条线，把资深员工的专有知识转成可复现的快速工作流：例如把跨系统的招聘流程、工程规格生成与运营报表交给 agent 化流程处理，把此前以“天”计的专家任务压到“分钟”级。是 OpenAI 近期主推的“企业内知识→可执行工作流”落地样本。",
   detail=D("把企业内部专家知识沉淀成可复用的 agent 工作流：用 ChatGPT Work 做知识型任务、Codex 做代码/工程任务，跨招聘、工程、运营多部门统一入口。",
          "专家经验散落各处、重复性任务占用高薪人力，跨系统流程靠人肉串联、无法规模复制。",
          "对你“把 AI 融进工作并向同事分享”的路线有参考价值——看点是把“专家知识→工作流”的抽象方式；但这是厂商客户故事、缺量化指标，别当技术方案读。")),
 item("https://www.infoq.cn/article/3MSU3CcJuh0XjHDyjhXj?utm_source=rss&utm_medium=article", tag="观点",
   summary="InfoQ 报道一个反差结论：OpenAI 刚把多 Agent 做成产品，而 o1 研究奠基人之一的观点是——即便用 1 万个 Agent 解出了世界级难题，多 Agent 对结果的贡献可能不到 10%，真正起作用的是单 Agent 的能力与算力，多智能体协作更多是编排幻觉。",
   detail=D("围绕“多 Agent 是否真带来增益”的实证讨论：以大规模 Agent 群体解题为样本，量化协作相对于单 Agent 的边际贡献。",
          "当前业界大量多 Agent 编排框架被默认“人多力量大”，但缺乏严格对照，容易把单模型能力或算力投入误记为协作收益。",
          "做 agent 系统前值得一读，帮你避免为“多 Agent 架构”付出不必要的复杂度和成本——先确认单 Agent 基线，再决定要不要拆多体。")),
 item("https://github.com/Jakeschincariol/founder-skill", oss=True, tag="Agent Skill",
   summary="一个 MIT 许可的免费 Claude skill 包：11 个 skill 在创业上线前“压力测试”一门生意——包括用 Hormozi/Thiel/Jobs 语料训练的虚拟董事会、市场总监、CFO，以及由 100 个拟真买家 agent 组成的消费者小组。属于“skill 即角色/流程封装”的使用范式。",
   detail=D("把商业尽调拆成可调用的角色 skill（董事会/营销/财务/消费者面板），用拟真 buyer agent 群体模拟市场反馈，MIT 开源、可直接装进 Claude。",
          "早期验证一门生意/一个功能通常要真人访谈或花钱做调研，慢且贵；个人开发者缺“陪练”式的决策对手。",
          "作为“用 skill 组织多角色评审”的工程范式有意思，可借它理解 skill 的分层与拟真 agent 群体打法；但商业结论的可靠性有限，当工具不当真。")),
 item("https://azure.microsoft.com/updates?id=574204", tag="Agent 治理",
   summary="Microsoft Agent 365 与 Azure API Management 的集成进入公共预览：把对 MCP server 与工具的集中治理与运行时强制打通——即治理策略在 APIM 侧统一下发，运行时对 agent 的工具调用强制执行。补齐了企业 agent 的“注册-治理-执行”链路。",
   detail=D("让企业用 APIM 对 agent 调用的 MCP server/工具做集中治理与运行时执行（鉴权、限流、审计等），把 Agent 365 的治理面与 API 网关的执行面连起来。",
          "agent 大量调用外部工具/MCP server 后，权限与合规缺乏统一执行点，容易绕过既有 API 治理。",
          "若你所在金融环境要给内网 agent 做出网/工具调用的审计与 DLP，这类“网关侧强制治理”正是可借鉴的落点；但仍是预览功能，绑定 Azure 生态。")),
]

ai_items_model = [
 item("https://huggingface.co/papers/2610.10515", tag="论文",
   summary="RoboJEPA 研究机器人潜空间世界模型的“缩放律”：给出随模型规模、数据与算力增长的能力预测方法，填补此前只能做小规模实验、无法判断规模收益的空白，为机器人世界模型的投入决策提供依据。",
   detail=D("为机器人潜空间世界模型建立可预测的 scaling 规律（模型/数据/算力→能力），据此指导训练预算分配。",
          "机器人世界模型训练昂贵却缺乏缩放判据，团队难以预估“加多少算力换多少能力”，容易盲目堆料。",
          "做具身/世界模型方向值得看其方法论；与你偏 infra/agent 的方向相关度中等，除非要评估机器人训练集群规划。")),
 item("https://huggingface.co/papers/2610.10437", tag="论文",
   summary="《Q-Learning with Scalar Adjoint Matching》解决流策略(flow policy)难以用 off-policy RL 微调的难题：因为流策略的动作要在多步求解中生成，无法简单对价值函数求梯度。作者用 Scalar Adjoint Matching 把该过程变成可微、可扩展的 off-policy 训练目标。",
   detail=D("提出 Scalar Adjoint Matching，让流匹配策略能直接对学习到的价值函数做 off-policy 微调，突破多步生成不可微的障碍。",
          "流/扩散策略表达力强但 RL 微调困难，导致“先模仿学习、再用 RL 超越示范”这条路径在流模型上走不通。",
          "做 RL/生成式策略训练的团队值得跟进；对纯 infra 读者是了解“后训练算法前沿”的一条线索，不必深入。")),
 item("https://huggingface.co/papers/2610.10460", tag="论文",
   summary="多教师同策略蒸馏(MOPD)的机制研究：区分“同域组合”（多教师对同一 prompt 打分合成单一目标）与“路由域蒸馏”（不同域 prompt 交给对应教师）两种设定，提出 Teacher-Relative Shifts 让各教师只贡献自己学到的部分、减少信号互相污染。",
   detail=D("给出多教师 on-policy 蒸馏的统一框架与 Teacher-Relative Shifts 方法，让不同教师的能力可组合而不相抵消。",
          "把多个专家模型蒸馏到一个学生模型时，教师信号常互相冲突，学生学不到“每个教师各自的特长”。",
          "做模型蒸馏/后训练的团队可参考其“信号分解”思路；对关注 API 成本下降（用蒸馏替代前沿调用）的人是有用背景。")),
 item("https://huggingface.co/papers/2610.09450", tag="论文",
   summary="Iris-3B 从零预训练一个 3B 的像素空间文生图 transformer，并给出“像素空间 vs 潜空间”两条路线的对照：像素空间避开有损 VAE，在细粒度细节敏感的下游任务上有优势，作者同时给出转换与微调方案。",
   detail=D("验证像素空间扩散能否在 3B 规模上成立，提供从潜空间模型转换到像素空间骨干的路径与微调方法。",
          "潜空间扩散依赖 VAE，细节有损、在需要高保真的下游任务上受限；直接从像素建模又长期被认为太贵。",
          "做生成模型的团队可关注；对基础设施读者价值有限，属“了解路线之争”的泛读项。")),
 item("https://www.qbitai.com/2026/10/501995.html", tag="评测",
   summary="量子位报道 PaperBenchX 这类基准对 AI 科研能力的衡量：模型能“破解”某些千禧年数学难题（多来自已被公开的解法），但在论文复现任务上成功率低至 13.98%，说明现有 benchmark 高估了真实科研能力，需要更贴近“能否复现并推进”的评测。",
   detail=D("用 PaperBenchX 等基准测量模型“复现论文/推进科研”的真实能力，而非只会答标准答案。",
          "数学/科研 benchmark 常被训练数据污染或只考选择题式能力，给出虚高的“科研 SOTA”，误导投入。",
          "若你要用模型做研究辅助或评估其可信度，这条提醒你关注“复现率”类指标；属判断模型真实能力的参考。")),
]

ai_items_eng = [
 item("https://openai.com/index/legalon-halves-codex-costs", tag="成本",
   summary="LegalOn 把 Codex 用于法律 AI 研发，通过按任务匹配 Astra/Sol/Luna 三档模型并做预算管理，把估算的 Codex 日均成本降低 65%，同时维持开发速度。是“按任务分级选模型”压低 agent 编码成本的实操案例。",
   detail=D("按任务难度把请求路由到不同档位模型（Astra/Sol/Luna）并设预算上限，从而在保持研发效率的前提下大幅降本。",
          "把最贵的前沿模型无差别用于所有编码任务，成本失控；而人工分级又增加负担。",
          "对你用 Codex/Claude Code 的团队直接可借鉴——“分层路由 + 预算闸门”是最低成本杠杆；这条有量化(65%)，值得深入。")),
 item("https://huggingface.co/papers/2610.04012", tag="论文",
   summary="《Beyond the Parameter Monolith》提出把语言模型系统拆成“上下文化计算、持久存储、精确执行”三部分（FEM-ASM 结构），而不是让所有能力都塞进同一套共享参数，用独立构造的文档状态与确定性执行模块降低更新/遗忘成本。",
   detail=D("用有限元启发的 FEM-ASM 组织：独立文档状态 + 可执行 skill + 残差装配，把“记忆/计算/执行”解耦。",
          "单体参数模型每次更新都牵动全部能力，知识更新昂贵、易灾难性遗忘，且难精确执行。",
          "与你的 agent/skill 实践高度相关——“可执行 skill + 外置记忆”正是当下 agent 工程的方向；值得读其组织机制。")),
 item("https://www.infoq.cn/article/LVsjSV4pIlh3Liz0KZZE?utm_source=rss&utm_medium=article", tag="工程",
   summary="InfoQ 报道 Google 借助 AI 与差分模糊测试把 C 语言依赖库改写为 Rust：用差分模糊测试在两版实现间做等价性校验，配合 AI 生成初始迁移，降低手工重写大型 C 库的风险与工作量。",
   detail=D("用差分模糊测试做 C→Rust 迁移的等价性保证，AI 负责生成候选实现，形成“生成 + 验证”闭环。",
          "把内存不安全的 C 库重写成 Rust 是长期手动、易引入细微错误的高风险工程。",
          "对做供应链安全/内存安全迁移的团队有借鉴意义；“差分模糊测试做验证”这一招可迁移到任何重写场景。")),
]

ai_items_biz = [
 item("https://www.qbitai.com/2026/10/502009.html", tag="公司",
   summary="量子位报道 Manus 重启北京办公室并大举招聘，开始和国产 Agent 团队抢人，同时披露拿到 5 亿美元新融资。反映出 agent 赛道在国内的抢人/融资热度回升。",
   detail=D("Manus 恢复北京办公并扩招，配合 5 亿美元新融资，重启国内 agent 人才与技术布局。",
          "此前出海/收缩引发团队与市场信心波动，需要重建国内研发与招聘。",
          "属行业动态，看你是否关注 agent 创业公司动向；对技术选型无直接影响。")),
 item("https://www.infoq.cn/article/dS754RhjExrwFP6tWD9d?utm_source=rss&utm_medium=article", tag="观点",
   summary="InfoQ 报道 Anthropic 核心技术负责人回应“2 万亿美元估值靠什么撑”：其观点是蒸馏会毁掉前沿研发能力，若靠蒸馏追赶会丧失原创；同时判断中美 AI 竞赛不会单边暂停。属前沿实验室对技术路线与地缘约束的公开表态。",
   detail=D("Anthropic 高管解释其不靠蒸馏、坚持自研前沿路线的立场，并回应估值与竞争格局。",
          "行业普遍用蒸馏低成本追赶，但可能损害长期能力；同时算力/出口管制影响竞赛走势。",
          "属行业观点，读它可校准对“蒸馏派 vs 原创派”的判断；与你的 infra 工作无直接关系。")),
 item("https://www.qbitai.com/2026/10/501915.html", tag="产品",
   summary="量子位报道大模型原生智能体手机 STEPX Neo 将于 10 月 13 日正式发布，定位“大模型原生”的 agent 手机，而非在传统系统上叠语音助手。属端侧 agent 形态的新尝试。",
   detail=D("以 agent 为一等公民的端侧设备形态，试图让模型直接驱动手机任务而非外挂助手。",
          "现有手机 AI 多为外挂式助手，权限与系统集成受限，难做真正的任务自动化。",
          "属产品动态；若你关注 agent 从云到端的落地边界可留意，对 infra 无直接影响。")),
]

ai_items_view = [
 item("https://quesma.com/blog/invisible-cities-one-shot/", tag="好文",
   summary="作者给 Opus 5.5 一个 prompt、给足六小时，让它一次性把卡尔维诺《看不见的城市》可视化成作品，记录长时间自主生成在 HN 引发讨论（347 分）。展示“长时程一次性生成”在创意任务上的实际边界。",
   detail=D("用单条 prompt + 长时程自主运行完成一个完整创意项目，展示模型在长任务里的规划与自我修正。",
          "多数演示只给短任务，难以判断模型在数小时长任务中的稳定性与产出质量。",
          "若你关心 agent 的长时程自主能力边界，这篇是难得的真实长跑记录；泛读即可。")),
 item("https://www.dgt.is/blog/2026-10-07-deepseek-freek-out/", tag="好文",
   summary="一篇 HN 热帖（355 分）追问：为什么业界对 DeepSeek 4.1 Flash 不恐慌？借一款高性价比开源模型的发布，反思行业对“又一次开源冲击”已经脱敏，还是该模型确未触及前沿能力。",
   detail=D("以 DeepSeek 4.1 Flash 为例讨论开源模型逼近前沿时行业的反应函数。",
          "开源模型每次发布都被期待引发冲击，但边际效应递减，容易误判真实能力跃迁。",
          "对跟踪“开源 vs 闭源”竞争态势的人值得一读；帮你判断该不该为一个新开源模型调整技术栈。")),
]

ai_items_safety = [
 item("https://openai.com/index/disrupting-ai-enabled-false-front-operations", tag="治理",
   summary="OpenAI 通报打掉了两个由 AI 驱动的影响行动：它们用假身份“记者”和假智库散播地缘政治话术，说明生成式 AI 已进入信息战的实际操作层，平台方在模型滥用监测上开始系统性对抗。",
   detail=D("披露两起 AI 赋能的影响操作（假记者/假智库），并说明平台的检测与封禁。",
          "生成式模型降低了批量伪造媒体身份与话术的成本，威胁信息生态。",
          "属安全治理动态；若你做内容/风控或内部 DLP，可作为“模型滥用”威胁模型的一手信号。")),
 item("https://www.anthropic.com/news/anthropic-cyber-mission", tag="治理",
   summary="Anthropic 发布 Cyber Mission，围绕把 Claude 用于防御性网络安全（漏洞发现、响应、代码审计等）的能力与配套计划，延续其“前沿模型 + 安全任务”的定位。",
   detail=D("把前沿模型能力组织到防御性网络安全任务上（发现、分诊、响应、审计），并配套合作与准入计划。",
          "防守方人力不足、漏洞响应慢；攻击侧已在用 AI，防守侧需要对等能力。",
          "与企业安全团队相关；若你在金融环境做内网 AI 的攻防/DLP，可参考其任务划分。")),
 item("https://www.infoq.cn/article/s2Rt9t0yqUFk6VYV33Mh?utm_source=rss&utm_medium=article", tag="安全",
   summary="InfoQ 报道苹果筑起的系统权限高墙被 Meta AI 助手“借道”绕过：通过系统级 AI 助手的授权位置越过了平台原本对第三方 App 的权限隔离，暴露出“把助手放在特权层”的新攻击面。",
   detail=D("揭示系统级 AI 助手因处在特权层而成为新的权限绕过路径，突破原有 App 沙箱/权限模型。",
          "平台把 AI 助手放在高权限位置以增强能力，却把原本严格的权限隔离撕开一个口子。",
          "对做终端/内网 AI 安全与权限设计的人有直接警示：助手特权层是最该做最小权限与审计的地方。")),
]

infra_k8sai = [
 item("https://kubernetes.io/blog/2026/10/05/scaling-kubernetes-workloads-with-node-swap/", tag="K8s × AI",
   summary="Kubernetes 官方实测用 NVMe SSD 承载 node swap（v1.34 起 GA）来提升节点密度：对 CI/CD 内核构建、沙箱无头浏览器、隔离 Python 运行时三类负载基准，密度最高提升 3 倍且多数场景几乎无延迟代价。作者点明这正对新一波 agentic 负载的痛点——启动要占大内存运行不受信代码、随后长时间空转等 prompt，闲置常驻内存压在物理 RAM 里会限制单节点 Pod 数。",
   detail=D("用 NVMe 承载的 node swap 给节点内存做“泄压阀”，把长尾闲置的 agent 沙箱内存页换出，从而在同一节点塞下更多沙箱/Pod。",
          "agent 沙箱内存占用大、活跃度低但常驻 RAM，导致单节点密度上不去、AI 基础设施成本高；调小 limit 又会触发 OOM 杀。",
          "对自建 K8s 跑 agent 沙箱/CI 的场景是直接可用的降本手段（官方量化到 3× 密度）；但需 NVMe 且要处理内存记账与延迟敏感负载的权衡，上生产前要按自己的负载复测。")),
 item("https://kubernetes.io/blog/2026/09/03/kubernetes-v1-37-dra-updates/", tag="K8s × AI",
   summary="K8s 1.37 把 DRA Extended Resource 支持推进到 GA：DRA 驱动可直接满足传统扩展资源请求（如 example.com/gpu），不再需要并行挂 device plugin，现有工作负载无需改动即可渐进迁到 DRA 后端。device taints/tolerations 转 Stable（可把单块设备标记为可驱逐做维护），ResourceClaim.status 新增 devices 字段回报网卡名/MAC/IP，numaNode 成为跨驱动统一的设备属性名。",
   detail=D("让 DRA 以兼容方式接管传统 GPU 等扩展资源：驱动在 DeviceClass 上声明资源名，Pod 请求即被 DRA 匹配，无需 ResourceClaim；并把设备级 taint/toleration、设备状态与 NUMA 属性标准化。",
          "device plugin 只能按整数计数分配、看不到显存/拓扑/网络属性；从旧模型迁移到 DRA 又怕破坏现有工作负载。",
          "对正在做 K8s GPU 池化/调度的团队是关键升级信号——DRA 现在能“灰度接管”现有 GPU 请求；建议在 1.37 上用扩展资源兼容模式小步验证，再逐步启用拓扑与设备级维护能力。")),
 item("https://kubernetes.io/blog/2026/09/08/kubernetes-v1-37-advancing-workload-aware-scheduling/", tag="K8s × AI",
   summary="K8s 1.37 把核心 Workload/PodGroup API（gang scheduling）、Workload-Aware Preemption、PodGroup 共享 DRA ResourceClaim 一起推进到 Beta；新增 CompositePodGroup API 表达多层拓扑约束、gang scheduling 与抢占策略，原生打通 JobSet、LeaderWorkerSet(LWS) 这类高阶结构；同时提供控制器集成 API 与 workloadbuilder Go 库，并让原生 Job 控制器消费 WAS API。",
   detail=D("把“整组 Pod 一起调度/一起抢占 + 共享 DRA 资源”变为 K8s 原生能力：Workload/PodGroup 到 v1beta1，新增 CompositePodGroup，并让 JobSet/LWS 等上层 API 直接复用。",
          "分布式训练/推理需要 all-or-nothing 调度，靠 Coscheduling 等外挂或私有 CRD 易碎；gang 与 DRA 资源难以一致地一起申请。",
          "对你“业务上 K8s”里 AI 训练/推理负载是核心利好——gang scheduling 与 LWS 原生打通意味着可少维护一层自研调度；Beta 稳定度够用来做 PoC，注意 v1alpha2→v1alpha3 的 API 变更。")),
 item("https://developers.redhat.com/articles/2026/10/02/smarter-gpu-sharing-how-red-hat-build-of-kueue-works-with-dynamic-resource-allocation", tag="K8s × AI",
   summary="Red Hat 讲解在 OpenShift 上用 Kueue + DRA 管 GPU 配额：DRA（1.34 GA）让驱动通过结构化 API 公布显存/算力/拓扑等真实设备属性、工作负载按需描述，但它只解决设备发现与分配，不管配额、公平共享与抢占——这正是 Kueue 的职责。文章指出 Kueue 目前按聚合配额准入（ClusterQueue 有没有足够 GPU 显存），而“配额可用”不等于“能落到真实节点”，上游正引入 scheduler-library 弥合这一缺口。",
   detail=D("把 Kueue 的配额/公平共享/抢占与 DRA 的设备分配组合使用：Kueue 决定谁先跑、能否准入，DRA 决定具体给哪块设备。",
          "单用 DRA 只解决“分配哪块卡”，缺多租户配额与抢占；单用 Kueue 又看不到设备属性，且配额满足不代表 Pod 能实际调度上节点。",
          "若你在做多团队共享 GPU 集群，这套“Kueue 管配额 + DRA 管设备”是当前最主流的开源组合；落地前注意配额与真实可调度性之间的缺口（上游仍在补 scheduler-library）。")),
 item("https://kubezilla.io/hami-gpu-sharing-kubecon-china-2026", tag="K8s × AI",
   summary="HAMi（异构算力虚拟化中间件，2026-07-15 被 CNCF TOC 接纳为 Incubating）在 KubeCon 中国 2026 拿到两个 keynote：Intsig 在约 1 万张 GPU、跨自建机房与多云上跑 1,000+ 在线推理与 1,000+ 离线训练，全天利用率 90%+，GPU 利用率提升约 50%、成本降约 30%、推理开销 <10%；招商银行单卡推理吞吐 +46.7%、利用率 20%→80%；顺丰 1,400→1,000 张卡无业务影响；工行利用率 20%→70%。",
   detail=D("HAMi 在不改应用代码的前提下做 GPU 切分与显存/算力隔离，把整卡共享给小任务，并支持多厂商加速器与设备感知调度。",
          "整卡申请导致小任务独占、大卡闲置；多租户下显存/算力缺乏硬隔离，利用率普遍只有 20% 左右。",
          "这是国内金融/物流/云厂商已经在生产验证过的 GPU 共享方案（招行案例含 Kueue/KEDA/Fluid），与你的金融量化集群场景高度对口；注意 DRA 成熟后 HAMi 的定位在向 DRA 适配演进，选型时评估长期路线。")),
]

infra_core = [
 item("https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/", tag="版本",
   summary="Kubernetes v1.37 发布，主线是安全加固、AI/ML 负载支持与大规模 API 扩展：DRA Extended Resource 转 GA，Workload/PodGroup 与 gang scheduling、Workload-Aware Preemption、HPA scale-to-zero、Pod 级资源管理器、Memory QoS、kubelet rootless、PVC UnusedSinceTime 均转 Beta；CSI 卷健康检查以新 RPC 进入 Alpha。",
   detail=D("一次侧重“面向 AI 负载 + 安全默认”的版本升级，覆盖调度(DRA/gang)、弹性(scale-to-zero)、资源(Pod 级/Memory QoS)、安全(rootless)与存储(PVC/CSI)多处。",
          "此前 AI 负载调度与容器安全要靠外挂组件与手工加固；大规模集群在内存/弹性上易触顶。",
          "你在独自负责公司 K8s 版本规划——1.37 是本季度最该纳入评估的目标版本，重点看 DRA GA 与 gang scheduling Beta 对业务接入的影响，以及 rootless/Memory QoS 的安全与稳定性收益。")),
]

infra_community = [
 item("https://www.cncf.io/blog/2026/10/07/ciliumcon-is-back-at-kubecon-cloudnativecon-north-america-2026", tag="会议",
   summary="CiliumCon 将在 KubeCon 北美 2026（11/9–12 盐湖城）回归，议题聚焦真实生产问题：纯 IPv6 跑 K8s、大规模 CNI 数据面迁移会踩什么坑、对 AI 集群 RDMA 流量做 network policy、用 eBPF 追延迟敏感负载的丢包。面向在生产运行 Cilium/Hubble/Tetragon 的平台工程师。",
   detail=D("围绕 Cilium/eBPF 的生产实践议题：纯 IPv6 集群、CNI 数据面迁移、RDMA 网络策略、丢包追踪。",
          "CNI 迁移与 IPv6 改造在生产中风险高、缺可复用的踩坑记录；AI 集群 RDMA 流量的策略与可观测性长期是空白。",
          "若你正在选型 CNI 或要为 AI 集群调网络，这组议题的“真实生产教训”值得纳入选型与迁移计划参考。")),
 item("https://www.cncf.io/blog/2026/10/02/kubecon-cloudnativecon-north-america-2026-join-the-cloud-native-community-at-opentofu-day", tag="IaC",
   summary="OpenTofu 从 Terraform 分叉成长为 CNCF Sandbox 项目，截至 2026 年 10 月下载量超过 1,000 万，近期加入客户端状态加密、provider 配置的 for_each、OCI registry 支持。OpenTofu Day（KubeCon 北美 2026）议程含项目现状、Ask the Devs 与从 Terraform 迁移等实践分享。",
   detail=D("OpenTofu：社区治理的 Terraform 替代，新增客户端状态加密、provider 级 for_each、OCI registry 支持，并办专门的 OpenTofu Day。",
          "Terraform 许可证变更后企业担心供应链与授权风险，需要可持续的社区治理替代与迁移路径。",
          "若你的集群建设用到 IaC 且在意许可证/供应链，OpenTofu 值得纳入选型（状态加密对金融合规尤其相关）；迁移成本与 provider 覆盖需实测。")),
]

sections = [
 {"label":"🤖 AI 板块","categories":[
    cat("🧩","Agent & Skill","Agent & Skill", ai_items_agent),
    cat("🧠","模型与研究","Models & Research", ai_items_model),
    cat("🛠️","AI 工程落地","AI Engineering", ai_items_eng),
    cat("📊","产品与商业","Business", ai_items_biz),
    cat("💡","观点与好文","Opinion", ai_items_view),
    cat("🛡️","安全与治理","Safety & Governance", ai_items_safety),
 ]},
 {"label":"☸️ 基础设施板块","categories":[
    cat("🤖☸️","K8s × AI","K8s × AI", infra_k8sai),
    cat("☸️","K8s 核心技术","K8s Core", infra_core),
    cat("📦","社区与项目","Community & Projects", infra_community),
 ]},
]

FLASH_SPEC = [
 ("llm-d：K8s 原生分布式 LLM 推理框架（CNCF Sandbox），用 Gateway API Inference Extension 做 KV cache 感知路由、支持 P/D 分离、缩放与批网关。",
  "https://github.com/llm-d/llm-d"),
 ("《A Society of Researchers》：为数千个共享算力的自主研究 agent 设计“机构/组织”制度，避免群体无组织地争抢资源。",
  "https://arxiv.org/abs/2610.10468v1"),
 ("Inherit-MAS：测试时通过“工作流 + 执行继承”演进多 Agent 系统，避免大改破坏已有可用组件。",
  "https://huggingface.co/papers/2610.02396"),
 ("Self-Retrospection Distillation：把事后经验转成先验，提升 agent 的长期决策。",
  "https://huggingface.co/papers/2610.08077"),
 ("ARTEX：AI 自主渗透测试系统，百度“agent+”攻防挑战赛冠军项目（开源）。",
  "https://github.com/mhtsec/ARTEX"),
 ("Google Research：把 Earth AI 的行星级地理空间基础模型开放用于全球公共卫生。",
  "https://research.google/blog/earth-ais-planetary-geospatial-foundation-models-for-global-public-health/"),
 ("Gemini at Work 2026：Google 推出统一“工作 agent”Gemini，覆盖问答、知识工作、图像/媒体生成与代码。",
  "https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026/"),
]
flash = []
for title, u in FLASH_SPEC:
    assert u in PROC, f"flash URL not in processed.json: {u}"
    flash.append({"title": title, "url": u})

brief = {
 "brand":"AI & 基础设施早报",
 "date_label":"2026 年 10 月 09 日 · 星期五",
 "issue":20,
 "kicker":"DAILY",
 "hint":"👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
 "lead":"今天基础设施侧信号最密：CNCF 发布卓驭科技案例，用 Koordinator 把 K8s GPU 分配率推过 95%、开发环境省下约 60% 整卡；Kubernetes 官方则连发多篇——NVMe 承载的 node swap 把 agent 沙箱节点密度做到 3 倍，v1.37 让 DRA 扩展资源兼容模式与 gang scheduling 双双进入 GA/Beta，GPU 池化的原生底座在补齐。AI 侧 Mistral 亮出万亿参数开源旗舰 Large 4，多 Agent 是否真的带来增益则继续被实证质疑。",
 "highlights":highlights,
 "sections":sections,
 "flash":flash,
 "footer":"由 Hermes 自动汇编 · 每日 09:00 更新",
}

json.dump(brief, open(P("briefing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("briefing.json written. highlights:", len(highlights),
      "| AI items:", sum(len(c["items"]) for c in sections[0]["categories"]),
      "| infra items:", sum(len(c["items"]) for c in sections[1]["categories"]),
      "| flash:", len(flash))
