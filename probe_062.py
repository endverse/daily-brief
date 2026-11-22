import re, json, subprocess, datetime
repos = ["openai/codex","google-gemini/gemini-cli","sst/opencode","stablyai/orca","anthropics/claude-code",
         "e2b-dev/E2B","daytonaio/daytona","microsandbox/microsandbox","kata-containers/kata-containers","firecracker-microvm/firecracker",
         "ai-dynamo/dynamo","NVIDIA/k8s-dra-driver-gpu","kubernetes-sigs/kserve","kubernetes-sigs/kueue","sgl-project/sglang","NVIDIA/KAI-Scheduler","vllm-project/vllm",
         "cilium/cilium","containerd/containerd","moby/buildkit","envoyproxy/envoy","istio/istio","kubernetes/kubernetes"]
out=[]
for r in repos:
    try:
        x = subprocess.run(["curl","-sSL","--max-time","25",f"https://github.com/{r}/releases.atom"],capture_output=True,text=True).stdout
    except Exception as e:
        continue
    ents = re.findall(r"<entry>(.*?)</entry>", x, re.S)
    for e in ents[:3]:
        tag = re.search(r"<title>(.*?)</title>", e, re.S)
        upd = re.search(r"<updated>(.*?)</updated>", e, re.S)
        lnk = re.search(r'<link[^>]*href="([^"]+)"', e)
        out.append({"repo":r,"tag":(tag.group(1) if tag else "").strip(),"updated":(upd.group(1) if upd else "")[:10],"url":lnk.group(1) if lnk else ""})
json.dump(out, open("atom_062.json","w"), ensure_ascii=False, indent=1)
for o in out:
    print(o["updated"], o["repo"], o["tag"], o["url"])
