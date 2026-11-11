#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 051 from the locked card template + briefing.json."""
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
 "🧩 **Agent & Skill** — Modern Web Guidance 把 web 最佳实践做成 skill 注入 coding agent（Chrome/Edge/Firefox/MDN 共维）；Snowflake CoCo 用动态工具发现 + 输出压缩把 SQL 修复通过率做到 86%，Claude Code 为 72%；GitHub 40% 的 PR 已由 agent 起草首版。",
 "🧠 **模型与研究** — Gemini 4 Carbon 全面开放：AutomationBench 53.9%、Antigravity 上线 /swarm 多 agent 编排；Deletion Tuning 归零不到 0.05% 权重即追平全参微调。",
 "🛠️ **AI 工程落地** — Google 一年发四套 TPU：8tx 做硬件级机密推理、8i Max 双芯单封装翻倍 HBM 带宽；Datadog Scout 用 GLM-5.3 Flash 后训练，90 个故障场景解 80 个、成本 1/3–1/8。",
 "📊 **产品与商业** — Claude Whiteboards / Sheets 公测、Dashboards 更名 Data 转 GA，产出留在对话里继续协作而不是导出到别处。",
 "💡 **观点与好文** — Simon Willison 让 Claude Code 造「蜂鸣定位仪」，五个设备三角定位误差 40cm，翻出一台等换电池的一氧化碳报警器。",
 "🛡️ **安全与治理** — VulnCheck 复盘 Glasswing：七个月 442 个 CVE、3.8 万条发现仅 19.4% 公开、217 条标记修复；OpenAI 开源 codex-security 的扫描—验证—补丁 CLI。",
 "🤖☸️ **K8s × AI** — KubeRay 捐给 CNCF，PARK 栈归一到 Linux Foundation；OpenShell 用 Cedar 把 agent 策略下沉到基础设施层；GKE CNP 三层优先级管住 LLM 命名空间；Istio Ambient Multi-Network GA。",
 "☸️ **K8s 核心技术** — CloudNativePG 与 OCM 同日进 CNCF Incubating：前者不用 StatefulSet 管 PostgreSQL，后者用异步 pull 管住 eBay 190+ 集群。",
 "🏘️ **社区与项目** — CNCF 观点：agent 让平台的使用者从工程师变成所有人，平台的设计假设需要重写。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年11月11日 · 星期三",
 "{issue}": "051",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-11.html",
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
