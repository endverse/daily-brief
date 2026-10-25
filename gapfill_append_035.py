#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append funnel step-3 gap-fill items to processed.json (issue 035)."""
import json, os

REPO = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(REPO, "processed.json")
items = json.load(open(p, encoding="utf-8"))
have = {it["url"] for it in items}

NEW = [
    dict(title="JobSet v0.13.0", url="https://github.com/kubernetes-sigs/jobset/releases/tag/v0.13.0",
         summary="JobSet 0.13.0 adds alpha Workload-Aware Scheduling (gang scheduling, DRA shared claims), "
                 "active deadlines and execution-attempt tracking behind feature gates.",
         published="2026-10-13T00:00:00+00:00", source="GitHub Releases", source_cat="K8s 官方",
         extra={}, board="基础设施", category="K8s × AI", oss=True, hot_score=14, is_hot=False),
    dict(title="Vertical Pod Autoscaler 1.8.1", url="https://github.com/kubernetes/autoscaler/releases/tag/vertical-pod-autoscaler-1.8.1",
         summary="VPA 1.8.1 fixes updater treating stale lastState OOM as a fresh quick OOM under InPlace and "
                 "DaemonSet replica counting from NumberReady instead of DesiredNumberScheduled.",
         published="2026-10-21T00:00:00+00:00", source="GitHub Releases", source_cat="K8s 官方",
         extra={}, board="基础设施", category="K8s 核心技术", oss=True, hot_score=12, is_hot=False),
    dict(title="cert-manager v1.21.3", url="https://github.com/cert-manager/cert-manager/releases/tag/v1.21.3",
         summary="cert-manager v1.21.3 drops the compromised eMudhra root CA and stops the controller copying a "
                 "private key from a Secret the Certificate does not own.",
         published="2026-10-23T00:00:00+00:00", source="GitHub Releases", source_cat="CNCF",
         extra={}, board="基础设施", category="云原生周边", oss=True, hot_score=13, is_hot=False),
    dict(title="External Secrets Operator v2.14.0", url="https://github.com/external-secrets/external-secrets/releases/tag/v2.14.0",
         summary="ESO v2.14.0 fixes the Vault metadata path not stripping the mount prefix, sanitizes controller "
                 "status/event errors and adds a GitHub App token generator sourcing IDs from Secrets.",
         published="2026-10-23T00:00:00+00:00", source="GitHub Releases", source_cat="CNCF",
         extra={}, board="基础设施", category="云原生周边", oss=True, hot_score=10, is_hot=False),
    dict(title="Karpenter v1.15.1", url="https://github.com/kubernetes-sigs/karpenter/releases/tag/v1.15.1",
         summary="Karpenter v1.15.1 and v1.14.3 are cherry-pick patch releases for the 1.15 and 1.14 lines.",
         published="2026-10-23T00:00:00+00:00", source="GitHub Releases", source_cat="K8s 官方",
         extra={}, board="基础设施", category="云原生周边", oss=True, hot_score=9, is_hot=False),
    dict(title="prometheus-operator 0.94.2", url="https://github.com/prometheus-operator/prometheus-operator/releases/tag/v0.94.2",
         summary="Rebuilt base images to remove the Comodo AAA Services and emSign ECC Root CA - G3 roots, and "
                 "rebuilt with Go 1.27.3.",
         published="2026-10-23T00:00:00+00:00", source="GitHub Releases", source_cat="CNCF",
         extra={}, board="基础设施", category="云原生周边", oss=True, hot_score=8, is_hot=False),
]

added = 0
for it in NEW:
    if it["url"] not in have:
        items.append(it)
        have.add(it["url"])
        added += 1

json.dump(items, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"appended {added}, processed.json now {len(items)} items")
