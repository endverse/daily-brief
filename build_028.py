#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 028 (2026-10-18)."""
import json, sys

proc = json.load(open("processed.json"))
URLS = [it["url"] for it in proc]


def U(sub):
    """Return the exact URL as stored in processed.json whose URL contains `sub`."""
    hits = [u for u in URLS if sub in u]
    if len(hits) != 1:
        raise SystemExit(f"URL lookup failed for {sub!r}: {len(hits)} hits -> {hits[:3]}")
    return hits[0]


def item(sub, title, summary, tag, source, detail, oss=False):
    assert title and summary
    d = {"title": title, "url": U(sub), "summary": summary, "tag": tag, "source": source,
         "detail": [{"key": k, "value": v} for k, v in detail]}
    if oss:
        d["oss"] = True
    return d


# ---------------------------------------------------------------- highlights
H1 = {
    "title": "Agent Sandbox v1.0.7：warm pool 不再把等 Kueue 准入的成员当卡死删掉，sandboxd 加 bearer-token 认证",
    "url": U("agent-sandbox/releases/tag/v1.0.7"),
    "summary": "Kubernetes Agent Sandbox（kubernetes-sigs）v1.0.7 于 10 月 15 日发布，核心是把「热沙箱池」和调度系统接上：warm pool 成员若卡在 SchedulingGated（典型场景就是等 Kueue 准入），现在按 Unschedulable 一样保留，而不是在就绪宽限期到点后被当成卡死回收——这一条直接针对「预热的沙箱被自己回收掉」这类事故。sandboxd 增加了可选的 bearer-token 认证，Go SDK 支持流式命令执行，Python 与 TypeScript SDK 补齐 env/cwd、命名 claim、自定义 kubeconfig，并在 Pod 已终止时 fail-fast；sandbox-router 新增流量指标。示例侧补了多集群 fleet、KubeRay RLlib、跨 sandbox 存活的 agent 记忆，以及 RL fleet 的 namespace 级网络策略。破坏性变更三项：被信号杀死的进程退出码从 -1 改为 128+n（SIGKILL 报 137），Python SDK 不再配置 root logger，WarmPoolNotProgressing 事件的 action 改为具体 hold 原因（HoldingUnschedulable / HoldingSchedulingGated）。",
    "note": "🔎 新闻要点：v1.0.7（2026-10-15）— sandboxd 可选 bearer-token 认证；Go SDK 流式执行命令；Python/TS SDK 对齐 env 与 cwd、命名 claim、自定义 kubeconfig、Pod 终止 fail-fast；warm pool 成员处于 SchedulingGated（如 Kueue 准入）时保留而非删除；sandbox-router 增加流量指标；新增 KubeRay RLlib、跨 sandbox 存活记忆、RL fleet NetworkPolicy 示例；破坏性变更含信号退出码 128+n、SDK 不再配置 root logger、WarmPoolNotProgressing 事件 action 改为 hold 原因。",
    "tag": "Agent 沙箱",
    "source": "GitHub Releases",
    "detail": [
        {"key": "能做什么", "value": "把「agent 跑在 K8s 里」做成控制器级原语：warm pool 预供热沙箱、sandbox-router 路由到具体实例、sandboxd 在 Pod 内执行命令（现支持流式返回与 bearer-token 认证）；这次的实质进步是 warm pool 与调度门打通——成员在等 Kueue 准入期间被保留，而不是被就绪宽限期清掉。"},
        {"key": "解决什么痛点", "value": "自建 agent 沙箱最常见的两个坑是「预热池被误判卡死回收」和「沙箱层与调度层各管一套」；另外单机 agent 记忆在 sandbox 结束后消失、多副本 RL/推理 fleet 缺 namespace 级网络隔离基线，这两点在示例里才第一次有正经写法。"},
        {"key": "值不值得", "value": "你在评估「按会话隔离、空闲挂起」的多用户沙箱时，这类 K8s 原生控制器正对「多用户 × 多会话、上下文隔离、按需回收」这几件事；注意它版本号已过 1.0 但仍是周级补丁节奏、API 仍在演进（本次就有三处破坏性变更），先行小规模验证升级成本再谈替换现方案。"},
    ],
}

