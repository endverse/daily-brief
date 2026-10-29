#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 039 from the locked card template + briefing.json."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json")
b = json.load(open(os.path.join(BASE, "briefing.json"), encoding="utf-8"))

spec = json.load(open(TPL, encoding="utf-8"))

hl = []
for i, h in enumerate(b["highlights"], 1):
    hl.append(f'**{i}. {h["title"]}**\n{h["summary"]}')
highlights = "\n\n".join(hl)

glance_lines = [
    "🧠 **模型与研究** — Gemini 4 Carbon 以 AA 智能指数 59 分登顶，主打安全基准（SEC-bench Pro 88.2% / ExploitGym 54.8% / CWE-bench 71.0%），$2/$10 定价、先给网络防御方；GPT-6.1 Terra 把 $1/$5 档的 Terminal-Bench 4.0 从 21.5% 拉到 50.3%、低强度错误率 53.6%→16.7%；蚂蚁开源 Ling-3.1-flash-1019，base 560B/激活 25B、MIT 许可，AA 指数 44 分。",
    "🧩 **Agent & Skill** — Snowflake 给出「雇智能体」落地框架：170 题五轮测试才准上线、搭一个 20 分钟但被采用要 8-9 个月、设计者/控制者/审计者三角色；AWS 开源 2B 决策模型 Strands Decider（3090 上 115ms、JevBench 72.3%）与内核级策略沙箱 Strands Box；Google 把 skill 当产品发版，21k star / 170+ skill，每次改动必须带评估证据；Antigravity SDK 支持本地模型，3400 个 token 只有 95 个上云。",
    "🛠️ **AI 工程落地** — Instagram 把 Android UI 整屏迁到 Compose 改造成 AI 原生代码库：UI 代码 -50%、每 agent 会话 token -33%、执行时间 -35%、交互轮次 -32%；扩散模型 Clover-35B-A3B 开源，680 tokens/s、SWE-bench Verified 73.6、Terminal-Bench 2.1 51.7，无人机空管 demo 7.32 秒对 62.3 秒。",
    "📊 **产品与商业** — 价格战进入买量阶段：Replit 1 亿美元合同拿 30%+ 折扣，Rippling 编程负载的 OpenAI 占比 16%→52%、Anthropic 57%→18%，DataCamp 成本降 80-90%，单款模型降幅最高 80%。",
    "💡 **观点与好文** — GitHub Octoverse 2026：合并 PR 不到一年翻三倍到 2.2 亿/月、commit 73.8 亿/月、新仓库 3030 万/月，agentic engineering 对平台产出最直白的一张图。",
    "🛡️ **安全与治理** — Snowflake 用「agent 身份 + 只减不增的会话权限上限 + 按 agent 活跃状态生效的掩码策略」控住越权；HoS 论文给注意力头装可学习门控做指令-数据分离，黑盒 RL-Hammer 的 ASR 从 97%/85% 压到 10%。",
    "🤖☸️ **K8s × AI** — Volcano v1.16 引入 NamespaceQueue 与 fairshare，租户可在自己 namespace 内建层级队列、按历史用量做公平分享；另加 Unschedulable Job Cache（默认关闭）、DRA scoring 与 K8s 1.36 支持。",
    "☸️ **K8s 核心技术** — K8s 同日发 1.38.0-alpha.3 与 1.37.2 / 1.36.6 / 1.35.10 / 1.34.13 四条补丁线；Calico v3.32.3 修掉 eBPF 策略程序被内核 verifier 判 unreachable insn 致节点 NotReady、IPv6 conntrack NAT 不过期、ArgoCD 永久 out-of-sync 等三十余项。",
    "🌐 **云原生周边** — AlloyDB Omni 的只读 Web UI 在 RHEL 与容器上 GA，可看硬件遥测、查询性能与配置 flag；Istio 1.32.0-rc.0 与 Envoy 1.40.2 同日推进。",
    "🏛️ **社区与项目** — Golden Kubestronaut 超过 570 人，认证从「考过整套证」转向按领域深度与持续贡献分层。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月29日 · 星期四",
    "{issue}": "039",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-29.html",
}

# chat_id: the 飞书『AI 早报』群 (template carries a stale private chat id)
spec["chat_id"] = "oc_18845bcfeabb63caffa3e86c69a96d6e"


def fill(o):
    if isinstance(o, str):
        for k, v in repl.items():
            o = o.replace(k, v)
        return o
    if isinstance(o, dict):
        return {k: fill(v) for k, v in o.items()}
    if isinstance(o, list):
        return [fill(x) for x in o]
    return o


spec = fill(spec)

blob = json.dumps({k: v for k, v in spec.items() if k != "_comment"}, ensure_ascii=False)
for k in repl:
    assert k not in blob, "unfilled placeholder: " + k
assert spec["chat_id"] == "oc_18845bcfeabb63caffa3e86c69a96d6e"
assert spec["header"]["template"] == "indigo" and spec["header"]["icon"] == "myai_colorful"

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w"), ensure_ascii=False, indent=1)
print("spec.json ok · chat_id ok · 无残留占位符")
