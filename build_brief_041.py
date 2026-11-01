#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 041 (2026-11-01)."""
import json

P = json.load(open('processed.json'))
by_url = {i['url']: i for i in P}


def U(frag):
    hits = [u for u in by_url if frag in u]
    if len(hits) != 1:
        raise SystemExit('URL lookup ambiguous/missing: %r -> %r' % (frag, hits))
    return hits[0]


def item(frag, title, summary, detail, tag=None, oss=None, source=None, note=None):
    u = U(frag)
    src = by_url[u]
    it = {
        'title': title,
        'url': u,
        'summary': summary,
        'tag': tag or src.get('category', '').replace('K8s × AI', 'K8s×AI'),
        'source': source or src.get('source', ''),
        'detail': [{'key': k, 'value': v} for k, v in detail],
    }
    if oss if oss is not None else src.get('oss'):
        it['oss'] = True
    if note:
        it['note'] = note
    assert it['title'] and it['summary'] and len(it['detail']) == 3
    return it


highlights = [
    item(
        'huggingface.co/papers/2610.34298',
        'MCP 与 CLI 能力对齐后行为仍分叉：2004 条轨迹里 94.3% 走了不同路径，DART 修复后最高 +9.0 分',
        '这篇论文问的是一个工程上很实际的问题：把同一批可执行能力分别以 MCP 和 CLI 两种形态暴露给模型，行为会不会变。作者做了 MICA（Matched Interface Comparison and Analysis），从共享的语义动作契约同时渲染出 MCP 与 CLI，并让解码出的动作走同一个运行时，在 6 个模型、3 个交互环境上对比。结果是能力相同、表现不同：任务成绩与交互成本都出现显著差异，而且差异不止在表层格式，还体现在语义动作选择、失败路径与恢复方式上。配对自然轨迹分析显示，2004 条 episode 中有 94.3% 出现结构性分叉，早期的差异会沿后续交互继续放大。作者据此提出 DART（Decoupled Action Realization and Targeted Repair）：保留已验证的语义承诺，只修接口相关的实现，在 6 个设置里全部涨分（最高 +9.0 分），并在三个环境里把 MCP 的 token 成本最多降低 27.1k/任务。',
        [
            ('能做什么', 'MICA 把 MCP 与 CLI 从同一份语义动作契约渲染出来，能力严格对齐、只变「模型看到的表示」；matched-state 探针进一步把敏感点定位到能力呈现、实现方式与反馈格式三处；DART 在不动语义决策的前提下重写接口实现，并保留已验证的语义承诺。'),
            ('解决什么痛点', '给 agent 接工具时，选 MCP 还是 CLI 常被当成风格问题；实测同样的能力换个接口形态，任务成绩和 token 成本都会变，且错误会从第一步一路传染到后续交互。它把「接口实现」确认为可直接干预的变量，而不是只能事后调 prompt。'),
            ('值不值得', '做多用户 agent 平台、要决定工具暴露形态的人值得读：结论是接口层可以单独优化，+9.0 分与 -27.1k token/任务是可量化的收益。限制是评测只在三个交互环境内，6 个模型的具体版本会随发布过期；DART 需要维护一份语义契约，等于给工具层再加一层抽象。'),
        ],
        tag='Agent 评测',
        note='🔎 新闻要点：方法 = MICA，从共享语义动作契约渲染 MCP/CLI 并共用运行时；规模 = 6 个模型 × 3 个交互环境；结果 = 能力匹配下任务成绩与交互成本显著不同，2004 条 episode 中 94.3% 结构性分叉，早期差异向后传播；诊断 = matched-state 探针定位到能力呈现、实现方式、反馈格式；修复 = DART，6 个设置全部提升，最高 +9.0 分，MCP token 成本最多降 27.1k/任务。',
    ),
    item(
        'the-three-layer-gke-network-mystery',
        'GKE 控制面静默丢包查了两个月：三层 bug 叠加，根因是 Linux 6.1 的 tcp_ack() 静默丢弃合法 FIN',
        'Google Cloud 复盘了一起 2026 年 1 月起的 GKE 故障：Pod 间歇性连不上 kube-apiserver、报 i/o timeout，最终波及 europe-west 五个集群、约 800 名开发者数周无法发布。排障先把自定义 operator、External Secrets Operator、安全 agent、conntrack 耗尽与控制面过载全部排除——conntrack 只用到 1.3M 默认上限的约 50%，扩容控制面也没有改善。同时在 KCP 虚机网卡与 kube-apiserver 容器内同时抓包后发现：新连接的 SYN 收到的是属于几分钟前另一条连接的 ACK，Wireshark 把它标成「TCP Port numbers reused」。根因是三层叠加：Private Service Connect 的 USPS 对新流走慢路径，导致 FIN/RST 相对 ACK 乱序；Envoy 用 SHUT_WR 半关闭，使 socket 不被内核视为 orphan，tcp_fin_timeout 不启动，socket 长期停在 FIN_WAIT_2；Linux 6.1 的 tcp_ack() 对「旧但仍在 RFC 5961 可接受窗口内」的 ACK 返回 0，FIN 处理路径看到 0 就静默丢弃。端口被 NAT 复用后内核发出 challenge ACK，而 USPS 的一次安全修复恰好把这类 ACK 当非法包丢弃，故障闭环形成。修复分三级：先回滚 USPS 止血，再做正确处理 challenge ACK 的替换变更并加 PacketDrill 回归测试，最后是 Eric Dumazet 的内核补丁（6.9.7 合入，回移 6.6.y / 6.1.y，随 GKE 1.33.5 起下发）。',
        [
            ('能做什么', '给出一套可复用的三层排障方法：在宿主机网卡、PIGv 虚拟网卡与容器内三点同时抓包，用「SYN 收到旧 ACK」这一异常定位到 FIN_WAIT_2 泄漏，再把 pcap 时间轴与 PSC 的 USPS 指标尖峰对齐，最后在实验环境复现内核行为。'),
            ('解决什么痛点', '这类故障的可怕之处是三层各有合理解释、每层解释都不完整：应用层看是超时，网络层看是 conntrack，内核层看是 TCP 状态机。只看单层日志会一直误判为业务问题，而实际是「乱序 + 半关闭 + 内核丢 FIN」三者叠加才致命。'),
            ('值不值得', '用 PSC 暴露控制面的 GKE 集群值得直接对号入座：症状是 i/o timeout、多个集群同时中招、系统组件也连不上自己的 API server。判断依据是修复已在 GKE 1.33.5 及以后的内核里；自建集群则要确认内核是否含 795a7dfbc3d9（6.1.y / 6.6.y 回移），老 COS 镜像这类 6.1 基线最容易中。'),
        ],
        tag='K8s 网络',
        note='🔎 新闻要点：时间线 = 2026-01 起、Day 15 升级 P0、2 月回滚 USPS、3 月初恢复；影响 = 5 个集群、约 800 名开发者、europe-west；Bug #1 = PSC 的 USPS miss 慢路径使 FIN/RST 相对 ACK 乱序；Bug #2 = Envoy SHUT_WR 半关闭使 socket 非 orphan，tcp_fin_timeout(60s) 不触发，FIN_WAIT_2 停留 >120s；Bug #3 = Linux 6.1 的 tcp_ack() 对 old-but-acceptable ACK 返回 0，tcp_fin() 未被调用、合法 FIN 被静默丢弃；放大因素 = PSC NAT 让多 Pod 共用源端口、5-tuple 冲突率高，challenge ACK 触发频繁，而新版 USPS 丢弃「invalid ACK」；修复 = USPS 回滚 → 替换变更 + PacketDrill 测试 → 内核 commit 795a7dfbc3d9（6.9.7 修复，回移 6.6.y / 6.1.y，GKE 1.33.5+）。',
    ),
]

