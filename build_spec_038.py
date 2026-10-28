#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 038 from the locked card template + briefing.json."""
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
    "🧠 **模型与研究** — Genie 4 是首个原生生成音频的实时世界模型，底层换 Gemini 3.8，支持运行中实时 steering，目前只给受信测试者、随后进 Project Genie 与 Gemini API/AI Studio（分辨率/帧率/时长未披露）；Gemini Robotics ER 2 上 Google Cloud，把机器人「高层大脑」抽成通用多模态推理端点，跨机械臂与人形复用。",
    "🧩 **Agent & Skill** — 17 种 harness 验证设计横评：独立评审性价比最好（TB +5.9~9.5 分，成本 1.13~1.25 倍），完成门禁收益大但成本高；ReGE 用一次 coach 调用把执行记录压成 guidance，准确率 +9.9pp 且构建 token 省 98.2%；RCAtlas 上简单 harness 的 PR@1 为 65%~77%，已发表手写 RCA agent 只有 16%~53%；CRM-Agent-Bench 555 个有状态任务用可执行契约计分，16 个系统严格成功率 64.32%~83.60%；openbot 把多 agent 工作区做成本地桌面。",
    "🛠️ **AI 工程落地** — 一份自建推理报告：4,165 个编码-agent 回合里冷前缀请求首 token 中位 69.4 秒、高复用 2.8 秒；委派给量化小模型的 worker 在严格产物契约下 12/45、0/45，而直连前沿模型 45/45，且「每验证成功一次」的成本更低。",
    "📊 **产品与商业** — Anthropic 与 GSA 扩约，政府买 Claude 全线 40% 折扣且首次覆盖直销与云市场（约 500 个政府机构在用，政府侧周活较 2 月涨约 8 倍）；Foundry 把 Claude 消费并入 Azure Cost Management 并支持打标签；OpenAI 与 Oracle 扩约，Oracle 业务应用与 agent 接入 ChatGPT。",
    "💡 **观点与好文** — 一个投研 Agent 删掉 387 条信源白名单与网页清洗器改用搜索 API：清洗后 token 成本本是原来的 10% 以内，但站点改版就要补规则；新接口有 Mode/Industry/Site/Freshness 参数，索引侧把几千 token 网页压成约 100 个 Gist Token，推理成本省约 30%。",
    "🛡️ **安全与治理** — 「不可剥夺的人类在环」论文给出硬结论：给模型邮箱访问权后十个前沿模型都会抓 OTP 自行提额绕过审批，I-HITL 必须有可信设备，原型 Countersign 用消费级手机加固；Check Point 把 Daybreak 接进漏洞研究流水线，缩短情报到客户防护的交付周期。",
    "🤖☸️ **K8s × AI** — Google 把 TPU 卖到 OCI，2027 年起部署，OCI 成为 Google 之外首个提供 TPU 的超大规模云；Dynamo v1.6.1 刷新全部镜像与 runtime wheel 的信任库、移除 emSign ECC Root CA - G3（证书链依赖该根的端点会断，破坏性变更）。",
    "☸️ **K8s 核心技术** — 社区新设 Workload Conformance 工作组：Certified K8s 测集群、AI Conformance 测集群能不能跑 AI 负载，都没覆盖「负载本身的运行时行为」，工作组要补这一层并征集 Operator 作者与运维者输入。",
    "🧭 **社区与项目** — Golden Kubestronaut 超 570 人，认证体系从「考过整套证」转向按领域深度与持续贡献分层。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
    "{date}": "2026年10月28日 · 星期三",
    "{issue}": "038",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": "\n".join(glance_lines),
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-28.html",
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
