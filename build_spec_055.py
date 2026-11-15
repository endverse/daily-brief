#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 055 from the locked card template + briefing.json."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json")
b = json.load(open(os.path.join(BASE, "briefing.json"), encoding="utf-8"))
spec = json.load(open(TPL, encoding="utf-8"))

hl = []
for i, h in enumerate(b["highlights"], 1):
    hl.append(f'**{i}. {h["title"]}**\n{h["summary"]}')
highlights = "\n\n".join(hl)

# 每个分类一行，按 emoji 查文案（不手写分类名，避免与 briefing.json 不一致）
BY_EMOJI = {
 "🧠": "DeepSeek 把 App 的联网搜索、深度搜索、文件上传、链接阅读与 OCR/ASR/TTS 拆成独立 API 分别计费，V4.1-Flash 已支持；SPU 用 116 任务、4207 次湿实验证明推理与算力不是瓶颈。",
 "🧩": "MixUA 给每条 agent 经验标四级作用域（用户对/用户/agent/全局），5 用户×7 agent 下 +16 分、偏好保留 90%、隐私探针泄漏 ≤0.02%。",
 "🧭": "腾讯开源 LoopForge（MIT，~900★）：Docker 沙箱 + SOP 引擎 + 人工闸门，统一编排 Codex/Claude Code/OpenCode 等 10 种 CLI，改动可回溯到需求。",
 "🏖️": "E2B 周更：文件传输切 HTTP/1.1、工作区改邀请制、新增 TencentOS/OpenCloudOS 模板，修掉「暂停时磁盘满连带杀掉同机沙箱」。",
 "🛠️": "Inkitt 用状态机 + 短时凭证 + 六类硬性禁区做「一次性 PR」；Shield 用 GPT-6 Astra 操作无 API 的遗留门户，第三方测算提速 35–40%。",
 "📊": "Google 把 agent 遥测统一收进客户自有 BigQuery：ADK/LangGraph 一行埋点，A2A 链路带 Cloud Trace span，审计日志与 CMEK 默认可用。",
 "🤖☸️": "vLLM 给出 EPD 分离实测：12 卡比 8 卡 PD 每卡吞吐高 6.6–9.5%、P90 TTFT 低 44–47%；KAI Scheduler v0.19.0 补 GPU 份额限额与 NUMA 归属。",
}

glance_lines = []
for s in b["sections"]:
    for c in s["categories"]:
        body = BY_EMOJI.get(c.get("emoji"))
        if not body:
            continue
        glance_lines.append(f'{c["emoji"]} **{c["title"]}** — {body}')

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = (f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · "
              f"{len(b['flash'])} 条快讯 · 数据源覆盖 72 小时")

repl = {
 "{date}": "2026年11月15日 · 星期日",
 "{issue}": "055",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-15.html",
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
print("footer:", spec["footer"])
