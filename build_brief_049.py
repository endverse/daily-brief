#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 049 (2026-11-09)."""
import json

PROC = json.load(open("processed.json", encoding="utf-8"))
BY_URL = {i["url"]: i for i in PROC}


def U(key):
    """Resolve a URL by prefix (before '?'), returning the exact processed URL."""
    hits = [u for u in BY_URL if u.split("?")[0] == key or u == key]
    if len(hits) != 1:
        raise SystemExit(f"URL lookup failed ({len(hits)}): {key}\n{[h for h in BY_URL if key in h]}")
    return hits[0]


def item(title, url_key, summary, d1, d2, d3, tag=None, oss=None):
    u = U(url_key)
    it = {
        "title": title, "url": u, "summary": summary,
        "source": BY_URL[u].get("source", ""),
        "detail": [
            {"key": "能做什么", "value": d1},
            {"key": "解决什么痛点", "value": d2},
            {"key": "值不值得", "value": d3},
        ],
    }
    if tag:
        it["tag"] = tag
    o = BY_URL[u].get("oss") if oss is None else oss
    if o:
        it["oss"] = True
    return it


# ---------------- highlights ----------------
highlights = [
    {
        "title": "Kinference：给 vLLM + Kubernetes 补一层 KV-cache 感知的推理控制面",
        "url": U("https://vllm.ai/blog/2026-11-04-introducing-kinference"),
        "source": "vLLM Blog（Buoyant 开源）",
        "summary": (
            "Buoyant 开源 Kinference，定位是 vLLM 之上的推理控制面，而不是又一个推理引擎：客户端把 OpenAI / Anthropic "
            "兼容请求指向它的 HTTP 端点，由它负责 token 速率限制、租户用量与成本核算、推理策略路由。最核心的机制是 "
            "KV-cache 感知的负载均衡——按 GPU 队列长度、历史性能以及目标 worker 上已有的 KV cache 内容打分，把请求发给"
            "「为这条请求要做的工作最少」的 vLLM worker，而标准 Kubernetes Service / kube-proxy 完全不看缓存。"
            "官方基准里，同等 SLO 下共享前缀负载的 goodput 是 kube-proxy 的 7.4 倍、多轮对话 3.5 倍，中位 TTFT 降低 95%，"
            "而且 kube-proxy 在测试的任一并发度都没能达到其设定 SLO。策略层用 CRD InferencePolicy 表达，可按租户、模型、"
            "GPU 池状态、提示词语义分类路由：低复杂度请求发给便宜模型，本地队列积压时溢出到 Bedrock / Databricks，"
            "命中 PII 时禁止出集群（fail closed）。策略是 YAML、可进 git、可 lint、可独立回滚，这是它和硬编码在网关里的"
            "路由规则最大的区别。"
        ),
        "note": (
            "Kinference 由 Buoyant 发起并开源，底层推理仍交给 vLLM。接入方式仅为把客户端指向其 HTTP endpoint，发送 "
            "OpenAI 或 Anthropic 兼容流量。控制面能力：token rate limiting、租户用量与成本追踪、KV-cache 感知负载均衡、"
            "InferencePolicy 策略。策略 CRD 为 kinference.buoyant.io/v1alpha1，示例包括按语义复杂度选模型、按队列深度"
            "溢出到云 provider、PII 请求 fail-closed。基准数字：共享前缀 goodput 7.4×、多轮 3.5×，中位 TTFT −95%，"
            "中位端到端延迟下降 45%（其中一类负载）。"
        ),
        "detail": [
            {"key": "能做什么", "value": "vLLM 之上的控制面：按 GPU 队列、历史性能与目标 worker 的 KV cache 内容做路由打分，叠加 token 限流、租户成本归属与 InferencePolicy CRD 策略（语义分类、队列积压时溢出到云 provider、PII fail-closed）。"},
            {"key": "解决什么痛点", "value": "K8s 默认 Service/kube-proxy 是四层转发，不看请求会命中哪份 KV cache，共享前缀与多轮对话会反复 prefill；多租户推理平台也缺限流、成本归属与可审计的路由策略。"},
            {"key": "值不值得", "value": "自建 vLLM 推理平台少见的「控制面」开源实现，且直接给出与 K8s 默认负载均衡的对比数字，和你在推的 K8s 上跑推理直接相关；但仍是 v1alpha1、单一厂商博客基准，生产前要验证与现有网关/鉴权/多集群的契合度和策略引擎的稳定性。"},
        ],
    },
    {
        "title": "阿里云 CIO 三年复盘：AI 生码率涨了，端到端交付只快 3%–7%",
        "url": U("https://www.infoq.cn/article/YZx670AAiudsqZjx3UNo"),
        "source": "InfoQ 中国",
        "summary": (
            "阿里云智能集团副总裁、CIO 蒋林泉复盘三年 AI 实践，给出一个反直觉结论：AI 生码率和代码量持续上涨，"
            "但端到端交付一个需求所消耗的人力几乎没变。他把需求全流程拆成六段——需求设计与评审 20%、交互视觉设计 10%、"
            "技术方案设计 15%、编码开发 20%、前后端联调集成 15%、测试与 Bugfix 20%。再拆编码这 20%：真正吃时间的是"
            "存量核心系统改造、与老系统融合、保证上线稳定的关键非功能性代码，代码量不大却占 65% 以上的编码时间；"
            "而 AI 最擅长的 CRUD、前端 UI、测试代码、胶水代码占大部分代码量，却只花不到 35% 的时间。按 20%×35% 计算，"
            "即便 AI 把这部分压到零，端到端理论收益上限也只有约 7%，业界实际多在 3%–5%。他进一步指出瓶颈已转移到"
            "Review 与线上责任：能兜底的少数「老司机」被大量 AI 生成代码打爆，绕过 Review 则直接变成技术债。"
        ),
        "note": (
            "讲者为阿里云智能集团副总裁、CIO 蒋林泉，内容为其负责的 CIO 线三年 AI 实践复盘。关键数字：需求六阶段耗时占比 "
            "20/10/15/20/15/20；存量核心与关键非功能代码占编码时间 65%+ 但代码量占比小；端到端提效理论上限约 7%，"
            "业界实测 3%–5%。核心判断：AI Native 是组织问题，token 用量、Vibe Coding、通用智能体的使用量不能证明组织"
            "形态发生变化；需要 CIO 与 CPO 联动，工具定义能力边界、组织决定能力能否进入真实工作。"
        ),
        "detail": [
            {"key": "能做什么", "value": "一套把「AI 提效」拆到流程颗粒度的度量方法：先按需求六阶段计时，再按代码类型（存量核心 vs 常规）拆编码耗时，算出端到端理论上限，用来解释局部快、整体不快。"},
            {"key": "解决什么痛点", "value": "企业习惯用生码率、token 消耗、Agent 覆盖率证明 AI 有效，但这些指标和 E2E 交付时间脱钩；同时大量 AI 代码把 Review 与线上责任压到少数资深工程师身上，形成新瓶颈。"},
            {"key": "值不值得", "value": "对正在推 AI-native 转型、需要向管理层解释投入产出的人是少见的量化框架，也能直接用来评估自家研发流程该往哪一段投人；但 7% 上限建立在「只优化常规代码」的假设上，需按自家代码结构与存量系统比例重算，不能直接照搬。"},
        ],
    },
]

