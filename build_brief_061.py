#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 061 (2026-11-21)."""
import json, os, sys

REPO = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(REPO, "processed.json"), encoding="utf-8"))

BY_PREFIX = {}
for it in items:
    u = it["url"]
    BY_PREFIX.setdefault(u.split("?")[0], u)
    BY_PREFIX.setdefault(u, u)


def U(frag):
    """Return the exact URL from processed.json that contains frag."""
    hits = [u for u in {i["url"] for i in items} if frag in u]
    if len(hits) != 1:
        hits2 = [u for u in {i["url"] for i in items} if frag in u]
        print("URL LOOKUP FAIL", frag, hits2, file=sys.stderr)
        raise SystemExit(1)
    return hits[0]


EMOJI = {
    "🧠 模型与研究": "🧠", "🧩 Agent & Skill": "🧩", "🧭 Agent 工具链": "🧭",
    "🏖️ 沙箱与运行时": "🏖️", "🛠️ AI 工程落地": "🛠️", "📜 平台政策与风控": "📜",
    "📊 产品与商业": "📊", "💡 观点与好文": "💡", "🛡️ 安全与治理": "🛡️",
    "🤖☸️ K8s × AI": "🤖☸️", "☸️ K8s 核心技术": "☸️", "云原生周边": "☁️",
    "社区与项目": "🧑‍🤝‍🧑", "公有云动态": "☁️",
}


def it3(can, pain, worth):
    return [{"key": "能做什么", "value": can},
            {"key": "解决什么痛点", "value": pain},
            {"key": "值不值得", "value": worth}]


# ---------------- highlights ----------------
highlights = [
    {
        "title": "Agent Sandbox v1.0.12：三个 SDK 统一支持 suspend/resume，空闲沙箱释放 Pod 但保留 claim 与持久卷",
        "url": U("agent-sandbox/releases/tag/v1.0.12"),
        "source": "GitHub Releases",
        "summary": "kubernetes-sigs 的 Agent Sandbox 11 月 20 日发布 v1.0.12，核心是把 suspend()/resume()/is_suspended() 补齐到 Go、Python、TypeScript 三个 SDK：通过对 Sandbox 打 spec.operatingMode 补丁（带 UID 守卫）释放 Pod，但保留 SandboxClaim 与持久卷。运行中的进程、内存与 emptyDir 不会随挂起保留，要连内存一起留住得配 pod snapshot。控制面新增 SandboxWarmPool 的 per-pool readinessGracePeriodSeconds（最小 30 秒，默认 5 分钟，可双向覆盖集群级默认）。sandbox-router 增加 Ed25519 v2 的沙箱级 scoped token，绑定 (namespace, name, uid)，在过期前授权该沙箱所有端口与方法；sandboxd 增加 ?stat=true 的单路径元数据与更细的 REST 错误码（ENOSPC/EDQUOT→507、ENAMETOOLONG→400）。示例里补了 CI runner sandbox 与 Claude Code 走集群内模型代理、跨 suspend/resume 保持会话两套。",
        "note": "v1.0.12 于 11 月 20 日发布；suspend/resume 覆盖 Go/Python/TypeScript 三个 SDK；readyness grace 最小 30s、默认 5m；Ed25519 v2 token 绑定 namespace+name+uid；新增 CI runner 与 Claude Code 两个示例。",
        "detail": it3(
            "用 operatingMode 让 Sandbox 的 Pod 释放、claim 与 PV 保留，三个语言的 SDK 都带 suspend/resume；WarmPool 可按池设就绪宽限（最小 30s）；router 的 Ed25519 token 能限定到单个沙箱的 namespace/name/uid。",
            "agent 会话大部分时间空闲，Pod 却一直占着 CPU 与内存；以前只能删沙箱（丢环境、丢卷）或自己写控制器做挂起回收，per-session 沙箱的成本迟迟降不下来。",
            "值得直接读 CRD 与三个 SDK 的实现：它把「挂起但保留工作区」做成 K8s 原语，正对多租户沙箱做空闲回收的痛点。限制是进程与内存不随挂起保留（需配 pod snapshot），且 scoped v2 token 要求所有 sandbox-router 副本先升级，老副本会 403。"),
    },
    {
        "title": "Inkling 2 Mini：中间层重复三遍的循环 Transformer，100B 以下开源权重在 agentic coding 上排到前列",
        "url": U("thinkingmachines.ai/news/inkling-2-mini"),
        "source": "Thinking Machines Lab",
        "oss": True,
        "summary": "Thinking Machines 11 月 20 日发布 Inkling 2 Mini，架构上是循环 Transformer：每个 token 都把模型中间层重复计算三次，官方说法是用更少的 token 换更高的推理质量，重点针对依赖推理质量的 agentic coding。总参数低于 100B，小到能在笔记本上跑。官方基准是 DeepSWE v1.1 解出 48.2%、Vals Index v2.2 拿到 46.5%，称在 100B 以下的开源权重里排第一，且在同等成绩的模型里理论 token/s 更高。权重已在 Hugging Face 放出，可通过 Tinker 调用。",
        "note": "11 月 20 日发布；循环 Transformer，中间层每 token 跑 3 次；总参数 <100B、可跑在笔记本；DeepSWE v1.1 48.2%、Vals Index v2.2 46.5%；权重开源在 Hugging Face，可经 Tinker 调用。",
        "detail": it3(
            "用循环深度代替堆参数：中间层每个 token 重复 3 次，在 <100B 规模把 DeepSWE v1.1 做到 48.2%、Vals Index v2.2 做到 46.5%，同时保持较高理论 token/s，权重开源、本地可跑。",
            "想用够强的 agentic coding 模型又不想把代码送出网的团队，长期只能在「小模型不够用」和「大模型跑不动」之间选，本地可跑且接近前沿的编码模型稀缺。",
            "值得实测本地吞吐与长任务稳定性：48.2% 是官方自测口径，循环层会推高单 token 延迟，理论 token/s 与真机差距要看；若单机能撑起 agent 循环，内网编码 agent 就是低成本试点。"),
    },
]

