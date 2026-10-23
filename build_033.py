#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 033 (2026-10-23).
URLs are looked up from processed.json by exact string; the script asserts every
URL exists there (machine-copied, never hand-typed)."""
import json, sys

PROC = {it['url']: it for it in json.load(open('processed.json'))}


def U(u):
    if u not in PROC:
        raise SystemExit(f'URL NOT IN processed.json: {u}')
    return u


def item(title, url, summary, tag, source, detail, oss=False):
    return dict(title=title, url=U(url), summary=summary, tag=tag, source=source,
                oss=oss, detail=[{'key': k, 'value': v} for k, v in detail])


# ---------------------------------------------------------------- highlights
highlights = [
    dict(
        title="Anthropic 把 Agent Skills 捐给 AAIF：skill 规范交给 Linux Foundation 托管，MCP 之后第二个",
        url=U("https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation"),
        summary="Anthropic 宣布把 Agent Skills——给 agent 提供专门知识与流程的开放标准——捐给 Agentic AI Foundation（AAIF）。AAIF 是去年由 Anthropic、Block、OpenAI 共同创立、挂在 Linux Foundation 下的基金会，MCP 规范此前已捐到同一处；官方理由是让 skills 保持「开放、社区驱动、厂商中立」。Simon Willison 当天写链接帖，翻出自己去年 12 月的判断（当时就推断 skills 会进 AAIF，因为 MCP 已先去），并提到他是用自己博客的 datasette-mcp 让 Claude 检索旧文才翻到这段预测的。",
        note="🔎 新闻要点：Agent Skills 标准捐给 AAIF（Linux Foundation 下、Anthropic/Block/OpenAI 共同创立）；MCP 规范此前已捐入同一基金会；官方措辞为「开放、社区驱动、厂商中立」；规范治理与后续演进转入基金会流程。",
        tag="Agent 标准",
        source="Anthropic News",
        detail=[
            {'key': '能做什么', 'value': '把 skill 的格式定义、兼容性预期与演进决策从单一厂商手里挪到中立基金会：第三方 agent 平台、IDE、运行时可以按同一份规范实现 skill 加载与披露，不必跟随某家的产品节奏；对已经按 skill 组织提示词与工具的项目，规范归属变化意味着长期兼容性有了外部约束。'},
            {'key': '解决什么痛点', 'value': 'agent 生态最大的隐性成本是「标准随时被上游改」——skill 目录结构、frontmatter 字段、渐进式披露语义都由单一厂商定义时，投入越多越被动。基金会托管把这类风险转成可参与的治理流程。'},
            {'key': '值不值得', 'value': '值得跟的是治理结构而不是新闻本身：短期规范不会有实质变化，真正要看的是 AAIF 的技术委员会席位、版本兼容策略与认证机制。风险在于基金会治理通常比单一厂商慢，且 MCP 的先例说明「捐出去」不等于生态自动统一。'},
        ],
    ),
    dict(
        title="Google 详解 Agent Compute Engine：每个 agent 一个微 VM，沙箱内零凭证、无网卡，空闲时 checkpoint 到零资源",
        url=U("https://cloud.google.com/blog/topics/ai-infrastructure/agent-compute-engine-deep-dive/"),
        summary="Google Cloud 首次系统讲 Agent Compute Engine 的设计：每个 agent 会话跑在一个单租户 microVM 里，启动是容器速度、隔离是 hypervisor 级，从而同时满足「要 root 与完整运行时」和「不能信任里面跑的模型」两个要求。安全模型是「假设攻击者已完全控制沙箱」——microVM 内没有任何持久凭证（无 API key、OAuth refresh token、服务账号密钥），不能访问云实例 metadata server，只拿一张 session 级 SPIFFE 证书和短时 token；沙箱没有标准网卡与默认网关，所有流量走 virtio-vsock 到本地无特权代理，再到节点外的 Agent Gateway。成本侧靠「空闲即近零」：agent 大部分时间在等模型或等人，运行时一旦进入 thinking 阶段就 checkpoint，唤醒时 restore，配合 DAX 直映射 + Copy-on-Write 共享基础镜像的物理页，官方称单机能承载比传统 VM 多几个数量级的存活 agent。",
        note="🔎 新闻要点：每会话一个单租户 microVM；沙箱零凭证 + 无 metadata server 访问 + 无标准网卡（仅 virtio-vsock → 本地代理 → Agent Gateway）；四种身份（用户 / 用户授权的 OBO 委托 / SPIFFE agent workload / agent 自有 workforce），网关校验「用户委托 + agent 身份 + 节点身份」三元组并做在途 token 替换；Titan + Titanium IPU 承载硬件根信任，宿主机 dm-verity 只读根文件系统、无持久状态；空闲 checkpoint、DAX + CoW 共享页面。",
        tag="Agent 沙箱",
        source="Google Cloud",
        detail=[
            {'key': '能做什么', 'value': '给每个 agent 会话一套「真电脑 + 保险箱」：完整 root、语言运行时、浏览器、持久磁盘，同时保证沙箱里拿不到任何能横向移动的凭证；出网请求在离机网关处才被注入真实后端凭证（in-flight token swap），并按用户委托、agent 身份、节点身份三元组做 egress 与 DLP 判定。平台侧还能做快照、fork、rewind、rollback，让一个 harness 并行开多个实验分支而不复制整份镜像。'},
            {'key': '解决什么痛点', 'value': '直接打在「多用户 × 每用户多会话」的沙箱成本与安全上：常规 VM 启动秒到分钟级、每会话独占 CPU/内存，而 agent 大部分时间在等模型；容器共享内核又快又轻，但跑不可信代码（coding agent、浏览器操作）时隔离不够、也没法给 root。ACE 的解法是把「快」和「隔离」分开取：microVM 保隔离，checkpoint/restore + 页共享保密度。安全侧则解决凭证外泄这个真实攻击面——提示注入让 agent 去偷 key 时，箱子里本来就什么都没有。'},
            {'key': '值不值得', 'value': '这是目前公开材料里最完整的一份「agent 沙箱该怎么造」的架构说明，值得细读的是三块：身份四分法与网关三元组校验、零凭证 + vsock 出网的可信边界、空闲 checkpoint 与 DAX/CoW 的成本模型。限制也很清楚：强绑 Google Cloud 的 Titan/Titanium 与 Gemini 平台治理组件，自建只能借鉴设计而非复用实现；且公开内容均为厂商自述，没有第三方压测数据。'},
        ],
    ),
]

# ---------------------------------------------------------------- AI 板块
agent_items = [
    item(
        "claude-howto 冲上 GitHub Trending 首位：给 Claude Code 补一份「按依赖顺序学」的模板库，4.3 万星",
        "https://github.com/luongnv89/claude-howto",
        "luongnv89/claude-howto 是 MIT 协议的 Claude Code 教程库，用 Mermaid 图与可复制模板把 slash 命令、hooks、记忆、subagent、skills、MCP 串成有先后顺序的学习路径，按「15 分钟入门 → 按角色进阶」组织，另附 CATALOG.md 全量特性索引；仓库目前 43,194 stars，README 提供中英日越乌克兰五语版本，标注对应 Claude Code 2.1+、自身版本 2.1.302。它明确针对官方文档「讲特性但不讲怎么组合」的缺口，示例从 hello-world 级升到带记忆、子代理与安全扫描的 code review 流水线。",
        "Claude Code 教程", "GitHub Trending",
        [('能做什么', '把 Claude Code 的能力按依赖关系排成路径（命令 → hooks → 记忆 → subagent → skills → MCP），每步给流程图和可直接拷进项目的模板，并说明哪些功能该组合使用、组合后解决什么场景。'),
         ('解决什么痛点', '官方文档是特性参考而不是工作流教材：工程师知道某功能存在，却不知道先学哪个、怎么把 hooks 与 subagent、记忆串成生产级流水线，结果大面积功能闲置。'),
         ('值不值得', '适合当团队 onboarding 材料的底稿，省掉自己写内部教程的时间；但它是第三方仓库、跟上游版本漂移快（自称对应 2.1+），涉及公司内部规范与凭证的模板必须自己重审后再用。')],
        oss=True,
    ),
    item(
        "紫荆智康「AI 医院」升级多分身协同：多专科医生分身同时坐诊，意见冲突在界面上高亮",
        "https://www.qbitai.com/2026/10/504734.html",
        "清华 AIR 孵化的紫荆智康把「多学科人类-Agent 协同」做进门诊流程：医生照常问诊，系统从患者持续补充的信息里识别需要哪些专科参与（例如甲亢患者提到哮喘史就引入呼吸科分身），以提醒方式把对应分身意见呈现给医生；对已明确需要 MDT 的病例，多个分身直接围绕诊断、用药给建议，系统分别展示各分身意见并高亮不一致之处，医生能看到意见来自哪个分身再结合依据做最终判断。平台对标的是微软 Healthcare Agent Orchestrator 这类医疗智能体编排系统。",
        "多智能体", "量子位",
        [('能做什么', '把多学科会诊从「挂多个号再凑一次 MDT」变成门诊过程中的实时旁路：分身按患者新信息被动触发、并行给意见，界面保留每个意见的来源与分歧点，形成可追溯的决策建议链。'),
         ('解决什么痛点', 'MDT 在现实里是稀缺资源——患者要跑多个科室、等会诊排期，疑难重症之外基本享受不到；而单一大模型给建议时会掩盖科室间分歧，医生无法判断该信哪一条。'),
         ('值不值得', '值得看的是「分歧显式化 + 来源可追溯」这个交互设计，它比「AI 替代医生」的叙事务实得多；但它属于厂商案例、没有公开的对照数据（准确率、误诊率、医生采纳率），医疗场景的合规与责任边界也未展开，短期更适合当产品形态参考。')],
    ),
]

eng_items = [
    item(
        "GitHub 用 AI 把 Copilot 运行时从 TypeScript 重写成 Rust：83 万行、14.5 周，启动交互 5.25s → 292ms",
        "https://www.infoq.cn/article/zGqDWHF8tHDtlYcImAJS?utm_source=rss&utm_medium=article",
        "GitHub 把 Copilot CLI、Copilot 应用与 Copilot SDK 背后的运行时从 TypeScript/Node.js 迁到 Rust，AI 辅助重写替换超过 80 万行代码，耗时约 14.5 周、128 个 PR，迁移期间照常发版（共 135 个版本，35 稳定 + 100 预发布）。客户端启动、会话创建与单轮交互从 5.25 秒降到进程内嵌入后的 292 毫秒；旧实现依赖 Node 与 V8、靠进程边界与宿主通信，每个客户端约多 100MB 工作集内存。最终运行时含 832,378 行生产 Rust 与 468,689 行 Rust 单测，临时 N-API 兼容层移除前有 2,019 个导出、3,356 处 TypeScript 调用点，4,478 次 cargo check 中 87.1% 一次通过。",
        "AI 重构", "InfoQ中国",
        [('能做什么', '给出了「用 agent 大规模重写生产运行时」的可核查流程：增量替换而非一次性切换，每换一个组件用临时 N-API 互操作层桥接，使既有端到端测试在新旧混合状态下仍可跑；Rust 侧通过 C ABI 直接嵌入宿主应用，也保留独立进程模式，SDK 覆盖 TS/Python/Go/.NET/Java/Rust 六种语言。'),
         ('解决什么痛点', 'Node/V8 + 进程边界带来的启动 5.25 秒与每客户端约 100MB 工作集，对「随手唤起」的 CLI/IDE 集成是硬成本；而一次性重写 80 万行在多团队并行发版的仓库里几乎不可能。'),
         ('值不值得', '这是目前最值得复盘的 AI 重构样本：真正的方法论是「AI 生成 + 编译/测试/人工评审兜底」和「增量集成保住测试」，而结论同样重要——取消、重试、背压这类行为回归编译期查不出来，社区质疑正集中在边界行为。若要复用到自研 agent 运行时，先按季度估迁移成本，再决定是否值得。')],
    ),
    item(
        "Snowflake Cortex AI Gateway 公测：单端点收口模型与 MCP 工具，动态路由把 dbt 流水线 token 效率提到 3 倍",
        "https://www.infoq.cn/article/v85ey09UlxhCDH4r3RS3?utm_source=rss&utm_medium=article",
        "Snowflake 的 Cortex AI Gateway 进入公开预览，定位是企业 AI 技术栈的集中控制面：一个端点代理 OpenAI、Grok、GLM、Gemini、Llama、Mistral、DeepSeek（Chat Completions）与 Claude（Messages API），流式、工具调用、结构化输出、prompt 缓存、图像输入与推理都按原生语义透传，客户端只需换 base URL 和一个 token（如 `snow ai opencode` 一条命令接管 OpenCode 流量）。访问控制复用 Snowflake RBAC，管理员决定哪些模型可被调用；私有预览中的动态模型路由按 agent 每一步选「能可靠完成且最便宜」的模型，内部评测里 dbt Pipeline 负载在质量相当下 token 效率最高 3 倍，另一项编程测试在 PR 吞吐不变的前提下 token 用量降约 25%。",
        "AI Gateway", "InfoQ中国",
        [('能做什么', '把「谁在调哪个模型、调了什么、花了多少」收进一个控制面：统一端点 + 统一凭证 + 统一计费归因，同时代理模型调用与 MCP 工具调用，并在每步做成本感知的模型选择；平台团队管策略，应用团队只对接一个端点。'),
         ('解决什么痛点', '企业 AI 技术栈碎片化的典型症状是访问路径爆炸——每个 agent、每个脚本各自持有 provider 凭证、各自出账、各自记日志，导致模型调用不可见、成本不可归因、权限不可收紧；而收紧权限又会把人推向未批准的影子 AI。'),
         ('值不值得', '方向对得上任何要做「多模型 + 多 agent」治理的平台：把 gateway 做成控制面而不是简单代理，是能同时解决可见性、成本与合规的少数位置。限制是要接受 Snowflake 作为控制面（绑定其账号与 RBAC），且动态路由还是私有预览、3 倍/25% 都是厂商内部评测。')],
    ),
    item(
        "Qwen 团队的 FlashQLA：把 GDN 线性注意力的四算子融成一个，用序列并行补上并行度短板",
        "https://www.infoq.cn/article/o9OcWNkkwgKvsZmgY45d?utm_source=rss&utm_medium=article",
        "阿里 Qwen 团队在 AICon 2026 深圳站讲了 FlashQLA——面向 GDN（Gated Delta Network）线性注意力的高性能 GPU 算子库。主流模型已转向「线性注意力 + softmax」混合架构（Qwen 三层 GDN 配一层 softmax，Kimi K3 用三层 KDA 配一层），但 GDN 的 chunk 递推有强数据依赖：每个注意力头只能开一个 CTA、占一个 SM，而 Qwen 小模型的线性注意力头数约 32、H100/GB 系列有上百个 SM，利用率被卡死；同时 FLA 的四算子实现会把 W/U/S 中间量反复写回 HBM，纯耗带宽。FlashQLA 用 WY representation 把递推改成 chunk=64 的矩阵乘，利用「相邻 chunk 状态差可由 dK×dK 矩阵递推」的性质做序列并行矫正，再用手写 warp specialization 替代 Triton 编排流水线。",
        "推理算子", "InfoQ中国",
        [('能做什么', '把线性注意力的 prefill 从「逐 token 递推」变成可并行的 chunk 矩阵乘：序列切开后各段独立算矫正矩阵，最后一次乘法完成矫正；算子融合后不再把 W/U/S 落 HBM；warp specialization 让矩阵乘、递推、输出三阶段按硬件单元分工流水。'),
         ('解决什么痛点', '混合架构把大部分层换成线性注意力，本意是省掉 O(N²)，但实现层面撞上并行度（头数 32 vs 上百 SM）与带宽（中间量往返 HBM）两个瓶颈，长序列 prefill 反而跑不满卡，也让 TP 切分更难。'),
         ('值不值得', '对自建推理栈的人是硬货：它解释了为什么同样的 GDN 模型在不同 kernel 实现上差几倍，以及序列并行并不是「切完再拼」那么简单。门槛在工程——手写 CUDA 级别的 warp specialization 需要团队有能力跟上游 kernel 演进，且结论强绑 Hopper/Blackwell 这一代硬件。')],
    ),
    item(
        "Open WebUI v0.12.3：聊天端到端加密（MLS）落地，Redis 流式改为按 key 追加",
        "https://github.com/open-webui/open-webui/releases/tag/v0.12.3",
        "Open WebUI v0.12.3 最实质的改动是把 DM 与私有群聊的端到端加密做成产品功能：成员在频道菜单发起 Encrypted Chat，消息在浏览器内用 MLS 加密、单条上限 16 KiB、只经服务器透传不落库，离开或刷新即清空，成员与权限变化时自动结束，参与者可互验短码；管理员在 Admin Settings 开启并受新的 Encrypted Channels 权限控制，要求 HTTPS 且关闭 websocket 服务端日志。另有 Redis 流式优化（每条回复独立 key 追加，不再重写共享 hash；每个实例只订阅本机用户的 room）、Google Drive 改为只申请用户挑选的文件权限（从而免掉受限 scope 审核）、以及给 skill 加读取上限（SKILL_CONTENT_MAX_CHARS 默认 20000、预览 5000）。",
        "自托管", "GitHub Releases",
        [('能做什么', '给自托管 LLM 前端补上两块企业常问的能力：一是 MLS 组密钥的端到端加密会话（服务器只转发密文，不落库），二是 skill 注入的字符预算控制，避免长 skill 一次吃掉上下文；顺带把 Redis 流式与共享搜索做轻。'),
         ('解决什么痛点', '自托管场景里「聊天要能证明服务器看不到」是硬需求，但多数前端只有 TLS 没有 E2E；另一个真实痛点是 skill/知识文件越写越长，模型每次全量读入既费 token 又挤掉对话预算，需要按字符设上限。'),
         ('值不值得', '如果你在用 Open WebUI 做团队入口，这个版本值得升：E2E 加密与 skill 读取上限都是能立刻用上的增量，升级风险主要在反向代理需支持 websocket 且要关服务端日志。注意 E2E 只覆盖临时会话（离开即清空），不是持久加密存档。')],
        oss=True,
    ),
]

model_items = [
    item(
        "中国电信开源 Xing4.0-29B-Intent：意图理解 + 参数抽取一个模型做完，输出几十 token、百毫秒级",
        "https://www.qbitai.com/2026/10/504832.html",
        "星辰通用人工智能实验室开源意图理解专用模型 Xing4.0-29B-Intent，同时放出 275 万条训练语料、模型权重与推理镜像。它把「做选择题」（类型化决策）和「做填空题」（参数抽取）合成一个任务，用 USP（统一 Schema 驱动语义解析）以「类别 + 参数」层级输出 JSON——「把卧室的灯调成暖黄」直接给出房间、设备、目标状态，一句话含多意图、多参数、多实体也能一次解析。相比通用模型先长篇推理再解析，它只输出决策所需字段，平均几十 token、完整响应百毫秒级；评测从 48 个中英文公开数据集抽 6000 题，覆盖意图理解、实体识别、关系抽取、事件抽取，已在电信万号客服、智能家居音箱上做工单路由与口语指令解析。",
        "意图理解", "量子位",
        [('能做什么', '把「自然语言 → 业务系统可执行的结构化参数」做成单次前向：统一 schema 约束字段与类型，输出可直接校验的 JSON，异构任务（意图/实体/关系/事件）共用一套输入输出格式，下游接入与迁移成本低。'),
         ('解决什么痛点', '高频业务调用里用通用大模型做分类与抽取，既贵又慢：长推理对「工单转给谁」这类问题毫无意义，自由文本输出还要下游解析纠错，同一问题能出现十种说法。'),
         ('值不值得', '对客服、工单、IoT 指令这类「场景收敛、选项固定、调用量大」的场合，专用意图模型确实比通用模型划算，且这次连语料都开源了，可以直接微调。限制是 29B 的自托管成本与长尾意图的泛化——先拿自家真实话术做一版评测再决定，不要只看公开数据集分数。')],
        oss=True,
    ),
    item(
        "Quant-Arena：A 股真实数据上的端到端量化研究基准，9 个前沿模型没一个跑赢等权市场",
        "https://huggingface.co/papers/2610.30113",
        "Quant-Arena 把量化研究的完整闭环作为评测对象：模型自己构造特征与选股代码，只在 2022–2023 数据上获得反馈，然后必须冻结一个策略，在封存的 2024 年上评估。评估器是现金账户模拟，计入交易约束、成本以及由模拟订单簿估算的市场冲击；分数以已实现的超额收益为主，辅以信号质量与策略所用特征的多样性。九个前沿模型中 GPT-6 Astra 得分最高，但在 2024 年没有任何模型跑赢等权市场；榜单对外开放，任何模型或 agent harness 都可提交。",
        "量化 Agent 基准", "HuggingFace Papers",
        [('能做什么', '把「LLM 能不能做量化研究」从主观 demo 变成可复现的协议：固定可见区间与封存年份、冻结策略防过拟合、按真实交易约束结算，并对特征多样性单独计分，避免所有模型收敛到同一批因子。'),
         ('解决什么痛点', '现有基准只测公式、代码或单笔交易决策，无法回答「这个 loop 跑完能否产出在样本外有效的策略」；而量化研究恰恰是全流程问题，任何一步（特征、回测、取舍）出错都会让样本外失效。'),
         ('值不值得', '对量化从业者这是少见的「说真话」的基准：结论（无模型跑赢等权）比任何正向结果都更有信息量，且协议本身可以直接借用来做内部 agent 评测。限制是单市场（A 股）、单一年份（2024）、市场冲击来自模拟订单簿，绝对结论不宜外推；另外它是 arXiv 预印本，未经同行评审。')],
    ),
]

biz_items = [
    item(
        "蚂蚁数科发 LingDT-Decision-1.0：4B/27B 决策模型，客服场景 token 降 90%、风险识别 76%→89%",
        "https://www.infoq.cn/article/wyGrRsTrfHM7i9MhuV5P?utm_source=rss&utm_medium=article",
        "蚂蚁数科发布决策模型 LingDT-Decision-1.0，提供 4B 与 27B 两档，面向智能客服、安全风控、金融等企业场景，处理意图识别、任务分类、工具选择与风险判断这类结构化决策，已上线 DTMaaS 平台限时免费体验。官方数据：数据标注场景相比 DS-V4-flash token 消耗降约 97%、速度提升约 10 倍；智能客服场景相比 Qwen-3.7-flash token 降约 90%、风险识别准确率从 76% 提升到 89%；23 项开源基准上 27B 版综合评分超过 Microsoft-Decision-1、Jev 1.13.0 与 Fastino/GLiDE。除单选/分类评级外还加了原生多选与按序决策，用于复合意图与存在依赖关系的任务链。",
        "决策模型", "InfoQ中国",
        [('能做什么', '把「先自由生成再解析」的环节换成在候选里直接判断：输出受预定义 schema 约束、可校验，支持多选与按序决策（识别哪些任务可并行、哪些必须等前置条件），并能给出工具组合选择，便于直接驱动下游执行。'),
         ('解决什么痛点', '高频业务里通用模型的 token 成本与延迟被成倍放大，且自由文本输出让下游难以稳定解析；金融/客服又要求判断可审计、口径一致。'),
         ('值不值得', '与星辰 Xing4.0-Intent 是同一趋势的两条样本：专用决策/意图模型在企业高频环节替代通用大模型。值得关注的是它把「按序决策」做进模型，这对多步工单编排有实际意义；但所有数字都是厂商自测（且对比对象是 flash 级小模型），选型必须用自家场景复测，同时注意 27B 的部署成本。')],
    ),
    item(
        "Claude 上 Google Cloud 多了一条 Anthropic 自营通道：GA 后按「谁做数据处理器」二选一",
        "https://cloud.google.com/blog/products/ai-machine-learning/expanding-claude-availability-on-google-cloud/",
        "Google Cloud 宣布 Claude 模型的 Anthropic 托管部署选项 GA，与原有 Google 托管选项并列：两者同样 day-zero 拿到前沿模型、同样价格、同样走 Google Cloud 账单，差别在谁当数据处理者以及能否第一时间用到 Claude Platform 新特性。Anthropic 托管版由 Anthropic 作为数据处理者、跑在 Google Cloud 基础设施上并按 Anthropic 条款，企业仍用 Google Cloud IAM 认证、保留 Cloud Audit Logging、花费并入既有账单与承诺，该通道可 day-zero 用到 Claude Managed Agents（beta）、skills、code execution；Google 托管版仍是 Google 做数据处理者，提供 VPC Service Controls、CMEK 与美/欧/亚太数据驻留，但新特性要等集成进 Google 侧。",
        "模型供给", "Google Cloud",
        [('能做什么', '让同一批 Claude 模型在同一个云上有两种合规形态：要「紧跟 Anthropic 新平台能力」选 Anthropic 托管，要「数据不出一等公民边界（VPC-SC / CMEK / 数据驻留）」选 Google 托管，认证与账单都统一在 Google Cloud 侧。'),
         ('解决什么痛点', '金融等强合规行业长期卡在「想用最新模型能力」与「数据处理者必须是已签合同的云厂商」之间；此前只能二选一，或者走第三方中转丢掉审计与承诺抵扣。'),
         ('值不值得', '对正在做模型接入合规评审的团队是直接可用的论据：把「数据处理者」从技术细节提升为采购选项后，同一模型的两种路径可以按业务线分别落地。注意 Anthropic 托管下数据处理者变成 Anthropic，DLP/驻留要求高的场景仍应走 Google 托管，代价是新特性滞后。')],
    ),
]

sec_items = [
    item(
        "AWS Continuum 代码漏洞服务 GA：先证明可利用再修，给攻击路径与爆炸半径而不是一个分数",
        "https://aws.amazon.com/blogs/aws/aws-continuum-for-code-vulnerabilities-is-now-generally-available/",
        "AWS Continuum for code vulnerabilities 正式 GA：它把代码仓库与 AWS 环境（账号内的 collector 采集 AWS Config 资源与网络配置）合成一张上下文图，判断某个漏洞在网络与实际可达资源上是否真的可利用，并给每条结论标注证据等级；能复现的漏洞会在隔离沙箱里跑通 exploit、附 PoC 与复现步骤。输出不是 CVSS 分数，而是攻击路径、源码分析与爆炸半径评估，同时评估既有防护能否拦住这条路径；修复以代码补丁、依赖升级或 PR 形式提交，默认「提出 → 人工批准 → 才发布」，未来才允许在护栏内自主执行。",
        "安全", "AWS News",
        [('能做什么', '把漏洞处理从「按分数排队」变成「按可达性排优先级」：结合代码路径与云上资源/网络上下文证明可利用性，给出攻击链与影响范围，并生成可审的修复补丁或 PR。'),
         ('解决什么痛点', '大型应用里扫描器每天产出成千上万条告警，其中大量不可达、已被运行时控制缓解或落在仅开发环境；通用严重度分数分不清「dev 工具上的 critical」与「离支付库一跳的 medium」，人工确认可利用性要数小时、协调修复要数天。'),
         ('值不值得', '方向值得跟：把「可利用性证明 + 爆炸半径」做成服务输出，比再做一个扫描器有价值。限制是强绑 AWS 环境（collector 只能看 AWS 侧资源），非 AWS 资产等于半盲；且默认人工批准意味着它省的是分析时间而不是决策责任。')],
    ),
]

sections = [
    dict(label="🤖 AI 板块", categories=[
        dict(emoji="🧩", title="Agent & Skill", en="AGENT & SKILL", items=agent_items),
        dict(emoji="🛠️", title="AI 工程落地", en="AI ENGINEERING", items=eng_items),
        dict(emoji="🧠", title="模型与研究", en="MODELS & RESEARCH", items=model_items),
        dict(emoji="📊", title="产品与商业", en="PRODUCT & BUSINESS", items=biz_items),
        dict(emoji="🛡️", title="安全与治理", en="SECURITY & GOVERNANCE", items=sec_items),
    ]),
]

k8sai_items = [
    item(
        "Dynamo v1.6.0：Router 变可插拔流控，K8s 侧引入 LPX/LPU 与 role 级 pod 模板",
        "https://github.com/ai-dynamo/dynamo/releases/tag/v1.6.0",
        "NVIDIA 的分布式推理平台 Dynamo 发布 v1.6.0，跨 654 个 PR、148 位贡献者（其中 58 位来自 NVIDIA 之外）。Router 引入可插拔流控：请求分类器钩子可以延迟、重排或改写调度输入，所有请求走按 deadline 排序的策略队列，Frontend、独立选路服务与 Gateway API EPP 共享同一套 worker 选择核心，评分参数收进一个 --router-policy-config。Kubernetes 侧新增 LPX 把 LPU 接入 DynamoGraphDeployments、多机组件的 prefill/decode 可用各自的 leader/worker pod 模板、Dynamo Snapshot 为 SGLang 与 vLLM 做主备故障转移；Planner 可通过 /v1/min-endpoints 在运行时改 GPU 预算上下限。引擎跟进 SGLang v0.5.21、TensorRT-LLM v1.3.0rc29、vLLM v0.31.0。",
        "推理平台", "GitHub Releases",
        [('能做什么', '把推理路由做成可编程的：分类器插件决定请求要不要延后、改调度输入或直指某个 worker，deadline 驱动的队列让 SLA 与优先级可表达；K8s 侧可以用 LPU 与 GPU 混布、给 prefill/decode 不同的 pod 模板、用快照做引擎故障转移，并用 Planner 在运行时调 GPU 预算而不是重部署。'),
         ('解决什么痛点', 'PD 分离与多机部署下，长期痛点是「路由策略写死在代码里、扩缩容要重部署、引擎挂了要重建」；agent 负载又带来会话亲和与 deadline 需求，传统轮询/最少连接表达不了。'),
         ('值不值得', '做 K8s 上的 LLM 推理平台，Dynamo 是目前和 Gateway API EPP 生态结合最紧的开源栈之一：统一选路核心意味着不必自研两套路由。门槛是概念密度高（Router/Planner/Operator/Snapshot 各一套配置），且部分能力（LPX、sidecar 形态）仍是实验级，升级前先读 breaking changes。')],
        oss=True,
    ),
    item(
        "Kueue v0.20.3：MultiKueue 支持 RayService 弹性切片自动伸缩，经典抢占加了候选排序缓存",
        "https://github.com/kubernetes-sigs/kueue/releases/tag/v0.20.3",
        "Kueue v0.20.3 的功能改动集中在多集群 GPU 队列：MultiKueue 新增对 worker 集群上 RayService in-tree 自动伸缩的支持，用 elastic workload slices 表达弹性伸缩，需要开启 MultiKueueRayInTreeAutoscaling 特性门；调度侧用「复用候选排序 + 按需生成候选」改善经典抢占性能（alpha 的 ClassicalPreemptionCandidateOrderCache，默认关闭）。同时修了 ConcurrentAdmission 下父 Workload 的并发准入缺陷。",
        "GPU 队列", "GitHub Releases",
        [('能做什么', '把 Ray 的弹性伸缩语义接进 Kueue 的多集群队列：RayService 的副本伸缩以 elastic workload slices 形式表达，由 MultiKueue 在 worker 集群上准入，从而与配额、优先级、抢占统一管理；抢占路径则通过缓存候选顺序减少大集群下的重复计算。'),
         ('解决什么痛点', 'GPU 集群里 Ray 服务自己扩缩容会绕过配额与公平性，导致队列形同虚设；而经典抢占在候选多（大集群、多队列）时每次都要重算排序，成为调度延迟热点。'),
         ('值不值得', '如果用 Kueue 管 GPU 池并跑 Ray，这个补丁版解决的是「弹性与配额打架」的现实问题，值得跟；但 RayService 自动伸缩要开 alpha 特性门，先在同版本的测试集群验证伸缩与抢占同时触发时的行为，再考虑上生产。')],
        oss=True,
    ),
    item(
        "CNCF 实测：一次 Claude Code 小任务产生 181 条遥测、289KB JSON，用 Collector 双流水线砍掉大头",
        "https://www.cncf.io/blog/2026/10/22/filtering-and-reducing-ai-agent-telemetry-with-the-opentelemetry-collector/",
        "CNCF 博客给出一组实测：让 Claude Code 修两个失败测试并补边界用例，全开内容开关后一次运行产出 181 条遥测记录、289KB JSON。问题在于默认埋点是按「调试单次运行」设计的——工具内容同时落在 span event 与 log 里（一次 Write 把整个文件存两份），指标按 session.id、user.id、user.email 和两个账号 id 打标签，25 个会话就让 8 个指标膨胀到 300 条时间序列。作者的做法是在 OpenTelemetry Collector 里用同一个 OTLP receiver 扇出两条流水线（原样 vs 优化），优化侧加过滤、去重与属性上提，两条都进同一个 Grafana LGTM，用红绿两条曲线直接量出省下的存储。",
        "Agent 可观测性", "CNCF Blog",
        [('能做什么', '把 agent 遥测从「全量落库」改成「先整形再发」：在 Collector 里丢弃不承载告警/看板价值的内容字段、把高基数属性从指标上提到 resource、对重复的 span event 与 log 去重，同时保留回答「跑了哪些工具、花了多少 token、哪一步失败」所需的计数与短属性。'),
         ('解决什么痛点', 'agent 遥测天然高基数高体积：内容字段（prompt、文件体、diff）对排障有价值但对趋势分析无用，却占据绝大部分字节；session/user 级标签制造永不回收的时间序列，存储与索引成本随用量线性上涨。'),
         ('值不值得', '如果你正在给 coding agent 接可观测性，这篇给了可直接复用的对照方法（同一输入扇出两条流水线量差），比任何「降本 N%」的宣传都实在。注意它只解决管道侧整形，不解决「哪些字段该留」的治理问题——那需要先和看板/告警对齐。')],
    ),
]

k8s_core_items = [
    item(
        "Istio 1.31.3 是安全版本：修 ISTIO-SECURITY-2026-008，istiod CA 过期可自愈",
        "https://github.com/istio/istio/releases/tag/1.31.3",
        "Istio 1.31.3 随 ISTIO-SECURITY-2026-008 发布，属安全修复版本。发布说明里的两处功能修正都在 ambient 与 CA 生命周期上：node-untaint 控制器此前只要 istio-cni 就绪就摘掉 cni.istio.io/not-ready 污点，现在可以选择等 ztunnel 也就绪（PILOT_NODE_UNTAINT_CHECK_ZTUNNEL=true，该分支默认关闭），避免 pod 被调度到 ztunnel 卡住的节点；istiod 在 Deployment 缩容到零、超过证书 TTL 导致 istio-ca-secret 里的自签 CA 过期时不再启动失败，而是用现有私钥自动续期。",
        "服务网格", "GitHub Releases",
        [('能做什么', '修掉两个运维期才会暴露的坑：ambient 模式下节点过早解除 not-ready 污点导致流量落到 ztunnel 未就绪节点；istiod 长期缩容后自签 CA 过期无法启动（现在自动用私钥续期，无需人工重建 secret）。'),
         ('解决什么痛点', '前者造成「pod 起来了但流量黑洞」，排查方向容易误判到 CNI 或应用；后者会让「按需缩容省钱」的策略在恢复时直接卡死控制面。'),
         ('值不值得', '跑 ambient 的集群建议跟这个版本：两处都是真实故障模式的修复，且安全修复必须落地。升级注意 ztunnel 等待行为是可选开关、默认关闭，若要启用需评估节点扩容时的调度空窗。')],
        oss=True,
    ),
    item(
        "Kyverno v1.19.2：CEL 准入每个请求只构建一次 request activation，引擎上下文拷贝降本",
        "https://github.com/kyverno/kyverno/releases/tag/v1.19.2",
        "Kyverno v1.19.2 以性能与修补为主：CEL 准入路径改为每个 admission 请求只构建一次 request activation（此前按策略重复构建），并降低了引擎 context checkpoint 的拷贝开销，还给 CEL 准入路径加了分配回归闸门测试（合并后跑）。修复项包括删除命名空间内资源时的分页处理、镜像校验策略 webhook 的命名冲突、autogen 对细粒度命名空间镜像策略的生成；imageExtractors 新增 filter 字段，支持通配数组过滤。",
        "策略引擎", "GitHub Releases",
        [('能做什么', '降低准入链路的固定开销：request activation 从「每策略一次」变成「每请求一次」，checkpoint 拷贝成本下降，并用 CI 的分配回归闸门防止后续退化；imageExtractors 的 filter 让镜像提取规则能按通配数组精确筛选。'),
         ('解决什么痛点', '策略数量一多，准入 webhook 的 CPU 与分配开销会直接放大 API Server 的写延迟，甚至触发超时导致资源创建失败；这类几何级放大在策略从几十条涨到几百条时才暴露。'),
         ('值不值得', '如果集群里 Kyverno 策略数量可观（尤其 CEL 策略），这是低风险高收益的补丁版：改动集中在热路径与 bug 修复。升级后建议对比 apiserver 的 admission 延迟指标确认收益，并把分配回归测试纳入自家 CI。')],
        oss=True,
    ),
]

sections.append(dict(label="☸️ 基础设施板块", categories=[
    dict(emoji="🤖☸️", title="K8s × AI", en="K8S × AI", items=k8sai_items),
    dict(emoji="☸️", title="K8s 核心技术", en="KUBERNETES CORE", items=k8s_core_items),
]))

# ---------------------------------------------------------------- flash
flash = [
    dict(title="Envoy v1.38.8：把被攻破的 eMudhra 中间 CA 从镜像、Mobile 根证书包与 Hickory DNS 解析器里剔除", url=U("https://github.com/envoyproxy/envoy/releases/tag/v1.38.8")),
    dict(title="Argo CD v3.3.18：同一 eMudhra CA 泄露事件的 3.3 线安全补丁", url=U("https://github.com/argoproj/argo-cd/releases/tag/v3.3.18")),
    dict(title="谁在给 OpenAI 供应具身数据？", url=U("https://www.qbitai.com/2026/10/504800.html")),
]

brief = dict(
    brand="AI & 基础设施早报",
    date_label="2026 年 10 月 23 日 · 星期五",
    issue=33,
    kicker="DAILY",
    hint="👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
    lead="今天最值得看的两件事都在「给 agent 造地基」。Google 首次公开 Agent Compute Engine 的完整设计：每个 agent 会话一个硬件隔离的微 VM，箱内零凭证、没有网卡，空闲时 checkpoint 到零资源——把「隔离」和「密度」这对矛盾分开解决。另一条是标准层面的：Anthropic 把 Agent Skills 捐给 Linux Foundation 下的 AAIF，skill 的演进从此有中立托管方。评测侧则有一份冷水：Quant-Arena 用 A 股真实数据做端到端量化研究基准，九个前沿模型没一个在封存的 2024 年跑赢等权市场。基础设施侧，Dynamo v1.6.0 把路由做成可插拔流控并接入 LPU，Kueue、Istio、Kyverno、Open WebUI 各有一个值得跟的版本。",
    highlights=highlights,
    sections=sections,
    flash=flash,
    footer="由 Hermes 自动汇编 · 每日 09:00 更新",
)

# ---- assertions: every item has a non-empty title & detail
def check(items, where):
    for it in items:
        assert it.get('title'), f'missing title in {where}'
        assert it.get('url'), f'missing url in {where}'
        assert it.get('detail') and len(it['detail']) == 3, f'bad detail in {where}: {it["title"][:40]}'


check(highlights, 'highlights')
n_items = len(highlights)
for s in sections:
    for c in s['categories']:
        check(c['items'], c['title'])
        n_items += len(c['items'])

json.dump(brief, open('briefing.json', 'w'), ensure_ascii=False, indent=1)
print(f'briefing.json written: {n_items} content items + {len(flash)} flash')
