#!/usr/bin/env python3
"""Issue 066: append gap-fill items to processed.json (and processed.dedup.json)."""
import json, subprocess, os

REPO = os.path.dirname(os.path.abspath(__file__))
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36'

NEW = [
    dict(title='OpenCode v2.4.0：Automations 定时/事件触发、内置桌面浏览器、MCP Events',
         url='https://opencode.ai/changelog/v2.4.0', source='OpenCode Changelog', source_cat='AI-工具链',
         summary='v2.4.0 让 agent 可按 cron、间隔或 MCP 服务端事件触发 prompt/脚本/shell 命令，新增桌面端内置浏览器（可导入 Chrome/Safari 登录态并由 agent 直接读写同一页面），跟随 MCP Events beta 做推送式工具调用，Claude Agent 提供商支持多账号按用量上限自动切换。',
         published='2026-11-23T00:00:00+00:00', board='AI 板块', category='Agent 工具链', oss=True, hot_score=17),
    dict(title='Claude Code v2.1.332：MCP 服务器的 skills 进入补全菜单（beta）',
         url='https://github.com/anthropics/claude-code/releases/tag/v2.1.332', source='Claude Code Releases', source_cat='AI-工具链',
         summary='v2.1.332 起 MCP 服务器可以提供 skills，以 server:skill 形式出现在 / 菜单；同时新增 PreSkillShellCommand hook 可在 skill/命令加载时拦截其内联 shell、OpenTelemetry assistant_response 事件，以及大量 MCP/压缩/钩子相关的卡死修复。',
         published='2026-11-25T00:00:00+00:00', board='AI 板块', category='Agent 工具链', oss=False, hot_score=15),
    dict(title='Vercel Sandbox SDK 5.0.0：沙箱一律由镜像创建，runtime 参数移除',
         url='https://github.com/vercel/sandbox/releases/tag/sandbox%405.0.0', source='Vercel Sandbox Releases', source_cat='AI-沙箱',
         summary='5.0.0 移除已废弃的 runtime 选项，沙箱改为始终从镜像创建（al- 前缀为 Amazon Linux 2023，无前缀为 Ubuntu），CLI 的 --runtime 同步改为 --image；新增 getAuthHeaders 以支持 DPoP（RFC 9449）等自定义认证头。',
         published='2026-11-25T00:00:00+00:00', board='AI 板块', category='沙箱与运行时', oss=False, hot_score=15),
    dict(title='在 Kubernetes 里跑 agent 的三种 Docker Sandboxes 隔离姿势',
         url='https://kubezilla.io/kubernetes-docker-sandboxes-sbx/', source='Kubezilla', source_cat='K8s',
         summary='Docker Sandboxes（sbx）给每个 agent 一个独立 microVM 与私有 Docker daemon；文中给出三种与 K8s 配合的做法：沙箱内用 kind/k3d 起一次性集群、给只读 ServiceAccount 让 agent 查真实集群、以及用网络策略与 sbx policy 限制出口，并附 sbx policy init/log/allow 的具体命令。',
         published='2026-11-24T00:00:00+00:00', board='AI 板块', category='沙箱与运行时', oss=False, hot_score=14),
    dict(title='Kubernetes v1.37.3 / v1.36.7 / v1.35.11 同步补丁版：修调度器崩溃与 CSINode 重注册',
         url='https://github.com/kubernetes/kubernetes/releases/tag/v1.37.3', source='Kubernetes Releases', source_cat='K8s',
         summary='11 月 25 日三条维护线同时发补丁：修复同名 Pod 快速删除重建导致的调度器崩溃、节点同名重建时 kubelet 无法注册 CSINode 导致 CSI 卷挂载失败、NativeHistograms 下默认桶丢失、kube-proxy 拓扑路由漏读 Node zone，以及 kubeadm etcd 升级失败后回滚路径错误；改用 Go 1.26.11 构建。',
         published='2026-11-25T00:00:00+00:00', board='基础设施', category='K8s 核心', oss=False, hot_score=13),
    dict(title='KAI-Scheduler v0.18.9：给独立 DRA ResourceClaim 加删除保护',
         url='https://github.com/kai-scheduler/KAI-Scheduler/releases/tag/v0.18.9', source='KAI-Scheduler Releases', source_cat='K8s-AI',
         summary='v0.18.9 为独立 DRA ResourceClaim 增加 delete-protection finalizer，确保被抢占的 GPU 设备能被真正释放；同时把 operator informer cache 收敛到 KAI 命名空间、允许 PodGroup/Queue 控制器记录 leader-election 事件，并让 Pod-grouper 日志只打 owner 引用避免泄漏环境变量。',
         published='2026-11-23T00:00:00+00:00', board='基础设施', category='K8s × AI', oss=True, hot_score=13),
    dict(title='KubeRay v1.7.3：go-openapi 与 x/net 升级修 CVE',
         url='https://github.com/kuberay-project/kuberay/releases/tag/v1.7.3', source='KubeRay Releases', source_cat='K8s-AI',
         summary='v1.7.3 是 1.7 线维护版，把 golang.org/x/net 升到 v0.62.0、go-openapi/swag 升到 v0.27.1 以修 CVE。',
         published='2026-11-23T00:00:00+00:00', board='基础设施', category='K8s × AI', oss=True, hot_score=10),
    dict(title='Apple container 1.7.1：Kata 内核升级到 4.3.1，集群支持共享镜像库',
         url='https://github.com/apple/container/releases/tag/1.7.1', source='apple/container Releases', source_cat='云原生',
         summary='1.7.1 把默认 Kata 内核升级到 4.3.1（vmlinux-6.18.56-208-debug），新增 container cluster create --shared-image-store 让集群节点直接用宿主镜像库（同时移除 load-image），集群列表改为一集群一行，worker 节点可用 --workers count=,cpus=,memory= 指定规格。',
         published='2026-11-14T00:00:00+00:00', board='基础设施', category='云原生周边', oss=True, hot_score=11),
    dict(title='Gemini CLI v0.71.0：PowerShell 命令异步解析修界面卡死',
         url='https://github.com/google-gemini/gemini-cli/releases/tag/v0.71.0', source='Gemini CLI Releases', source_cat='AI-工具链',
         summary='v0.71.0 主要是修复版：PowerShell 命令改为异步解析以避免 spinner 冻结，其余为版本号与发布流程变更。',
         published='2026-11-24T00:00:00+00:00', board='AI 板块', category='Agent 工具链', oss=True, hot_score=9),
]

