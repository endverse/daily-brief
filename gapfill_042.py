import subprocess, re, json, datetime
repos = ["kubernetes-sigs/kueue","kserve/kserve","llm-d/llm-d","Project-HAMi/HAMi","NVIDIA/k8s-dra-driver-gpu","ai-dynamo/dynamo","sgl-project/sglang","volcano-sh/volcano","kubernetes-sigs/lws","kubernetes/kubernetes","kubernetes-sigs/gateway-api","cilium/cilium","containerd/containerd","envoyproxy/envoy","istio/istio","moby/buildkit","projectcalico/calico","NVIDIA/gpu-operator","kubernetes-sigs/karpenter","ray-project/kuberay","kubernetes-sigs/kwok","kubernetes-sigs/cluster-api","argoproj/argo-cd","kubernetes/ingress-nginx","kubernetes-sigs/metrics-server","kubernetes-sigs/kubespray","open-telemetry/opentelemetry-collector","kedacore/keda","kubernetes-sigs/kueue","kubernetes-sigs/jobset","kubernetes-sigs/node-feature-discovery","kubernetes-sigs/dra-driver-samples","NVIDIA/nvidia-container-toolkit","kubernetes-sigs/kubeflow","kubeflow/katib","kubeflow/training-operator"]
cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)
out=[]
for r in dict.fromkeys(repos):
    raw = subprocess.run(["curl","-sSL","--max-time","25",f"https://github.com/{r}/releases.atom"],capture_output=True,text=True).stdout
    for e in re.findall(r"<entry>(.*?)</entry>", raw, re.S)[:8]:
        t = re.search(r"<title>(.*?)</title>", e, re.S)
        u = re.search(r'<link[^>]*href="([^"]+)"', e)
        up = re.search(r"<updated>(.*?)</updated>", e)
        if not (t and u and up): continue
        try: dt = datetime.datetime.fromisoformat(up.group(1).replace("Z","+00:00"))
        except: continue
        if dt < cutoff: continue
        out.append({"repo":r,"title":t.group(1).strip(),"url":u.group(1),"date":dt.strftime("%Y-%m-%d")})
for o in sorted(out,key=lambda x:x["date"],reverse=True):
    print(o["date"], o["repo"], o["title"][:65], o["url"])
json.dump(out,open("gapfill_042_atom.json","w"),ensure_ascii=False,indent=1)