# ---------------- AI sections ----------------
ai_cats = []

ai_cats.append({"label": "🧠 模型与研究", "items": [
    {
        "title": "27B 开源模型自己改自己的权重：无梯度、不训练，未见题目上准确率 +6.6 点",
        "url": U("huggingface.co/papers/2611.21885"),
        "source": "HuggingFace Papers", "oss": True,
        "summary": "论文提出 self-rewriting：把权重、评分后的答案和「运行自己」的能力交给模型，让它诊断自己的失败并直接改写背后的权重，全程没有梯度也没有训练。在一个开放 27B 模型上，一次自编辑让未见题目的准确率提升 6.6 个点，并在连续八次会话里单调上升——每次先在练习题上验证编辑，只提交有效的。它还能修一个几乎全错的自身副本：不重训、不读原始权重，恢复到原模型 80% 以上的图像任务准确率。作者称该能力随规模涌现：同一模型家族里小模型改不动或把自己改坏，只有最大的那个能改进并自修。",
        "detail": it3(
            "模型把自身权重当可编辑对象：自评 + 自运行定位失败，再写权重补丁；27B 单次编辑 +6.6 点，八次会话单调提升，还能把损坏副本恢复到 >80% 准确率。",
            "常规后训练要重跑训练管线与 GPU 集群；推理期的 prompt/scaffold 收益任务一结束就消失。self-rewriting 把收益写进权重，且每次回答不额外付费。",
            "值得跟进但别急着上生产：目前是单模型、单任务族的结果，编辑正确性靠自评把关，退化风险与可复现性仍需第三方复现；关注持续学习方向的话，这是近期最具体的一篇。"),
    },
]})

