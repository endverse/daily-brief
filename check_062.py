import json,re,glob,os
from urllib.parse import urlsplit,urlunsplit
def norm(u):
    u=u.replace("&amp;","&").strip(); s=urlsplit(u)
    q="&".join(p for p in s.query.split("&") if p and not p.startswith("utm_"))
    return urlunsplit((s.scheme,s.netloc.lower(),s.path.rstrip("/"),q,""))
seen={}
for f in glob.glob("2026/*.html"):
    for h in re.findall(r'href="([^"]+)"', open(f,encoding="utf-8",errors="ignore").read()):
        seen[norm(h)]=os.path.basename(f)
cands=[l.split() for l in """codex 0.173
gemini-cli 0.71
opencode 2.3
claude-code 2.1.330
microsandbox 0.8
kata 4.4
firecracker 1.18
e2b 2.64
kueue 0.21
sglang router
vllm 0.34
dynamo 1.5.1
kai-scheduler 0.16
cilium 1.20.5
buildkit 0.35
istio 1.32""".strip().split("\n")]
titles=[]
for f in glob.glob("2026/*.html"):
    html=open(f,encoding="utf-8",errors="ignore").read()
    for t in re.findall(r"<h3[^>]*>(.*?)</h3>",html,re.S):
        titles.append((os.path.basename(f),re.sub(r"<[^>]+>","",t).strip()))
# print archive entries matching keywords
for kw in ["codex","gemini","opencode","claude code","microsandbox","kata","firecracker","e2b","kueue","sglang","vllm","dynamo","kai-scheduler","cilium","buildkit","istio"]:
    hits=[(f,t) for f,t in titles if kw in t.lower()]
    print(f"-- {kw}: {len(hits)}")
    for f,t in hits[-4:]: print("    ",f,t[:80])