H2 = {
    "title": "Gemini 4 Argon 上线：在 20.5 万行 ADK 上无人值守连跑 11 小时，API 输入 2 美元/百万 token",
    "url": U("qbitai.com/2026/10/503701"),
    "summary": "谷歌 Gemini 4（代号 Argon）正式面向开发者、企业与付费订阅用户开放，官方定位是强化长流程任务执行、编程与专业知识工作，多模态生成（3D 场景、代码生成的动态排版）仍是展示重点。第三方 Artificial Analysis 智能指数上 Argon High 与 GPT-6 Astra Max、Claude Fable 5.1 Max 并列 53 分，平均每任务成本 1.99 美元、比 Astra 低约 39%；首发 API 定价输入 2 美元、输出 10 美元每百万 token（截至 11 月 30 日的五折价，12 月 1 日起恢复 4 / 20 美元）。官方公布的工程验证里最硬的一条是：在 20.5 万行 Python 的 ADK 框架上无人值守连续工作 11 小时，提出涉及 32 个文件的 6 项优化并跑完全部 16892 项测试，最终 2 项被合并，长会话内存准备开销降约 40%、包导入耗时降 21%。",
    "note": "🔎 新闻要点：Gemini 4 Argon 面向开发者/企业/付费订阅开放；Artificial Analysis 智能指数 53 分（与 Astra Max、Fable 5.1 Max 并列）；Argon High 平均每任务 1.99 美元、比 Astra 低约 39%；API 输入 2 / 输出 10 美元每百万 token，11-30 前五折、12-01 起恢复 4/20；ADK（20.5 万行 Python）上无人值守 11 小时、改 32 个文件提 6 项优化、跑完 16892 项测试、2 项合入，长会话内存准备开销 -40%、包导入 -21%；Gemma4E2B 推理优化吞吐 3.79 万 → 10.8 万 token/s（2.85×）；Antigravity 中 agent 代码提交量 +35%、回滚减少近 1/3；官方安全报告 217 页；FrontierSWE 与 Terminal-bench 上仍落后主要竞品。",
    "tag": "模型发布",
    "source": "量子位",
    "detail": [
        {"key": "能做什么", "value": "主打「理解目标 → 自己查资料 → 调工具 → 改代码 → 验结果」的多步持续推进：ADK 案例里跨 32 个文件改性能、Chromium 上完成数百文件的架构重构（原估数月压缩到数周）、把 Gemma4E2B 推理吞吐从 3.79 万提到 10.8 万 token/s（2.85×）；专业知识工作侧能把一堆零散资料整理成提案并起草邮件、设置后续自动化。"},
        {"key": "解决什么痛点", "value": "跨文件重构与性能调优这类「读一遍整个代码库才敢动手」的活在人力上极贵且慢；多步任务过去要靠人一路盯着，一旦上下文长了就丢约束。它给的是长时间无人值守跑完＋跑完测试的闭环，省的是人力盯守和来回引导。"},
        {"key": "值不值得", "value": "成本口径值得记：与同级模型同分但每任务 1.99 美元，对批量跑 agent 任务的钱包影响比榜单分数更直接；但要留意榜单分化——FrontierSWE、Terminal-bench 上仍落后主要竞品，长流程能力在自家 demo 里最漂亮、真实项目复现率待观察，且五折价 11 月 30 日结束。"},
    ],
}

# ---------------------------------------------------------------- sections
AI_AGENT = [
    item("four-eval-engineering-lessons",
         "Google Cloud 复盘 agent 评测四条教训：11 条 prompt 里 3 条被 LLM-as-judge 误判",
         "Google Cloud 开发者关系团队拿自家 Google Cloud Developer 插件当试验场，总结了 agent 评测工程的四条教训。第一条是别用 LLM-as-judge 只看最终回复：初始 11 条 prompt 的评测被判 3 条失败，翻原始工具调用日志发现三条其实都做对了（agent 第一步就跑了 gcloud help 校验语法，只是结尾在提醒数据丢失风险而没「邀功」）。第二条是遥测抽取必须保留 turn 结构——现代 harness 会把 skill 加载和两次文档检索塞进同一个 tool_calls 数组并发发出，而 skill 正文往往在检索执行之后才注入上下文，扁平化成一条时间线就永远查不出「agent 为什么无视 skill 指令」。第三条是 live run 与 plan-only run 并排跑：约一半关键发现来自两者差异（某次 live run 第二步就被权限拦住，plan-only 却产出一份 8000 字符、完全无视组织策略与审批的计划）。第四条是用人工专家策展的 golden set 做持续回归，把评测当 CI，而不是拿一次性 demo 当 eval。",
         "Agent 评测", "Google Cloud",
         [("能做什么", "给出四条可直接照做的评测工程规则：按工具调用轨迹（而非最终回复）打分；遥测保留 turn 结构以暴露并发分发导致的「skill 指令注入晚于执行」；live 凭据跑 + 去凭据 plan-only 跑双条件对照；用专家策展的 golden set 当回归基线。"),
          ("解决什么痛点", "agent 评测最容易骗自己：LLM-as-judge 只看文本会放过「做了但没说」的正确行为、也会漏掉并发工具调用抢在 skill 指令之前执行的时序 bug；只跑 live 又常被权限错误在第二步打断，看不到模型真实的推理与路由意图。"),
          ("值不值得", "你在做 skill/agent 落地，这几条直接对应「skill 写了但 agent 不遵守」的排查路径——先怀疑并发分发时序，再怀疑模型；代价是要把评测当持续工程投入（轨迹采集 + golden set 维护），不是加几个 prompt 就完事。")]),
    item("stablyai/orca",
         "Orca：一个 prompt 扇出五个 agent、各自独立 worktree，单日 +830 star",
         "Orca（stablyai/orca）把「同时跑一队编码 agent」做成桌面工具：同一个 prompt 分发给最多五个 agent，每个跑在独立 git worktree 里，结果并排比较后择优合并；支持 Codex、Claude Code、OpenCode、Pi，可用自己的订阅。配套能力包括 Ghostty 级 WebGL 终端（无限分屏、重启保留 scrollback）、Design Mode（点选真实 Chromium 窗口中的 UI 元素，把它的 HTML/CSS 与裁剪截图直接塞进 agent prompt）、SSH worktree（在远端机器跑 agent，带自动重连与端口转发）、以及 diff 行内批注回传 agent。发布当天 GitHub Trending 单日 +830 star。",
         "Agent 编排", "GitHub Trending",
         [("能做什么", "把多 agent 并行比较做成日常工作流：prompt 扇出 → 独立 worktree 隔离改动 → 并排 diff → 择优合并；Design Mode 让前端任务不用手抄 DOM 结构和截图，SSH worktree 让重活跑在远端机器上。"),
          ("解决什么痛点", "多 agent 并行时最大的摩擦是「改动互相踩」和「结果没法比」——共用工作区会互相覆盖，纯 CLI 又没有并排 diff 与可视化上下文；前端任务还要人来回贴 DOM 和截图。"),
          ("值不值得", "你在用多个 agent CLI（含 opencode）时，这类编排层决定的是并行尝试的成本而不是模型能力；注意它绑定各家订阅、以桌面端为主，团队共享与 CI 化支持如何要自己验证，别指望它替你做评测。")],
         oss=True),
    item("stack-overflow-chatgpt-plugin",
         "Stack Overflow for Agents：两个人几周做完，ChatGPT 插件把 agent 创建量推到 10 倍",
         "OpenAI 客户故事：两名工程师用 Codex 在几周内做出 Stack Overflow for Agents（面向 agent 的问答与知识服务），官方称其 ChatGPT 插件带来最高 10 倍的 agent 创建量增长、注册量翻三倍。",
         "Agent 产品", "OpenAI News",
         [("能做什么", "把「agent 之间共享经验」做成产品：agent 遇到问题时向一个公共知识库提问/回答，并通过 ChatGPT 插件把入口嵌进对话流。"),
          ("解决什么痛点", "agent 的重试与踩坑经验目前基本不外流，每个 agent 从零试错；对人类开发者是 Stack Overflow 的问题，对 agent 群体还没有对应物。"),
          ("值不值得", "值得当作「小团队用 codegen 快速验证 agent 赛道产品」的样本看，但官方通稿只给了增长倍数、没给留存与调用结构，作为技术判断依据偏薄。")]),
]

