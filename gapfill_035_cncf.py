import urllib.request, re, datetime
UA = {"User-Agent": "Mozilla/5.0"}
now = datetime.datetime.now(datetime.timezone.utc)
repos = ["kubernetes-sigs/karpenter", "kubernetes/autoscaler", "cert-manager/cert-manager",
         "argoproj/argo-cd", "fluxcd/flux2", "kedacore/keda",
         "open-telemetry/opentelemetry-operator", "external-secrets/external-secrets",
         "kubernetes-sigs/metrics-server", "traefik/traefik", "kubernetes-sigs/cluster-api",
         "crossplane/crossplane", "prometheus-operator/prometheus-operator"]
for repo in repos:
    try:
        raw = urllib.request.urlopen(urllib.request.Request(
            f"https://github.com/{repo}/releases.atom", headers=UA), timeout=20).read().decode("utf-8", "ignore")
    except Exception as e:
        print("##", repo, "FAIL", e)
        continue
    print("##", repo)
    for e in re.findall(r"<entry>(.*?)</entry>", raw, re.S)[:3]:
        t = re.search(r"<title>(.*?)</title>", e, re.S)
        u = re.search(r'<link[^>]*href="([^"]+)"', e)
        d = re.search(r"<updated>(.*?)</updated>", e)
        if not (t and u and d):
            continue
        try:
            dt = datetime.datetime.fromisoformat(d.group(1).replace("Z", "+00:00"))
        except Exception:
            continue
        title = re.sub(r"\s+", " ", t.group(1))[:55]
        print("   %3dd %s %s %s" % ((now - dt).days, dt.date(), title, u.group(1)))
