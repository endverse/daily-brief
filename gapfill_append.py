#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append gap-fill items (funnel step 3) to processed.json so verify_links accepts them."""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(ROOT, 'processed.json')
items = json.load(open(P, encoding='utf-8'))
have = {i['url'] for i in items}

new = [
 {"title": "How the Claude Code team thinks about verification",
  "url": "https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/",
  "summary": "Claude Code 团队：约 90% 代码由 Claude 写与审；给 agent 可验证的证据（E2E/属性/差分测试）才能并行跑几十上百个 agent。",
  "source": "claude.dev (HN 255)", "source_cat": "工程博客", "board": "AI 板块",
  "category": "AI 工程落地", "oss": False, "hot_score": 20, "is_hot": False},
 {"title": "opencode v2.3.1",
  "url": "https://github.com/sst/opencode/releases/tag/v2.3.1",
  "summary": "opencode v2.3.1：超时命令转后台、后台压缩默认开启、automations（cron/MCP 事件触发）、接入 GPT-6.2。",
  "source": "opencode releases", "source_cat": "GitHub Release", "board": "AI 板块",
  "category": "Agent 工具链", "oss": True, "hot_score": 18, "is_hot": False},
 {"title": "Orca v1.4.262",
  "url": "https://github.com/stablyai/orca/releases/tag/v1.4.262",
  "summary": "Orca v1.4.262：隐藏会话视图暂停刷新降内存、工作区清理删除孤儿聊天、多 Claude/Codex 账号命名与切换。",
  "source": "Orca releases", "source_cat": "GitHub Release", "board": "AI 板块",
  "category": "Agent 工具链", "oss": True, "hot_score": 17, "is_hot": False},
 {"title": "Claude Code v2.1.327",
  "url": "https://github.com/anthropics/claude-code/releases/tag/v2.1.327",
  "summary": "Claude Code v2.1.327：/status 列出坏掉的 agent/skill/command 文件、mcp add-json 从 stdin 读 token、远程 MCP 断线后台重试约一天。",
  "source": "Claude Code releases", "source_cat": "GitHub Release", "board": "AI 板块",
  "category": "Agent 工具链", "oss": False, "hot_score": 16, "is_hot": False},
 {"title": "gVisor release-20261116.0",
  "url": "https://github.com/google/gvisor/releases/tag/release-20261116.0",
  "summary": "gVisor 20261116.0：fscheckpoint 文件系统检查点格式与兼容语料、沙箱收进 device cgroup、seccomp 收紧 fallocate/accept、arm64 4K/64K 单二进制。",
  "source": "gVisor releases", "source_cat": "GitHub Release", "board": "AI 板块",
  "category": "沙箱与运行时", "oss": True, "hot_score": 18, "is_hot": False},
 {"title": "Reinforcement Learning: Optimizing 0.6B Dense Models on TPU v7 via vLLM",
  "url": "https://vllm.ai/blog/2026-11-12-rl-small-dense-tpu-v7",
  "summary": "vLLM 在 64 卡 TPU v7 上跑 Qwen3-0.6B GRPO：decode 4K→130.5K tok/s，单步 616s→369s（-40.1%），最终中位 56s/步、85% 时间在 rollout。",
  "source": "vLLM Blog", "source_cat": "工程博客", "board": "基础设施板块",
  "category": "K8s × AI", "oss": True, "hot_score": 17, "is_hot": False},
 {"title": "Kata Containers 4.4.0",
  "url": "https://github.com/kata-containers/kata-containers/releases/tag/4.4.0",
  "summary": "Kata Containers 4.4.0：runtime-rs 跨 VMM 复用 VMDK 助手、dragonball 快照恢复保留设备生命周期、kata-deploy 保留 TOML 空数组与 CRI 配置 mtime。",
  "source": "Kata Releases", "source_cat": "GitHub Release", "board": "AI 板块",
  "category": "沙箱与运行时", "oss": True, "hot_score": 12, "is_hot": False},
]
added = [n for n in new if n['url'] not in have]
items.extend(added)
json.dump(items, open(P, 'w'), ensure_ascii=False, indent=1)
print('appended', len(added), 'items; total', len(items))
for n in added: print(' +', n['title'][:60])