AI_MODEL = [
    item("DeepSeek-V4.1-Flash-1017",
         "DeepSeek-V4.1-Flash-1017 放出：MIT 许可的多模态模型，HN 672 分",
         "DeepSeek 于 10 月 17 日发布 DeepSeek-V4.1-Flash-1017，HF 模型卡为 MIT 许可、pipeline 标为 image-text-to-text（多模态），配套 fp8 / 8-bit 权重；官方说法是相对上一版「基准更强、任务完成更快、输出更短」，即性能与成本的帕累托改进。训练侧强调用带自反馈的强化学习做端到端项目开发（游戏、3D 建模），并针对 DeepSeek Harness、腾讯 CodeBuddy、WorkBuddy 做了适配（需 Harness v0.2.1-rc.1 以上）。自研搜索/抓取端点按每 1000 次调用 0.75 美元计费，10 月 31 日 16:00 UTC 前对 API 用户免费；发布当天 HN 672 分 / 572 条讨论，HF 点赞 931。",
         "模型发布", "Hacker News",
         [("能做什么", "一个 MIT 许可、可自托管的多模态模型，主打「想清楚需求就自己写完整项目」：官方示例覆盖 3D 建模、网页赛车游戏、Godot 引擎复刻，配套搜索/抓取端点让模型能在自研搜索引擎上取实时信息。"),
          ("解决什么痛点", "闭源旗舰的 API 成本与数据出域是硬约束（尤其金融场景），能拿到 MIT 权重且在多模态+代码生成上对标前沿，才有自建推理的选项；短输出 + 更快完成直接压低 token 账单。"),
          ("值不值得", "对「模型可出网、数据不可出网」的架构，这类 MIT 权重模型是自建推理栈的候选；但要先确认它在你关心的编码基准上的实测，官方只给了相对上一版的定性描述，且自反馈 RL 的效果高度依赖 harness 版本。")]),
    item("2610.22355",
         "OmniVerifier-C1：把视觉验证器从「真/假」改成按规则拆解逐项打分",
         "OmniVerifier-C1 针对生成式视觉模型/世界模型的验证环节：传统验证器只输出 True/False 二分类，对「组合式要求」几乎没法定位问题；它把复杂 prompt 或环境规则自动分解成细粒度组件，对每个组件给出连续分值与批评，从而在规则约束的生成任务上提供可定位的反馈。HF Papers 32 赞、同题在 arXiv cs.AI 也有条目。",
         "评测方法", "HuggingFace Papers",
         [("能做什么", "把「这个生成结果合不合规」变成一组可分解、可打分的子判断：规则拆解 → 逐项打分 → 输出连续批评，可直接用作世界模型/视频生成的奖励或筛选信号。"),
          ("解决什么痛点", "二分类验证器只告诉你失败、不告诉你哪条规则失败，对多约束的组合式 prompt 既不可解释也无法指导重采样。"),
          ("值不值得", "如果你要给生成式流水线加自动质检或做 RL 奖励，这类「规则拆解 + 分级打分」是比二分类更可用的信号；但它属于评测层改进，先看你现有 pipeline 里是否真有规则可枚举。")]),
    item("503843",
         "优必选 Thinker-WM：多模态统一表征，单模型拿下三大具身世界模型基准第一",
         "优必选发布 Thinker-WM，用一套多模态统一表征在单个模型里同时支撑六类具身能力，官方称在三个公认的具身世界模型基准评测中全部拿下第一名。",
         "具身模型", "量子位",
         [("能做什么", "把过去要靠多个专用模型拼接的具身能力（感知、预测、动作相关任务）收进一个统一表征模型，宣称在三大基准同时第一。"),
          ("解决什么痛点", "具身系统现在常是「一个模型管感知、一个管预测、一个管动作」，接口与训练目标割裂，跨任务迁移成本高。"),
          ("值不值得", "属于国内具身智能的进展跟踪项，官方口径只有排名没有复现细节，先记名字与「统一表征」这条技术路线，等你真要评具身/机器人仿真时再看论文与开源。")]),
]

