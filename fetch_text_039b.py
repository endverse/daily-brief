import subprocess, re, html, json
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
urls={
 'terra_qbit':'https://www.qbitai.com/2026/10/505719.html',
 'ling_infoq':'https://www.infoq.cn/article/wIuu0NSaLSaqJJpXVExD',
 'calico_notes':'https://raw.githubusercontent.com/projectcalico/calico/v3.32.3/CHANGELOG.md',
 'istio_notes':'https://raw.githubusercontent.com/istio/istio/1.32.0-rc.0/releasenotes/notes/1.32.0.yaml',
}
def strip(h):
    h=re.sub(r'<script.*?</script>','',h,flags=re.S); h=re.sub(r'<style.*?</style>','',h,flags=re.S)
    ps=re.findall(r'<p[^>]*>(.*?)</p>',h,re.S)
    return re.sub(r'\s+',' ',' '.join(html.unescape(re.sub(r'<[^>]+>','',p)).strip() for p in ps))
for k,u in urls.items():
    raw=subprocess.run(['curl','-sSL','--max-time','30','-A',UA,u],capture_output=True,text=True).stdout
    art=re.findall(r'<article[^>]*>(.*?)</article>',raw,re.S)
    body=strip(art[0]) if art else (raw[:3000] if k.endswith('notes') else strip(raw))
    print('='*15,k,len(body)); print(body[:1800]); print()
