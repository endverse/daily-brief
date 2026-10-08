#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 019 from briefing.json + the locked card template.
Only placeholders are substituted; title/icon/color/footer/block order untouched."""
import json, os

TPL = "/Users/endverse/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json"
COVER = "/Users/endverse/daily_brief_cover.png"
b = json.load(open("briefing.json"))
spec = json.load(open(TPL))

assert os.path.exists(COVER), COVER

# header
spec["chat_id"] = "oc_18845bcfeabb63caffa3e86c69a96d6e"
spec["header"]["subtitle"] = "2026年10月08日 · 星期四 · 第019期"
spec["cover_image"] = COVER

# highlights block: numbered bold title + summary
hl = []
for n, h in enumerate(b["highlights"], 1):
    hl.append(f"**{n}. {h['title']}**\n{h['summary']}")
highlights = "\n\n".join(hl)

# glance block: per category emoji + bold label + one sentence per section
labels = {"Agent & Skill": "🧩", "模型与研究": "🧠", "AI 工程落地": "🛠️",
          "产品与商业": "📊", "观点与好文": "💡", "安全与治理": "🛡️",
          "K8s × AI": "🤖☸️", "K8s 核心技术": "☸️", "社区与项目": "📦",
          "云原生周边": "☁️", "公有云动态": "🌩️"}
G = {
 "Agent & Skill": "Cloudflare 开源 security-audit skill（六阶段安全审计）；OpenAI×Ironclad 用 11 个合同任务推进 computer use；nanoMuse 提出开源个人 agent；cmux 是给编码 agent 的 Ghostty 系终端。",
 "模型与研究": "GPT-6 携 Intelligent UI 全球铺开；Sherpa 用多轮 RL 教 LLM「因材施教」；混合注意力 LLM 的多语言行为首份系统研究；OpenAI 开源 722 篇模型产出的数学手稿。",
 "AI 工程落地": "OPD 用同策略蒸馏给 rubric 式 RL 热启动；论文追问可训练输入嵌入表是否必要；VLA 实时推理的端到端延迟分解与两步流去噪。",
 "产品与商业": "Meshy 进入 a16z 消费级 AI 月收入 Top 50（唯一 AI 3D 公司）；国内 AI 影视公司引入《怪物史莱克》编剧、视频模型称全球第二。",
 "安全与治理": "论文检验「按来源筛选合成数据」的两个前提；CheckerBench 评测 agent 能否合成静态分析检查器；投机解码的安全面研究。",
 "K8s × AI": "Red Hat 给出 Kueue×DRA 方案，GPU 配额从按张数改为按显存计费；Anyscale on Azure GA，在 AKS 上托管运行 Ray。",
 "社区与项目": "Meshery 升入 CNCF 孵化项目，定位统一云原生管理平面。",
}
lines = []
for sec in b["sections"]:
    for cat in sec["categories"]:
        emoji = labels.get(cat["title"], cat.get("emoji", "•"))
        lines.append(f"{emoji} **{cat['title']}** — {G[cat['title']]}")
glance = "\n".join(lines)

n_items = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
n_cats = sum(len(s["categories"]) for s in b["sections"])
count_line = f"共 {len(b['highlights'])} 条重点 · {n_cats} 大板块 {n_items} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

# fill blocks in the locked order: highlights md, hr, glance md, grey count
blocks = spec["blocks"]
assert blocks[0]["type"] == "markdown" and "今日重点" in blocks[0]["content"]
assert blocks[1]["type"] == "hr"
assert blocks[2]["type"] == "markdown" and "今日看点" in blocks[2]["content"]
assert blocks[3]["type"] == "grey"
blocks[0]["content"] = "**🔥 今日重点**\n\n" + highlights
blocks[2]["content"] = "**📌 今日看点**\n\n" + glance
blocks[3]["content"] = count_line

spec["button"]["url"] = "https://endverse.github.io/daily-brief/2026/2026-10-08.html"
# footer / title / icon / template left as-is from the locked template

json.dump(spec, open("spec.json", "w"), ensure_ascii=False, indent=2)
print("spec.json written:", "chat", spec["chat_id"], "| blocks", len(blocks), "| count_line:", count_line)
