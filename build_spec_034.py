#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 034 from the locked card template + briefing.json."""
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
    "🧩 **Agent & Skill** — 讯飞 Agent OS + APA 称跨系统协同效率 +90%、75% 流程自主流转，招采智能评审准确率约 97%；GitLab 19.4 给 Duo CLI 加 /goal 目标驱动模式（双模型互检），MCP 工具按读写分级授权。",
    "🛠️ **AI 工程落地** — StartLux 开源决策模型专用推理引擎 Prism，单张 H200 最高 5.3 倍（92.9ms→17.4ms）且输出概率逐位一致；IQuest-Q1 出 320B MoE（激活 15B）agentic CLI 基座。",
    "🧠 **模型与研究** — Kimi K3.1 Pro 拿 Artificial Analysis 55 分，承诺 11 月 4 日前放权重，价格约为 Opus 5.5 一半；FlagOS 2.2 九个算子库 1454 个算子，10 款异构芯片跨芯性能 +27%。",
    "📊 **产品与商业** — Xcode 27.2 用 JSON 项目格式取代 pbxproj（更利于 agent 改配置、少合并冲突）；PostgreSQL 19 因 AI 审查集中扫出长尾缺陷推迟到 11 月 19 日。",
    "💡 **观点与好文** — Arm 认为 Agent 让 CPU 回到关键路径：GPU 在等 CPU 跑编译、测试与沙箱，只说 Token 吞吐会算错容量。",
    "🛡️ **安全与治理** — Agent Mosaic 实测：即使加了密级标签与聚合规则，跨文档拼接泄露仍出现在 32.37% 的回答里，且拒答本身是侧信道。",
    "🤖☸️ **K8s × AI** — 只用 K8s 原生能力（PSA restricted + 命名空间级 RBAC + Quota + 默认拒绝 NetworkPolicy + ValidatingAdmissionPolicy）就能把 agent 生成的代码关进沙箱，实测 VAP 生效有延迟窗口。",
    "☸️ **K8s 核心技术** — Cilium 1.20.4 修 1.20.3 引入的 Gateway API 回归（CPU 飙高且无法转发）；Gateway API v1.7.0-rc.3 把 TLSRouteMixedMode 提到 Standard。",
    "☁️ **云原生周边** — Envoy v1.40.1 与 Prometheus v3.15.1 同批处理 eMudhra 中间 CA 泄露；Argo CD v3.5.6 修 server-side diff 误报与 SOCKS5 下 SSH 拉取。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月24日 · 星期六",
    "{issue}": "034",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-24.html",
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
