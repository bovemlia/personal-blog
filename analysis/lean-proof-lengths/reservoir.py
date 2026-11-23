"""Lean lines in every package indexed by Lean Reservoir.

Usage: reservoir.py CACHE_DIR REPOS_DIR

Lists every metadata.json in github.com/leanprover/reservoir-index, then asks
the GitHub languages API how many bytes of Lean each package's repo holds.
Bytes are converted to lines with the bytes-per-line ratio measured on the
local clones in REPOS_DIR (Mathlib plus the large formalization projects).
API responses are cached in CACHE_DIR so reruns don't refetch. Needs `gh`.
"""

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

import pandas as pd

from leanlines import lean_files

cache, repos = Path(sys.argv[1]), Path(sys.argv[2])
cache.mkdir(parents=True, exist_ok=True)
OUT = Path(__file__).resolve().parents[2] / "static/data/lean-proof-lengths"


def gh(path):
    return json.loads(subprocess.run(["gh", "api", path], check=True, capture_output=True, text=True).stdout)


def cached(name, fetch):
    f = cache / name
    if not f.exists():
        f.write_text(json.dumps(fetch()))
    return json.loads(f.read_text())


tree = cached("index-tree.json", lambda: gh("repos/leanprover/reservoir-index/git/trees/HEAD?recursive=1"))
paths = [t["path"] for t in tree["tree"] if t["path"].endswith("/metadata.json")]
RAW = "https://raw.githubusercontent.com/leanprover/reservoir-index/HEAD/"


def package(path):
    meta = cached(path.replace("/", "__"), lambda: json.load(urlopen(RAW + quote(path))))
    src = next((s for s in meta.get("sources", []) if s.get("host") == "github"), None)
    if not src:
        return {"package": meta["fullName"], "repo": None, "stars": meta.get("stars"), "lean_bytes": None}
    repo = src["fullName"]

    def langs():
        try:
            return gh(f"repos/{repo}/languages")
        except subprocess.CalledProcessError:
            return {"_error": True}

    lang = cached("lang__" + repo.replace("/", "__") + ".json", langs)
    return {
        "package": meta["fullName"],
        "repo": repo,
        "description": meta.get("description"),
        "stars": meta.get("stars"),
        "lean_bytes": None if "_error" in lang else lang.get("Lean", 0),
    }


with ThreadPoolExecutor(16) as pool:
    df = pd.DataFrame(pool.map(package, paths))

# Bytes per line, measured on code we have locally.
nbytes = nlines = 0
for d in repos.iterdir():
    if d.is_dir():
        for f in lean_files(d):
            b = f.read_bytes()
            nbytes += len(b)
            nlines += b.count(b"\n")
ratio = nbytes / nlines
df["lean_lines_est"] = (df.lean_bytes / ratio).round()
df = df.sort_values("lean_lines_est", ascending=False)
df.to_csv(OUT / "reservoir-packages.csv", index=False)

ok = df[df.lean_lines_est > 0]
print(f"{len(paths)} packages; {len(ok)} with Lean code on GitHub; {df.lean_bytes.isna().sum()} unreachable")
print(f"bytes per line: {ratio:.1f}")
print(ok.lean_lines_est.describe().round())
print(ok[["package", "lean_lines_est", "stars"]].head(12).to_string(index=False))