sections = []

ai_cats = [
    {
        'label': '🧠 模型与研究',
        'en': 'Models & Research',
        'items': [
            item(
                'infoq.cn/article/O6mtiB7FVd0VSDHJe348',
                'EmbeddingGemma 2：文本/代码/图像/视频/音频共用 768 维空间，参数量 2.7 亿到 7.4 亿',
                'Google 发布 EmbeddingGemma 2，Apache 2.0、基于 Gemma 4 的紧凑多模态嵌入模型，把文本、代码、图像、视频与音频映射进同一个 768 维空间，检索系统不必再为每种模态维护互不兼容的嵌入。可按需只加载所需编码器，参数从 2.7 亿（文本/代码）到 7.4 亿（全模态），面向手机与笔记本等消费级硬件。支持 MRL 截断：100 万个 768 维 bf16 向量约 1.5GB，截到 128 维只需 250MB，但 128 维下文本任务保留约 90% 质量、图像/视频/语音掉到约 75%。',
                [
                    ('能做什么', '用一份权重、一个 768 维空间同时做文本、代码、截图、录音与视频检索；编码器按需加载，MRL 让同一份向量可截断到 128 维以压存储与提速。官方称在代码搜索与技术内容检索上显著超过 EmbeddingGemma 1。'),
                    ('解决什么痛点', '多模态检索过去要为每种模态各养一个嵌入模型与一套索引，跨模态对齐靠额外映射；设备端场景又受显存与存储限制，1.5GB 的向量库在手机上放不下。'),
                    ('值不值得', '做本地代码库索引、私有知识库或端侧 RAG 的可以直接试：128 维只掉 10% 文本质量、存储降到六分之一，是很实用的折中。注意两个已知坑——索引文档必须用 title: none | text: 前缀，MRL 要先切片再对短向量做 L2 归一化，否则范数不对。'),
                ],
                tag='嵌入模型',
            ),
            item(
                'huggingface.co/papers/2610.38331',
                'Soft-MTP：一行改动去掉 MTP 梯度里的噪声残差，167M→1.2B 全线优于标准 MTP',
                '论文指出标准多 token 预测（MTP）训练有个被忽视的缺陷：MTP 的交叉熵梯度可精确分解为一个 KL 自蒸馏项——把每个 MTP head 拉向模型自身的下一 token 分布，正是投机解码受益的来源——和一个信噪比很低的残差，后者会同时干扰 next-token 与多 token 学习，并随规模放大。作者给出 KL gradient-recovery：当两个分布共享线性输出头时，用 straight-through 梯度路由组合两者的交叉熵梯度即可精确还原 KL 梯度，不需要词表大小的 logit 矩阵，也兼容标准融合交叉熵 kernel。据此的 Soft-MTP 只是一行改动，不加参数、无可测开销，兼容 DeepSeek 与 Meta 两种 MTP 结构，在 167M 到 1.2B 参数上均优于标准 MTP。',
                [
                    ('能做什么', '把 MTP 训练中真正有用的 KL 自蒸馏信号与噪声残差分离，只回传前者；复用已有的 NTP/MTP 交叉熵计算，不需要额外的大矩阵，工程上是改一行代码的量级。'),
                    ('解决什么痛点', 'MTP 已是主流预训练配方，但它的收益有一部分被梯度噪声抵消，且模型越大越明显——等于白付了 MTP 的算力与显存。'),
                    ('值不值得', '自己做预训练或继续预训练、且已经在用 MTP 的值得直接套：零参数、零可测开销，还顺带提升投机解码的接受率。限制是结论止于 1.2B 参数的受控实验，更大规模与长训练周期下的表现论文没给。'),
                ],
                tag='训练方法',
            ),
        ],
    },
    {
        'label': '🧩 Agent & Skill',
        'en': 'Agents & Skills',
        'items': [
            item(
                'infoq.cn/article/FJqN3mFVyN1lMqHOiegs',
                'Google 开源 EnvHarness：不改智能体、不改环境，只换交互层，四个模型普遍涨 2.9–3.7 个点',
                'EnvHarness 是 Google 研究人员开源的框架，用来按智能体的短板动态改造训练环境，前提是不动智能体、不动环境本身、也不动评估系统。动机很直接：自我进化型智能体只会重写提示词、学新技能，很少改环境，于是在固定基准上练到能解所有任务后就没有新信号了；而重新造环境成本高、要领域流水线，还要依赖昂贵或不可靠的验证器。EnvHarness 用标准 reset()/step() 把现有环境包一层可编程封装，只改智能体看到的交互接口，提供三种可组合组件：setup 定义初始状态、rule 约束状态转移、link 定制观察呈现。配套的 EnvRigger 会分析智能体行为、找出反复出现的薄弱点、生成针对性修改并用新交互验证，循环跑下去形成智能体与环境的共同进化。论文报告在 WebArena、SWE-bench Verified、ALFWorld 上均有提升，Gemini 3.1 Flash-Lite、Qwen3.6 27B、Gemini 3.5 Flash、Claude Sonnet 4.6 四个模型提升 2.9–3.7 个百分点，且原任务与人工验证器保持不变。',
                [
                    ('能做什么', '在不碰智能体代码与环境源码的前提下，用 setup/rule/link 三个组件改写「智能体看到什么、能做什么、得到什么反馈」；EnvRigger 自动从行为轨迹里找薄弱点并生成下一轮环境变体。'),
                    ('解决什么痛点', '固定基准一旦被刷满就失去训练信号，而造新环境是最贵的一环；同时改环境和评估又会让分数不可比。只换交互层等于把「环境生成」降级成「接口改写」。'),
                    ('值不值得', '做 agent 训练或评测流水线的值得看它的抽象：保留原验证器、只包一层，是成本最低的持续加难方案。限制是它仍需领域相关的封装逻辑（作者也这么说），且 2.9–3.7 点的提升是在已有基准上，不等于泛化能力提升。'),
                ],
                tag='Agent 训练',
            ),
            item(
                'huggingface.co/papers/2610.38342',
                'Investor\'s Last Exam：343 万份文档版本冻结时点，前沿模型总分 68.1，预测建模只有 52.5',
                'ILE 是买方投资人主导的股票研究基准，核心是把信息集严格冻结：版本化财务数据库覆盖 343 万份文档版本、九类来源，配结构化行情数据，检索与计算都受校验过的时间戳约束。评分不只看结论，而是用金融依赖图把评分标准绑定到来源、计算与假设，覆盖 86 个作业，同时评研究质量、预测准确率与模拟投资表现。GPT-6 Astra 与 Claude Opus 5.5 以 68.1 / 66.9（满分 100）领先，但 Astra 在「预测与建模」单项只有 52.5——说明当前最强模型仍无法把研究能力转化成预测能力。',
                [
                    ('能做什么', '第一次把「证据 → 假设 → 判断」这条链拆成可打分的环节：同一份冻结信息集下，能看出模型是在检索、计算还是假设环节掉分，而不是只给一个总分。'),
                    ('解决什么痛点', '金融 agent 的评测长期靠知识问答或单点预测，前者不涉及判断、后者无法归因；而且不冻结信息集就会泄漏未来信息，分数虚高。'),
                    ('值不值得', '量化研究侧最该看的是它的问题构造方式：86 个作业、依赖图绑定来源与计算，比榜单数字有用。限制是基准闭源程度与更新节奏未知，68.1 这类绝对值会随模型版本快速过期，真正的信号是「研究能力 68、预测能力 52」这个结构性缺口。'),
                ],
                tag='金融基准',
            ),
            item(
                'huggingface.co/papers/2610.38293',
                'EPSBench：六个模型对分析师共识没有优势，标称 80% 的预测区间实际只覆盖 37–70%',
                'EPSBench 用 149 个公司季度（86 家美国公司）测 agent 的季度盈利预测：agent 读固定的财报、电话会记录与新闻，给出带引用的利润表驱动项估计，再由共享的会计计算器折算成 GAAP 稀释 EPS。与同日期的分析师共识对比，六个模型里有三个的点预测误差没有显著差异、三个更差；更严重的是标称 80% 的预测区间只在 37–70% 的运行里真正覆盖了实际 EPS，且多数漏在上界之上（预测系统性偏低）。模型之间的误差差距主要来自营业利润这一项估计。',
                [
                    ('能做什么', '把「预测 EPS」拆成可核对的驱动项：每个利润表科目都要给估计值与引用证据，再用统一会计计算器折算，误差因此可以归因到具体科目而不是笼统的「预测不准」。'),
                    ('解决什么痛点', 'agent 做财务预测最常见的失败是「看起来很专业、区间毫无意义」；只报点预测无法暴露校准问题，而覆盖率 37–70% 说明模型对自己的不确定性完全没有概念。'),
                    ('值不值得', '做量化因子或投研 agent 的，这份结论值得当基线：目前 LLM agent 在季度 EPS 上打不过分析师共识，且区间不可信。可复用的部分是它的评测口径（GAAP 折算 + 带引用驱动项），可以直接搬进内部评测。'),
                ],
                tag='金融基准',
            ),
            item(
                'arxiv.org/abs/2610.40578',
                'VeriCUA：把任务完成验证做成「agent 自己去查证」，跨桌面/移动/Web 统一一套流程',
                '计算机使用 agent（CUA）在桌面、移动、Web 上跑，最缺的是可靠的任务完成判定——数据清洗、评测、强化学习都要它。常见做法要么让 VLM 看轨迹打分，要么生成程序去读应用状态，两者都只看到局部：VLM 只能用给定的观测，程序依赖可访问的内部状态，关键证据可能根本不在视野里；而且为不同平台、不同访问方式各写一套验证器，工程成本会持续叠加。VeriCUA 把验证变成一次 agent 式探索：先看可用上下文写出任务 rubric，再针对未满足的要求选择 GUI 检查或代码检查，最后按显式证据规则合并结论，在线与离线、不同平台与观测模态共用同一套流程。实验显示与参考标注的一致率优于对比基线，离线难例提升最大，在线对「假称完成」的拒绝更强。',
                [
                    ('能做什么', '把「任务做完了吗」从单次判断改成主动取证：自建 rubric、按需选择 GUI 或代码检查、按证据规则合并；同一套流程覆盖在线与离线、桌面/移动/Web。'),
                    ('解决什么痛点', 'CUA 的强化学习与评测都卡在验证上——VLM 裁判会被漂亮的轨迹骗过，程序化检查又依赖内部状态；验证不可靠，RL 的奖励就是噪声。'),
                    ('值不值得', '做 agent 平台的可以直接借用它的 rubric + 证据合并结构，比自己拼 VLM 裁判更可控。限制是它本身也是 agent 流程，单次验证成本更高，论文未给出延迟与成本数据。'),
                ],
                tag='Agent 验证',
            ),
        ],
    },
    {
        'label': '🛠️ AI 工程落地',
        'en': 'AI in Production',
        'items': [
            item(
                'huggingface.co/papers/2609.05881',
                '审计 305 个 GGUF 量化包：7 个官方 tag 连 164 题里 6 题都做不对，权重却一个字节没坏',
                '论文审计了 Ollama 官方库里 15 条模型线的 305 个可用代码类 GGUF tag，外加 22 个 Hugging Face 社区热门文件——所有被检查的注册表都没有记录过功能测试。15 题代码筛查找出可疑项，再用全部 164 道 HumanEval+ 复测：7 个官方 tag（2.3%）最多只做对 6 题，全是参数量不超过 4B 的低比特量化。作者从原始权重重建了其中 5 个，与注册表文件逐 tensor 完全一致，说明不是文件损坏，而是量化配方本身把能力打没了。在权重、工具链与 tensor 组合都固定的情况下，加 importance matrix 让 Qwen2.5-Coder-3B 在三个量化档位从 0 题提升到 76–113 题；同样的未校准配方对 Qwen2.5-Coder-1.5B 却仍然可用，说明单看配方无法预测失败。',
                [
                    ('能做什么', '给出一套可复现的量化包体检流程：15 题代码筛查做初筛、164 题 HumanEval+ 复测做判定，并用逐 tensor 比对区分「文件损坏」与「配方失效」；同时开源审计数据与 quantcheck 工具。'),
                    ('解决什么痛点', '从注册表下载 GGUF 本地跑是最常见的私有化路径，而注册表从不做功能测试——一个 2.3% 的失败率意味着你随手拉的量化包里可能就有「能加载、能生成、但代码全错」的版本。'),
                    ('值不值得', '自建推理服务、把模型权重固化进镜像的，值得把 15 题筛查加进上线前的门禁：成本极低，能挡住这类静默失效。结论也提示优先选带 importance matrix 校准的量化产物，并注意小模型（≤4B）低比特量化的风险显著更高。'),
                ],
                tag='模型运维',
            ),
            item(
                'infoq.cn/article/HHgKMMKa8BNZYQuMFSMS',
                'Efiwe：把 Python 与 SQL 塞进手机浏览器离线跑，2.2 万学习者、160 个国家',
                '作者复盘了自己做的编程教育平台 Efiwe：面向没有笔记本、网络不稳、付不起订阅的学习者，用 PWA 分发，首次加载后离线可用，代码在设备本地执行。执行层用 Pyodide（编译成 WebAssembly 的 CPython）与 sql.js（WebAssembly 版 SQLite），两者体积大、初始化慢，处理不好会阻塞主线程；作者因此定了一条硬规则——任何运行时都不在主线程初始化、也不提前初始化，学生选课时才按需起 Worker，挑战页首屏绝不等待运行时。目前有 2.2 万多名学习者、覆盖 160 个国家，在尼日利亚拉各斯州、奥贡州与印度北阿坎德邦有组织试点；早期一批 80 名学员只有 6 人毕业，多数是网络撑不到下课。文中把踩过的坑归到存储、配额、冷启动与失败路径四类，而不是模型质量。',
                [
                    ('能做什么', '用 PWA + Service Worker 把「安装」变成「点开就开始」，用 Pyodide / sql.js 把判题执行放到设备本地，做到一次加载后零流量判题；Worker 化保证首屏不被运行时初始化阻塞。'),
                    ('解决什么痛点', '把每次判题发到服务器，在弱网教室里根本跑不通（学生要试 10–12 次才能解一题）；而原生 APK 的安装流量本身就是门槛。'),
                    ('值不值得', '做端侧 / 弱网产品的人值得读它的失败路径设计：存储配额、冷启动、离线升级这些坑与模型质量无关，却决定留存。限制是文章只讲前端工程，没给 Pyodide 在低端机上的实际耗时数据。'),
                ],
                tag='端侧工程',
            ),
        ],
    },
    {
        'label': '📊 产品与商业',
        'en': 'Products & Business',
        'items': [
            item(
                'qbitai.com/2026/10/506855',
                'Anthropic 把 Max 20x 改名 Ultra 并取消 5 小时窗口，周额度仍是 Pro 的 10 倍',
                'Anthropic 调整高价订阅：Max 5x / Max 20x 改名为 Max / Ultra，200 美元的 Ultra 在周额度内可连续使用，不再受 5 小时窗口限制，周额度维持 Pro 的 10 倍。现有 Ultra 用户已陆续放开，新账号需通过账号与支付历史自动验证。负责订阅产品的 Mike Overell 承认「20x」原本指单个 5 小时窗口的 20 倍、与用户对周额度的理解存在偏差，并为沟通问题道歉。',
                [
                    ('能做什么', '把「每 5 小时重置」改成「每周额度内连续用」，长任务不再被窗口切断；套餐命名从倍数改成档位（Max / Ultra）。'),
                    ('解决什么痛点', '跑长时 agent 或连续编码的人，5 小时窗口会在任务中途重置额度，实际可用量取决于起始时间点而非需求。'),
                    ('值不值得', '按 200 美元档在用的人值得确认 Settings → Usage 里的 5 小时进度条是否已消失；周额度没变，所以总容量没涨，只是分配更连续。注意验证是自动的，新账号可能还要等。'),
                ],
                tag='定价',
            ),
        ],
    },
    {
        'label': '💡 观点与好文',
        'en': 'Essays & Insight',
        'items': [
            item(
                'how-i-built-the-most-ai-pilled-company-in-the-world',
                'Spawn：每月烧 300 万美元 token，让 agent 直接改线上代码、每小时上线，一小时没发布算 SEV-0',
                'Jacob Sansbury 的这篇复盘是一个把 agentic engineering 推到极端的样本：Spawn 是多人游戏环境，玩家用提示词让游戏内 agent Savi 直接改世界，Simon Willison 在手机上几句话就造出城堡、龙，并骑着龙飞了一圈。开发侧由一群 Fable 级模型驱动的 agent 自主进行，每月 token 花费超过 300 万美元，作者的说法是「AI token 开销是工资的 30 倍」。agent 直接改线上代码并每小时发布，自己读错误、bug 报告与指标；约 60% 的工作起点是生产错误、Savi 提的 bug、日志异常或功能请求，Savi 自己会提 bug，问题进到一个 agent 判断是真 bug、不修还是设计决策，通常一小时内作为变更回到提出者。配套的运维纪律是：一小时没有发布按 SEV-0 处理——未发布的改动会堆积、线上问题会拖更久、反馈变慢，而 agent 只能把几小时的上下文放在脑子里；坏改动可在 30 秒内就地回滚，监控或日志告警会唤起一个「拥有该事故」的 agent。',
                [
                    ('能做什么', '展示了一套闭环：生产错误/用户反馈 → agent 判定 → 直接改线上代码 → 一小时内发布 → 30 秒就地回滚，并把「不发布」本身定义为事故。'),
                    ('解决什么痛点', 'agent 写代码的瓶颈不在生成，而在反馈周期与上下文长度：长流水线会让 agent 丢掉上下文，人工评审队列又比 agent 产出慢一个数量级。'),
                    ('值不值得', '值得读它的运维约束（发布节奏当作 SLA、回滚半径压到最小、告警直接唤起责任 agent），这些与业务无关、可移植。但别照搬：每月 300 万美元 token 换来的容错来自「可以随便错、30 秒回滚」，放到金融这类高 stakes 系统上前提不成立。'),
                ],
                tag='工程实践',
            ),
            item(
                'simonwillison.net/2026/Oct/30/nesformer',
                '把 NES 模拟器塞进 Qwen3.5-4B 的权重里：能玩《超级马里奥》，就是很慢',
                'Drew Breunig 受 qwenputer 启发，把一台能跑 Nintendo Entertainment System 6502 CPU 的模拟器「烤」进了 Qwen3.5-4B 的权重，可以直接加载 NES ROM 玩《超级马里奥兄弟》，速度很慢。他在 Hacker News 的评论里公开了构建用的 Opus 5.5 提示词：先让模型读 qwenputer 的文章与源码，再探索能否在权重里模拟芯片与内存。',
                [
                    ('能做什么', '用语言模型的权重承载一个确定性状态机（6502 CPU + 内存 + 帧缓冲），输入是 ROM 与按键、输出是画面。'),
                    ('解决什么痛点', '它不解决实际问题，但给「权重里到底能编码多少确定性计算」提供了一个可玩的上界样例。'),
                    ('值不值得', '当趣味项目看即可，工程上无直接用途；真正的信息是这类「把计算烤进权重」的实验已经能被一次性提示词复现，说明长上下文 + 代码理解的组合门槛在快速下降。'),
                ],
                tag='趣味',
            ),
        ],
    },
    {
        'label': '🛡️ 安全与治理',
        'en': 'Security & Governance',
        'items': [
            item(
                'how-we-took-over-chatgpt-accounts',
                'Parameter Labs 用四条链拿下 ChatGPT 账号：MathLive postMessage → innerHTML → YouTube oEmbed 反射 JS',
                'Parameter Labs 公布了针对 ChatGPT「HTML 预览」（原 Canvas）的攻击链：OpenAI 用 MathLive 做图形支持，该库的虚拟键盘可被沙箱 iframe 通过 postMessage() 在父页面触发，而接收端用 innerHTML 拼接，且没有限制其他沙箱 frame（包括 HTML 预览）调用这个方法。注入的新 iframe 不带 sandbox 限制，CSP 虽禁内联脚本但允许从少数域加载脚本，其中 YouTube 的 oEmbed 端点可被用来反射回可执行的 JavaScript。拿到 JS 执行后，读取用户私有数据并经图片引用外带就是常规操作——一个分享链接即可在他人登录态下窃取数据或代为操作。OpenAI 已修复并支付 5000 美元赏金，Simon Willison 认为对这个严重级别偏低。',
                [
                    ('能做什么', '完整展示了一条「沙箱逃逸四步链」：跨 frame 的 postMessage 入口 → innerHTML 注入 → 无 sandbox 的子 iframe → 白名单域（YouTube oEmbed）反射脚本，最后是数据外带。'),
                    ('解决什么痛点', '渲染用户/模型生成的 HTML 是 agent 产品的标配（预览、artifact、可交互输出），而沙箱边界往往只防了直接脚本执行，没防「借父页面已信任的库做跳板」。'),
                    ('值不值得', '做 HTML 预览、artifact 或任何 iframe 沙箱的团队应当按这条链自查：postMessage 接收端是否用 innerHTML、是否校验 origin 与 frame 来源、白名单域里有没有可反射内容的端点。限制是文章是转述，原始细节要看 Parameter Labs 的报告。'),
                ],
                tag='沙箱安全',
            ),
        ],
    },
]
sections.append({'label': '🤖 AI 板块', 'categories': ai_cats})