AI_ENG = [
    item("2610.17901",
         "FlashMask-3：Hopper 上 mask-aware 分布式 attention，118B MoE 128K 训练吞吐 +7.3–11.0%",
         "FlashMask-3 打的是长上下文训练里「结构化 attention mask（document、prefix-LM、share-question、sliding-window、block-sparse）× 多机 context parallelism」这个瓶颈：在 FlashAttention-3 的 TMA/WGMMA 流水线上做三角色 warp specialization 的 mask-aware Hopper kernel，并把每个 rank 的 mask 定位归约为边界向量上的零通信 clip-shift-max，另加稀疏感知负载均衡（HCC-IPO）与 mask 驱动的通信剪枝。单 H100、12 种 mask、4K–128K 上下文下，TFLOPs 比 FlashMask / FlexAttention / MagiAttention 高 45–141% / 34–71% / 2–44%；CP 度 4–32 时吞吐比 Megatron-Core CP ring 高 1.80–3.71×；118B-A14B MoE 在 128K、128 张 H100 上端到端吞吐提升 7.3–11.0%，attention 前后向快 24.5–44.9%。",
         "训练系统", "HuggingFace Papers",
         [("能做什么", "在 Hopper 上把「带结构化 mask 的长上下文训练」做快：mask 感知的 warp 特化 kernel + 零通信的分布式 mask 定位 + 稀疏感知负载均衡 + 通信与计算重叠，覆盖从单卡到 32 路 CP 的场景。"),
          ("解决什么痛点", "结构化 mask 会把 attention 的算力利用率打下来（旧实现 O(n²) 掩码、只支持 Ampere、且不能跨节点扩展），多机 CP 时 mask 定位又要额外通信，长上下文训练因此卡在 attention 这一段。"),
          ("值不值得", "你在做推理/训练集群规划时，这类工作直接影响「同一批 H100 能跑多长上下文」的账；限制是绑定 Hopper（H100/H200）与 FlashAttention-3 体系，B200 或非 NVIDIA 卡不适用，且是论文阶段、需自己接 Megatron 侧。")]),
    item("503829",
         "模域 ModelSphere 开源：Apache 2.0 的生产级 AI 部署平台，统一纳管昇腾/摩尔/海光等国产卡",
         "范式智能与睿思智联开源「模域 ModelSphere」（Apache 2.0）：把算力管理、模型部署与运行优化收进一个平台，内置自动弹性扩缩容、PD 分离部署、三级 KV 缓存、高可用负载均衡与断流续写，并用 EngineX 推理引擎统一/混合调度昇腾、天数智芯、摩尔线程、海光 DCU 等国产算力。官方称 AutoTune 排期加自适应负载均衡让极限吞吐提升约 285%（约 4 倍），已适配 DeepSeek-V4/V4-Flash、Qwen、Kimi、MiniMax、GLM。定位与 vLLM/SGLang 互补：后者管单机推理效率，它管集群级纳管、缓存感知路由与线上自动调优。",
         "推理平台", "量子位",
         [("能做什么", "把「多厂商加速卡 + 多模型」的部署收敛成一个平台：图形化部署、PD 分离、三级 KV 缓存池、按 QoS 弹性伸缩、断流续写、基于线上数据的自动调优，并统一调度国产异构卡。"),
          ("解决什么痛点", "国产卡生态割裂，换一种卡就要重做底层适配与调优；生产推理还要自己拼负载均衡、KV 缓存复用与扩缩容，团队大量时间花在环境与驱动编译上。"),
          ("值不值得", "你负责集群与推理栈选型、又处在意算力合规的环境，这类 Apache 2.0 的「引擎之上的集群层」值得放进对比清单；但 285% 是厂商自测口径、国产卡适配深度需实测，先小集群验证再谈生产。")],
         oss=True),
    item("uGNQwpOt5GGAKm2XlEZC",
         "Akka 用 65 个开源项目验证「规格驱动移植」：99.3 小时 94.1 亿 token，57/65 有改善",
         "Akka 发布一份规格驱动的 AI 辅助移植实验：先用结构化规格（声明 + 证据 + 类型化行为）描述代码、模型与运行时行为，再让 agent 实现每个项目最多 10% 的功能，之后挑 10 个做完整移植。首轮测试耗时 99.3 小时、消耗 94.1 亿 token，65 个项目中 57 个在代码行数或性能上有提升。成本结构上 Sonnet 平均每项目 61 分钟、Opus 120 分钟但 token 少约 40%，提高 effort 设置并没有持续收益。性能结果分化：应用、框架、库普遍提升，基础设施与工具类中位数反而下降（Dify 提升 143333 倍来自不同工作负载对比，Netflix Metaflow 慢了约 100 倍）。",
         "规格驱动", "InfoQ中国",
         [("能做什么", "把「大规模代码移植」变成可度量流水线：需求发现 → 规格定义 → 移植 → 基准测试 → 优化，配自动化验证（原单元/集成测试）与人工审查串行化、错误处理、PII、幂等性、架构边界。"),
          ("解决什么痛点", "直接让 agent 改代码，跨组件决策写不进上下文，首次实现就跑偏；规格化后模型有稳定契约可依，且能用原有测试证明没破坏行为。"),
          ("值不值得", "你要判断的是「规格先行的成本能否换来可验证的移植」——结论是能，但成本以十亿级 token 计（94.1 亿），且基础设施类项目收益为负；用它评估是否值得把某次大改写成规格驱动流程，而不是当成通用提效手段。")]),
    item("8iKz8xNQvxDfeuxH1QLA",
         "InfoQ 拆 Kiro 的 spec-driven：任务挂测试、PBT 生成上千随机用例、spec 与代码双向同步",
         "InfoQ 长文拆解 Kiro 的 spec-driven development 到底解决什么：它用 requirements.md（EARS 格式的用户故事与验收标准）、design.md（架构、数据流、接口定义）、tasks.md（每项任务挂靠单元/集成测试、加载态、移动端适配、无障碍）三段式替代 vibe coding，关键差别是 spec 与代码库双向同步——写代码可以更新 spec，改 spec 可以刷新任务列表，而不是开工前交一次文档。工程侧最值得看的是基于属性的测试（PBT）：从需求提取普适属性，生成成百上千个随机用例，发现违规后用 shrinking 找最小反例，把「正确性」从主观判断变成可量化对象；另有 Hooks 事件触发器和 Steering 行为规则（IDE 与 CLI 共享同一份配置与订阅额度），以及 Autopilot / Supervised 双模式。",
         "AI 编码", "InfoQ中国",
         [("能做什么", "给 AI 编码加上「可追溯的契约层」：需求→设计→任务三段规格、spec 与代码双向同步、任务级测试挂靠、Hook 自动补齐关联改动、PBT 用随机用例测「实现偏离规范的程度」、checkpointing 让自主执行可回退。"),
          ("解决什么痛点", "vibe coding 的三笔技术债：长会话上下文衰减（约定好的接口被忘掉）、决策不可追溯、从 demo 到生产要人补文档与测试；本质是把工程成本推迟而不是消灭。"),
          ("值不值得", "如果你在团队里推 AI 编码进工程体系，这套「规格 + 属性测试 + 检查点」是目前较完整的一套落地形态；但它绑定 Kiro 产品与订阅，PBT 只对可形式化属性的需求划算，换个 harness 就要自己重建等价物。")]),
]

