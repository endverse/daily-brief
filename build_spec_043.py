#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 043 from the locked card template + briefing.json."""
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
    "🧠 **模型与研究** — LeCun 新论文给「柏拉图表征假说」补证明：1.09 亿参数 JEPA 的跨模态对齐分 0.184 超过 Qwen2.5-72B 的 0.154，样本效率约 42 倍（按 token 算 14 倍）；GPT-6.2 Astra 已在 Pro 档灰度，20% 请求被路由。",
    "🧩 **Agent & Skill** — Buildkite 给 CI 加 validate_pipeline / compare_builds / create_pipeline_webhook 三个 MCP 工具，密钥收到流水线作用域；worktrunk 给并行 agent 一人一个 git worktree（10k star）。",
    "🛠️ **AI 工程落地** — Qodo 用 Codex 插件把公司编码规范带进评审，目标是在开 PR 前拦下 P0 级问题。",
    "📊 **产品与商业** — 百度搜索 AI API 增强版压到 4.9 元/千次（限时活动价），抢 Agent 的默认检索入口；ChatGPT Pro 额度全面翻倍，Pro 500 = Plus 的 50 倍。",
    "💡 **观点与好文** — 飞猪/货拉拉/江苏移动划企业 Agent 边界：求解器算票价、业务 ID 换短 ID、钱包相关动作必须人工确认，网关要防 agent 的重试风暴。",
    "🛡️ **安全与治理** — Mandiant 记录 LLMJacking 单日盗刷超 10 万美元、累计到 100 万美元，已出现 LLM Mixer 转售网关；OpenAI 新 Model Spec 首条改为「忠于人类意图」。",
    "🤖☸️ **K8s × AI** — NVIDIA AICR 把 Vera Rubin 的驱动/DRA/内核组合写成可复现配方，NCCL 门禁 744.71 GB/s；KAI-Scheduler v0.18.7 修绑定重试时丢失 GPU 预留。",
    "☸️ **K8s 核心技术** — Envoy v1.39.6 单点安全发布：distroless 换掉 ca-certificates，剔除被攻破的 eMudhra 中间 CA，1.39.5 仍在信任。",
    "🌐 **云原生周边** — Argo CD v3.5.7 修 Rollout 无 status 时的 actions 列表，镜像带 cosign 签名与 SLSA L3 provenance。",
    "🏘️ **社区与项目** — Linkerd 十周年纪录片 11 月 9 日在 KubeCon NA（盐湖城）首映。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年11月03日 · 星期二",
    "{issue}": "043",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-03.html",
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
for ph in ["{date}", "{issue}", "{cover}", "{highlights}", "{glance}", "{count_line}", "{page_url}"]:
    assert ph not in blob, "leftover placeholder: " + ph
assert spec["chat_id"] == "oc_18845bcfeabb63caffa3e86c69a96d6e"
assert spec["header"]["template"] == "indigo" and spec["header"]["icon"] == "myai_colorful"

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, highlights=%d chars" % (len(spec["blocks"]), len(highlights)))
