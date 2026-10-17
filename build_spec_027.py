#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 027 from the locked card template + briefing.json."""
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
 "🧩 **Agent & Skill** — LEASH 用弱模型隐状态的不确定性决定何时升级到强模型（OSWorld 上比随机升级高 6.55–11.94 分）；MAI-Gym 把 GUI agent 的评测/采集/在线 RL 训练合成一个平台，9B 模型在 OSWorld-Verified 拿 76.2%、mocked 应用训练可迁移真机（28.8%→48.1%）；Pi 1.0 把 MCP 装进核心并推出长时 Harness「Pi Durable」。",
 "🧠 **模型与研究** — 四个 Gemini 4 Argon agent 在《我的世界》写 2783 个程序、27 小时打败末影龙（死亡 605 次）；苹果用 4 台 Mac Studio 跑 816B 的 Muse Spark Open，解码 36+ tokens/s；OpenGCUA 开源 computer-use 全栈，OSWorld-v2 平均分 +19.6、步数 −53%。",
 "🛠️ **AI 工程落地** — 远程 KV cache 分层实测反直觉：命中比重算还慢（16k p99 3.96s→17.3s），改造后从 83.32s 降到 0.67s；大型零售库存平台把 LLM 当平台基础设施治理，幻觉率 15%→1.5%；手淘 TEKO 量化出 AI 生成用例综合可执行率仅 6.4%，自主性 = 判据 × 信号。",
 "📊 **产品与商业** — 库克称苹果智能接入阿里千问、10 月底在中国发测试版（首批含实时翻译/书写工具，不含 Siri AI）；量子位智库发布 Agent 落地报告，拆解企业智能化六大断点。",
 "💡 **观点与好文** — Claude Code 团队：Claude 写自己约 90% 的代码，6→9 月合并 PR 翻倍而回滚占比降 40%+；Linus 用 Claude Code 的内核补丁把读取吞吐提升 23 倍，bug 却由人类审查者揪出。",
 "🛡️ **安全与治理** — 弱到强验证器加固：用 hacker-fixer 循环自动找验证器漏洞并修复，早期版本已被 Terminal Bench 官方仓库采用；Google Cloud 把 agent 定义为新的非人类身份（NHI），配套 secure-by-default 边界。",
 "🤖☸️ **K8s × AI** — Nirmata Runtime for Kyverno 把策略执行从准入控制下沉到内核（BPF-LSM + eBPF），专治 agent 的运行时行为；Reflection 的 Beam 在 GKE 上获 Day 0 支持，llm-d + NVIDIA Dynamo 带来 5 倍性能。",
 "☸️ **K8s 核心技术** — Istio 1.31.2 修四枚 CVE（含 AuthorizationPolicy over HTTP/2 方法大小写绕过 CVSS 7.4）；containerd 2.3.7 修 1 个 CVE + 3 个 GHSA 并做四项硬化；GKE 内置 Wiz Runtime Sensor（预览）。",
 "📦 **社区与项目** — CNCF 讲 n8n on EKS 从单容器+SQLite 到 workers/PostgreSQL/Redis 的生产化与迁移；Nepal 首位、最年轻 Golden Kubestronaut 的认证经历。",
 "☁️ **公有云动态** — Azure Databricks 私有网络网关进入公共预览，serverless 计算可经单一托管网关接入 VNet 与其传递可达网络。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年10月17日 · 星期六",
 "{issue}": "027",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-17.html",
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
