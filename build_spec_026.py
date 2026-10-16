#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 026 from the locked card template + briefing.json."""
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
 "🧩 **Agent & Skill** — Cortex 把 agent 的 skill/rule 当假设来测（18 项留下 16 条 rule，通过率 +55 分）；APUS AI 开源 Reflex Agent，用决策模型而非提示词管 Harness；K-Dense 放出 177 个科研 skill；阶跃星辰开源 600B/27B 激活的 Step 5 Preview（1M 上下文）。",
 "🧠 **模型与研究** — 蚂蚁百灵开源 Ling-3.1-flash（560B 总参 / 25B 激活 / 1M 上下文）；Mistral 首发时序基础模型 Timestral（209M 参数、CPU 可跑）；OpenAI 案例里 Third Moment 同时跑 10000 个 agent、单次研究 36–48 小时。",
 "🛠️ **AI 工程落地** — Amp 用 GPT-6 Astra + Ultrafast + GPT-Live-1 把 agent 推出编码之外；SentinelOne 用 Daybreak 把恶意软件分析从「周」压到「小时」；Latent Compaction 用测试时训练压 KV cache。",
 "📊 **产品与商业** — Anthropic 向投资人披露季度收入 48 亿 → 115 亿 → 168 亿美元、Q3 环比近 +50%，每 1 美元算力换 1.70 美元收入；西蒙斯基金会投 1500 万美元帮数学家适应 AI。",
 "💡 **观点与好文** — Geoffrey Huntley 用 pre-commit hook 拦住绕过观测库的提交并注入纠正提示，替代会漂移的 AGENTS.md；Simon Willison 用 Claude 手机聊天模式生成 three.js 小游戏。",
 "🛡️ **安全与治理** — Archestra 开源 OpenAPPA：确定性规则在 agent 循环外挡住数据外泄，攻击成功率 0（对照 Claude Auto-Mode 10%、FIDES 31%）；微软一轮致谢 23 个漏洞，署名「Yuki Chen using GLM from z.ai」，含 CVSS 9.8。",
 "🤖☸️ **K8s × AI** — CNCF 主张不给 agent root、让它提出下一个系统状态（不可变镜像宿主 + 短生命周期会话）；商汤大装置支撑上海量子城市首批政务智能体，调度效率提升 80%；Temporal worker 改用 Cloud Run 按需预扩。",
 "☸️ **K8s 核心技术** — Cilium 同日发 1.20.3/1.19.9/1.18.15：修 conntrack 回收误删导致 NAT 映射丢失与 SNAT 端口重分配、CNP 带 nodeSelector 静默不生效；Kueue v0.20.2 修 DRA 配额计费与 FairSharing 误抢占。",
 "🧩 **云原生周边** — 软件碳强度 (SCI) 想进 OpenTelemetry 语义约定，把碳排放做成一等信号；Istio 1.31 支持 agentgateway（Rust + MCP）作七层 waypoint，同时停止 Google Cloud 镜像与 Helm 分发，要求 12 月前迁移。",
 "☁️ **公有云动态** — Azure Files 支持跨区域复制与同步（Storage Mover，预览）；Amazon S3 含 S3 Tables 与 S3 Vectors 原生上架 Vercel Marketplace；BigQuery 生成式 AI 函数上线 token 级成本管理（GA）。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年10月16日 · 星期五",
 "{issue}": "026",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-16.html",
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

# no placeholders may survive (except the _comment documentation line)
blob = json.dumps({k: v for k, v in spec.items() if k != "_comment"}, ensure_ascii=False)
for k in repl:
    assert k not in blob, f"unfilled placeholder {k}"
assert spec["chat_id"] == "oc_18845bcfeabb63caffa3e86c69a96d6e"

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written |", spec["header"]["subtitle"], "|", spec["button"]["url"])
print("count_line:", count_line)
