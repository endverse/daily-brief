#!/usr/bin/env python3
"""Issue 066 gap-fill: pull releases.atom from toolchain / sandbox / K8s repos."""
import json, re, os, subprocess, email.utils, datetime, html

REPO = os.path.dirname(os.path.abspath(__file__))
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

REPOS = [
    # agent toolchain
    'anomalyco/opencode', 'openai/codex', 'anthropics/claude-code',
    'google-gemini/gemini-cli', 'stablyai/orca',
    # sandbox / runtime
    'superradcompany/microsandbox', 'e2b-dev/E2B', 'daytonaio/daytona',
    'gvisor/gvisor', 'kata-containers/kata-containers',
    'firecracker-microvm/firecracker', 'microvm-nix/microvm.nix',
    'microsoft/wsl2', 'apple/container',
    # k8s x ai
    'kubernetes-sigs/kueue', 'kserve/kserve', 'vllm-project/vllm',
    'ai-dynamo/dynamo', 'sgl-project/sglang', 'NVIDIA/k8s-dra-driver-gpu',
    'kubeflow/trainer', 'ray-project/kuberay', 'NVIDIA/KAI-Scheduler',
    # k8s core / cloud native
    'cilium/cilium', 'containerd/containerd', 'istio/istio',
    'rook/rook', 'envoyproxy/envoy', 'kubernetes-sigs/gateway-api',
    'moby/buildkit', 'open-telemetry/opentelemetry-collector',
]

def norm(u):
    u = html.unescape(u or '').strip()
    u = re.sub(r'[?&]utm_[^&]*', '', u); u = re.sub(r'\?&', '?', u)
    u = re.sub(r'[?&]$', '', u); return u.rstrip('/').lower()

arch = set()
import glob
for f in glob.glob(os.path.join(REPO, '2026', '*.html')):
    raw = open(f, encoding='utf-8').read()
    for h in re.findall(r'href="([^"]+)"', raw):
        if h.startswith('http'):
            arch.add(norm(h))
    for t in re.findall(r'<h3><a [^>]*href="([^"]+)"', raw):
        arch.add(norm(t))

cutoff = datetime.datetime(2026, 11, 12, tzinfo=datetime.timezone.utc)
out = []
for repo in REPOS:
    try:
        raw = subprocess.run(['curl', '-sSL', '--max-time', '25', '-A', UA,
                              f'https://github.com/{repo}/releases.atom'],
                             capture_output=True, text=True).stdout
    except Exception as e:
        print('ERR', repo, e); continue
    entries = re.findall(r'<entry>(.*?)</entry>', raw, re.S)
    rows = []
    for e in entries:
        tag = re.search(r'<title>(.*?)</title>', e, re.S)
        link = re.search(r'<link[^>]*href="([^"]+)"', e)
        upd = re.search(r'<updated>(.*?)</updated>', e)
        if not (tag and link):
            continue
        try:
            dt = datetime.datetime.fromisoformat(upd.group(1).replace('Z', '+00:00'))
        except Exception:
            continue
        if dt < cutoff:
            continue
        rows.append((dt.date().isoformat(), tag.group(1).strip(), link.group(1)))
    rows.sort(reverse=True)
    print(f'== {repo}  ({len(rows)} recent)')
    for d, t, l in rows[:4]:
        seen = norm(l) in arch
        print(f'   {"[SEEN]" if seen else "[NEW] "} {d} {t[:50]} {l}')
        if not seen:
            out.append({'repo': repo, 'date': d, 'tag': t, 'url': l})

json.dump(out, open(os.path.join(REPO, 'gapfill_066_atom.json'), 'w'), ensure_ascii=False, indent=1)
print(f'\nNEW candidates: {len(out)}')