# ---------------- AI 板块 ----------------
agent_skill = [
    item(
        "EvoMemState：把 agent 记忆从「独立事实」改成带关系与推理状态",
        "https://huggingface.co/papers/2611.03743",
        "现有 agent 长期记忆多按「抽取事实—存储—检索」组织，事实之间如何互相更新、约束、冲突，以及当前请求该用哪条，都是隐式的。"
        "EvoMemState 增加两种状态：Relational State 记录每条事实的有效性、作用域与演化关系，Reasoning State 由强化学习训练的策略按当前请求生成，决定这些事实该如何应用。"
        "在长期对话与记忆使用基准上，它的检索完整性与记忆 grounding 的回答准确率都稳定优于现有记忆系统，代码已开源。",
        "把记忆建成「持久事实 + 关系状态 + 推理状态」三层：本体引导抽取事实并建关系，RL 把记忆使用经验内化成策略，按请求生成 Reasoning State 再驱动回答。",
        "把记忆当互不相干的事实堆着，新事实与旧事实冲突、过期、限定条件不同时无法处理，检索出来的内容也不知道该不该用。",
        "做个人 agent / 长期陪伴类产品时，这是一条比「向量库 + 摘要」更结构化的路线，且有开源实现；代价是引入本体与 RL 训练环节，冷启动和调参成本高于纯检索方案。",
    ),
    item(
        "VisSearch-Bench：多模态 agent 长程视觉搜索，最强系统只完整解出 26.47%",
        "https://huggingface.co/papers/2611.04894",
        "现有搜索基准多是「用图片定位实体，然后转文本检索」，测不到 agent 如何跨图像、对象与搜索步骤串联证据。"
        "VisSearch-Bench 提供 204 个人工编写任务、覆盖 7 个主域 25 个子域，分集合式视觉搜索、序列式视觉搜索、宽深混合搜索、竞争性视觉消歧、视觉结构引导搜索五类。"
        "每道题给出参考答案、可追溯证据与评分规则，准确率看整题是否解出，Process Score 单独算子问题与中间证据的正确性。"
        "16 个多模态模型中最好的系统即使带搜索工具也只完整解出 26.47%。",
        "204 题、7 域 25 子域的长程视觉搜索基准，五类任务覆盖跨图证据串联，同时给整题准确率与过程分两套指标。",
        "多模态 agent 的视觉能力评估长期停在单图问答或「图片只用来认实体」，无法判断它在多步搜索中能否管理视觉上下文、串联证据。",
        "做视觉/浏览器类 agent 评测时可以直接拿来当压力测试集，26.47% 的上限说明这块远未解决；但它偏学术基准，和业务任务的分布差距需要自行校准。",
    ),
    item(
        "phoneuse：用 Linux 主机操作未越狱 iPhone，并封装成 agent skill",
        "https://github.com/lxe/phoneuse",
        "phoneuse 把 iPhone 画面通过 AirPlay 镜像到 Linux 主机，再用蓝牙 HID 反向注入鼠标键盘，不装 App、不越狱就能「看见并操作」一台真实 iPhone。"
        "仓库同时提供 CLI 与供 agent 调用的 skill，把「手机在环」变成可脚本化的接口。",
        "AirPlay 入、蓝牙 HID 出，加一层 CLI 与 agent skill 封装，实现无侵入的真机操作闭环。",
        "移动端流程验证要么依赖模拟器（覆盖不到真机行为），要么要人手动点；agent 想测 App 没有可用的操作接口。",
        "如果团队有 iOS 端要验证、又不想上云真机平台，这是很轻的一条路子；但依赖同一局域网、AirPlay 稳定性与蓝牙配对，适合验证不适合大规模并发。",
        oss=True,
    ),
]