ai_cats.append({"label": "🧩 Agent & Skill", "items": [
    {
        "title": "System 1 agents：不生成文本、把工具调用做成选择题，1952 次请求里 97.0% 选对工具",
        "url": U("huggingface.co/papers/2611.21053"),
        "source": "HuggingFace Papers", "oss": True,
        "summary": "论文针对「敏感临床数据不能出网、本地 LLM 又会编参数」的两难，提出 System 1 agents：本地 agent 调工具时不生成文本。做法是用一个确定性编译器，把每个工具的 schema 与请求变成若干选择题——选项只来自请求和 schema——再由一遍式决策模型作答。在 157 个生物医学工具、1952 次请求上，最好的 System 1 agent 选对工具或正确拒答的比例是 97.0%，高于 18 个本地 LLM agent 设置里最好的 95.2%；6056 个参数值填对 97.0%，且没有任何一次调用含编造内容，而 LLM 调用有 5.5%–19.7% 含编造值。框架已开源。",
        "detail": it3(
            "把开放式生成换成受限多选题：工具选择与参数填充都变成从 schema/请求里枚举的选项，决策模型一遍作答，因此不可能产出 schema 之外的值。",
            "医疗等场景不能把数据发给云端 LLM，本地小模型又会幻觉参数，而一次编造的值会污染后续每一步工具调用。",
            "值得读它的编译器设计——把「工具调用」降成「分类 + 填空」是可控 agent 的通用套路，可迁移到任何有清晰 schema 的内部工具集；限制是工具必须有严格 schema，开放式任务不适用。"),
    },
    {
        "title": "Repo-Premium 基准：稠密检索的领先大半来自评测口径，用 LLM 生成标识符再 grep 就能追平",
        "url": U("huggingface.co/papers/2611.20455"),
        "source": "HuggingFace Papers", "oss": True,
        "summary": "论文指出代码检索基准里「稠密向量远胜 BM25」多半是评测选出来的：查询精心构造、代码偏旧、BM25 还被削弱（把文件切块、把改过的测试算作相关）。作者自建 Repo-Premium——真实仓库的文件级排序、Python/JS/TS/Go/Rust/Java 六种语言、2022–2026 的 PR、91 个仓库的预注册测试池。结论是稠密优势可拆成两部分：偏袒稠密的评测选择，以及查询里缺少代码中的稀有标识符。用 LLM 先写出可能的标识符再 grep（generate-then-grep），在每一个 Python 测试池里都能追平稠密检索，包括模型发布之后才开的 PR。作者给出三条建议：跟公平的词法基线比、稠密与 BM25 融合、给缺词的查询补上代码里的词。",
        "detail": it3(
            "用 91 个真实仓库、六语言、四年 PR 的基准把「稠密 vs 词法」拆开度量，并给出廉价补强：让 LLM 生成候选标识符再 grep。",
            "团队常按论文结论直接上向量库，忽略 BM25 基线，换来很小的实际收益却付出索引与延迟成本；代码 agent 里 grep 明明够用，却说不清为什么。",
            "值得用来校准内部代码检索选型：先做公平 BM25 基线，再决定是否加向量；不宜据此彻底放弃稠密——论文自己也承认没有方法能预测单条查询该用哪个，融合更稳。"),
    },
]})

ai_cats.append({"label": "🧭 Agent 工具链", "items": [
    {
        "title": "Claude Code v2.1.330：企业管理员控制台登录落地、内置 easel 图表、自托管 runner 加两个时延指标",
        "url": U("claude-code/releases/tag/v2.1.330"),
        "source": "GitHub Releases", "oss": True,
        "summary": "11 月 20 日的 v2.1.330 把企业侧打通：支持登录由 Anthropic Enterprise Admin Console 管理的组织，claude auth login 之后自动套用组织设置并走组织指定的云厂商或网关。新增内置 easel mod，被要求画图时直接出图，也能画在 MCP 指标结果下面（Pro/Max 与部分 Team/Enterprise，macOS 与 Linux，可在 /config 关掉自动图表）。自托管 runner 增加 --start-dir / SELF_HOSTED_RUNNER_START_DIR，让会话从仓库某个子目录开始；/metrics 增加 order→registered 与 order→first-session 两个秒级指标。修复面很实：长对话 compact 后卡死数分钟、WebFetch 在部分页面卡住或返回空、多进程并发写设置互相覆盖、子 agent 声明的 MCP server 被提前关闭、退出 worktree 时删掉另一个会话正在用的 worktree。",
        "detail": it3(
            "组织级登录与策略下发走 Admin Console；easel 是内置图表 mod（含 MCP 指标可视化）；runner 增加启动目录与两个排队时延指标；一批并发与卡死 bug 被修掉。",
            "企业内推广 Claude Code 最难的是账号与策略统一（谁属于哪个组织、走哪个网关），以及长会话卡死、多开实例互相踩设置这类日常磨损。",
            "值得升级，尤其是有自托管 runner 或多开窗口的用法；升级前确认组织确实在 Admin Console 里管理，否则这条登录路径不生效。"),
    },
    {
        "title": "Codex 0.171.0：模型目录加入 GPT-6.2 Sol/Astra、TUI 工作区默认开、codex exec 可挂远端 app server",
        "url": U("codex/releases/tag/rust-v0.171.0"),
        "source": "GitHub Releases", "oss": True,
        "summary": "0.171.0 把 GPT-6.2 Sol 与 Astra 写进模型目录，Sol 成为默认目录选项。TUI 工作区默认启用：主对话旁可并排看可搜索的文档预览、图片预览与子 agent 转录。非交互场景新增 codex exec --remote <ADDR>，直接在已有的 app server 上开或续会话；TUI 里用 /rc、/remote 管本地远控与设备配对码。修复切换或恢复会话时草稿与排队 follow-up 丢失、换工作目录后权限 profile 失效、上一轮的完成事件取消新一轮审批、steering 时聚合 diff 丢旧编辑等问题。",
        "detail": it3(
            "模型目录接入 Sol/Astra 且 Sol 默认；TUI 变多面板工作区（文档/图片/子 agent 转录）；exec 支持远端 attach，/rc 管设备配对码。",
            "在服务器上跑 app server、本地只做前端的人，很难把非交互任务挂到同一会话；多面板省掉在终端与编辑器之间来回切。",
            "值得跟，尤其是有「远端会话 + 本地 TUI」用法的人；Sol 成为默认目录项意味着新配置默认选它，脚本里显式指定模型的要复核。"),
    },
]})

