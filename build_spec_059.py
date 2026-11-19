#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build spec.json for issue 059 from briefing.json + the locked card template."""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.expanduser("~/code/endverse/skills/skills/workflows/daily-brief/templates/card-template.json")
TPL_COPY = os.path.join(ROOT, "card-template.json")

if not os.path.exists(TPL_COPY):
    shutil.copy(TPL, TPL_COPY)

brief = json.load(open(os.path.join(ROOT, "briefing.json"), encoding="utf-8"))
spec = json.load(open(TPL_COPY, encoding="utf-8"))

# 1) highlights block: numbered bold title + condensed summary first sentences
def clip(text, n=2):
    parts = re.split(r"(?<=。)", text.strip())
    out = "".join(parts[:n]).strip()
    return out if len(out) <= 180 else out[:178].rstrip("，、；") + "…"

hl_lines = []
for i, h in enumerate(brief["highlights"], 1):
    hl_lines.append(f"{i}. **{h['title']}**\n{clip(h['summary'], 2)}")
highlights_block = "\n\n".join(hl_lines) if hl_lines else "（今日无重点条目）"

# 2) glance block: per category emoji + bold label + first bullet's gist
glance_lines = []
for sec in brief["sections"]:
    for cat in sec["categories"]:
        items = cat["items"]
        if not items:
            continue
        gist = clip(items[0]["summary"], 1)
        glance_lines.append(f"{cat['emoji']} **{cat['title']}** · {gist}")
glance_block = "\n\n".join(glance_lines)

# 3) count line
n_sec = sum(len(c["items"]) for s in brief["sections"] for c in s["categories"])
n_cat = sum(1 for s in brief["sections"] for c in s["categories"] if c["items"])
count_line = (f"共 {len(brief['highlights'])} 条重点 + {n_cat} 个板块 {n_sec} 条精选"
              f" + {len(brief['flash'])} 条快讯 · 数据源覆盖 72 小时")

page = f"https://endverse.github.io/daily-brief/2026/2026-11-19.html"

subs = {
    "{date}": brief["date_label"].replace(" · ", " · "),
    "{issue}": f"{brief['issue']:03d}",
    "{cover}": "/Users/endverse/daily_brief_cover.png",
    "{highlights}": highlights_block,
    "{glance}": glance_block,
    "{count_line}": count_line,
    "{page_url}": page,
    "{date}·第": "{date}·第",
}

raw = json.dumps(spec, ensure_ascii=False)
raw = raw.replace("{date}", subs["{date}"]).replace("{issue}", subs["{issue}"])
raw = json.dumps(json.loads(raw), ensure_ascii=False)  # noop safety
spec = json.loads(raw)

spec["header"]["subtitle"] = f"{subs['{date}']} · 第{subs['{issue}']}期"
spec["cover_image"] = subs["{cover}"]
spec["blocks"][0]["content"] = "**🔥 今日重点**\n\n" + highlights_block
spec["blocks"][2]["content"] = "**📌 今日看点**\n\n" + glance_block
spec["blocks"][3]["content"] = count_line
spec["button"]["url"] = page
spec["chat_id"] = "oc_18845bcfeabb63caffa3e86c69a96d6e"

chk = {k: v for k, v in spec.items() if k != "_comment"}
blob = json.dumps(chk, ensure_ascii=False)
left = sorted(set(re.findall(r"\{[a-z_]+\}", blob)))
assert not left, f"leftover placeholders: {left}"
assert "08:30" in spec["footer"], spec["footer"]
assert spec["chat_id"] == "oc_18845bcfeabb63caffa3e86c69a96d6e"
assert spec["header"]["template"] == "indigo"
assert [b["type"] for b in spec["blocks"]] == ["markdown", "hr", "markdown", "grey"]

json.dump(spec, open(os.path.join(ROOT, "spec.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("spec.json written")
print("subtitle:", spec["header"]["subtitle"])
print("count_line:", count_line)
print("highlights len:", len(highlights_block), "glance len:", len(glance_block))
