import re, json, subprocess, datetime
REPOS = [
 "kubernetes-sigs/kueue","kserve/kserve","llm-d/llm-d","vllm-project/vllm",
 "NVIDIA/k8s-dra-driver-gpu","ai-dynamo/dynamo","sgl-project/sglang",
 "NVIDIA/KAI-Scheduler","volcano-sh/volcano","kubernetes-sigs/lws",
 "cilium/cilium","projectcalico/calico","containerd/containerd","moby/buildkit",
 "envoyproxy/envoy","istio/istio","kubernetes-sigs/gateway-api","kubernetes/kubernetes",
 "kubeflow/trainer","ray-project/kuberay","kubernetes-sigs/jobset",
]
out=[]
for r in REPOS:
    try:
        raw = subprocess.run(["curl","-sS","--max-time","25","-A","Mozilla/5.0",
            f"https://github.com/{r}/releases.atom"],capture_output=True,text=True).stdout
        ents = re.findall(r"<entry>(.*?)</entry>", raw, re.S)
        for e in ents[:4]:
            tag = re.search(r"<title>(.*?)</title>", e, re.S)
            upd = re.search(r"<updated>(.*?)</updated>", e, re.S)
            link = re.search(r'<link[^>]*href="([^"]+)"', e)
            if tag and upd:
                out.append({"repo":r,"tag":tag.group(1).strip(),
                            "date":upd.group(1)[:10],"url":link.group(1) if link else ""})
    except Exception as ex:
        print("ERR",r,ex)
cut = (datetime.date(2026,11,7)-datetime.timedelta(days=16)).isoformat()
print("cutoff",cut)
for o in out:
    if o["date"]>=cut:
        print(o["date"], o["repo"], o["tag"], o["url"])
json.dump(out, open("gapfill_047_atom.json","w"), ensure_ascii=False, indent=1)
