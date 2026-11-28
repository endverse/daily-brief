#!/usr/bin/env python3
"""Build spec.json for the issue-068 Feishu card from briefing.json + locked template."""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json")
brief = json.load(open(os.path.join(BASE, "briefing.json"), encoding="utf-8"))
spec = json.load(open(TPL, encoding="utf-8"))

# --- date label: "2026 年 11 月 28 日 · 星期六" -> "2026年11月28日 · 星期六"
date = brief["date_label"].replace(" 年 ", "年").replace(" 月 ", "月").replace(" 日", "日")
issue = f'{brief["issue"]:03d}'

lines = []
for i, h in enumerate(brief["highlights"], 1):
    s = re.sub(r"\s+", " ", h["summary"]).strip()
    s = s[:170].rstrip("，。、； ") + "…"
    lines.append(f'{i}. **{h["title"]}**\n{s}')
highlights = "\n\n".join(lines)

glance_lines = []
for sec in brief["sections"]:
    for c in sec["categories"]:
        first = c["items"][0]
        head = re.split(r"[：:—]", first["title"])[0]
        glance_lines.append(f'· **{c["title"]}** — {head}')
glance = "\n".join(glance_lines)

n_items = sum(len(c["items"]) for s in brief["sections"] for c in s["categories"])
n_cat = sum(len(s["categories"]) for s in brief["sections"])
count_line = (f'共 {len(brief["highlights"])} 条重点 + {n_cat} 个板块 {n_items} 条精选 '
              f'+ {len(brief["flash"])} 条快讯 · 数据源覆盖 72 小时')

page_url = f'https://endverse.github.io/daily-brief/2026/2026-11-28.html'

repl = {
    "{date}": date,
    "{issue}": issue,
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights,
    "{glance}": glance,
    "{count_line}": count_line,
    "{page_url}": page_url,
}
spec["chat_id"] = "oc_18845bcfeabb63caffa3e86c69a96d6e"

def subst(obj):
    if isinstance(obj, str):
        for k, v in repl.items():
            obj = obj.replace(k, v)
        return obj
    if isinstance(obj, list):
        return [subst(x) for x in obj]
    if isinstance(obj, dict):
        return {k: subst(v) for k, v in obj.items()}
    return obj

spec = subst(spec)

# assertions
blob = json.dumps(spec, ensure_ascii=False)
blob_wo_comment = json.dumps({k: v for k, v in spec.items() if k != "_comment"}, ensure_ascii=False)
left = re.findall(r"\{[a-z_]+\}", blob_wo_comment)
assert not left, f"unfilled placeholders: {left}"
assert spec["chat_id"] == "oc_18845bcfeabb63caffa3e86c69a96d6e"
assert "08:30" in spec["footer"], spec["footer"]
assert spec["header"]["template"] == "indigo" and spec["header"]["icon"] == "myai_colorful"
assert len(spec["blocks"]) == 4 and spec["blocks"][1]["type"] == "hr"
assert page_url in spec["button"]["url"]
assert issue in spec["header"]["subtitle"]

json.dump(spec, open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("spec.json OK")
print("subtitle:", spec["header"]["subtitle"])
print("count_line:", count_line)
print("--- highlights ---"); print(highlights)
print("--- glance ---"); print(glance)
