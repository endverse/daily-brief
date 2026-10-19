#!/usr/bin/env python3
"""Build briefing.json for issue 029 (2026-10-19). URLs are looked up from processed.json."""
import json

P = json.load(open("processed.json", encoding="utf-8"))
BY = {}
for it in P:
    BY.setdefault(it["url"].split("?")[0], []).append(it["url"])

def U(frag):
    """Return the exact URL as stored in processed.json, matched on the part before '?'."""
    hits = [u for k, us in BY.items() for u in us if frag in k]
    assert len(hits) == 1, f"{frag} -> {hits}"
    return hits[0]

def item(title, url, summary, tag, source, detail, oss=False):
    d = {"title": title, "url": url, "summary": summary, "tag": tag, "source": source, "detail": detail}
    if oss:
        d["oss"] = True
    return d

def det(a, b, c):
    return [{"key": "能做什么", "value": a}, {"key": "解决什么痛点", "value": b}, {"key": "值不值得", "value": c}]

META_URL = U("infoq.cn/article/EuYOPRUBAeBgBGBu5ktk")
CF_URL = U("infoq.cn/article/YmllSwKbZXY0bcVjjw70")
ANTH_URL = U("anthropic.com/news/an-update-on-independent-evaluators")

meta_sum = ("Meta 于当地时间 10 月 15 日开放 Muse Spark Open 权重：稀疏 MoE 总参数 8160 亿、每 token 激活约 420 亿，"
            "支持 1,048,576 token 上下文，输入可含文本/图片/音频/视频、输出为文本，官方定位是端到端 agent 任务、代码编写调试与长程工具调用。"
            "本地运行靠 MLX 在两台 M5 Ultra Mac Studio 上完成，官方给出的 GPU 方案是 BF16 用 8 张 B300（权重约 1.65 TB）、NVFP4 用 4 张 B300（约 537 GB）。"
            "基准上 JobBench 61.8、MCP-Atlas 89.2、OSWorld Verified 80.4、Terminal-Bench 2.1 76.4、DeepSWE 1.1 60，后两项低于 GLM 5.3 max 与 Kimi K3 max；"
            "许可证为 Muse Model License，MaaS 提供方若连续 12 个月合计收入超 2000 万美元需先通知 Meta 并另签协议。")

meta_note = ("🔎 新闻要点：8160 亿总参数 / 约 420 亿激活；1,048,576 token 上下文；输入文本+图像+音频+视频、输出文本；"
             "本地为 2× M5 Ultra Mac Studio（MLX），BF16 权重约 1.65 TB、NVFP4 约 537 GB，GPU 示例 8×/4× B300；"
             "JobBench 61.8、MCP-Atlas 89.2、OSWorld Verified 80.4、Terminal-Bench 2.1 76.4、DeepSWE 1.1 60（后两项输给 GLM 5.3 max、Kimi K3 max）；"
             "苹果研究展示 4 台 Mac Studio 分布式推理 >36 token/s；托管伙伴含 Baseten、Fireworks、Groq、Modal、Nebius、Together、OpenRouter。")

cf_sum = ("Cloudflare 披露 Containers 平台（也为 Sandboxes 提供底座）的跨租户数据泄露：每个容器跑在 Firecracker microVM 里，根盘用 dm-thin 精简配置，"
          "受影响资源池的块大小为 64 KiB 且开了 skip_block_zeroing，向未映射区域写 4 KiB 会分配一个 64 KiB 物理块、剩下最多 60 KiB 保留前一租户内容。"
          "研究者 Oren Yomtov 用 ext4 目录块校验和区分归属，在 6 个生产部署里 5614/5614 个可测目录块都来自其他用户、识别出 2700 个外部 inode，"
          "24 个部署点中 18 个、22 个节点中 20 个发现残留。Cloudflare 当天 21:27 合并运行时修复、9 月 7 日完成部署，并因已映射块不会自动清零而停掉全部运行中容器磁盘、清空主机与镜像缓存，9 月 19 日收尾。")

cf_note = ("🔎 新闻要点：根因是存储分配器的 skip_block_zeroing（不是 Firecracker 边界）；64 KiB 块 / 4 KiB 写 → 60 KiB 残留；"
           "5614 个目录块全部命中他人数据、2700 个外部 inode；24 个部署点中 18 个、22 个节点中 20 个有残留；"
           "9 月 4 日 15:26 收到报告、21:27 合并修复、9 月 7 日部署完、9 月 19 日完成存量清理；攻击者无法选择受害者或主机，也未发现恶意利用。")