infra_cats = [
    {
        'label': '🤖☸️ K8s × AI',
        'en': 'K8s × AI',
        'items': [
            item(
                'grove/releases/tag/v0.2.0-beta1',
                'Grove v0.2.0-beta1：API 升到 v1beta1，packDomain 改名 pack.required，minReplicas 默认改跟 minAvailable',
                'NVIDIA 系的 K8s AI 工作负载编排器 Grove 10 月 30 日发 v0.2.0-beta1，把 grove.io 与 operator.config.grove.io 两组 API 提升到 v1beta1，并让 v1beta1 成为存储版本；v1alpha1 仍提供服务但已弃用，每次请求返回弃用告警，PodCliqueSet 由 operator 的 conversion webhook 在两个版本间转换。新版本行为与 v1alpha1 一致，只删掉不再使用的字段：topologyConstraint.packDomain 移除、改用 pack.required（旧值会被自动转换），PodCliqueSetStatus.podGangStatuses 移除，operator 配置里去掉 KaiSchedulerConfiguration。一个容易踩的默认值变化是：PodClique 与 PodCliqueScalingGroup 的 scaleConfig.minReplicas 现在默认等于 minAvailable 而不是 replicas，autoscaler 因此可以缩到 minAvailable。升级需带 crdInstaller.upgradeCRDs=true，已有对象不会被重写，storedVersions 变成 [v1alpha1, v1beta1]，并提供了 run-api-downgrade 以便 Helm 回滚到 v0.1.0-alpha.16。',
                [
                    ('能做什么', '给 AI 推理负载提供 K8s 侧的分组编排原语：PodCliqueSet / PodClique / PodCliqueScalingGroup 描述「哪些 Pod 必须一起调度、一起伸缩」，配合 PodGang 交给 gang 调度器，v1beta1 把这些 CRD 从 alpha 提升为可长期依赖的 API。'),
                    ('解决什么痛点', '大模型推理的 prefill/decode 与多角色组件有强耦合的启动顺序与拓扑约束，Deployment/StatefulSet 表达不了「整组要么全起要么不起」；v1beta1 的意义是终于可以按稳定 API 写清单，不用再赌 alpha 字段。'),
                    ('值不值得', '已经在用 Grove（或跟着 Dynamo 生态走）的必须按 release notes 改清单：packDomain → pack.required，且 minReplicas 默认值变化会直接改变缩容下限。还在选型阶段的可以观察——它仍是 beta、且 operator 配置 API 还会再变一次。'),
                ],
                tag='K8s×AI',
            ),
        ],
    },
    {
        'label': '☸️ K8s 核心技术',
        'en': 'K8s Core',
        'items': [
            item(
                'announcing-workload-conformance-wg',
                'Kubernetes 新设 Workload Conformance WG：给「工作负载怎么跑」写标准，每条要求必须有可执行测试',
                'Kubernetes 社区成立 Workload Conformance Working Group，要给工作负载在集群上的运行行为写一份共享标准。动因是认证体系缺了一环：Certified Kubernetes 测集群，AI Conformance 测集群能不能跑 AI/ML 负载，但没有东西测工作负载本身——于是每次例行维护或升级前，集群运维只能逐个应用手工检查，节点 drain 时才发现应用扛不住中断、升级时才发现还依赖已移除的 API 版本。范围覆盖安全、中断韧性、资源使用、网络、存储、API 用法与可观测性，具体要求和测试方式尚未定；已定死的一条规则是每条要求都必须能被测试二进制客观验证，主观项不进规范。规范只管「怎么跑」不管「做什么」，应用逻辑不在范围内，也不重复 Certified Kubernetes 已覆盖的项、不指定打包格式或厂商工具。目标是两到三个 release 周期内出第一版稳定规范与可运行测试。',
                [
                    ('能做什么', '把「这个工作负载能不能安全地跑在我的集群上」变成一份可执行清单：安全、中断韧性、资源、网络、存储、API、可观测性七类要求，每条都配测试二进制。'),
                    ('解决什么痛点', '同一套评估被每个集群运维重复做一遍，应用维护者又要回答每个环境的同样问题；而现有文档是散落的指南，无法自动化，也没法作为升级前的门禁。'),
                    ('值不值得', '自建集群、要定「业务接入标准」的人值得跟：它给出的正是准入清单的骨架，且明确不绑定打包格式与厂商工具，可直接映射成内部接入评审项。限制是现在只有范围和原则，没有一条具体要求，两三个 release 周期内别指望能落地。'),
                ],
                tag='标准',
            ),
        ],
    },
    {
        'label': '🌐 云原生周边',
        'en': 'Cloud Native',
        'items': [
            item(
                'infoq.cn/article/fcdAAd69U452t9b39rLU',
                'AWS Lambda 支持直接跑 Express/Hono：并发请求 + 流式响应，按活跃 CPU 计费',
                'AWS 推出 Lambda Web Functions，可以在 Lambda 上直接运行 Express、Hono、Fastify、Next.js 等 Node.js 框架写的标准 HTTP 服务器，无需适配层，一条命令部署。新函数支持并发 HTTP 请求与流式响应（含 LLM 增量输出、SSE），计费按活跃 CPU 时间与内存，等待下游服务期间不计 CPU；多区域路由把请求送到最近区域，预热好的执行环境可同时处理多个请求，冷启动显著减少。原有 Lambda 函数改称 Event Functions、无需改动；端点默认用 Lambda 域名，要自定义域名、边缘缓存或 WAF 需前置 CloudFront。目前仅支持 Node.js。',
                [
                    ('能做什么', '把「一请求一调用」的模型换成常驻 HTTP 服务器 + 并发处理：同一个执行环境同时接多个请求，支持 SSE 与流式输出，按活跃 CPU 而不是等待时间计费。'),
                    ('解决什么痛点', '传统 Lambda 的编程模型要求把框架拆成 handler，等待数据库或下游的时间也计入时长；对流式 LLM 输出尤其别扭，往往还得单独挂一层托管。'),
                    ('值不值得', '适合间歇性流量的 Web/API 后端，尤其想把 LLM 增量输出直接吐给客户端又不想维护容器的场景。要留意两点：并发进来后同步与互斥要自己管（不再是天然隔离），以及内存仍按整个执行环境生命周期计费。'),
                ],
                tag='Serverless',
            ),
        ],
    },
]
sections.append({'label': '☸️ 基础设施板块', 'categories': infra_cats})