ai_eng = [
    item(
        "vLLM v0.33.0 起发 LibTorch Stable ABI wheel：升级 PyTorch 不用重编",
        "https://vllm.ai/blog/2026-11-06-stable-abi-cuda",
        "vLLM 的 C++ 后端大量调用 LibTorch，过去 PyTorch 一升级就要重编重链 vLLM。v0.33.0 起 vLLM 发布 LibTorch ABI Stable 的 CUDA wheel，"
        "同一份 vLLM wheel 可跨兼容的 PyTorch 版本使用，换 torch wheel 后直接导入即可。实现依赖 PyTorch 三层 stable ABI（C shim、C++ 包装、"
        "headeronly 工具），未覆盖的算子走 torch_call_dispatcher；迁移覆盖 175 个 .cpp/.cu 与 120+ 头文件，按块搬进独立 stable 库，"
        "并用 TORCH_TARGET_VERSION 让构建在引入不稳定头文件时直接失败。代价是少量 host 侧类型转换开销，CUDA Graphs 下基本消失。",
        "发布 ABI 稳定的 CUDA wheel：把 kernels 迁到 stable C shim / C++ 包装上，未稳定的 API 用 torch_call_dispatcher 兜住，并用构建标志强制约束。",
        "PyTorch 版本节奏快于 vLLM 发版节奏，每次升级都要重编整个推理引擎，发行版与用户都被卡在旧 torch 上。",
        "自建推理服务、又需要跟进新 torch/CUDA 特性时价值直接：升级路径从「等 vLLM 重编」变成「换 wheel」；但要接受 stable ABI 只覆盖部分算子，且仍有 CUDA 版本与 Python API 的兼容约束。",
        oss=True,
    ),
    item(
        "Cloudflare Auto Router 基准：可靠性 +10 个百分点，成本约三分之一",
        "https://www.infoq.cn/article/gOcDmZM2MPAQhWtNb6IJ",
        "Cloudflare 在 AI Gateway 推出 Auto Router 公测：模型名设为 cloudflare/auto 后，边缘 GPU 上的多头分类器给请求分配 14 类任务概率，"
        "并从复杂性、歧义性、风险程度、上下文依赖四个维度打 1–5 分，再按公开公式「效用 = 预期质量 − 自适应成本惩罚」选模型。"
        "官方基准用 97 个任务、每模型采样 3 次、1 万次 bootstrap 重采样，结果是可靠性提升约 10 个百分点、成本约为原来的三分之一。"
        "限制也很明确：分类只看最近几轮、文本上限 8 KiB；没有 session ID 时同一对话的请求可能落到不同模型，前缀缓存无法复用；"
        "路由权重来自基准测试，新模型要手工加进评分矩阵。",
        "两阶段路由：先按格式/凭证/预算过滤候选池，再在边缘用 Workers AI 跑多头分类器（14 类任务 + 四维 1–5 分），按「质量 − 成本惩罚」打分选模型。",
        "多模型网关里「该用哪个模型」通常靠人工规则或全量走最贵模型，缺少按请求难度动态降本的可审计机制。",
        "做模型网关/多 provider 路由时这份基准与公式值得当参考，尤其它公开了自家路由器落败的对照组；但分类上下文只有 8 KiB 且按最近几轮判风险，长会话里的高风险指令可能被降级，生产要自己补跨轮风险标签。",
    ),
    item(
        "腾讯混元：163 名内部专家盲测，模型迭代压到 2–3 个月一版",
        "https://www.infoq.cn/article/azhgYaRTIjsSSVfA8AaU",
        "腾讯云披露混元研发体系的调整：2025 年 12 月启动重组，2026 年 1 月升级后训练基础设施以适配 agent 长程推理，此后稳定在每 2–3 个月一次重大版本。"
        "评测上除 Terminal-Bench、DeepSWE 与 Arena，还组织 163 名内部高频使用大模型的业务专家，围绕软件工程、游戏开发等四类场景做盲测。"
        "MaaS 侧要解决的是同一批模型在不同算力环境下的稳定交付，以及百万 token 成本从「元」降到「角」「分」之后的调度与推理优化。",
        "用 163 名内部专家盲测替代纯公开榜单，按 CodeBuddy / WorkBuddy 的真实任务定义优化方向，并以 2–3 个月节奏迭代。",
        "公开 benchmark 集中在编程类任务（一项研究统计 43 套 agent 基准、7.2 万任务，与 1016 种职业对照后发现管理与法律等场景覆盖不足），榜单好不等于长程任务能完成。",
        "如果团队在用国内 MaaS，这篇给出了厂商侧评测与成本曲线的口径，可作为选型时的提问清单；但内容偏发布会叙述，缺少可复现的对比数据。",
    ),
]

