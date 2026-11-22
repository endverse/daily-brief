#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 062 (2026-11-22)."""
import json, os, sys

REPO = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(REPO, "processed.json"), encoding="utf-8"))
ALL_URLS = {i["url"] for i in items}


def U(frag):
    hits = [u for u in ALL_URLS if frag in u]
    if len(hits) != 1:
        print("URL LOOKUP FAIL", frag, hits, file=sys.stderr)
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


highlights = [
    {
        "title": "Hebbia 用 GPT-6 Astra 做金融研究：引用相关性 99.5%，必需来源类型覆盖领先最好替代 13.6 个百分点",
        "url": U("business/customer-stories/hebbia"),
        "source": "OpenAI News",
        "summary": "Hebbia 的 Matrix 把尽调材料（约 2000 个文件的 data room）连到可追溯的引用单元格，客户经理问「收入为什么能持续」「和同业比怎样」，答案直接挂到原始文档。他们拿 OpenAI 的 GPT-6 Astra 测了这条链路的两端：找出问题所需来源，以及按用户给的简报结构生成演示。测试里引用摘录与问题的相关性达 99.5%，必需来源类型的覆盖比测过的最好替代模型高 13.6 个百分点；演示要求满足率 97.9%，同一维度领先 14.4 个百分点。产出是原生 PowerPoint，按用户给的结构和规范出页，而不是把文本塞进模板。Hebbia 产品侧的评价是「在这两个方向上，GPT-6 Astra 比此前测过的任何模型都强」。",
        "note": "OpenAI 11 月 20 日发布的客户案例：引用摘录相关性 99.5%，必需来源类型覆盖 +13.6pp，演示要求满足 97.9%（+14.4pp），尽调场景约 2000 文件，输出原生 PowerPoint。",
        "detail": it3(
            "把长文档研究的两个动作交给模型：先在 data room 里挑出回答问题所需的来源并给出引用，再把结论按用户结构与规范生成原生 PPT 页面；案例给出引用相关性 99.5%、来源覆盖 +13.6pp、演示要求满足 97.9% 三个可对比指标。",
            "金融研究里最贵的不是写结论，是让每个数字可追溯、来源类型齐全、格式合规；人工做尽调包要反复在几千份文件里对表格与合同，出错就得重来。",
            "值得当作「金融文档 agent」的落地基准看：它的评测口径是客户自己的任务集，不是通用 benchmark，正好对应量化/投研场景里「引用能不能信」这个核心问题；限制是案例只覆盖研究与演示两端，没有给延迟与单份成本。"),
    },
    {
        "title": "开源 Agnes Harness：Sys1 双系统 + 版本化 Playbook，设备入库验收从 30 分钟超时压到 8 分钟",
        "url": U("qbitai.com/2026/11/511582"),
        "source": "量子位", "oss": True,
        "summary": "Agnes Harness 是 Apache 2.0 开源（GitHub 2.1k star）的 agent 执行框架，核心是两件事：Sys1 双系统决策，把快判断交给专门的小模型、慢推理交给大模型；以及 TTT × RSI 双层自进化——TTT 在当下任务里边做边调 prompt/memory/skills/subagent 的组合，RSI 把验证有效的新方法固化成版本化 Playbook 供后续任务复用，且新方法要先过仿真测试才允许写进手册。官方用一个设备入库验收任务演示：第一次称重台未稳定就抢读数，折腾 30 分钟超时；第二次直接按沉淀下来的流程走，8 分钟内完成。9 项基准里 6 项拿第一、1 项与 Codex 并列，DeepPlanning 87.07、BigCodeBench-Hard V1 通过率 40.69%。业务工具、模型适配器、skills 甚至操作界面都能做成插件，硬件侧另有一套 MHS（Model Hardware Standard）描述设备状态与可执行动作，实时控制与物理安全仍留给设备控制器。",
        "note": "Apache 2.0 开源（2.1k star）；Sys1 双系统 + TTT 适应 + RSI 版本化 Playbook；验收任务 30 分钟超时 → 8 分钟；9 项基准 6 项第一、1 项与 Codex 并列；DeepPlanning 87.07、BigCodeBench-Hard V1 40.69%；插件化 + MHS 硬件标准。",
        "detail": it3(
            "把「执行经验」变成可复用资产：TTT 在任务内试新做法，RSI 把验证过的流程写进带版本的 Playbook，下次同类任务直接复用；插件层承载业务工具与模型适配器，MHS 让机械臂/传感器按统一格式申报状态和动作。",
            "agent 落地最贵的不是开发而是适配：每个客户的流程、工具、设备都要重新教一遍，同一个场景第 100 次和第一次犯一样的错，token 花了经验没留下。",
            "值得读它的 Playbook 与验证回路（先仿真、再入库、带版本）——这套「经验必须可回归验证」的做法可直接搬到内部 skill 体系；限制是基准为官方自评，本地部署要 Node 24.10+/pnpm 10.34.5，工业设备侧 MHS 还在以插件形式接入。"),
    },
]

