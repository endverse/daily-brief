#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 046 from the locked card template + briefing.json."""
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
 "🧠 **模型与研究** — 百度开源文心 5.5 Flash Base：2800 亿 MoE、每 token 激活 140 亿，预训练 33.5 万亿 token；腾讯混元 Hy4 升到 770B 并首次支持 Computer Use。",
 "🧩 **Agent & Skill** — Google 把 SKILL.md 当程序用 AlphaEvolve 进化、配对评测后涨 33 分；五条铁律指出 Δ=0 九成是 skill 没被加载；快手用 415 条规则做 Skill 门禁，累计拦下 3000+ 问题。",
 "🛠️ **AI 工程落地** — Gemini 4 Argon 11 小时无人值守改 ADK：会话准备降 40%、包导入降 21%，但 6 项改动有 4 项被人评审拒掉；谷歌开源端侧 GPU 引擎 ML Drift，内存比 llama.cpp 低 12%。",
 "🛡️ **安全与治理** — GPT-6 Astra 在“安全研究”框架下少完成约 40% 评分项且思维链无明确决定；Claude Code 被报把用户邮箱写进 User-Agent 发给任意网站。",
 "🤖☸️ **K8s × AI** — Agent Substrate 1.0 上 GKE：Actor/Worker 拆分、空闲 500ms 挂起恢复、密度 10 倍；Kueue 0.20.5 修并发准入配额泄漏，Dynamo 1.6.2 修超长 prompt 的 500。",
 "☸️ **K8s 核心技术** — prometheus-operator 0.95 给 CRD 加 extraScrapeMetrics，补一批 Alertmanager receiver 校验（0.95.1 只是镜像重发）。",
 "🌐 **社区与项目** — kpt 发布 v1.0.0，Porch 并回组织，GitOps 包管理终于定版。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年11月06日 · 星期五",
 "{issue}": "046",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-06.html",
}
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
for ph in ["{date}", "{issue}", "{cover}", "{highlights}", "{glance}", "{count_line}", "{page_url}"]:
    assert ph not in blob, "leftover placeholder: " + ph
assert spec["chat_id"] == "oc_18845bcfeabb63caffa3e86c69a96d6e"
assert spec["header"]["template"] == "indigo", spec["header"]
assert spec["header"]["title"] == "📰 AI & 基础设施早报"
json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, glance=%d, count_line=%s" % (len(spec["blocks"]), len(glance_lines), count_line))
