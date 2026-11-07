#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 047 from the locked card template + briefing.json."""
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
 "🧠 **模型与研究** — StrataFlux 显存不变让 Qwen3-8B 的 AIME 从 11.0% 升到 47.1%；SAE 拆 MoE 发现 Java 代码与前端代码各有独立专家；同一份数据换随机种子，越狱面就换一批（150 个模型）。",
 "🧩 **Agent & Skill** — Harness-S 不找万能 harness，而让兄弟变体互补地救失败样本；SwarmEvolve 在 latent 空间用几百个廉价 agent 传 KV cache，3–8 分钟追平别人 60 分钟。",
 "🛠️ **AI 工程落地** — Terminal-Bench 2.0 自查出约 30% 的题目有问题，修复版准确率涨 10 个百分点；tsrs 靠指挥 Claude Opus 5.5 移植 TypeScript 编译器，37,000 文件从 80 秒到 7 秒。",
 "📊 **产品与商业** — 腾讯 Hy4 调用激增，WorkBuddy 十倍扩容；DigitalOcean 把 agent 会话回写成可检索数据，接 Signals 找失败、Simulations 演练修复。",
 "🛡️ **安全与治理** — OpenAI 发布 GPT-6 Cyber，专做授权范围内的漏洞挖掘与修复；Google 明确表态 agent 时代被动防御不再成立。",
 "🤖☸️ **K8s × AI** — GCE Z4M 存储优化机型 GA，同时给 VM 与裸金属，面向 checkpoint、分布式 KV cache 与并行文件系统。",
 "☸️ **K8s 核心技术** — 1.38 beta 让 seccomp 配置可按 digest 从 OCI registry 拉取、DRA Device Binding 转 GA；Istio 1.31.4 修 5 个 CVE，ambient 端口级 STRICT mTLS 会被静默跳过。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年11月07日 · 星期六",
 "{issue}": "047",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-07.html",
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
assert spec["header"]["template"] == "indigo", spec["header"]
assert spec["header"]["title"] == "📰 AI & 基础设施早报"
json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, glance=%d, count_line=%s" % (len(spec["blocks"]), len(glance_lines), count_line))
