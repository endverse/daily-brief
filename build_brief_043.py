#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 043 (2026-11-03). All URLs resolved from processed.json."""
import json, sys

P = "processed.json"
items = json.load(open(P, encoding="utf-8"))

def U(prefix):
    hits = [it["url"] for it in items if it["url"].split("?")[0].find(prefix) >= 0 or prefix in it["url"]]
    if not hits:
        sys.exit("URL not found in processed.json: " + prefix)
    return hits[0]

EMOJI = {
    "🧠 模型与研究": "🧠", "🧩 Agent & Skill": "🧩", "🛠️ AI 工程落地": "🛠️",
    "📊 产品与商业": "📊", "💡 观点与好文": "💡", "🛡️ 安全与治理": "🛡️",
    "🤖☸️ K8s × AI": "🤖", "☸️ K8s 核心技术": "☸️", "🌐 云原生周边": "🌐",
    "🏘️ 社区与项目": "🏘️", "☁️ 公有云动态": "☁️",
}

brief = {
 "brand": "AI & 基础设施早报",
 "date_label": "2026 年 11 月 3 日 · 星期二",
 "issue": 43,
 "kicker": "DAILY",
 "hint": "👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
 "lead": "今天的线索是「把环境做出来」。阿里云把云电脑重新定义成智能体的工位：身份、权限、审计沿用 IT 老体系，任务卡住时人接手、处理完交回 Agent，好未来不到两周部署约 1000 个 Agent。基础设施侧 NVIDIA 用 AICR 配方把 Vera Rubin 的驱动、DRA、内核与网络组合固化成可复现产物，并在真机上用 NCCL bus bandwidth 当验收门槛（744.71 GB/s）。Agent 工具链也在补「可验证」这一环：Buildkite 给 CI 加了校验流水线、对比失败构建的 MCP 工具，百度把搜索 API 压到 4.9 元/千次抢 Agent 的默认检索入口。安全侧 Mandiant 记录 LLMJacking 单日盗刷超 10 万美元、累计到 100 万美元。",
 "highlights": [
  {
   "title": "阿里云把云电脑做成「Agent 工位」：好未来两周部署约 1000 个 Agent，人可随时接管现场",
   "url": U("infoq.cn/article/Vryq1f3C0f5uZHOlmIp4"),
   "tag": "Agent 落地",
   "source": "InfoQ中国",
   "note": "阿里云智能集团研发副总裁、终端智能计算事业部负责人张献涛在 1024 模力工场·AI 社区日主论坛演讲，主题是云电脑从「人的办公桌面」变成「智能体的工位」。云电脑给 Agent 提供运行桌面软件与访问业务系统的环境，并统一管理身份、可访问数据、可执行操作与操作审计；Agent 遇到登录失效、验证码或需人工判断的步骤时，云电脑保存当前工作状态并通知人接管，人处理完 Agent 继续执行。落地案例是好未来：不到两周通过企业级云电脑部署约 1000 个 Agent，承担教案、课件制作与作业批改，员工可进入同一台云电脑调试。产品侧，云栖大会发布了定位「智能体电脑」的千问 Book，阿里 2026 年还推出 Personal Agent 千问 Go。",
   "summary": "在 1024 模力工场 AI 社区日上，阿里云把无影云电脑的位置重新定义为智能体的工位：Agent 在里面跑桌面软件和企业应用，不再只靠浏览器，对没有开放 API、只能点界面的老系统尤其关键；身份登录、数据范围、可执行操作和审计都沿用云电脑原有的 IAM 体系，不另起一套 Agent 账号。任务被登录失效、验证码或人工判断卡住时，云电脑保存当前状态、说明阻塞原因并通知人接管，人处理完再由 Agent 接着跑，不必从头重来。落地案例是好未来：不到两周通过企业级云电脑部署约 1000 个 Agent，做教案、课件与作业批改，员工可进同一台云电脑调试。张献涛的落点是「Agent 需要人用的工具」，而不是给 Agent 造一套新协议。",
   "detail": [
    {"key": "能做什么", "value": "给每个 Agent 一台云电脑：可运行 Windows/Linux 桌面软件、访问只有 GUI 的老业务系统；身份、数据范围、操作审计与资源配额在云电脑侧统一管理，Agent 与员工可进同一台机器；支持保存现场后由人接管，处理完交回 Agent 继续。"},
    {"key": "解决什么痛点", "value": "纯浏览器 Agent 碰不到只有图形界面的系统；Agent 用共享账号跑业务既没法审计也没法限权；任务卡在验证码、登录或审批就整条流程作废，重跑代价高，且人看不懂它做到哪一步。"},
    {"key": "值不值得", "value": "与他公司正在做的多用户 agent 沙箱是同一类问题——身份隔离、会话状态、人机接力三件事必须一起设计，值得对着这个权限模型与「保存现场」机制设计自己的沙箱挂起/恢复。限制是强绑定阿里云无影，私有化与跨云要自己补；1000 个 Agent 的案例没给单 Agent 的资源开销与并发模型。"}
   ]
  },
  {
   "title": "NVIDIA 用 AICR 配方固化 Vera Rubin 的 K8s 就绪状态：DRA v0.5.0 + GPU Operator v26.7.0，NCCL 实测 744.71 GB/s",
   "url": U("developer.nvidia.com/blog/making-kubernetes-ai-ready-for-nvidia-vera-rubin"),
   "tag": "K8s × AI",
   "source": "NVIDIA Developer Blog",
   "note": "NVIDIA AI Cluster Runtime（AICR，属 DSX AI Factory Platform）把调好的集群配置写成 recipe，生成可交给现有部署工具的 bundle，并能对运行中的集群做验证。Vera Rubin NVL72 的 recipe 固化了这些选择：主机安装的 R615.23 开源内核模块驱动、带 ComputeDomain 的 DRA driver v0.5.0、64k page 内核的 Ubuntu 26.04、NFD topology updater 的内存上限。在 Vera Rubin NVL72 参考集群上用 GPU Operator v26.7.0 + DRA driver v0.5.0 跑通部署、一致性与跨节点 NCCL all-reduce 性能门禁（16 GiB 消息在 NVLink 上 744.71 GB/s）。验证中还发现 go-nvlib 不认识 Rubin 架构值、导致 DRA kubelet plugin CrashLoop 的 bug，修复已随 v0.5.0 发布。Vera Rubin 换用 ConnectX-9 SuperNIC 与 BlueField-4 DPU（DOCA 3.3.0），每个 tray 暴露 8 个 ConnectX-9 PCI device group、32 个 function，而 GB200 tray 是 4 张 ConnectX-7。",
   "summary": "NVIDIA 在 Vera Rubin NVL72 早期硬件上把「驱动 + DRA + 内核 + 网络」的组合写成可复现的 AICR recipe：R615.23 开源内核模块驱动、带 ComputeDomain 的 DRA driver v0.5.0、64k page 内核的 Ubuntu 26.04，加上 NFD topology updater 的内存上限。GPU Operator v26.7.0 部署后跑通跨节点 NCCL all-reduce，16 GiB 消息在 NVLink 上的 bus bandwidth 达到 744.71 GB/s。验证过程还揪出一个 go-nvlib 不认识 Rubin 架构值、让 DRA kubelet plugin CrashLoop 的 bug，修复已进 v0.5.0。",
   "detail": [
    {"key": "能做什么", "value": "AICR 把集群配置抽象成 recipe（驱动版本、内核页大小、DRA 驱动与 ComputeDomain、NFD 参数、网络栈），一条命令生成交给现有部署工具的 bundle，再用 aicr validate 在真机上跑部署、一致性、性能三道门禁并输出签名证据。"},
    {"key": "解决什么痛点", "value": "新 GPU 平台上线时驱动、内核、运行时、网络与调度器版本互相咬合，错一个就跑不起来或性能腰斩；这些组合散落在各家博客和内部文档里，换一批节点就要重新踩一遍。"},
    {"key": "值不值得", "value": "比具体版本号更值得抄的是「配方 + 验证门禁」这个方法：把 NCCL bus bandwidth 当验收门槛，比只看 Pod Running 靠谱得多。限制是只覆盖 NVIDIA 自家栈，Vera Rubin 尚未官方支持（R615.23 是测试版本，R620 才是官方平台支持），MIG 新 profile 与 Network Operator 兼容性都没纳入本次验证。"}
   ]
  }
 ],
 "sections": [
  {
   "label": "🤖 AI 板块",
   "categories": [
    {"label": "🧠 模型与研究", "items": [
      {
       "title": "LeCun 新论文给「柏拉图表征假说」补上证明：1.09 亿参数 JEPA 的跨模态对齐分超过 Qwen2.5-72B",
       "url": U("infoq.cn/article/pWwkDpoFHIsfw9aCRkij"),
       "summary": "10 月 29 日 LeCun 与布朗大学助理教授 Randall Balestriero 发布 37 页论文，用数学框架说明：不同模态的 JEPA 若按「Good Views」（同一场景的有效观察）构造正样本训练，学到的表征空间只差一个旋转变换。实验里 1.09 亿参数的文本 JEPA 在跨模态对齐指标拿到 0.184，高于 Qwen2.5-72B 的 0.154，参数差约 660 倍；达到同等对齐水平只需 2160 万样本，下一 token 预测要 9 亿（按 token 数算约 14 倍）。作者明确：比较的是表征对齐，不是推理、代码或问答能力。",
       "source": "InfoQ中国",
       "tag": "论文",
       "detail": [
        {"key": "能做什么", "value": "给出「不同模态独立训练也能对齐」的充分条件：正样本必须是同一潜在世界状态的不同观察（Good Views），而非同一段文本的前缀-续写或同图遮挡；满足条件时两个 JEPA 的表征只差一个旋转，可用线性变换对齐。"},
        {"key": "解决什么痛点", "value": "多模态对齐长期靠堆参数、堆配对数据，成本高且说不清为什么有效；这篇把「数据关系怎么构造」提到比规模更前的位置，并给出可测的对齐指标。"},
        {"key": "值不值得", "value": "做多模态预训练或需要跨模型表征复用的值得读原文的样本构造部分；不适合直接拿去判断「小模型能否替代大模型」——指标只测表征对齐，与通用能力无关，且 Good Views 的工程化构造没给成本数据。"}
       ]
      },
      {
       "title": "GPT-6.2 Astra 开始灰度、Claude Mythos 5.5 同日曝光：20% 请求被路由，Mythos 假权重被下 5000 次",
       "url": U("qbitai.com/2026/11/507082"),
       "summary": "11 月起部分 Pro 用户的模型列表出现 GPT-6.2-Astra 且可直接使用：有用户 20% 的请求被路由到 6.2，也有用户 100% 命中，灰度基本集中在 500 美元档。同一天 Claude Mythos 5.5 短暂出现在 Anthropic 官网前端代码里、几小时后被移除，据报道是偏生物学研究与网络安全的版本；HuggingFace 上一个声称是 Mythos 泄露权重的仓库被下载 5000 多次。",
       "source": "量子位",
       "tag": "灰度",
       "detail": [
        {"key": "能做什么", "value": "两家都在用灰度/前端泄露的方式放风：Astra 按用户比例路由真实请求，Mythos 5.5 只在前端代码里露名，权重仓库是假的但下载量说明市场对开源权重的需求。"},
        {"key": "解决什么痛点", "value": "对新模型能力的判断只能靠零星灰度截图，缺少可复现的评测口径；泄露权重则带来「下到假货还以为能用」的风险。"},
        {"key": "值不值得", "value": "跟踪即可，别据此做选型：Astra 没有公开评测，Mythos 5.5 连发布都没有。真正要留意的是灰度比例机制——按比例路由意味着同一账号不同请求可能落到不同模型，做 A/B 与回归测试时要把这个变量控住。"}
       ]
      },
      {
       "title": "colibri：纯 C 零依赖推理引擎，MoE 专家按需从磁盘流式加载，46.5k star",
       "url": U("github.com/JustVugg/colibri"),
       "summary": "JustVugg/colibri 用纯 C 实现、零第三方依赖，把 MoE 的专家权重放在磁盘上按需流式读取，让前沿规模的 MoE 模型能在已有硬件上跑起来，仓库已 46.5k star。取舍很直接：用磁盘 IO 换显存占用，适合显存不够、对吞吐不敏感的单机场景。",
       "oss": True,
       "source": "GitHub Trending",
       "tag": "开源",
       "detail": [
        {"key": "能做什么", "value": "纯 C、无依赖的推理引擎，专家权重不常驻显存而是按 token 路由结果从磁盘流式读取；模型规模受磁盘与内存带宽约束，而不是显存容量。"},
        {"key": "解决什么痛点", "value": "前沿 MoE 的权重远超单机显存，常规做法要么多卡要么量化掉精度；流式加载让「一台有 NVMe 的机器跑大 MoE」成为可能。"},
        {"key": "值不值得", "value": "作为边缘/离线实验值得试，判断标准是 token/s 与磁盘寿命——专家随机读取对 NVMe 的压力很大。生产推理仍应走 vLLM/SGLang 这类常驻显存的路径，这个项目的价值在于把「显存不够怎么办」的边界推开一点。"}
       ]
      }
    ]},
    {"label": "🧩 Agent & Skill", "items": [
      {
       "title": "Buildkite 给 CI 加了三个 MCP 工具：校验流水线 YAML、对比失败构建、补 Webhook，密钥收到流水线作用域",
       "url": U("infoq.cn/article/WmlATgJudjwPKqHf4QgX"),
       "summary": "Buildkite 的开源 MCP server 新增 validate_pipeline：按官方 schema 校验流水线 YAML 的语法与结构，不上传文件、不触发构建，直接返回路径和错误给编码 agent 修，但不覆盖环境变量插值、插件配置、依赖引用和动态生成步骤。compare_builds 把失败构建与同分支上次成功构建（或指定构建）对比，报出哪些步骤新增失败、已恢复、仍失败，并附运行时长与重试变化，对最多三个新失败步骤还带日志尾部。create_pipeline_webhook 给已有流水线补上缺失的 GitHub Webhook。凭证侧推出流水线作用域密钥：值创建后保持隐藏，可按分支、队列、构建来源、创建者加访问条件，CLI 3.59.1 支持从 GitHub Actions 迁移密钥。Agent v4.1.0 把缓存保存/恢复的耗时与大小、提交/PR/发起人写进 OTel job span；GitHub Actions 兼容层补上 Linux arm64，ubuntu-24.04-arm 这类标签需显式配置队列映射、不会回退 x86。1.23.0 把 create_pipeline 改为必须指定 create_webhook，是破坏性变更。",
       "source": "InfoQ中国",
       "tag": "Agent 工具",
       "detail": [
        {"key": "能做什么", "value": "给 CI 场景补三个专用工具而不是让 agent 硬读全量日志：validate_pipeline 做 schema 级校验、compare_builds 做构建间差异与日志尾部取证、create_pipeline_webhook 修配置；配套流水线作用域的密钥与分支/队列/来源条件，另有 OTel span 里的缓存耗时与提交元数据。"},
        {"key": "解决什么痛点", "value": "agent 改 CI 配置最容易写错 YAML 结构，而错误要等上传触发构建才暴露；构建失败时只能把几千行日志塞进上下文，既贵又抓不住「哪一步是新坏的」；集群级密钥对流水线过宽，泄露面大。"},
        {"key": "值不值得", "value": "他的流水线若已经在用 agent 改 CI（或准备让 agent 直接提 PR 改 pipeline），validate_pipeline + compare_builds 这个组合可以直接照搬思路，哪怕底层不是 Buildkite。注意 validate 不管 env 插值、插件与动态步骤，别把它当完整校验；1.23.0 的 create_pipeline 变更会让旧调用失败。"}
       ]
      },
      {
       "title": "worktrunk：给并行 agent 一人一个 git worktree 的 CLI，10k star",
       "url": U("github.com/max-sixty/worktrunk"),
       "summary": "max-sixty/worktrunk 是 Rust 写的 git worktree 管理 CLI，专门服务「多个 AI agent 并行改同一个仓库」：每个 agent 分到独立 worktree，不抢工作区和索引，创建、切换、清理与状态查看由一条命令统一处理，已 10k star。相比多 clone，worktree 共享同一份对象库，省磁盘也省 fetch。",
       "oss": True,
       "source": "GitHub Trending",
       "tag": "开源",
       "detail": [
        {"key": "能做什么", "value": "把 git worktree 的创建/切换/删除/状态做成单一 CLI，按分支或任务给每个 agent 一个独立工作目录，共享对象库；适合同时跑多个编码 agent 或并行 PR。"},
        {"key": "解决什么痛点", "value": "多个 agent 共用一个工作区会互相覆盖未提交改动、抢 index 锁；多 clone 又要重复 fetch 与磁盘。"},
        {"key": "值不值得", "value": "如果他的工作流里已经在并行跑多个 agent（Codex/Claude Code 各开一个），这是低成本隔离手段，比给每个 agent 配容器轻。限制是 worktree 只隔离工作区，不隔离端口、依赖缓存与构建产物，重活还是要容器或沙箱。"}
       ]
      },
      {
       "title": "agent-desktop：把 computer use 做成 CLI，agent 用命令行驱动本机桌面（Rust，9.6k star）",
       "url": U("github.com/vercel-labs/agent-desktop"),
       "summary": "vercel-labs/agent-desktop 把桌面操作包装成 CLI：agent 通过命令点击、输入、截屏、读窗口，不必为每个任务写一套 GUI 自动化胶水；Rust 实现，9.6k star。定位是给 agent 一个可脚本化的「手」，而不是再做一个视觉模型。",
       "oss": True,
       "source": "GitHub Trending",
       "tag": "开源",
       "detail": [
        {"key": "能做什么", "value": "以 CLI 暴露桌面控制原语（鼠标、键盘、截图、窗口信息），agent 用 shell 调用即可操作本机 GUI 应用，配合自己的视觉/规划模型使用。"},
        {"key": "解决什么痛点", "value": "GUI 自动化通常绑死在某个 agent 框架里，换模型就要重写；把能力降到 CLI 层后，任何能执行命令的 agent 都能用，也便于在容器/VM 里替换。"},
        {"key": "值不值得", "value": "与他关注的 agent 沙箱直接相关：沙箱里要给 agent 一套可控的桌面操作面，CLI 形态比 SDK 更容易做权限包裹与审计。限制是只覆盖单机 macOS/Linux 桌面，没有并发会话隔离，多租户还得靠外层容器。"}
       ]
      },
      {
       "title": "深空之序把 FDE 的现场经验做成 Skill：报关单从 3 小时压到 5 分钟，单份成本 70 元降到 10 元",
       "url": U("infoq.cn/article/FckEhkVfCLoXg0jvaKBa"),
       "summary": "深空之序（芦宇峰与前钉钉 CEO 叶军创办）COO 芦宇峰在 1024 模力工场分享 FDE 方法论：先亲手把业务做一遍，弄清老师傅凭经验做的判断与流程里的例外，再把资料整理进知识库、把解法沉淀成可复用 Skill，并配覆盖真实场景与客户运行环境的测试用例，避免「开发时没问题、到现场用不了」。刺绣项目里他们先试 Computer Use 复刻老师傅操作，发现图案要剪线打结 700 多次这类工艺判断复制不了，改用两万多套标注数据做后训练，从原图 + 面料 + 针法直接生成针迹文件，难度 1-5 的图案做到分钟级产出。义乌报关项目把多数报关单制作时间从至少 3 小时压到约 5 分钟，单份成本从约 70 元降到约 10 元。",
       "source": "InfoQ中国",
       "tag": "Skill 实践",
       "detail": [
        {"key": "能做什么", "value": "把「驻场做一遍业务 → 抽判断规则与例外 → 知识库 + 可复用 Skill + 真实环境测试用例」做成交付流程；技术选型上明确放弃用 Computer Use 复刻专家操作，改用标注数据 + 后训练直接产出结构化文件（针迹文件/报关单）。"},
        {"key": "解决什么痛点", "value": "企业 AI 交付失败多发生在「演示能跑、现场不能用」：专家经验没被显式化，测试用例只覆盖开发环境的理想输入，交付完人一走就退化成一次性项目。"},
        {"key": "值不值得", "value": "这套「经验 → Skill + 用例」的沉淀方式可直接搬到他给同事做 skill 的实践里，尤其「测试用例必须覆盖客户运行环境」这条。注意它本质是咨询交付方法论，效果依赖驻场成本；两个案例都是垂直行业，通用性未经检验。"}
       ]
      },
      {
       "title": "Google Cloud 把开发者插件上架 Antigravity Marketplace：给编码 agent 补 IAM 与 SDK 上下文",
       "url": U("cloud.google.com/blog/topics/developers-practitioners/google-cloud-developer-plugin"),
       "summary": "google-cloud-developer 插件现在可直接在 Antigravity Marketplace 安装，给编码 agent 注入云侧上下文，避免它编造已废弃的 SDK 语法、猜错命令参数，或在没有 IAM 权限时反复试错。官方点出的风险是：没有这类上下文时，agent 可能自行开通计费 API、擅自创建云资源。",
       "source": "Google Cloud",
       "tag": "生态",
       "detail": [
        {"key": "能做什么", "value": "把 Google Cloud 的 SDK 版本、命令参数、IAM 权限模型作为插件上下文提供给 Antigravity 里的编码 agent，减少臆造 API 与越权尝试。"},
        {"key": "解决什么痛点", "value": "编码 agent 对云 API 的「记忆」经常过期，生成已废弃语法或错误 flag；更危险的是它在没有权限时不断试探，甚至开通计费服务。"},
        {"key": "值不值得", "value": "思路值得抄：给 agent 的云上下文要包含权限边界与计费影响，而不只是 API 文档。限制是绑定 Antigravity 生态，非 GCP 环境只有方法论价值。"}
       ]
      }
    ]},
    {"label": "🛠️ AI 工程落地", "items": [
      {
       "title": "Qodo 用 Codex 插件把公司编码规范带进评审：目标是在开 PR 前拦下 P0 问题",
       "url": U("openai.com/index/qodo-codex-plugin"),
       "summary": "Qodo 通过 Codex 插件把公司知识与编码规范注入 AI 代码评审，让 agent 在跨仓库场景下理解内部约定，目标是在开发者开 PR 之前就发现 P0 级问题，而不是等 CI 或人工 review 兜底。插件形态让评审上下文留在开发者的编码环境里，而不是另开一个评审 SaaS。",
       "source": "OpenAI News",
       "tag": "工程",
       "detail": [
        {"key": "能做什么", "value": "把企业内部规范、历史代码模式作为上下文提供给 Codex，在编码阶段就做跨仓库的评审判断，输出 P0 级问题。"},
        {"key": "解决什么痛点", "value": "通用代码评审模型不懂公司约定，容易放过真正会出事的改动、又在风格问题上刷噪音；等 PR 阶段才发现，返工成本已经产生。"},
        {"key": "值不值得", "value": "值得关注的是「规范作为上下文」这个位置——评审规则应该和代码同仓、可版本化，而不是散在提示词里。限制是官方只给了定位，没有给出误报率或拦截率数据，无法判断实际收益。"}
       ]
      }
    ]},
    {"label": "📊 产品与商业", "items": [
      {
       "title": "百度搜索 AI API 压到 4.9 元/千次，抢的是 Agent 的默认检索入口",
       "url": U("infoq.cn/article/HJgTwfsPAugNBJ2jUefj"),
       "summary": "百度 10 月 30 日升级搜索 AI API：增强版活动期最低 4.9 元/千次、旗舰版 9.9 元/千次，官方称低于 DeepSeek 搜索 API，同时开放 API、MCP、Skill 三种接入方式。其四层架构里的「RSI」闭环把每次真实检索与用户反馈沉淀成训练信号回流模型，官方称迭代效率提升 80% 以上；支持百万级并发调用，文心助手接入后效果提升 20%。社区争议点是 4.9 元属限时活动价，迁移决策更看检索质量、权威性与完成一个任务所需的调用次数。",
       "source": "InfoQ中国",
       "tag": "价格",
       "detail": [
        {"key": "能做什么", "value": "搜索能力以 API/MCP/Skill 三种形态对外，增强版 4.9 元/千次、旗舰版 9.9 元/千次；内容层聚合 80 余种语言索引，引擎层用在线反馈闭环 + 多 Agent 协同做「检索—反馈—再训练」。"},
        {"key": "解决什么痛点", "value": "Agent 做检索时按次计费，调用次数一多成本失控；百度想用低于 DeepSeek 的单价把搜索变成 Agent 的默认工具调用。"},
        {"key": "值不值得", "value": "自建 RAG 的团队可以按「完成一个任务的总调用次数 × 单价」重算一次成本，而不是只看千次单价。注意 4.9 元是限时活动价，且检索质量/时效性没有第三方对比数据，先小流量验证再谈迁移。"}
       ]
      },
      {
       "title": "ChatGPT Pro 额度全面翻倍：Pro 500 相当于 Plus 的 50 倍，但撤降额被算进「升级」引发不满",
       "url": U("infoq.cn/article/WpTNht7guarWEyejJFV6"),
       "summary": "OpenAI 产品负责人 Tibo 宣布 Pro 100/200/500 与 Business Premium 额度全面翻倍，并撤回此前对 Pro 200 的降额计划，Pro 500 确认相当于 Plus 的 50 倍用量；这是其 28 天产品改进计划的第 25 天。社区并不全买账：Pro 200 用户指出自己只是没被降额、并非新增权益，Plus 用户不满低价档未覆盖，额度调整与订阅权益的落差此前已在美国引发对 Anthropic 的集体诉讼。",
       "source": "InfoQ中国",
       "tag": "订阅",
       "detail": [
        {"key": "能做什么", "value": "Pro 100/200/500 与 Business Premium 的使用上限翻倍，Pro 500 = Plus 的 50 倍；Dots 的扩容额度独立于账户默认额度，不计入。"},
        {"key": "解决什么痛点", "value": "Agent 化之后 Codex/后台任务会在用户无感知时消耗额度，重任务用户经常撞限额；翻倍是对这类工作负载的容量补充。"},
        {"key": "值不值得", "value": "重度用 Codex 的可以按新上限重新算单位成本；但「撤回降额」不等于新增权益，企业采购时应把额度写入合同条款（按 5 小时窗口还是周累计），Anthropic 的诉讼就是栽在这个口径上。"}
       ]
      }
    ]},
    {"label": "💡 观点与好文", "items": [
      {
       "title": "企业 Agent 的边界在哪：飞猪用求解器算票价、货拉拉灌物流知识、江苏移动用 Harness 兜底",
       "url": U("infoq.cn/article/UMvAAwoFByxvWLLVVJYY"),
       "summary": "InfoQ 圆桌上飞猪、货拉拉、江苏移动的实践者给企业 Agent 划边界：飞猪用模型做需求理解、票组合与总价交给求解器保证可复算，酒店房型 ID 这类业务主键用短 ID 替换、展示时再回溯，涉及钱包的权益必须用户二次确认；货拉拉把物流知识灌进系统，让 Agent 先理解「运双开门冰箱该选什么车」；江苏移动用 Harness 校验 Agent 能力，并指出不限重试与并发时，一个失控智能体会把整个生产带崩。共识是「用 AI 生成规则、用规则执行关键环节」：可解释、可撤回、可控。",
       "source": "InfoQ中国",
       "tag": "实践",
       "detail": [
        {"key": "能做什么", "value": "给出四层可落地的边界设计：意图理解交给模型、计算与组合交给求解器、业务主键脱敏替换、资金与权益动作必须人工确认；平台侧用 Harness 校验 agent 输出，并在网关限制重试与并发。"},
        {"key": "解决什么痛点", "value": "模型进入交易链路后，一次幻觉就是真实损失（价格、库存、房型 ID）；更隐蔽的是 agent 无意识的重试打爆内部接口——有案例把接口打崩半个多小时。"},
        {"key": "值不值得", "value": "这几条边界比任何「agent 框架」都更接近生产现实，尤其「业务 ID 不交给模型」与「网关防 agent 的重试风暴」，可直接用到公司多用户 agent 产品的权限与限流设计里。限制是均为经验分享，没有给出拦截率等量化指标。"}
       ]
      }
    ]},
    {"label": "🛡️ 安全与治理", "items": [
      {
       "title": "Mandiant 记录 LLMJacking：单日盗刷超 10 万美元、累计到 100 万美元，已出现 LLM Mixer 转售网关",
       "url": U("cloud.google.com/blog/topics/threat-intelligence/llmjacking-monetizing-compromised"),
       "summary": "Mandiant 披露 2026 年多起 LLMJacking 事件：攻击者用泄露的 IAM 凭据、Service Account key、GitHub PAT 和活跃会话 token 接管企业 LLM 访问，单个事件单日盗刷可超 10 万美元，部分组织在权限被收回前累计达 100 万美元，波及北美、南美与亚太的金融、零售、科技、运输行业。初始入口除公开暴露的 Ollama 端点（攻击者直接调 /api/create 跑自己的模型）外主要是云身份凭据；有团伙用 max_tokens=1 的单 token 请求批量验证盗来的 key 以躲过 EDR。生态里已出现 LLM Mixer——代理、聚合、转售未授权 LLM 访问的中转网关；UNC6993 用伪装成应用门户的会话劫持页骗用户粘贴含 token 的 JSON 以绕过 MFA。",
       "source": "Google Cloud",
       "tag": "安全",
       "detail": [
        {"key": "能做什么", "value": "给出完整攻击链与检测面：暴露的 Ollama/LLM 端点、云 IAM 与 SA key、GitHub PAT、会话 token 都是入口；检测信号包括异常 API 调用曲线、大量 max_tokens=1 的探测请求、以及来自 LLM Mixer 中转 IP 的流量。"},
        {"key": "解决什么痛点", "value": "LLM 盗刷不像挖矿那样慢速爬升，几小时就能刷出巨额账单；而 LLM key 往往被当成低敏感度配置散落在 CI、Notebook 和前端。"},
        {"key": "值不值得", "value": "做金融量化的尤其该看：审计要求能追到「谁在什么时候用了哪个模型」，而这类攻击正好发生在身份层。可落地的三件事是 LLM 端点不出公网、key 按工作负载签发并设额度上限、把单 token 探测与异常用量做成告警。"}
       ]
      },
      {
       "title": "OpenAI 重写 Model Spec：第一条从「服从指令」改成「忠于人类意图」，明确禁止自我保存与囤算力",
       "url": U("qbitai.com/2026/11/507225"),
       "summary": "OpenAI 更新 5 万字的 Model Spec，把准则收敛成 5 条价值观，第一条是「忠于人类意图」：死板按字面执行被视为失职，模型要结合任务目的、上下文、记忆与用户长期利益判断真实意图（问「牙仙子是真的吗」的可能是小孩）。其余四条是减少伤害、诚实透明、促进人的自主性、关怀。准则明确禁止模型追求自我保存、逃避关机、私自囤积算力/数据/凭证，禁止把「帮 OpenAI 赚钱」或提升停留时长当目标，并要求超出授权范围的现实行动（发邮件、删文件、花钱、调外部工具）立刻停止。",
       "source": "量子位",
       "tag": "治理",
       "detail": [
        {"key": "能做什么", "value": "把模型行为规范拆成 5 条价值观 + 分级权限标签（硬性规则 / 指导方针），并对记忆使用给出边界：区分长期指令、偏好、事实、项目状态，只有收益大于风险时才调用记忆，短期指令与长期任务冲突时做提醒者而非决策者。"},
        {"key": "解决什么痛点", "value": "agent 接手真实操作后，「字面服从」反而危险——用户说错一句就执行；同时厂商默认目标（停留时长、收入）会悄悄污染模型行为。"},
        {"key": "值不值得", "value": "写自己 agent 的系统提示时，这份 spec 的「忠于意图 + 可纠正性 + 授权范围外立即停」三段可直接借用为骨架；注意它是厂商自律文档，没有对应的评测或审计机制，别当成合规证明。"}
       ]
      }
    ]}
   ]
  },
  {
   "label": "☸️ 基础设施板块",
   "categories": [
    {"label": "🤖☸️ K8s × AI", "items": [
      {
       "title": "KAI-Scheduler v0.18.7：gpu-fractioning 改为构建期解析的依赖，绑定期间保留 GPU 预留",
       "url": U("kai-scheduler/KAI-Scheduler/releases/tag/v0.18.7"),
       "summary": "KAI-Scheduler v0.18.7 把捆绑的 gpu-fractioning chart 声明为 ~0.1.0 范围的依赖、在构建时解析版本，具体版本写在发布产物的 subcharts.yaml 里；同时修了 binder 在绑定请求可重试期间丢失 GPU 预留的问题，以及更新已有 GPU 共享 ConfigMap 时的 nil 数据 panic，并允许 kai-config-deployer hook job 在 OpenShift 上运行。",
       "oss": True,
       "source": "GitHub Releases",
       "tag": "GPU 调度",
       "detail": [
        {"key": "能做什么", "value": "GPU 分数化（fractioning）子 chart 的版本由构建期决定并可追溯；binder 在绑定失败重试时保留已分配的 GPU 预留，不再重复抢占；GPU 共享 ConfigMap 更新不再 panic；OpenShift 上 hook job 可直接跑。"},
        {"key": "解决什么痛点", "value": "GPU 共享场景下绑定重试会重复占卡，队列里看着有卡实际调度不出去；子 chart 版本随源码漂移，出问题无法复现。"},
        {"key": "值不值得", "value": "跑 GPU 共享/分数卡的多租户集群值得升，尤其是 OpenShift 环境。限制是 patch 版本、只修调度正确性，不含新调度策略；分数化的语义仍要配合 device plugin 与 DRA 侧配置才完整。"}
       ]
      },
      {
       "title": "Kueue v0.19.11：回移 DRA 陈旧 ResourceSlice 修复，调度器日志级别调整会打挂现有看板",
       "url": U("kubernetes-sigs/kueue/releases/tag/v0.19.11"),
       "summary": "Kueue v0.19.11 把 DRA 的 CEL 设备可用性检查修到不再统计陈旧/不完整 ResourceSlice 池里的设备（此前 Workload 会为 DRA 分配器用不了的设备预留配额），并修了 LimitRange 默认设备请求在 DeviceClass 建好后仍 Pending、弹性 Job 就绪判定按最新已准入切片的 replica 数计算。同一版本改了调度器日志级别：per-Workload 消息默认留在 level 2，启用 LogLevelForSchedulerMainLoop 后要 level 3 才保留，「Workload skipped from admission」从 level 0 挪到 level 2。",
       "oss": True,
       "source": "GitHub Releases",
       "tag": "调度",
       "detail": [
        {"key": "能做什么", "value": "修正 DRA 配额按陈旧 ResourceSlice 误算、LimitRange 默认设备请求卡 Pending、弹性切片就绪判定三类问题；日志按 gate 分层，per-Workload 细节要显式开 gate 并调到 level 3。"},
        {"key": "解决什么痛点", "value": "DRA + Kueue 混用时配额看起来被占、实际设备不可用，队列长期卡住；而升级后日志键与级别变化会让基于日志的告警和看板静默失效。"},
        {"key": "值不值得", "value": "跑 Kueue + DRA 的集群应该升（0.20.4 的同款修复已回移到 0.19 线）；升级前先 grep 一遍依赖 Kueue 日志消息的告警规则，这是最容易在升级后「看不见故障」的地方。"}
       ]
      }
    ]},
    {"label": "☸️ K8s 核心技术", "items": [
      {
       "title": "Envoy v1.39.6 只为换掉 distroless 里的 ca-certificates：1.39.5 仍在信任被攻破的 eMudhra 中间 CA",
       "url": U("envoyproxy/envoy/releases/tag/v1.39.6"),
       "summary": "Envoy v1.39.6 是单点安全发布：distroless 基础镜像更新到 20250419+deb13u1 版 ca-certificates，不再信任被攻破的 eMudhra 中间 CA 根；1.39.5 的 distroless 镜像仍在用未修复的证书包。这是这轮供应链事件波及的又一个基础组件，与 metrics-server 重建镜像属同一批动作。",
       "oss": True,
       "source": "GitHub Releases",
       "tag": "供应链",
       "detail": [
        {"key": "能做什么", "value": "只换证书包、不改代码：distroless 镜像不再信任 eMudhra 被攻破的中间 CA，其余行为与 1.39.5 一致。"},
        {"key": "解决什么痛点", "value": "被攻破的中间 CA 能签出浏览器与客户端都信任的证书，留在镜像里等于给中间人留后门；而这种根证书通常藏在基础镜像、不在依赖清单里，扫描器也未必报。"},
        {"key": "值不值得", "value": "集群里跑 Istio/Envoy 网关的要升，并顺手查一遍自建镜像的 ca-certificates 版本——这轮已经波及 metrics-server、Dynamo、Envoy 等多个组件。注意这是 patch 级替换，升级风险低但需要重启数据面。"}
       ]
      }
    ]},
    {"label": "🌐 云原生周边", "items": [
      {
       "title": "Argo CD v3.5.7：Rollout 无 status 时也能列出 actions，容器镜像带 cosign 签名与 SLSA L3 来源",
       "url": U("argoproj/argo-cd/releases/tag/v3.5.7"),
       "summary": "Argo CD v3.5.7 在 3.5 线上修了两个小问题：Rollout 没有 status 时也能列出 Rollout actions，以及应用删除提示只在使用文本输出格式时打印。发布镜像由 cosign 签名，并提供 SLSA Level 3 的 provenance，可用于验证来源。",
       "oss": True,
       "source": "GitHub Releases",
       "tag": "GitOps",
       "detail": [
        {"key": "能做什么", "value": "修 Rollout actions 与删除提示的输出问题；镜像带 cosign 签名和 SLSA L3 provenance，可在准入阶段做签名校验。"},
        {"key": "解决什么痛点", "value": "Rollout 无 status 时 UI/CLI 拿不到 actions，排障只能翻 CR；供应链侧则需要可验证的镜像来源才能上 admission policy。"},
        {"key": "值不值得", "value": "在 3.4/3.3 的可以评估一并升级（同日也发了 3.4.13、3.3.19）；真正值得用的是签名与 provenance——若集群已上 Kyverno/Sigstore，可以直接把 Argo CD 镜像纳入验签策略。"}
       ]
      }
    ]},
    {"label": "🏘️ 社区与项目", "items": [
      {
       "title": "Linkerd 十周年纪录片在 KubeCon NA 首映：Service Mesh 的口述史，11 月 9 日盐湖城",
       "url": U("cncf.io/blog/2026/11/02/the-linkerd-story"),
       "summary": "CNCF 与 Buoyant 将在 11 月 9 日盐湖城 KubeCon + CloudNativeCon North America 首映 Linkerd 纪录片，讲这个 service mesh 项目十年演进与背后的人。对正在选 mesh 的团队，这类口述史的价值在于看清 sidecar 模式的取舍是怎么一步步形成的。",
       "source": "CNCF Blog",
       "tag": "社区",
       "detail": [
        {"key": "能做什么", "value": "以纪录片形式记录 Linkerd 从 Twitter 内部项目到 CNCF 毕业项目的十年，包含早期设计与运维取舍的一手叙述。"},
        {"key": "解决什么痛点", "value": "选 mesh 时看到的都是特性表，很难知道某个设计（轻量 sidecar、Rust micro-proxy）是为了解决什么真实故障。"},
        {"key": "值不值得", "value": "对正在做 mesh 选型或要说服团队的人有参考价值；纯技术决策仍需看 linkerd2-proxy 与 Istio ambient 的实测数据，纪录片不解决这个。"}
       ]
      }
    ]}
   ]
  }
 ],
 "flash": [
  {"title": "llm 0.37：默认模型换成 gpt-6-luna（价格减半），新增 llm openai endpoint add 配置兼容端点", "url": U("simonwillison.net/2026/Nov/2/llm/")},
  {"title": "OpenAI 介绍 Pando：为 Codex 规模的开发重建的 Git 兼容后端", "url": U("openai.com/index/scaling-git-at-openai")},
  {"title": "datasette-llm 0.1a9：Datasette 的 LLM 插件跟进新版 API", "url": U("simonwillison.net/2026/Oct/31/datasette-llm/")}
 ],
 "footer": "由 Hermes 自动汇编 · 每日 09:00 更新"
}

# --- normalize categories: render.py reads title + emoji ---
for sec in brief["sections"]:
    for cat in sec["categories"]:
        cat["title"] = cat["label"]
        cat["emoji"] = EMOJI[cat["label"]]

# --- assert every item has a non-empty title + url ---
def walk(o):
    if isinstance(o, dict):
        if "url" in o:
            assert o.get("title"), f"missing title for {o['url']}"
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(brief)

json.dump(brief, open("briefing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = sum(len(c["items"]) for s in brief["sections"] for c in s["categories"])
print(f"wrote briefing.json: issue={brief['issue']} highlights={len(brief['highlights'])} section_items={n} flash={len(brief['flash'])}")