highlights = [
    {"title": "Meta 开放 Muse Spark Open：8160 亿参数 MoE、106 万上下文，两台 M5 Ultra Mac Studio 本地跑",
     "url": META_URL, "summary": meta_sum, "note": meta_note, "tag": "开放权重", "source": "InfoQ 中国",
     "detail": det(
        "开放权重的 8160 亿参数稀疏 MoE（每 token 约 420 亿激活），1,048,576 token 上下文，可读文本/图片/音频/视频；主打端到端 agent 任务、代码编写与调试、长程工具调用。官方演示里用 Muse Code 在本地完成开源 Mastodon 客户端 Ice Cubes 的 iOS 修复/加功能/构建，以及操作 DaVinci Resolve 逐帧挑素材做竖屏裁剪。",
        "大开放权重模型过去基本只能进数据中心：想在私有环境跑 agentic coding，又要控制数据不出域，缺少「权重可下载 + 能在 Apple 硅上多机分布式推理」的选项。BF16 权重约 1.65 TB 是真实显存墙，NVFP4 537 GB 才让两台 512 GB 的 Mac Studio 成为可行配置。",
        "若你在算「私有化 agent 编码」的硬件账，这是目前最具体的一组数字：2×M5 Ultra、4×B300（NVFP4）、36 token/s，可先按这个量级估成本。但 Terminal-Bench 2.1 与 DeepSWE 1.1 都输给 GLM 5.3 max、Kimi K3 max，且许可证对年收入 >2000 万美元的 MaaS 提供方要单独签约——商用前先过条款。")},
    {"title": "Cloudflare Containers 跨租户泄露复盘：Firecracker 没破，dm-thin 的 skip_block_zeroing 漏了 60 KiB",
     "url": CF_URL, "summary": cf_sum, "note": cf_note, "tag": "多租户隔离", "source": "InfoQ 中国",
     "detail": det(
        "一份完整的块级泄露复盘：Firecracker microVM 的根盘走 dm-thin 精简配置，64 KiB 块 + skip_block_zeroing 意味着 4 KiB 写入只覆盖块的一角，剩余最多 60 KiB 保留上一租户的目录块、数据库页甚至完整 SQLite 文件；研究者用 ext4 目录块校验和把「自己的块」与「别人的块」分开统计。",
        "平台侧习惯把隔离押在 microVM 或网络边界上，但块分配器的性能开关会从下面绕过；对跑不可信代码的 agent 沙箱、多租户容器/函数平台，这类「边界之下」的复用路径通常没有单独的验收测试。",
        "可直接拿去用的检查项：对每个复用卷路径验证「分配时清零/释放时擦除」，并做原始读测试；文中 5614/5614 的命中率与 4 小时修复时间线，适合作为隔离评审的基线材料。对做多用户 agent 沙箱的团队，这是当前最值得读的一份事故报告。")},
]

