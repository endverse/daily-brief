#!/usr/bin/env python3
"""Append funnel step-3 gap-fill items into processed.json (so verify_links passes)."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(BASE, "processed.json")
items = json.load(open(P, encoding="utf-8"))
have = {i["url"] for i in items}

NEW = [
 dict(title="vLLM-GR：把 beam search 做进 vLLM 引擎，为生成式推荐一次请求产出候选 SID",
      url="https://vllm.ai/blog/2026-11-24-vllm-gr-announcement",
      summary="vLLM-GR 是基于 vLLM 的开源生成式推荐推理框架，用跨越整个搜索过程的 beam session 复用 paged KV cache，一次请求返回多路径候选。",
      published="2026-11-24T00:00:00+00:00", source="vLLM Blog", source_cat="项目官方",
      board="基础设施板块", category="K8s × AI", oss=True),
 dict(title="Dynamo v1.7.0：跨池 Global Router 与仿真选型的 Operator",
      url="https://github.com/ai-dynamo/dynamo/releases/tag/v1.7.0",
      summary="Dynamo v1.7.0 是第 20 个特性版本，763 个 PR、150 名贡献者，新增跨池路由、Planner 批调度与实时调参、Operator 仿真搜索部署。",
      published="2026-11-24T07:08:34+00:00", source="GitHub Releases", source_cat="开源项目",
      board="基础设施板块", category="K8s × AI", oss=True),
 dict(title="Rook v1.21.3：Ceph operator 补丁，OSD 并行更新可按故障域限流",
      url="https://github.com/rook/rook/releases/tag/v1.21.3",
      summary="Rook v1.21.3 是 Ceph operator 的补丁版本，含 OSD 并行更新限单故障域、mon secret 移出清理 Job、对象存储删除前停网关等修复。",
      published="2026-11-24T00:00:00+00:00", source="GitHub Releases", source_cat="开源项目",
      board="基础设施板块", category="K8s 核心技术", oss=True),
 dict(title="gVisor 20261123.0：chroot 根挂载保留 nosuid/noexec，seccomp 缓存跨任务复用",
      url="https://github.com/gvisor/gvisor/releases/tag/release-20261123.0",
      summary="gVisor 周更版本，重点在隔离面：Sentry chroot 根挂载保留 nosuid/nodev/noexec、seccomp 过滤器按需拆分并复用缓存、overlay 叠加深度限制为 2。",
      published="2026-11-24T21:32:59+00:00", source="GitHub Releases", source_cat="开源项目",
      board="AI 板块", category="沙箱与运行时", oss=True),
 dict(title="microsandbox v0.8.2：可选的运行时隔离档位与严格主机文件打开",
      url="https://github.com/superradcompany/microsandbox/releases/tag/v0.8.2",
      summary="microsandbox v0.8.2 增加 runtime isolation 选项、strict host file opens、快照文件独立物化与有界 patch 源码暂存。",
      published="2026-11-24T11:44:54+00:00", source="GitHub Releases", source_cat="开源项目",
      board="AI 板块", category="沙箱与运行时", oss=True),
 dict(title="Orca v1.4.273：Bot 面板显示下次运行时间，手机端可管账号与群组",
      url="https://github.com/stablyai/orca/releases/tag/v1.4.273",
      summary="Orca v1.4.273 把 Bot 的运行排期、待回答问题与 Google 账号接入搬到面板和手机端，流式浏览器页面支持键盘操作与打印 PDF。",
      published="2026-11-24T10:20:48+00:00", source="GitHub Releases", source_cat="开源项目",
      board="AI 板块", category="Agent 工具链", oss=True),
 dict(title="OpenCode v2.4.1：模型服务档位变成可记忆的速度，配置里的 Ollama 直接出现在 /models",
      url="https://github.com/anomalyco/opencode/releases/tag/v2.4.1",
      summary="OpenCode v2.4.1 修复 macOS 12 会话保存，config-only provider 的模型直接出现在 /models，compaction 保留量按 keep.tokens 生效。",
      published="2026-11-23T15:57:40+00:00", source="GitHub Releases", source_cat="开源项目",
      board="AI 板块", category="Agent 工具链", oss=True),
 dict(title="Gemini CLI v0.72.0-preview.0：A2A server 强制 bearer token 并校验输入",
      url="https://github.com/google-gemini/gemini-cli/releases/tag/v0.72.0-preview.0",
      summary="Gemini CLI 预览版修了一处 A2A server 鉴权缺口（强制 bearer token + 请求输入校验），并修正嵌套 .gitignore 否定规则与 session 恢复选择。",
      published="2026-11-24T00:00:00+00:00", source="GitHub Releases", source_cat="开源项目",
      board="AI 板块", category="Agent 工具链", oss=True),
 dict(title="ERNIE 5.5 Flash Preview：280B MoE 只激活 14B，1M 上下文，vLLM 当天支持",
      url="https://vllm.ai/blog/2026-11-24-ernie-5-5-flash-preview",
      summary="百度 ERNIE 5.5 Flash Preview 是 280B 总参、14B 激活的稀疏 MoE，支持 1M 上下文与工具调用，通过 vLLM-ERNIE 插件在 vllm 0.32.0 上当天可用。",
      published="2026-11-24T00:00:00+00:00", source="vLLM Blog", source_cat="项目官方",
      board="AI 板块", category="模型与研究", oss=False),
 dict(title="Kueue v0.21.0-rc.2",
      url="https://github.com/kubernetes-sigs/kueue/releases/tag/v0.21.0-rc.2",
      summary="Kueue 0.21 第二个候选版本，延续 DRA 优先设备列表与可消耗容量配额默认开启的改动。",
      published="2026-11-24T00:00:00+00:00", source="GitHub Releases", source_cat="开源项目",
      board="基础设施板块", category="K8s × AI", oss=True),
 dict(title="OpenTelemetry Collector v0.166.0",
      url="https://github.com/open-telemetry/opentelemetry-collector-releases/releases/tag/v0.166.0",
      summary="OpenTelemetry Collector 0.166.0 常规发布。",
      published="2026-11-25T00:00:00+00:00", source="GitHub Releases", source_cat="开源项目",
      board="基础设施板块", category="云原生周边", oss=True),
]

added = 0
for it in NEW:
    if it["url"] in have:
        continue
    base = dict(published="", source="", source_cat="", extra={}, board="", category="",
                oss=False, hot_score=0, is_hot=False)
    base.update(it)
    base.setdefault("extra", {})
    items.append(base)
    have.add(it["url"])
    added += 1

json.dump(items, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"appended {added}, total {len(items)}")
