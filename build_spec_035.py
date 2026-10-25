#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 035 from the locked card template + briefing.json."""
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
    "🧠 **模型与研究** — 反向谄媚实验：32 人跟被植入 0–100% 假事实的助手学科学，测验分从 7.4 掉到 2.9，植入假答案被选 60%（OR 12.5），置信度区分对错的 AUROC 从 0.70 掉到随机。",
    "🧩 **Agent & Skill** — Hallmark 用 48 个主题 + 真浏览器 lint + 三层门禁做「反 AI 味」设计 skill；video-editor-skills 用 12 个纯文本 skill 把 Claude Code 变成 Resolve 一稿剪辑师；AWS 官方 Agent Toolkit GA 进 Anthropic 插件市场。",
    "🛠️ **AI 工程落地** — OpenAI 讲 FDE：先用 LLM 的构建速度把有价值的东西塞进用户手里，看什么站得住再规模化，最后把自己的定制实现换掉。",
    "📊 **产品与商业** — Decisions API 转 GA：/v1/decisions 只回概率/选项/分数不出文本，$0.10 每百万输入 token、无输出计费，号称比 Responses API 快 10 倍。",
    "💡 **观点与好文** — 奥特曼：已一年没看过一行代码，缺的不是更聪明的模型而是产品、算力与能持续感知现实的硬件；ICAAS 圆桌则警告路线过度集中。",
    "🛡️ **安全与治理** — OLMo-3 的 RLVR 检查点轨迹非单调：工具性行为 25.0% → 46.1%（约 200 步）→ 11.8%（最终），32B 端点同向。",
    "🤖☸️ **K8s × AI** — JobSet v0.13.0 把 Workload-Aware Scheduling 做进 alpha：整组 JobSet/ReplicatedJob/单副本三种粒度的 gang 调度 + 组内共享 DRA claim。",
    "☸️ **K8s 核心技术** — VPA 1.8.1 修 InPlace 下把几天前的 OOM 当新 OOM，以及 DaemonSet 副本数按 NumberReady 而非 DesiredNumberScheduled 计算。",
    "☁️ **云原生周边** — cert-manager 1.21.3 摘掉被攻破的 eMudhra 根证书，并堵住「能写 certificates/status 就能换走任意 Secret 私钥」的提权链；ESO 2.14.0 给状态与事件错误脱敏。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月25日 · 星期日",
    "{issue}": "035",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-25.html",
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
