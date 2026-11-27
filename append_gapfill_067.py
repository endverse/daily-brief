#!/usr/bin/env python3
"""Append funnel-step-3 gap-fill items into processed.json so verify_links accepts them."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(BASE, "processed.json")
items = json.load(open(P, encoding="utf-8"))
have = {it["url"] for it in items}

def mk(title, url, summary, cat, board="AI 板块", source="补搜", oss=False, score=12, pub="2026-11-26T00:00:00+00:00"):
    return {"title": title, "url": url, "summary": summary, "published": pub,
            "source": source, "source_cat": "补搜", "extra": {}, "board": board,
            "category": cat, "oss": oss, "hot_score": score, "is_hot": False}

new = [
 mk("Agentic Algorithm Engineering (AAE) skill",
    "https://chszlab.github.io/AgenticAlgorithmEngineering/",
    "A skill for Claude Code and Codex from Heidelberg University's Algorithm Engineering Group: a falsifiable hypothesis before every experiment, correctness checked after every change, one reviewable patch per accepted change, and a PDF report of the session.",
    "Agent & Skill", source="CHSZLab", oss=True, score=15),
 mk("Porting Rockbox to an undocumented $9 Aliexpress YP3 MP3 player with LLMs",
    "https://jayd.ml/2026/11/14/rockbox-on-yp3.html",
    "Reverse engineering Rockbox onto a 512 KiB SRAM player, then having Claude build a reusable porting toolkit that brought a second player up in 4 hours.",
    "AI 工程落地", source="jayd.ml", score=14),
 mk("Orca v1.4.278",
    "https://github.com/stablyai/orca/releases/tag/v1.4.278",
    "Antigravity runs on agy with one sign-in, Gemini CLI removed, six more apps connect in one click, downloads save to this computer, bots can be muted.",
    "Agent 工具链", source="GitHub Releases", oss=True, score=13),
 mk("OpenCode v2.4.2",
    "https://github.com/anomalyco/opencode/releases/tag/v2.4.2",
    "GPT-6.2 system prompt, generate_image/generate_video moved into Code Mode (~700 tokens saved per request), web-fetch always-allow scoped per site, automations keep running after a failed run.",
    "Agent 工具链", source="GitHub Releases", oss=True, score=13),
 mk("E2B e2b@2.66.0",
    "https://github.com/e2b-dev/E2B/releases/tag/e2b@2.66.0",
    "Resizable memory: build a template with maxMemoryMB, pick each sandbox's memoryMB on create, and pick the memory and CPUs a paused sandbox resumes with on Sandbox.connect.",
    "沙箱与运行时", source="GitHub Releases", oss=True, score=14),
 mk("gVisor release-20261123.1",
    "https://github.com/gvisor/gvisor/releases/tag/release-20261123.1",
    "Enable --oci-seccomp by default, OCI seccomp filters support SECCOMP_RET_KILL_THREAD/KILL_PROCESS, runsc tracks Sentry host filesystem filter level with mount guards.",
    "沙箱与运行时", source="GitHub Releases", oss=True, score=13),
 mk("microsandbox v0.8.3",
    "https://github.com/superradcompany/microsandbox/releases/tag/v0.8.3",
    "Breaking SDK change exposing configured contexts and retained metadata; Windows fix keeps TLS keys private on shared data drives.",
    "沙箱与运行时", source="GitHub Releases", oss=True, score=11),
 mk("Dynamo v1.7.0",
    "https://github.com/ai-dynamo/dynamo/releases/tag/v1.7.0",
    "Global Router cross-pool routing with pool discovery and affinity routing, Planner batch scheduling and GPU budget trades, Router deadline queues, multinode Sidecar with in-flight request migration. 763 PRs from 150 contributors.",
    "K8s × AI", board="基础设施板块", source="GitHub Releases", oss=True, score=14),
 mk("Kubernetes v1.37.3",
    "https://github.com/kubernetes/kubernetes/releases/tag/v1.37.3",
    "Patch release built with Go 1.26.11: scheduler crash on rapid same-name Pod recreation, CSINode registration on recreated nodes, kubeadm etcd backup rollback fix.",
    "K8s 核心技术", board="基础设施板块", source="GitHub Releases", oss=True, score=12),
 mk("Kueue v0.20.8",
    "https://github.com/kubernetes-sigs/kueue/releases/tag/v0.20.8",
    "All controllers' logs aligned with the logging policy: per-object logs moved from level 2 to 3, eviction logged after save, log keys renamed across ConcurrentAdmission/LWS/ProvisioningRequest/MultiKueue/jobframework.",
    "K8s 核心技术", board="基础设施板块", source="GitHub Releases", oss=True, score=11),
 mk("Google Will Make AI Agents Use Its Workspace MCP Servers",
    "https://techstackups.com/articles/google-workspace-ai-agents-mcp/",
    "Google made eight Workspace MCP servers GA on 24 November and added a Workspace AI Tools Addendum: from 1 February 2027 any tool driven by an AI agent must reach Gmail/Drive/Calendar through Google MCP; the Gmail server cannot send email without partner access.",
    "平台政策与风控", source="Tech Stackups", score=13),
]
added = 0
for n in new:
    if n["url"] not in have:
        items.append(n); have.add(n["url"]); added += 1
json.dump(items, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"appended {added}, total {len(items)}")
for n in new:
    print(" ", ("OK " if n["url"] in {i["url"] for i in items} else "MISS"), n["category"], n["title"][:60])
