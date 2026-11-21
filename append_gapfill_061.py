#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append gap-fill candidates (funnel step 3) to processed.json for issue 061."""
import json, os

REPO = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(REPO, "processed.json")
items = json.load(open(p, encoding="utf-8"))
have = {i["url"] for i in items}

NEW = [
    dict(title="Agent Sandbox v1.0.12: SDK 全面支持 suspend/resume，空闲沙箱释放 Pod 但保留 claim 与 PV",
         url="https://github.com/kubernetes-sigs/agent-sandbox/releases/tag/v1.0.12",
         source="GitHub Releases", category="沙箱与运行时", oss=True,
         summary="kubernetes-sigs 的 Agent Sandbox 在 11 月 20 日发布 v1.0.12，核心是跨 Go/Python/TypeScript 三个 SDK 的 suspend()/resume()：改 spec.operatingMode 释放 Pod，但保留 SandboxClaim 与持久卷，UID guard 防止并发打错对象。另加 SandboxWarmPool 的 per-pool readinessGracePeriodSeconds（最小 30 秒，默认 5 分钟）、sandbox-router 的 Ed25519 沙箱级 v2 token、sandboxd 的 files.stat()?stat=true 单路径元数据。新增 CI runner sandbox 与 Claude Code proxy/suspend-resume 两个示例。"),
    dict(title="Inkling 2 Mini：循环 Transformer 把中间层跑三遍，百亿级开源权重在笔记本上跑出 agentic coding 新前列",
         url="https://thinkingmachines.ai/news/inkling-2-mini/",
         source="Thinking Machines Lab", category="模型与研究", oss=True,
         summary="Thinking Machines 11 月 20 日发布 Inkling 2 Mini：一个 looped transformer，每个 token 把模型中间层重复跑三次，用更少的 token 换更多推理。总参数在 100B 以下，官方称在 DeepSWE v1.1 拿到 48.2%、Vals Index v2.2 拿到 46.5%，是 100B 以下开源权重里的最好成绩，且跑得比同级模型快；权重在 Hugging Face，可通过 Tinker 调用。"),
    dict(title="Claude Code v2.1.330: 企业管理员控制台登录、内置 easel 图表 mod、自托管 runner 指标",
         url="https://github.com/anthropics/claude-code/releases/tag/v2.1.330",
         source="GitHub Releases", category="Agent 工具链", oss=True,
         summary="Claude Code 11 月 20 日发布 v2.1.330。新增对 Anthropic Enterprise Admin Console 管理组织的登录支持：claude auth login 之后自动套用组织设置、走组织的云厂商或网关。内置 easel mod 可按要求画图表，并画在 MCP 指标结果下面（Pro/Max 与部分 Team/Enterprise，macOS 与 Linux）。自托管 runner 增加 --start-dir 与 order→registered / order→first-session 两个指标。修复长对话 compact 后卡死数分钟、WebFetch 卡住、多进程并发写设置丢失、子 agent 声明的 MCP server 被提前关闭等一批问题。"),
    dict(title="Codex rust-v0.171.0: 模型目录加入 GPT-6.2 Sol / Astra，TUI 工作区默认打开",
         url="https://github.com/openai/codex/releases/tag/rust-v0.171.0",
         source="GitHub Releases", category="Agent 工具链", oss=True,
         summary="Codex 11 月 20 日发布 0.171.0：模型目录加入 GPT-6.2 Sol 与 Astra，Sol 成为默认目录选项；TUI 工作区默认启用，主对话旁可并排看可搜索的文档预览、图片预览与子 agent 转录。新增 codex exec --remote <ADDR> 在已有 app server 上开/续非交互会话，/rc 与 /remote 管理本地远控与设备配对码。修复切换会话时草稿与排队 follow-up 丢失、权限 profile 换目录后失效、滚动插字与光标跳等问题。"),
    dict(title="Kueue v0.21.0-rc.1: DRA 优先级列表与可消费容量配额升 Beta，拒绝受管的 LWS groupIdentity: Hash",
         url="https://github.com/kubernetes-sigs/kueue/releases/tag/v0.21.0-rc.1",
         source="GitHub Releases", category="K8s × AI", oss=True,
         summary="Kueue 11 月 20 日发 v0.21.0-rc.1：DRA 的 KueueDRAIntegrationPrioritizedList 升 Beta 并默认开启，调度时会把 firstAvailable 请求的 CEL 选择器与集群内实际设备比对；DRA 可消费容量配额（consumable capacity）也升 Beta，DeviceClass 的容量维度可用独立配额资源计费，并在请求取整导致多收费时给出报告。Kueue 现在拒绝受管的 LeaderWorkerSet 使用 spec.groupIdentity: Hash——此前该模式下 leader Pod 绕过准入、worker 一直被门控。Helm 增加 managerConfig.structuredOverrides。"),
]

added = 0
for n in NEW:
    if n["url"] in have:
        print("skip existing:", n["title"][:40])
        continue
    n.setdefault("detail", None)
    items.append(n)
    have.add(n["url"])
    added += 1

json.dump(items, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"appended {added}, processed.json now {len(items)} items")
