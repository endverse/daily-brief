#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 044 from the locked card template + briefing.json."""
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
    "🧠 **模型与研究** — LoL 让 Transformer 推理时动态重排层顺序；CoworkOS 把长周期 agent 的任务策略与执行管理分离；CUA-Master 用递归自改进扩展计算机操作 agent；SWE-Trail 用历史轨迹引导编码 agent 训练数据收集。",
    "🧩 **Agent & Skill** — p-e-w/heretic 免训练注入方向向量改 LM 行为（701 star）；Balanov/shim 零依赖本地优先 AI harness；spotify/portal-ai-plugins 把内部 AI 能力做成可调用插件；Usagi 闲鱼监控是 GUI 爬虫+AI 的落地样例。",
    "🛠️ **AI 工程落地** — DistDebug-Bench 用 120 个真实分布式 bug 评测 agent 排障；OpenAI 称 Codex 正在加速 CAD/PCB/仿真等物理世界工程。",
    "📊 **产品与商业** — 量子位称模型谁都买得到、差距在 AI 生产力系统；AWS 把 Step Functions（220+ 服务编排）直接作为工具交给 agent 调用。",
    "💡 **观点与好文** — honnibal 指「Astra 读写权重改进 Qwen」帖子有误导；Simon Willison 实测 Qwen 3.8 27B 也能在笔记本上解读权重文本。",
    "🛡️ **安全与治理** — MCP Tool Poisoning 首次跨框架、带真实执行证明工具描述污染会致失守；VeriHarm-Bench 可验证地衡量编码 agent 的「有害成功」。",
    "🤖☸️ **K8s × AI** — OpenKruise Agents v0.6.0 把多用户 agent 沙箱直接做成 K8s 上的开源运行时，补隔离/凭证/配额与自动回收。",
    "☸️ **K8s 核心技术** — Azure Application Gateway for Containers 公测 JWT 校验、MCP 网关与私有入口；Capsule v0.15.2 给多租户加 OpenShift 开关（最低 K8s 1.36）。",
    "🌐 **云原生周边** — BuildKit v0.34.2 修两处安全漏洞，含恶意客户端借控制 API 越权写宿主 xattr。",
    "🏘️ **社区与项目** — Fujifilm 将磁带产能提升 5 倍，AI 训练/推理的冷数据归档需求推高老存储介质。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年11月4日 · 星期三",
    "{issue}": "044",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-04.html",
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
assert spec["header"]["template"] == "indigo" and spec["header"]["icon"] == "myai_colorful"

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, highlights=%d chars, count_line=%s" % (len(spec["blocks"]), len(highlights), count_line))
