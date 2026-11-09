#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 049 from the locked card template + briefing.json."""
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
 "🧩 **Agent & Skill** — EvoMemState 把 agent 记忆建成「事实 + 关系状态 + 推理状态」三层；VisSearch-Bench 204 题长程视觉搜索，最强模型带工具只完整解出 26.47%。",
 "🛠️ **AI 工程落地** — vLLM v0.33.0 发 LibTorch Stable ABI wheel，升级 PyTorch 不用重编；Cloudflare Auto Router 公开基准：可靠性 +10pp、成本约 1/3。",
 "🧠 **模型与研究** — Muir 把门控压成低秩投影，1.34B 外推 1000 万 token 无漂移；微信 WeLM-Image 单张 H20 上 4.98 秒出 1024²。",
 "📊 **产品与商业** — OpenAI 自研 Git 后端 Pando，单次推送中位耗时降近八成，并收购 Pierre 补 Codex 的代码存储。",
 "💡 **观点与好文** — 同一 parse_number()：C 扩展 14KB vs Rust 321KB，手写快速路径后 C 才以 16–19ns/行反超。",
 "🤖☸️ **K8s × AI** — Agent Sandbox v1.0.10：路由支持 gRPC-Web，NetworkPolicy 改为只放行带 sandbox-name-hash 标签的 Pod（破坏性变更）。",
 "☸️ **K8s 核心技术** — K8s 1.36.6 修 DRA claim 状态抖动与 kube-proxy sysctl 回归；Istio 1.30.8 一次修 7 个 CVE，ambient 明文绕过 mTLS 达 CVSS 8.2。",
 "☁️ **云原生周边** — Lima v2.3 在 Windows 上不依赖 QEMU 起 VM，Linux 新增 shared/host/bridged 网络；OTel Collector 0.165 删 confighttp 废弃字段。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年11月09日 · 星期一",
 "{issue}": "049",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-09.html",
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
