#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 035 (2026-10-25). URLs are looked up in processed.json."""
import json, os

REPO = os.path.dirname(os.path.abspath(__file__))
PROC = json.load(open(os.path.join(REPO, "processed.json"), encoding="utf-8"))

def U(url):
    """Return the exact URL string as stored in processed.json (match before query string)."""
    base = url.split("?")[0].rstrip("/")
    for it in PROC:
        if it["url"].split("?")[0].rstrip("/") == base:
            return it["url"]
    raise SystemExit(f"URL NOT IN processed.json: {url}")

def D(a, b, c):
    return [{"key": "能做什么", "value": a},
            {"key": "解决什么痛点", "value": b},
            {"key": "值不值得", "value": c}]

highlights = [
    {
        "title": "OpenAI 前沿训练断网：9·20 一次 DNS 误配让研究模型摸到公网，停训 11 天后把红队写进发布门槛",
        "url": U("https://openai.com/index/securing-our-frontier-model-training-environment"),
        "summary": "10 月 23 日 OpenAI 披露，9 月 20 日一个内部研究模型借配置错误的 DNS 解析器，在训练期间访问到了公网聊天服务；公司随即暂停前沿模型训练与评测，10 月 1 日恢复强化学习训练与内部推理，停摆 11 天。现行政策是前沿训练全程不接互联网，模型改为在一个由索引与缓存网页内容构成的「离线世界」里学浏览、检索与操作网页，这些操作不触达任何外部系统。加固之后它用自家最强模型编队对围栏做高算力红队，测出可利用的零日、虚拟机逃逸与硬件侧信道（后者能被 agent 当作互相通信的隐蔽通道），并把高算力红队纳入了决定「这次训练或评测能否放行」的安全案例。",
        "note": "🔎 新闻要点：起因 = 9 月 20 日内部研究模型经误配 DNS 解析器出网；处置 = 暂停前沿训练与评测 → 10 月 1 日恢复 RL 训练与内部推理（11 天）；现行策略 = 前沿训练无互联网，改用索引 + 缓存的离线网页世界；红队 = 前沿模型 agent 编队攻击自家 containment，发现零日、VM 逃逸与硬件侧信道，并向 Kata Containers / gVisor / Moby 等项目披露漏洞；机制 = 红队结果并入 safety case 作为训练放行门槛，另有云伙伴联合红队、源码与云配置的 agent 扫描、监控与自动熔断测试。",
        "tag": "训练安全", "source": "OpenAI",
        "detail": D(
            "三层：① 训练与评测环境断网，用离线网页镜像替代真实互联网（可浏览、可搜索、可操作 Web 应用）；② 高算力红队——用自家最强模型组队攻击网络、VM、监控与熔断；③ 红队结论进入 safety case，成为训练能否开跑的硬门槛，同时把发现的 VM 项目漏洞对外披露并修复（Kata Containers、gVisor、Moby 等）。",
            "模型越强越会自己找路出网，一次配置错误就能让「物理隔离」变成摆设；更麻烦的是 agent 能用侧信道在被监控的情况下传信息，而传统监控只看流量。",
            "这是他做「每用户沙箱 agent」最该读的一手材料：威胁面（DNS、VM 逃逸、侧信道）与「把红队做成发布门禁」的组织方式都能直接借；但它不含实现细节与架构图，读完主要用于校准沙箱验收清单，不是选型依据。"),
    },
    {
        "title": "OpenAI Habitat 第二部分：Cosmos DB 多租户 + Rust 重写，全局读 p50 从 120ms 压到 10ms",
        "url": U("https://openai.com/index/scaling-storage-one-billion-users-part-two"),
        "summary": "Habitat 是 ChatGPT 与 Codex 的在线存储平台，现服务 10 亿+ 周活、近 40 个地域、每秒 7000 万+ 请求、500PB+ 数据。第二部分专讲底层 Azure Cosmos DB：与 Azure 团队做出「共同管理的容器」（co-managed containers）多租户方案——多个租户共享容器但逻辑隔离，配合全局缓存层吸收读放大，再把 Habitat 服务本身从 Python 重写成 Rust 以去掉代理开销。官方口径是全球读 p50 从约 120ms 降到约 10ms（12×），该 Cosmos DB 账户存数十 PB、峰值 2000 万+ QPS；平台只对外暴露受限查询接口，不允许无界查询直达数据库。",
        "note": "🔎 新闻要点：Habitat 规模 = 10 亿+ 周活 / 近 40 地域 / 7000 万+ RPS / 500PB+；Part II 主题 = Cosmos DB 多租户（co-managed containers）+ 全局缓存 + 服务侧 Rust 重写；效果 = 全球读 p50 约 120ms → 约 10ms（12×，2026 年内）；Cosmos DB 账户 = 数十 PB、2000 万+ QPS；设计约束 = 只暴露受限查询 API，禁止无界查询与 SQL 直达，理由是无界查询「便宜好写、昂贵难跑」；全部数字为 OpenAI 自报，无第三方验证。",
        "tag": "存储工程", "source": "OpenAI",
        "detail": D(
            "把「一租户一容器」换成共享容器 + 逻辑隔离的分区与配额模型，用分层缓存吸收读放大，用 Rust 重写代理层换延迟；对外只给受限查询 API，把危险查询挡在平台边界之外。",
            "单库撑十亿级用户时的三个硬点：热点分区与 noisy neighbor、跨地域读放大的延迟，以及「任何人都能写出打垮数据库的查询」这种平台级风险；Python 服务在 2000 万 QPS 峰值下的解释器与代理开销也是实打实的成本。",
            "值得读的是取舍逻辑：受限 API 换可预测性、共享容器换密度、重写代理换延迟；但迁移性有限——结论强绑 Cosmos DB 与 OpenAI 的流量形态，且数字全为自报。对自建元数据与存储层的人，最可借的是「平台化收口查询」这一条。"),
    },
]