models = [
    item(
        "Muir：门控压成低秩投影，1.34B 外推 1000 万 token 无困惑度漂移",
        "https://huggingface.co/papers/2611.08376",
        "线性注意力把上下文压进固定大小的 KV state，门控 delta 规则要同时做擦除与写入。作者分析发现 state 更新对擦除的敏感度远低于写入"
        "（key 能量经激活与归一化后集中在少数通道），于是 Muir 把全部门控融进一个敏感度分配的低秩投影，再用匹配滤波读出给 state 行重新加权，"
        "省下的参数投到更宽的 FFN。166M–1.34B 规模上困惑度比 GDN-2 低 1.8%–2.0%、比 Transformer 低 2.5%–3.6%，常识准确率最高 +1.9 分；"
        "1.34B 模型从 4K 训练长度外推到 1000 万 token 流无困惑度漂移，100 万 token passkey 接近 100%，吞吐与 GDN-2 持平。",
        "按擦除/写入敏感度不对称做低秩门控 + 匹配滤波读出，并设计大 chunk 下数值稳定的并行更新算法。",
        "门控线性注意力里慢衰减 state 行范数过大会主导读出、逼出更强的写入擦除，形成干扰；标准 chunkwise 算法在大 chunk 下数值不稳定。",
        "跟踪长上下文架构时值得读：它把「门控该多精细」这件事量化了，且给出 10M token 外推的实测；但仍是 1.34B 规模的研究模型，离生产推理栈还有距离。",
    ),
    item(
        "WeLM-Image：微信单卡图像模型，31.7B 总参 / 5.4B 激活，H20 上 4.98 秒出 1024²",
        "https://huggingface.co/papers/2611.07392",
        "微信的 WeLM-Image 把文生图、指令编辑、多参考合成放进一个模型：文本、参考图与目标 latent 拼成一条交错序列，MoT 主干共享 attention 但理解与生成各用独立参数，"
        "两条路径再接 MoE，总参 31.7B、每个目标 latent token 约激活 5.4B。它面向单卡部署，1536 分辨率版本在 PRISM-Bench、Qwen-Image-Bench、UnicBench 上"
        "位列所评开源模型第一；MeanFlow 少步蒸馏出的 Turbo 版在单张 H20 上 8 步、4.98 秒生成 1024×1024。",
        "MoT + MoE 的统一图像模型，理解与生成参数分离以降低优化干扰，配套生成导向的数据引擎与 rubric/checklist 奖励分阶段训练，最后做噪声感知的 on-policy 蒸馏。",
        "统一多模态模型里理解与生成任务互相干扰，且大模型难以在单卡、消费级并发下部署。",
        "关注「单卡可部署的图像基础模型」时这是目前少见的工业级样本（微信大规模消费场景）；但权重是否开放、许可证与中文场景表现需再去仓库确认。",
    ),
    item(
        "PACT 跨模型传递被拆穿：部分收益用「无用信号」也能复现",
        "https://huggingface.co/papers/2611.06976",
        "PACT 把大模型的 prompt 表示传给小模型做生成，理论上兼顾能力与成本。作者开源 PLatour 框架（冻结模型 + 零初始化线性桥，支持混合注意力），"
        "在生成任务上超过开源基线，并在数学与代码基准上以更小的 sender 超过 Mostik 报告的结果。"
        "但受控实验发现：部分任务的收益用无信息 sender 信号、自通信或只训 receiver 也能复现——可训练桥本身是参数高效适配器，未必真用上了 sender 信息。"
        "为此作者提出 PACT-Check，量化一个训练好的 PACT 系统里有多少增益真正来自通信。",
        "开源的 PACT 框架 + 归因方法：用零初始化线性桥连接冻结的大小模型，再用 PACT-Check 做消融，判断增益来自通信还是桥的适配效应。",
        "跨模型 latent 通信的论文普遍只报任务提升，缺少「收益是否真的来自 sender」的对照，容易把参数高效微调的效果误读成模型协作。",
        "做小模型+大模型协同推理时，这篇的结论比方法更有价值：先做 PACT-Check 式消融，别把适配器收益算成通信收益；框架本身可直接复用。",
    ),
]

