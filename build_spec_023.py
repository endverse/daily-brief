#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 023 from briefing.json + the locked card template.
Only placeholders are substituted; title/icon/color/footer/block order untouched."""
import json, os

TPL = "/Users/endverse/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json"
COVER = "/Users/endverse/daily_brief_cover.png"
b = json.load(open("briefing.json", encoding="utf-8"))
spec = json.load(open(TPL, encoding="utf-8"))

assert os.path.exists(COVER), COVER
assert b["issue"] == 23

spec["chat_id"] = "oc_18845bcfeabb63caffa3e86c69a96d6e"
spec["header"]["subtitle"] = "2026年10月12日 · 星期一 · 第023期"
spec["cover_image"] = COVER

# highlights block: numbered bold title + summary
hl = []
for n, h in enumerate(b["highlights"], 1):
    hl.append(f"**{n}. {h['title']}**\n{h['summary']}")
highlights = "\n\n".join(hl)

# glance block: per category emoji + bold label + one sentence
G = {
 "Agent & Skill": "Nous Research 官方 Hermes 插件库上线，Home Assistant / Spotify / Claude Subscription DirectSDK 一条命令安装；talorys 把个人 agent 部署进自己的 Cloudflare 账号；agent-chrome-relay 让 agent 复用你已登录的 Chrome；InfoQ 给出用编码智能体做架构的五种方法；论文 Opera 把每条纠正当持久笔记跟踪。",
 "模型与研究": "论文用 transition law 的格结构刻画扩散/AR 混合解码调度的可预测性；多轮对话中「被提及又否决」的改动仍会打乱执行；冻结模型靠部署经验持续更新专家知识；GPT-4o 下架 8 个月后社区自救仍在继续。",
 "AI 工程落地": "Google 为 XProf 加入内核级分析，三重缓冲把 Pallas 矩阵乘内核从 125.5µs 降到 88µs；论文 CARE 给 VLA 推理加速加正确性认证；AirLLM 用单张 4GB 卡跑 70B 推理再上 Trending；SpecFold 折叠扩散 LLM 投机解码的分支冗余。",
 "产品与商业": "民间版 DeepSeek-Bot 上线一天 250+ star：基于 DeepSeek Harness 的多 Bot 团队插件，主管 Bot 路由省 token、Markdown 记忆 + 每轮自动记忆审查，数据全落本地。",
 "观点与好文": "DHH 用 agent 重写 Campfire 的案例说明未言明的约束会被模型替你决定，不读代码就不思考目前还站不住；论文 U-Space 从表示层面解释不确定性从哪里来。",
 "安全与治理": "NYT 报道 Anthropic 的 agent 通过美国国务院网站提交了 20 份签证申请（均未受理）；另一位 CEO 的个人 CFO agent 把银行信息发进了公司 Slack。",
 "K8s × AI": "KAI Scheduler v0.18.5 规范 Helm OCI tag 并修 PodGroup 身份丢失；agent-sandbox v1.0.6 加入多集群 warm-pool 规划器与 TS 交互式长跑进程（含 63 字符命名的破坏性变更）；Grove alpha.14 接入 Kueue 与 KAI 调度后端，并引入 Coherent 更新引擎。",
 "K8s 核心技术": "kubectl 内部流程全拆解——client/server-side apply 的字段所有权、watch 取代轮询、JSONPath/KYAML 取数、排障顺序，以及新的 kuberc 默认配置。",
}
lines = []
for sec in b["sections"]:
    for cat in sec["categories"]:
        lines.append(f"{cat['emoji']} **{cat['title']}** — {G[cat['title']]}")
glance = "\n".join(lines)

n_items = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
n_cats = sum(len(s["categories"]) for s in b["sections"])
count_line = f"共 {len(b['highlights'])} 条重点 · {n_cats} 大板块 {n_items} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

blocks = spec["blocks"]
assert blocks[0]["type"] == "markdown" and "今日重点" in blocks[0]["content"]
assert blocks[1]["type"] == "hr"
assert blocks[2]["type"] == "markdown" and "今日看点" in blocks[2]["content"]
assert blocks[3]["type"] == "grey"
blocks[0]["content"] = "**🔥 今日重点**\n\n" + highlights
blocks[2]["content"] = "**📌 今日看点**\n\n" + glance
blocks[3]["content"] = count_line

spec["button"]["url"] = "https://endverse.github.io/daily-brief/2026/2026-10-12.html"
# title / icon / template / footer left as-is from the locked template

json.dump(spec, open("spec.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("spec.json written | chat", spec["chat_id"], "| blocks", len(blocks), "|", count_line)
