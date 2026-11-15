#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append funnel-step-3 gap-fill items into processed.json for issue 055."""
import json, os

REPO = os.path.dirname(os.path.abspath(__file__))
NEW = [
    {
        "title": "E2B weekly: HTTP/1.1 file transfers and invitation-only workspace membership",
        "url": "https://e2b.dev/changelog",
        "summary": "E2B's Nov 9 weekly ships SDK file transfers over HTTP/1.1 (JS 2.62.2 uploads, Python 2.62.1 downloads) regardless of the configured protocol, an invitation-only workspace membership model, TencentOS Server 4 / OpenCloudOS 9 template bases, sandbox-timestamped Code Interpreter output, and fixes for paused-sandbox timeouts and pause-time disk exhaustion killing sibling sandboxes.",
        "published": "2026-11-09",
        "source": "E2B Changelog",
        "source_cat": "AI-官方",
        "extra": {},
        "board": "AI 板块",
        "category": "沙箱与运行时",
        "oss": False,
        "hot_score": 12,
        "is_hot": False,
    },
    {
        "title": "Encoder/Prefill/Decode disaggregation in vLLM: metadata-only EPD and what it buys",
        "url": "https://vllm.ai/blog/2026-11-11-encoder-disaggregation-epd",
        "summary": "vLLM details EPD disaggregation (separate encoder, prefill and decode instances) with EC connectors, metadata-only forwarding and shared encoder caching: on a 12-GPU EPD layout vs an 8-GPU PD baseline it gains 6.6-9.5% input+output throughput per GPU and cuts P90 TTFT 44-47% at concurrency 64-128, and GPU preprocessing plus NVDEC decode roughly doubles end-to-end throughput on a 30-frame MMVU run.",
        "published": "2026-11-11",
        "source": "vLLM Blog",
        "source_cat": "AI-官方",
        "extra": {},
        "board": "AI 板块",
        "category": "K8s × AI",
        "oss": True,
        "hot_score": 15,
        "is_hot": False,
    },
    {
        "title": "KAI Scheduler v0.19.0: gpu-memory/gpu-fraction limits, NUMA-aware memory manager",
        "url": "https://github.com/kai-scheduler/KAI-Scheduler/releases/tag/v0.19.0",
        "summary": "KAI Scheduler v0.19.0 adds gpu-memory.limit and gpu-fraction.limit for NvFraction mode, models GPU memory manager NUMA groups in scheduling and exports per-pod observed memory ownership, adds opt-in preempt/reclaim for kubelet-deferred in-place resizes, keeps DRA devices, host ports and pod affinity of terminating pods when pipelining, and makes Ray clusters use minReplicas as the worker gang minimum.",
        "published": "2026-11-11",
        "source": "GitHub Releases",
        "source_cat": "开源",
        "extra": {},
        "board": "AI 板块",
        "category": "K8s × AI",
        "oss": True,
        "hot_score": 13,
        "is_hot": False,
    },
    {
        "title": "Calico v3.33.1: IPAM leak fixes for Multus pools and per-family eBPF conntrack autoscaling",
        "url": "https://github.com/projectcalico/calico/releases/tag/v3.33.1",
        "summary": "Calico v3.33.1 is a bugfix release: the IPAM garbage collector now releases IPs leaked by a pod's earlier sandboxes and by Succeeded/Failed pods (which could exhaust small Multus secondary pools), eBPF conntrack autoscaling doubles only the IP family above 80% full and records sizes per family, pods can no longer forge TCP RSTs past egress connection limits, and IP pools release tunnel addresses when nodeSelector changes.",
        "published": "2026-11-12",
        "source": "GitHub Releases",
        "source_cat": "开源",
        "extra": {},
        "board": "基础设施",
        "category": "K8s 核心技术",
        "oss": True,
        "hot_score": 11,
        "is_hot": False,
    },
]

p = json.load(open(os.path.join(REPO, "processed.json"), encoding="utf-8"))
have = {x["url"] for x in p}
added = 0
for it in NEW:
    if it["url"] in have:
        continue
    p.append(it)
    added += 1
json.dump(p, open(os.path.join(REPO, "processed.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("appended", added, "total", len(p))
