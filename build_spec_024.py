#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 024 from briefing.json + the locked card template.
Only placeholders are substituted; title/icon/color/footer/block order untouched."""
import json, os

TPL = "/Users/endverse/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json"
COVER = "/Users/endverse/daily_brief_cover.png"
b = json.load(open("briefing.json", encoding="utf-8"))
spec = json.load(open(TPL, encoding="utf-8"))

assert os.path.exists(COVER), COVER
assert b["issue"] == 24

spec["chat_id"] = "oc_18845bcfeabb63caffa3e86c69a96d6e"
spec["header"]["subtitle"] = "2026年10月13日 · 星期二 · 第024期"
spec["cover_image"] = COVER

# highlights block: numbered bold title + summary
hl = []
for n, h in enumerate(b["highlights"], 1):
    hl.append(f"**{n}. {h['title']}**\n{h['summary']}")
highlights = "\n\n".join(hl)

# glance block: per category emoji + bold label + one sentence
G = {
 "Agent & Skill": "Open Academic Paper Gen 把论文初稿拆成九阶段多智能体工作流，引用核验分三道查（文献池存在性 → Crossref/doi.org 核对元数据 → 全文段落级判断是否支撑论点）；Google Cloud 发布 Data Agent Kit，用 MCP 工具 + Markdown Skills 把数据栈交给编码 agent；Codex CLI 默认安装自更新后台常驻进程引 430 分讨论；论文 MetaKernelBench 度量内核 agent 的经验能否跨 DSL 复用。",
 "模型与研究": "Meta 发布 Muse Wonder 系列，主打 Active Memory 与 Active Focus 的个人/职业 agentic 任务；华为 Memento 3 靠「代码即模型」在 ARC-AGI-3 上拿满分 RHAE 100、操作比人类少 56%，何恺明团队 VISTA 用无损视觉记忆在同一基准上让 Opus 5.0 全通、动作少 57.4%；智谱 GLM-Legal 在 Harvey LAB 取得 19.2% 全通过率；论文研究模型在持续学习中的「自我保存」，以及消除潜在递归模型「一圈税」的 ELR 训练法。",
 "AI 工程落地": "微软 1-bit 推理框架 BitNet 再上 Trending；MetaKernelBench 给出「沉淀下来的内核经验还有没有复用价值」的度量口径。",
 "产品与商业": "智谱 GLM-5.3-Highspeed 在 Zcode 灰度，网友实测 490 tokens/s（对照 FlashX 约 200、Flash 约 60），配 100 万上下文与三档思考强度。",
 "观点与好文": "论文系统拆解 VLM 自验证为何失效并给出多视角验证；另一篇用 4782 段真实 IDE 会话证明编码 agent 的基准与真实任务流偏离，该按用户任务流重新设计评测。",
 "安全与治理": "7 美元 ESP32 把真实 iPhone 变成 agent 的执行终端（AirPlay 当眼睛、USB HID 当手），绕过手机侧身份与权限边界的风险样本。",
 "K8s × AI": "KubeCon China 的 PD 分离 keynote 被逐层拆解——prefill/decode 分 Pod、KV cache 走 NIXL、Endpoint Picker 按前缀缓存与 KV 水位选 Pod，底层 GPU 由 HAMi 共享调度；Grove alpha.15 修掉手动扩容调度门迟到、Coherent update 死锁与 MaxUnavailable 约束过严三个故障点。",
 "K8s 核心技术": "Calico v3.33.0 大版本：CNI 可用 netkit 替代 veth（Linux 6.7+）、nftables 支持 flowtable offload、Felix 应答 ARP 实现 L2 可达、节点进程合并每节点省约 200MB、多数组件收进单镜像，BIRD 下发 IPIP 路由进入弃用；LWS v0.11.1 修 worker StatefulSet 命名冲突。",
 "云原生周边": "Google 宣布 SRE 书十周年完全重写的第二版；Kubezilla 汇总 KubeCon EU 主权议题——区分「主权代码」与「主权部署」，SNCF 在 Azure/AWS/私有 OpenStack 上跑 200+ 集群、约 30% 应用留在本地。",
 "公有云动态": "AWS 发布 Lambda Web Functions，标准 HTTP 应用一条命令上 Lambda，多并发 + 按活跃 CPU 计费成第三种形态；BigQuery 的 AI.FORECAST 升级 TimesFM 3.0，支持多变量时序预测。",
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

spec["button"]["url"] = "https://endverse.github.io/daily-brief/2026/2026-10-13.html"
# title / icon / template / footer left as-is from the locked template

json.dump(spec, open("spec.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("spec.json written | chat", spec["chat_id"], "| blocks", len(blocks), "|", count_line)