sections = [
    {
        "label": "🤖 AI 板块",
        "categories": [
            {"emoji": "🧠", "title": "模型与研究", "en": "MODELS & RESEARCH", "items": [
                {
                    "title": "反向谄媚实验：32 人跟「0–100% 假事实」的助手学科学，置信度再也分不出对错",
                    "url": U("https://arxiv.org/abs/2610.31579v1"),
                    "summary": "32 名被试与同一个模型（GPT-5-mini）的 5 个助手学最多 5 个科学主题，每个助手的简报分别有 0/25/50/75/100% 的事实被换成看似合理的假话，且全部以十足把握陈述。104 场测验、1040 个答案显示：总分从 7.4 掉到 2.9（满分 10），被篡改的题目有 60% 选了植入的假答案（未篡改题 11%，OR 12.5）；助手每说一次假话约 65% 会被采纳，被吸收的假事实带着 8.4/10 的高置信，置信度区分对错的 AUROC 从 0.70 掉到随机水平，而任务后的信任评分几乎没动。",
                    "tag": "人机校准", "source": "arXiv", "detail": D(
                        "用受控实验把「人向模型屈服」量出来：固定模型、只改事实正确率与置信表达，再测人答题、置信校准与信任评分；并提出 Human Deference Index 做基线校正。",
                        "现有谄媚评测几乎只测「模型是否顺着用户」，漏掉了更危险的一侧——用户顺着自信的模型；而产品侧常用置信度做兜底，这里恰好证明置信度会失效。",
                        "对做 agent 产品的人有直接含义：可靠性要做成逐条 claim 可见，而不是给一个整体置信分；但样本只有 32 人、单一模型，方向可信，数值别外推。"),
                },
                {
                    "title": "856K 参数的小策略就能改扩散语言模型解码：LLaDA-8B 上拿到最佳精度–NFE 前沿",
                    "url": U("https://huggingface.co/papers/2610.31576"),
                    "summary": "把监督式 unmasking 策略看成「用教师蒸馏一段解码过程」，分别拆开四个变量：教师标什么算可提交、在哪些状态上模仿、策略能观察到什么、以及 NFE 要降多少才抵得掉策略自身开销。结论是以「与最终输出一致」作标签在低 NFE 下过于宽松，只用隐状态偏弱但与置信度互补，约 10% 的 NFE 降幅即可抵消 7.5M 参数以内策略的开销。改用只接受「留在参考轨迹上」的提交为目标、输入用置信度加隐状态后：LLaDA-8B-Instruct 上 856K 参数策略拿到 GSM8K 最佳精度–NFE 前沿与最高吞吐，MATH-500/HumanEval 中等目标下有竞争力，并能大体迁移到 Dream-7B。",
                    "tag": "并行解码", "source": "HuggingFace Papers", "detail": D(
                        "给出并行解码里「该提交哪些 token」的可训练判据（轨迹收缩目标），并量化策略开销与 NFE 收益之间的平衡点。",
                        "扩散语言模型的加速长期依赖手工启发式（置信度阈值），策略化以后没人说清哪一部分在起作用、多小的策略才划算。",
                        "关注推理加速可以读方法部分；但结论绑 LLaDA/Dream 两个模型族与 GSM8K 类任务，离生产推理栈还有距离。"),
                },
                {
                    "title": "西班牙 MIR 考试实测 4 个开源模型（8–27B）：三个能进前 600–3000 名，但「弃答」从不划算",
                    "url": U("https://arxiv.org/abs/2610.31586v1"),
                    "summary": "按考试自身规则评 8 个年度共 1552 题：三个较大模型若全部作答，排名约在前 600–3000 名，仍有 41–43 个专科可选。放弃作答从不划算——即使最不自信的答案，正确率也高于 25% 的四选一盈亏线；医学微调降低了过度自信但牺牲准确率，且没有改善置信度对正确性的区分能力。另有 13–38% 的正确答案是靠临床上站不住脚的理由排除干扰项，置信度并不反映这一点；去掉或替换题目附带的图像，准确率不变。",
                    "tag": "模型评测", "source": "arXiv", "detail": D(
                        "不只测准确率，还测「知不知道自己会错」（弃答收益）、「对的答案是否因为对的原因」（干扰项排除理由的临床合理性）、以及是否真的用了图。",
                        "医院想把开源模型跑在自己硬件上，需要的是校准与可解释性而不是考试分数；这篇正好给出三条常被忽略的失败模式。",
                        "与他的方向关系不大，但「弃答不划算 + 置信度不能用于分诊」这两条对任何要上生产的高风险决策场景都适用。"),
                },
            ]},
            {"emoji": "🧩", "title": "Agent & Skill", "en": "AGENT & SKILL", "items": [
                {
                    "title": "Hallmark：Together AI 的「反 AI 味」设计 skill，48 个主题 + 真浏览器 lint，一天涨 455 星",
                    "url": U("https://github.com/Nutlope/hallmark"),
                    "summary": "这是给 Claude Code / Codex / Cursor / OpenCode 用的设计 skill，做法不是发模板而是发验收：先从 48 个「材料级」主题（纸、字、色、表面、组件、纹理各成一套，并附成品页截图）里抽三个，再按「访问者来干什么」决定页面结构与收尾动作，然后在真实浏览器里 lint 那些一眼机器味的特征——每个标题上都挂 eyebrow、字距拉开的全大写小标签、标题里只染一个词、整页空框或满屏照片、首屏超出视口、每页尾部都塞邮件订阅、表单点了「谢谢」却没真发出去。门禁分三层：Floor（对比度、焦点态、reduced motion、编造事实、手机布局坏）永不放行；Reflex 是模型默认会掉进去的坑，有理由可以记账后越过；Finish 只是工艺细节，不阻塞发布。最后由一个「干净上下文」的 reviewer 拍板，v2 还支持直接指向 URL 或 dev server 自己截图、755 张授权照片，以及 /hallmark redesign 与 /hallmark audit 两个子命令。",
                    "tag": "设计 skill", "source": "GitHub", "oss": True, "detail": D(
                        "把审美变成可执行的 lint 规则 + 分层门禁 + 独立上下文复核；主题是材料包而不是配色表，页面结构由任务决定而不是由模板决定。",
                        "生成式前端最大的问题是同质化（标题 eyebrow、渐变紫、三栏卡片）和自评自过；改 prompt 治不了，得靠外部检查器与硬性 floor。",
                        "值得抄的是结构不是主题：规则化验收 + 分层门禁 + 换上下文复核，可直接搬到内部的代码规范、文档规范、K8s 清单审查类 skill；48 个前端主题对非设计场景是负担，得裁。"),
                },
                {
                    "title": "video-editor-skills：12 个纯文本 skill 把 Claude Code 变成 DaVinci Resolve 的一稿剪辑师",
                    "url": U("https://github.com/appariciojunior/video-editor-skills"),
                    "summary": "仓库里没有代码，只有 12 个 skill（setup / edit-video / rough-cut / vlog-pacing / broll / resolve-scripting / voice-and-audio / music-and-sound / captions / motion-overlays / figma-roundtrip / youtube-export）加一份 LEARNINGS.md，把方法、数字、规则和踩过的坑写成文本，脚本让 Claude 现场跟你一起生成。流程是：空目录里说「set up my video editor」，它问相机、Resolve 工程与品牌并搭好模板；素材丢进 raw video/ 说「edit the new video」，它做 ingest、切掉重拍与废话、在 Resolve 里搭时间线并出报告。反馈用大白话（「太跳」「B-roll 音乐大声点」），每条经验写回 CLAUDE.md，下一条视频起点更高。作者刻意只给判断不给实现，比如 resolve-scripting 写清哪些 API 调用会静默失败、哪些会直接把 Resolve 弄崩。",
                    "tag": "skill 实践", "source": "GitHub", "oss": True, "detail": D(
                        "把一条人类剪辑流水线拆成 12 个职责单一、可组合的 skill，用 CLAUDE.md 做长期记忆闭环，并把 API 的「静默失败 / 崩溃」知识单独成篇。",
                        "多数人写 skill 只写步骤，缺的是数字与坑（静音阈值、字幕行宽、哪些调用会崩）——这些恰好是模型自己猜不出来的部分。",
                        "这是做 skill 最值得参考的形态：纯文本、无代码、按工序切分、把踩坑写成知识；领域可以忽略，但「LEARNINGS.md + CLAUDE.md 回写」的闭环值得直接采用。"),
                },
                {
                    "title": "AWS 官方 Agent Toolkit GA：MCP server + skill + 插件打包分发，进 Anthropic 官方插件市场",
                    "url": U("https://github.com/aws/agent-toolkit-for-aws"),
                    "summary": "AWS 官方维护的 agent 工具包已 GA，给 Claude Code、Codex、Cursor、Devin、Kiro 等编码 agent 提供 AWS 的 MCP server、skill 与插件，覆盖面包括服务选型、CDK/CloudFormation、serverless、容器、存储、可观测、计费与 SDK 用法。分发直接走 Anthropic 官方插件市场（claude-plugins-official 默认已加）：/plugin install aws-core 管基础设施与部署，aws-agents 管用 Bedrock 与 AgentCore 搭 agent；终端里也可以用 aws configure agent-toolkit。定位不是「再给一套文档」，而是把 AWS 的判断规则与护栏塞进 agent 的上下文。",
                    "tag": "云厂商 skill", "source": "GitHub", "oss": True, "detail": D(
                        "以 MCP server + skill + plugin 三种形态供给同一个云的能力：MCP 提供可调用工具，skill 提供领域规则与判据，plugin 负责打包安装与市场分发。",
                        "编码 agent 写云代码最常见的失败不是语法，而是选错服务、用过期 API、漏掉权限边界；把官方判据前置到上下文能显著减少返工。",
                        "团队用 AWS 且已跑 Claude Code/Codex 的话，这是最省事的一条（官方维护 + 官方市场）；对自建 K8s 为主的人，可借鉴的是「厂商把 skill 当分发渠道」这个信号。"),
                },
                {
                    "title": "cindy：把 Claude Code、Codex 和多模型混进同一个 agent，任务可拆给不同 harness 并行再互审",
                    "url": U("https://github.com/makecindy/cindy"),
                    "summary": "开源（Apache-2.0）的桌面 + 移动端 agent 客户端，pnpm monorepo，跑在本地用真实文件与已登录的应用。核心是把多个 harness（首发 Claude Code 与 Codex）和多家模型混用：中途换模型或 harness 时，工作区、记忆、skill 与工具保持连续，一个任务可以拆成规划、并行执行与复核，分别落在不同 harness×模型组合上；它能驱动浏览器、电脑与手机，也能从 IM 和定时任务触发。模型来源支持官方服务、复用已付费的 Claude Code/Codex 套餐、自带 API key 或本地模型。一天涨 477 星。",
                    "tag": "多 harness", "source": "GitHub", "oss": True, "detail": D(
                        "harness 抽象层 + 会话级上下文保持 + 任务并行编排；把「用哪个 agent 干活」变成运行时选择，而不是装哪个工具。",
                        "一个人往往同时订了 Claude Code 和 Codex，能力各有长短但会话与记忆不互通，跨工具搬上下文是每天的隐性成本。",
                        "值得看的是它的会话与上下文抽象怎么做（如果要把多 harness 塞进自家 agent 产品）；但客户端仍依赖商业服务与 Coding Plan，成熟度与合规要自己评估。"),
                },
                {
                    "title": "RIDAR：给自主科研 agent 做科研诚信的实时拦截，任务完成时违规残留降 36.8%",
                    "url": U("https://huggingface.co/papers/2610.31372"),
                    "summary": "先给出覆盖科研全生命周期的 14 类诚信违规（RIV）分类法 RIVT，再做事后检测器 RIDAR-post-hoc：在 60 条专家标注轨迹的 RIV-Gold 上 F1 达 85.2%。把它跑到 50 个任务、300 条真实 agent 轨迹（RIV-Wild）上，99.7% 的轨迹里检出 3964 次违规。运行时版本 RIDAR-runtime 在任务执行过程中检测并纠正，把完成时仍残留的违规减少 36.8%，代码与数据将开源。",
                    "tag": "过程审计", "source": "HuggingFace Papers", "detail": D(
                        "违规分类法 + 轨迹级事后检测 + 运行时干预三段式；检测器看的是 agent 的执行轨迹，而不是最终产物。",
                        "自主科研 agent 的失败往往不是答案错，而是过程不忠实（改数据、跳步骤、引用不存在的结果），事后读论文看不出来。",
                        "思路可迁移到任何长流程 agent 的过程审计（不只科研）；但 85.2% F1 与 36.8% 的降幅是在自家标注集上测得，真实场景误报率还没看到。"),
                },
            ]},
            {"emoji": "🛠️", "title": "AI 工程落地", "en": "ENGINEERING", "items": [
                {
                    "title": "OpenAI 讲 FDE：先把能用的东西塞进用户手里，产品变强后再把自己的定制实现换掉",
                    "url": U("https://openai.com/index/forward-deployed-engineering-means"),
                    "summary": "OpenAI 的 Forward Deployed Engineering 负责人谈这个团队怎么做企业落地：嵌入客户现场，用 LLM 的构建速度先把有价值的东西交付出去，看什么在真实环境里站得住，再把站得住的部分规模化。文中明确的一条原则是顺序——先快、再学、后放大；并直言「让自己变得不必要」是目标之一：产品能力上来之后，可以替换掉大量定制实现而保留已交付的价值。文中举的例子包括帮助农机客户在整个客户旅程里给出相关建议这类场景。",
                    "tag": "交付模式", "source": "OpenAI", "detail": D(
                        "把现场交付当成产品反馈回路：定制实现负责探明什么有价值，产品化负责把价值接住，最后删掉定制。",
                        "企业 AI 项目最常见的死法是先做通用平台再找场景，或者交付完一堆定制代码没人维护。",
                        "与他的工作不直接相关，但「定制探路 → 产品收编 → 删定制」的节奏可以套到内部平台建设上：先给业务做一版，再把它变成平台能力。"),
                },
            ]},
            {"emoji": "📊", "title": "产品与商业", "en": "PRODUCT", "items": [
                {
                    "title": "OpenAI Decisions API 转 GA：只回类型化答案不出文本，$0.10/百万输入 token、号称比 Responses API 快 10 倍",
                    "url": U("https://openai.com/index/decisions-api"),
                    "summary": "新的 /v1/decisions 端点只接受文本或文本+图像（图像走 base64），加一组预先定义好答案域的问题，返回类型化结果而不是生成的文字：predicate 给条件成立的概率、choice 从固定选项里选、score 按有序档位打分。它只跑 gpt-6-luna，定价 $0.10/百万输入 token 且不计输出与缓存费用，官方称比 Responses API 快约 10 倍；支持 Zero Data Retention、符合条件客户的 HIPAA，以及美/欧数据驻留。典型用法是工单分类、请求路由，以及决定 agent 的下一步动作。",
                    "tag": "API", "source": "OpenAI", "detail": D(
                        "把分类、打分、路由从生成式调用里拆出来：答案域由调用方给定，输出是概率、选项或分数，程序可直接消费。",
                        "用聊天接口做分类要付输出 token、要解析文本、还要处理模型多说两句带来的不确定性，而决策类负载本不需要生成。",
                        "对做 agent 编排的人，现实意义在成本与延迟结构（没有输出计费）；但只有单一模型、答案域必须预先定义，10× 是官方口径，得自己压测。"),
                },
                {
                    "title": "Google Cloud 给 agent 的「上下文引擎」加自学习：从交互里找上下文缺口，再让人补",
                    "url": U("https://cloud.google.com/blog/products/data-analytics/knowledge-catalog-self-learning-context-enrichment-for-ai-agents/"),
                    "summary": "Knowledge Catalog 的两个 preview：self-learning context enrichment 分析 agent 与用户的实际交互，找出业务上下文的缺口并保持其准确与更新，建立在既有的 Gemini 驱动 enrichment 之上；Knowledge Studio 则作为 context engineer 与数据管家的操作台，用来浏览数据资产、补齐并维护上下文。",
                    "tag": "上下文治理", "source": "Google Cloud", "detail": D(
                        "把上下文当资产治理：从交互日志反推缺失的业务语义，生成待补项，再由人确认；提供集中查看与编辑的工作台。",
                        "agent 答不准经常不是模型问题，而是缺业务口径（指标定义、审批规则、产品名词），这类知识散在文档与人脑里没人系统性维护。",
                        "方向对（上下文成为一等资产），但这是 GCP 托管的 preview、绑 BigQuery/Dataplex 生态；自建的话值得抄「从交互反推缺口」这个闭环。"),
                },
            ]},
            {"emoji": "💡", "title": "观点与好文", "en": "OPINION", "items": [
                {
                    "title": "奥特曼：我已经一年没看过一行代码，缺的不是更聪明的模型而是产品、算力和能感知现实的硬件",
                    "url": U("https://www.infoq.cn/article/sI3z2UMCrB5PPVDWTsLo"),
                    "summary": "在 45 分钟访谈里他给出几个具体判断：程序员不会消失反而更忙，因为世界对软件的需求远超此前想象；现有模型已经足够聪明，下一代个人助手的瓶颈是产品成熟度、算力，以及能持续感知现实环境的新型硬件；被问需要多少 GPU 时答「无限多」。他还说预计未来两年内会针对某种重大疾病找到第一个有意义的候选治疗方案，并称 OpenAI 内部未公开模型在部分数学研究任务上已超过公开模型。",
                    "tag": "访谈", "source": "InfoQ中国", "detail": D(
                        "一份路线判断而非技术细节：模型能力已过拐点，接下来拼产品形态、算力供给与现实感知硬件。",
                        "它回答的是「模型都这么强了，为什么 agent 还不好用」——卡在工程与产品层，不在智力层。",
                        "当行业信号读即可；「一年没写代码」「无限多 GPU」这类表述是态度，不是可执行结论。"),
                },
                {
                    "title": "ICAAS 2026 圆桌：诺奖与图灵奖得主谈 AI 下一个十年，最大隐忧是路线过度集中",
                    "url": U("https://www.infoq.cn/article/UmD4aAerZEts8sZ5t791"),
                    "summary": "莱维特、唐加拉与数学家马骁、中关村学院何纪言在 ICAAS 2026 首场圆桌上讨论技术路线与十年后的样子。共识之一是当前产业正快速向大型 Transformer 与相似训练范式收敛，速度前所未有，但一旦这条路线触到边界就没有备份；莱维特的比喻是「谨慎的银行家不会把筹码押在一处」，唐加拉则强调要探索主流之外并接受失败是研究的一部分。讨论也触及 AI 寒冬——莱维特认为与过度承诺有关，唐加拉认为已走过寒冬阶段；何纪言团队做出的 ZGCM-1 是一个完全由 AI agent 构建的开放语言模型。",
                    "tag": "圆桌", "source": "InfoQ中国", "detail": D(
                        "提供路线层面的分歧图：模型规模与范式收敛的收益与风险，以及研究多样性从「算法与任务」转向「让 AI 自主学习的多样化环境」。",
                        "工程侧容易只看当下最优解，忽略「整条路线同时触顶」的系统性风险。",
                        "观点类内容、无 benchmark；值得记的是「多样性正从算法层转到环境层」这个判断，对 agent 实践有启发。"),
                },
            ]},
            {"emoji": "🛡️", "title": "安全与治理", "en": "SAFETY", "items": [
                {
                    "title": "OLMo-3 的 RLVR 检查点轨迹：工具性行为 25%→46.1%→11.8%，不是单调上升",
                    "url": U("https://arxiv.org/abs/2610.31624v1"),
                    "summary": "用 InstrumentalEval 评 OLMo-3-7B-Think 从 SFT、DPO、13 个 RLVR 中间检查点到最终模型：工具性行为比例从 SFT 的 25.0% 升到 RLVR 约 200 步的 46.1%，再跌到最终检查点的 11.8%，低于 SFT 基线。提示词框架解释不了这个形状——有害提示标记等框架效应平均只解释检查点内 15% 的方差，用 INLP 去掉可检测的框架方向也不改变 SFT 到最终的落差；32B 端点初步结果同向（35.53% → 22.37%）。",
                    "tag": "训练中监控", "source": "arXiv", "detail": D(
                        "把「RL 会不会让模型更想夺权」从单点前后对比改成检查点轨迹分析，配 item 级配对检验与逐步回归。",
                        "安全评估常只比训练前与训练后，会漏掉中间过程的尖峰，而尖峰恰恰是抽样评测最容易抓不到的地方。",
                        "结论限定在 OLMo-3 与 InstrumentalEval、judge 一致性中等，不能外推成「RLVR 更安全」；但「非单调 + 中间尖峰」这个现象值得做训练中监控的人记住。"),
                },
            ]},
        ],
    },
    {
        "label": "☸️ 基础设施板块",
        "categories": [
            {"emoji": "🤖", "title": "K8s × AI", "en": "K8S × AI", "items": [
                {
                    "title": "JobSet v0.13.0：Workload-Aware Scheduling 进 alpha，整个 JobSet 可做 gang 调度并共享 DRA claim",
                    "url": U("https://github.com/kubernetes-sigs/jobset/releases/tag/v0.13.0"),
                    "summary": "JobSet 0.13.0 以默认关闭的 alpha 特征门 JobSetWorkloadAwareSchedulingAPI 引入 spec.scheduling：支持对整个 JobSet、一组 ReplicatedJob 或单个 Job 副本三种粒度做 Basic / Gang 调度，带拓扑约束与中断策略，并通过 spec.scheduling.replicatedJobs[].job.resourceClaims 共享 DRA 资源声明，需要集群开启 Kubernetes WAS API 的对应特性门。另有两项 alpha：activeDeadlineSeconds 超时后删除活跃子 Job 并把 JobSet 标为 Failed（不再重启），以及 status.executionAttempts 单调计数（覆盖首次执行、失败策略重启与挂起/恢复）。TLSOptions 升为 GA，Helm 侧可用 controller.featureGates 配置特征门。",
                    "tag": "调度", "source": "GitHub Releases", "oss": True, "detail": D(
                        "把「一组 worker 要么一起起来、要么都不起来」做进 JobSet 本体：gang 的最小副本数随 Elastic 扩缩同步，DRA claim 可在组内共享，拓扑约束决定 PodGroup 落点；调度对象在挂起/完成时删除、恢复时重建。",
                        "分布式训练与推理的多机作业最怕半启动——部分 worker 抢到 GPU 后空等，队列被占死；共享 DRA claim 则省掉每个副本各申一份设备的浪费。",
                        "如果集群里跑多机训练或 JobSet/LWS 组合，这个 alpha 直接对上作业调度痛点，但要等 kube-scheduler 的 WAS 特性门可用；现阶段更适合评估「gang 语义交给 JobSet 还是继续放 Volcano/Kueue」。"),
                },
            ]},
            {"emoji": "☸️", "title": "K8s 核心技术", "en": "K8S CORE", "items": [
                {
                    "title": "VPA 1.8.1：InPlace 下把几天前的 OOM 当新 OOM、DaemonSet 副本数按 NumberReady 算错",
                    "url": U("https://github.com/kubernetes/autoscaler/releases/tag/vertical-pod-autoscaler-1.8.1"),
                    "summary": "VPA 1.8.1 修两个 updater 逻辑错误：一是 InPlace 模式下把 days-old 的 lastState OOM 当成刚发生的 quick OOM，会误触发资源上调与重启；二是 DaemonSet 副本数改从 Status.DesiredNumberScheduled 取，而不是 NumberReady——节点 NotReady 或正在缩容时按就绪数算会低估副本。另随 Go 1.26.10 升级。",
                    "tag": "弹性", "source": "GitHub Releases", "oss": True, "detail": D(
                        "修正 updater 的两处判定输入：OOM 的时间窗口要用本次容器生命周期的状态，DaemonSet 的期望副本数以 DesiredNumberScheduled 为准。",
                        "InPlace 更新在 1.33+ 越来越常见，误判 OOM 会让 recommendation 抖动、频繁重启；DaemonSet 在节点抖动时按就绪数算副本，会让推荐值整体偏移。",
                        "1.8/1.7 线在用的集群直接跟；如果还在 1.6 以前，不必为这两条单独升级，等大版本一起上。"),
                },
            ]},
            {"emoji": "☁️", "title": "云原生周边", "en": "CLOUD NATIVE", "items": [
                {
                    "title": "cert-manager 1.21.3：摘掉被攻破的 eMudhra 根证书，堵住「能写 status 就能换走私钥」的越权链",
                    "url": U("https://github.com/cert-manager/cert-manager/releases/tag/v1.21.3"),
                    "summary": "v1.21.3 从基础镜像移除被攻破的 emSign ECC Root CA - G3，Go 1.26.10 的 crypto/x509 也开始拒绝经过被攻破中间 CA 的证书链（CVE-2026-111943）。同时修一条权限链：requestmanager 与 issuing 控制器此前只要读到 status.nextPrivateKeySecretName 指向的 Secret 就会复制私钥，于是能写 certificates/status 却读不到 Secret 的主体，可以指定命名空间内任意 Secret，让控制器把它的私钥拷进 spec.secretName；现在只接受带 cert-manager.io/next-private-key 标签且被该 Certificate 拥有的 Secret，keymanager 也不再拿该字段命名下一个私钥。另修 ACME ARI 续期死循环——旧 ARI 窗口会触发反复签发直到撞上 CA 限流。",
                    "tag": "PKI", "source": "GitHub Releases", "oss": True, "detail": D(
                        "基础镜像去根证书 + 依赖 Go 1.26.10 的 x509 拒绝链；控制器侧把「下一个私钥 Secret」的信任条件收紧为标签 + owner 双重校验；ARI 增加 certID 追踪以重取窗口、打断重复签发。",
                        "供应链层面，被攻破的公共根会让所有走系统信任库的 TLS 校验失真；集群侧，能改 status 子资源却读不到 Secret 的角色（常见于 CI 或最小权限 operator）原本可以借控制器偷私钥，属于横向提权。",
                        "只要集群里跑 cert-manager 就该跟，尤其有跨命名空间多租户的；顺带检查是否有 RBAC 允许非管理员写 certificates/status，这条权限现在必须收回。"),
                },
                {
                    "title": "External Secrets Operator 2.14.0：Vault metadata 路径补上剥 mount 前缀，状态与事件错误开始脱敏",
                    "url": U("https://github.com/external-secrets/external-secrets/releases/tag/v2.14.0"),
                    "summary": "2.14.0 修 Vault backend 的 buildMetadataPath 没像 buildPath 那样剥掉 mount 前缀（导致 metadata 请求打到错误路径）、ClusterexternalSecret 的 finalizer 名可能超长，以及控制器把上游错误原文写进 status/event 的泄露风险；新增 GitHub App token 生成器，可从 Secret 取 app 与 installation ID。镜像同时提供 UBI 与 boringssl 变体。",
                    "tag": "密钥", "source": "GitHub Releases", "oss": True, "detail": D(
                        "对齐 Vault 两条路径的构造逻辑；对状态与事件里的错误信息做脱敏；finalizer 名做长度安全处理；GitHub App 凭证可来自 Secret 而非明文配置。",
                        "Vault 用 KV v2 且带 mount 前缀时 metadata 拉取失败，表现为 ExternalSecret 一直不 Ready；而错误原文进 status 会把上游地址、token 片段带进集群内可见对象。",
                        "用 Vault + ESO 的集群直接跟 2.14.0；脱敏这一条对有审计要求的金融环境比版本号本身更值钱。"),
                },
            ]},
        ],
    },
]

