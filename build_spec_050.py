#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 050 from the locked card template + briefing.json."""
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
 "🧩 **Agent & Skill** — Addy Osmani 的 agent 管理工作流（测试/Linter 自验、Stop Hook 关闸、子 agent 评审）；openJiuwen TTSE 把环境事实与执行方法分成两条轨道演进。",
 "🛠️ **AI 工程落地** — Anthropic 用自研 Scion 换掉单体仓库的 Git：日合并 3 万次，检出快两个数量级；AgentCore Runtime V2 用快照恢复把 P75 冷启动稳在 2 秒。",
 "🧠 **模型与研究** — Claude Fable 5.2 降价登顶 FrontierCode，Meta Muse Ember 以 $0.10/$0.50 压在帕累托前沿；蚂蚁灵波开源 LingBot-Touch 触觉基础模型。",
 "💡 **观点与好文** — Jeff Dean 的 Discovery Loop（约 20 个自动化改进循环）与李飞飞同场泼的 RSI 冷水：瓶颈在验证，不在想法。",
 "🛡️ **安全与治理** — AWS 用 agent 分诊内核 CVE（3.4 秒/个、脚本先丢 70%），仍留两名工程师复核；Gartner 2027 趋势主线改为智能体治理。",
 "🤖☸️ **K8s × AI** — Google 的开源 AI-native 栈：llm-d 1.0 把 KV 命中率 35%→70%、TTFT 降 70–85%；Cloud Pathways / Dynamic Slicing GA；TPU Sync 把 TTFT 再压 90%。",
 "☸️ **K8s 核心技术** — 两份可当检查表用的整理：调度两阶段与六种放置手段、三种探针的职责边界与参数语义。",
 "☁️ **云原生周边** — kpt v1.0.0 结束 pre-release；CNCF 调研 492 人：VM 仍占生产应用 53%，34% 的扩 VM 动因来自 AI/agent 负载。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年11月10日 · 星期二",
 "{issue}": "050",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-10.html",
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
print("spec.json written: blocks=%d, glance=%d" % (len(spec["blocks"]), len(glance_lines)))
print(count_line)