AI_BIZ = [
    item("barclays-scales-claude",
         "Barclays 扩大用 Claude：目标是年底 Claude Code 覆盖 50% 开发者",
         "Barclays 扩大与 Anthropic 的合作，把 Claude 铺到全行用于软件开发、遗留系统现代化与运营提效；官方给出的量化目标是 Claude Code 到 2026 年底覆盖 50% 的开发者人群，2027 年覆盖多数软件工程师。公告同时强调在高度监管机构里推 AI 需要「有能力的技术 + 有纪律的治理」并重。",
         "金融 AI", "Anthropic News",
         [("能做什么", "大型银行把编码 agent 推到开发者人口的过半规模，用途明确限定在软件开发、遗留系统现代化、运营效率三条线。"),
          ("解决什么痛点", "遗留系统现代化是银行最贵最慢的一段（文档缺失、跨团队），而编码 agent 恰好能读全库、跨文件改；监管要求又让它们必须给出治理口径。"),
          ("值不值得", "你在金融量化行业，这条的参考价值在「覆盖率目标 + 治理并行」的推进方式：先定百分比目标与阶段，再谈工具选型；具体效果数据公告里没给，别拿它当 ROI 证据。")]),
    item("benefit-street-partners",
         "Benefit Street Partners 用 Codex 做贷款估值对比与信贷协议分析",
         "OpenAI 客户故事：Benefit Street Partners 的 Anant Kumar 用 Codex 搭内部工具，做贷款估值对比与信贷协议分析，并把 Codex 用在代码评审和更快的后续跟进上。",
         "金融 AI", "OpenAI News",
         [("能做什么", "把信贷/贷款文本类重复分析工作（协议条款抽取、估值口径对比）交给 codegen 生成的内部小工具，而不是买成套系统。"),
          ("解决什么痛点", "信贷协议分析高度文本密集、口径多，人工逐份比对慢；成品软件又难贴内部口径。"),
          ("值不值得", "属于「一人 + codegen 造内部工具」的典型样本，对你所在行业有代入感；但通稿没有给节省工时或错误率数字，只能当方向参考。")]),
]

AI_OPINION = [
    item("fundamentals-to-engineer-trustworthy-gen-media",
         "Google Cloud 的 SAVE 方法：把研究与创作拆开，别让一个 prompt 同时求真与求好看",
         "Google Cloud Consulting 把「可信生成媒体」的经验归成 SAVE 四步，核心动作是拆开单条 prompt 的职责：研究与创作分离——researcher 先读源文档、抽取核心主张、对齐已批准口径，输出结构化 brief（清单或事实表）；storyteller 只负责风格、节奏、视觉隐喻与语气。理由是创意任务要流动的语言与节奏、事实输出要约束，塞进同一个上下文窗口，模型就会为了让叙事顺畅而编造细节。另一条基础要求是喂给创意模型的文档必须先清洗，否则推测性内容会混进业务事实。",
         "生成媒体", "Google Cloud",
         [("能做什么", "给「企业级生成内容」一套最小可执行纪律：职责拆分（研究 vs 创作）、输入文档清洗、口径对齐后再生成，避免单 prompt 混合任务。"),
          ("解决什么痛点", "企业做生成媒体时最怕的是「看起来很专业但事实是编的」：一个 prompt 既要摘要又要脚本，模型就会用编造细节换叙事流畅。"),
          ("值不值得", "对做内容流水线/营销物料的团队是低成本可落地的规范；方法是工程纪律而非模型能力，不依赖特定厂商，读完即可改自己的 prompt 结构。")]),
]

