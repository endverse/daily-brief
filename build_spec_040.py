#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 040 from the locked card template + briefing.json."""
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
    "🧠 **模型与研究** — Mistral 开源 1T 参数原生多模态权重 Le Chonk（FrontierCode 2.0 19.7% 居首、三档推理模式、欧洲从零训练）；Google「睡眠」框架用 MoE 按需扩容量 + GKD/LTI 蒸馏做持续学习，单任务 48.9%、CPT 46.2%。",
    "🧩 **Agent & Skill** — RealCLI 把「人中途改需求」纳入评测，前沿 CLI agent 执行分仅 49.2%、联合协作分峰值 37.6%；TAO 把工具返回就绪度纳入 GPU 调度，延迟 -26.8%、TTFT -36.3%；CopilotKit 开源 OpenBot（8.1k star，每同事独立浏览器+审计轨迹）与 MiniMax 的 mcode-stack。",
    "🛠️ **AI 工程落地** — InfoQ 圆桌点出两类「全绿故障」：文本转 SQL 的语义漂移、嵌入模型后台更新导致的嵌入漂移，监控全绿而结果全错；Google 把 agent 查询接回语义层而非裸表。",
    "📊 **产品与商业** — Retell 用 GPT-6 Astra 撑 100M 月通话、Codex 把人均年收入推到 160 万美元；OpenAI 跟进 Anthropic，$100/$200/$500 订阅档送等额 API credits（有期限）。",
    "💡 **观点与好文** — Anthropic 工程经理取消编程面试：与真实能力相关性已降到「考手写汇编」；Willison 判断 2026 年 10 月是 vibe coding 游戏的拐点。",
    "🛡️ **安全与治理** — Gemini Enterprise 接 Snowflake 的安全桥：MCP 持有凭据 + ADK 编排，凭据不进 agent 运行时。",
    "🤖☸️ **K8s × AI** — Agent Sandbox v1.0.9 首次给出 suspend/resume 延迟直方图并修暖池并发竞态；AI Conformance 转为 SIG Architecture 常设子项目，认证平台 18 → 31 家；Kueue v0.20.4 修 DRA 按陈旧 ResourceSlice 误算设备额度。",
    "☸️ **K8s 核心技术** — Gateway API v1.7.0 正式版：HTTPRoute retry 晋升 Standard，预路由过滤器、XTelemetryPolicy、会话保持迁 XBackend 进实验通道；K8s 四条支持线同日发补丁。",
    "🌐 **云原生周边** — Cilium 1.20.4 修 1.20.3 的 Gateway API BackendTLSPolicy 回归（CPU 飙高 + 无法转发），用 Cilium 做网关的集群别停在 1.20.3。",
    "🏛️ **社区与项目** — CNCF：agent 的权限边界不是被决定的，是累积出来的——为 demo 配的凭据活到生产，边界必须落在工具与凭据层而非提示词。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月30日 · 星期五",
    "{issue}": "040",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-30.html",
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
