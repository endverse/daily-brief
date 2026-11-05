import re, subprocess, sys, html
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
def txt(url):
    raw = subprocess.run(["curl","-sSL","--max-time","30","-A",UA,url],capture_output=True,text=True).stdout
    m = re.findall(r'<article[^>]*>(.*?)</article>', raw, re.S)
    body = m[0] if m else raw
    ps = re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)
    out=[]
    for p in ps:
        t = re.sub(r'<[^>]+>','',p)
        t = html.unescape(t).strip()
        if len(t)>25: out.append(t)
    return "\n".join(out)
for u in sys.argv[1:]:
    print("#####", u)
    print(txt(u)[:3500])
