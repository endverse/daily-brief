#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 042 from the locked card template + briefing.json."""
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
    "🧠 **模型与研究** — EasyProver 不训练模型就证出 PutnamBench 669/672、IMO 2026 全部 6 题；统一训练把预训练/SFT/RL 收进一个似然目标；AIR 指出该调度有效学习率，128B MoE 末端 loss 比 cosine 低约 0.01；Youtu-Parsing-Omni 用 5B 单模型统一文档/图像/音频/视频解析，OmniDocBench 96.96。",
    "🧩 **Agent & Skill** — REA 用 MCP 把 Ghidra/Hopper/IDA 接给编码 agent，20 万 star，DX-Ball 反编译对上 3205 条 x86 用例；stack-diagram 把「一句描述出架构图」做成 349 star 的 agent skill。",
    "🛠️ **AI 工程落地** — Grafana 把幻觉/完成度做成 SLI + SLO + 错误预算（30 天 95% 对话算完成）；Nolan Lawson 让 9 个前端框架各建 5 次站，SvelteKit/Gracile+Lit/Angular 的 agent 建站成本明显更高。",
    "📊 **产品与商业** — 新芯航途首发 X7 Ultra 车规 SoC：700 TOPS、NPU 利用率 98.7%、量化输出与 FP32 相似度 99.99%，用 Momenta R7 世界模型当跑分。",
    "💡 **观点与好文** — 毕玄复盘 SREAgent：让 agent 跑长任务、用熟通用工具正在变成模型自身能力，靠补短板撑不起垂类 Agent 的长期竞争力，壁垒在专有数据的接入与业务建模。",
    "🛡️ **安全与治理** — OpenAI 认共享 robots.txt 信号 __usage_ai-training，一个 token 对多厂商声明训练偏好（Google/Microsoft 同表态）；AiSOC 给每个 agent 步骤留可回放决策账本；Anthropic 在 Opus 5.5 系统提示里禁「复刻现有游戏」，误伤原创项目。",
    "🤖☸️ **K8s × AI** — Kubeflow Trainer v2.4.0-rc.0 用 OptimizationJob CRD 收编 Katib 的 HPO，并修掉 helm uninstall 会连带 GC 全部 TrainJob 的坑；Kubezilla 讲透 GPU 监控为什么难：DCGM Exporter 靠 pod-resources API 把指标挂到 Pod 上。",
    "☸️ **K8s 核心技术** — Gateway API v1.7.0 把 HTTPRoute 重试提升到 Standard，新增 XTelemetryPolicy（OTel 语义追踪）、pre-routing filter、ClusterTrustBundle 引用；metrics-server v0.9.1 重建镜像剔除 eMudhra 根证书。",
    "🌐 **云原生周边** — OTel Collector v0.164.0 让 otlp_http 报错给出真实目标 URL，OpAMP 上报原始配置时脱敏环境变量字面默认值。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年11月02日 · 星期一",
    "{issue}": "042",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-02.html",
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
for ph in ["{date}", "{issue}", "{cover}", "{highlights}", "{glance}", "{count_line}", "{page_url}"]:
    assert ph not in blob, "leftover placeholder: " + ph
assert spec["chat_id"] == "oc_18845bcfeabb63caffa3e86c69a96d6e"
assert spec["header"]["template"] == "indigo" and spec["header"]["icon"] == "myai_colorful"

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, highlights=%d chars" % (len(spec["blocks"]), len(highlights)))
