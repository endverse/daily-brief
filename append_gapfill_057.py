#!/usr/bin/env python3
"""Append funnel-step-③ gap-fill items to processed.json (issue 057)."""
import json

P = "processed.json"
d = json.load(open(P))
have = {i["url"] for i in d}

add = [
    {
        "title": "Claude Code v2.1.326",
        "url": "https://github.com/anthropics/claude-code/releases/tag/v2.1.326",
        "summary": "Claude Code 2.1.326：agent teams 开启时默认进入 Code Mode，/status 显示被关闭的功能项，新增 OTEL_RESOURCE_INCLUDE_HOST。",
        "published": "2026-11-16T00:00:00+00:00",
        "source": "GitHub Releases",
        "source_cat": "AI-工具链",
        "extra": {},
        "board": "AI 板块",
        "category": "Agent 工具链",
        "oss": False,
        "hot_score": 0,
        "is_hot": False,
    },
    {
        "title": "Istio 1.32.0 release notes",
        "url": "https://istio.io/latest/news/releases/1.32.x/announcing-1.32/",
        "summary": "Istio 1.32.0：delta xDS 内存优化、headless TCP 服务可选单 listener、DestinationRule 离群检测支持自定义 HTTP 错误码。",
        "published": "2026-11-09T00:00:00+00:00",
        "source": "Istio Releases",
        "source_cat": "云原生-官方",
        "extra": {},
        "board": "基础设施",
        "category": "K8s 核心技术",
        "oss": False,
        "hot_score": 0,
        "is_hot": False,
    },
    {
        "title": "Kubeflow Trainer v2.4.0",
        "url": "https://github.com/kubeflow/trainer/releases/tag/v2.4.0",
        "summary": "Kubeflow Trainer v2.4.0：KEP-3015 workload-aware scheduling 第一阶段落地，MPI 插件改用 PRTE 环境变量属破坏性变更。",
        "published": "2026-11-06T00:00:00+00:00",
        "source": "GitHub Releases",
        "source_cat": "K8s-AI",
        "extra": {},
        "board": "基础设施",
        "category": "K8s × AI",
        "oss": True,
        "hot_score": 0,
        "is_hot": False,
    },
]

new = [a for a in add if a["url"] not in have]
d.extend(new)
json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print(f"appended {len(new)} items; total {len(d)}")
for a in new:
    print(" +", a["category"], a["url"])
