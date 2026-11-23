#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 063 from briefing.json + the locked card template.
Only placeholders are substituted; title/icon/template/footer/block order untouched."""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json")
TPL_COPY = os.path.join(ROOT, "card-template.json")
if not os.path.exists(TPL_COPY):
    shutil.copy(TPL, TPL_COPY)

brief = json.load(open(os.path.join(ROOT, "briefing.json"), encoding="utf-8"))
spec = json.load(open(TPL_COPY, encoding="utf-8"))


def clip(text, n=2):
    parts = re.split(r"(?<=。)", text.strip())
    out = "".join(parts[:n]).strip()
    return out if len(out) <= 180 else out[:178].rstrip("，、；") + "…"


hl = [f"{i}. **{h['title']}**\n{clip(h['summary'], 2)}" for i, h in enumerate(brief["highlights"], 1)]
highlights_block = "\n\n".join(hl) if hl else "（今日无重点条目）"

glance = []
for sec in brief["sections"]:
    for cat in sec["categories"]:
        if not cat["items"]:
            continue
        glance.append(f"**{cat['title']}** · {clip(cat['items'][0]['summary'], 1)}")
glance_block = "\n\n".join(glance)

n_sec = sum(len(c["items"]) for s in brief["sections"] for c in s["categories"])
n_cat = sum(1 for s in brief["sections"] for c in s["categories"] if c["items"])
count_line = (f"共 {len(brief['highlights'])} 条重点 + {n_cat} 个板块 {n_sec} 条精选"
              f" + {len(brief['flash'])} 条快讯 · 数据源覆盖 72 小时")

issue = f"{brief['issue']:03d}"
subs = {
    "{date}": brief["date_label"],
    "{issue}": issue,
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights_block,
    "{glance}": glance_block,
    "{count_line}": count_line,
    "{page_url}": "https://endverse.github.io/daily-brief/2026/2026-11-23.html",
}

raw = json.dumps(spec, ensure_ascii=False)
for k, v in subs.items():
    esc = json.dumps(v, ensure_ascii=False)[1:-1]   # keep it valid inside a JSON string
    raw = raw.replace(k, esc)
spec = json.loads(raw)

spec["chat_id"] = "oc_18845bcfeabb63caffa3e86c69a96d6e"

chk = {k: v for k, v in spec.items() if k != "_comment"}
blob = json.dumps(chk, ensure_ascii=False)
left = sorted(set(re.findall(r"\{[a-z_]+\}", blob)))
assert not left, f"leftover placeholders: {left}"
assert "08:30" in spec["footer"], spec["footer"]
assert spec["chat_id"] == "oc_18845bcfeabb63caffa3e86c69a96d6e"
assert spec["header"]["template"] == "indigo"
assert spec["header"]["title"] == "📰 AI & 基础设施早报"
assert [b["type"] for b in spec["blocks"]] == ["markdown", "hr", "markdown", "grey"]
assert "2026-11-23" in spec["button"]["url"]

json.dump(spec, open(os.path.join(ROOT, "spec.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("spec.json written")
print("subtitle:", spec["header"]["subtitle"])
print("count_line:", count_line)
print("highlights chars:", len(highlights_block), "glance chars:", len(glance_block))
