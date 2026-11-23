import json, re, subprocess, urllib.request, datetime
repos = [
 "anthropics/claude-code","openai/codex","google-gemini/gemini-cli","sst/opencode",
 "stablyai/orca","e2b-dev/E2B","daytonaio/daytona","microsandbox/microsandbox",
 "google/gvisor","kata-containers/kata-containers","firecracker-microvm/firecracker",
 "llm-d/llm-d","kubernetes-sigs/kueue","kserve/kserve","ai-dynamo/dynamo","sgl-project/sglang",
 "NVIDIA/k8s-dra-driver-gpu","kubernetes/kubernetes","cilium/cilium","containerd/containerd",
 "kubernetes-sigs/gateway-api","volcano-sh/volcano","NVIDIA/KAI-Scheduler","HAMi-cloud/HAMi",
 "kubernetes-sigs/lws","envoyproxy/envoy","istio/istio","moby/buildkit",
]
now = datetime.datetime.now(datetime.timezone.utc)
out=[]
for r in repos:
    url=f"https://github.com/{r}/releases.atom"
    try:
        req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        x=urllib.request.urlopen(req, timeout=25).read().decode("utf-8","ignore")
    except Exception as e:
        print("ERR",r,e); continue
    ents=re.findall(r"<entry>(.*?)</entry>",x,re.S)
    for e in ents[:4]:
        t=re.search(r"<title>(.*?)</title>",e,re.S)
        u=re.search(r'<link[^>]*href="([^"]+)"',e)
        d=re.search(r"<updated>(.*?)</updated>",e)
        if not t: continue
        dt=d.group(1) if d else ""
        try:
            ts=datetime.datetime.fromisoformat(dt.replace("Z","+00:00"))
            days=(now-ts).days
        except Exception:
            days=999
        out.append({"repo":r,"tag":t.group(1).strip(),"url":u.group(1) if u else "","date":dt[:10],"days":days})
        if days<=21:
            print(f"{days:>3}d {r:<38} {t.group(1).strip()[:40]:<40} {dt[:10]}")
json.dump(out,open("atom_063.json","w"),ensure_ascii=False,indent=1)
print("total entries",len(out))
