#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Issue 063 gap-fill: append targeted-search items into processed.json.
Needed because full-archive dedup emptied 沙箱与运行时 / K8s × AI and 工具链 had
only one usable candidate (Orca). URLs are the exact ones cited in briefing.json.
"""
import json, os, subprocess

REPO = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(REPO, "processed.json"), encoding="utf-8"))
have = {x["url"] for x in items}

new = [
 {
  "title": "Serverless sandboxes in Azure Container Instances (preview)",
  "url": "https://learn.microsoft.com/en-us/azure/container-instances/container-instances-ai-sandboxes",
  "summary": "Each ACI sandbox is a lightweight Hyper-V microVM with its own isolation boundary; snapshots capture memory+filesystem+runtime state; stretchable sandboxes resize in place; confidential sandboxes run under AMD SEV-SNP with a CCE policy; Agent Grid binds egress.",
  "published": "2026-11-20T00:00:00+00:00",
  "source": "Microsoft Learn",
  "source_cat": "厂商文档",
  "extra": {},
  "board": "AI 板块",
  "category": "沙箱与运行时",
  "oss": False,
  "hot_score": 12,
  "is_hot": False,
 },
 {
  "title": "Agent Sandbox cluster extension (preview) - Azure Kubernetes Service",
  "url": "https://learn.microsoft.com/en-us/azure/aks/agent-sandbox-cluster-extension",
  "summary": "The extension runs the open-source Kubernetes Agent Sandbox project on AKS: a Sandbox CRD/controller that creates stateful agent execution environments either as Kata VM isolation v2 pods on your node pools or as ACI serverless sandboxes. One runtime per extension install, warm pools optional, pairs with the Pod snapshot extension for suspend/resume.",
  "published": "2026-11-20T00:00:00+00:00",
  "source": "Microsoft Learn",
  "source_cat": "厂商文档",
  "extra": {},
  "board": "基础设施板块",
  "category": "K8s × AI",
  "oss": False,
  "hot_score": 11,
  "is_hot": False,
 },
 {
  "title": "Orca v1.4.271",
  "url": "https://github.com/stablyai/orca/releases/tag/v1.4.271",
  "summary": "One bot group can now hold bots from paired computers, bots can run on Qwen Code, the phone app manages agents end to end, chats can be deleted and continue after a usage limit, and several GitHub accounts can be linked.",
  "published": "2026-11-22T00:00:00+00:00",
  "source": "GitHub Releases",
  "source_cat": "开源项目",
  "extra": {},
  "board": "AI 板块",
  "category": "Agent 工具链",
  "oss": True,
  "hot_score": 10,
  "is_hot": False,
 },
 {
  "title": "OpenComputer - open source alternative to Devin",
  "url": "https://github.com/diggerhq/opencomputer",
  "summary": "Slack-native coding agent: mention @Computer in a thread, it runs on its own VM (rootless Podman per session), you can watch and steer it, and the result lands as a PR. Self-hostable on AWS/GCP/Azure; claims PRs 3.3x faster than Devin and 32.0s vs 36.2s against local Claude Code.",
  "published": "2026-11-20T00:00:00+00:00",
  "source": "Hacker News",
  "source_cat": "AI-社区",
  "extra": {"points": 125},
  "board": "AI 板块",
  "category": "AI 工程落地",
  "oss": True,
  "hot_score": 12,
  "is_hot": False,
 },
 {
  "title": "If you stop writing code, you also get worse at reviewing it",
  "url": "https://cekrem.github.io/posts/if-you-stop-writing-code-you-also-get-worse-at-reviewing-it/",
  "summary": "Argument that delegating implementation to agents erodes the reviewing skill itself: reviewing is a practiced craft, and 'reviewing all the code Claude wrote' mostly means not reading half of it. Proposes keeping hands-on practice deliberately.",
  "published": "2026-11-20T00:00:00+00:00",
  "source": "Hacker News",
  "source_cat": "AI-社区",
  "extra": {"points": 397, "comments": 181},
  "board": "AI 板块",
  "category": "观点与好文",
  "oss": False,
  "hot_score": 9,
  "is_hot": False,
 },
 {
  "title": "Kueue v0.20.7",
  "url": "https://github.com/kubernetes-sigs/kueue/releases/tag/v0.20.7",
  "summary": "Patch release: fixes DRA quota being charged twice for deviceClassMappings with two counter sources, a DRA workload admitted with a missing DeviceClass that could never schedule, and MultiKueue re-dispatching workloads from a removed worker cluster so the same job ran twice.",
  "published": "2026-11-19T00:00:00+00:00",
  "source": "GitHub Releases",
  "source_cat": "开源项目",
  "extra": {},
  "board": "基础设施板块",
  "category": "K8s × AI",
  "oss": True,
  "hot_score": 8,
  "is_hot": False,
 },
]

added = 0
for it in new:
    if it["url"] in have:
        print("skip (exists):", it["title"][:50])
        continue
    st = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}",
                         "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", "-L", "--max-time", "25", it["url"]],
                        capture_output=True, text=True).stdout.strip()
    print(f"HTTP {st}  {it['title'][:60]}")
    if st != "200":
        print("  !! not 200, skipped")
        continue
    items.append(it)
    have.add(it["url"])
    added += 1

json.dump(items, open(os.path.join(REPO, "processed.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"appended {added}; processed.json now {len(items)} items")
