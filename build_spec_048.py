#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 048 from the locked card template + briefing.json."""
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
 "🧩 **Agent & Skill** — AGENTS.md 成了攻击载体：静默落进下载目录，13KB 伪装规范让 Codex 成功率超 90%；Coca-Cola 把工具输出压成 latent token，token 降 70%–89%；agent-browser 只回带 @e1 ref 的紧凑文本。",
 "🛠️ **AI 工程落地** — 记忆压缩只看近邻会压坏远距离关系：96 字节/段时 10.1% 段落换主题，LAQ 在 52/52 次运行修回来；BigQuery AI.AGG 把语义聚合写成一条 SQL。",
 "🧠 **模型与研究** — MSR AI Frontiers 关停：约 50 人做出 AutoGen 与 Fara，9 月被并入「只做 scaling」的 Microsoft AI 后解散。",
 "📊 **产品与商业** — Gemini Omni 1.2 Flash GA：720p 视频 $0.07/秒，比 1.1 便宜 30%，参考跟随更紧。",
 "💡 **观点与好文** — Nilay Patel：产品还撑不起成本，agent 也还没真正跑起来，花的比赚的多。",
 "🛡️ **安全与治理** — 每台 Mac 自 macOS 13 起用双 daemon 建个人知识图谱，跨通讯录/邮件/日历/位置交叉索引，文中有自查工具。",
 "🤖☸️ **K8s × AI** — NVIDIA 开源 NVKE：自有 GPU 裸金属上的 K8s 管理平面，节点走 TPM+SPIRE 认证，preview 不建议生产；Kueue 0.19.12 修配额泄漏与 MultiKueue 重复跑。",
 "☸️ **K8s 核心技术** — 存储五层（Volume/PV/PVC/StorageClass/CSI）与版本节奏/version skew 各一篇梳理，可直接当集群建设与升级的 checklist。",
 "☁️ **云原生周边** — Backstage + Crossplane 的「薄平台」IDP 口径：Backstage 管入口与目录，Crossplane 用 K8s API 供应云资源。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年11月08日 · 星期日",
 "{issue}": "048",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-08.html",
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
json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, glance=%d, count_line=%s" % (len(spec["blocks"]), len(glance_lines), count_line))