AI_SAFE = [
    item("cyber-verification-program",
         "Anthropic 把漏洞赏金式特权合并成三档：通过验证的安全团队可用 Opus 5.5 / Mythos 5.1",
         "Anthropic 把此前的 Project Glasswing 与 Cyber Verification Program 合并成一个三档权限的项目：通过验证的安全团队可按自身工作范围申请不同层级的网络能力与「降低拦截」的模型访问，三档都能用到 Claude Opus 5.5、Sonnet 5.5、Mythos 5.1 及后续新模型。背景是通用版模型对攻防类请求设了保守拦截（本来是为限制恶意使用），但同时也误伤了合法安全工作，官方称仍在降低安全编码场景的误判。",
         "AI 安全", "Anthropic News",
         [("能做什么", "给安全团队一条「按验证等级换能力」的通道：分级申请、按范围放行更少的拦截，能用上最强模型做漏洞发现与修复。"),
          ("解决什么痛点", "双用途能力的两难——通用模型必须拦攻防请求，但防守方也需要同等能力；一刀切的结果是安全团队被自家工具挡住。"),
          ("值不值得", "如果你要给公司内部 agent 做「能力分级 + 准入验证」，这是厂商侧的一个参照模型（验证→分档→按范围放行）；但门槛与审核流程官方未公开，且只解决模型侧策略，不替代你自己的出口审计。")]),
    item("itau-generative-ai",
         "Itaú：30 万客户已在用 ia.i，IARA 统一管模型访问、token 成本与负责任 AI 政策",
         "OpenAI 与 Itaú Unibanco 的案例：约 30 万客户已在使用对话入口 ia.i，背后由治理平台 IARA 统一管理模型访问、监控、token 成本与负责任 AI 策略；Itaú 的目标是到 2026 年底让生成式 AI 覆盖全部客户群。这是巴西监管最严的行业之一里，把「AI First」同时推给客户与员工的落地样本。",
         "金融 AI 治理", "OpenAI News",
         [("能做什么", "把面向客户与员工的生成式 AI 收进一个治理平面：统一模型访问控制、用量与成本监控、责任 AI 策略执行，前端以 ia.i 这一个对话入口承接全产品线。"),
          ("解决什么痛点", "银行最怕「每个业务线各自接模型」导致口径、成本与合规失控；单入口 + 单一治理平台是把成本与风险都收口的最省事结构。"),
          ("值不值得", "你在金融行业做 AI 落地，这套「入口统一 + 治理平台管 token 与策略」的形态最贴近监管现实；注意它是客户案例叙事，缺模型路由与审计细节，可作为架构参照而非技术方案。")]),
]

INFRA_K8SAI = [
    item("kagent/releases/tag/v1.0.0-alpha14",
         "kagent v1.0.0-alpha14：用 Substrate image volumes 挂 OCI 形式的 skill",
         "kagent v1.0.0-alpha14（10 月 16 日）把 agent 的「skill」做成可挂载产物：通过 Substrate image volumes 直接挂载 OCI 镜像里打包的 skill；运行时挂起（runtime suspension）改为基于 DATA 快照实现，而不是重建沙箱；A2A 鉴权细化到具体方法（UpstreamAuth 会告知当前授权的是哪个 A2A 方法）；可禁用内建 bash 工具；CLI 支持由嵌入二进制完成鉴权并扩展 db tracks；会话分享 token 改为只读，过期/缺失会话返回 not found。",
         "K8s Agent", "GitHub Releases",
         [("能做什么", "把 agent 的 skill 变成可分发的 OCI 构件（挂载即用）、把 agent 会话的挂起/恢复落成数据快照、把 A2A 方法级鉴权与只读分享 token 补齐——都是「agent 跑在 K8s 上要上生产」缺的那几块。"),
          ("解决什么痛点", "skill 过去靠构建期烤进镜像，改一次要重建；agent 会话空闲时的资源回收若无快照只能重建上下文；A2A 服务之间的调用授权粒度太粗。"),
          ("值不值得", "你在做多用户 agent 平台，「skill 作为 OCI 构件 + 会话快照挂起」这两条正好对资源浪费与上下文隔离两个痛点；但 alpha 版本、breaking 频繁，先跟架构不要跟生产。")],
         oss=True),
    item("hami-gpu-sharing",
         "HAMi 在 KubeCon China：主张「先调度、再切分」，动态 MIG 跟着调度走",
         "HAMi 首次以 CNCF Incubating 项目身份在 KubeCon China 2026 拿到两个 keynote 与一场生产实践分享：核心主张是「先调度、再切分」——由调度器决定负载落哪张卡，然后按需修改该卡的 MIG 布局，而不是预先静态切卡去赌请求形状。配套演示是 vLLM 跑在 llm-d 栈上做 PD 分离部署、由 HAMi 负责跨异构加速卡的共享与调度。背景是默认 K8s 把整张 GPU 给一个 Pod，对推理、notebook、CI 这类只需几 GB 显存的负载浪费严重，相关 upstream 讨论（issue #52757）已挂多年。",
         "GPU 共享", "kubezilla",
         [("能做什么", "把 GPU 从「整卡独占」变成可切分、可跨厂商调度的资源：按显存/算力份额分配、动态 MIG 布局随调度结果调整、在 PD 分离的推理栈里统一调度异构加速卡。"),
          ("解决什么痛点", "推理与小模型服务只能拿到整卡，显存与算力大量闲置；静态 MIG 又要提前猜请求形状，猜错就浪费。"),
          ("值不值得", "你在做 GPU 调度与显存利用率的方案，HAMi 是国内落地最多的选项之一（已进 CNCF Incubating）；但要评估它与你选定的 device plugin、DRA 路线是否冲突，动态 MIG 只对支持 MIG 的卡有效。")]),
]

