#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 028 from the locked card template + briefing.json."""
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
    "🧩 **Agent & Skill** — Google Cloud 四条评测教训：11 条 prompt 里 3 条被 LLM-as-judge 误判；Orca 把同一 prompt 扇出五个 agent 各跑独立 worktree；Stack Overflow for Agents 两人几周做完，插件带来 10 倍 agent 创建量。",
    "🧠 **模型与研究** — DeepSeek-V4.1-Flash-1017 放出（MIT、多模态、HN 672 分，搜索端点免费到 10-31）；OmniVerifier-C1 把视觉验证器从真假二分类改成按规则拆解逐项打分；优必选 Thinker-WM 称拿下三大具身世界模型基准第一。",
    "🛠️ **AI 工程落地** — FlashMask-3 在 Hopper 上做 mask-aware 分布式 attention，118B MoE 128K 训练吞吐 +7.3–11.0%；模域 ModelSphere 以 Apache 2.0 开源、统一纳管国产卡；Akka 用 65 个项目验证规格驱动移植（99.3 小时、94.1 亿 token、57/65 有改善）。",
    "📊 **产品与商业** — Barclays 目标年底 Claude Code 覆盖 50% 开发者；Benefit Street Partners 用 Codex 造贷款估值与信贷分析工具。",
    "💡 **观点与好文** — Google Cloud 的 SAVE 方法：把研究与创作拆成两个角色，别让一个 prompt 同时求真与求好看。",
    "🛡️ **安全与治理** — Anthropic 把 Glasswing 与 CVP 合并成三档权限，验证团队可用 Opus 5.5 / Mythos 5.1；Itaú 30 万客户在用 ia.i，IARA 统一管模型访问、token 成本与责任 AI 策略。",
    "🤖☸️ **K8s × AI** — kagent alpha14 用 Substrate image volumes 挂载 OCI 形式的 skill、会话挂起改数据快照；HAMi 在 KubeCon China 主张「先调度、再切分」，动态 MIG 跟着调度走。",
    "☸️ **K8s 核心技术** — Karpenter v1.15.0 支持 DRA 候选设备优先级回退、新增 VPA 预测控制器；Cluster API v1.14.3 管理集群支持到 K8s v1.37 并修 KCP 代理竞态。",
    "📦 **社区与项目** — Argo CD v3.5.5 修 reposerver 陈旧 manifest 与 goroutine 泄漏；OTel Collector v0.163.0 修 block_on_overflow 死锁、抓取成本从 O(n²) 降到 O(n)。",
    "☁️ **公有云动态** — Azure Databricks Private network gateway 公预览，serverless 经单一托管网关访问 VNet；Cloud Run 用 worker pools 按需求预扩容跑 Temporal worker。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月18日 · 星期日",
    "{issue}": "028",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-18.html",
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

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written |", spec["header"]["subtitle"], "|", spec["button"]["url"])
print("count_line:", count_line)
