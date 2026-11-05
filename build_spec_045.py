#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 045 from the locked card template + briefing.json."""
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
 "🧠 **模型与研究** — 论文实测长上下文后段 token 成本可达 7 倍、频繁压缩几乎不掉点；投机解码的数值噪声会改变 30 步后的 agent 推理分布。",
 "🧩 **Agent & Skill** — 谷歌 Data Agent Kit GA：37 个技能做引导、IAM 拒绝策略做强制；Harbor 把每个 agent 评测任务放进独立内核的 microVM；openJiuwen 用视听双流按事件组织长视频记忆。",
 "🛠️ **AI 工程落地** — TokenSpeed 按 agent 负载重写推理引擎，128K→1M 解码吞吐只降 16%；哈佛 718 家企业研究：代码 +30% 但工单只 +12%、评审时长 +49%。",
 "📊 **产品与商业** — OpenAI 收购 Pierre 补 Codex 的代码存储与 diff；Images 2.6 支持 GIF 与逐帧编辑；腾讯云把 agent 能力收进 AgentHosting。",
 "🛡️ **安全与治理** — OpenAI 流水线一轮复现 1,724 个漏洞、其中 948 个内核提权；Anthropic OSS Scanner 六个月 2.9 万潜在漏洞、人工只审约 6,000。",
 "🤖☸️ **K8s × AI** — HAMi 2.11.0 补 Flexible-MIG、Cluster Autoscaler 与 Remote CUDA，整卡分配改由 NVML 出指标。",
 "☸️ **K8s 核心技术** — CoreDNS 1.15.0 支持 DoQ 上游并修 7 个 CVE；etcd 3.7.3 修 MVCC 与 RangeStream 数据竞争。",
 "🌐 **云原生周边** — Argo CD 3.6.1 修侧栏布局与子路径部署下 --rootpath 失效。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年11月05日 · 星期四",
 "{issue}": "045",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-05.html",
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
json.dump(spec, open(os.path.join(BASE, "spec.json"), "w"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, glance=%d, count_line=%s" % (len(spec["blocks"]), len(glance_lines), count_line))
