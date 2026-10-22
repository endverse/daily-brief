#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 032 from the locked card template + briefing.json."""
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
    "🧩 **Agent & Skill** — Cloudflare 开源 Clef 决策模型，9B 版一次前向输出各选项概率、中位延迟 38.8ms；HarnessAdapt-RL 让 harness 与策略一起进化，9B 模型在 SWE-bench Verified 比 GRPO 高 9.8 个点。",
    "🛠️ **AI 工程落地** — OpenAI 的 COBOL 迁移评测把「逐字节一致」当判据，GPT-6.1 Sol 从 5.4% 升到 97.9%；Cache Engineering 让 agent 直接 drop/repos KV cache，成本降 27.7% 还不触发重算。",
    "🧠 **模型与研究** — 16 个开源模型的闭卷错误里有相当一部分是「首个 token 选错」，喂对第一个 token 能纠正两成到五成的错误。",
    "📊 **产品与商业** — Anthropic 上线主动式 agent 应用 Claude Duet（Opus 5.5、6000+ 连接器）；Google Cloud 把 OpenAI 模型上架 Model Garden。",
    "🛡️ **安全与治理** — Patch the Planet 用 Codex + 安全工程师在 19 个开源项目跑完整闭环，已合并数十个补丁。",
    "💡 **观点与好文** — Andy Pavlo：Agent 删库不是新问题，是数据库护栏没接进工具链，权限与回滚几十年前就有了。",
    "🤖☸️ **K8s × AI** — SREGym 50 个注入故障实测：agent 只读上下文后 2 分钟内诊断达标率 60%→86%；GKE Inference Gateway + llm-d 把 ZenteiQ 批量推理吞吐拉到 4.07 倍。",
    "☸️ **K8s 核心技术** — Volcano 1.16 引入 NamespaceQueue 与 fairshare 插件、HyperNode 独立控制器与 Unschedulable Job Cache；containerd 2.4.2 修 3 个安全通告。",
    "☁️ **公有云动态** — 空隔区 ECR 用仓库创建模板把 CMEK、不可变标签、扫描固化成默认；Confidential G4 机密 GPU 正式 GA。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月22日 · 星期四",
    "{issue}": "032",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-22.html",
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
assert "oc_bf5fe15d7eef9babda1d709cc085f641" not in blob

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written |", spec["header"]["subtitle"], "|", spec["button"]["url"])
print("count_line:", count_line)
