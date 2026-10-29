import json
p='processed.json'
d=json.load(open(p))
have={i['url'] for i in d}
add=[
 {"title":"Kubernetes v1.38.0-alpha.3 与 1.37.2 / 1.36.6 / 1.35.10 / 1.34.13 同日发布","url":"https://github.com/kubernetes/kubernetes/releases/tag/v1.38.0-alpha.3","summary":"10 月 28 日 Kubernetes 同时放出 1.38 开发线的 alpha.3 与四条受支持线（1.37.2 / 1.36.6 / 1.35.10 / 1.34.13）的补丁版本。","published":"2026-10-28T00:00:00+00:00","source":"Kubernetes Releases","source_cat":"K8s","extra":{},"board":"基础设施","category":"K8s 核心","oss":True,"hot_score":8,"is_hot":False},
 {"title":"Calico v3.32.3：eBPF 策略程序被内核 verifier 拒绝致节点 NotReady 等一批修复","url":"https://github.com/projectcalico/calico/releases/tag/v3.32.3","summary":"Calico v3.32.3 于 10 月 26 日发布，修掉 eBPF 数据面策略程序被内核 verifier 判 unreachable insn 导致节点 NotReady、IPv6 conntrack NAT 反向条目不过期等问题。","published":"2026-10-26T00:00:00+00:00","source":"Calico Releases","source_cat":"K8s","extra":{},"board":"基础设施","category":"K8s 核心","oss":True,"hot_score":8,"is_hot":False},
 {"title":"Envoy v1.40.2 补丁发布","url":"https://github.com/envoyproxy/envoy/releases/tag/v1.40.2","summary":"Envoy 1.40.2 于 10 月 27 日发布，同时 1.39.6 / 1.38.9 / 1.37.11 各线补丁跟进。","published":"2026-10-27T00:00:00+00:00","source":"Envoy Releases","source_cat":"CloudNative","extra":{},"board":"基础设施","category":"云原生周边","oss":True,"hot_score":5,"is_hot":False},
 {"title":"Istio 1.32.0-rc.0 发布","url":"https://github.com/istio/istio/releases/tag/1.32.0-rc.0","summary":"Istio 1.32 首个 RC 于 10 月 28 日发布，1.31.3 / 1.30.7 / 1.29.10 同期发补丁。","published":"2026-10-28T00:00:00+00:00","source":"Istio Releases","source_cat":"CloudNative","extra":{},"board":"基础设施","category":"云原生周边","oss":True,"hot_score":5,"is_hot":False},
]
n=0
for a in add:
    if a['url'] not in have:
        d.append(a); have.add(a['url']); n+=1
json.dump(d,open(p,'w'),ensure_ascii=False,indent=1)
print('appended',n,'total',len(d))
