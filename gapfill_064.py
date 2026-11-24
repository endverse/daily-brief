#!/usr/bin/env python3
"""gap-fill: 把定向补搜到的新条目追加进 processed.dedup.json 与 processed.json"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

gap = [
 {
  "title": "Codex CLI 0.172.0",
  "url": "https://github.com/openai/codex/releases/tag/rust-v0.172.0",
  "summary": "### New Features ...",
  "published": "2026-11-24T00:06:41Z",
  "source": "GitHub Releases",
  "source_cat": "Agent 工具链",
  "extra": {}, "board": "AI 板块", "category": "Agent 工具链",
  "oss": True, "hot_score": 18, "is_hot": False
 },
 {
  "title": "Claude Code v2.1.331",
  "url": "https://github.com/anthropics/claude-code/releases/tag/v2.1.331",
  "summary": "### What's changed ...",
  "published": "2026-11-23T21:34:41Z",
  "source": "GitHub Releases",
  "source_cat": "Agent 工具链",
  "extra": {}, "board": "AI 板块", "category": "Agent 工具链",
  "oss": True, "hot_score": 17, "is_hot": False
 },
 {
  "title": "Abundant runs two million sandboxes a month on Modal",
  "url": "https://modal.com/blog/abundant-efficient-rollout-architecture-with-modal-sandboxes",
  "summary": "Abundant builds RL environments...",
  "published": "2026-11-19T12:00:00Z",
  "source": "Modal Blog",
  "source_cat": "沙箱与运行时",
  "extra": {}, "board": "AI 板块", "category": "沙箱与运行时",
  "oss": False, "hot_score": 19, "is_hot": False
 },
 {
  "title": "Skip the DRAM tier: NVMe KV cache pools for agentic serving",
  "url": "https://vllm.ai/blog/2026-11-23-skip-the-dram-tier",
  "summary": "Most traffic in agentic serving is multi-turn sessions...",
  "published": "2026-11-23T00:00:00Z",
  "source": "vLLM Blog",
  "source_cat": "K8s × AI",
  "extra": {}, "board": "基础设施", "category": "K8s × AI",
  "oss": False, "hot_score": 18, "is_hot": False
 },
 {
  "title": "Kueue v0.21.0-rc.1",
  "url": "https://github.com/kubernetes-sigs/kueue/releases/tag/v0.21.0-rc.1",
  "summary": "Changes since v0.20.0 ...",
  "published": "2026-11-20T18:04:57Z",
  "source": "GitHub Releases",
  "source_cat": "K8s × AI",
  "extra": {}, "board": "基础设施", "category": "K8s × AI",
  "oss": True, "hot_score": 15, "is_hot": False
 },
 {
  "title": "Understanding ChatGPT and Codex usage limits",
  "url": "https://help.openai.com/en/articles/20001625-understanding-chatgpt-and-codex-usage-limits",
  "summary": "Starting in December, Plus, Pro, and Business plans' usage allowance will be shared across ChatGPT and Codex.",
  "published": "2026-10-31T00:00:00Z",
  "source": "OpenAI Help Center",
  "source_cat": "平台政策",
  "extra": {}, "board": "AI 板块", "category": "平台政策与风控",
  "oss": False, "hot_score": 16, "is_hot": False
 },
]

# 追加到 processed.json（校验源）与 processed.dedup.json（编辑用）
for fn in ("processed.json", "processed.dedup.json"):
    items = json.load(open(fn, encoding="utf-8"))
    have = {i["url"] for i in items}
    added = 0
    for g in gap:
        if g["url"] not in have:
            items.append(dict(g)); added += 1
    json.dump(items, open(fn, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{fn}: +{added} → {len(items)} 条")
