#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 056 from the locked card template + briefing.json."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json")
b = json.load(open(os.path.join(BASE, "briefing.json"), encoding="utf-8"))
spec = json.load(open(TPL, encoding="utf-8"))

hl = []
for i, h in enumerate(b["highlights"], 1):
    hl.append(f'**{i}. {h["title"]}**\n{h["summary"]}')
highlights = "\n\n".join(hl)

# 每个分类一行，按 emoji 查文案（不手写分类名，避免与 briefing.json 不一致）
BY_EMOJI = {
 "🧠": "JustRUA 把 robot-use agent 的四项设计拆开做消融：只要「保留完整 episode 历史 + 动作提前停止」的瘦 harness，RoboDojo 就从 29.7 到 50.3；Agent-R^2 用 4k 真实语料任务训 4B，GDPval 51.0% 超过 235B 的 48.0%。",
 "🧩": "NVIDIA 开源 SkillEvaluator：静态质量门 + 「有/无 skill」两组实跑对比，把「skill 到底有没有用」变成 CI 门禁；另一篇论文用可采信证据判定超时动作是失败/已提交/在飞行，58 配对单元认证完成 30 vs 9。",
 "🧭": "Google Labs 的 stitch-skills 涨到 9.2k 星：三包 agent 插件按 Agent Skills 标准分发，Codex/Claude Code/Cursor 一套内容通用，把设计稿到组件交给 agent。",
 "🏖️": "E2B SDK 2.64.0 支持模板声明 maxCpuCount、按沙箱选 vCPU，并可用 OAuth 头认证；Kubezilla 讲清运行时层——RuntimeClass 一行声明 gVisor/Kata，SIG Apps 的 Agent Sandbox 仍是 alpha，笔记本侧 sbx 用 microVM 跑 CLI。",
 "🛠️": "Yelp 用「原生外壳 + CHAOS 服务端渲染对话区」绕开发版周期，事件里带 UI 指令；京东 11.11 把保障经验做成 5 个在京 Me 群里干活的数字人，只输出可追溯证据链。",
 "💡": "HN 千点讨论「AI 生成的代码都该开源」：语料是开源代码与 CC 授权的 SO，闭源等于洗许可；无人类作者不可版权，建议统一以开源许可或 CC0 发布。",
 "🛡️": "Claude-BugHunter：82 个 skill、15 个斜杠命令、681 条披露报告模式，覆盖 24 类核心漏洞与企业身份/基础设施攻击矩阵。",
 "🤖☸️": "给 agent 划 K8s 地盘的四件套：PSA restricted、automountServiceAccountToken=false、默认拒绝出网只放 DNS（域名级要用 Cilium FQDN 或 egress 代理）、ResourceQuota 防死循环，另封 169.254.169.254。",
}

glance_lines = []
for s in b["sections"]:
    for c in s["categories"]:
        body = BY_EMOJI.get(c.get("emoji"))
        if not body:
            continue
        glance_lines.append(f'{c["emoji"]} **{c["title"]}** — {body}')

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = (f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · "
              f"{len(b['flash'])} 条快讯 · 数据源覆盖 72 小时")

repl = {
 "{date}": "2026年11月16日 · 星期一",
 "{issue}": "056",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-16.html",
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
assert spec["header"]["title"] == "📰 AI & 基础设施早报"
assert spec["header"]["template"] == "indigo"
json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written: blocks=%d, glance=%d" % (len(spec["blocks"]), len(glance_lines)))
print(count_line)
print("footer:", spec["footer"])
