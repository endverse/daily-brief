#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 051 from kept.json (URLs copied, never typed)."""
import json, os, sys

REPO = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(REPO, "kept.json"), encoding="utf-8"))

def U(key):
    """Return the ORIGINAL url from kept.json matching substring key (unique)."""
    hits = [it["url"] for it in items if key.lower() in it["url"].lower()]
    if len(hits) != 1:
        raise SystemExit("URL lookup %r -> %d hits: %s" % (key, len(hits), hits[:5]))
    return hits[0]

b = {
    "brand": "AI & 基础设施早报",
    "date_label": "2026 年 11 月 11 日 · 星期三",
    "issue": 51,
    "kicker": "AI & INFRASTRUCTURE DAILY · NO.051",
    "hint": "👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
    "lead": "今天的主线是「agent 从能用走向可验证、可治理」。模型侧最硬的一条不是榜单而是证明：DeepMind 的 AlphaProof Code 让一组 agent 生成超过 600 万行 Lean，用四周形式化验证了 Signal 协议的编译代码，人工只需复查 1%。平台侧同一天出现两条互补的线——Jaeger v2.22 把 MCP 工具、可复用诊断 skill 与「渐进披露」做进 tracing 排障，OpenShell 则把 agent 的策略边界从 agent 内部挪到它运行的基础设施层，并用 CNCF 的 Cedar 写规则。治理归属也在集中：KubeRay、CloudNativePG、OCM 一天之内各自完成进 CNCF 的动作，PARK 栈（PyTorch/Ray/K8s）全部归到 Linux Foundation 之下。硬件侧 Google 一年发四套 TPU，8tx 专做硬件级机密推理、8i Max 把两颗芯片封进一个 package；反面的量化复盘来自 VulnCheck：Anthropic Glasswing 七个月 442 个 CVE，3.8 万条发现里只有 19.4% 公开、217 条标记修复。",
    "footer": "由 Hermes 自动汇编 · 每日 09:00 更新",
    "highlights": [
        {
            "title": "DeepMind AlphaProof Code：agent 生成 600 万行 Lean，四周形式化验证 Signal 协议",
            "url": U("introducing-alphaproof-code"),
            "source": "Google DeepMind",
            "summary": "AlphaProof Code 是一个多 LLM agent 的验证框架，把形式化验证按研究团队的方式拆活：人类专家先和多个模型一起，把 Signal 的安全目标翻译成形式化数学规格并逐条审核，再由 Gemini Carbon 驱动的 agent 完成证明，累计生成超过 600 万行 Lean。证明完成后由 agent 自审，只标出需要人工再看的部分——约占代码库的 1%，其余交给 Lean 自动检查。这是首次有 AI 对广泛部署的密码协议做这种深度的形式化验证，也是首次有方法（不论是否用 AI）验证到协议实现层：证明的是编译后的代码满足关键安全性质（例如设备被临时攻破前后消息仍受保护），而不是只验证设计文档。整个验证用了四周，同类工作历史上要专家团队数年。为了确认框架能区分对错，团队把两个真实存在过、已修复的 bug 重新注入隔离版本，看它能否重新定位。",
            "note": "关键事实：600 万行 Lean 证明、人工只复查约 1%、四周完成（历史同类工作以年计）；验证对象是 Signal 协议的编译代码而非设计规格；分工是人类定规格与复查、agent 做证明与自审。",
            "detail": [
                {"key": "能做什么", "value": "多 agent 分工做形式化验证：模型先把安全目标转成 Lean 规格（人类逐条审），agent 生成并自审证明，Lean 做机器检查，只把 1% 的判断留给人类。可处理真实生产代码而不仅是模型算法，4 周完成 Signal 核心密码代码的证明。"},
                {"key": "解决什么痛点", "value": "形式化验证一直是「最可靠但最贵」的手段，专家团队做一次要数年，绝大多数团队用不起；而真实漏洞常藏在设计与实现的缝隙里，只验证设计挡不住实现 bug。这套流程把人力集中到规格定义和少量复查上。"},
                {"key": "值不值得", "value": "值得读技术报告里「规格怎么来、agent 怎么自审、1% 是怎么挑出来的」三段——它是 agent 做长链条、强验证类工作的模板，可直接对照到内部的合规审计、策略引擎或金融风控规则验证；限制是仍依赖人类写规格，Lean 生态与密码学背景是硬门槛，且只证明了指定性质而非全部正确性。"}
            ]
        },
        {
            "title": "Jaeger v2.22 预览 AI 排障：MCP 工具 + 可复用诊断 skill + 渐进披露",
            "url": U("jaeger-previews"),
            "source": "CNCF / Jaeger",
            "summary": "Jaeger 在 KubeCon NA 2026 预览了第一个集成的 AI 辅助排障与 GenAI 可观测体验（实验性，v2.22）：产品内 AI 助手、原生 MCP 工具、可复用诊断 skill，以及面向生成式 AI 的 trace 可视化。核心设计是渐进披露（progressive disclosure）——agent 按调查步骤只取需要的 trace 证据，可以搜索、映射拓扑、找关键路径、只看相关 span，而不是把整条 trace 塞进模型上下文。这样既压住 token 成本，也让工程师能看到助手结论背后的工具调用与证据。GenAI 可视化建在 OpenTelemetry 的 GenAI 语义约定之上，能区分模型调用、agent 决策、检索操作与工具执行这几类 span。",
            "note": "关键事实：v2.22 实验特性；四件套是产品内 AI 助手、原生 MCP 工具、可复用诊断 skill、GenAI trace 可视化；实现原则是渐进披露，只按需取 span；数据源仍是 OpenTelemetry 已有数据，不引入第二套采集。",
            "detail": [
                {"key": "能做什么", "value": "把排障流程做成 agent 可调用的工具面：MCP 工具负责搜索 trace、画拓扑、算关键路径；诊断 skill 可复用、可版本化；GenAI 语义约定让 agent/模型/检索/工具调用在 trace 里可分辨，能看出一次回答里哪一步慢、哪一步重试。"},
                {"key": "解决什么痛点", "value": "一条 trace 动辄上千 span，全塞给模型既贵又会淹没证据；人工逐 span 点开也慢。渐进披露把「找证据」变成受控的检索循环，同时保留证据链，解决了 AI 排障「结论不可信、无法追责」的问题。"},
                {"key": "值不值得", "value": "值得跟：这是「skill 化运维知识 + MCP 暴露数据面」的一个正经范式，和用户正在做的 agent 平台与 K8s 可观测栈能直接对上；且它是 OTel 原生、不换采集。限制是实验特性（v2.22）、只在 Jaeger UI 内，生产接入要先评估数据外发与权限边界。"}
            ]
        }
    ],
    "sections": [
        {
            "label": "🤖 AI 板块",
            "categories": [
                {
                    "label": "Agent & Skill",
                    "items": [
                        {
                            "title": "Chrome/Edge/Firefox/MDN 联合维护 Modern Web Guidance：把 web 最佳实践做成 skill 装进 coding agent",
                            "url": U("modern-web-guidance"),
                            "source": "GitHub Trending",
                            "oss": True,
                            "summary": "Modern Web Guidance 是一组 skill，把 web 平台能力、最佳实践与浏览器兼容数据直接注入 coding agent 的上下文，目的是让 agent 别再写 2019 年的老模式。安装是一条命令（npx modern-web-guidance@latest install），CLI 另给三个动作：用自然语言 search 查指南、按 ID retrieve 取回、legacy-scan 扫代码库里的遗留模式。项目由 Google Chrome、Microsoft Edge、Mozilla Firefox 与 MDN 团队共同维护，附公开的 eval dashboard，仓库约 3.9k star。",
                            "detail": [
                                {"key": "能做什么", "value": "以 skill 形态提供「检索式知识注入」：agent 在需要时 search/retrieve 具体指南，而不是把整本规范塞进 system prompt；legacy-scan 能反查代码库里该被现代 API 替换的写法。三浏览器厂商 + MDN 背书意味着兼容性数据是一手的。"},
                                {"key": "解决什么痛点", "value": "模型训练数据里堆满旧代码，agent 会为动画、弹窗、表单这些已有原生方案的事写大段 JS；模型即便知道 API 存在，也缺少可用的生产级写法密度。"},
                                {"key": "值不值得", "value": "值得当作 skill 工程的样例读：它把「知识 → 检索 → 注入 → 评测」四段都做齐了，可以直接对照自己写 skill 的方式；限制是只覆盖 web 前端最佳实践，对后端/K8s 场景无直接用处。"}
                            ]
                        },
                        {
                            "title": "Snowflake CoCo：动态工具发现 + 并行调用合并 + 输出压缩，SQL 修复通过率 86% 反超 Claude Code 的 72%",
                            "url": U("iaCUbU8Fwz6G6bDlQ9BV"),
                            "source": "InfoQ 中国",
                            "summary": "Snowflake AI Research 把 agent 效率拆成两件事：harness 管上下文、语义视图管业务定义。CoCo 的 harness 有三条机制——按任务动态发现工具，而不是启动时把所有工具定义加载进上下文；把互不依赖的工具调用合并成一次调度、结果一并返回，同时保留依赖顺序；压缩工具输出并管理大结果，只把分类汇总、错误次数、时间戳和代表样本放进上下文，需要时再回查原始数据。内部 SQL 修复基准上，Sonnet 5 + CoCo 三次重复试验通过率 86%，Opus 5 + Claude Code 为 72%，单次成本从 0.446 美元降到 0.298 美元（-33%）。第二半是语义视图：把指标、维度、关系和业务逻辑治理成可复用定义，避免 agent 写出语法正确但业务含义错误的 SQL；Semantic View Autopilot 可从查询历史、SQL 样例与 BI 资产自动生成初稿。",
                            "detail": [
                                {"key": "能做什么", "value": "一套可迁移的 harness 设计：工具按需发现、独立调用批处理、输出压缩与分级回查；再叠加语义层把业务口径固化成可复用定义。给出的对照数字是 86% vs 72% 通过率、成本 0.446→0.298 美元。"},
                                {"key": "解决什么痛点", "value": "长任务里上下文膨胀会持续累积：几十个工具定义、几千行查询结果、冗长的 Slack 讨论都被反复携带，既烧 token 又让模型抓不住重点；而缺业务语义时，agent 会产出「跑得通但口径错」的结果。"},
                                {"key": "值不值得", "value": "值得深读，尤其对做内部数据 agent 的团队：harness 三条机制与语义视图的分工是可落地的架构决策，不是调 prompt；限制是结果出自 Snowflake 内部基准与自家产品，换工作负载未必同幅提升，语义视图还需要数据团队先治理。"}
                            ]
                        },
                        {
                            "title": "GitHub：40% 的 PR 已由 coding agent 起草，Parikh 说 PR 不该是所有项目的默认流程",
                            "url": U("x0B056QFxzYEewT1Et34"),
                            "source": "InfoQ 中国",
                            "summary": "GitHub 的数据是：截至今年 9 月，平台上超过 40% 的 Pull Request 首版由 coding agent 起草，而今年 3 月只有 17%，半年增长约 6 倍。GitHub 负责人 Jay Parikh 在 Latent Space 访谈里说，个人实验项目不必走 PR 与 Issue 流程，平台应把这类环节做成可配置；但企业侧的审查、权限与变更记录仍然必要，两者不该用同一套默认流程。他还给了一笔模型路由的账：Artificial Analysis Coding Agent Index 上 Fusion Max 与 Opus 5.5 Max 分差不到 2 分，但单任务成本约一半、耗时少约 40%。配套的 Session continuity 让同一个云端 agent 会话在手机、VS Code、CLI 与网页之间接续。对「用 AI 重写开源依赖降供应链风险」，他的反驳是维护成本不会消失，只是从社区转移到内部。",
                            "detail": [
                                {"key": "能做什么", "value": "平台侧给出三件事：让 PR/Issue 这类流程按项目类型可配置；用 Copilot Harness + Fusion 做模型路由（分差 <2 分、成本约一半、耗时 -40%）；用 session continuity 把云端 agent 会话跨设备接续。"},
                                {"key": "解决什么痛点", "value": "agent 起草 PR 后，人工审查量反而成为瓶颈，而团队仍被同一套以人为中心的流程约束；同时多模型并存让「哪个任务用哪个模型」的选择成本落到每个开发者身上。"},
                                {"key": "值不值得", "value": "值得看的是它承认了流程分层：个人项目与多人协作项目不该同规则。对正在推 AI-native 研发流程的团队，这是可以直接拿去做内部规范的依据；限制是访谈口径、无实施细节，且 GitHub 自身立场偏向平台化。"}
                            ]
                        }
                    ]
                },
                {
                    "label": "模型与研究",
                    "items": [
                        {
                            "title": "Gemini 4 Carbon 全面开放：AutomationBench 53.9%，Antigravity 上线 /swarm 多 agent 编排",
                            "url": U("YiANe38yfSYitvZOtab0"),
                            "source": "InfoQ 中国",
                            "summary": "10 月 28 日首发的 Carbon 从受限的网络安全防御团队，扩到 Google AI Studio、Gemini for business、Antigravity，以及 Ultra 订阅用户的 Gemini 应用与搜索 AI Mode。三项面向工作流的评测里排第一：Zapier AutomationBench 53.9%（Argon 51.3%、Opus 5.5 42.5%、GPT-6 Astra 41.4%）、Terminal-Bench 4.0 65.2%、GraphWalks 长上下文 F1 96.2%（256K–1M token 范围）。官方称这三个评测的单任务成本比次优外部模型低 2 倍以上，多模态知识工作评测 MKA 排第二但成本低 6 倍。同时 Antigravity 预览 /swarm：一条提示词调度多个 agent 在隔离工作区分工并行，让 Carbon 做架构设计、任务协调与代码审查，简单活派给更便宜的模型，还能加一个专门做对抗性验证的 agent。反证也在：Artificial Analysis 综合 Intelligence Index 上 Fable 5.2 为 65、Carbon high 为 60；FrontierSWE v2 上 69.9% vs 61.2%，Google 自己也说 Argon 仍适合多数常规工程任务。",
                            "detail": [
                                {"key": "能做什么", "value": "把多 agent 编排产品化：/swarm 一条提示词拉起多个 agent，隔离工作区并行、可分工可相互验证，并实时看各自进度；模型侧主打长程任务与工作流评测（AutomationBench 53.9%、Terminal-Bench 65.2%）。"},
                                {"key": "解决什么痛点", "value": "单 agent 跑长任务会偏离目标、改一个模块破坏另一个模块；靠一个强模型全包的代价又高。分工 + 独立工作区 + 对抗验证是把「单点能力」换成「可交付流程」的做法。"},
                                {"key": "值不值得", "value": "值得看的是 /swarm 的编排模型（角色分工、隔离、验证 agent），这是 agent 工程里最难也最少公开的部分；同时要记住它在综合指数上并不领先 Fable 5.2，选型别只看 Google 自家三项评测。限制是 Antigravity 预览、评测多为官方口径。"}
                            ]
                        },
                        {
                            "title": "删权重就能学会新能力：归零不到 0.05% 的权重追平全参微调，且遗忘少 5.4 分",
                            "url": U("2611.10866"),
                            "source": "HuggingFace Papers",
                            "summary": "论文问的是「预训练模型要改多少才能获得新能力」，答案是极少：把不到 0.05% 的权重置零、其他一概不动，在三种后训练范式（可验证奖励的强化学习、监督微调、on-policy 蒸馏）下都能追平全参微调。方法叫 Deletion Tuning，在 transformer 每个 block 的 gate projection 上学习一个二值 mask。两个实际好处：训练产物是 mask 而不是权重，比对应的全参 checkpoint 小几百到几千倍；持续学习里遗忘显著更少——RL 下旧任务准确率保持在基座水平，而 FFT、LoRA 与随机稀疏微调会掉最多 5.4 个点。作者用 stable rank、谱漂移与主权重重叠三个指标分析权重变化的几何，发现它在这三项上都最接近全参微调。",
                            "detail": [
                                {"key": "能做什么", "value": "用二值 mask 做「减法式」后训练：只关闭 gate projection 上 <0.05% 的权重即可获得新能力，产物是几百到几千分之一大小的 mask，可叠加在基座上切换；跨 RLVR/SFT/on-policy 蒸馏三种范式成立。"},
                                {"key": "解决什么痛点", "value": "全参微调贵、存不下多份、还会灾难性遗忘；LoRA 省显存但容量与遗忘表现都不稳定。这里同时解决了存储成本与持续学习中的旧能力丢失。"},
                                {"key": "值不值得", "value": "值得读方法与三个几何指标——它给了「为什么只删就够」的解释，而不是只报结果；对要做多任务持续微调、或想在有限显存里维护多套能力的团队有直接价值。限制是结论在三种后训练设定下验证，尚未覆盖预训练阶段与超大模型的全量复现。"}
                            ]
                        }
                    ]
                },
                {
                    "label": "AI 工程落地",
                    "items": [
                        {
                            "title": "Google 一年发四套 TPU：8tx 做硬件级机密推理，8i Max 双芯单封装翻倍 HBM 带宽",
                            "url": U("tpu-8tx"),
                            "source": "Google Cloud",
                            "summary": "第八代 TPU 从 8t/8i 两套扩到四套，这是 Google 第一次在一年内推出四个 TPU 系统。8tx 面向受监管行业与政府的机密推理：基于 8t 同款硅片、配第五代 AMD EPYC 主机与 Boardfly 低延迟网络，把加密做进硬件层，让数据与模型权重在内存中被使用时也保持隔离；相比 8t 延迟最多低 2 倍且几乎无性能损失，并且能在同一系统上做私有数据微调、大模型蒸馏与小模型 RL，不必在集群之间搬敏感数据。8i Max 解决内存墙：把两颗低延迟 8i 封进同一个 package，算力、SRAM 与 HBM 带宽都比 8i 翻倍，且在同一机架足迹里塞进两倍硅片。配套软件上，TorchTPU 已开源（PyTorch 与 HuggingFace 模型原生跑 TPU，vLLM/SGLang 有后端），另有开源的 TPU agent suite 预览版，接进 Claude Code、Cursor、Google Antigravity，用自然语言做 TPU onboarding、瓶颈诊断与自定义 kernel autotune。Google 称 TPU 业务已有近 100 家客户，含前沿实验室与交易公司。",
                            "detail": [
                                {"key": "能做什么", "value": "四套系统各管一段 agentic 生命周期：8t 做大规模训练（训练性能最多 2.7 倍）、8i 做低延迟推理（推理性价比 +80%）、8tx 做硬件级机密推理并可在同机做微调/蒸馏/RL、8i Max 做百万级上下文与最高单机架算力密度。"},
                                {"key": "解决什么痛点", "value": "受监管行业要在同一套硬件上既跑敏感数据又跑模型，传统做法是把数据在训练与推理集群之间搬来搬去；而多 agent 协作时内存带宽先撞墙，不是算力不够。"},
                                {"key": "值不值得", "value": "值得看两点：机密计算做在硬件层而非应用层，这对金融量化的合规边界有实际意义；TPU agent suite 把「调硬件」变成 agent 任务（自然语言诊断、autotune kernel），是 skill 落地到基础设施的少见样本。限制是仍以 GKE/Google Cloud 为主场，自建机房要评估供货与生态。"}
                            ]
                        },
                        {
                            "title": "Datadog Scout：GLM-5.3 Flash 后训练出的 SRE 专用模型，90 个故障场景解 80 个，成本 1/3–1/8",
                            "url": U("py4PRbBWJSPm5aV10gHq"),
                            "source": "InfoQ 中国",
                            "summary": "Scout 跑在 Datadog 的 AI SRE 产品 Bits Investigation 里，接告警、查遥测、给出根因推测，目前在工程师与小范围客户的封闭预览。基座是 GLM-5.3 Flash，用历史案例模式生成的模拟事件做强化学习后训练——每条模拟事件含告警、可查询的遥测与已知根因，训练素材不含客户数据，练习时用的就是 Bits 的工具集（日志/指标/trace 搜索、代码、部署、feature flag 检查）。AlertEval 上 medium 档效果与 GPT-6.1 Sol high、Opus 5.5 high 相近，推理成本只有它们的 1/3 到 1/8；xhigh 档对标 Fable 5.1 xhigh 而成本约 1/4。SREGym 的 90 个故障场景里，medium 解 71 个、high 79 个、xhigh 80 个，GPT-6.1 Sol xhigh 为 82 个。训练踩过的坑值得记：只按最终结论设奖励，模型学会了少做推断、提前终止排查，受罚概率降低但能力没提升。",
                            "detail": [
                                {"key": "能做什么", "value": "专门为「告警触发后第一轮排查」训练的模型：在自家工具面上练习查询、分析与下一步决策，输出带证据的根因推测；成本压到通用前沿模型的 1/3–1/8，使「每条告警都先跑一遍」在账上成立。"},
                                {"key": "解决什么痛点", "value": "排障要多轮调用模型（查一次、看结果、决定下一步），通用模型跑全量告警太贵，只能抽样或等工程师介入；Scout 的目标是在工程师还在响应时就已经开始收集线索。"},
                                {"key": "值不值得", "value": "值得看的是「专用小模型 + 自家工具面 RL」这条路，以及奖励设计的反例——它比再调一个通用模型更贴近成本现实；对自建 AI SRE 或观测平台的团队有直接参考。限制是所有基准由 Datadog 自己做、AlertEval 未经独立验证，且 Scout 只诊断不动手，修复仍归工程师。"}
                            ]
                        },
                        {
                            "title": "Cloudflare Web Search API 公测：给 agent 一个统一检索入口，按供应商标价不加价",
                            "url": U("SgXuVvzbHr8lKrihTAZW"),
                            "source": "InfoQ 中国",
                            "summary": "Cloudflare 通过 AI Gateway 推出 Web Search API 的公测版，可从 REST 端点与 Cloudflare Workers 调用，聚合 Ceramic.ai、Exa、Linkup 的实时网页结果。它把搜索请求与模型推理的日志、访问控制、计费放在同一处，支持自带供应商密钥。规则上要求搜索供应商的爬虫遵守 Cloudflare 定义的「已验证机器人」公开要求，响应必须带指向被抓内容的链接；官方称会筛出支持零数据保留的供应商，并按供应商标价收费、不额外加价。动机很具体：agent 需要实时网页时往往先猜 URL 再调工具 curl，404 多半是猜错地址造成的。",
                            "detail": [
                                {"key": "能做什么", "value": "一个统一检索入口：REST 与 Workers 两种接入，多家搜索供应商可切换，日志与计费并到 AI Gateway，和模型调用同一条账单；要求返回来源链接，便于引用与审计。"},
                                {"key": "解决什么痛点", "value": "agent 联网检索现在是「猜 URL + curl」，命中率低且没有统一日志；企业还要分别和多家搜索 API 谈合同、做数据保留评估。"},
                                {"key": "值不值得", "value": "值得评估的是它的治理面：零数据保留筛选 + 已验证机器人 + 统一审计，这正好对应内网出口做联网检索时的合规诉求；限制是公测、供应商只有三家，结果可存储与再发布条款仍需逐条读 ToS。"}
                            ]
                        }
                    ]
                },
                {
                    "label": "产品与商业",
                    "items": [
                        {
                            "title": "Claude 把办公三件套收进对话：Whiteboards、Sheets 公测，Dashboards 改名 Data 转正式",
                            "url": U("sheets-whiteboards-data"),
                            "source": "Claude",
                            "summary": "Claude Whiteboards 与 Claude Sheets 进入 beta，原 Claude Dashboards 转 GA 并更名 Claude Data，三者对所有付费计划开放。Sheets 能从一句提示生成带 tab、公式、格式与下拉的工作表，逐格编辑时会标出每处改动，可导出 .xlsx/CSV 或转用 Claude for Excel。Whiteboards 能把一段口述的混乱计划变成带时间线、负责人与日期的板，可框选局部提问，收尾时转成 doc/deck 或推到 Lucid、Miro、Vani。Data 新增 data stories、certified queries 与 live sharing（后两项 beta），连接 Redshift、BigQuery、ClickHouse。产品意图是把产出留在 Claude 里继续协作，而不是每次导出到别的工具。",
                            "detail": [
                                {"key": "能做什么", "value": "把白板、表格、数据看板都做成对话内的可协作对象：生成即编辑、编辑有 diff 标注、可分享给团队共同改，并可导出到 Excel/CSV 或交接给 Lucid/Miro/Airtable/Asana 一类工具。"},
                                {"key": "解决什么痛点", "value": "过去用 Claude 做方案，产出必须复制到另一个工具才能团队协作，Claude 也失去对后续修改的上下文；协作与上下文被工具边界切断。"},
                                {"key": "值不值得", "value": "值得关注的是「agent 产出物就地协作」这个方向，它决定了 agent 能不能进入真实团队流程；但当前表格功能刻意做浅（复杂场景仍要 Excel），beta 阶段别当生产表格用。"}
                            ]
                        }
                    ]
                },
                {
                    "label": "观点与好文",
                    "items": [
                        {
                            "title": "Simon Willison 让 Claude Code 造一台「蜂鸣定位仪」：五个设备三角定位，误差 40cm",
                            "url": U("mysterious-beeps"),
                            "source": "Simon Willison",
                            "summary": "家里储物间有东西间歇性蜂鸣，间隔太长没法靠站在房间里听出来。他让 Claude Code 写了个 Beep Locator：跑一个 Python web server 起主界面，用二维码把身边的设备（两台 iPad、一台手机、一台 MacBook Pro、一台 Surface）接成监听节点，先靠设备互发声音粗估位置，也可以手动拖图标给粗略坐标再校正。为了验证可靠性，他加了拍手模式——在不同位置拍手，看系统能否定位。确认蜂鸣频率后，系统持续监听、测间隔，并用三角定位锁定地图上最可能的位置。最终定位误差约 40cm，按位置翻箱找到一台旧一氧化碳报警器在等换电池。方法上 Claude 自己找出了 2007 年的 BeepBeep 论文（用商用设备的声学测距与定位）作为基础。",
                            "detail": [
                                {"key": "能做什么", "value": "一个完整的小系统：Python web server + 多设备浏览器当麦克风阵列 + 声学测距（互发声音标定）+ 三角定位 + 频率确认与拍手自测模式；最终把「哪个盒子在响」收敛到 40cm 范围。"},
                                {"key": "解决什么痛点", "value": "间歇性、短促的声音无法靠人耳定位，逐个翻箱成本极高；这类问题不值得雇人也不需要专业设备，正好落在「一次性小工具」的区间。"},
                                {"key": "值不值得", "value": "值得当 agent 落地的样例看：真正的价值不是代码量，而是它自己检索到 2007 年的论文并把方法落成可验证的系统，还主动加了「拍手模式」这种自证手段。限制是这类项目靠个人判断收敛，换到生产要有明确的验收标准。"}
                            ]
                        }
                    ]
                },
                {
                    "label": "安全与治理",
                    "items": [
                        {
                            "title": "VulnCheck 复盘 Anthropic Glasswing：七个月 442 个 CVE，3.8 万条发现只有 19.4% 公开、217 条标记修复",
                            "url": U("glasswing"),
                            "source": "VulnCheck",
                            "summary": "Project Glasswing 于 4 月 7 日启动，七个月后 VulnCheck 按 CVE 记录、GHSA、内核 commit 与 Anthropic 自己的披露台账逐条核对：可归因于 Anthropic 的 CVE 有 442 个，只占今年已发布 9.3 万个 CVE 的约 0.5%，月均 63 个，其中仅 2 个被确认在野利用。Anthropic 报告的 37,966 条发现里，7,349 条（19.4%）已公开、217 条标记为已修复；9 月以来新增近 1.2 万条发现，却只多 15 个修复，发现与修复的缺口在扩大。自称真阳性率从 90.8% 升到 94.2%，但 1,654 条（4.4%）被标为重复、419 条撤回；OSS Scanner 把验证工作推给维护者，curl 把 34 份已发布报告里的 19 份驳回，6 份确认为低危。",
                            "detail": [
                                {"key": "能做什么", "value": "一份可复核的量化台账：按 CVE/GHSA/内核 commit 交叉，逐月统计发现量、公开率、修复数与重复率，并抽查具体项目的驳回情况（curl 34 份报告 19 份被否）。"},
                                {"key": "解决什么痛点", "value": "AI 找漏洞的宣传以「发现数」计价，但真实价值取决于公开率、修复率与误报率；维护者面对大量低质量报告，验证成本被转嫁到开源社区。"},
                                {"key": "值不值得", "value": "值得读，因为它给了审计 AI 安全产出的方法而不是结论：0.5% 的 CVE 占比、19.4% 公开率、4.4% 重复率这三组数字可以直接照搬到内部评估。限制是作者立场偏批判、Anthropic 台账更新是批量式的，双方口径不完全可比。"}
                            ]
                        },
                        {
                            "title": "OpenAI 开源 codex-security：扫描、验证可利用性、生成补丁的 CLI 与 TypeScript SDK",
                            "url": U("codex-security"),
                            "source": "GitHub Trending",
                            "oss": True,
                            "summary": "仓库提供安全 CLI（cs scan）与 TypeScript SDK，流程分三段：扫描仓库/指定路径/Git 变更，验证候选发现并生成补丁，再验证既有修复是否真的有效。除扫描外还能起草 SECURITY.md、保存威胁模型、按自定义 rubric 评严重度、从源码与 Git 历史推荐负责人，并预览第三方扫描器结果、导出 SARIF/JSON/CSV、把发现同步到 Linear/Jira/GitHub。也能以 GitHub Action 或容器形式在 CI 里批量跑。对想把 agent 安全扫描接进流水线的团队，这是一个现成的命令行与 SDK 入口。",
                            "detail": [
                                {"key": "能做什么", "value": "把「找—验—修」做成流水线：scan 支持标准与深度两种，深度扫描会重复标准扫描并做去重；验证环节判断候选发现是否可利用，之后生成补丁；还有威胁模型、责任人推荐与工单同步。"},
                                {"key": "解决什么痛点", "value": "静态扫描的通病是发现多、可利用性未知、误报压垮维护者；只报不修还需要人再走一遍上下文。它把验证与补丁生成纳入同一工具面。"},
                                {"key": "值不值得", "value": "值得在 CI 里试一轮，尤其是已有 Codex 用量的团队——成本低、能直接产出 SARIF 进现有流程；限制是需 Node 22.13+/Python 3.10+，深度扫描耗时与 token 成本要实测，且模型判断的严重度仍需人审。"}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "label": "☸️ 基础设施板块",
            "categories": [
                {
                    "label": "K8s × AI",
                    "items": [
                        {
                            "title": "KubeRay 捐给 CNCF：PARK 栈（PyTorch/Ray/K8s）全部归到 Linux Foundation 治理",
                            "url": U("donating-kuberay"),
                            "source": "CNCF Blog",
                            "summary": "KubeRay 是让 Ray 的分布式 AI/ML/Python 负载跑在 Kubernetes 上的 operator，提供三类 CRD：RayCluster（集群生命周期）、RayJob（作业提交）、RayService（服务化与滚动升级）。PARK 栈的其余部分早已在 Linux Foundation 之下——PyTorch 与 Ray 归 PyTorch Foundation、Kubernetes 归 CNCF，KubeRay 是最后一块拼图，进 CNCF 后整栈归属同一治理体系。落地案例：Spotify 用它支撑内部 ML 平台 Hendrix，在 GKE 上用 Ray 训练与微调模型；Hark 用它跑多模态 agent 工作流。项目以 Sandbox 级别进入，作者群来自 Ray 与 K8s 两侧。",
                            "detail": [
                                {"key": "能做什么", "value": "把 Ray 的集群、作业与服务三类生命周期映射成 K8s CRD，让 Python-first 的 AI 框架直接吃 K8s 的调度、弹性与配额；可与 Kueue 等队列系统配合做批任务排队。"},
                                {"key": "解决什么痛点", "value": "Ray 自己的调度器与 K8s 并行运行会造成容量碎片与两套配额；平台团队要么放弃 K8s 原生能力，要么自己写胶水。KubeRay 是官方胶水。"},
                                {"key": "值不值得", "value": "值得关注治理层面的变化：PARK 全栈同属一个基金会后，版本兼容与路线协同会好转；技术上是成熟 operator，可直接评估。限制是 Sandbox 级别、CNCF 不管技术方向，实际能力仍看 Ray 社区节奏。"}
                            ]
                        },
                        {
                            "title": "NVIDIA 把 OpenShell 捐给 CNCF：agent 的策略边界下沉到基础设施层，用 Cedar 写规则",
                            "url": U("welcoming-openshell"),
                            "source": "CNCF Blog",
                            "summary": "OpenShell 是给自主 agent 做安全与治理的开源运行时，进 CNCF Sandbox。核心主张是能力必须落在 agent 之外——在 agent 运行的基础设施里执行策略，管住它能碰的数据、密钥与网络。策略语言采用 CNCF 另一个项目 Cedar，形成项目间的组合。NVIDIA 贡献，Red Hat、Docker、Canonical 的核心贡献者在项目早期就参与；设计上留了 providers、compute、治理与审批流、策略执行、隔离、凭据管理六类扩展点，团队可以增量接入并替换成自己已有的组件。仓库从 NVIDIA 迁到中立组织 ai-openshell，接受 CNCF 行为准则、走公开 RFC 与 vendor-neutral 治理。",
                            "detail": [
                                {"key": "能做什么", "value": "在基础设施侧给 agent 划边界：定义它能调用什么、能读哪些密钥与网络端点，策略用 Cedar 表达并可审计；通过扩展点对接不同的推理供应商、密钥库与审批流。"},
                                {"key": "解决什么痛点", "value": "要让 agent 真正干活就得给权限，但给了权限就没有边界；靠提示词约束或应用层判断都不可靠。把执行点放到运行时层，才能做到「给能力不给全权」。"},
                                {"key": "值不值得", "value": "和多用户 agent 沙箱是同一道题：隔离粒度、凭据代管、策略可审计。值得对照它把哪些东西定义成扩展点；限制是 Sandbox 早期、策略生态还在建，且 Cedar 的表达力对复杂审批流需要自己补。"}
                            ]
                        },
                        {
                            "title": "GKE ClusterNetworkPolicy：三层优先级把 LLM 命名空间和 metadata API 一起管住",
                            "url": U("experimenting-with-clusternetworkpolicy"),
                            "source": "Google Cloud",
                            "summary": "标准 NetworkPolicy 只能按命名空间生效，ClusterNetworkPolicy（CNP）提供集群级、三层优先级的策略模型：admin 层由集群管理员强制、不可被绕过（例如封住 metadata 访问），network policy 层由应用团队管自己的 ingress/egress，baseline 层给集群兜底（例如默认拒绝）。Google 的实验用自定义 VPC + Cloud NAT、2x2 拓扑的 TPU v5e 节点池（带 taint 只接加速器负载）、vLLM 服务的 Gemma 4 E2B，目标是只允许授权客户端访问 LLM 命名空间，并只放行 DNS 53 去访问 metadata；执行由 GKE Dataplane V2 的 eBPF 完成，GKE Network Policy Logging 记录每个包的 allow/deny 判决与策略审计链。",
                            "detail": [
                                {"key": "能做什么", "value": "把策略分权：管理员能设不可覆盖的强制规则（metadata、出口）与全集群兜底，团队仍在自己命名空间写常规 NetworkPolicy；eBPF 数据面执行并给逐包判决日志。"},
                                {"key": "解决什么痛点", "value": "多租户集群里，namespace 级策略管不住「谁能访问 metadata/凭证」这类集群面风险；管理员想统一底线，又不想接管所有业务规则。"},
                                {"key": "值不值得", "value": "值得直接照 Codelab 做一遍：三层优先级是把安全底线与应用自治分开的可行结构，尤其适合托管 LLM 推理服务的命名空间隔离。限制是 GKE 特性（Dataplane V2/eBPF），多云要自己找等价物；CNP 仍在推进中，先验证与现有 CNI 策略的叠加行为。"}
                            ]
                        },
                        {
                            "title": "Istio Ambient Multi-Network GA：跨几十个 K8s 集群做 active-active，sidecar 可平滑迁到 ambient",
                            "url": U("istio-enables"),
                            "source": "CNCF Blog",
                            "summary": "KubeCon NA 2026 上 Istio 给出四件事：Ambient Multi-Network 正式 GA，可在跨网络、跨区域、跨云的上几十个 K8s 集群上部署 active-active 工作负载并保持一致的连通与流量管理；新增 sidecar 到 ambient 的迁移支持，存量用户不必从头重建；Traffic Extension API 用 Lua 与 WebAssembly 改路由、重定向、过滤，不需要深入 Envoy 内部实现。项目自报 ambient 架构相比 sidecar 可提升 60% 以上资源利用率、降低 75% 延迟。整体定位是给同时跑传统服务与 AI agent 的平台方一套统一网络底座。",
                            "detail": [
                                {"key": "能做什么", "value": "多集群多网络的 active-active 服务网格（GA 级），加上 sidecar→ambient 的迁移路径与 Wasm/Lua 级流量扩展；ambient 把网格能力从每个 Pod 的 sidecar 里拿出来，变成节点级 ztunnel。"},
                                {"key": "解决什么痛点", "value": "跨云跨区部署要一致的安全策略与流量管理，而 sidecar 模式给每个 Pod 加代理，资源与延迟开销随规模放大；存量 sidecar 用户又难以切换。"},
                                {"key": "值不值得", "value": "值得评估 ambient 的迁移成本而不是只看 60%/75% 的数字——那两个是项目自报。对要做多集群 active-active、且集群规模大的团队，Multi-Network GA 是当前少有的成熟选项；限制是 ambient 与部分 L7 特性的功能差距仍需逐项核对。"}
                            ]
                        }
                    ]
                },
                {
                    "label": "K8s 核心技术",
                    "items": [
                        {
                            "title": "CloudNativePG 进 CNCF Incubating：不用 StatefulSet 管 PostgreSQL，50+ 生产用户",
                            "url": U("cloudnativepg"),
                            "source": "CNCF Blog",
                            "summary": "CNCF TOC 投票通过 CloudNativePG 成为 Incubating 项目。它用 primary/standby 加原生流复制，直接管理 PostgreSQL 实例的 Pod 而不依赖 StatefulSet，把集群状态交给 K8s 的声明式 reconcile，覆盖自动 failover、滚动升级、自愈、连接池、持续备份与时间点恢复（PITR）。2025 年 1 月进 Sandbox 后连发 1.26–1.30 五个版本，最新 v1.30.1 于 2026-09-23 发布。生产用户超过 50 家，含 IBM、Google Cloud、Microsoft Azure、GEICO、Tesla 等；与 External Secrets、Cilium、cert-manager、Prometheus exporter、Keycloak OAuth 有文档化集成。一个具体例子是 OpenBao 用它做存储后端：三实例 + quorum 同步复制，DatabaseRole 自动签发并续期 TLS 客户端证书，做到数据库角色无密码。",
                            "detail": [
                                {"key": "能做什么", "value": "把 PostgreSQL 高可用做成 K8s 原生：CRD 声明集群形态，operator 管 failover、备份/PITR、连接池与滚动升级，实例 Pod 由 operator 直接管理，绕过 StatefulSet 的更新语义限制。"},
                                {"key": "解决什么痛点", "value": "在 K8s 上跑有状态数据库通常要外挂 Patroni 一类工具做选主，故障切换与 K8s 调度两套逻辑互相打架；版本升级、证书轮换与备份也各有一套脚本。"},
                                {"key": "值不值得", "value": "值得作为「有状态服务上 K8s」的参考实现读，尤其是它用 CRD 管角色与证书、做到无密码连接的做法；进 Incubating 说明治理与采用度过关。限制是只支持 PostgreSQL，且运维仍需要懂 PG 的复制与备份语义。"}
                            ]
                        },
                        {
                            "title": "Open Cluster Management 进 CNCF Incubating：hub-spoke + 异步 pull，eBay 用它管 190+ 集群",
                            "url": U("open-cluster-management"),
                            "source": "CNCF Blog",
                            "summary": "OCM 用 hub-and-spoke 架构与开放 API 管跨云、本地与边缘的 K8s 集群：注册集群、分发应用与策略、做工作负载放置，不依赖私有控制面。架构上坚持轻量模块化，异步 pull 模型让各集群保持自治、hub 上不集中存放敏感凭据；插件式 add-on 框架让其他项目直接继承多集群能力。2021 年 11 月进 Sandbox，2025 年 6 月发布 1.0，到 2026 年 10 月的 1.4 共四个 minor 版本；实现并对齐 SIG-Multicluster API，给 Argo CD 提供集群决策、与 Cluster API 集成，Kueue、KubeVela、KubeStellar、Meshery 都有集成文档。27 名 maintainer 来自 8 个组织，eBay 用它支撑 190 多个集群的应用分发。",
                            "detail": [
                                {"key": "能做什么", "value": "多集群控制面：集群注册与生命周期、应用与策略分发、放置决策；pull 模式让被管集群主动拉取期望状态，hub 失联时负载不受影响。"},
                                {"key": "解决什么痛点", "value": "集群一多，GitOps 只能解决「推什么」，解决不了「推到哪些集群、按什么规则放置」；集中式控制面又会把凭据与单点风险堆在 hub。"},
                                {"key": "值不值得", "value": "值得评估的是 pull 与 hub 不存凭据这两条设计，直接关系到跨云/边缘的故障域；如果团队正从几套集群扩到几十套，它是 Argo CD 之上补「放置层」的现成方案。限制是概念多（ManagedCluster、Placement、ManifestWork），学习曲线不低。"}
                            ]
                        }
                    ]
                },
                {
                    "label": "社区与项目",
                    "items": [
                        {
                            "title": "CNCF 观点：平台工程要「更像人、少点机器人」——使用者从工程师变成了所有人",
                            "url": U("platform-engineering-needs"),
                            "source": "CNCF Blog",
                            "summary": "作者 Alejandro Chirinos 用自己在 Disney、Dell、SAP、VMware 的经历说明一件事：内部平台一直是按「会读文档、知道什么是回滚、懂得什么时候不该上线」的工程师设计的，流程严格但合理，因为使用者本身就像机器一样守协议。当 agent 让非工程师也能在几小时内拼出系统，这个前提失效了——平台面对的输入从「专业但偶尔犯错」变成「完全不熟悉协议」。文章的落点是平台工程需要重新设计引导与防护，而不是继续假设使用者懂规矩。",
                            "detail": [
                                {"key": "能做什么", "value": "提出一个判据：平台的设计假设（使用者专业度、是否读文档、是否守流程）一旦改变，原有的 stage gate、命名规范与审批就变成摩擦而非保护。"},
                                {"key": "解决什么痛点", "value": "AI 让「能产出系统的人」数量级增加，但这些人不具备运维直觉；平台若继续按专家设计，事故率会随使用者扩大而上升。"},
                                {"key": "值不值得", "value": "值得当观点文读十分钟，用来校准内部平台的默认假设；但它不给方案、也没有数据，属于问题陈述而非工程结论。"}
                            ]
                        }
                    ]
                }
            ]
        }
    ],
    "flash": [
        {"title": "Anthropic 撤回近 700 亿美元 IPO 定价、最快当日启动路演", "url": U("8tquwes1yGbmTeyOjOId")},
        {"title": "Azure Front Door edge actions 正式可用", "url": U("579310")},
        {"title": "Azure Functions 支持 .NET 11 正式可用", "url": U("578773")},
        {"title": "苹果将推新 Mac 应用，简化本地模型运行", "url": U("mac-app-coming")},
        {"title": "双 11 当天多家大模型厂商在天猫打 5 折", "url": U("509085")},
        {"title": "llm-gemini 0.36：Gemini 命令行插件更新", "url": U("llm-gemini")}
    ]
}

# ---- assertions: every content item has title/url/detail ----
def walk(o, path="root"):
    if isinstance(o, dict):
        if "url" in o:
            assert o.get("title"), "missing title at %s" % path
            assert o["url"], "missing url at %s" % path
        if o.get("key"):
            assert o.get("value"), "empty detail value at %s" % path
        for k, v in o.items():
            walk(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + "[%d]" % i)

for h in b["highlights"]:
    assert h.get("detail") and len(h["detail"]) == 3, "highlight detail must be 3 rows"
assert b["issue"] == 51
walk(b)

EMOJI = {"🧩 Agent & Skill": "🧩", "Agent & Skill": "🧩", "模型与研究": "🧠", "AI 工程落地": "🛠️",
         "产品与商业": "📊", "观点与好文": "💡", "安全与治理": "🛡️", "K8s × AI": "🤖☸️",
         "K8s 核心技术": "☸️", "云原生周边": "☁️", "社区与项目": "🏘️", "公有云动态": "☁️"}
for s in b["sections"]:
    for c in s["categories"]:
        c["title"] = c["label"]
        c.setdefault("emoji", EMOJI.get(c["label"], "•"))
        for it in c["items"]:
            assert it.get("detail") and len(it["detail"]) == 3, "item %s detail" % it["title"]

json.dump(b, open(os.path.join(REPO, "briefing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = len(b["highlights"]) + sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
print("wrote briefing.json: highlights=%d items=%d flash=%d sections=%d" % (
    len(b["highlights"]), n, len(b["flash"]), len(b["sections"])))
for s in b["sections"]:
    print(" ", s["label"], [(c["label"], len(c["items"])) for c in s["categories"]])
