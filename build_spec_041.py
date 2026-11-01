#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 041 from the locked card template + briefing.json."""
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
    "🧠 **模型与研究** — EmbeddingGemma 2 把文本/代码/图像/视频/音频放进同一个 768 维空间，编码器按需加载（2.7 亿–7.4 亿参数），MRL 截到 128 维只掉 10% 文本质量、存储降到 1/6；Soft-MTP 一行改动去掉 MTP 梯度里的噪声残差，167M→1.2B 全线优于标准 MTP。",
    "🧩 **Agent & Skill** — EnvHarness 只换交互层（setup/rule/link）就按短板改环境，四个模型涨 2.9–3.7 点；Investor's Last Exam 用 343 万份冻结文档评股票研究，最强模型总分 68.1、预测建模仅 52.5；EPSBench 显示六个模型对分析师共识无优势、80% 区间只覆盖 37–70%；VeriCUA 把任务完成验证改成 agent 主动取证。",
    "🛠️ **AI 工程落地** — 审计 305 个 GGUF 量化包：7 个官方 tag（2.3%）连 164 题里 6 题都做不对，权重逐 tensor 无损，问题在量化配方；加 importance matrix 让 Qwen2.5-Coder-3B 从 0 题回到 76–113 题。Efiwe 用 Pyodide/sql.js 把 Python 与 SQL 塞进手机浏览器离线跑，2.2 万学习者。",
    "📊 **产品与商业** — Anthropic 把 Max 5x/20x 改名 Max/Ultra，200 美元 Ultra 取消 5 小时窗口，周额度仍是 Pro 的 10 倍。",
    "💡 **观点与好文** — Spawn 每月烧 300 万美元 token、agent 直接改线上代码每小时发布，一小时没发布按 SEV-0、坏改动 30 秒就地回滚；另有把 NES 模拟器烤进 Qwen3.5-4B 权重的实验。",
    "🛡️ **安全与治理** — Parameter Labs 的 ChatGPT 账号接管链：MathLive postMessage → innerHTML → 无 sandbox 子 iframe → YouTube oEmbed 反射 JS，一个分享链接即可在他人登录态下窃数据。",
    "🤖☸️ **K8s × AI** — Grove v0.2.0-beta1 把 API 提到 v1beta1（packDomain→pack.required，minReplicas 默认改跟 minAvailable），AI 推理分组编排可写稳定清单。",
    "☸️ **K8s 核心技术** — 社区新设 Workload Conformance WG：给「工作负载怎么跑」定标准，覆盖安全/中断韧性/资源/网络/存储/API/可观测性，每条要求必须能被测试二进制客观验证。",
    "🌐 **云原生周边** — AWS Lambda Web Functions 可直接跑 Express/Hono，支持并发请求与流式响应，按活跃 CPU 计费、等下游不计费。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年11月01日 · 星期日",
    "{issue}": "041",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-01.html",
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
for ph in ["{date}", "{issue}", "{cover}", "{highlights}", "{glance}", "{count_line}", "{page_url}"]:
    assert ph not in blob, "leftover placeholder: " + ph
assert spec["chat_id"] == "oc_18845bcfeabb63caffa3e86c69a96d6e"
assert spec["header"]["template"] == "indigo" and spec["header"]["icon"] == "myai_colorful"

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, highlights=%d chars" % (len(spec["blocks"]), len(highlights)))
