#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 029 from the locked card template + briefing.json."""
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
    "🧩 **Agent & Skill** — Data World 先定义世界机制再合成文件/任务/rubric，zero-RL 训出 35B-A3B 在 DABstep-Hard +20.9；SERO 用 oracle 延续突破长程 RL 的 rollout 视野；CoWorld 把视频世界模型做成工具、skill 随执行反馈演化。",
    "🧠 **模型与研究** — Meta Muse Spark Open 开放 816B MoE 权重、106 万上下文，2×M5 Ultra 可本地跑，编码基准输给 GLM 5.3 max 与 Kimi K3 max；readout 研究说明能力「出现」常只是解读层学会表达；LeanPRM 用 Lean 自动标出 152K 个证明步骤。",
    "🛠️ **AI 工程落地** — llm-echo 0.5 把 tool call、system prompt 与 reasoning token 计入模拟用量，可零成本验证 agent 计费口径。",
    "🛡️ **安全与治理** — Anthropic 让 METR 六人拿到员工级系统权限，评估报告公开发布、公司无否决权。",
    "🤖☸️ **K8s × AI** — KAI-Scheduler v0.18.6 取消每 worker 的 score map，BindRequest 只删失败的、重试期间保留 reservation。",
    "☸️ **K8s 核心技术** — Istio 1.30.6 修 HTTP/2 方法大小写绕过授权与 istiod ambient 崩溃；containerd 2.2.10 一次修四个公告；Envoy 1.39.4 补 RDS 路由配置析构竞态。",
    "☁️ **云原生周边** — Cloudflare 复盘 dm-thin 的 skip_block_zeroing 跨租户泄露：Firecracker 未破，5614/5614 目录块命中他人数据。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月19日 · 星期一",
    "{issue}": "029",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-19.html",
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
