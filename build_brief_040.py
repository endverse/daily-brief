#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build briefing.json for issue 040 (2026-10-30)."""
import json

P = json.load(open('processed.json'))
by_url = {i['url']: i for i in P}


def U(frag):
    """返回 processed.json 中的原样 URL（含 query），frag 用唯一子串匹配。"""
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
        'agent-sandbox/releases/tag/v1.0.9',
        'Agent Sandbox v1.0.9：router 原生 gRPC 代理、挂起/恢复延迟指标，修掉暖池抢占式重复建沙箱',
        'Kubernetes SIG 的 agent-sandbox 10 月 29 日发 v1.0.9。sandbox-router 现在原生代理 gRPC（含 sandboxd 的 ProcessService，unary 与 streaming 都走），8080 端口同时接受 h2c（cleartext HTTP/2），v1.0.7 起坏掉的 WebSocket 链路恢复。新增一组沙箱生命周期指标：agent_sandbox_suspend_total / resume_total 计数器与 suspend_latency_ms / resume_latency_ms 直方图，另有 finished_total、expired_total，全部按 namespace、sandbox_template、owned_by 打标——这是第一次能直接看「挂起恢复花了多久、失败在哪个结果」。控制器修了两个暖池竞态：SandboxClaim 领到暖沙箱后写状态撞 409 冲突被丢弃，没有任何事件再触发 reconcile，claim 卡在 Ready=False 直到 SDK 等待超时；以及从陈旧缓存 reconcile 的 claim 在主沙箱已分配后又冷建出第二个 Sandbox，两者一直保留到 claim 删除。Suspend 阶段不再从 Pod phase 推导 Finished=True（kubelet 会先把删掉的 Pod 标成 Failed/Succeeded），否则 ttlSecondsAfterFinished 设成 0 这类极小值的 claim 会被误过期，连 Sandbox 和 PVC 一起删。配置侧新增 agent-sandbox-config ConfigMap，控制器可从 19 个白名单参数里读调优项（命令行优先），适配 OLM 这类改不动 Deployment args 的安装方式。',
        [
            ('能做什么', '把「按会话起停沙箱」的生命周期做成可观测、可排障的资源：router 原生代理 gRPC 与 WebSocket，sandboxd 的 ProcessService 走同一条链路；新增 suspend/resume 成功数与延迟直方图，按 sandbox_template 与 owned_by 打标，能区分「挂起慢」「恢复失败」「TTL 过期」；暖池并发领取的两个状态竞态被修掉，claim 不再卡 Ready=False，也不会同时留两个 Sandbox。'),
            ('解决什么痛点', '自建多用户 agent 沙箱最痛的是空闲挂起与恢复：以前没有 suspend/resume 延迟指标，只能靠经验调 TTL；暖池在并发洪峰下会漏领、重复建、甚至因 409 丢状态写而卡死在未就绪。这次把「冷启动/挂起/恢复/过期」四段拆成可打点的计数器与直方图，等于给了调「多久挂起、什么时候回收」的实测依据，而不是猜。'),
            ('值不值得', '值得直接跑一遍：社区沙箱方案里它的 CRD 边界（Sandbox / SandboxTemplate / SandboxClaim / SandboxWarmPool）与「空闲挂起 + 暖池」正好覆盖按会话隔离的成本问题，v1.0.9 的指标可以直接拿来和 Daytona 的常驻沙箱做单位成本对比。限制是它仍是 v1.x 的 SIG 项目、默认 authz-mode=allow-all，router 的 NetworkPolicy 新增了到 TCP 9090 的 egress 且用 namespaceSelector: {} 覆盖所有命名空间——生产上先按 podSelector 收窄，否则任何能访问 router 的客户端可经 X-Sandbox-Pod-IP 打到任意 Pod 的 9090。'),
        ],
        tag='K8s×AI',
        note='🔎 新闻要点：版本 = v1.0.9（2026-10-29）；router = 原生 gRPC（unary + streaming，含 sandboxd ProcessService）、8080 支持 h2c、修复 v1.0.7 起的 WebSocket；新指标 = agent_sandbox_suspend_total / resume_total / suspend_latency_ms / resume_latency_ms / finished_total / expired_total，label = namespace + sandbox_template + owned_by；修复 = 暖池领取后 409 丢状态写致 claim 卡 Ready=False、陈旧缓存致重复冷建 Sandbox、Suspend 误报 Finished=True 致 TTL=0 的 claim 连 PVC 被删、volumeClaimTemplates 准入校验；配置 = agent-sandbox-config ConfigMap 19 个白名单参数（命令行优先，启动读一次）；安全 = NetworkPolicy 新增 TCP 9090 egress，namespaceSelector: {} 覆盖全部 Pod，默认 allow-all 下可打任意 Pod。',
    ),
    item(
        'gateway-api/releases/tag/v1.7.0',
        'Gateway API v1.7.0 正式版：HTTPRoute retry 进 Standard，预路由过滤器与 XTelemetryPolicy 进实验通道',
        'Gateway API 10 月 29 日发布 v1.7.0，是 v1.6.3 之后的第一个正式版。最重要的变化是 HTTPRoute retry（codes / attempts / backoff）从实验通道晋升 Standard，配套新增 HTTPRouteRetryCodes 与 HTTPRouteRetryConnectionError 两个一致性特性，旧的 HTTPRouteRetry、HTTPRouteRetryBackendTimeout 特性被删除——意味着实现方要通过一致性测试，必须真的支持按响应码重试，而不是自己发明字段。实验通道一次性加了六项：GatewayListenerFilters（listener 级、在路由决策之前执行的过滤器，官方用例是外部鉴权与 payload 处理，Gateway 与 ListenerSet 都能挂）、XTelemetryPolicy（基于 OpenTelemetry 语义约定的厂商中立属性字典，先覆盖分布式追踪，指标与访问日志暂未覆盖）、会话保持从 route 内联与 BackendTrafficPolicy 迁到 XBackend 资源、BackendTLSPolicy 可用 caCertificateRefs 引用 ClusterTrustBundle（不用再往每个 namespace 拷 CA 包）、按 Gateway 地址表达 routability（空 = 实现默认、Cluster、或域名前缀的实现自定义值）、以及 XBackend 的端口字段整理。破坏性变更都在实验 API：sessionName 拆成 cookie.name 与 header.name、cookieConfig 改名 cookie、XBackend 的 spec.port.port 改名 number 且引用 XBackend 时禁止再写 backendRef.port；Go 类型里 ForwardBodyConfig.MaxSize 从 uint16 改成 int32。',
        [
            ('能做什么', '把「重试」变成可移植的 API 契约：HTTPRoute 里直接写 codes / attempts / backoff，一致性测试强制实现方支持；预路由过滤器把外部鉴权、请求体处理前移到 listener 层，不必再靠实现私有 CRD；XTelemetryPolicy 用 OTel 语义约定统一追踪字段；BackendTLSPolicy 引用 ClusterTrustBundle 解决多 namespace CA 分发。'),
            ('解决什么痛点', '换网关实现时重试语义各家不同、字段不通用，是最常见的迁移成本；鉴权要么写进每个 HTTPRoute 的 filter 链，要么依赖厂商 CRD，导致「同一套 YAML 换不了实现」。v1.7.0 把这两块抬到标准/实验 API 层，配置的可移植性显著提升；ClusterTrustBundle 则直接消掉「每个 namespace 手工同步 CA」的运维动作。'),
            ('值不值得', '正在选网关或准备把 ingress 迁到 Gateway API 的话，这是该锁定的版本线：Standard 通道的 retry 有 conformance 兜底，实验项可按需开。门槛在实现侧——要先确认 Cilium / Envoy Gateway / Istio 各自实现对 v1.7.0 的支持矩阵，尤其是预路由过滤器与 XBackend 会话保持这类新实验 API，通常要等一个版本周期。另外若走 Cilium 的 Gateway API 实现，先升到 1.20.4：1.20.3 的 BackendTLSPolicy 处理有回归，会导致 CPU 飙高且无法转发流量。'),
        ],
        tag='K8s 核心',
        note='🔎 新闻要点：版本 = v1.7.0（2026-10-29，v1.6.3 之后首个正式版）；Standard 晋升 = HTTPRoute retry（codes / attempts / backoff）+ HTTPRouteRetryCodes / HTTPRouteRetryConnectionError 特性，删除 HTTPRouteRetry 与 HTTPRouteRetryBackendTimeout；实验新增 = GatewayListenerFilters（预路由过滤器）、XTelemetryPolicy（OTel 语义约定属性字典，仅追踪）、会话保持迁至 XBackend、BackendTLSPolicy 引用 ClusterTrustBundle、按 Gateway 地址的 routability；破坏性 = sessionName → cookie.name / header.name、cookieConfig → cookie、XBackend spec.port.port → number、ForwardBodyConfig.MaxSize uint16 → int32；其余 = HTTPRouteBackendRequestRedirect 特性被移除，cookie Path 默认改为 /。',
    ),
]

