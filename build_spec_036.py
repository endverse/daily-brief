#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 036 from the locked card template + briefing.json."""
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
    "🧠 **模型与研究** — HyperDrone 把多旋翼动力学 + 光追渲染全放 GPU，批量仿真比同行走快 20 倍、消费级卡上百万 FPS，纯仿真训练的偏航策略直接上 Crazyflie；微信开源 WeVisOne-VL，用 <OBJ> token 接轻量像素解码器统一检测/分割/matting；扩散 LM 成本按前向次数算，写故事每 token 是语法纠错的 3 倍以上。",
    "🧩 **Agent & Skill** — TradingAgents v0.7.0（约 11.4 万星）可用自己的 ChatGPT Plus/Pro 跑，回测按决策后首个收盘价结算；claude-seo 用 26 个子 skill + 19 个子 agent 做 SEO 审计，1077 个测试全过；Heartbeat Thinking 心跳式投机执行让语音 agent 工具覆盖 +16pp、末响应延迟降 36.4%。",
    "🛠️ **AI 工程落地** — Cerebras 拆解 3 万亿参数模型的铺法：4bit 权重、每片 44GB 片上内存、dense 层一片一层留 KV cache、线性层两片一层，共 59 片 WSE-3T，晶圆间只传激活、RDMA 每跳约 2 微秒。",
    "📊 **产品与商业** — Anthropic 承诺 5% 股份进公共福利基金，估值每涨 50% 可再追加 2%，刻意用 LLC 保持分配形式灵活，并写明不用于游说与政治献金。",
    "🛡️ **安全与治理** — LLM-Attack Suite 统一拆分式 LLM 的隐私红队口径：GPT-2 上加入训练梯度后 token 恢复率 94.2%→97.4%、整文档精确恢复 13.7%→37.8%，并要求防御附未防御对照基线。",
    "🤖☸️ **K8s × AI** — Kyverno 把策略从准入推到内核：BPF-LSM 挂 bprm_check_security/file_open、按 Pod 挂 cgroup eBPF 管出口，出口按应用层协议而非端口判定；GPU 共享四条路线对照（MIG 硬隔离 / time-slicing 无隔离 / MPS 仍 experimental / DRA 需 1.34.2+）。",
    "☁️ **云原生周边** — OTel Collector 裁剪 Claude Code 遥测：一次小任务 181 条记录 289KB，删 api_request 与六个属性、哈希 session/user、指标去维度后 300 条时序变 12 条，与原始管道总量差 <0.5%。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月26日 · 星期一",
    "{issue}": "036",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-26.html",
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