for it in NEW:
    r = subprocess.run(['curl', '-sSL', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '25',
                        '-A', UA, it['url']], capture_output=True, text=True)
    code = r.stdout.strip()
    print(f'{code}  {it["url"]}')
    assert code in ('200', '403'), 'BAD URL'

p = os.path.join(REPO, 'processed.json')
items = json.load(open(p, encoding='utf-8'))
have = {x['url'] for x in items}
added = 0
for it in NEW:
    if it['url'] in have:
        continue
    row = {'title': it['title'], 'url': it['url'], 'summary': it['summary'],
           'published': it['published'], 'source': it['source'], 'source_cat': it['source_cat'],
           'extra': {}, 'board': it['board'], 'category': it['category'],
           'oss': it['oss'], 'hot_score': it['hot_score'], 'is_hot': False}
    items.append(row); added += 1
json.dump(items, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'processed.json: +{added} -> {len(items)}')

d = os.path.join(REPO, 'processed.dedup.json')
ded = json.load(open(d, encoding='utf-8'))
have2 = {x['url'] for x in ded}
for it in NEW:
    if it['url'] in have2:
        continue
    ded.append({'title': it['title'], 'url': it['url'], 'summary': it['summary'],
                'published': it['published'], 'source': it['source'], 'source_cat': it['source_cat'],
                'extra': {}, 'board': it['board'], 'category': it['category'],
                'oss': it['oss'], 'hot_score': it['hot_score'], 'is_hot': False})
json.dump(ded, open(d, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'processed.dedup.json: {len(ded)}')
