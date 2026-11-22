#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append target-searched gap-fill items (funnel step 3) into processed.json for issue 062."""
import json, os

REPO = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(REPO, "processed.json")
items = json.load(open(p, encoding="utf-8"))
have = {i["url"] for i in items}

def add(title, url, summary, source, source_cat, board, category, oss=True, published="2026-11-21T00:00:00+00:00"):
    if url in have:
        print("skip existing:", url)
        return
    items.append({
        "title": title, "url": url, "summary": summary, "published": published,
        "source": source, "source_cat": source_cat, "extra": {}, "board": board,
        "category": category, "oss": oss, "hot_score": 10, "is_hot": False,
    })
    have.add(url)
    print("added:", title[:60])

add("Orca v1.4.269: Bots can run on Kiro, Kimi Code, Auggie, Gemini CLI, Kilo Code, MiMo Code, Droid and Goose",
    "https://github.com/stablyai/orca/releases/tag/v1.4.269",
    "Orca 1.4.269 lets Bots run on eight more agents (Kiro, Kimi Code, Auggie, Gemini CLI, Kilo Code, MiMo Code, Droid, Goose), adds @Name hand-offs between bots in group rooms, lets phone clients answer questions and approve access in 'Needs you', and cuts idle Mac terminal CPU with Git work moved to the background worker.",
    "Orca", "AI-官方", "AI 板块", "Agent 工具链", published="2026-11-21T17:57:28+00:00")

add("Gemini CLI v0.70.0: re2js linear-time policy matching, skips system MCP servers with insecure commands",
    "https://github.com/google-gemini/gemini-cli/releases/tag/v0.70.0",
    "v0.70.0 replaces the policy engine's argsPattern evaluation with re2js (linear time, no catastrophic backtracking), skips system MCP servers whose launch commands have insecure permissions, reports accurate per-model output token limits in the models list, scales undici bodyTimeout when the request timeout exceeds 300s, and keeps ASK_USER for shell commands with unresolved variable expansion.",
    "GitHub Releases", "AI-官方", "AI 板块", "Agent 工具链", published="2026-11-19T21:08:05+00:00")

add("Kata Containers 4.4.0: snapshot restore keeps device state, multi-layer EROFS via VMDK on CLH",
    "https://github.com/kata-containers/kata-containers/releases/tag/4.4.0",
    "Kata 4.4.0: runtime-rs preserves device lifecycle state across snapshot restore, ships multi-layer EROFS container images as VMDK for Cloud Hypervisor, reserves explicit PCIe root-port addresses before hotplug, isolates network cleanup from Tokio workers, and completes cleanup for hotplugged block/VFIO devices; kata-deploy can append to CRI config, preserve empty TOML arrays and mtimes; dcgm-exporter bumped to 4.8.4 and nvgpu bundles kata-ctl.",
    "GitHub Releases", "AI-官方", "AI 板块", "沙箱与运行时", published="2026-11-17T00:00:00+00:00")

add("vLLM v0.34.0: extensible KV cache on by default, Model Runner V1 removed, up to 1.95x decode",
    "https://github.com/vllm-project/vllm/releases/tag/v0.34.0",
    "vLLM 0.34.0: 1,061 commits from 412 contributors, 10 new models (Mistral Large 4 1T/52B active, MiniMax-M3.1-Flash, Nemotron-3.5-Transcribe...), extensible KV cache now default (cache sized from memory free after warmup: MiniMax-M3 on H200 433k to 672k tokens), Model Runner V1 removed, default block size 16 to 64, up to 1.95x decode on GB200 and 1.6x throughput on GLM-5.3-Flash.",
    "GitHub Releases", "AI-官方", "基础设施", "K8s × AI", published="2026-11-18T00:00:00+00:00")

add("Dynamo v1.5.1-kimi-k3-post.1: Kimi-K3 on SGLang with DCP/DSpark patches, GB300 1P1D recipes",
    "https://github.com/ai-dynamo/dynamo/releases/tag/v1.5.1-kimi-k3-post.1",
    "Experimental Dynamo snapshot serving moonshotai/Kimi-K3 from an SGLang 0.5.18 runtime on Dynamo 1.5.1, bundling two needed fixes (DCP prefill/decode with DSpark draft-KV transfer, SM100 MoonViT cuDNN guard). GB300 recipes: aggregated 2 workers on 16x GB300 with DCP8 attention/TP8 MoE, disaggregated 1P1D with Mooncake KV transfer over NVLink, plus an AIPerf replay of a 64K-ISL/400-OSL/90% KV-reuse agentic trace.",
    "GitHub Releases", "AI-官方", "基础设施", "K8s × AI", published="2026-11-18T00:00:00+00:00")

add("BuildKit v0.35.1: skip empty attestation manifests, restore snapshot key sharing with docker pull",
    "https://github.com/moby/buildkit/releases/tag/v0.35.1",
    "BuildKit 0.35.1 skips empty attestation manifests, restores sharing of snapshot key names with docker pull as allowed before v0.33.x, and fixes a regression where large filesync pattern lists could error out.",
    "GitHub Releases", "AI-官方", "基础设施", "K8s 核心技术", published="2026-11-19T00:00:00+00:00")

add("microsandbox v0.8.1 / v0.8.0: SDK resolves named volumes before sandbox creation",
    "https://github.com/superradcompany/microsandbox/releases/tag/v0.8.1",
    "microsandbox 0.8.1/0.8.0 fix named mounts on the cloud backend by resolving volumes (reuse existing or create missing) before sandbox creation, shared across all SDK bindings, rejecting unsupported creation options.",
    "GitHub Releases", "AI-官方", "AI 板块", "沙箱与运行时", published="2026-11-20T11:28:21+00:00")

json.dump(items, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("processed.json now:", len(items))