product = [
    item(
        "OpenAI 自研 Git 后端 Pando：单次推送中位耗时降近八成，并收购 Pierre",
        "https://www.qbitai.com/2026/11/508449.html",
        "OpenAI 公开内部 Git 后端 Pando 承接代码存取，4 月起已承载真实开发流量，官方称换上后单次推送的中位耗时降了近八成；"
        "背景是 Codex 让一名工程师可同时推进多份改动，GitHub 服务中断频发。面向 Codex 用户，OpenAI 还准备收购 Pierre，"
        "把其 Trees、Diffs 与 Code Storage 能力并入产品——Lovable 用 Pierre 时每周新建超 800 万个仓库、峰值每秒 250 个。",
        "自建 Git 存储后端承接高频小提交，叠加收购来的 Trees/Diffs/Code Storage 做面向 agent 的代码存储与差异视图。",
        "AI 生成代码把提交频率与仓库数量推高一个量级，通用 Git 托管在推送吞吐与中断上成为瓶颈。",
        "对平台侧是明确信号：agent 时代的代码基础设施要按「每秒数百仓库、推送密集」重新设计；自建 Git 后端投入大，但 Lovable 这类客户量级说明需求真实存在。",
    ),
]

opinion = [
    item(
        "Simon Willison：同一 parse_number()，C 扩展 14 KB vs Rust 321 KB",
        "https://simonwillison.net/2026/Nov/8/sqlite-parse-number-c-vs-rust/",
        "他用 Claude Opus 5.5 把同一个 parse_number()（把 -$1,234.56、12.5% 这类字符串转成数值）分别实现为 C 与 Rust 的 SQLite 可加载扩展。"
        "产物大小差距明显：C 扩展 14 KB，Rust 用 rusqlite 是 321 KB、sqlite-loadable-rs 是 298 KB；但最初 Rust 更快，因为 Rust 的 strtod 等价实现约快一倍。"
        "随后让模型手写 C 的十进制快速路径后反超：200 万行净耗时混合数据 19 ns/行（Rust 41–46 ns，原 C 67 ns），整数 16 ns、小数 18 ns，"
        "8 百万次 fuzz 校验各版本结果一致。",
        "四种实现（两个 C、两个 Rust）跑同一套类型保持、解析规则与浮点精度测试，公开每行纳秒级成本与 .so 体积。",
        "选 SQLite 扩展语言时缺少可比的体积/性能数据，容易凭语言偏好决定。",
        "写 SQLite 扩展或做「C 与 Rust 互操作」选型时，这是一份可直接复现的最小基准；结论也不是「C 更快」，而是热点路径手写后 C 才反超，默认实现反而 Rust 占优。",
    ),
]

