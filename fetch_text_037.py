#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch article bodies for issue 037 candidates -> /tmp/t037/*.txt"""
import subprocess, re, html, os, sys

OUT = "/tmp/t037"
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"

TARGETS = {
    "terra": "https://simonwillison.net/2026/Oct/26/gpt-61-terra/",
    "greptile": "https://openai.com/index/greptile-code-review-codex-astra",
    "linux_foundation_pr": "https://www.infoq.cn/article/9TSuUDxrUSGS26XTA2yB",
    "huajiao_agents": "https://www.infoq.cn/article/O7lcxqKD2avRPbNoMmtg",
    "touyan_agent": "https://www.infoq.cn/article/NrUkJExfuuFOICsjVYbb",
    "qcon_sh": "https://www.infoq.cn/article/0C1Wgt7N9NzM6KjHSFeA",
    "softdev_org": "https://www.infoq.cn/article/b32Mw2zaPrxyJ6ChePD5",
    "backstage": "https://www.infoq.cn/article/hilBQCk7QcvclfrgZbSf",
    "tf_gcp": "https://www.infoq.cn/article/qJB2DapLThovtxzyOtKW",
    "kolab": "https://arxiv.org/abs/2610.21109",
    "iam_helper": "https://cloud.google.com/blog/products/identity-security/scale-agents-securely-with-iam-helper-agent-skills-and-mcp-tools",
    "skillspector": "https://raw.githubusercontent.com/NVIDIA/SkillSpector/main/README.md",
    "tig": "https://huggingface.co/papers/2610.31931",
    "onpolicy_selftrain": "https://huggingface.co/papers/2610.32770",
    "biometric": "https://arxiv.org/abs/2610.25118",
}

def strip(raw):
    raw = re.sub(r"<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<header.*?</header>|<footer.*?</footer>",
                 " ", raw, flags=re.S | re.I)
    m = re.findall(r"<article[^>]*>(.*?)</article>", raw, re.S)
    body = m[0] if m else raw
    body = re.sub(r"<[^>]+>", "\n", body)
    body = html.unescape(body)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\n\s*\n+", "\n\n", body)
    return body.strip()

for name, url in TARGETS.items():
    try:
        r = subprocess.run(["curl", "-sSL", "-A", UA, "--max-time", "30", url],
                           capture_output=True, text=True, timeout=40)
        raw = r.stdout
        if url.endswith(".md"):
            txt = raw
        else:
            txt = strip(raw)
        open(f"{OUT}/{name}.txt", "w", encoding="utf-8").write(txt)
        print(f"{name}: {len(txt)} chars  <- {url}")
    except Exception as e:
        print(f"{name}: FAIL {e}")
