#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append gap-filled items (funnel step 3) into processed.json for issue 056."""
import json, os

REPO = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(REPO, "processed.json"), encoding="utf-8"))
have = {x["url"] for x in P}

NEW = [
    {
        "title": "opencode v2.3.0: subagents now run in the background by default",
        "url": "https://github.com/anomalyco/opencode/releases/tag/v2.3.0",
        "source": "GitHub Releases",
        "category": "Agent 工具链",
        "summary": "opencode v2.3.0 makes background subagents the default: subagents return their session id immediately, keep running, and report back whenever idle, so the parent session can run several concurrently. Quiet transcripts collapse each run of tool calls and thoughts into one row; desktop adds Jump to message (Cmd+Alt+G). Also adds experimental MCP events, shell commands surviving server handoffs, opt-in shell_timeout_background, and mTLS client certs per provider.",
        "oss": True,
        "published": "2026-11-13",
    },
    {
        "title": "e2b@2.64.0: resizable templates and OAuth auth headers",
        "url": "https://github.com/e2b-dev/E2B/releases/tag/e2b%402.64.0",
        "source": "GitHub Releases",
        "category": "沙箱与运行时",
        "summary": "E2B SDK 2.64.0 adds resizable templates: build with maxCpuCount and choose each sandbox's cpuCount at create time; Template.list()/delete() move to the SDK paginator; commands.run gains a shell option; the API client accepts an Authorization header (OAuth access token) plus X-Team-ID instead of an API key.",
        "oss": True,
        "published": "2026-11-13",
    },
    {
        "title": "The runtime layer of sandboxing: gVisor, Kata, microVMs and Docker Sandboxes (sbx)",
        "url": "https://kubezilla.io/kubernetes-sandboxing-runtime-layer-docker-sbx/",
        "source": "Kubezilla",
        "category": "沙箱与运行时",
        "summary": "Third part of a sandboxing series: a runc container shares the host kernel, so RuntimeClass (gvisor/runsc, kata) is the second wall behind cluster-level policy. Covers the SIG Apps Agent Sandbox CRD (agents.x-k8s.io/v1alpha1, alpha) which is runtime agnostic, and Docker Sandboxes sbx (microVM CLI for Claude Code/Codex/Gemini CLI with --clone, policy allow network, policy log).",
        "oss": False,
        "published": "2026-11-15",
    },
    {
        "title": "The cluster layer of Kubernetes sandboxing: namespaces, RBAC, NetworkPolicy and Pod Security for AI agents",
        "url": "https://kubezilla.io/kubernetes-sandboxing-cluster-layer/",
        "source": "Kubezilla",
        "category": "K8s × AI",
        "summary": "Second part of a sandboxing series: per-agent namespace with Pod Security Admission restricted, automountServiceAccountToken false, namespace-scoped Role (never ClusterRole) for agent workloads, default-deny egress with a DNS allow rule, DNS-aware policy via Cilium FQDN, blocking 169.254.169.254, and ResourceQuota to contain agent loops.",
        "oss": False,
        "published": "2026-11-15",
    },
]

added = 0
for n in NEW:
    if n["url"] in have:
        print("skip existing:", n["url"])
        continue
    P.append(n)
    have.add(n["url"])
    added += 1

json.dump(P, open(os.path.join(REPO, "processed.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("appended:", added, "total:", len(P))