# ---------------- 基础设施板块 ----------------
k8s_ai = [
    item(
        "Agent Sandbox v1.0.10：路由支持 gRPC-Web，NetworkPolicy 改为按沙箱标签放行",
        "https://github.com/kubernetes-sigs/agent-sandbox/releases/tag/v1.0.10",
        "K8s SIG 的 agent 沙箱项目发布 v1.0.10：sandbox-router 增加 gRPC-Web 转码以支持浏览器客户端，sandboxd 增加单次执行超时与 "
        "mkdir、递归 list、create-only 写入、move、copy、tar 解包等文件操作，镜像正式进 registry.k8s.io。"
        "Go SDK 为 Kata 与 gVisor 增加 ConnectivityRouterPortForward，控制器修了 SandboxClaim 镜像同步与 SandboxWarmPool 副本计数。"
        "破坏性变更在 NetworkPolicy：sandbox 出网只允许带 agents.x-k8s.io/sandbox-name-hash 标签的 Pod，且放行全部 TCP 端口；"
        "同时对任意目的地放行 443/6443 与 53，修掉 API server 跑在 host-network 节点（如 Cilium）时 Pod-cache 与 TokenReview 失败的问题。",
        "新增能力：gRPC-Web 转码、sandboxd 单次执行上限与扩展文件操作、registry.k8s.io 镜像、Kata/gVisor 的端口转发、Hyperlight microVM 与 GKE L4 GPU 快照示例。",
        "agent 沙箱既要隔离又要能被浏览器/网关调用，还要在 host-network + Cilium 这类环境下正常做鉴权与 Pod 缓存同步。",
        "如果公司在评估 Daytona 的替代方案，这是最贴近「K8s 原生 agent 沙箱」的上游项目，v1.0.x 已进入补丁节奏、且有 NetworkPolicy 这类生产细节；但升级要按 release note 补 NetworkPolicy，否则路由到无标签 Pod 会直接不通。",
        oss=True,
    ),
]

