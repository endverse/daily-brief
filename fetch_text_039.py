import subprocess, re, html, sys, json
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
urls={
 'anthropic_breach':'https://www.infoq.cn/article/mFXr0u4z0XftUGUg5Wm7',
 'hire_agents':'https://www.infoq.cn/article/II91QKxeaEg7RuZR2rrf',
 'aws_agent_oss':'https://www.infoq.cn/article/YmgmEh686wTClmj3PY8o',
 'instagram':'https://www.infoq.cn/article/bXKVgLdpf7HONYHIi6Su',
 'diffusion35b':'https://www.infoq.cn/article/0tgCLAMXFiFo0Dco5P9m',
 'agent_gov':'https://www.infoq.cn/article/CxWoiprQltg8YXmwmghd',
 'gke_net':'https://cloud.google.com/blog/products/networking/gke-networking-dataplane-for-large-agentic-ai-workloads',
 'gcp_skills':'https://cloud.google.com/blog/topics/developers-practitioners/behind-the-scenes-two-months-later-how-we-ship-google-agent-skills-like-products',
 'gemini4carbon':'https://deepmind.google/blog/gemini-4-carbon-our-next-frontier-model/',
 'octoverse':'https://simonwillison.net/2026/Oct/28/github-octoverse-2026/',
 'volcano':'https://www.cncf.io/blog/2026/10/28/volcano-v1-16-released-namespacequeue-fairshare-and-a-broader-hypernode-ecosystem/',
}
def strip(h):
    h=re.sub(r'<script.*?</script>','',h,flags=re.S)
    h=re.sub(r'<style.*?</style>','',h,flags=re.S)
    ps=re.findall(r'<p[^>]*>(.*?)</p>',h,re.S)
    txt=' '.join(html.unescape(re.sub(r'<[^>]+>','',p)).strip() for p in ps)
    return re.sub(r'\s+',' ',txt)
out={}
for k,u in urls.items():
    raw=subprocess.run(['curl','-sSL','--max-time','30','-A',UA,u],capture_output=True,text=True).stdout
    art=re.findall(r'<article[^>]*>(.*?)</article>',raw,re.S)
    body = strip(art[0]) if art else strip(raw)
    out[k]=body
    print('='*20,k,len(body))
    print(body[:2600])
json.dump(out,open('/tmp/t039.json','w'),ensure_ascii=False)