sections = [
    {"label": "🤖 AI 板块", "categories": [
        {"emoji": "🧩", "title": "Agent & Skill", "en": "Agent & Skill", "items": [
            item("Data World：先造「世界」再生成文件，2,135 条合成任务把 35B-A3B 在 DABstep-Hard 上拉高 20.9 分",
                 U("huggingface.co/papers/2610.21656"),
                 "数据 agent 用代码处理异构文件并得出结论，但训练环境靠人工收集、受隐私与 IP 限制，开放式发现又没有已知的生成真值可验证。Data World 的做法是先写清「文件背后的世界机制」，再由多智能体引擎同时合成环境、任务与评分 rubric，独立审计检查目标能否从观察到的文件恢复，rubric 直接充当评测与 RL 奖励。"
                 "人工偏好筛选出 100 条任务（50 个留出世界、16 个领域）构成 DataWorld-Bench，引擎另产出 1,037 个不相交世界里的 2,135 条训练任务；十个前沿模型在该基准上仍显吃力，尤其在洞察发现上存在稳定的「计算—洞察」差距。"
                 "只用 RL-zero 在合成任务上训练（不做轨迹蒸馏），从 Qwen3.6-35B-A3B 得到 DataWorld-35B-A3B，在 DataWorld-Bench +7.06、DAComp +14.28、DABstep-Hard +20.90、JobBench +12.13。",
                 "Agent 数据合成", "HuggingFace Papers",
                 det("把「环境生成」拆成机制描述 → 文件世界 → 任务 → rubric 四层，用独立审计保证任务目标确实可从文件推出；rubric 既是评测标准也是 RL 奖励，因此同一套合成数据能直接用于 zero-RL 训练。",
                     "数据 agent 的训练环境最难的是「造得像、且可判分」：人工造环境贵，真实文件有隐私/IP 问题，开放式结论没有标准答案。多智能体合成 + 可恢复性审计把这三件事一起解了。",
                     "做 agent 数据飞轮或评测集的人值得细读，尤其是 7.06/14.28/20.90/12.13 这组跨基准增益的对照方式；门槛在于要先为每个领域写「世界机制」，领域建模本身是成本，且目前任务集中在数据分析类。"), True),
            item("SERO：把 oracle 的未来接在策略真实到达的状态后面，长程 agent RL 不再受 rollout 视野限制",
                 U("huggingface.co/papers/2610.19397"),
                 "长程 agentic RL 的天花板是「当前策略走到过哪些状态」：rollout 没碰到的状态，再好的信用分配也给不出监督。SERO 先恢复一个当前策略真实到达过的状态，再让只在训练期存在的 oracle 在真实环境里继续交互，把后续观察与 oracle 动作本身变成训练轨迹。"
                 "它用 policy-reachability weighting 按冻结行为策略与前序 oracle 动作的兼容度给每个 oracle 步加权，使更深的监督随策略靠近 oracle 分支而逐步生效；oracle loss 与基础 RL 估计器分开优化，推理时不使用 oracle。"
                 "在 ALFWorld 与 WebShop 上用 Qwen2.5-1.5B/7B 验证：学习完整的可执行延续明显优于只监督根节点的 oracle 动作，加权进一步改善分布外表现。",
                 "Agent RL", "HuggingFace Papers",
                 det("把 on-policy RL 与「可执行 oracle 延续」拼起来：从策略实际到达的状态出发，让训练期 oracle 在真实环境里继续走，产生可学习的后续观察与动作；再用可达性权重控制深度监督何时生效。",
                     "长程任务的稀疏奖励与状态覆盖不足：策略走不到的分支永远学不到，on-policy distillation 又只教当前状态。SERO 补的是「未来轨迹」这一段监督。",
                     "如果自建 agent RL 训练（尤其是可重置环境），这篇给出了一个不需要推理期 oracle 的可行配方；限制是必须有能在真实环境里执行 continuation 的 oracle，且目前只在 ALFWorld/WebShop 两个经典交互环境上验证。"), True),
            item("CoWorld Reasoner：把视频世界模型做成 agent 的「想象工具」，工具与 skill 随执行反馈共同演化",
                 U("huggingface.co/papers/2610.21910"),
                 "VLM 越来越需要回答「画面之外」的运动、动作与视角变化，视频世界模型（VWM）能生成任务相关的视觉内容作为补充证据，但现有做法把它固定在「新视角合成」这类预设流水线里。CoWorld Reasoner 把 VWM 当成统一的视觉推理引擎：harness 通过工具暴露多种视觉操作，再用 skill 指导 VLM 判断要不要想象、选哪个操作、怎么构造生成请求、如何解释生成的证据。"
                 "它还提出 VLM-VWM Harness Co-Evolution：模型权重冻结，只根据执行反馈联合修改工具、skill 与执行代码。在空间智能、时序与因果推理、感知推理等七个基准上，最强变体全部超过同 backbone 的直接推理，MMSI 相对提升 11.8%、ERQA 提升 13.0%，并在五个基准上压过五个同样会演化的基线。",
                 "Agent 工具编排", "HuggingFace Papers",
                 det("把视觉世界模型包装成一组可调用工具，用 skill 文件约束「何时想象、怎么请求、怎么读结果」；外层 harness 的 tools/skills/code 依据执行反馈迭代，模型本身不动。",
                     "多模态 agent 在需要反事实或视角推理时，单靠输入图像没有证据；固定 pipeline 又无法适配不同任务。它把「要不要生成视觉证据」变成 agent 的一个决策。",
                     "对做 agent harness / skill 体系的人有直接参考价值：演化的是外围工具与 skill 而非权重，成本低；但依赖一个可用的 VWM，且提升幅度（11.8%/13.0%）属于中等，适合作为 harness 设计的样例而非马上上生产。"), True),
        ]},
        {"emoji": "🧠", "title": "模型与研究", "en": "Models & Research", "items": [
            item("Meta 开放 Muse Spark Open：8160 亿参数 MoE、106 万上下文，两台 M5 Ultra Mac Studio 本地跑",
                 META_URL, meta_sum, "开放权重", "InfoQ 中国",
                 det("开放权重的 8160 亿参数稀疏 MoE（约 420 亿激活），1M token 上下文，接收文本/图片/音频/视频；能承担多步工具调用与代码修改，官方在本地用 Muse Code 完成 Ice Cubes iOS 客户端的修复与构建。",
                     "想在私有硬件上跑 agentic coding 的团队，长期只有「小模型不够用、大模型出不了机房」两难；这条给出了一条可下载权重 + Apple 硅多机推理的路径。",
                     "硬件账很清楚：NVFP4 4×B300 或 2×512GB Mac Studio 起步，BF16 要 8×B300；编码基准并非最强（输给 GLM 5.3 max、Kimi K3 max），是否值得投入取决于你对数据出域的敏感度与许可证条款。")),
            item("Learning to Read Out：能力「出现」的时间，可能只是 readout 学会表达的时间",
                 U("huggingface.co/papers/2610.21025"),
                 "发展性研究通常用「模型何时开始输出正确 token」来给能力出现定时，但这条路径要经过仍在训练中的 unembedding（readout）。作者提出 parameter-trajectory crosscoding：对每个 checkpoint 的每个 token readout 行拟合同一个稀疏字典，只依赖权重、不需要激活。"
                 "在 Pythia 预训练进度 0.4–1.1% 的窄窗口里，readout 发生重组、WordNet 词类变得可解码，而此时 hidden state 上的线性探针已经能解码模型输出尚未体现的任务信息。只改 readout 学习率从头预训练小模型，读取更早发生、差距更早闭合，最终 loss 几乎不变。",
                 "可解释性", "HuggingFace Papers",
                 det("用 checkpoint 权重轨迹而不是激活做 crosscoding，直接追踪 unembedding 何时把已有表征「读出来」；再用只改 readout 学习率的对照实验证明时间差可被人为移动。",
                     "「能力涌现」的时间点常被当作训练阶段的属性，但如果测的是 readout，结论会把「已编码」误判成「未学会」，影响 curriculum、early stopping 与 scaling 分析的判断。",
                     "做预训练分析或模型发育研究的人值得看，方法只需 checkpoint（不必存激活）成本低；局限是目前主要在 Pythia 与小型模型上，结论能否外推到前沿规模未知。"), True),
            item("给 MoE 做个性化：crosscoder 定位到具体专家，干预这些专家就能把非个性化模型推向个性化行为",
                 U("huggingface.co/papers/2610.22127"),
                 "现有 LLM 个性化多在 dense 模型上做，但多语义神经元让「个性化到底存在哪」难以定位。作者改在 MoE 上做：token 稀疏路由到少数专家，降低多语义性；在三个开放权重 MoE 上用大规模个性化数据微调，再对「个性化/非个性化」配对激活训练 crosscoder，得到可解释的个性化 latent。"
                 "结果是 MoE 个性化模型与 dense 模型表现相当，但只激活一小部分参数、多语义性更低；同族模型内，个性化 latent 与原始模型共享更少。因果干预显示这些 latent 足以恢复个性化行为，增强对应专家也能把非个性化模型推向该行为，不同个性化特征走不同路由路径。",
                 "MoE 可解释性", "HuggingFace Papers",
                 det("用 crosscoder 从配对激活里学个性化 latent，并把它映射回具体专家；通过增/减专家激活做因果验证，证明这些路由路径是行为差异的实际载体。",
                     "个性化通常被当成一个整体向量或 prompt，出问题时无法定位；在 MoE 上把功能收敛到专家，才有机会做「按特征开关」而不是整体重训。",
                     "对做多租户/多用户个性化（同一底座服务不同用户）的团队有参考价值：MoE 的稀疏性让「按用户开专家」比 dense 更可操作；但目前是三个开放权重模型 + 离线数据，线上路由成本与串扰未验证。"), True),
            item("LeanPRM：用 Lean 给自然语言证明逐步打标签，4B 验证器步级准确率 48.2 → 74.7",
                 U("huggingface.co/papers/2610.17697"),
                 "AI 写的数学证明越来越长，逐步校验成为瓶颈；训练步级验证器又缺少标签——人工标注贵、最终答案推不出步骤对错、把每个证明形式化又要专家投入。LeanPRM 让模型同时写自然语言证明与配套形式证明（不给 Lean 反馈），由 Lean 给每一步打标，再用第二个模型剔除「只是形式语法失败」的负例。"
                 "数据集含 10,634 个证明、152K 个带标签步骤，零人工标注。用其训练的 Qwen3-4B 验证器在 200 个留出证明（LeanPRM-Bench）上把精确步级准确率从 48.2 提到 74.7，而同样底座用 PRM800K 训练只有 60.3；在 IMO 级题目的 best-of-N 选择与四个外部验证基准中的三个上也更好。",
                 "过程监督", "HuggingFace Papers",
                 det("把 Lean 当成自动标注器：自然语言证明 + 形式证明成对生成，Lean 逐步验证，语法噪声由第二模型过滤；产出的步级标签直接训练 PRM，并可随形式化题库扩张。",
                     "过程奖励模型最贵的是步级标签。答案级监督无法定位错在哪一步，人工标注又跟不上模型产出证明的速度。",
                     "做数学/代码等可形式化领域的验证器时，这条流水线值得借鉴，成本结构是「生成形式证明 + Lean 计算」而非人力；限制是必须能写出配套形式证明，纯自然语言、不可形式化的领域用不上。"), True),
            item("SAE 要多少激活数据：重建很早饱和，但特征一一复现要的数据多得多",
                 U("huggingface.co/papers/2610.20680"),
                 "SAE 通常在数亿到数十亿激活 token 上训练，但这一规模是否必要缺少检验。作者在三个语言模型、四种 SAE 架构上，把预算从 5M 拉到 500M token 参考值，分别看「标准评测上的功能表现」与「学到的特征能否一一复现」。"
                 "结论是功能指标强烈依赖度量：重建往往在远小于全量的预算就接近参考，而特征复现率持续随数据增长——Gemma-2-2B BatchTopK 的严格匹配特征比例从 5M 时的 2% 升到 50M 时的 29%。数据选择同样重要：随机采样更保真原始激活分布、利于重建，多样性采样常提升 AutoInterp；理论分析把「子采样的统计一致性」与「一一复现所需的可辨识性/优化条件」分开。",
                 "可解释性", "HuggingFace Papers",
                 det("用 5M–500M 的预算梯度测两种收敛：重建/功能指标 vs 特征严格匹配率；再比较随机采样与多样性采样对重建、AutoInterp 的不同影响，并给出可辨识性角度的理论区分。",
                     "很多 SAE 结论建立在「特征」上，但训练预算不足时特征根本不可复现，功能分数却已接近饱和——这会让特征级解释无法被别人复现。",
                     "做 SAE 特征研究的人应当把「严格匹配率」当作必报指标，而不是只看重建 loss；实践含义是按目标选预算：要重建可以省数据，要特征结论就得加数据。"), True),
        ]},
        {"emoji": "🛠️", "title": "AI 工程落地", "en": "AI Engineering", "items": [
            item("llm-echo 0.5：假模型也要算准账，模拟用量开始计入 tool call、system prompt 与 reasoning token",
                 U("simonwillison.net/2026/Oct/18/llm-echo/"),
                 "llm-echo 是 Simon Willison 的 LLM 调试插件，提供一个完全不调用模型的「echo 模型」，原样回显喂进去的 prompt。0.5 版把模拟 token 用量改为计入 tool calls、system prompt 与 reasoning token，用来在没花钱的情况下检查多轮工具调用与思考预算的计费口径。"
                 "它同时暴露了 LLM 0.33 切到 httpx2 的兼容性问题：直接依赖 httpx 的插件会断，配套的 llm-tools-datasette 0.1.1 就是这次修复。",
                 "调试工具", "Simon Willison",
                 det("一个零成本的假模型，回显 prompt 并按新口径统计输入/输出/推理 token，可在本地验证 tool call 循环与 usage 统计是否符合预期。",
                     "调试 agent 循环时，真实模型的调用既慢又花钱，而且 usage 字段常常被忽略；用 echo 模型能把「账怎么算」单独拿出来测。",
                     "自己写 LLM 插件或 agent 计费逻辑的人值得装来当单测夹具；对生产系统价值有限，属于工具链卫生。"), True),
        ]},
        {"emoji": "🛡️", "title": "安全与治理", "en": "Safety & Governance", "items": [
            item("Anthropic 给 METR 六名员工「员工级权限」：风险评估将公开发布，公司无权否决",
                 ANTH_URL,
                 "Anthropic 10 月 15 日更新独立评估安排：已让非营利机构 METR 的一个团队获得「员工级访问」——六名 METR 员工配公司硬件、办公室，可访问与内部风险评估团队大致相同的工具与系统。例外只有客户数据、律师特权信息与模型架构等少数类别，其余信息内部员工被鼓励像对待同事一样共享。"
                 "METR 将公开发布其风险评估结论，Anthropic 不能否决发布，但可要求对特定内容做遮盖；SecureBio 与 Accenture 也在评估方之列，与 Hugging Face 等机构处于早期商谈。Anthropic 给出的评估方四条标准是专业度、独立性（不持股、不财务依赖）、足够访问权限、发表自由，并以银行监管的驻场检查员作类比。",
                 "AI 治理", "Anthropic",
                 det("把第三方评估从「给报告」推进到「驻场」：六人团队拿员工级系统权限、可看训练与防护机制，评估结果对外发布且公司无否决权（仅可要求遮盖）。",
                     "前沿实验室掌握最多风险信息，但出于商业敏感与滥用风险不能全公开；外部评估又常因看不到训练细节而流于表面。驻场访问试图缩小这个信息差。",
                     "对做模型采购或合规评审的团队，这是一份可参照的「评估方权限清单」（专业度/独立性/访问/发表自由）；但仍是厂商自愿安排，无外部强制力，实际报告质量要看 METR 后续发布。")),
        ]},
    ]},
    {"label": "☸️ 基础设施板块", "categories": [
        {"emoji": "🤖☸️", "title": "K8s × AI", "en": "K8s × AI", "items": [
            item("KAI-Scheduler v0.18.6：任务打分不再为每个 worker 建 score map，绑定请求只删失败的",
                 U("kai-scheduler/KAI-Scheduler/releases/tag/v0.18.6"),
                 "NVIDIA 系 GPU 批调度器 KAI-Scheduler 10 月 15 日发布 v0.18.6。改动集中在调度热路径：为任务做节点打分与排序时不再为每个 worker 单独构建 score map（#2409），降低大规模集群下的内存与分配开销。"
                 "修复两项：替换产生的子组（replacement subgroups）现在保持在 job 要求的拓扑域内（#2318）；调度器只删除失败的 BindRequest，binder 跳过已进入终态的对象、丢弃重复 reconcile 事件，并在重试期间保留 reservation（#2343）。",
                 "GPU 调度", "GitHub Releases",
                 det("面向 GPU 批任务的 gang/拓扑感知调度器：这次把「节点打分」从每 worker 一份 score map 改成任务级共享，并收紧 BindRequest 的生命周期管理（只删失败、跳过终态、去重 reconcile、重试保留 reservation）。",
                     "大规模 GPU 集群里，调度器每次打分都复制一份 worker 级 map 会放大内存与 GC；绑定失败重试时若把 reservation 提前释放，任务会被反复重新排队，表现为「明明有配额却一直 Pending」。",
                     "自建 GPU 集群、用 KAI 做 gang 调度的团队可以直接评估这个补丁版本；它属于稳定性修复而非新能力，升级收益取决于你是否踩到绑定重试或拓扑域漂移。"), True),
        ]},
        {"emoji": "☸️", "title": "K8s 核心技术", "en": "K8s Core", "items": [
            item("containerd 2.2.10：四个安全公告，日志软链、镜像引用 `..` 与 seccomp socket 域一起收紧",
                 U("containerd/containerd/releases/tag/v2.2.10"),
                 "containerd 2.2 线第 10 个补丁版 2.2.10（10 月 13 日）以安全修复为主，包含 CVE-2026-95839 与 GHSA-5p7c-hggf-c748、GHSA-8647-2jxj-p2rc、GHSA-hc94-p972-ch66 四个公告。"
                 "具体硬化项：CRI 不再跟随容器日志文件的符号链接；镜像分发拒绝含 `..` 路径组件的引用，并修复 multipart 拉取的挂起与数据损坏；默认 seccomp 配置改为对 socket 域做 allowlist。",
                 "容器运行时", "GitHub Releases",
                 det("2.2 维护线的安全补丁：日志文件符号链接不再被跟随、镜像引用拒绝 `..` 路径、multipart 镜像拉取的挂起/损坏修复、默认 seccomp 对 socket 域改 allowlist。",
                     "容器逃逸与镜像供应链攻击常从「路径穿越 + 符号链接」和过宽的 socket 域开始；这类问题不会在功能测试里暴露，只能靠运行时默认值收紧。",
                     "跑 2.2 线的节点应当尽快跟到这个补丁；若已在 2.3/2.4 线，昨天那期已覆盖对应补丁，不必回退。升级前确认自定义 seccomp profile 是否依赖被移除的 socket 域。"), True),
            item("Istio 1.30.6：HTTP/2 改方法大小写可绕过 AuthorizationPolicy，ambient 模式 istiod 可被打崩",
                 U("istio/istio/releases/tag/1.30.6"),
                 "Istio 1.30.6（10 月 15 日）是安全补丁版，对应 ISTIO-SECURITY-2026-007。两个高危项：GHSA-w44g-8m76-8gc5（CVSS 7.4）——通过改变 HTTP/2 方法的大小写可绕过 AuthorizationPolicy 的方法规则；GHSA-7p2q-4xvg-vxc6（CVSS 7.7）——ambient 模式下 ServiceEntry 等资源占用 IP 寻址 waypoint 的地址时 istiod 会崩溃。"
                 "另修 istioctl 在通过 service account token 连接 XDS 时跳过 istiod 证书校验的问题（现在默认用 istio-ca-root-cert 与 server name 校验，需显式 --insecure 才跳过），以及 manifest translate 把未转义值写进安装脚本导致的命令注入。",
                 "服务网格", "GitHub Releases",
                 det("修两个 Istio 高危（HTTP/2 方法大小写绕过 AuthZ、ambient 下 waypoint 地址冲突打崩 istiod），加两个 Envoy CVE（OAuth2/api_key_auth 在无 :path 的 CONNECT 请求上崩溃），并补上 istioctl 的证书校验与脚本注入。",
                     "授权策略被大小写绕过意味着「以为拒绝了 POST」实际放行；istiod 崩溃在 ambient 模式会直接影响整个网格的控制面，属于可远程触发。",
                     "跑 1.30 线且有 AuthorizationPolicy 或 ambient 部署的集群应优先升级；升级后重点回归 HTTP/2 方法规则与 waypoint 相关配置。1.31 线对应版本见官方公告。"), True),
            item("Envoy v1.39.4：RDS 更新时六处路由配置的跨线程析构竞态修掉了",
                 U("envoyproxy/envoy/releases/tag/v1.39.4"),
                 "Envoy 1.39.4（10 月 12 日）集中修复 RDS 路由配置替换时的竞态：aws（请求签名与 Lambda filter）、composite、dynamic_modules、filter_chain、local_ratelimit、sds 六处的路由级配置可能在 worker 线程被析构，甚至把动态模块就地卸载。"
                 "另修一个 1.38.0 引入的 stats bug：Prometheus native histogram 的 bucket index 多导出了一个桶。",
                 "数据面代理", "GitHub Releases",
                 det("修 RDS 更新替换路由配置时，路由级对象（AWS 签名/Lambda、composite、dynamic modules、filter chain、本地限流、SDS 密钥提供者）在 worker 线程被销毁的竞态；顺带修 native histogram 桶索引 off-by-one。",
                     "控制面频繁下发路由时，数据面偶发 crash 或模块被卸载，日志里往往只有 worker 线程崩溃栈，很难归因到「一次 RDS 更新」。",
                     "用 Envoy 1.38/1.39 且频繁变更路由（Gateway API、多租户网关）的环境值得升级；这是稳定性修复，不做会以低频崩溃的形式存在。"), True),
            item("Cilium 1.19.9：selector cache 数据竞争会导致 agent panic，endpoint GC 复用 ID 时误删新端点",
                 U("cilium/cilium/releases/tag/1.19.9"),
                 "Cilium 1.19.9（10 月 15 日）是 1.19 线的 bugfix 版。最值得关注的是 selector cache 中一个罕见数据竞争，可能导致 agent panic；以及 endpoint GC 迭代时复用刚被回收的 ID、错误删除新 endpoint 的问题。"
                 "其余修复包括：终止中的 backend 在重启期间重新变为 active 时被错误留在 quarantine；ip6tables 链重命名的错误被静默忽略；恢复保留内部 endpoint 时跳过清理；gateway-api 从 infrastructure metadata 过滤 CEC 控制项。",
                 "CNI", "GitHub Releases",
                 det("修 CNI agent 的稳定性问题：selector cache 数据竞争导致 panic、endpoint GC 的 ID 复用误删、终止 backend 的 quarantine 状态恢复、ip6tables 重命名错误被吞。",
                     "agent panic 会短暂丢失该节点的网络策略与端点状态；endpoint ID 复用误删则表现为「Pod 网络突然不通」，两类问题都难在事后定位。",
                     "仍在 1.19 线的集群建议跟补丁；已在 1.20.3 的按昨天那期走。Cilium 的补丁节奏很密，维护窗口里优先看 agent panic 与 GC 相关条目。"), True),
            item("Cluster API v1.13.7：KCP 在 Node 注册后误删 learner，proxy DialContext 竞态修复",
                 U("kubernetes-sigs/cluster-api/releases/tag/v1.13.7"),
                 "Cluster API v1.13.7（10 月 7 日）合入 10 个提交、修 4 个 bug。管理集群支持 v1.32–v1.36，工作负载集群 v1.30–v1.36。"
                 "修复项包括：KCP 在 Node 注册后误删 learner（#14210）、KCP proxy DialContext 的竞态（#14280）、没有 ClusterClass 的 Cluster 也补上 cluster-name 标签（#14309）；依赖侧把 grpc 升到 1.83.2 修安全公告、cert-manager 升到 v1.21.2。",
                 "集群生命周期", "GitHub Releases",
                 det("v1.13 维护版：修 KCP 的 learner 误删与控制面代理建连竞态，统一 Cluster 的 cluster-name 标签，并把 grpc 升到 1.83.2 以覆盖安全公告。",
                     "KCP 误删 learner 会让新控制面节点加入过程反复，表现为滚动升级卡住；DialContext 竞态则会造成控制面代理偶发连不上。",
                     "用 Cluster API 管多集群、且在做控制面滚动升级的团队建议跟到该补丁；版本支持矩阵已到 K8s 1.36，老版本管理集群需先确认兼容。"), True),
        ]},
        {"emoji": "☁️", "title": "云原生周边", "en": "Cloud Native", "items": [
            item("Cloudflare Containers 跨租户泄露复盘：Firecracker 没破，dm-thin 的 skip_block_zeroing 漏了 60 KiB",
                 CF_URL, cf_sum, "多租户隔离", "InfoQ 中国",
                 det("完整复盘一次块级跨租户泄露：dm-thin 64 KiB 块 + skip_block_zeroing，4 KiB 写入留下最多 60 KiB 前租户数据；研究者用 ext4 目录校验和统计归属。",
                     "隔离验证通常只测边界（microVM/网络），不测块分配器的复用路径；这一例证明性能开关可以在边界之下打穿多租户隔离。",
                     "把「分配时清零/释放时擦除」加入共享存储的验收项，并做原始读测试；对做 agent 沙箱或多租户容器的团队，这篇的时间线与命中率是最好的评审材料。")),
        ]},
    ]},
]