k8s_core = [
    item(
        "Kubernetes v1.36.6：修 resourceClaimStatuses 抖动与 kube-proxy 的 sysctl 回归",
        "https://github.com/kubernetes/kubernetes/releases/tag/v1.36.6",
        "v1.36.6 是本轮补丁版本，改动集中在几个会咬人的地方：Pod 使用多个 claim 时 .status.resourceClaimStatuses 会在不完整列表之间来回抖动；"
        "同名重建的 Job 会继承上一个 Job 的 pending Pod expectations 而长期不收敛；kube-scheduler 对使用负操作符的 namespaceSelector "
        "在 pod affinity/anti-affinity 上判断错误，导致被排除命名空间的 Pod 仍影响过滤与打分。"
        "另外 apiserver 把请求头值上限提到 16384，避免 Go 1.27 默认的 500 让带 500+ 组的被代理/模拟用户直接吃 HTTP 431；"
        "kube-proxy 在无权改 sysctl 时不再强设 nf_conntrack_max，修掉 1.36 引入的回归。",
        "补丁版本，含 DRA 相关的 status 抖动修复、Job 控制器 expectations 修复、调度器 namespaceSelector 修复、apiserver 请求头上限与 kube-proxy sysctl 回归修复。",
        "DRA 与多 claim Pod 的状态抖动会干扰上层控制器判断，负操作符 namespaceSelector 的误判会让亲和性调度结果与预期不符。",
        "如果集群已上 1.36 且用 DRA 或 pod affinity，这个补丁值得跟；kube-proxy 那条对收紧过 sysctl 权限的节点尤其相关。升级前仍按惯例看 CHANGELOG 的 Urgent Upgrade Notes。",
    ),
    item(
        "Istio 1.30.8：一次修 7 个 CVE，ambient 明文可绕过 mTLS（CVSS 8.2）",
        "https://github.com/istio/istio/releases/tag/1.30.8",
        "Istio 1.30.8 是安全补丁版，一次修 7 个 CVE。最严重的是 ambient 模式下端口级策略的运算符优先级错误，"
        "使允许明文的策略覆盖了要求 mTLS 的端口，攻击者可用明文访问本应强制 mTLS 的端口（CVSS 8.2）；"
        "其次是畸形 xDS 资源名可让 istiod 崩溃并全网格循环重启（7.7），以及复用已拆除连接的 4 元组绕过 sidecar conntrack（7.4）。"
        "其余包括：ambient AuthorizationPolicy 条目未通过 webhook 时导致 istiod 崩溃、多集群下 proxy 可冒领他集群 SDS secret、"
        "ztunnel 解析畸形 HTTP 头 panic、JWKS 后台刷新未校验响应形状。",
        "安全版本，修 7 个 CVE（8.2/7.7/7.4 三个 High，其余 Moderate），涉及 ambient 端口策略、istiod xDS 解析、sidecar conntrack、多集群 SDS、ztunnel HBONE 头解析与 JWKS 缓存校验。",
        "ambient 模式默认开启后，策略表达式的优先级与 conntrack 复用成为新的绕过面；istiod 单点崩溃会直接停掉全网格配置分发。",
        "跑 Istio、尤其开了 ambient 的集群应尽快升；升级只涉及控制面与 ztunnel/sidecar 镜像，但要确认 1.30.8 与当前 CRD 版本兼容，并在测试集群验证策略优先级变化不会阻断正常流量。",
    ),
]

cloud_native = [
    item(
        "Lima v2.3：Windows 上不依赖 QEMU 起 VM，Linux 主机新增共享/桥接网络",
        "https://www.cncf.io/blog/2026/11/08/lima-v2-3-native-on-windows-vmnet-on-linux-and-menu-tui/",
        "Lima v2.3 于 11 月 6 日发布：Windows 主机上通过实验性 HCS 驱动直接启动 VM，不再依赖 QEMU，并支持原生 Windows OpenSSH；"
        "Linux 主机新增实验性 lima:shared、lima:host、lima:bridged 三种网络，由新的 lima-privileged-net helper 实现；"
        "macOS 的 VZ 驱动可把宿主机块设备直通给 guest（limactl start --block-device），并新增 audio.microphone 与 hostLoopback 隔离选项；"
        "另有 limactl menu 菜单式 TUI、limactl screenshot，以及本地转发端口也开始校验 guest SSH host key。",
        "v2.3 新增 HCS 驱动（Windows 无需 QEMU）、Linux 侧共享/桥接网络、VZ 块设备直通、菜单 TUI 与 SSH host key 校验；Windows guest 支持 provision。",
        "在 Windows 或 Linux 主机上起轻量 VM 跑容器/K8s 试验环境，长期受限于 QEMU 依赖与网络模式单一。",
        "你要用 multipass/Lima 在本机搭 K8s 集群，这版的 Linux 桥接网络与块设备直通直接相关；但网络三项都标了 experimental，先别放进依赖稳定性的流程里。",
    ),
    item(
        "OpenTelemetry Collector v0.165.0：confighttp 删废弃字段，memory_limiter 可关强制 GC",
        "https://github.com/open-telemetry/opentelemetry-collector/releases/tag/v0.165.0",
        "v0.165.0 的破坏性变更集中在 pkg/confighttp：移除已废弃的 IdleConnTimeout、MaxIdleConns、MaxIdleConnsPerHost、DisableKeepAlives 四个字段，"
        "配置里还留着的会直接报错。功能侧，memory_limiter 新增 garbage_collector.enabled，可关掉内存超限时的强制 GC；"
        "queue_batch 处理器在 traces/metrics/logs 升到 beta、profiles 为 alpha；pdata 的 Map Get/Range/All 减少分配，"
        "confighttp/confgrpc 的 client 构造允许替换 dialer；service 在 pipeline 同时用 batch processor 与 exporterhelper 批处理时启动告警。",
        "破坏性字段移除 + memory_limiter GC 开关 + queue_batch 升 beta + pdata 性能优化 + 自定义 dialer 注入。",
        "Collector 作为所有遥测流量的汇聚点，内存抖动与 GC 停顿会直接影响采样与导出；废弃字段长期不清又会让配置升级踩坑。",
        "自建 observability 栈、Collector 版本跟得比较紧的话，这个版本要先扫一遍配置里有没有那四个字段；memory_limiter 的 GC 开关对高吞吐场景调优有用。",
        oss=True,
    ),
]

