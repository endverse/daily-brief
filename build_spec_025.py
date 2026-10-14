#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 025 from the locked card template + briefing.json."""
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
 "🧩 **Agent & Skill** — Anthropic 给 Managed Agents 上线动态工作流：把多 agent 编排写成可执行程序，边界是累计 1000 个 agent / 64 并发 / 24 小时；machine-skill 用一行描述生成跑真实物理的仿真；vercel-labs/skills 一条 npx 命令跨 80+ 编码 agent 装 skill。",
 "🧠 **模型与研究** — 面壁开源 MiniCPM-V 4.7：35B-A3B 在断网 iPhone 上只占约 3G 内存、13 token/s；论文 Thinking Inertia 证明「关掉思考模式」不等于停止推理；同一份输出换一套 gold 就能移动多语言基准分数。",
 "🛠️ **AI 工程落地** — Python 3.15 内置采样 profiler 定位 web-edit 热点（64.8% 栈在混合行尾保留，95.1% 栈来自工作线程），优化由另一个模型照报告完成；高通把 Snapdragon X2 的 Linux 支持提前推进上游主线，NPU 走上游 FastRPC。",
 "📊 **产品与商业** — 千问 AI 眼镜 N1 Pro 支持体征监测与虹膜核身支付（官方称误识率低于百万分之一）；魔法原子 EchoPolicy-0 以 75.4% 操作成功率拿下 MolmoSpaces 零样本榜单全球第一。",
 "💡 **观点与好文** — Armature 用 17000 次工具选择会话说明 agent 选型让厂商二十年品牌建设失效；一篇 HN 记录发帖后个人站被 AI 爬虫流量淹没。",
 "🛡️ **安全与治理** — 补丁 PR 提交后数分钟就出现匹配探测：拿到 CVE 描述时 GPT-4 agent 对基准 15 个漏洞的利用率达 87%，无描述时只有 7%。",
 "🤖☸️ **K8s × AI** — DRA GPU 驱动 v0.5.1 修 ComputeDomain 竞态与 kubelet 重复报错；Dynamo v1.5.1 修 K8s 上 RL worker 发现失败；SGLang v0.5.21 的 PD 角色可免重启切换并默认用 Rust 前缀缓存。",
 "☸️ **K8s 核心技术** — containerd 同一天发布四条维护线补丁（含 CVE-2026-95839），并修镜像拉取时下载快于写入导致的内存暴涨。",
 "🧩 **云原生周边** — BuildKit v0.34.0 支持 BoltDB 压实；Envoy 1.40.0 把 HTTP/3 与 QUIC 转稳定、默认启用后量子混合密钥交换，并开始按 OpenAI/Anthropic/Gemini 方言提取 LLM token 用量。",
 "☁️ **公有云动态** — Google Cloud 的 U4 机器族与超低延迟方案 GA，面向云上高频交易；AWS 周报汇总 Prime Day 2026 容量数据、Claude Haiku 5.5 与 Nova 2.5 Sonic。",
]

n_sec = sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
count_line = f"共 {len(b['highlights'])} 条重点 · {len(glance_lines)} 大板块 {n_sec} 条精选 · {len(b['flash'])} 条快讯 · 数据源覆盖 72 小时"

repl = {
 "{date}": "2026年10月14日 · 星期三",
 "{issue}": "025",
 "{cover}": "/Users/endverse/daily_brief_cover.png",
 "{highlights}": highlights,
 "{glance}": "\n".join(glance_lines),
 "{count_line}": count_line,
 "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-10-14.html",
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

# no placeholders may survive (except the _comment documentation line)
blob = json.dumps({k: v for k, v in spec.items() if k != "_comment"}, ensure_ascii=False)
for k in repl:
    assert k not in blob, f"unfilled placeholder {k}"

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("spec.json written |", spec["header"]["subtitle"], "|", spec["button"]["url"])
print("count_line:", count_line)
