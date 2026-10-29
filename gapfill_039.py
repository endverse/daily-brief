import subprocess, re, json, datetime, glob, urllib.parse
repos = ["kubernetes-sigs/kueue","kserve/kserve","llm-d/llm-d","Project-HAMi/HAMi","NVIDIA/k8s-dra-driver-gpu","ai-dynamo/dynamo","sgl-project/sglang","volcano-sh/volcano","kubernetes-sigs/lws","kubernetes/kubernetes","kubernetes-sigs/gateway-api","cilium/cilium","containerd/containerd","envoyproxy/envoy","istio/istio","moby/buildkit","projectcalico/calico","NVIDIA/gpu-operator","kubernetes-sigs/karpenter","ray-project/kuberay"]
cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=16)
out=[]
for r in repos:
    try:
        raw = subprocess.run(["curl","-sSL","--max-time","25",f"https://github.com/{r}/releases.atom"],capture_output=True,text=True).stdout
    except Exception as e:
        print("ERR",r,e); continue
    entries = re.findall(r"<entry>(.*?)</entry>", raw, re.S)
    for e in entries[:6]:
        t = re.search(r"<title>(.*?)</title>", e, re.S)
        u = re.search(r'<link[^>]*href="([^"]+)"', e)
        up = re.search(r"<updated>(.*?)</updated>", e)
        if not (t and u and up): continue
        try: dt = datetime.datetime.fromisoformat(up.group(1).replace("Z","+00:00"))
        except: continue
        if dt < cutoff: continue
        out.append({"repo":r,"title":t.group(1).strip(),"url":u.group(1),"date":dt.strftime("%Y-%m-%d")})
for o in sorted(out,key=lambda x:x["date"],reverse=True):
    print(o["date"], o["repo"], o["title"][:60], o["url"])
json.dump(out,open("gapfill_039_atom.json","w"),ensure_ascii=False,indent=1)
