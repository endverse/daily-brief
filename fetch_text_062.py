import re, subprocess, sys, html
UA='Mozilla/5.0 (Macintosh)'
def grab(u):
    raw = subprocess.run(["curl","-sSL","--max-time","30","-A",UA,u],capture_output=True,text=True).stdout
    m = re.findall(r'<article[^>]*>(.*?)</article>', raw, re.S)
    seg = m[0] if m else raw
    ps = re.findall(r'<p[^>]*>(.*?)</p>', seg, re.S)
    txt = "\n".join(re.sub(r'<[^>]+>','',html.unescape(p)).strip() for p in ps)
    if len(txt) < 200:
        t = re.sub(r'<script.*?</script>','',raw,flags=re.S)
        t = re.sub(r'<[^>]+>','\n',t)
        txt = "\n".join(x.strip() for x in t.split("\n") if x.strip())
    return txt
for u in sys.argv[1:]:
    print("=====", u)
    print(grab(u)[:2600])
