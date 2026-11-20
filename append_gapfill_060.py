#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append gap-fill candidates (funnel step 3) to processed.json for issue 060."""
import json, os

REPO = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(REPO, "processed.json")
items = json.load(open(p, encoding="utf-8"))
have = {i["url"] for i in items}

NEW = [
    dict(title="Orca v1.4.265: Introducing Orca Bots", url="https://github.com/stablyai/orca/releases/tag/v1.4.265",
         source="GitHub Releases", category="Agent 工具链", oss=True,
         summary="每个受管 agent 会话都获得自己的工具与身份，不再局限于 Claude/Codex；bot 可以像 owner 一样分享；Slack 线程显示当前 turn 在做什么；Gmail 触发器按真实发件地址匹配；新增可选自动更新。"),
    dict(title="Codex rust-v0.170.0", url="https://github.com/openai/codex/releases/tag/rust-v0.170.0",
         source="GitHub Releases", category="Agent 工具链", oss=True,
         summary="TUI 增加实时语音的 WebRTC 协商；OpenTelemetry HTTP 导出器自动刷新认证头；实验性支持跨环境同名 MCP server；修复 Windows 沙箱文件权限与权限转换丢沙箱限制的问题。"),
    dict(title="Claude Code v2.1.329", url="https://github.com/anthropics/claude-code/releases/tag/v2.1.329",
         source="GitHub Releases", category="Agent 工具链", oss=True,
         summary="Code Mode 可在开启 OpenTelemetry 事件与指标时使用；/tasks 纳入计划任务、/loop 唤醒、目标与会话分叉；/mcp 显示远端 HTTP MCP 的 JSON-RPC 错误；修复 macOS Keychain 只读导致反复登出。"),
    dict(title="Firecracker v1.18.0: Nitro Sandboxes support", url="https://github.com/firecracker-microvm/firecracker/releases/tag/v1.18.0",
         source="GitHub Releases", category="沙箱与运行时", oss=True,
         summary="新增 Nitro Sandboxes：Firecracker 可启动由 Nitro Hypervisor 从父 EC2 实例切出的隔离 VM，走 /dev/nitro_enclaves 而不是 /dev/kvm，保留原有 API、jailer 与 virtio 设备模型，新增 PUT /enclave 接口，支持 confidential 与 direct 两种模式。"),
    dict(title="gVisor release 20261116.0", url="https://github.com/gvisor/gvisor/releases/tag/release-20261116.0",
         source="GitHub Releases", category="沙箱与运行时", oss=True,
         summary="加入 fscheckpoint 语料与兼容性测试、并把 checkpoint 格式版本化文档化为 agent 可用的存档/恢复能力；sandbox 被限制进 device cgroup；seccomp 收紧 fallocate 模式；单个二进制同时支持 arm64 4K/64K 页。"),
    dict(title="Kueue v0.21.0-rc.0", url="https://github.com/kubernetes-sigs/kueue/releases/tag/v0.21.0-rc.0",
         source="GitHub Releases", category="K8s × AI", oss=True,
         summary="ConcurrentAdmission 迁移模式缺省改为 TryPreferredFlavors；拒绝受管的 LeaderWorkerSet 使用 groupIdentity: Hash（此前 leader Pod 绕过准入、worker 被门控）；Helm 新增 structuredOverrides；MultiKueue 改读 ClusterProfile v1alpha2。"),
    dict(title="Cilium 1.20.5", url="https://github.com/cilium/cilium/releases/tag/1.20.5",
         source="GitHub Releases", category="K8s 核心", oss=True,
         summary="修复 egress 策略里 toServices+toPorts 在 Service 不存在或无后端时放行任意目的地；修复 strict egress encryption 在 CIDR 含 host bits 时允许明文；修复带宽管理器在单包超时后丢弃该 Pod 全部出向流量数十秒。"),
    dict(title="Usage policies (effective November 20, 2026)", url="https://openai.com/policies/usage-policies",
         source="OpenAI", category="平台政策与风控", oss=False,
         summary="新版使用政策 11 月 20 日生效：运营模型路由器/AI 网关等「让第三方直接访问模型」的中介平台须事先获得 OpenAI 审核批准；把模型集成进自家功能的应用不受此条约束；禁止用输出训练竞品模型、禁止提取受保护推理过程；引入 SafetyIDs。"),
    dict(title="Release v0.70.0", url="https://github.com/google-gemini/gemini-cli/releases/tag/v0.70.0",
         source="GitHub Releases", category="Agent 工具链", oss=True,
         summary="修复 Unicode 提示与会话预览中的 ANSI 片段、认证重启后保留 worktree、模型列表准确报告输出 token 上限；策略参数匹配改用 re2js 做线性时间求值。"),
    dict(title="e2b@2.64.0", url="https://github.com/e2b-dev/E2B/releases/tag/e2b%402.64.0",
         source="GitHub Releases", category="沙箱与运行时", oss=True,
         summary="Sandbox SDK 与 CLI（@e2b/cli 2.24.0、code-interpreter 2.11.10）同步发布 2.64.0。"),
]

added = 0
for n in NEW:
    if n["url"] in have:
        print("skip existing:", n["title"])
        continue
    n.setdefault("detail", None)
    items.append(n)
    have.add(n["url"])
    added += 1

json.dump(items, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"appended {added}, processed.json now {len(items)} items")