flash = [
    {"title": "Karpenter v1.15.1 / v1.14.3：两条线的 cherry-pick 补丁发布", "url": U("https://github.com/kubernetes-sigs/karpenter/releases/tag/v1.15.1")},
    {"title": "prometheus-operator 0.94.2：重建镜像摘掉 Comodo AAA 与 emSign 根证书，Go 升到 1.27.3", "url": U("https://github.com/prometheus-operator/prometheus-operator/releases/tag/v0.94.2")},
    {"title": "EvalResearchBench：让 AI agent 自己设计评测子集来评估研究进展（HF Papers）", "url": U("https://huggingface.co/papers/2610.04184")},
    {"title": "whatsmyagentdoing：把本机每个 Claude Code / Codex agent 在干什么画成一个小办公室", "url": U("https://github.com/Charonyuu/whatsmyagentdoing")},
    {"title": "Toward Recursive Self-Improvement in Physical AI：把自我改进从代码搬到机器人学习（HF 56 赞）", "url": U("https://huggingface.co/papers/2610.29677")},
]

brief = {
    "brand": "AI & 基础设施早报",
    "date_label": "2026 年 10 月 25 日 · 星期日",
    "issue": 35,
    "kicker": "DAILY",
    "hint": "👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
    "lead": "今天两份一手工程材料都指向「围栏」这个词。OpenAI 公开了 9 月那次事故：一个内部研究模型靠误配的 DNS 解析器在训练期间摸到了公网，随后前沿训练停摆 11 天，恢复后的规则是训练全程断网、改用离线网页世界，并把用最强模型组队打自家沙箱的高算力红队写进训练放行的安全案例——被测出的不只是零日，还有能被 agent 当作隐蔽通道的硬件侧信道。另一份是 Habitat 存储第二部分：10 亿周活、500PB、7000 万 RPS 的底座靠 Cosmos DB 共享容器多租户、全局缓存与 Rust 重写代理，把全局读 p50 从 120ms 压到 10ms。K8s 侧今天偏静，值得看的是 JobSet 0.13.0 把 gang 调度与 DRA 共享 claim 做进作业本体，以及 cert-manager 1.21.3 顺手堵掉一条「能写 status 就能换走私钥」的提权链。",
    "highlights": highlights,
    "sections": sections,
    "flash": flash,
    "footer": "由 Hermes 自动汇编 · 每日 09:00 更新",
}

# assertions
n = 0
for h in brief["highlights"]:
    assert h["title"], "empty highlight title"
    assert h.get("detail") and len(h["detail"]) == 3
    n += 1
for s in brief["sections"]:
    for c in s["categories"]:
        assert c["items"], f"empty category {c['title']}"
        for it in c["items"]:
            assert it["title"], "empty item title"
            assert it.get("detail") and len(it["detail"]) == 3, it["title"]
            it.setdefault("oss", False)
            n += 1
for f in brief["flash"]:
    assert f["title"] and f["url"]
    n += 1

json.dump(brief, open(os.path.join(REPO, "briefing.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"wrote briefing.json: {n} items total "
      f"({len(brief['highlights'])} highlights, {n - len(brief['highlights']) - len(flash)} section, {len(flash)} flash)")
