#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 052 from the locked card template + briefing.json."""
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
 "🧩 **Agent & Skill** — 上下文即控制平面：把知识/记忆/上下文分三层，用「上下文引擎」在模型外编译推理状态；Qwen Code 1.0 Preview 把 Qoder 的 harness 并进开源 CLI，带 Auto-Skills 与 Agent Teams。",
 "🧠 **模型与研究** — 6 bit 是拐点：同一成本口径下，多跑 4 次选项重排比继续降比特划算；用 margin 闭式解出 LoRA adapter 的免训练合并系数。",
 "🛠️ **AI 工程落地** — Evolving Infra 把算力分配与 KV cache 解耦，P95 TTFT 比 Dynamo 低最多 14 倍；SparseRead 给 agent 加「读多少」闸门，token 降 92.9%；MACaQ 用 32.5 GB 显存 64 分钟量化 122B。",
 "📊 **产品与商业** — Anthropic 路演定价 70–78 美元/股、最高募资 643.5 亿美元，11 月 19 日挂牌 ANT；Google 把 MCP/A2A/REST 连接器与声明式 skill 做成 ISV 分发通道。",
 "🤖☸️ **K8s × AI** — OpenShell 在 K8s 上的完整沙箱生命周期：每 agent 一个 Supervisor Pod，策略细到「哪个二进制、哪个 HTTP 方法」；AKS 上线拿本地 NVMe 做分布式读缓存 DACS。",
 "☸️ **K8s 核心技术** — Calico v3.32.4 修 IPAM 泄漏与 nftables 配置被忽略；Volcano v1.15.4 修只申请 DRA 的 Pod 绕过 gang 约束与配额虚占。",
 "☁️ **云原生周边** — BuildKit v0.35.0：内置 Dockerfile 前端升到 1.29，HTTP 源重试遵循 Retry-After。",
 "🏘️ **社区与项目** — CNCF 启动 User Group 计划，按行业与问题域建长期组织，取代一次性 End User 群。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年11月12日 · 星期四",
 "{issue}": "052",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-12.html",
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
assert spec["header"]["title"] == "📰 AI & 基础设施早报"
assert spec["header"]["template"] == "indigo"
json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, glance=%d" % (len(spec["blocks"]), len(glance_lines)))
print(count_line)