ai_cats = []

ai_cats.append({"label": "🧠 模型与研究", "items": [
    {
        "title": "OpenAI 公布反蒸馏防线：改版后各类抽取攻击平均成功率降到 1% 以下",
        "url": U("openai.com/index/combatting-adversarial-distillation"),
        "source": "OpenAI News",
        "summary": "OpenAI 11 月 20 日公开对抗性蒸馏的防护体系：对抗测试、模型训练、分类器与 API 级防护叠加，再配合对协同抽取行为的调查与执法，防护等级对齐生物与网络安全领域。给出的量化结果是「从早先请求抽取受保护推理」这类攻击的攻击成功率从 54% 级降到 1% 以下，改版后每种攻击类型的平均 ASR 均低于 1%。文章强调保护 reasoning trace 本身就是安全边界：被蒸馏的模型会脱离原有拒答与审核。",
        "detail": it3(
            "四层叠加：训练阶段硬化、推理侧分类器、API 级行为限制，加上对批量抽取账号的调查与封停；公开的度量是各攻击类型平均 ASR <1%。",
            "蒸馏把前沿能力复制到没有同等防护的模型上，再用它做原模型会拒答的事（如网络攻击）；单靠输出过滤挡不住成规模的抽取。",
            "值得关注两条：一是「保护推理过程」正成为供应商的默认立场，做二次训练/评测数据管线的团队要重新评估合规边界；二是它和本月两条用量政策收紧是同一套逻辑。"),
    },
    {
        "title": "华为云开源 CloudRobo-WM1.2：RoboTwin 2.0 与 LiberoPro 2.0 双榜第一，11 月 30 日放权重",
        "url": U("infoq.cn/article/LCqRiGDSeMBfXo4iktdA"),
        "source": "InfoQ中国", "oss": True,
        "summary": "华为云 11 月 16 日发布昇腾原生具身世界模型 CloudRobo-WM1.2，称在 RoboTwin 2.0 与 LiberoPro 2.0 两项评测中均列第一，并将在 11 月 30 日开放模型权重、推理代码与后训练代码。技术上有五处设计：PPA 多模态世界表征（理解物体物理属性并预测交互后的变化）、世界模型原生的 DualAct 动作架构（世界模型直接输出动作，动作专家规模可按任务定义）、多粒度监督自适应预训练（兼容缺动作标注、缺深度、视角不全的数据）、本体语义保真的跨具身建模（单臂/双臂/轮式共享模型但保留各自运动语义）、以及 World/Expert Action × Joint/Action-only 四种可组合的弹性推理模式。",
        "detail": it3(
            "共享世界模型骨干 + 原生动作生成，把「看懂物理过程」和「输出动作」放在一个模型里；跨本体建模让单臂/双臂/轮式共用训练数据，推理侧可按算力与延迟在四种模式间切换。",
            "具身模型的实际痛点是异构数据利用率低（缺标注就整条丢弃）与跨形态迁移差，每换一种机器人就要重训。",
            "值得等 11 月 30 日的权重落地再看：双榜第一是厂商口径，真正要验证的是昇腾之外的硬件能否跑、四种推理模式在延迟与成功率上差多少。"),
    },
]})

