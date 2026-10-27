#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 037 from the locked card template + briefing.json."""
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
    "🧠 **模型与研究** — TWIG 把每个权重写成一条离散决策路径（符号+2 的幂移位+零门+共享表索引），剪枝/量化/低秩/码本变成同一对象的编辑，幂次版还能退化成加法器电路；OPST 只给话题描述就让模型自出题自训练，文本与 VQA 都涨；扩散 LLM 做投机草稿有两个旋钮（扩散步数 + 接受松紧），联合调参能把速度-质量 Pareto 前沿推得比单步扩散更远。",
    "🧩 **Agent & Skill** — NVIDIA 开源 SkillSpector：17 类 71 种漏洞模式、0-100 风险分、SARIF 输出，引用的数据集里 31,132 个 skill 中 26.1% 含漏洞、5.2% 疑似恶意；Kolab 用 115 小时真实录屏（50 人 / 40 种职业）发现前沿模型系统性高估自己被专家采纳的程度，给更长上下文也没用；花椒复盘 30 个 Agent 落地，结论是运行时/权限/统计要抽成公共内核，业务侧只留方法与验收标准。",
    "🛠️ **AI 工程落地** — Faros AI 覆盖 1 万开发者、1255 个团队：PR 合并量 +98% 的同时审查时间 +91%，AI 采用率与企业交付指标无显著相关；对照 LF 报告的 52% 编码提速与 25% 低质量 PR，瓶颈已从写代码转到审查与集成。",
    "📊 **产品与商业** — Anthropic 递交 Form S-1，拟以代码 ANT 上 Nasdaq 全球精选市场，承销商高盛与摩根士丹利，股数与价格区间未定，注册声明尚未生效。",
    "💡 **观点与好文** — Raschka 的推理模型视频课：8 集 11 小时，从预训练 LLM 起步，用 PyTorch 手写评估、推理时扩展、强化学习与蒸馏。",
    "🛡️ **安全与治理** — 只用认证的「通过/拒绝」二元反馈就能重建受保护生物特征模板，且能做到数值精度上的完美重建，与模板保护机制无关；接人脸扩散先验后所需查询数再降 5 倍。",
    "🤖☸️ **K8s × AI** — AWS 给出 EKS 上 AI agent 的两套可观测性架构：Strands SDK 直连 Langfuse（agent 少、故障域小）vs 共享 OTel Collector（统一采样、换后端不动 agent），Bifrost 网关按 5000 QPS 自开销 <60 微秒；KAI-Scheduler v0.16.14 修 binder 更新 GPU 共享 ConfigMap 时的 nil panic。",
    "☸️ **K8s 核心技术** — Envoy v1.38.9 补 distroless 镜像的证书包（20250419~deb12u2）：10 月 23 日的 1.38.8 distroless 其实还信任被攻破的 eMudhra 中间 CA。",
    "☁️ **云原生周边** — Backstage 1.55 加 scaffolder.taskRecovery 支持从最后完成步骤续跑（要求 action 幂等，内置 DB provider 50MB 只够开发）；Terraform GCP 8.0 把 backend_service/global_forwarding_rule 默认 load_balancing_scheme 改成 EXTERNAL_MANAGED 并删掉一批下线资源；AWS 那篇 DORA 度量给了一组数据：29.6% 平台团队完全不度量、40.8% 用 DORA。",
    "☁️ **公有云动态** — GKE 把 C4D 裸金属机型（单机 384 vCPU）转 GA，1.36+ 可建裸金属节点池，1.37.0-gke.4713000 起接 autoscaler / NAP / 自定义 ComputeClass。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月27日 · 星期二",
    "{issue}": "037",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-27.html",
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
