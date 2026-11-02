import sys,subprocess,re,html
def text(url):
    raw=subprocess.run(["curl","-sSL","--max-time","40","-A","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",url],capture_output=True,text=True).stdout
    m=re.findall(r'<article[^>]*>(.*?)</article>',raw,re.S)
    body=m[0] if m else raw
    ps=re.findall(r'<p[^>]*>(.*?)</p>',body,re.S)
    out=[html.unescape(re.sub('<[^>]+>','',p)).strip() for p in ps]
    out=[o for o in out if len(o)>25]
    return "\n".join(out[:40])
for u in sys.argv[1:]:
    print("=====",u)
    print(text(u)[:3500])