flash = [
    {"title": "KAI-Scheduler v0.16.12（10-18）维护版发布，0.16 线继续跟补丁。",
     "url": U("kai-scheduler/KAI-Scheduler/releases/tag/v0.16.12")},
    {"title": "Argo Workflows v4.1.5（10-09）补丁版发布，release 正文只指向 changelog。",
     "url": U("argoproj/argo-workflows/releases/tag/v4.1.5")},
    {"title": "llm-tools-datasette 0.1.1 修复 LLM 0.33 切 httpx2 后的插件断链。",
     "url": U("simonwillison.net/2026/Oct/18/llm-tools-datasette/")},
    {"title": "kubezilla 拆解 CNCF Landscape：300 star 入库门槛、TOC 晋级检查项与归档规则。",
     "url": U("kubezilla.io/cncf-landscape-explained")},
]

lead = ("今天的两条主线都不在榜单上。模型侧，Meta 把 8160 亿参数的 Muse Spark Open 开放权重，并用 NVFP4 加两台 M5 Ultra Mac Studio "
        "把「本地跑大型 agent 模型」变成可估算的硬件账——代价是编码基准输给 GLM 5.3 max 与 Kimi K3 max，许可证还带 2000 万美元的 MaaS 门槛。"
        "基础设施侧，Cloudflare 的事故复盘说明隔离的失败点常在边界之下：Firecracker 没被攻破，dm-thin 的 skip_block_zeroing 让 64 KiB 块里剩下 60 KiB 前租户数据，"
        "5614 个可测目录块全部命中他人内容。其余更新以安全补丁为主：Istio 修了 HTTP/2 方法大小写绕过授权，containerd 一次修四个公告，Envoy 补 RDS 析构竞态。")

brief = {
    "brand": "AI & 基础设施早报",
    "date_label": "2026 年 10 月 19 日 · 星期一",
    "issue": 29,
    "kicker": "DAILY",
    "hint": "👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回",
    "lead": lead,
    "highlights": highlights,
    "sections": sections,
    "flash": flash,
    "footer": "由 Hermes 自动汇编 · 每日 09:00 更新",
}

# --- assertions ---
proc_urls = {it["url"] for it in P}
seen = []
for h in brief["highlights"]:
    assert h["title"], "highlight title missing"
    seen.append(h["url"])
for s in brief["sections"]:
    for c in s["categories"]:
        for it in c["items"]:
            assert it.get("title"), f"missing title in {c['title']}"
            assert len(it.get("detail", [])) == 3, it["title"]
            seen.append(it["url"])
for f in brief["flash"]:
    seen.append(f["url"])
bad = [u for u in seen if u not in proc_urls]
assert not bad, f"URLs not from processed.json: {bad}"

json.dump(brief, open("briefing.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("briefing.json written:", len(seen), "urls,", sum(len(s['categories']) for s in sections), "categories")
print("highlights:", len(highlights), "items:", sum(len(c['items']) for s in sections for c in s['categories']), "flash:", len(flash))
