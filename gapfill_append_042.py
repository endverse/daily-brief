#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gap-fill: append K8s x AI / K8s-core items found via funnel step 3 to processed.json."""
import json

add = [
    {
        "title": "Kubeflow Trainer v2.4.0-rc.0",
        "url": "https://github.com/kubeflow/trainer/releases/tag/v2.4.0-rc.0",
        "summary": "Kubeflow Trainer v2.4.0-rc.0 ships Phase 1 of the OptimizationJob CRD, the successor to Katib: hyperparameter optimization for TrainJobs as its own CRD, shared model/dataset initialization across trials, push-based metric collection through the SDK, and an OptimizerClient API. It also keeps the four CRDs (TrainJob, TrainingRuntime, ClusterTrainingRuntime, OptimizationJob) on helm uninstall via helm.sh/resource-policy: keep, because uninstalling previously garbage-collected every job in the cluster.",
        "published": "2026-10-31T20:22:55+00:00",
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
        "title": "Kubernetes GPU Monitoring: Metrics, Challenges and Best Practices",
        "url": "https://kubezilla.io/kubernetes-gpu-monitoring/",
        "summary": "A deep dive into why GPU monitoring on Kubernetes is harder than CPU monitoring: a pod can hold nvidia.com/gpu: 1 and still sit idle, and a GPU can read 100% busy while doing little real work. The recommended path is NVIDIA DCGM Exporter as a DaemonSet, which maps metrics to pods through the kubelet pod-resources API so every metric carries namespace/pod/container labels, turning 'GPU 3 on node 7 is busy' into 'the GPU of my training job is busy'.",
        "published": "2026-10-31T06:15:10+00:00",
        "source": "Kubezilla",
        "source_cat": "K8s-社区",
        "extra": {},
        "board": "基础设施板块",
        "category": "K8s × AI",
        "oss": False,
        "hot_score": 0,
        "is_hot": False,
    },
    {
        "title": "Gateway API v1.7.0",
        "url": "https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.7.0",
        "summary": "Gateway API v1.7.0 graduates HTTPRoute retries (codes, attempts, backoff) to the Standard channel together with the HTTPRouteRetryCodes and HTTPRouteRetryConnectionError conformance features. New experimental APIs: per-address Gateway routability (GEP-5093), XTelemetryPolicy for tracing based on OpenTelemetry semantic conventions, pre-routing listener filters (GEP-5224), ClusterTrustBundle references in caCertificateRefs, and session persistence moved onto XBackend; Go is bumped to 1.27.",
        "published": "2026-10-29T18:00:00+00:00",
        "source": "GitHub Releases",
        "source_cat": "GitHub",
        "extra": {},
        "board": "基础设施板块",
        "category": "K8s 核心",
        "oss": True,
        "hot_score": 0,
        "is_hot": False,
    },
    {
        "title": "metrics-server v0.9.1",
        "url": "https://github.com/kubernetes-sigs/metrics-server/releases/tag/v0.9.1",
        "summary": "metrics-server v0.9.1 rebuilds the release image to drop the distrusted eMudhra roots from the CA bundle, bumps Go to 1.26.10 and Kubernetes dependencies to v0.36.5. Same supply-chain cleanup that envoy, calico and dynamo shipped this week: the image, not just the code, had to be rebuilt.",
        "published": "2026-10-29T09:00:00+00:00",
        "source": "GitHub Releases",
        "source_cat": "GitHub",
        "extra": {},
        "board": "基础设施板块",
        "category": "K8s 核心",
        "oss": True,
        "hot_score": 0,
        "is_hot": False,
    },
    {
        "title": "OpenTelemetry Collector v0.164.0",
        "url": "https://github.com/open-telemetry/opentelemetry-collector/releases/tag/v0.164.0",
        "summary": "OpenTelemetry Collector v0.164.0 makes otlp_http error messages report the URL the request was actually sent to (middleware that cloned and rewrote the request used to leave the configured placeholder in 4xx/5xx text), and redacts non-empty literal defaults in unexpanded env references such as ${env:NAME:-literal} from the raw config reported by the OpAMP extension. mdatagen gains supported_platforms for component metadata.",
        "published": "2026-10-26T12:00:00+00:00",
        "source": "GitHub Releases",
        "source_cat": "GitHub",
        "extra": {},
        "board": "基础设施板块",
        "category": "云原生周边",
        "oss": True,
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
