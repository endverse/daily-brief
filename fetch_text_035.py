import re, urllib.request, json
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "ignore")

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()

print("################ ARXIV ABSTRACTS")
for aid in ["2610.31576", "2610.31579", "2610.31624", "2610.31372", "2610.31586"]:
    try:
        raw = get(f"https://arxiv.org/abs/{aid}")
        m = re.search(r'<blockquote class="abstract[^"]*">(.*?)</blockquote>', raw, re.S)
        title = re.search(r'<h1 class="title[^"]*">(.*?)</h1>', raw, re.S)
        print(f"\n=== {aid} :: {clean(title.group(1)).replace('Title:','') if title else ''}")
        print(clean(m.group(1)).replace("Abstract:", "").strip()[:2200] if m else "NO ABSTRACT")
    except Exception as e:
        print(aid, "FAIL", e)
