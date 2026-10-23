#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 031 from the locked card template + briefing.json."""
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
    "🧩 **Agent & Skill** — 腾讯测试 Agent 用「知识库/脚本/执行产物」三层数据替代提示词堆砌，失败按证据归因后自动升版；HarnessPro 用 Pareto 选型换到 +2.0pp 通过率与 -26.1% 单任务成本，而 Harness-Delta 归因发现这类收益里 54% 是评测集过拟合。",
    "🧠 **模型与研究** — MemT-1.0 把记忆做进计算，128K 历史下推理快 1.86 倍、持久化存储省 66 倍；MiniMax M3.1 Flash 价格是 Opus 5.5 的 1/88 却在 Agent 与 AA 榜双第一。",
    "🛠️ **AI 工程落地** — Alaya-DFlash2 用推测解码让 GLM-5.3 长文解码 3.41 倍（288.2 vs 84.5 tokens/s）；300 位工程负责人调查显示写码 9.8h、调试 16.9h，79% 认为发布并没变快。",
    "📊 **产品与商业** — OpenAI 收购 Orchestra Bio 把 AI 运营带进生命科学研发；一家连锁加盟商用 ChatGPT Work 把现金对账时间砍掉 94%。",
    "💡 **观点与好文** — 首席架构师的 5 条反常识原则：骨架自己搭、主 Agent 禁改代码、看不懂就扔；另有「发假统计被 LLM 引用」的实操复盘。",
    "🛡️ **安全与治理** — Anthropic 称蒸馏攻击发生率降 90%+；CyberArena 让两个 agent 同场对称攻防，12 个前沿模型打了 466 场。",
    "🤖☸️ **K8s × AI** — llm-d 1.0 已在重点里；TorchTPU 开源让 TPU 成为 PyTorch 原生后端，Transformers v5 里 device_map=\"tpu\" 即可。",
    "☸️ **K8s 核心技术** — BuildKit 0.34.1 因吊销 eMudhra 中间 CA，会让依赖旧证书链的镜像拉取/推送直接 TLS 失败。",
    "🧰 **云原生周边** — Nirmata Runtime for Kyverno 用 BPF-LSM 把策略从准入推进到运行时，拦截 exec/file_open/egress 与内核同步。",
    "☁️ **公有云动态** — GDC air-gapped 把 Gemini 企业搜索、开源权重模型与新 IaaS 栈搬进离网环境；AWS 推出账号级 ECS Gateway。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月21日 · 星期三",
    "{issue}": "031",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-21.html",
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
