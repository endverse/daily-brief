#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 053 from the locked card template + briefing.json."""
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
 "🧠 **模型与研究** — Thinking Machines 开源 Inkling 2 Small（594B/17B 激活、1M 上下文），vLLM 当天 TP4 跑到 630 tokens/s/user；MiniMax 开源 H3-Image，原生 4K、约两毛一张，能给产品图推正交三视图。",
 "🧭 **Agent 工具链** — Claude Code 2.1.323 上线实验性 Code Mode：Claude 写 JavaScript 调工具，不再一次一个 tool call；Gemini CLI 0.69 preview 的 /stats 加按日 token 热力图。",
 "🏖️ **沙箱与运行时** — Agent Sandbox v1.0.11 让沙箱路由支持浏览器路径前缀（可跑 JupyterLab），加 router-tunnel 与 X-Sandboxd-Token；sandboxd 拒绝 FIFO/设备文件、删除只删符号链接本身。",
 "🛠️ **AI 工程落地** — JioHotstar 用 8 周做出 5 亿人用的语音内容发现，复盘是「先定不该答什么，再谈 eval」；Amplitude 的 Wave 约 80% 由 OpenAI 模型驱动，把洞察到上线压到 1–2 天。",
 "📜 **平台政策与风控** — OpenAI 新版 Usage Policies 11 月 20 日生效：模型路由与 AI 网关须先获 OpenAI 审批，新增 SafetyIDs 区分终端用户。",
 "🤖☸️ **K8s × AI** — DeepSeek-V4.1-Flash 搬上 Vera Rubin NVL72，单卡 1.7M tokens/s、官方口径 58× GB300；vLLM-Omni 四卡原生 4K 出图中位 0.87 秒。",
 "☸️ **K8s 核心技术** — Kueue v0.20.6 修 v0.20 升级后 kube-apiserver watch cache 初始化失败，以及弹性切片重复计费导致的配额虚占。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年11月13日 · 星期五",
 "{issue}": "053",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-13.html",
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
