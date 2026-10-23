#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 033 from the locked card template + briefing.json."""
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
    "🧩 **Agent & Skill** — claude-howto 冲上 GitHub Trending 首位：43,194 星的 Claude Code 教程库，把 slash 命令、hooks、记忆、subagent、skills、MCP 串成有依赖顺序的学习路径。",
    "🛠️ **AI 工程落地** — GitHub 用 AI 把 Copilot 运行时从 TS 重写成 Rust，80 万行、14.5 周，启动交互 5.25s→292ms；Qwen 的 FlashQLA 用 chunk 矩阵乘 + 序列并行解掉 GDN 线性注意力的并行度瓶颈。",
    "🧠 **模型与研究** — Quant-Arena 用 A 股真实数据考端到端量化研究：9 个前沿模型没一个在封存的 2024 年跑赢等权市场；中国电信开源 Xing4.0-29B-Intent，意图理解+参数抽取一次输出 JSON。",
    "📊 **产品与商业** — 蚂蚁数科 LingDT-Decision-1.0（4B/27B）客服场景 token 降 90%、风险识别 76%→89%；Claude 在 Google Cloud 多了一条 Anthropic 自营通道，按「谁做数据处理器」二选一。",
    "🛡️ **安全与治理** — AWS Continuum 代码漏洞服务 GA：先在沙箱里证明可利用、给出攻击路径与爆炸半径，再以补丁/PR 形式提交修复。",
    "🤖☸️ **K8s × AI** — Dynamo v1.6.0 把 Router 变成可插拔流控并接入 LPU；Kueue v0.20.3 让 MultiKueue 支持 RayService 弹性切片；CNCF 实测一次 Claude Code 小任务产出 181 条遥测、289KB JSON。",
    "☸️ **K8s 核心技术** — Istio 1.31.3 安全版本（ambient 等 ztunnel 就绪再摘污点、istiod CA 过期自愈）；Kyverno v1.19.2 把 CEL 准入的 request activation 改成每请求一次。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月23日 · 星期五",
    "{issue}": "033",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-23.html",
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
    assert k not in blob, f"unfilled placeholder {k}"
assert spec["chat_id"] == "oc_18845bcfeabb63caffa3e86c69a96d6e"
assert "oc_bf5fe15d7eef9babda1d709cc085f641" not in blob

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written |", spec["header"]["subtitle"], "|", spec["button"]["url"])
print("count_line:", count_line)