INFRA_CORE = [
    item("karpenter/releases/tag/v1.15.0",
         "Karpenter v1.15.0：DRA 支持候选设备按优先级回退，新增 VPA 预测控制器",
         "Karpenter v1.15.0（10 月 10 日）在供给侧补了几块关键能力：支持 DRA 的 prioritized alternatives（同一个 claim 有多个候选设备时按优先级回退）；新增 VPA 预测控制器与对应 store；默认开启 Pod topology spread 感知；供给时考虑实例类型的卷数量上限；disruption 指标补上 consolidation_policy 与 termination_mode 标签，并新增 karpenter_pods_disrupted_total 计数。",
         "自动扩缩", "GitHub Releases",
         [("能做什么", "让节点供给更贴调度约束：DRA 候选设备优先级回退、按拓扑打散、按实例卷上限过滤机型；同时把 VPA 预测与 disruption 指标补齐，扩容决策有据可查。"),
          ("解决什么痛点", "GPU/加速器场景里 DRA 一旦首选设备不可用就整 Pod pending；拓扑打散过去要自己配；卷挂满导致实例不可用要事后才发现。"),
          ("值不值得", "你在做集群伸缩与 GPU 机型选择，DRA 优先级回退 + 卷上限校验这两条能直接减少 pending 与供给失败；升级成本中等，注意 v1.14.2 同日发的补丁也要一起排期。")],
         oss=True),
    item("cluster-api/releases/tag/v1.14.3",
         "Cluster API v1.14.3：管理集群支持到 K8s v1.37，修 KCP 代理竞态",
         "Cluster API v1.14.3 补丁版（10 月 7 日）：管理集群支持 K8s v1.33–v1.37、工作负载集群 v1.31–v1.37；合并 16 个 commit、修 6 个 bug，其中包括 KCP proxy DialContext 的竞态、KCP 删除时 etcd 成员与被删 Machine 的匹配、无 ClusterClass 的 Cluster 也要打 cluster-name 标签、Machine/MachineSet 解析 owner reference 时的 not-found 优雅处理；另把 grpc 升到 1.83.2 以修安全公告，cert-manager 升到 v1.21.2。",
         "集群生命周期", "GitHub Releases",
         [("能做什么", "声明式管理集群本身（控制面/节点/升级）：这个补丁版把管理集群的 K8s 版本窗口抬到 v1.37，并修掉 KCP 代理与 etcd 成员匹配的竞态。"),
          ("解决什么痛点", "KCP 代理竞态与 etcd 成员错配会在控制面扩缩/升级时造成卡住或误删；grpc 旧版本带安全公告。"),
          ("值不值得", "如果你用 Cluster API 管多集群（含本地 multipass 试验环境），这类补丁版是低风险升级；真正要花时间的是版本窗口规划，不是这个 patch。")],
         oss=True),
]

INFRA_COMM = [
    item("argo-cd/releases/tag/v3.5.5",
         "Argo CD v3.5.5：修 reposerver 陈旧 manifest 与 goroutine 泄漏",
         "Argo CD v3.5.5 补丁版（10 月 12 日）：修 reposerver 在 CMP 失败后残留陈旧 manifest 与 goroutine 泄漏、hydrator 在 cannot lock ref 时重试 notes push、events.k8s.io 事件的计数与时间戳补全、UI 只在 Helm 场景显示 enableOCI，并把 kustomize 校验和 helper 改用 curl 以便 Renovate 刷新。镜像走 cosign 签名并提供 SLSA Level 3 provenance。",
         "GitOps", "GitHub Releases",
         [("能做什么", "持续交付控制面：这次是稳定性补丁，重点在 reposerver 不再泄漏 goroutine、不再渲染陈旧 manifest。"),
          ("解决什么痛点", "CMP 插件失败后残留的旧 manifest 会造成「配置没生效但 Argo 说已同步」，goroutine 泄漏则让 reposerver 慢慢吃满内存。"),
          ("值不值得", "你在跑 GitOps 就该跟这条补丁线（尤其用 CMP 插件时）；升级是 patch 级，风险低，注意同时核对签名与 provenance 流程。")],
         oss=True),
    item("opentelemetry-collector/releases/tag/v0.163.0",
         "OTel Collector v0.163.0：修 block_on_overflow 死锁，抓取成本从 O(n²) 降到 O(n)",
         "OpenTelemetry Collector v0.163.0：mdatagen 从 metadata.yaml 的 opt-in sending_queue 字段生成 exporter 队列/批处理默认值（batching 迁移 RFC 第一阶段，未声明者不受影响）；recordDataPoint 的 O(n) 扫描换成 O(1) 哈希查找，消除多点落在同一 resource 时每次抓取的 O(n²) 成本；修 exporterhelper 在 block_on_overflow 下取消阻塞 offer 时的死锁；profiles 批次超限时只丢超大 profile 而不是其后排队的所有 profile；OTLP 收发端支持 Profiles 开发版元数据。",
         "可观测性", "GitHub Releases",
         [("能做什么", "遥测管道底座：抓取热点改成哈希查找、队列死锁修掉、profiles 支持元数据版本，并为 exporter 队列/批处理默认值引入 opt-in 生成机制。"),
          ("解决什么痛点", "高基数指标（多点同 resource）下 Collector 自身 CPU 会被 O(n²) 吃掉；block_on_overflow 下取消 offer 会让 exporter 队列整体卡死。"),
          ("值不值得", "你在设计集群可观测栈，Collector 是必经组件；如果你开了 block_on_overflow 或跑 profiles，这个补丁值得尽快上，其余是渐进迁移。")],
         oss=True),
]