ai_cats.append({"label": "🛠️ AI 工程落地", "items": [
    {
        "title": "Frostbite：AI 从零设计出一颗通用 CPU，ISA、微架构、RTL、验证到 GDS 全由 agent 群迭代",
        "url": U("architectlabs.com/blog/frostbite"),
        "source": "Architect Labs",
        "summary": "Architect Labs 11 月 18 日发布 Frostbite：一颗指令集全新设计的通用 CPU，从编译器、ISA、微架构、RTL、验证到最终 GDS 都由 AI 系统自主迭代产出，公司称全程「零架构先验」，过程中跑的是多个 agent swarm。设计押在 interaction nets 上——程序的每一步都是局部的、依赖显式、每个值只有一个所有者——因此不必靠乱序执行在运行时重新发现依赖。作者给的例子是五皇后搜索：顺序程序一次只看一个候选，interaction net 平均每一步有约 12 个交互可并行执行，而程序本身一行没改。公司称由此拿到「免多线程」的并行（无锁、无竞争）与台阶式的性能提升。",
        "detail": it3(
            "用 agent swarm 跑完架构探索→ISA→微架构→RTL→验证→GDS 全链路，产出一个基于 interaction nets 的新 ISA 通用 CPU 设计。",
            "通用 CPU 架构几十年停滞，根因之一是主流语言把依赖藏在共享可变状态里，硬件只能在运行时猜；interaction nets 把并行性暴露在程序结构里，省掉乱序与一致性开销。",
            "值得读方法论而不是等芯片：这是「agent 群做长链路硬件工程」目前最完整的公开案例，验证与收敛怎么组织比结果更有参考价值；性能数字要打折看——来自公司自己的工作负载与仿真。"),
    },
    {
        "title": "生产 DAG 半夜 OOM 没有 traceback：Managed Airflow Agent 把 worker 内存与重试对上，给出三条修法",
        "url": U("scaling-airflow-pipelines-with-ai-agents"),
        "source": "Google Cloud",
        "summary": "Google Cloud 用一个具体案例讲 Managed Airflow（原 Cloud Composer）里的 agent：零售商 Cymbal 的 clickstream DAG 由 agent 生成并部署到 Airflow 2.11.1 环境（worker 2 vCPU/4GB，1–6 台自动伸缩）。10 月大促加新版 App 让一小时事件从约 350MB 涨到约 1.4GB，pandas 把整小时 concat 进内存后，10 月 23 日 14:00 UTC 那次运行三次重试全挂且任务日志无报错。控制台的 Investigate 让 agent 自己查：它把 worker 内存指标与任务重试对上，报告里每条结论都附证据，最后给出三条修法——直接写 BigQuery、分批处理、或加 worker 内存。运维先选加内存，再让 agent 分析整个环境该给多少内存。",
        "detail": it3(
            "在控制台对失败 run 一键 Investigate：关联 worker 内存指标、任务重试与日志，输出带证据链的诊断与可执行修法；同一 agent 还能判断 DAG 是否适配新版本 Airflow。",
            "生产管道失败的难点不是修而是定位——任务无 traceback 死掉时，线索散在 task log、scheduler log 与 worker 指标三处，人工要跨三处对时间线。",
            "值得看它的「证据链」设计：每条结论给依据，是把 agent 放进运维闭环的前提；但它绑定 Managed Airflow 控制台，自建 Airflow 只能借鉴「指标 + 重试」的关联诊断思路。"),
    },
]})

