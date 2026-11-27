#!/usr/bin/env python3
"""Build briefing.json for issue 067 (2026-11-27). URLs are looked up from processed.json by prefix."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
proc = json.load(open(os.path.join(BASE, "processed.json"), encoding="utf-8"))
BYURL = {it["url"]: it for it in proc}

def U(prefix):
    """Return the exact URL from processed.json whose URL starts with / contains prefix."""
    hits = [it["url"] for it in proc if prefix in it["url"]]
    assert len(hits) == 1, f"U({prefix}) -> {hits}"
    return hits[0]

DATE_LABEL = "2026 年 11 月 27 日 · 星期五"
ISSUE = 67

lead = (
 "今天的主线是「把 agent 的不确定动作换成可验证的工程闭环」。工程侧，海德堡大学算法工程组把可证伪假设、正确性断言与逐 patch 回滚写成 AAE skill，KaHIP 求解器跑完 122 次实验后整体快 3.9×，"
 "同一套流程的成果直接进了 DIMACS 挑战赛论文；另一头有人用 Claude 把 Rockbox 塞进 512 KiB SRAM 的 9 美元 MP3，再把成功路径沉淀成工具包，第二个机型只花 4 小时。"
 "运行时侧集体往「按需给资源」走：E2B 2.66.0 让模板定内存上限、创建时按需分配、暂停恢复时换规格，gVisor 则把 OCI seccomp 默认打开并加了挂载护栏。"
 "平台侧出现一条硬期限——Google 八套 Workspace MCP server 转 GA，2027 年 2 月 1 日起任何「由 AI agent 驱动」的工具必须走官方 MCP，而 Gmail 那套至今不能发信。"
 "基础设施这边，Dynamo v1.7.0 用 Global Router 把推理流量跨池调度、Sidecar 支持多机引擎故障迁移，Kubernetes v1.37.3 修掉调度器同名 Pod 快速重建崩溃。"
)

highlights = [
 {
  "title": "AAE：把「可证伪假设 + 正确性断言」写进 agent 循环，KaHIP 求解器 122 次实验后快 3.9×",
  "url": U("chszlab.github.io/AgenticAlgorithmEngineering"),
  "summary": (
   "海德堡大学算法工程组开源 AAE（Agentic Algorithm Engineering），一个给 Claude Code 和 Codex 用的算法优化 skill。"
   "用法是先和 agent 谈定基准、指标、正确性断言与实验预算，之后它自主循环四步：从 profiling 与分析出发写下可证伪假设（「改 X 会让指标提升约 Z，因为…」）、做最小改动并提交 Git、跑正确性断言、跑基准，只有「更快且仍正确」才保留，否则回滚。"
   "KaHIP kaffpa 会话的实测记录是 122 次实验、69 个假设、41 个被接受的 patch、整体 3.9× 加速；每次接受的改动都是一个可评审 patch，整场会话导出 PDF 报告，学到的技巧进跨会话共享知识库。"
   "同组把这套流程用在共享内存精确最小割上，成果进了 DIMACS Implementation Challenge 的论文（arXiv:2609.07204）。"
  ),
  "note": "AAE 由海德堡大学 Algorithm Engineering Group 发布，支持 Claude Code（/plugin install aae --marketplace CHSZLab/AgenticAlgorithmEngineering）与 Codex（scripts/install_codex_skill.py，调用 $aae），其他 agent 可跟随仓库里的 AAE.md。每轮实验强制三件事：先写方向与量级的可证伪假设、改动后跑正确性断言、跑基准并只在更好时保留。KaHIP kaffpa 会话累计 122 次实验、69 个假设、41 个 patch、3.9× 总加速。仓库带 10 分钟 quick-start（一个慢但正确的最短路程序 + 基准 + 正确性检查）。",
  "detail": [
   {"key": "能做什么", "value": "把算法工程的标准科研循环交给 agent：假设先行、单点最小改动、正确性断言兜底、基准不达预期就回滚。每一步都留可评审 patch 与 PDF 报告，人工只在 setup 阶段定基准与预算，中途不用盯。知识库跨会话累积优化技巧，agent 开工前先读。"},
   {"key": "解决什么痛点", "value": "一般的「让 agent 优化性能」是黑箱试错：改了哪里、为什么快、有没有偷偷牺牲正确性都说不清，回滚也回不干净。AAE 用可证伪假设强迫 agent 先讲清预期方向与量级，用正确性断言挡住「快但错了」，用 Git 单 patch 保证可回退——正好对上 code review 与论文复现的要求。"},
   {"key": "值不值得", "value": "值得。它示范的是 skill 的正确形态：不是一段提示词，而是一套带断言、带产物、带回滚的流程约束，这比任何「优化专用 agent」都更容易搬到自己领域（调度器、存储引擎、编解码）。门槛是得先有可重复的基准与正确性断言，否则循环没有裁判。"}
  ],
  "tag": "落地实践",
  "source": "CHSZLab"
 },
 {
  "title": "E2B 2.66.0：沙箱内存从「模板写死」变成可调——模板定上限、创建时分配、恢复时换规格",
  "url": U("e2b-dev/E2B/releases/tag/e2b@2.66.0"),
  "summary": (
   "E2B 2.66.0 把沙箱内存做成可调参数：构建模板时用 maxMemoryMB 设上限，创建沙箱时用 memoryMB 选实际内存，暂停的沙箱在 Sandbox.connect 恢复时可以指定新的内存与 CPU 数。"
   "onResume 在原有 'restore' / 'reboot' 字符串之外新增对象形式 {action, memoryMB, cpuCount}（Python 为 memory_mb / cpu_count），旧写法保持有效。"
   "规格只在该次 connect 真正恢复暂停沙箱时生效，沙箱承受不了的规格会被明确拒绝而不是静默降级。"
   "Template.list()、getInfo()、listBuilds() 现在返回 maxMemoryMB，CLI 的 template list 增加一列 Max RAM MiB。"
  ),
  "note": "变更集中在 SDK 的模板与生命周期接口：模板构建参数新增 maxMemoryMB；创建时传 memoryMB；Sandbox.connect 的 onResume 支持 {action, memoryMB, cpuCount} 对象（Python: memory_mb / cpu_count），与旧的 'restore' / 'reboot' 字符串并存。超出沙箱能力的规格会被拒绝。Template.list() / getInfo() / listBuilds() 返回 maxMemoryMB，e2b template list 新增 Max RAM MiB 列。",
  "detail": [
   {"key": "能做什么", "value": "同一个模板可以派生不同内存档的沙箱，并且能在暂停后按新规格恢复——把「沙箱规格」从部署期常量变成运行期参数。配合 CPU 数一起调，小任务不必为大模板付内存，大任务也能在恢复时临时加档。"},
   {"key": "解决什么痛点", "value": "多租户 agent 平台最浪费的两块就是内存与 CPU：模板为了兼容最大用例把上限拉高，所有沙箱都按上限计费；或者反过来把小任务塞进小模板，跑大任务时只能重建沙箱丢掉状态。可调内存 + 恢复时改规格让「状态保留」与「按需给资源」不再二选一，正好对上空闲挂起省资源的诉求。"},
   {"key": "值不值得", "value": "值得跟进。它是目前少数把「暂停-恢复-换规格」做成 SDK 一等公民的方案，直接对应自建 agent 沙箱平台的核心成本项；门槛是要注意恢复时才生效、且规格下发会被校验，容量规划需按 maxMemoryMB 留余量。"}
  ],
  "tag": "隔离运行时",
  "source": "GitHub Releases"
 },
]

def item(title, url, summary, detail, tag=None, source=None, oss=False):
    d = {"title": title, "url": url, "summary": summary, "detail": detail}
    if tag: d["tag"] = tag
    if source: d["source"] = source
    if oss: d["oss"] = True
    return d

ai_sections = []

ai_sections.append({
 "label": "🧩 Agent & Skill",
 "items": [
  item("AAE skill：用可证伪假设约束 agent 的每一次实验，41 个 patch 换来 3.9× 加速",
       U("chszlab.github.io/AgenticAlgorithmEngineering"),
       "海德堡大学算法工程组把算法工程循环做成 Claude Code / Codex 的 skill：setup 阶段与 agent 谈定基准、指标、正确性断言和预算，之后每轮先写可证伪假设、再提交最小改动、跑断言与基准，只有更快且正确才保留。KaHIP kaffpa 会话记录 122 次实验、69 个假设、41 个 patch、整体 3.9×。所有被接受的改动都是可评审的单 patch，整场会话导出 PDF 报告，技巧沉淀进跨会话知识库。",
       [{"key": "能做什么", "value": "把「先假设、后测量、不达预期就回滚」固化成 agent 的强制流程，并输出 Git 单 patch + PDF 报告两类可审计产物。提供 /aae 斜杠命令与 10 分钟 quick-start，其他 agent 可跟 AAE.md 走。"},
        {"key": "解决什么痛点", "value": "性能优化交给 agent 后最常见的失控是：说不清改了什么、说不清为什么快、正确性悄悄退化、想回滚找不到边界。AAE 用假设和断言把这三件事都变成硬约束。"},
        {"key": "值不值得", "value": "值得精读它的流程设计而不只是用。它证明「skill = 带断言的流程」比「skill = 提示词模板」可靠得多，可直接搬到调度器、存储引擎、编解码这类有基准的优化工作；前提是你得先有可重复基准。"}],
       tag="skill 设计", source="CHSZLab", oss=True),
  item("Google 要把 agent 的 Workspace 访问收进自家 MCP，但 Gmail 那个至今不能发信",
       U("techstackups.com/articles/google-workspace-ai-agents-mcp"),
       "11 月 24 日 Google 把八套 Workspace MCP server 转为 GA，同时在 API 条款里加了 Workspace AI Tools Addendum：2027 年 2 月 1 日起，任何「本身是、或由 AI agent / AI harness / AI 模型驱动」的工具访问 Gmail、Drive、Calendar 必须走 Google 的 MCP server，伪装成非 agent 规避被明确禁止，违反可被切断访问或停号。技术面同步收紧——同日起来直接调 REST 的 agent 一律按 Standard 档配额限速，无论项目付费到哪一档。Gmail server 只能搜信、读串、建草稿、打标签，发信/回复/转发/改草稿都标注「需要 partner access，未 GA」。",
       [{"key": "能做什么", "value": "用条款把 agent 的 Workspace 数据通路统一到官方 MCP，同时用配额档位让绕过 MCP 直连 REST 的 agent 降速；非 AI 的确定性脚本、备份任务、CRM 同步不受影响。"},
        {"key": "解决什么痛点", "value": "Google 要在「让 agent 能用 Workspace」和「不让 agent 无限制读写邮件」之间划界。对平台方是治理手段，对开发者则是能力天花板：官方 MCP 拿不到发信权限，业务就断在最后一步。"},
        {"key": "值不值得", "value": "值得当作合规截止日记下来：2027-02-01 前要判定自建 agent 是否踩到定义，以及是否接受「只能读到草稿、发不出去」的功能边界。想做完整邮件自动化的，路子只剩 partner access 或换通道。"}],
       tag="政策", source="Tech Stackups"),
 ]
})

ai_sections.append({
 "label": "🧭 Agent 工具链",
 "items": [
  item("Orca v1.4.278：Gemini CLI 被移除、Antigravity 全面改用 agy，下载可直接流到本机",
       U("stablyai/orca/releases/tag/v1.4.278"),
       "这一版把 Antigravity 全部切到 agy 上跑，且能在 Orca 内直接完成 agy 登录；同时移除 Gemini CLI 支持，官方理由是 Google 已把用户导向 Antigravity。新增 ClickUp、Airtable、Todoist、Zapier、Granola、Intercom 六个应用一键接入，不再需要 Composio 账号。在服务端工作区里下载的文件可以流式保存到本机（内存占用保持平稳，不整包读进内存）。Bots 支持静音、老会话折叠到 Show N older；New bot 的 Computer 选择器可直接加 WSL 发行版（实验性），新建 bot 默认用默认 agent 而不是永远 Claude。长回复改为逐词流式增长，打字不再卡顿。",
       [{"key": "能做什么", "value": "把多家 agent 的入口统一成一个 ADE：Claude、Codex、Antigravity(agy)、Qwen Code 可混用，Bots 能跨多台电脑组队、按计划或事件触发，连接器从 Composio 依赖里解耦出来一键接。"},
        {"key": "解决什么痛点", "value": "多 agent 并行的实际瓶颈在「切换成本」和「产物带不走」：不同 CLI 各自的登录与配额、在远端工作区跑出的文件要手动搬。Orca 这两版在收这两个口子。"},
        {"key": "值不值得", "value": "值得跟版本但不急着切。移除 Gemini CLI 是一个信号——上游把流量导向 Antigravity 后，第三方 ADE 只能跟着改；如果你的 workflow 依赖 Gemini CLI 参数，升级前先确认 agy 是否能等价替代。"}],
       tag="release", source="GitHub Releases", oss=True),
  item("OpenCode v2.4.2：GPT-6.2 专用系统提示，图像/视频生成收进 Code Mode 每请求省约 700 token",
       U("anomalyco/opencode/releases/tag/v2.4.2"),
       "v2.4.2 为 GPT-6.2 Sol / Astra 以及 gpt-latest 别名换上专门写的系统提示；generate_image 与 generate_video 从顶层工具移进 Code Mode 执行，工具定义不再给每个请求加约 700 token。安全侧收紧：网页抓取的「总是允许」从放行所有 URL 改成只放行该站点，旧版本保存的授权保持不变。可靠性侧，automation 一次失败后仍按计划继续跑（只有创建它的会话/目录消失或配置失效才暂停），自动化里超时的 shell 命令直接判失败而不是转到后台继续跑；向已归档会话发送消息、命令、skill 会自动取消归档。",
       [{"key": "能做什么", "value": "按模型切换系统提示、把两个重工具定义移出常驻上下文（每请求省约 700 token）、把网页访问授权粒度收到站点级，并让无人值守的 automation 失败后可继续。"},
        {"key": "解决什么痛点", "value": "agent 每请求的固定开销里，工具 schema 是最大一块沉没成本——用不到也得付费；「总是允许抓取」这类一次点选的宽授权则是长期安全债。两处都在这版被收掉。"},
        {"key": "值不值得", "value": "值得升。700 token/请求在长会话里是实打实的钱；站点级授权对多租户或共享机器的团队更重要。注意 automation 行为变了：以前失败即停，现在会继续排下一次。"}],
       tag="release", source="GitHub Releases", oss=True),
 ]
})

ai_sections.append({
 "label": "🏖️ 沙箱与运行时",
 "items": [
  item("E2B 2.66.0：模板定内存上限、创建时分配、暂停恢复时还能换规格",
       U("e2b-dev/E2B/releases/tag/e2b@2.66.0"),
       "模板构建时用 maxMemoryMB 设上限，创建沙箱时用 memoryMB 选实际内存，暂停沙箱在 Sandbox.connect 恢复时可指定内存与 CPU；onResume 新增对象形式 {action, memoryMB, cpuCount}（Python 为 memory_mb / cpu_count），旧的 'restore' / 'reboot' 字符串继续有效。规格只在该次 connect 真正恢复暂停沙箱时生效，超出沙箱能力的规格被拒绝而不是静默降级。Template.list() / getInfo() / listBuilds() 返回 maxMemoryMB，CLI 的 template list 多一列 Max RAM MiB。",
       [{"key": "能做什么", "value": "同一模板派生不同内存档沙箱；暂停后按新规格恢复，状态不用重建。内存与 CPU 一起成为运行期参数而不是部署期常量。"},
        {"key": "解决什么痛点", "value": "模板按最大用例定规格会让所有沙箱都按上限计费，按小任务定规格又会在跑大任务时被迫重建丢状态。可调内存让「保留状态」与「按需给资源」同时成立。"},
        {"key": "值不值得", "value": "值得跟进。这是把「空闲挂起 + 恢复时调档」做成 SDK 一等公民的少数方案，直接对着自建多租户沙箱平台的成本项；注意规格只在恢复时生效、且会被校验，容量规划按 maxMemoryMB 留余量。"}],
       tag="release", source="GitHub Releases", oss=True),
  item("gVisor 20261123.1：OCI seccomp 默认打开，sentry 追踪宿主文件系统过滤级别并加挂载护栏",
       U("gvisor/gvisor/releases/tag/release-20261123.1"),
       "这次把 --oci-seccomp 改为默认开启（#17846），OCI seccomp 过滤器支持 SECCOMP_RET_KILL_THREAD 与 SECCOMP_RET_KILL_PROCESS（#17849）；systrap 把未显式指定的系统调用参数统一清零，stub 的 seccomp 失败改为显式报错（loud）。runsc 记录 Gofer 挂载是否为目录、追踪 Sentry 的宿主文件系统过滤级别并加挂载护栏，gofer 在能创建宿主 socket 时允许 unlinkat，并给 Gofer bind tree 应用递归属性。另外修了 arm64 futex 在虚假唤醒时的地址重载。",
       [{"key": "能做什么", "value": "默认启用 OCI seccomp 让「用户自带 seccomp profile」直接生效，并支持两种立即杀进程的返回值；sentry 侧把宿主文件系统过滤级别变成可追踪状态并加挂载护栏，缩小 gofer 的可操作面。"},
        {"key": "解决什么痛点", "value": "沙箱默认配置往往是「能跑就行」，seccomp 不默认开等于把一半内核攻击面留着；gofer 与挂载路径又是容器逃逸的经典口子，缺护栏就只能靠人记得配。"},
        {"key": "值不值得", "value": "值得，尤其对把 agent 代码执行放到 gVisor 里的场景：默认安全基线抬高了，升级即获得而不是靠额外参数。注意默认变更可能暴露之前被默默忽略的 seccomp 违规。"}],
       tag="sandbox", source="GitHub Releases", oss=True),
  item("microsandbox v0.8.3：SDK 破坏性改动暴露上下文与保留元数据，修 Windows 共享盘 TLS 私钥",
       U("superradcompany/microsandbox/releases/tag/v0.8.3"),
       "v0.8.3 主要是一条破坏性 SDK 变更（#2177）：把已配置的 context 与保留的 metadata 暴露出来，调用方可以读到沙箱创建时的上下文信息，升级需要改代码。另修 Windows 上共享数据盘里 TLS 私钥未保持私有（#2176），并在 README 里宣布 microsandbox cloud。其余为锁文件与版本号维护。",
       [{"key": "能做什么", "value": "把沙箱的 context 与 metadata 变成可读的 SDK 一等对象，便于多租户场景做归属追踪与清理；Windows 侧补上共享盘上的密钥保护。"},
        {"key": "解决什么痛点", "value": "轻量沙箱在本地批量起停时最难管的是「这个沙箱属于谁、用的什么配置」——元数据不可读就只能自己另建账本；Windows 共享盘上的私钥泄漏则是本地开发环境的真实风险。"},
        {"key": "值不值得", "value": "轻量级、单机优先的沙箱需求值得看，但这一版的价值主要在元数据可见性，能力增量有限；升级前先评估 context/metadata 的 API 破坏性改动。"}],
       tag="sandbox", source="GitHub Releases", oss=True),
 ]
})

ai_sections.append({
 "label": "🛠️ AI 工程落地",
 "items": [
  item("用 Claude 把 Rockbox 塞进 512 KiB SRAM 的 9 美元 MP3，再把成功路径沉淀成工具包，第二个机型 4 小时跑通",
       U("jayd.ml/2026/11/14/rockbox-on-yp3"),
       "作者花 9.71 美元买了个无名 AliExpress MP3（自报 yp3_2.0.43，512 KiB SRAM），而 Rockbox 现有最小目标是 2 MiB——内存差四倍。他把逆向与移植交给 Claude：约一周后能在「每个缓冲区都砍到骨头」的构建上启动并出声，再花一个月调优，目前硬件功能基本齐全。真正可复用的是第二步——让 Claude 依据第一次成功的路径沉淀出一套移植工具包 auto-rockbox，随后第二个机型 TS47 只花 4 小时就跑起 Rockbox。ROM 下载模式与 flash 读写工具的突破口来自 ilyakurdyukov 的既有工作，作者自评「几乎没怎么参与」。",
       [{"key": "能做什么", "value": "用 LLM 完成嵌入式逆向这类传统上极耗人力的工作：读固件、定位内存布局、把每个缓冲区压到极限、让构建在 512 KiB 里启动；更重要的是把一次成功沉淀成可复用工具包，第二次同类移植从一周降到 4 小时。"},
        {"key": "解决什么痛点", "value": "嵌入式移植的瓶颈不是写代码，而是「没文档、没符号、内存差四倍」的探索成本，且每次换机型都要重来一遍。这里的关键动作是「先做成一例、再让模型把它固化成工具」，把一次性运气变成可重复流程——和 skill 的思路一致。"},
        {"key": "值不值得", "value": "值得读完它的方法段落：这是「agent 做长尾工程 + 沉淀 skill」最干净的案例，成本是 9.71 美元硬件加一份订阅。可迁移的判断是：凡是有明确成功信号（能启动、能出声、能过测试）的探索性工程，都适合这套打法。"}],
       tag="case study", source="jayd.ml"),
 ]
})

ai_sections.append({
 "label": "🧠 模型与研究",
 "items": [
  item("Mixture-of-Loops Transformer：用 KV 当跨循环记忆，700M 模型 CE token 效率 1.7×、3B MoE 十任务涨 2.1 点",
       U("huggingface.co/papers/2611.34923"),
       "Looped Transformer 靠复用共享层提升表达力但牺牲效率，MoLT 重新定义「循环之间传什么」：MoLA 把 keys/values 当作跨深度、跨循环选择性复用的记忆。MoLT-R 保留 residual stream、跨循环读本地 KV 换表达力；MoLT-KV 从 embedding 重启、只读当前循环的本地 KV 加前序循环的 memory KV，消除同位置跨循环依赖，配合 loop forcing 可并行训练，并解锁超出训练循环范围的单遍 MoL 解码。U 形 U-MoLT 把记忆构建与预测读出分离、跳过无用的 decoder 遍历。400B token 预训练下，U-MoLT 在 700M/1.5B dense 与 3B MoE 上全面优于 OLMo3，700M 达 1.7× 验证 CE token 效率，3B MoE 十域困惑度改善 0.75、十任务准确率 +2.1 点。",
       [{"key": "能做什么", "value": "在不增加参数量的前提下，通过控制「循环间传什么」把表达力与效率同时往前推；单遍解码让推理不必真的跑满训练时的循环次数。"},
        {"key": "解决什么痛点", "value": "循环复用层的思路一直卡在效率账上：多跑一遍循环就多一遍算力。把 KV 选择性地跨循环复用、并让无用的遍历可跳过，等于把「深度」做成可调度资源。"},
        {"key": "值不值得", "value": "值得关注但不紧迫：这是架构层研究，短期不改变你手上的部署选型；如果你的推理平台按 token 成本核算，1.7× CE token 效率这类指标值得记一笔作趋势判断。"}],
       source="HuggingFace Papers"),
  item("NVIDIA 让模型自己管上下文：32K 预算下 GPT 6.1 分数从 21% 到 56%，Kimi 输入 token 少 41%",
       U("huggingface.co/papers/2611.34147"),
       "现有 agent harness 在窗口满时替模型做 compaction 摘要；这篇研究反过来——给模型一个 context API，由它自己决定何时、压缩什么。作者在 NVIDIA 开源 harness nooa 里给了模型这个控制权，在文档研究与机器学习工程两类任务、8K 到 512K 的预算区间对比两种策略：会用 API 的模型准确率更高且常常输入 token 更少，紧预算下尤其明显——GPT 6.1 在 32K 预算的 OfficeQA Pro v2 上从 21% 升到 56%（近三倍），Kimi 最多省 41% 输入 token。但模型之间差异极大：用 API 的频率、压缩力度、开始压缩的时机都不同，改提示词就会改时机。作者还证明推理引擎能降低这种编辑的成本：复用未改动后缀的 KV cache，每请求 prefill 计算最多减 15%，准确率无可测变化。",
       [{"key": "能做什么", "value": "把「什么时候压缩上下文」从 harness 的固定策略交给模型自己判断，并把压缩变成推理引擎可增量重算的 KV 编辑；结果是紧预算下准确率与 token 效率同时改善。"},
        {"key": "解决什么痛点", "value": "harness 统一 compaction 的坏处是「一刀切」：简单任务被过度摘要，复杂任务摘要得太晚。模型自管上下文能按任务调节，但代价是行为差异大、提示词一变时机就变。"},
        {"key": "值不值得", "value": "值得读，因为你正在做多用户多会话的 agent 平台：结论直接指向两个可落地点——暴露 context API 给模型、以及让推理引擎支持 KV cache 编辑以降低 prefill。也要注意「模型间差异大」意味着不能指望换模型后行为不变。"}],
       source="HuggingFace Papers"),
  item("ELITE：不在进化环里跑下游评测，SWE-bench Pro 从 60.0% 提到 85.6%",
       U("huggingface.co/papers/2611.21056"),
       "自我改进的 coding agent 通常用「evaluate-and-select」：把候选实现放到下游任务上跑，用结果决定哪条血统继续。这篇问的是能不能在进化环里完全不跑下游评测。ELITE（Explore-then-Integrate）每一代让 agent 提出多个聚焦改进、从同一父本独立实现，然后检查这些程序找出互补/冗余/冲突的机制，再把兼容子集重新实现成一个连贯后代；环内只用结构化与运行有效性的确定性检查，不用任务成绩或解题轨迹。SWE-bench Pro 上把初始 agent 从 60.0% 提到 85.6%，对比 evaluate-and-select 的 86.7%。",
       [{"key": "能做什么", "value": "把「多方案探索 + 机制整合」作为进化算子，用确定性检查替代昂贵且有基准污染风险的下游评测；一次整合出一个连贯的后代而不是留下多条互斥血统。"},
        {"key": "解决什么痛点", "value": "evaluate-and-select 的两个死结：探索越广评测成本越高；反复对固定评测分布优化会滑向基准特化。ELITE 用「不看下游成绩」绕开两者，代价是略低的天花板（85.6% vs 86.7%）。"},
        {"key": "值不值得", "value": "值得看它的取舍逻辑，尤其如果你在搭自改进 pipeline：用确定性有效性检查替代下游评测，能把进化成本压到常数级。1.1 个点的让步换来的是没有评测成本和基准污染风险。"}],
       source="HuggingFace Papers"),
 ]
})

ai_sections.append({
 "label": "📜 平台政策与风控",
 "items": [
  item("Google Workspace 新条款落地：2027-02-01 起 agent 访问 Gmail/Drive/Calendar 必须走官方 MCP",
       U("techstackups.com/articles/google-workspace-ai-agents-mcp"),
       "11 月 24 日八套 Workspace MCP server 转 GA，同时 API 条款新增 Workspace AI Tools Addendum：自 2027 年 2 月 1 日起，「本身是、或由 AI agent / AI harness / AI 模型驱动」的工具访问 Gmail、Drive、Calendar 等必须经 Google 的 MCP server；伪装成非 agent 被明文禁止，违反可被限制/移除访问或停号。同日起来直接调 REST 的 agent 按 Standard 档配额限速，与项目付费档无关。功能面仍有缺口：Gmail MCP 只能搜索、读串、建草稿、打标签，发信/回复/转发/改草稿标注需要 partner access、未 GA。纯确定性脚本（夜间备份、CRM 同步）不受影响。",
       [{"key": "能做什么", "value": "用一份 addendum 把 agent 的 Workspace 数据通路统一收口，并用配额分档让绕过 MCP 的直连降速；同时用「禁止伪装」条款堵住把 agent 包装成脚本的路子。"},
        {"key": "解决什么痛点", "value": "平台方要的是可治理：谁在代表用户读邮件、读多少、走哪条通道。对开发者是能力边界问题——官方通道拿不到发信权限，邮件自动化就断在最后一步。"},
        {"key": "值不值得", "value": "值得当截止日记下来。2027-02-01 前要判定自建 agent 是否落入定义、是否需要 partner access；如果你的产品靠 Gmail API 读写，先把「只能到草稿」当成默认假设做设计。"}],
       tag="条款变更", source="Tech Stackups"),
 ]
})

ai_sections.append({
 "label": "💡 观点与好文",
 "items": [
  item("数据侧观察：Astra 6.2 与 Sol 6.2 更像「为省钱调过」的模型——输出与推理 token 显著低于同代",
       U("micjm.com/blog/openai-is-in-cost-control-mode"),
       "作者用自家对战数据对比 GPT-6 与 GPT-6.2：把每个模型的「相对花费比」对 Elo 作图后，Astra 6.2 与 Sol 6.2 落在明显偏「便宜」的一侧；再看推理量（相对对手的 reasoning token），Astra 6 与 Sol 6.1 属于正常范围，而 6.2 两版成为「推理不足」的离群点。显著性上，输出 token 下降 Sol p=0.0055、Astra p=0.022；推理 token 下降 Sol p=0.00013、Astra p=0.0064。作者结论是这两版相对前代做了成本调优，程度已到「underthinking」。",
       [{"key": "能做什么", "value": "给出一种可复用的评估角度：不看模型自报能力，而看「单位 Elo 的花费」与「相对对手的推理 token 量」，据此判断一代模型是否被成本约束改了行为。"},
        {"key": "解决什么痛点", "value": "同代小版本升级常不写清改了什么，用户在「好像变快了」和「好像变笨了」之间无从判断；这种双轴分析能把「省钱调优」和「能力提升」区分开。"},
        {"key": "值不值得", "value": "值得当方法论看。对你的实际意义是：换小版本前先跑自己的基准并看 token 消耗，不要假设小版本只升不降；p 值给到了，结论不算拍脑袋。"}],
       source="micjm.com"),
 ]
})

infra_sections = [{
 "label": "🤖☸️ K8s × AI",
 "items": [
  item("Dynamo v1.7.0：Global Router 跨池路由 + Planner 预算交易，Sidecar 支持多机引擎故障迁移",
       U("ai-dynamo/dynamo/releases/tag/v1.7.0"),
       "第 20 个 feature release，763 个 PR、150 位贡献者（54 位来自外部）。核心是 Global Router：新的发现服务通过 HTTP 注册池与 router，一个 Dynamo Frontend 就能按负载跨多个池路由，--router-policy affinity 让会话留在同一池，/metrics 报每池请求数、错误与 TTFB；K8s 上 DynamoPoolRelay 为每个图起两个 active Relay pod。Planner 增加批调度策略、跨池 GPU 预算交易的池优先级排序、/engine/planner/config 热更新（无需重启），以及实验性 live retune（回放 trace 搜可热改的 Router/Planner 字段）。Router 加截止时间感知队列（最早到期优先、过期即拒）与 transfer-island KV fetch 提示。Operator 可先在模拟中搜索部署配置再部署，并预取部署固定 checkpoint；Sidecar 支持多机 SGLang/TensorRT-LLM/vLLM，引擎挂掉时迁移在途请求并自动重启重注册。引擎版本升到 SGLang v0.5.23、TensorRT-LLM v1.4.0rc2、vLLM v0.33.0。",
       [{"key": "能做什么", "value": "把多池推理集群当成一个逻辑资源来调度：跨池按负载路由并保持会话亲和、按池优先级交易 GPU 预算、按截止时间排队、在部署前用模拟搜配置。Sidecar 让未改动的引擎也能获得 KV 感知路由、PD 分离与故障迁移。"},
        {"key": "解决什么痛点", "value": "多团队共用 GPU 池时，真实问题是「谁该让出预算」和「某个池崩了流量去哪」——过去靠人工改副本数与手工切流。Global Router 与 Planner 的预算交易把这两件事变成配置项；Sidecar 则让「换引擎不用改推理栈」成为可能。"},
        {"key": "值不值得", "value": "值得，尤其你在做 K8s 上的推理/训练混部：Dynamo 已经是 K8s × AI 轴事实标准之一，这版的跨池路由与 budget trade 正对着「多租户共用 GPU」的现实问题。门槛是组件面变宽（发现服务、Relay、Operator、Planner），要先把运维边界想清楚。"}],
       tag="release", source="GitHub Releases", oss=True),
 ]
}, {
 "label": "☸️ K8s 核心技术",
 "items": [
  item("Kubernetes v1.37.3：修调度器同名 Pod 快速重建崩溃、节点同名重建 CSINode 注册失败",
       U("kubernetes/kubernetes/releases/tag/v1.37.3"),
       "补丁版改用 Go 1.26.11 构建，kube-cross/go-runner 与 distroless-iptables v0.9.10 同步更新。修复项里几条值得注意：调度器在 Pod 同名同命名空间被快速删除重建时会崩溃（#144204）；kubelet 在节点同名快速重建时注册不上 CSINode，导致 CSI 卷挂不到新节点（#143771）；KCM 与 kubelet 因 inline vsphere 卷崩溃（#144312）；开启 NativeHistograms 后，未显式声明 Buckets 的直方图（如 kubelet 的 prober_probe_duration_seconds）只剩 le=\"+Inf\"（#144156）；kube-proxy 在 informer 回放缓存 Node 时丢掉初始 zone，导致拓扑感知路由失效；kubeadm upgrade plan 取不到最新 apiserver 版本时返回错误而非 panic，etcd 升级失败后的数据目录回滚改到正确位置并最多重试 30 秒。",
       [{"key": "能做什么", "value": "一次补丁覆盖调度器、CSI、监控指标三个真实崩溃/错数路径，以及 kubeadm 的升级回滚正确性——多数是「偶发但难查」的类型。"},
        {"key": "解决什么痛点", "value": "同名 Pod/Node 快速重建在滚动发布与节点自愈场景里很常见，崩溃与卷挂不上都被当成环境玄学；NativeHistograms 那条更隐蔽——指标只是少了几档 bucket，不报错。"},
        {"key": "值不值得", "value": "值得升，尤其开了 NativeHistograms 或跑 CSI 存储的集群。升级前先看 kubeadm 那条：etcd 回滚路径变了，脚本里若依赖旧的备份目录结构需要调整。"}],
       tag="patch", source="GitHub Releases", oss=True),
  item("Kueue v0.20.8：全组件日志按策略重排，级别与键名变更会打断看板与告警",
       U("kubernetes-sigs/kueue/releases/tag/v0.20.8"),
       "这版主体不是功能而是可观测性：把 ConcurrentAdmission、LeaderWorkerSet、ProvisioningRequest、MultiKueue、kueue-importer / populator / priority-booster / kueueviz、jobframework 以及 JobSet/MPIJob/RayJob/SparkApplication/TrainJob 各 webhook 的日志统一到 logging policy。具体变化：per-object 日志从 level 2 挪到 level 3，eviction 改成「保存后再记」，成功写操作改为写后记录，键名批量重命名（flavor→resourceFlavor、Variant→admittedVariant、cluster→workerCluster、localQueueName→localQueue、oldLimits/newLimits→previousLimits/limits 等），job webhook 校验日志从 level 0 挪到 5，watch 丢失与 GC 生命周期日志降到 level 1。",
       [{"key": "能做什么", "value": "让所有控制器的日志级别与键名一致，便于跨组件统一查询与降噪；per-object 明细仍可用，但需要显式把级别调到 3 以上。"},
        {"key": "解决什么痛点", "value": "Kueue 的日志此前各控制器自成一派，键名同一个概念多种写法，做统一看板要先做字段映射；级别也乱，per-object 明细在默认级别下刷屏。"},
        {"key": "值不值得", "value": "升级前必看。功能没变，但依赖日志字段的看板/告警会静默失效——键名改了不报错，只是查不到数据。把日志级别设到 3 以上可保留 per-object 明细。"}],
       tag="patch", source="GitHub Releases", oss=True),
 ]
}]

flash = [
 {"title": "Google DeepMind：用 Antigravity 里的 Mass Spec Skill 把质谱图读成分子结构",
  "url": U("deepmind.google/blog/interpreting-mass-spectra"),
 },
 {"title": "Snowflake CoCo 再进化：数据开发进入 agent 自主执行",
  "url": U("infoq.cn/article/vfmBDlfQRRfHq4Jyi5b6"),
 },
 {"title": "Uber 的安全 AI 框架：对智能体做全生命周期治理",
  "url": U("infoq.cn/article/xA3g2i0VtTZIOVePMedY"),
 },
 {"title": "CLI agent 让家用服务器自托管重新变得好玩（HN 216 分）",
  "url": U("janlukas.blog/posts/ai-self-hosting"),
 },
 {"title": "Single-Database Rewards Are Hackable：用反事实执行让数据库 agent 的奖励不可刷",
  "url": U("huggingface.co/papers/2611.34363"),
 },
]

# sanity: flash URLs must exist
for f in flash:
    assert f["url"] in BYURL, f["url"]

brief = {
 "brand": "AI & 基础设施早报",
 "date_label": DATE_LABEL,
 "issue": ISSUE,
 "kicker": "AI & INFRASTRUCTURE DAILY · NO.067",
 "hint": "👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
 "lead": lead,
 "highlights": highlights,
 "sections": [{"label": "🤖 AI 板块", "categories": ai_sections},
              {"label": "☸️ 基础设施板块", "categories": infra_sections}],
 "flash": flash,
 "footer": "由 Hermes 自动汇编 · 每日 08:30 更新",
}

EMOJI = {"🧩 Agent & Skill": "🧩", "🧭 Agent 工具链": "🧭", "🏖️ 沙箱与运行时": "🏖️",
         "🛠️ AI 工程落地": "🛠️", "🧠 模型与研究": "🧠", "📜 平台政策与风控": "📜",
         "💡 观点与好文": "💡", "🤖☸️ K8s × AI": "🤖☸️", "☸️ K8s 核心技术": "☸️"}
for sec in brief["sections"]:
    for c in sec["categories"]:
        c["title"] = c["label"]
        c["emoji"] = EMOJI[c["label"]]

# assertions: every item has non-empty title/summary/url/detail, url in processed.json
n = 0
for sec in brief["sections"]:
    for c in sec["categories"]:
        assert c["title"] and c["emoji"], c
        for it in c["items"]:
            n += 1
            assert it.get("title"), it
            assert it.get("summary"), it
            assert len(it.get("detail", [])) == 3, it["title"]
            assert it["url"] in BYURL, it["url"]
for h in brief["highlights"]:
    n += 1
    assert h.get("title") and h.get("summary") and len(h.get("detail", [])) == 3
    assert h["url"] in BYURL, h["url"]
print("items:", n, "flash:", len(brief["flash"]))

json.dump(brief, open(os.path.join(BASE, "briefing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written briefing.json")