flash = [
    {'title': 'KubeCon + CloudNativeCon NA 2026（11/9–12，盐湖城）End User TAB 发布参会建议', 'url': U('kubecon-cloudnativecon-na-2026-end-user-tab')},
    {'title': 'lightpanda-io/browser：专为 AI 与自动化设计的无头浏览器（开源）', 'url': U('github.com/lightpanda-io/browser')},
    {'title': '英伟达基于 MiniMax H3 的开源视频增强方案，最高支持 4K 重生成', 'url': U('qbitai.com/2026/10/506743')},
    {'title': 'THU-MAIC/OpenMAIC：一键起一个多智能体互动课堂', 'url': U('github.com/THU-MAIC/OpenMAIC')},
]

EMOJI = {
    '🧠 模型与研究': '🧠', '🧩 Agent & Skill': '🧩', '🛠️ AI 工程落地': '🛠️',
    '📊 产品与商业': '📊', '💡 观点与好文': '💡', '🛡️ 安全与治理': '🛡️',
    '🤖☸️ K8s × AI': '🤖☸️', '☸️ K8s 核心技术': '☸️', '🌐 云原生周边': '🌐',
    '🏛️ 社区与项目': '🏛️',
}
for s in sections:
    for c in s['categories']:
        c['title'] = c['label']
        c['emoji'] = EMOJI[c['label']]

