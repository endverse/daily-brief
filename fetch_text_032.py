#!/usr/bin/env python3
"""Fetch article text for shortlisted URLs → scratch files."""
import urllib.request, re, sys, os, html

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
urls = {
 "cncf_aisre": "https://www.cncf.io/blog/2026/10/21/before-you-evaluate-an-ai-sre-give-your-existing-agent-context/",
 "gke_zenteiq": "https://cloud.google.com/blog/products/containers-kubernetes/zenteiq-scales-physical-ai-inference-4x-with-gke-and-llm-d/",
 "infoq_clef": "https://www.infoq.cn/article/iqCrZLLizNkRTpfo2Jrb",
 "infoq_deepseek": "https://www.infoq.cn/article/NBXP966Bz3eqr6Qidvaf",
 "infoq_dbguard": None,
 "aws_airgap": "https://aws.amazon.com/blogs/containers/automating-secure-container-registry-management-for-air-gapped-aws-workloads/",
 "cncf_autoscale": "https://www.cncf.io/blog/2026/10/19/how-ai-workloads-are-reshaping-kubernetes-autoscaling/",
}
os.makedirs('scratch', exist_ok=True)
for name, u in urls.items():
    if not u:
        continue
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"})
        raw = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'ignore')
    except Exception as e:
        print(f"ERR {name}: {e}")
        continue
    arts = re.findall(r'<article[^>]*>(.*?)</article>', raw, re.S)
    body = arts[0] if arts else raw
    ps = [html.unescape(re.sub(r'<[^>]+>', '', p)).strip() for p in re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)]
    text = '\n'.join(p for p in ps if len(p) > 30)
    if len(text) < 500:
        ps = [html.unescape(re.sub(r'<[^>]+>', '', p)).strip() for p in re.findall(r'<p[^>]*>(.*?)</p>', raw, re.S)]
        text = '\n'.join(p for p in ps if len(p) > 30)
    open(f'scratch/{name}.txt', 'w').write(text)
    print(f"OK {name} {len(text)} chars")