sections = [
    {"label": "🤖 AI 板块", "categories": [
        {"label": "Agent & Skill", "title": "Agent & Skill", "emoji": "🧩", "items": agent_skill},
        {"label": "AI 工程落地", "title": "AI 工程落地", "emoji": "🛠️", "items": ai_eng},
        {"label": "模型与研究", "title": "模型与研究", "emoji": "🧠", "items": models},
        {"label": "产品与商业", "title": "产品与商业", "emoji": "📊", "items": product},
        {"label": "观点与好文", "title": "观点与好文", "emoji": "💡", "items": opinion},
    ]},
    {"label": "☸️ 基础设施板块", "categories": [
        {"label": "K8s × AI", "title": "K8s × AI", "emoji": "🤖☸️", "items": k8s_ai},
        {"label": "K8s 核心技术", "title": "K8s 核心技术", "emoji": "☸️", "items": k8s_core},
        {"label": "云原生周边", "title": "云原生周边", "emoji": "☁️", "items": cloud_native},
    ]},
]

flash = [
    {"title": "OpenAI 新融资到账 110 亿美元，不及原计划一半", "url": U("https://www.qbitai.com/2026/11/508344.html")},
    {"title": "资本正在撤离「世界模型」：头部基金愿投的项目一只手数得过来", "url": U("https://www.qbitai.com/2026/11/508466.html")},
    {"title": "vLLM 当天支持 Kimi K3.1 Pro：KDA 混合注意力稀疏 attention + FP8/NVFP4 packed KV cache", "url": U("https://vllm.ai/blog/2026-11-04-kimi-k31-pro")},
    {"title": "meta/astryx：可完全定制、面向 agent 的开源设计系统", "url": U("https://github.com/meta/astryx")},
]

lead = (
    "今天的重心是「推理平台的控制层」和「AI 提效的真实账」。基础设施侧，Buoyant 开源 Kinference，把 KV-cache 感知路由、"
    "租户限流与策略化路由做成 vLLM 之上的控制面，给出对 kube-proxy 共享前缀 goodput 7.4 倍、中位 TTFT 降 95% 的数字；"
    "K8s SIG 的 Agent Sandbox 进入 v1.0.10 补丁节奏，NetworkPolicy 改成按沙箱标签放行，是能直接对照自建 agent 沙箱的一手细节。"
    "AI 侧，阿里云 CIO 把三年 AI 实践拆到流程颗粒度：编码只占端到端 20%，其中 AI 擅长的部分又只占编码时间 35%，"
    "端到端提效上限约 7%、业界 3%–5%——这组数字比任何生码率都更能解释「局部快、整体不快」。另有 vLLM 的 LibTorch Stable ABI、"
    "Cloudflare 自动路由的公开基准，以及 Kubernetes 1.36.6 与 Istio 1.30.8（7 个 CVE）两个值得跟的补丁。"
)

brief = {
    "brand": "AI & 基础设施早报",
    "date_label": "2026 年 11 月 9 日 · 星期一",
    "issue": 49,
    "kicker": "DAILY",
    "hint": "👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
    "lead": lead,
    "footer": "由 Hermes 自动汇编 · 每日 09:00 更新",
    "highlights": highlights,
    "sections": sections,
    "flash": flash,
}

# sanity: every item has non-empty title
for h in highlights:
    assert h.get("title")
for s in sections:
    for c in s["categories"]:
        for it in c["items"]:
            assert it.get("title"), it
            assert it.get("detail") and len(it["detail"]) == 3, it["title"]

json.dump(brief, open("briefing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = len(highlights) + sum(len(c["items"]) for s in sections for c in s["categories"])
print("wrote briefing.json · items:", n, "· flash:", len(flash))