ai_cats.append({"label": "🧭 Agent 工具链", "items": [
    {
        "title": "Orca v1.4.269：Bots 一次扩到 8 个 agent，组房间里可用 @名字 交接任务",
        "url": U("orca/releases/tag/v1.4.269"),
        "source": "GitHub Releases", "oss": True,
        "summary": "Orca 1.4.269 让 Bots 能跑在 Kiro、Kimi Code、Auggie、Gemini CLI、Kilo Code、MiMo Code、Droid、Goose 八个新 agent 上，Chat 也能直接开 Kiro、Auggie、Goose，且 Kiro 会话会执行你自己的 hooks。群组房间里，bot 在回复里 @ 某个成员就由该成员接手这一轮，等于把多 agent 接力写进聊天协议。手机端补上回答 agent 提问、处理 Google/Composio 配置卡、在 Needs you 里批工具授权与访问申请；空闲 Mac 终端的 CPU 占用下调，Git 操作移到后台 worker。",
        "detail": it3(
            "把「一个 bot 绑一个 agent」放开成八个可选后端，并把交接做成群聊里的 @ 语义；手机端能完成审批与配置，等于把 agent 值守从桌面挪到随身。",
            "多 agent 协作最麻烦的是会话与身份绑定，以及审批必须回到电脑前；换个 agent 就要重配一遍工具与身份。",
            "值得升级：如果你已经在用 Orca Bots（1.4.265 起），这次扩容直接决定能不能把 Gemini CLI / Goose 这类后端纳入同一套 bot 身份；注意手机端功能需要匹配的移动端版本。"),
    },
    {
        "title": "Gemini CLI v0.70.0：策略引擎换 re2js 线性时间匹配，跳过启动命令不安全的系统 MCP server",
        "url": U("gemini-cli/releases/tag/v0.70.0"),
        "source": "GitHub Releases", "oss": True,
        "summary": "v0.70.0 把策略引擎里 argsPattern 的求值换成 re2js，避免正则回溯导致的线性时间退化，等于给策略匹配上了执行时间上限。安全侧新增：启动命令权限不安全的系统级 MCP server 会被跳过；对含未解析变量展开的 shell 命令继续保留 ASK_USER 确认；commandPrefix/commandRegex 规则改为匹配顶层命令参数，减少误放行。可用性上，models 列表现在报告准确的输出 token 上限，请求超时超过 300 秒时同步放大 undici 的 bodyTimeout。",
        "detail": it3(
            "策略求值不再可能被恶意正则拖死（re2js 线性时间），系统 MCP server 的启动命令要先过权限检查，shell 展开无法解析时强制问人。",
            "agent 工具的 allow/deny 规则本身就是攻击面：正则回溯能让策略进程卡住，系统级 MCP server 又常以高权限启动。",
            "值得跟进，尤其你在用 MCP + 细粒度命令策略；升级后要复读自己的 commandPrefix 规则，因为匹配对象改成了顶层命令参数。"),
    },
    {
        "title": "Entire：前 GitHub CEO 做的 agent 原生 Git 平台，用 trails 给每次推送打合并分数",
        "url": U("infoq.cn/article/6swrOq5xUXwVqrREwJwc"),
        "source": "InfoQ中国",
        "summary": "Entire 是 Thomas Dohmke（前 GitHub CEO）做的代码托管平台，判断 PR 模式不适合 agent 高速迭代：合并请求的时间线变成只有 agent 会读的审计日志。它的核心对象是 trails——按缺陷工单或需求发起、可跨多个仓库，每次推送都会触发云沙箱里的评审 agent，从代码质量、安全性、slop（低质量代码）与是否需要人工评审四个维度打分并给理由，界面同时显示最近 5 轮与当前结果，分数稳定前应继续迭代；仓库级 Gates 定义合并门槛。平台称推送速度最高达 GitHub 的 89 倍，另配 continuous memory：两个开源工具把仓库图谱与历史会话、Git 历史合成持久记忆层。",
        "detail": it3(
            "把「能不能合」变成可迭代的分数：每轮推送重新评审，看 5 轮趋势而不是单次结论，Gates 定义硬门槛；continuous memory 给 agent 提供「变更原因」的上下文。",
            "agent 一天能提几十个 PR，人类评审跟不上，时间线也读不完；单次评审经常漏掉关键问题。",
            "值得关注它的评分口径（质量/安全/slop/人工必要性）——这套指标能直接搬进内部 CI 门禁；限制是平台绑定，89 倍推送速度是官方数据，尚未有第三方复现。"),
    },
]})

