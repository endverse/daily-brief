#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 058 from briefing.json + locked card template."""
import json, re, os

TPL = os.path.expanduser("~/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json")
PAGE = "https://endverse.github.io/daily-brief/2026/2026-11-18.html"
CHAT = "oc_18845bcfeabb63caffa3e86c69a96d6e"
COVER = "/Users/endverse/daily_brief_cover.png"
ISSUE = "058"

b = json.load(open("briefing.json"))
tpl = json.load(open(TPL))

def one(s, n=130):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"

hl_lines = []
for i, h in enumerate(b["highlights"], 1):
    hl_lines.append(f"{i}. **{one(h['title'], 62)}**\n{one(h['summary'], 210)}")
highlights = "\n\n".join(hl_lines)

glance_lines = []
for sec in b["sections"]:
    for cat in sec["categories"]:
        first = cat["items"][0]
        glance_lines.append(f"{cat['emoji']} **{cat['title']}**：{one(first['title'], 46)}")
glance = "\n".join(glance_lines)

n_items = len(b["highlights"]) + sum(len(c["items"]) for s in b["sections"] for c in s["categories"])
n_cat = sum(len(s["categories"]) for s in b["sections"])
count_line = (f"共 {len(b['highlights'])} 条重点 + {n_cat} 个板块 {n_items} 条精选 + "
              f"{len(b['flash'])} 条快讯 · 数据源覆盖 72 小时")

spec = json.loads(json.dumps(tpl))
spec["chat_id"] = CHAT
spec["cover_image"] = COVER
spec["header"]["subtitle"] = spec["header"]["subtitle"].replace("{date}", b["date_label"]).replace("{issue}", ISSUE)
spec["blocks"][0]["content"] = spec["blocks"][0]["content"].replace("{highlights}", highlights)
spec["blocks"][2]["content"] = spec["blocks"][2]["content"].replace("{glance}", glance)
spec["blocks"][3]["content"] = spec["blocks"][3]["content"].replace("{count_line}", count_line)
spec["button"]["url"] = PAGE
spec.pop("_comment", None)

blob = json.dumps(spec, ensure_ascii=False)
left = sorted(set(re.findall(r"\{[a-z_]+\}", blob)))
assert not left, f"residual placeholders: {left}"
assert "08:30" in spec["footer"], spec["footer"]
assert spec["chat_id"] == CHAT
assert spec["header"]["subtitle"].endswith("第058期"), spec["header"]["subtitle"]
assert spec["cover_image"] == COVER
assert spec["button"]["url"] == PAGE

json.dump(spec, open("spec.json", "w"), ensure_ascii=False, indent=1)
print("✅ spec.json written; residual placeholders:", left)
print("subtitle:", spec["header"]["subtitle"])
print("count_line:", count_line)
print("---- highlights ----\n" + highlights)
print("---- glance ----\n" + glance)
