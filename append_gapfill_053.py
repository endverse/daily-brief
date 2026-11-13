#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append issue-053 gap-fill items (agent-sandbox / OpenAI policy / vLLM blog / claude-code / kueue)
into processed.json so verify_links.py accepts them as fetched sources."""
import json, os

REPO = os.path.dirname(os.path.abspath(__file__))
extra = json.load(open(os.path.join(REPO, "gapfill_053_extra.json"), encoding="utf-8"))
proc = json.load(open(os.path.join(REPO, "processed.json"), encoding="utf-8"))
have = {it.get("url") for it in proc}
added = 0
for e in extra:
    if e["url"] in have:
        continue
    proc.append(e)
    added += 1
json.dump(proc, open(os.path.join(REPO, "processed.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("processed.json:", len(proc), "items (+%d)" % added)