ai_cats.append({"label": "🏖️ 沙箱与运行时", "items": [
    {
        "title": "Kata Containers 4.4.0：快照恢复保留设备生命周期，CLH 上用 VMDK 装多层 EROFS",
        "url": U("kata-containers/kata-containers/releases/tag/4.4.0"),
        "source": "GitHub Releases", "oss": True,
        "summary": "4.4.0 的重点在 runtime-rs：快照恢复时保留设备生命周期状态（dragonball 后端），并补完热插块设备与 VFIO 设备的清理链路；Cloud Hypervisor 后端改用 VMDK 磁盘格式承载多层 EROFS 容器镜像，减少逐层拉取；热插前先显式预留 PCIe root port 地址，避免地址冲突；网络清理从 Tokio worker 里隔离出来，防止阻塞运行时主循环。部署侧 kata-deploy 支持追加 CRI 配置、保留未改动的 mtime、写入 TOML 时保留空数组，devkit 安装要求 kata-ctl；GPU 侧 dcgm-exporter 升到 4.8.4，nvgpu 镜像带上 kata-ctl。",
        "detail": it3(
            "把 VM 级隔离的运维细节补齐：快照恢复不丢设备状态、多层镜像用 VMDK 一次挂载、热插地址先预留、清理不阻塞主循环；配套 GPU 监控组件同步升级。",
            "沙箱做快照/恢复时设备状态容易错乱（重启后 VFIO 设备失效、块设备残留），多层镜像逐层拉取也拖慢冷启动。",
            "用 Kata 跑多租户 agent 或 CI 的话值得跟：这些条目直接影响快照恢复的可靠性；升级要注意 kata-deploy 行为变化（devkit 需要 kata-ctl）与 CRI 配置被追加而非覆盖。"),
    },
]})

ai_cats.append({"label": "🛠️ AI 工程落地", "items": [
    {
        "title": "火山引擎把企业上下文做成目录树：规则召回率 43%→100%，Issue Fix 机器人两天提 67 个 PR",
        "url": U("infoq.cn/article/YTGHxcabs0RI3btLIUxm"),
        "source": "InfoQ中国", "oss": True,
        "summary": "字节开源的 OpenViking（40k+ star 上下文数据库）给出的做法是给企业知识一个统一地址：用 viking:// 目录树把知识、记忆、技能、规则和实时数据挂在一起，用 L0/L1/L2 分层加目录递归检索替代平铺切片，用「上下文编译」把原始资料持续加工成业务知识，并把规则作为独立的上下文类型，保证该遵守的一条不漏。授权在检索阶段完成——目录级 ACL 决定哪些能看，而不是取回后再过滤；长期记忆与 Handoff 让经验跨会话、跨人、跨 agent 沉淀。官方给的数据是记忆 benchmark 上规则召回率从 43% 提升到 100%，内部 Issue Fix 数字员工两天提交 67 个 PR、合入 28 个。",
        "detail": it3(
            "用目录树 + 分层摘要 + 上下文编译，把散落的文档/代码/Wiki/指标变成 agent 可寻址的上下文；规则单独成类保证不漏，ACL 在检索期生效，记忆与 Handoff 做跨会话沉淀。",
            "接 agent 后最常见的问题不是模型答不出，而是找不到对的资料、找不全要遵守的规则、分不清哪些能看哪些能做；向量检索只能捞回相似片段。",
            "值得看它的分层与 ACL 设计——这两点决定了「上下文」能不能进生产；目前数据来自厂商自述（召回 43%→100% 的口径要看 benchmark 定义），但目录树 + 检索期授权这套结构对多租户 agent 是可复用的。"),
    },
    {
        "title": "Vodafone 用 Data Engineering Agent 把数据管道成本降 30%",
        "url": U("vodafone-cuts-data-pipeline-costs-30-via-data-engineeringagent"),
        "source": "Google Cloud",
        "summary": "Google Cloud 的客户案例：Vodafone 把数据管道的建设与调优交给 Data Engineering Agent，官方口径是管道成本下降 30%。案例的重点不是「AI 写 SQL」，而是让 agent 在既有 BigQuery/Dataflow 资产上做诊断与改写，人保留审批。",
        "detail": it3(
            "agent 在既有数据平台上做管道诊断与改写，产出可审的变更而不是黑盒执行；公开指标是成本下降 30%。",
            "数据管道成本高但没人有空逐个查执行计划，优化往往滞后于故障。",
            "参考价值在于「成本」而非「生成」这个落点：如果你的 K8s 侧也在跑批处理，这套「agent 只提变更、人审批」的模式比其他全自动叙事更可信；30% 是客户口径，适用边界未公开。"),
    },
]})

ai_cats.append({"label": "📊 产品与商业", "items": [
    {
        "title": "美国 AI 音乐公司做视频生成，底层模型来自中国 MiniMax",
        "url": U("qbitai.com/2026/11/511722"),
        "source": "量子位",
        "summary": "一家美国 AI 音乐巨头进军视频生成，其底层视频模型来自中国厂商 MiniMax。这条的价值在于供应结构：海外应用层开始直接采购中国的视频基座模型，而不是自研或多方比价。",
        "detail": it3(
            "海外应用公司把视频生成能力外包给中国基座模型，自己只做产品与分发。",
            "视频生成自研成本极高，应用层需要快速上线能力。",
            "关注供应链信号即可：模型能力开始按「基座—应用」分层，国内厂商在视频这类重算力方向上有了出海通道。"),
    },
]})

