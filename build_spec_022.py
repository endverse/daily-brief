#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 022 from briefing.json + the locked card template.
Only placeholders are substituted; title/icon/color/footer/block order untouched."""
import json, os

TPL = "/Users/endverse/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json"
COVER = "/Users/endverse/daily_brief_cover.png"
b = json.load(open("briefing.json", encoding="utf-8"))
spec = json.load(open(TPL, encoding="utf-8"))

assert os.path.exists(COVER), COVER
assert b["issue"] == 22

spec["chat_id"] = "oc_18845bcfeabb63caffa3e86c69a96d6e"
spec["header"]["subtitle"] = "2026年10月11日 · 星期日 · 第022期"
spec["cover_image"] = COVER

# highlights block: numbered bold title + summary
hl = []
for n, h in enumerate(b["highlights"], 1):
    hl.append(f"**{n}. {h['title']}**\n{h['summary']}")
highlights = "\n\n".join(hl)

# glance block: per category emoji + bold label + one sentence
G = {
 "Agent & Skill": "Karpathy 的 LLM 写码坑被固化成一份 CLAUDE.md；Claude Code 团队称静态指令文件以后可能都不用写；Google Data Agent Kit 转 GA，把 15+ 数据服务接进编码 agent；另有 REMORY 软记忆 token 与 SGUID 的 skill 效用筛选两篇论文。",
 "模型与研究": "GPT-6.1 Sol 新增 Ultrafast 档位，Token 单价为标准模式的 6 倍；论文重算 METR 时间跨度、指出线性外推会系统性高估能力；另有两篇空间推理基准与机器人推理配方。",
 "AI 工程落地": "腾讯云分享 AI Native SRE Agent：以全景运行图谱支撑运行态的可理解/可操作/可验证；QCon 上海预告「AI 降低了生成成本，却没降低正确性交付成本」；论文提出深度研究报告的增量更新框架。",
 "产品与商业": "OpenAI 在 DevDay 发布 Decisions API（用最小的 GPT-6 Luna 从预设选项中作答，150 毫秒），被指直接冲击 Jev；开源 ppt-master 能把文档转成原生可编辑 PPT。",
 "观点与好文": "AI 开源的评价标准正从「开放了什么」转向「能力能否被验证与复用」；另有密码学家对「AI 制造意外的速度远快于标准替换速度」的风险判断。",
 "安全与治理": "金融监管报送场景的约束式 agent 实践：知识底座 + 数据底座 + 受控状态机 + 全链路可追溯，做到「宁可不答、不能答错」；论文复盘 2026 年三起 agent 越界事故，并用探针把欺骗检测做到 98.8% AUC。",
 "K8s × AI": "vLLM v0.31.0 用权重常驻 + CRIU 快照压缩重启成本；llm-d v0.10 硬化生产路径并改用 cosign 签名镜像；Kueue v0.20 移除 v1beta1 API、公平共享相关变更默认开启；KServe v0.21 让 ServingRuntime 接上 DRA；GKE Pod 快照把 70B 模型加载压到 37 秒。",
 "K8s 核心技术": "官方明确 cgroup v1 已弃用，v1.35 起 cgroup v1 节点上 kubelet 默认启动失败；Gateway API v1.7 候选版把 HTTPRoute 重试配置升入 Standard 通道。",
 "社区与项目": "KubeCon 北美 2026 新增 Platform Engineering Day，并发布面向基础设施工程师的参会路线，重心继续向 AI 负载倾斜。",
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

spec["button"]["url"] = "https://endverse.github.io/daily-brief/2026/2026-10-11.html"
# title / icon / template / footer left as-is from the locked template

json.dump(spec, open("spec.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("spec.json written | chat", spec["chat_id"], "| blocks", len(blocks), "|", count_line)