ai_cats.append({"label": "🛡️ 安全与治理", "items": [
    {
        "title": "Grab 给 AI 生成代码上分层防御：预生产门禁 + 灰度 + 开关，崩溃自动映射到具体 PR",
        "url": U("AH8deOIGb5hMHRPIKfrf"),
        "source": "InfoQ 中国",
        "summary": "Grab 说 AI 编程助手普及后每版代码变更量变大，缺陷与崩溃概率随之上升，于是把稳定性防线做成四段：合并前用 Android Lint/SwiftLint（含自研规则）与单测、UI 测试拦；预生产用 Grab Early Access 把早期包发给内部用户持续监控——只有少数内部用户会碰到的崩溃，到生产规模就是崩溃率飙升与紧急热修；发布阶段用分阶段放量与功能开关，崩溃率超阈值就关开关而不发版；发布后用 Crashlytics + BigQuery 实时监控，自动分诊把崩溃元数据与堆栈映射到具体 PR，事后复盘再反哺 Lint 规则与测试覆盖。",
        "detail": it3(
            "用左移的 lint/测试、内部灰度门禁、分阶段放量与实时崩溃监控四层接住 AI 带来的变更量增长，并形成「事故→规则」的反馈环。",
            "AI 让提交变多、单次变更变大，崩溃更难定位——并非所有崩溃都有符号化堆栈，得交叉比对发布时间表、开关发布记录与会话元数据。",
            "值得抄结构而不是工具：内部灰度门禁 + 开关兜底 + 崩溃→PR 映射这套组合，对任何「AI 提效后变更量翻倍」的团队都成立；门槛是会话与版本元数据要打通。"),
    },
]})

# ---------------- infra sections ----------------
infra_cats = [
    {"label": "🤖☸️ K8s × AI", "items": [
        {
            "title": "Kueue v0.21.0-rc.1：DRA 优先级列表与可消费容量配额升 Beta，拒收受管的 LWS groupIdentity: Hash",
            "url": U("kueue/releases/tag/v0.21.0-rc.1"),
            "source": "GitHub Releases", "oss": True,
            "summary": "rc.1 把两个 DRA 特性推到 Beta：KueueDRAIntegrationPrioritizedList 默认开启，调度时会把 firstAvailable 请求的 CEL 选择器与集群实际设备比对；consumable capacity 配额也升 Beta，DeviceClass 的容量维度可以用独立配额资源计费，请求取整导致多收费时会报告。另一处是准入收紧：受 Kueue 管理的 LeaderWorkerSet 用 spec.groupIdentity: Hash 会被直接拒绝——此前该模式下 leader Pod 绕过准入、worker 一直被门控。Helm 增加 managerConfig.structuredOverrides，可在不复制整份配置的前提下改 manager 设置。",
            "detail": it3(
                "让 DRA 的设备申请进入 Kueue 的配额与优先级体系（含按设备容量维度计费、取整多收费提示），并堵上 LWS 的准入漏洞。",
                "GPU 用 DRA 申请后配额仍按整卡计数，与实际可切分容量对不上；LWS 的 Hash 模式让部分 Pod 绕过队列，等于配额失效。",
                "用 DRA + Kueue 做 GPU 配额的话值得上 rc 验证：升级要同时处理 feature gate——关 KueueDRAIntegration 必须一并关 ConsumableCapacity 与 PrioritizedList，否则 controller 起不来。"),
        },
    ]},
    {"label": "☸️ K8s 核心技术", "items": [
        {
            "title": "Argo CD 的 self-heal 会跳过 Sync hook：5 个 region 里 2 个没跑迁移，36–44 分钟跑的是新代码",
            "url": U("argo-cd-self-heal-skipped-the-migration-hook"),
            "source": "CNCF Blog",
            "summary": "一篇 CNCF 博客复盘了真实现象：发布时 5 个 region 的 Application 同时上线同一 commit，3 个跑了数据库迁移、2 个没跑，新代码随后 36–44 分钟里一直报错——而 UI 上这两个 Application 显示 Synced + Healthy、「successfully synced (all tasks run)」。根因是两种刷新在抢：level-2 刷新来自约 2–3 分钟一次的 reconcile 定时器、会完整比对 Git；level-1 刷新由被管理对象变化触发、复用控制器已知状态。deny window 关闭时没有任何事件通知，先到的 level-1 被当成「修漂移」处理，而修漂移从不执行 hook。作者用最小复现（一个 Application + Sync hook Job + 四分钟 deny window）在 6 次里复现 5 次，并指出控制器日志里那次操作只列了 13 个资源、self-heal 计数为 1。",
            "detail": it3(
                "解释「同步成功但 hook 没跑」的竞态：self-heal 走 level-1 刷新时只修漂移、不执行 Sync hook，而 UI 与 last operation 都显示成功。",
                "把迁移放在 Sync hook 又开 self-heal 的团队会遇到「部分 region 迁移没跑、代码却已上线」，排查时被绿色状态误导，事故窗口被拉长。",
                "必读类：作者给了可复现的最小实验，读完能自己判断该改成 PreSync/PostSync 显式 hook、还是关掉 self-heal 或调整 deny window 策略。"),
        },
    ]},
]