ai_cats.append({"label": "🛡️ 安全与治理", "items": [
    {
        "title": "ChatPRD 关掉免费试用：token 欺诈者拿试用额度转卖模型调用",
        "url": U("simonwillison.net/2026/Nov/20/token-fraud-is-here-and-its-bad"),
        "source": "Simon Willison",
        "summary": "ChatPRD 创始人 Claire Vo 公开复盘了持续的 token 欺诈：有人批量注册免费试用、拿促销码，再把流量隧道进她的 agent 转卖，甚至有人在上面跑「Roblox / Fortnite 地图工作室」这类生意。一个典型信号是 agent 里反复出现「骑自行车的鹈鹕」SVG 提示词——用来探测底层是哪个模型家族。她最终的处置是彻底关停免费试用。",
        "detail": it3(
            "披露的是滥用模式而非漏洞：免费额度 + 单一 agent 端点 = 可转售的推理通道，提示词指纹（pelican on a bicycle）被用来识别后端模型。",
            "自助注册型 AI 产品对新用户送额度，等于把付费推理能力开放给批量注册者，账单与滥用同时上涨。",
            "值得当作自查清单：如果你的多租户 agent 对外发放试用，至少要有账号级限速、提示指纹检测与额度隔离；关闭试用是止损而非治理。"),
    },
]})

infra_cats = [
    {"label": "🤖☸️ K8s × AI", "items": [
        {
            "title": "vLLM v0.34.0：KV cache 改为按剩余显存自动定容，Model Runner V1 移除，GB200 解码快 1.95 倍",
            "url": U("vllm/releases/tag/v0.34.0"),
            "source": "GitHub Releases", "oss": True,
            "summary": "v0.34.0 是 1061 个 commit、412 位贡献者的大版本，新增 10 个模型（含 Mistral Large 4 的 1T 总参/52B 激活、MiniMax-M3.1-Flash、Nemotron-3.5-Transcribe）。最大变化是可扩展 KV cache 默认开启：显存按 warmup 与 CUDA graph 捕获之后实际空闲的内存来定容，MiniMax-M3 在 H200 上从 433k 扩到 672k token；代价是部分模型在并发 128 时 TPOT 上升 6–18%，可用 --gpu-memory-utilization 0.9 或关闭该特性退回。Model Runner V1 被删除（V2 成为唯一 GPU runner），默认 block size 从 16 改为 64，ROCm 7.2 产物不再发布，要求 huggingface_hub ≥ 2.0.0。性能上 Blackwell 解码最高 1.95 倍（GB200 上的 Step5）、GLM-5.3-Flash 吞吐 1.6 倍、长 prompt TTFT 改善 1.24–1.40 倍。",
            "detail": it3(
                "KV cache 从「按 gpu_memory_utilization 估算」改成「按 warmup 后的真实空闲内存定容」，同一张卡能装更多 KV；同时删掉 V1 runner、统一走 MRV2（含投机解码与 DCP 的 dual-batch overlap）。",
                "显存估算偏保守导致 KV cache 留白、高并发时 TTFT 变差；配置项又要人肉按卡型试。",
                "跑推理服务的话这是必须评估的升级点：多数场景应直接删掉 gpu_memory_utilization；但 block size 64、MRV2 唯一、ROCm 与 fp_quant/Marlin W4A8 的移除都是破坏性变更，先在灰度集群验证 TPOT 与 OOM。"),
        },
        {
            "title": "Dynamo v1.5.1-kimi-k3-post.1：Kimi-K3 跑在 SGLang 后端，GB300 给出聚合与 1P1D 两套配方",
            "url": U("dynamo/releases/tag/v1.5.1-kimi-k3-post.1"),
            "source": "GitHub Releases", "oss": True,
            "summary": "这是一个实验性快照发布，明确不建议上生产：把 moonshotai/Kimi-K3 跑在 Dynamo 1.5.1 + SGLang 0.5.18 的运行时上，并内置两个 Kimi-K3 必需的修复——DCP prefill/decode 配合 DSpark draft-KV 传输，以及 SM100 上 MoonViT 的 cuDNN 守卫。GB300 给了两套配方：聚合式用 2 个 worker、16 张 GB300、DCP8 attention + TP8 MoE、带 load-aware 路由；分离式是 1P1D，prefill TEP8、decode DCP8+TEP8，KV 走 Mooncake over NVLink。配方里还带了 64K 输入/400 输出/90% KV 复用率的 agentic trace 的 AIPerf 回放。",
            "detail": it3(
                "把新模型的上线前置工作做成可复用的容器与配方：镜像、并行度（DCP/TP/TEP）、KV 传输后端与压测 trace 都给全，换模型时不用从零调并行。",
                "新模型（尤其是带 DSpark 草稿的 Kimi-K3）在 vLLM/SGLang 上常有缺失的 kernel 补丁，团队要自己踩；GB300 这类新硬件配方更稀缺。",
                "适合当作模板：它的价值是「K8s 上跑 16 卡大模型的配方长什么样」，而不是版本号本身；实验性构建 + 单模型，生产要等 1.7 稳定线。"),
        },
    ]},
    {"label": "☸️ K8s 核心技术", "items": [
        {
            "title": "BuildKit v0.35.1：恢复与 docker pull 共享快照键名，修大文件同步模式列表报错",
            "url": U("buildkit/releases/tag/v0.35.1"),
            "source": "GitHub Releases", "oss": True,
            "summary": "0.35.1 是补丁版：跳过空的 attestation manifest；恢复 v0.33.x 之前允许的「与 docker pull 共享快照键名」的行为；修掉 filesync 模式列表过大导致报错的回归。",
            "detail": it3(
                "三处修复分别对应：空 attestation 造成的 manifest 异常、与 docker pull 共享快照键导致的重复拉取、大仓库 filesync 规则过多时的失败。",
                "0.33 起的回归会让多工具共用同一镜像缓存的构建变慢或直接报错。",
                "值得跟一个小版本：如果 CI 里 buildkit 与 docker pull 混用同一 store，0.35.1 修的就是你；无破坏性变更。"),
        },
    ]},
]

