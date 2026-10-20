#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 030 from the locked card template + briefing.json."""
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
    "🧩 **Agent & Skill** — Librarian Agents 让 agent 预先造可复用工作区，BrowseComp-Plus 高出最强基线 33 个百分点；Lean4AgenticRL 用 Lean4 打多级过程奖励，LAR-27B 在 TerminalBench-2.1 拿 77.3%。",
    "🧠 **模型与研究** — ACT3D 只喂单张图、靠 RL 学主动探索，六个 3D 基准平均 53.2% 超过 Gemini 3.6 Flash 且帧数少 50–70%；VAST 开源 EdenLive，单张 5090 上 720P 超 24FPS。",
    "🛠️ **AI 工程落地** — Cloudflare 推 agent 原生 CLI「cf」：默认 JSON、覆盖 3000+ API 操作，Wrangler 走 18 个月退场；阿里云 7 个样板间把全链路 2 小时压到 5 分钟。",
    "📊 **产品与商业** — 智谱 GLM-Legal 拿下 Vals AI 法律双榜开放权重第一，Harvey LAB 全通过率 19.2%，成本约为 Gemini 4 Argon 的 1/70。",
    "💡 **观点与好文** — Simon Willison 转的「编程讣告」把 AI 焦虑拆成「爱交付」与「爱解谜」两类人；Google 列出 LLM-as-judge 五种偏差，换选项顺序就能翻转判决。",
    "🛡️ **安全与治理** — Intact 按元素来源与能力而非文本隔离网页，注入攻击通过率从 73.1% 降到 12.8%。",
    "🤖☸️ **K8s × AI** — kubezilla 在 v1.34.1 上用双 namespace + PSA restricted + 只许建 Job 的 RBAC 搭 agent 沙箱；Kyverno 生态把策略推进到内核（eBPF + LSM），按协议而非端口拦外联。",
    "☸️ **K8s 核心技术** — KEP-5945 给 DRA 加 skipNodeOperations，v1.38 默认开启；PodFailurePolicy 规则可命名，Job 失败能指到具体规则。",
    "🧰 **云原生周边** — Kepler 维护者主张把 SCI 做成 OTel 语义约定，难点从「测得出」变成「分摊归属」。",
    "🌱 **社区与项目** — LWKD：十月 patch release 推迟到 10/20，SIG Autoscaling 新增 model-serving-signals 子项目。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月20日 · 星期二",
    "{issue}": "030",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-20.html",
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
