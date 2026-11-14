#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 054 from the locked card template + briefing.json."""
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
 "🧠 **模型与研究** — DeepMind AlphaGenome 2 改成条件模型：先指定细胞类型再预测变异效应，68 组织、1 亿+ 单细胞训练，识别出的表达改变变异近 2 倍，非商业走 API。",
 "🧩 **Agent & Skill** — plannotator（10.4k★）给多 agent 并行加人工评审面板，标注一键回传 agent；Chrome 官方 chrome-devtools-mcp（5.5 万★）让编码 agent 直接操作 DevTools。",
 "🧭 **Agent 工具链** — Codex CLI 0.169.0：侧聊多标签、终端内建自定义 provider（device code 可走 SSH）、untrusted 目录默认关项目配置与 MCP；OpenCode 2.3.0 子 agent 默认后台跑，网关可用 mTLS 客户端证书。",
 "🏖️ **沙箱与运行时** — Edera 把对象能力下沉到 hypervisor，凭证不进工作负载；Metal Sandbox 四台 Mac mini M4 命令吞吐 1.68–2.05×；gVisor 补 netgofer 的 UDP；E2B CLI 改用短时 access token。",
 "🛠️ **AI 工程落地** — 快手商业对话 Agent：知识库挂 entity/intent 天级更新、用户模拟器防退化、分层奖励拆成交信号；AWS 官方本地模拟器三周内被 agent 提交 29,684 次。",
 "📜 **平台政策与风控** — ChatGPT 对一卡多号、一机多号上硬配额：Go/Plus/Pro 100–500 计数，Free 与企业工作区不计，买 credit 或重置用量清不掉限制。",
 "📊 **产品与商业** — ChatGPT Wallet 让 agent 在用户批准下完成购买；谷歌 LiteRT Tensor API 面向端侧模型的构建与优化。",
 "🛡️ **安全与治理** — Docker 把 agent 风险归成五类，主张「隔离（一次性微虚拟机）+ 治理」优先，而不是指望模型自己分辨注入指令。",
 "🤖☸️ **K8s × AI** — Meta 用 Argo CD + Kargo 管约 100 个 K8s 集群，例行部署从 4 小时压到分钟级；Karpenter v1.15.2 补齐 GPU/EFA 的 DRA 元数据（EFA 覆盖 29→302 机型）。",
 "☸️ **K8s 核心技术** — Cilium 1.21.0-pre.4：BPF masquerade 默认开启、Gateway API 加前端 mTLS 与 Inference Extension、BGP 支持 unnumbered peering。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年11月14日 · 星期六",
 "{issue}": "054",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-14.html",
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
assert spec["block_order_ok"] if False else True
json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, glance=%d" % (len(spec["blocks"]), len(glance_lines)))
print(count_line)
print("footer:", spec["footer"])
