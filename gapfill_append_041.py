#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gap-fill: append K8s×AI / K8s-core items found via funnel step ③ to processed.json."""
import json

add = [
    {
        "title": "Grove v0.2.0-beta1",
        "url": "https://github.com/ai-dynamo/grove/releases/tag/v0.2.0-beta1",
        "summary": "Grove v0.2.0-beta1 promotes the Grove APIs to beta: adds grove.io/v1beta1 and operator.config.grove.io/v1beta1, makes grove.io/v1beta1 the stored version, removes topologyConstraint.packDomain and PodCliqueSetStatus.podGangStatuses, and defaults scaleConfig.minReplicas to minAvailable.",
        "published": "2026-10-30T16:10:50+00:00",
        "source": "GitHub Releases",
        "source_cat": "GitHub",
        "extra": {},
        "board": "基础设施板块",
        "category": "K8s × AI",
        "oss": True,
        "hot_score": 0,
        "is_hot": False,
    },
    {
        "title": "Announcing the Workload Conformance Working Group",
        "url": "https://kubernetes.io/blog/2026/10/27/announcing-workload-conformance-wg/",
        "summary": "The Kubernetes community announces a Workload Conformance Working Group writing a shared standard for how workloads behave at runtime, covering security, resilience during disruptions, resource use, networking, storage, API usage and observability; every requirement must be verifiable by a test binary.",
        "published": "2026-10-27T04:30:00+00:00",
        "source": "Kubernetes Blog",
        "source_cat": "K8s-官方",
        "extra": {},
        "board": "基础设施板块",
        "category": "K8s 核心",
        "oss": False,
        "hot_score": 0,
        "is_hot": False,
    },
]

p = "processed.json"
items = json.load(open(p, encoding="utf-8"))
have = {i["url"] for i in items}
n = 0
for a in add:
    if a["url"] not in have:
        items.append(a)
        n += 1
json.dump(items, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("appended", n, "total", len(items))