flash = [
    {"title": "microsandbox 0.8.1 / 0.8.0：SDK 在创建沙箱前解析命名卷，修云后端命名挂载失败", "url": U("superradcompany/microsandbox/releases/tag/v0.8.1"), "source": "GitHub Releases"},
    {"title": "Azure Database for PostgreSQL 的 Database Agent 进入公共预览", "url": U("azure.microsoft.com/updates?id=579579"), "source": "Azure Updates"},
    {"title": "Google Duplex 演进：Gemini 现在能替你打电话问商家营业时间与价格", "url": U("research.google/blog/how-google-duplex-evolved"), "source": "Google Research"},
    {"title": "GKE Dataplane V2 支持原地迁移，不用重建节点", "url": U("gke-dataplane-v2-in-place-migration"), "source": "Google Cloud"},
    {"title": "InfoQ 视频：Agent 上岗之后，哪些动作敢真正放手", "url": U("infoq.cn/video/qafOtORWUX0eD0WfSlYi"), "source": "InfoQ中国"},
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

lead = ("今天三条都在回答同一个问题：agent 怎么才算真的落地。Hebbia 用 GPT-6 Astra 把金融研究里的引用做成可核查的 99.5%，"
        "开源 Agnes Harness 用版本化 Playbook 让设备验收从 30 分钟超时压到 8 分钟，Orca 则把 Bots 一次扩到 8 个 agent、用群聊 @ 交接任务。"
        "沙箱侧 Kata 4.4.0 把快照恢复做到设备生命周期级别；基础设施侧 vLLM 0.34.0 把 KV cache 改成按真实空闲显存自动定容，"
        "代价是默认 block size 与 Model Runner 都变了，升级前要先过一遍破坏性变更清单。")

brief = {
    "brand": "AI & 基础设施早报",
    "date_label": "2026 年 11 月 22 日 · 星期日",
    "issue": 62,
    "kicker": "AI & INFRASTRUCTURE DAILY · NO.062",
    "hint": "👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
    "lead": lead,
    "highlights": highlights,
    "sections": sections,
    "flash": flash,
    "footer": "由 Hermes 自动汇编 · 每日 08:30 更新",
}

json.dump(brief, open(os.path.join(REPO, "briefing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = len(highlights) + sum(len(c["items"]) for s in sections for c in s["categories"])
print("wrote briefing.json | items:", n, "| flash:", len(flash),
      "| sections:", [(s["label"], [(c["label"], len(c["items"])) for c in s["categories"]]) for s in sections])