sections = []

# ---------------- AI 板块 ----------------
ai_cats = [
    {
        'label': '🧠 模型与研究',
        'en': 'Models & Research',
        'items': [
            item(
                'mistral.ai/news/mistral-large-4-oss',
                'Mistral 开源 1T 参数多模态权重 Le Chonk：FrontierCode 2.0 拿 19.7% 居首',
                'Mistral 把旗舰 Mistral Large 4（代号 Le Chonk）的权重开源：1 万亿参数、原生多模态，官方称其为最佳开源编码模型，且在 Cognition 的私有 FrontierCode 2.0 上以 19.7% 排第一（GLM-5.3 17.8%、Kimi K3 17.3%、DeepSeek V4.1 Flash 14.2%、Beam 1.0 2.9%），Terminal-Bench 也领先。相比三周前的公开预览，主要增量来自继续扩大的强化学习：编码与防御性网络安全两项提升最快，官方称「仍未看到饱和」。模型提供三档推理模式以平衡成本与性能，并在欧洲基础设施上从零训练，主打主权 AI 与可自托管。',
                [
                    ('能做什么', '一次给出 1T 参数的原生多模态权重（不是只开 API）：可自托管、可改、可继续训练；三档推理模式在同一权重上切换成本/能力档位；FrontierCode 2.0 的评测口径是「仓库维护者会不会合并 agent 的改动」，19.7% 已是当前开源最高。'),
                    ('解决什么痛点', '金融量化这类不能把代码与数据送云的场景，前沿能力长期只能通过闭源 API 获得；Le Chonk 把「接近前沿的编码/安全能力」变成可放进自有集群的权重，主权与合规不必二选一。'),
                    ('值不值得', '值得盯但别急着上线：1T 总量意味着即便按 MoE 稀疏推理，自托管也要多机 H 卡与高速互联，单机跑不动；更现实的用法是当教师模型做蒸馏、或做私有化微调的基座。判断依据是 FrontierCode 2.0 只领先第二名 0.4 个百分点，且为厂商在他人私有基准上的自报成绩，公开复现前不宜当作定论。'),
                ],
                tag='开源模型',
            ),
            item(
                'research.google/blog/the-sleep-framework',
                'Google 提出「睡眠」框架做持续学习：解锁 MoE 记忆块 + 自生成练习，单任务 48.9%',
                'Google Research 提出把持续学习拆成「清醒 / 睡眠」两态：清醒阶段正常处理输入、把新信息存进高频短时记忆；睡眠阶段停止接新输入，解锁预分配的 MoE 记忆块，用自生成的练习样本更新权重。记忆巩固由两步组成——用 MoE + Hope 架构把新解锁的低秩专家并入低频稳定记忆块，避免灾难性遗忘；再用广义知识蒸馏（GKD）加强化学习式模仿（LTI，按与教师前缀的语义与 Levenshtein 相似度给奖励）把短时记忆搬到长期参数里。随后「做梦」阶段做自我改进。论文报告在单任务 48.9%、持续预训练（CPT）46.2%，另三项基准为 79.2% / 69.0% / 46.1%，均高于 SFT、GRPO 与 on-policy 自蒸馏基线。',
                [
                    ('能做什么', '给已部署模型一条「不重训也能吸收新知识」的自动化后训练回路：训练期间按需扩 MoE 容量，把新知识放进新增专家而不动老参数；短时上下文记忆经蒸馏+RL 写入长期权重，形成闭环。全程限定在固定架构与人工定义的训练规则内。'),
                    ('解决什么痛点', '持续微调的两大坑是灾难性遗忘与「越训越窄」；把记忆分层（高频短时 / 低频长期）并按需扩容量，是绕开「要么忘旧、要么学不进新」的工程解法，也让模型更新不必每次都全量重训。'),
                    ('值不值得', '方向值得跟，但离落地还有距离：结论来自论文级评测（单任务与 CPT 两个设置），没有给出训练时长、显存增量与 MoE 扩张后的推理成本，也未验证长周期下容量膨胀的收敛性。对自建推理集群的人，真正的看点是「训练与推理共用同一份权重、睡眠期不接流量」这种调度形态——它要求集群能按阶段切分 GPU，属于 K8s 侧 batch/online 混部的问题。'),
                ],
                tag='论文',
            ),
        ],
    },
    {
        'label': '🧩 Agent & Skill',
        'en': 'Agents & Skills',
        'items': [
            item(
                'huggingface.co/papers/2610.22507',
                'RealCLI：把「人中途改需求」纳入评测，前沿 CLI agent 联合协作分最高只有 37.6%',
                'RealCLI 是一个配对基准，专门评「人和 agent 一起做长任务」：EXEC 模式一次给全规格，COLLAB 模式用脚本化用户在过程中逐步补信息、纠错、改约束、做授权决策，同一任务两种跑法形成对照。协作质量用五维框架展开成 22 个子维、51 个交互场景模板。结果显示能力断层明显：最好的配置在任务执行上平均只有 49.2%，切换到联合协作分 J_collab 后峰值仅 37.6%；作者指出任务完成度与协作质量严重脱耦，模型普遍栽在可引导性（steerability）、信任校准与安全边界管理上。',
                [
                    ('能做什么', '第一次把「执行结果」与「协作过程」分开打分：同一任务跑两遍（全规格 vs 渐进信息），差值就是「会不会跟人配合」；22 个子维覆盖纠错接受、约束变更、授权请求等具体交互。'),
                    ('解决什么痛点', '现有 CLI/agent 基准要么假设指令固定不变，要么只看终态对不对——而真实工作里需求天天在变，agent 的分数虚高。它把「能不能被中途纠正」变成可测指标。'),
                    ('值不值得', '值得拿它的维度表当自己 agent 产品的验收清单：49.2% 与 37.6% 的落差说明「能干活」和「能一起干活」是两种能力，做多用户 agent 平台时后者决定留存。限制是脚本化用户不等于真人，51 个模板覆盖不到长尾，且 37.6% 这类绝对值会随模型版本快速过期。'),
                ],
                tag='评测',
            ),
            item(
                'huggingface.co/papers/2610.37230',
                'TAO：把「工具还没返回」纳入调度，agent 服务延迟最多降 26.8%、TTFT 降 36.3%',
                'TAO 针对 agent 服务的真实形态：模型推理在集群 GPU 上、外部工具调用在分布式 CPU 上，两者交替。现有系统有两个盲点——评估服务时忽略「工具返回就绪度」，以及在 GPU 上做准入与放置时用启发式策略。TAO 的价值接口把近端工具就绪度、带时间衰减的节点级缓存信用、token 占用三者合成一个标量，再用动态规划在容量约束下联合选择与放置等待中的会话。在 12 组模型-负载-并发设置下，相对各自最佳 SOTA 基线，延迟最多降 26.8%、平均首 token 时间降 36.3%、decode 吞吐升 29.5%。',
                [
                    ('能做什么', '把 GPU 调度从「请求到了就排队」改成「等工具返回的会话先别占 GPU、但保留 KV 缓存信用」：用带衰减的缓存信用决定谁先上卡，动态规划一次性决定选谁、放哪。'),
                    ('解决什么痛点', 'agent 请求的 GPU 占用是碎片化的：一次工具调用可能几十毫秒也可能几十秒，期间 GPU 空转或反复换出 KV 缓存。忽略工具就绪度就会把 GPU 分给还要等很久的会话，TTFT 与吞吐同时受损。'),
                    ('值不值得', '对自建推理网关/多模型服务的人有直接参考价值：它的信号（工具就绪、缓存信用衰减、token 占用）都不依赖特定框架，可映射到 Kueue/llm-d 这类队列与路由层。限制是它是研究原型，评测在合成负载上，真实环境里「工具时长分布」极长尾，动态规划的求解开销也未给出。'),
                ],
                tag='论文',
            ),
            item(
                'github.com/CopilotKit/OpenBot',
                'OpenBot：给每个「AI 同事」配独立浏览器与登录态，动作先决策后留痕（8.1k star，MIT）',
                'CopilotKit 开源 OpenBot，8.1k star、MIT：定位是「公司能真正拥有的 AI 助手」，形态与 ChatGPT/Claude 类似，但跑在自己的基础设施上，通过 AG-UI 接任意 agent 栈。核心设计是每个同事拿到一台自己的「电脑」——真浏览器、独立的登录态、自己的文件，以及按需授予的工具；每个动作在执行前先被决策、执行后留记录，形成可审计的 before/after 轨迹。',
                [
                    ('能做什么', '把「多用户 agent」做成有身份、有隔离、有审计的实体：每用户一份浏览器 profile 与文件系统、工具按需授权、动作前后各留一条记录；agent 栈通过 AG-UI 协议接入，不锁死框架。'),
                    ('解决什么痛点', '多用户 agent 最难的不是推理，而是「谁的身份在操作、能操作什么、事后怎么追溯」。共享一份浏览器登录态会串号，纯提示词约束又不可验证——OpenBot 把身份与工具授权放到运行时层。'),
                    ('值不值得', '值得读它的隔离与审计模型：这与你手上「多用户 × 多会话沙箱」的问题是同一个（Daytona 常驻沙箱成本、会话隔离、越权审计）。限制是它偏产品化交付、单机部署形态，没给出多租户规模下的调度与回收数据；8.1k star 说明生态热度高，但生产成熟度要看它的 CI/安全徽章背后的测试覆盖。'),
                ],
                tag='开源',
            ),
            item(
                'github.com/MiniMax-AI/mcode-stack',
                'MiniMax 开源自己团队每天在用的 workflow 与 skill（MIT，413 star）',
                'MiniMax 把 MiniMax Code 团队内部的 workflow 与 skill 开源成 mcode-stack，MIT 许可。项目明确说这不是 prompt 合集、也不是「最佳实践清单」，而是团队每天真实在用的东西：如何让 AI 写的代码保持在高水位、如何组织评审与验证。skill 放在 stacks/ 目录下，仓库自带 validate CI 做结构校验，可直接安装到支持 markdown 规则文件的工具里。',
                [
                    ('能做什么', '给出一套「模型厂商自己怎么用 coding agent」的一手样本：workflow 定义流程阶段，skill 承载具体能力，validate CI 保证结构不腐化。'),
                    ('解决什么痛点', '市面上的 prompt/skill 合集大多是二手拼装、无人维护；由模型厂商的 coding 团队开源日常资产，可信度与针对性都更高，也更容易看出「哪些步骤值得固化成 skill」。'),
                    ('值不值得', '对在维护个人 skill marketplace 的人是可以直接对照的样本：看它如何切分 workflow 与 skill 的边界、如何用 CI 校验。限制是 413 star、规模小，且绑定 MiniMax Code 的工具体系，迁移要改路径与调用约定。'),
                ],
                tag='开源',
            ),
            item(
                'azure.microsoft.com/updates?id=578662',
                'Azure MCP Server 3.0 正式可用：备份、韧性、SRE Agent、Terraform 工具集一次补齐',
                'Azure MCP Server 3.0 转为正式可用，新增与扩充的工具集覆盖 Azure Backup（保管库、策略、恢复点、保护治理）、Resilience Management（恢复计划）、Azure SRE Agent、Terraform 与 Azure Advisor。Terraform 侧可以检索 AzureRM 与 AzAPI provider 文档、浏览 Azure Verified Modules（含 pattern 模块）、用 aztfexport 把既有资源导出为 IaC 并做校验。该版本同时带了新的安全默认值与破坏性变更。',
                [
                    ('能做什么', '把「查文档 / 看恢复点 / 导出现有资源为 Terraform / 问 SRE Agent」这些云运维动作暴露成 MCP 工具，agent 不必再靠截图或自写脚本操作门户。'),
                    ('解决什么痛点', 'agent 做云运维时最缺的不是推理而是「有权限、有语义的工具」：直接给 shell 等于给全权限，写私有封装又重复劳动。标准 MCP 工具集把权限粒度收在工具这一层。'),
                    ('值不值得', '如果你在给内部 agent 平台定「工具即权限」的边界，这是一个现成的参照实现（尤其 aztfexport 那类只读+生成的工具很适合放进沙箱）。限制是绑定 Azure；3.0 有破坏性变更与新的安全默认值，升级前要过一遍 release notes。'),
                ],
                tag='MCP',
            ),
        ],
    },
    {
        'label': '🛠️ AI 工程落地',
        'en': 'AI in Production',
        'items': [
            item(
                'infoq.cn/article/tsyyFmCmzphHw4gWy7Fo',
                '生产级 AI 的两类「全绿故障」：语义漂移与嵌入漂移，监控面板看不出问题',
                'InfoQ 一场圆桌把 agent 上生产的失效模式摊开讲。ThoughtWorks 的 Xiong 举了文本转 SQL 的语义漂移：agent 把销售域和客服域的「会员」当成同一个概念，下游报表悄悄出错，而链路追踪全绿。金融 AI 从业者 Lan Chu 给了更狠的例子——用向量相似度阈值拦截违规投资建议的合规 agent，底层嵌入模型一次后台更新改变了向量距离分布，线上误报与漏报同时飙升，所有基础设施健康检查仍然正常。会上还提到 RAG 会意外检索到敏感文档、模型记忆训练数据可被用于去匿名化、以及 GitSpawn 这类恶意仓库配置在常规命令执行时触发未授权代码。给出的做法：CI 里自动化风格/语法检查，人工评审只留架构与业务意图；把评估当持续运转的基础设施（span 级在线追踪 + LLM 分类故障模式）；给每个 agent 独立非人类身份、分级访问（只读 vs 可回滚写）、MCP 依赖版本化、API 密钥隔离在沙箱外。',
                [
                    ('能做什么', '给出两类「监控看不见」的故障机理与对应动作：语义漂移（领域词义映射错，trace 正常但指标错）靠语义层约束与对照校验；嵌入漂移（模型版本更新改变向量分布）靠固定嵌入版本 + 分布漂移监控，而不是只盯健康检查。'),
                    ('解决什么痛点', '传统 SRE 的信号（延迟、错误率、CPU）对「结果错但系统正常」完全失明；agent 生成代码的速度又超过人工逐行评审的上限，评审流程本身成为瓶颈。'),
                    ('值不值得', '最实用的是「评估即基础设施」和「非人类身份 + 分级写权限」两条：前者对应对 agent 质量做持续回归，后者正好接住多用户 agent 平台的越权问题。限制是圆桌形式、无量化数据，具体阈值（漂移告警线、变异测试覆盖率）仍需自己定。'),
                ],
                tag='工程实践',
            ),
            item(
                'cloud.google.com/blog/products/data-analytics/expanded-semantic-model-support-in-knowledge-catalog',
                'Google 把 agent 的查询接回治理过的语义层：错不在模型，在裸表',
                'Google Cloud 在 Knowledge Catalog 扩展语义模型支持，主打「一个上下文图把 agent 接到你已经信任的语义模型上」。文章用一个典型场景开场：销售 VP 问上季度头部企业客户净收入，agent 几秒给出漂亮图表，但数字和财务报告对不上——因为把已取消订单算成收入、还从没验证过的 staging 表取数。结论是 agent 不是「理解错了」，而是缺一层被治理的语义定义。',
                [
                    ('能做什么', '让 agent 走语义层而不是裸表：指标定义、维度、口径集中在一处，agent 生成的查询被语义层解析，越权表与未验证数据集直接不可达。'),
                    ('解决什么痛点', '自然语言转 SQL 的失败多发生在口径与血缘上，不在语法；每个团队各自复述一份指标定义，agent 越多错得越一致。'),
                    ('值不值得', '做金融量化数据平台时这条最值得抄：先把指标与口径做成机器可读的语义层，再让 agent 接入，比事后给 agent 加提示词约束有效得多。限制是绑定 GCP 的 Knowledge Catalog，开源替代（dbt semantic layer / Cube）需要自己补治理与权限。'),
                ],
                tag='数据平台',
            ),
        ],
    },
    {
        'label': '📊 产品与商业',
        'en': 'Products & Business',
        'items': [
            item(
                'openai.com/index/retell-ai',
                'Retell 用 GPT-6 Astra 撑 100M 月通话，Codex 把它的人均年收入推到 160 万美元',
                'OpenAI 的客户案例：语音 agent 公司 Retell 用 GPT-6 Astra 跑每月 1 亿通电话，该模型在它自己的语音 agent 基准上排第一；同时用 Codex 做研发提效，把人均年收入推到 160 万美元的水平。案例的核心是「同一个供应商同时供模型与编码 agent」带来的复用。',
                [
                    ('能做什么', '给出一个规模化语音 agent 的实测口径：1 亿通/月的通话量、模型在其自有基准上的排名、以及编码 agent 对人均产出的影响（160 万美元 ARR/人）。'),
                    ('解决什么痛点', '语音 agent 的成本结构里延迟与打断处理最关键，选型要看自家基准而非通用榜单；研发侧则要回答「coding agent 到底有没有变成财务指标」。'),
                    ('值不值得', '数字来自厂商案例、口径未公开，只能当方向参考：人均 160 万美元 ARR 是极小的团队基数下的结果，不能外推。真正的信息是「模型 + 编码 agent 同源」正在成为中小 AI 公司的默认组合。'),
                ],
                tag='案例',
            ),
            item(
                'simonwillison.net/2026/Oct/29/api-credits',
                'OpenAI 跟进 Anthropic：订阅档送等额 API credits',
                'Simon Willison 记录：Anthropic 本月初给 Max/Team 订阅加了新权益——每月 $100/$200/$500 的档位分别送等额（有期限）API credits；OpenAI 现在推出了几乎完全一样的方案，同样是 $100/$200/$500 档位送等额 credits，可应用到一个 API 组织上。',
                [
                    ('能做什么', '订阅费可以直接折成 API 额度：同一笔钱既买席位也买 token，对以「订阅 + 少量 API」为主的个人与小团队更划算。'),
                    ('解决什么痛点', '过去订阅与 API 是两套计费，试做原型要额外充 API；credits 有期限，等于把「先付费后使用」变成「当期必须用掉」。'),
                    ('值不值得', '如果同时用订阅与 API，值得对一下额度是否够覆盖当月实际调用；限制是 credits 会过期、且只能绑一个 API 组织，团队多组织场景反而麻烦。'),
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
                'infoq.cn/article/EQTckj5GQQymiQES22Bo',
                'Anthropic 工程经理取消编程面试：与真实能力的相关性已降到「考手写汇编」',
                'Anthropic 工程经理、Electron 联合维护者 Felix Rieseberg 公开表示已把编程面试从招聘流程移除：「至少在我负责的团队里，编程面试已经死了，它不再提供有效的判断信号。」他的类比是，用 React 小题测候选人，越来越接近考察工程师能否熟练手写汇编——Claude 在这类任务上已经足够强，而团队里最有影响力的工程师未必是代码测试分数最高的人。文章后半段是他对「AI 抹平资历差距」的判断：Hunger beats tenure，进入行业不久的工程师可以借 AI 快速超过基础更好、年限更长的同行，因为新人还没接受组织内部「什么事做不了」的默认判断。',
                [
                    ('能做什么', '给出一条可检验的招聘判断：编码题测的是「模型已能代劳的执行能力」，应当换成对问题定义、判断力与推动力的评估；文中用 Notion 离线模式与办公室电视两个亲身案例说明「组织惯性伪装成技术限制」。'),
                    ('解决什么痛点', '当 AI 能完成大部分编码题，面试信号与岗位产出的相关性失效，继续用旧题会筛掉真正能推动事情的人。'),
                    ('值不值得', '做技术管理或带团队的人值得读：它给的是「怎么识别组织里被当成共识的假限制」，这比招聘本身更有复用价值。限制是单人经验、单一公司，且没有给出替代评估方案的具体设计——取消之后用什么筛人，文中没有答案。'),
                ],
                tag='行业观点',
            ),
            item(
                'simonwillison.net/2026/Oct/28/vibe-game-development',
                'Willison：2026 年 10 月是 vibe coding 游戏的拐点',
                'Simon Willison 认为又一个拐点到了：2025 年 11 月是编码 agent 的拐点（Opus 4.5 与 GPT-5.1 让 coding agent 成为工程师的日常工具），而 2026 年 10 月是「vibe coding 游戏」的拐点。他点名了一批能直接玩的作品——Tree、Appreciator、Emberwick、Battle Drones、Pumpkin Farmer、Quarter Sun Cove 等，判断依据是这些游戏已经不只是 demo，而是有完整玩法循环、能被普通玩家玩下去的东西。',
                [
                    ('能做什么', '给出一个可验证的观察方法：不看榜单看「能不能玩下去」，用一批具体作品与玩法循环作为拐点证据。'),
                    ('解决什么痛点', '「AI 能写代码」和「AI 能做出完整产品」之间的差距，通常卡在美术、音效、玩法调优这些非代码环节；这批作品说明闭环正在被打通。'),
                    ('值不值得', '值得当行业节奏参考：它提示 coding agent 的下一步增量在「多模态资产生成 + 长周期一致性」，而不是更快的补全。限制是样本是个人策展、标准主观，且作品质量参差。'),
                ],
                tag='观点',
            ),
        ],
    },
    {
        'label': '🛡️ 安全与治理',
        'en': 'Security & Governance',
        'items': [
            item(
                'cloud.google.com/blog/products/data-analytics/bridge-gemini-enterprise-and-snowflake-with-google-adk',
                'Gemini Enterprise 接 Snowflake 的安全桥：MCP + ADK，凭据不进 agent',
                'Google Cloud 给出把 Gemini Enterprise 接到 Snowflake 数据的参考架构：用 Model Context Protocol 暴露 Snowflake 能力，用 Agent Development Kit（ADK）编排 agent，让 agent 把自然语言问题转成对数据仓库的受控查询，同时保持数据治理与访问控制。重点是凭据与网络边界不进 agent 运行时。',
                [
                    ('能做什么', '把「agent 查数仓」拆成三段：MCP server 持有凭据并做查询代理、ADK 负责编排与工具选择、Gemini Enterprise 只管对话；权限收敛在 MCP 这一层。'),
                    ('解决什么痛点', '企业不愿把数仓凭据交给 agent，也不愿开公网入口；把凭据放进 MCP server 的运行时、agent 只见工具名与参数，是最小暴露面的做法。'),
                    ('值不值得', '和你「出口做联网搜索 + 审计/DLP」的思路同构：把外联与凭据集中在受控代理层，agent 本身不持有任何长期凭据。限制是文章是参考架构、无性能与合规认证细节，Snowflake 侧仍需自行验证私有连接。'),
                ],
                tag='安全架构',
            ),
        ],
    },
]
sections.append({'label': '🤖 AI 板块', 'categories': ai_cats})

# ---------------- 基础设施板块 ----------------
infra_cats = [
    {
        'label': '🤖☸️ K8s × AI',
        'en': 'K8s × AI',
        'items': [
            item(
                'kubernetes.io/blog/2026/10/29/sig-arch-ai-conformance-2026',
                'AI Conformance 从临时 WG 转为 SIG Architecture 常设子项目，认证平台 18 → 31 家',
                'Kubernetes 官方博客的 SIG Architecture 专访：AI Conformance 从一次性的 Working Group 转为 SIG Architecture 下的常设子项目，理由是 WG 的目标（发布初版要求、跑通认证流程）已完成，而 AI 需要长期治理。认证平台数量在两次 KubeCon 之间从 18 家增至 31 家。要求被刻意限制在基础设施层：加速器通过 DRA 暴露、高性能网络、workload-aware 编排、低延迟推理，不绑定具体 AI 框架或模型服务器；需求用 KAR 模板提，自动化 Go 测试套件放在 kubernetes-sigs/ai-conformance 的 test/ 目录。',
                [
                    ('能做什么', '给出一份厂商中立的「AI 就绪 K8s」验收面：DRA 加速器、高性能网络、workload-aware 调度、低延迟推理四项，外加可执行的 Go 一致性测试与 KAR 需求模板。'),
                    ('解决什么痛点', '各家 AI 平台的差异藏在调度器、设备插件与网络栈里，用户迁移时才发现踩空；把要求抬到 SIG Architecture 并配一致性测试，等于把「能不能跑 AI 负载」变成可验证的清单。'),
                    ('值不值得', '自建集群时可以直接拿它当验收清单，尤其是 DRA 与 workload-aware 编排这两项——正好对应你在选的调度与 GPU 方案。限制是它不覆盖推理框架与模型服务层，认证偏「平台供应商」视角，自建集群只能借用要求条目而非认证。'),
                ],
                tag='K8s×AI',
            ),
            item(
                'kueue/releases/tag/v0.20.4',
                'Kueue v0.20.4：DRA 按陈旧 ResourceSlice 误算设备额度，弹性 Job 就绪判定修复',
                'Kueue 10 月 29 日发 v0.20.4（v0.19.11 同步）。DRA 侧修了两处会直接卡住 GPU 申请的问题：CEL 设备可用性检查会把陈旧或不完整 ResourceSlice 池里的设备算作可用，Workload 因此为 DRA 分配器根本用不了的设备占住额度；设备请求来自 LimitRange 默认值的 Workload，在匹配的 DeviceClass 建好之后仍停在 Pending。ElasticJobsViaWorkloadSlices 下修了 WaitForPodsReady 把已准入的弹性 Job 误判为未就绪（改为按最新准入 slice 的授予副本数判定），以及 PodsReadyTimeout 在扩容 slice 等额度期间误驱逐已就绪的 Workload。',
                [
                    ('能做什么', '让 DRA 的额度核算与真实可分配设备对齐，并让弹性 Job 的就绪/超时判定按「已准入的副本数」而不是 Pod 实际状态来算。'),
                    ('解决什么痛点', 'GPU 池里最贵的浪费是「额度被占但卡分不出去」：陈旧 ResourceSlice 让队列以为设备可用，实际分配器拿不到；弹性训练任务则容易在扩容窗口被超时误杀。'),
                    ('值不值得', '如果你打算用 DRA + Kueue 管 GPU 配额，这是必须跟的补丁版本；升级前注意 v0.20.4 改了调度器日志的 verbosity（Workload 级消息默认降到 level 2，开 LogLevelForSchedulerMainLoop 才升到 3），依赖日志的告警要一起调。'),
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
                'kubernetes/releases/tag/v1.37.2',
                'Kubernetes 四条支持线同日发补丁：1.37.2 / 1.36.6 / 1.35.10 / 1.34.13',
                '10 月 28 日 Kubernetes 同时为四条受支持分支发补丁版本：1.37.2、1.36.6、1.35.10、1.34.13，另有 1.38 开发线的 alpha.3。例行安全与回归修复节奏，选哪条线取决于集群当前 minor 与支持的 skew 窗口。',
                [
                    ('能做什么', '给在跑的每个 minor 一条最新补丁线，覆盖安全修复与回归。'),
                    ('解决什么痛点', '补丁窗口内不升级会累积 CVE；跨太多补丁版本升级又容易踩到行为变更。'),
                    ('值不值得', '按 skew 策略滚动升级即可，没有需要特别评估的新特性；真正要看的是各版本 release notes 里的 action required 项。'),
                ],
                tag='版本',
            ),
        ],
    },
    {
        'label': '🌐 云原生周边',
        'en': 'Cloud Native',
        'items': [
            item(
                'cilium/cilium/releases/tag/1.20.4',
                'Cilium 1.20.4 修 1.20.3 的 Gateway API 回归：BackendTLSPolicy 致 CPU 飙高、无法转发',
                'Cilium 10 月 23 日发布 1.20.4（1.19.10、1.18.16 同步补丁）。CHANGELOG 里最重要的一条是修 1.20.3 引入的回归：Gateway API 实现错误处理 BackendTLSPolicy 配置，导致 Cilium CPU 占用飙升并且无法转发流量——用 Cilium 做 Gateway API 实现的集群，1.20.3 属于不该停留的版本。其余修复包括 NAT46x64 网关前缀转换 panic、6.12 以下内核 IPv6 ClusterIP 反向 NAT 对 CHECKSUM_PARTIAL 包的 L4 校验和错误、CiliumEnvoyConfig 会重定向其他 namespace 的 Service（CiliumClusterwideEnvoyConfig 无 namespace 的引用恢复默认 default）、以及通过提高 Standalone DNS Proxy 策略快照下发频率来减少 Pod 启动瞬间的 SERVFAIL/REFUSED。',
                [
                    ('能做什么', '把 1.20.3 的 Gateway API 转发故障与一批数据面校验和/panic 问题修掉，同时收窄 CiliumEnvoyConfig 的跨 namespace 重定向行为。'),
                    ('解决什么痛点', 'BackendTLSPolicy 在 1.20.3 上会同时表现为「CPU 高」与「流量不通」，很容易被误判为业务问题；跨 namespace 的 Envoy 配置误重定向则属于静默的行为偏差。'),
                    ('值不值得', '用 Cilium 做 CNI 或 Gateway API 实现的集群应当排期升到 1.20.4；如果已在 1.20.3 且配了 BackendTLSPolicy，建议先回滚该策略或直接升级。限制是这类补丁版本不带新特性，升级风险主要在 eBPF 数据面重启窗口。'),
                ],
                tag='CNI',
            ),
        ],
    },
    {
        'label': '🏛️ 社区与项目',
        'en': 'Community',
        'items': [
            item(
                'cncf.io/blog/2026/10/29/the-boundary-problem',
                'CNCF：agent 的权限边界不是被决定的，是累积出来的',
                'CNCF Ambassador William Rizzo 与 Francesco Beltramini 的文章指出一个反复出现的形状：agent 实际能做的事，几乎从来不是谁刻意决定的，而是累积出来的——为一个流程加的工具对所有权流程都可见，为 demo 配的凭据活到了生产，周五为解锁部署加的委派变成图上的永久边。没有人「决定」给 agent 那么大的触达范围，因为触达范围从未被决定过。作者认为把它当治理问题、用评审委员会解决是瞄准了错误的层：流程管的是人做出的决定，而问题恰恰出在没人做出的决定。用提示词让 agent 自知边界在结构上无效——agent 的输出是条件于上下文的下一个动作的概率分布，99 次守住第 100 次放手不叫边界。真正有效的是在 substrate 层强制：工具绑定与凭据才是真实权限。',
                [
                    ('能做什么', '给出一个可操作的诊断角度：不看 agent 的指令写了什么，而是枚举它实际持有的工具绑定与凭据，以及这些授权是何时、由谁、以什么理由加进来的。'),
                    ('解决什么痛点', '权限漂移是静默的：每一次授权都合理，合起来就越界。等到有人问「它怎么能做这个」，答案通常是「它已经能做几周了」。'),
                    ('值不值得', '对做多用户 agent 平台的人是核心设计输入：边界必须落在运行时（工具与凭据），不能落在提示词。限制是文章停在论点与方向，没有给出具体实现（如能力清单、授权图审计）的工程方案。'),
                ],
                tag='平台治理',
            ),
        ],
    },
]
sections.append({'label': '☸️ 基础设施板块', 'categories': infra_cats})

flash = [
    {'title': 'SGLang v0.5.23 发布', 'url': U('sglang/releases/tag/v0.5.23')},
    {'title': 'OpenAI 更新 Model Spec：以五条核心价值观约束更强模型', 'url': U('openai.com/index/updated-model-spec')},
    {'title': 'Claude-Code-Game-Studios：49 个 agent + 72 个 skill 拼成「游戏工作室」（29k star）', 'url': U('github.com/Donchitos/Claude-Code-Game-Studios')},
    {'title': 'OpenAI 与 ServiceNow 扩大合作，覆盖企业工作流', 'url': U('openai.com/index/openai-servicenow-partnership-expansion')},
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
    'date_label': '2026 年 10 月 30 日 · 星期五',
    'issue': 40,
    'kicker': 'DAILY',
    'hint': '👆 点击任意条目<b>摘要区域</b>，展开「值不值得深入」的判断；再次点击收回',
    'lead': '今天两条线都落在「把边界做进 API」上。基础设施侧，Kubernetes SIG 的 Agent Sandbox 发 v1.0.9：router 原生代理 gRPC，首次给出 suspend/resume 延迟直方图，并修掉暖池并发下的重复建沙箱与状态丢失——按会话起停沙箱缺的正是这层可观测性；同一天 Gateway API v1.7.0 正式版把 HTTPRoute retry 抬进 Standard 通道，预路由过滤器与 XTelemetryPolicy 进实验通道，换网关实现时「同一套 YAML」终于有了 conformance 兜底。模型侧 Mistral 把 1T 参数原生多模态的权重开源，FrontierCode 2.0 拿到 19.7%；Google 用「睡眠」阶段的 MoE 扩容量做持续学习。工程上最有料的是 InfoQ 那场圆桌：语义漂移与嵌入漂移这两类故障，监控面板全绿、结果全错。CNCF 那篇则把话说透——agent 的权限边界不是被决定的，是累积出来的。',
    'highlights': highlights,
    'sections': sections,
    'flash': flash,
    'footer': '由 Hermes 自动汇编 · 每日 09:00 更新',
}

# 断言：所有 URL 均来自 processed.json，标题非空
for it in [x for s in sections for c in s['categories'] for x in c['items']] + highlights:
    assert it['url'] in by_url, it['url']
    assert it['title'] and it['summary'] and len(it['detail']) == 3
for f in flash:
    assert f['url'] in by_url, f['url']

json.dump(brief, open('briefing.json', 'w'), ensure_ascii=False, indent=1)
n = sum(len(c['items']) for s in sections for c in s['categories']) + len(highlights)
print('items:', n, 'flash:', len(flash))
