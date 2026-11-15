import subprocess, re, datetime
repos = [
 "stablyai/orca","anthropics/claude-code","openai/codex","google-gemini/gemini-cli","sst/opencode",
 "e2b-dev/E2B","daytonaio/daytona","microsandbox/microsandbox","google/gvisor","kata-containers/kata-containers",
 "kubernetes-sigs/agent-sandbox","ai-dynamo/dynamo","vllm-project/vllm","llm-d/llm-d",
 "kubernetes-sigs/kueue","kserve/kserve","NVIDIA/k8s-dra-driver-gpu","NVIDIA/KAI-Scheduler",
 "kubernetes/kubernetes","cilium/cilium","projectcalico/calico","containerd/containerd","istio/istio",
]
for r in repos:
    try:
        raw = subprocess.run(["curl","-sSL","--max-time","25",f"https://github.com/{r}/releases.atom"],capture_output=True,text=True).stdout
        ents = re.findall(r"<entry>(.*?)</entry>", raw, re.S)
        print(f"### {r}  entries={len(ents)}")
        for e in ents[:4]:
            t = re.search(r"<title[^>]*>(.*?)</title>", e, re.S)
            u = re.search(r'<link[^>]*href="([^"]+)"', e)
            d = re.search(r"<updated>(.*?)</updated>", e)
            print("   ", (d.group(1)[:10] if d else "?"), "|", (t.group(1).strip()[:60] if t else "?"), "|", (u.group(1) if u else "?"))
    except Exception as ex:
        print("###", r, "ERR", ex)