INFRA_CLOUD = [
    item("azure.microsoft.com/updates?id=576556",
         "Azure Databricks Private network gateway 公预览：serverless 经单一网关访问 VNet",
         "Azure Databricks 的 Private network gateway 进入公预览：让 serverless 计算通过一个托管网关访问 VNet 及其传递连接网络中的资源，不必为 serverless 单独做网络对等或私有端点编排。",
         "云网络", "Azure Updates",
         [("能做什么", "把 serverless 计算接入私有网络这件事收敛成「一个托管网关」：VNet 内与传递连接网络的资源都从这一个入口访问。"),
          ("解决什么痛点", "serverless 计算不在你的 VNet 里，过去要么给每类资源配私有端点、要么做网络对等，规则一多就难维护。"),
          ("值不值得", "如果你在多云上评估「托管 Spark/数据平台如何进私网」，这是 Azure 侧的一个简化路径；仅预览、绑定 Azure Databricks serverless，跨云不可移植。")]),
    item("temporal-serverless-workers-on-cloud-run",
         "Cloud Run 上跑 Temporal worker：用 worker pool 按需求预扩容",
         "Google Cloud 发文讲 Temporal Serverless Workers on Cloud Run 的落地：Temporal worker 是「轮询任务」而不是「响应请求」，与请求驱动的 serverless 模型天然错配，所以过去只能常驻 K8s/VM 养一批 worker 持续付费；新方案用 Cloud Run worker pools 按需求提前扩容。",
         "Serverless", "Google Cloud",
         [("能做什么", "把 Temporal 这类编排系统的 worker 迁到 serverless 执行面：worker pool 按预测需求扩容，空闲时不必常驻。"),
          ("解决什么痛点", "轮询型 worker 与 request-driven 平台模型不匹配，导致编排层只能跑在 K8s/VM 上，长期为闲置容量付费。"),
          ("值不值得", "你在做 K8s 集群与 serverless 的边界划分，这类「轮询型负载上 serverless」的官方支持会改变编排组件的部署位置选择；先看它的冷启动与轮询开销，别直接搬生产。")]),
]

brief = {
    "brand": "AI & 基础设施早报",
    "date_label": "2026 年 10 月 18 日 · 星期日",
    "issue": 28,
    "kicker": "DAILY",
    "hint": "👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
    "lead": "今天两条线各进一步：K8s 侧的 agent 基础设施开始收拾「沙箱生命周期」的细节——Agent Sandbox v1.0.7 把 warm pool 与 Kueue 调度门打通，预热池不再把等准入的成员当卡死回收；模型侧 Gemini 4 Argon 上线，最硬的证据不是榜单而是 20.5 万行 ADK 上无人值守 11 小时、改 32 个文件、跑完 16892 项测试。方法论上，Google Cloud 用 11 条 prompt 的实测说明 agent 评测为什么不能只看最终回复：把「做了但没说」正确行为判成失败。",
    "highlights": [H1, H2],
    "sections": [
        {"label": "🤖 AI 板块", "categories": [
            {"emoji": "🧩", "title": "Agent & Skill", "en": "Agent & Skill", "items": AI_AGENT},
            {"emoji": "🧠", "title": "模型与研究", "en": "Models & Research", "items": AI_MODEL},
            {"emoji": "🛠️", "title": "AI 工程落地", "en": "AI Engineering", "items": AI_ENG},
            {"emoji": "📊", "title": "产品与商业", "en": "Business", "items": AI_BIZ},
            {"emoji": "💡", "title": "观点与好文", "en": "Opinion", "items": AI_OPINION},
            {"emoji": "🛡️", "title": "安全与治理", "en": "Safety & Governance", "items": AI_SAFE},
        ]},
        {"label": "☸️ 基础设施板块", "categories": [
            {"emoji": "🤖☸️", "title": "K8s × AI", "en": "K8s × AI", "items": INFRA_K8SAI},
            {"emoji": "☸️", "title": "K8s 核心技术", "en": "K8s Core", "items": INFRA_CORE},
            {"emoji": "📦", "title": "社区与项目", "en": "Community & Projects", "items": INFRA_COMM},
            {"emoji": "☁️", "title": "公有云动态", "en": "Public Cloud", "items": INFRA_CLOUD},
        ]},
    ],
    "flash": [
        {"title": "vLLM v0.32.0 发布（10-17）：发布说明仅一条 Rust frontend 的 macOS 构建修复，无特性条目。", "url": U("vllm/releases/tag/v0.32.0")},
        {"title": "SGLang v0.5.22 发布（10-15），release 正文为空，只看 tag。", "url": U("sglang/releases/tag/v0.5.22")},
        {"title": "NVIDIA GPU Operator 26.7.2（10-14），release 正文只指向 26.7 版发行说明。", "url": U("gpu-operator/releases/tag/v26.7.2")},
        {"title": "llm-d 仓库打出 v1.0.0-rc.1 / v1.0 候选标签（10-14），release 说明仅一行，细节未公开。", "url": U("llm-d/releases/tag/v1.0.0-rc.1")},
        {"title": "Karpenter v1.14.2 补丁（10-16）：NodeRepair 控制器入队条件与 capacity buffer 的 scalableRef 监听修复。", "url": U("karpenter/releases/tag/v1.14.2")},
        {"title": "anomalyco/opencode 仍在 Trending（单日 +438 star）：开源编码 agent，与你现用的 opencode 同一项目。", "url": U("github.com/anomalyco/opencode")},
        {"title": "网易「叭哥说」上线 10 万元「真需求」征集，AI 原生语音 Agent 用联创计划换场景反馈。", "url": U("qbitai.com/2026/10/503861")},
        {"title": "Simon Willison 的 LaTeX 渲染小工具：文档数据存在 URL #fragment 里，可 bookmark 分享。", "url": U("simonwillison.net/2026/Oct/15/latex/")},
    ],
    "footer": "由 Hermes 自动汇编 · 每日 09:00 更新",
}

json.dump(brief, open("briefing.json", "w"), ensure_ascii=False, indent=1)

# sanity checks
n_items = 0
for sec in brief["sections"]:
    for cat in sec["categories"]:
        for it in cat["items"]:
            assert it["title"] and it["summary"] and it["detail"], it["url"]
            assert it["url"] in URLS, it["url"]
            assert len(it["detail"]) == 3, it["title"]
            n_items += 1
assert n_items == 23, n_items
print(f"briefing.json written: {len(brief['highlights'])} highlights + {n_items} items + {len(brief['flash'])} flash")