# ---------------- flash ----------------
flash = [
    {"title": "Azure Firewall for Containers 进入公共预览：把防火墙策略延伸到容器化工作负载", "url": U("azure.microsoft.com/updates?id=581963"), "source": "Azure Updates"},
    {"title": "Google Cloud 给 data agent 造「风洞」：用可复现的仿真仓库替代生产数据做测试", "url": U("a-data-simulator-to-test-agents"), "source": "Google Cloud"},
    {"title": "Levent Alpöge 称与 Claude 合作给出黎曼猜想证明，尚无同行评议", "url": U("simonwillison.net/2026/Nov/20/levent-alpoge"), "source": "Simon Willison"},
]

sections = []
for group_label, cats in (("🤖 AI 板块", ai_cats), ("☸️ 基础设施板块", infra_cats)):
    out_cats = []
    for c in cats:
        if not c["items"]:
            continue
        for item in c["items"]:
            assert item.get("title") and item.get("url") and item.get("summary"), item
            assert len(item["detail"]) == 3, item["title"]
        out_cats.append({"label": c["label"], "title": c["label"], "emoji": EMOJI[c["label"]], "items": c["items"]})
    if out_cats:
        sections.append({"label": group_label, "categories": out_cats})

lead = ("今天最实用的一条落在沙箱上：Kubernetes 原生的 Agent Sandbox 把 suspend/resume 补齐到三个 SDK，挂起时释放 Pod、保留 claim 与持久卷——空闲 agent 会话不再只能靠删沙箱省钱。"
        "模型侧 Thinking Machines 放出 Inkling 2 Mini，用「中间层重复三遍」的循环 Transformer 在 100B 以下做到 DeepSWE v1.1 48.2%，还能跑在笔记本上；一篇论文则让 27B 模型自己改写自己的权重，未见题目 +6.6 点。"
        "落地案例有两条：Architect Labs 用 agent 群从零设计出通用 CPU（ISA 到 GDS 全链路），Google 则演示了 Airflow agent 如何在没有 traceback 的 OOM 事故里，把 worker 内存指标和重试记录对上再给修法。"
        "基础设施侧 Kueue rc.1 把 DRA 优先级列表与可消费容量配额推到 Beta；CNCF 一篇复盘值得所有用 Sync hook 跑迁移的人看——Argo CD 的 self-heal 会跳过 hook，5 个 region 里 2 个就这么漏了迁移。")

brief = {
    "brand": "AI & 基础设施早报",
    "date_label": "2026 年 11 月 21 日 · 星期六",
    "issue": 61,
    "kicker": "AI & INFRASTRUCTURE DAILY · NO.061",
    "hint": "👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
    "lead": lead,
    "highlights": highlights,
    "sections": sections,
    "flash": flash,
    "footer": "由 Hermes 自动汇编 · 每日 08:30 更新",
}

json.dump(brief, open(os.path.join(REPO, "briefing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = len(highlights) + sum(len(c["items"]) for s in sections for c in s["categories"])
print("wrote briefing.json | items:", n, "| flash:", len(flash), "| sections:", [(s["label"], [(c["label"], len(c["items"])) for c in s["categories"]]) for s in sections])