brief = {
    'brand': 'AI & 基础设施早报',
    'date_label': '2026 年 11 月 1 日 · 星期日',
    'issue': 41,
    'kicker': 'DAILY',
    'hint': '👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回',
    'lead': '周日这两篇最值得读，都是把「看不见的失败」摊开的材料。一篇是 Google Cloud 对 GKE 控制面故障的完整复盘：三层 bug 叠加——PSC 的 USPS 让 FIN 乱序、Envoy 的 SHUT_WR 让 socket 停在 FIN_WAIT_2、Linux 6.1 的 tcp_ack() 静默丢掉合法 FIN——五个集群、约 800 名开发者卡了几周，最终靠一个内核补丁收尾。另一篇是 MCP 与 CLI 的受控对比：能力严格对齐后，2004 条轨迹里 94.3% 仍走不同路径，说明接口形态本身就是决策环境的一部分。工程侧还有两份硬数据：305 个 GGUF 量化包里有 7 个官方 tag 基本不能用，而权重一个字节没坏；六个模型在季度 EPS 预测上对分析师共识没有优势，标称 80% 的区间只覆盖 37–70%。基础设施侧，Kubernetes 新设 Workload Conformance WG，要给「工作负载怎么跑」定标准；Grove 把 API 推到 v1beta1。',
    'highlights': highlights,
    'sections': sections,
    'flash': flash,
    'footer': '由 Hermes 自动汇编 · 每日 09:00 更新',
}

for it in [x for s in sections for c in s['categories'] for x in c['items']] + highlights:
    assert it['url'] in by_url, it['url']
    assert it['title'] and it['summary'] and len(it['detail']) == 3
for f in flash:
    assert f['url'] in by_url, f['url']

json.dump(brief, open('briefing.json', 'w'), ensure_ascii=False, indent=1)
n = sum(len(c['items']) for s in sections for c in s['categories']) + len(highlights)
print('items:', n, 'flash:', len(flash))
