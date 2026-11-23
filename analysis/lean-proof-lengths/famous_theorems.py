"""Lean lines behind each famous theorem formalized in Mathlib.

Usage: famous_theorems.py MATHLIB_DIR DECLARATION_DATA_JSON

  MATHLIB_DIR   shallow clone of leanprover-community/mathlib4
  DECL_JSON     mathlib4_docs/declarations/declaration-data.bmp (it is JSON)

For each entry in Mathlib's docs/100.yaml and docs/1000.yaml that names a
Mathlib declaration, find the module(s) declaring it and sum the lines of every
Mathlib/Archive file in their transitive import closure: how much Mathlib you
would have to check to trust the theorem from scratch (Lean core, Batteries and
other upstream packages are not counted). It is an upper bound, since importing
a file brings in everything in it, not just what the proof uses.
"""

import json
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

from leanlines import MathlibGraph

mathlib = Path(sys.argv[1])
decl_data = json.loads(Path(sys.argv[2]).read_text())["declarations"]
OUT = Path(__file__).resolve().parents[2] / "static/data/lean-proof-lengths"
OUT.mkdir(parents=True, exist_ok=True)

g = MathlibGraph(mathlib)

# Archive files are not in the docs index, so fall back to searching Archive/
# for a declaration with the same last name component.
archive_text = {g.module_name(f): f.read_text(errors="replace") for f in (mathlib / "Archive").rglob("*.lean")}


def find_module(decl):
    hit = decl_data.get(decl)
    if hit:
        return hit["docLink"].split("#")[0].removeprefix("./").removesuffix(".html").replace("/", ".")
    short = re.escape(decl.split(".")[-1])
    pat = re.compile(
        rf"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
        rf"(?:theorem|lemma|def|abbrev|instance|structure|inductive)\s+(?:[\w.]*\.)?{short}\b",
        re.M,
    )
    return next((m for m, t in archive_text.items() if pat.search(t)), None)


rows, missing, upstream = [], [], []
for list_name in ["100", "1000"]:
    entries = yaml.safe_load((mathlib / f"docs/{list_name}.yaml").read_text())
    for key, v in entries.items():
        if not v:
            continue
        decls = v.get("decls") or ([v["decl"]] if v.get("decl") else [])
        if not decls:
            continue
        mods = {find_module(d) for d in decls}
        if None in mods:
            missing.append((list_name, v.get("title"), decls))
            mods.discard(None)
        outside = {m for m in mods if m not in g.lines}
        if outside:
            upstream.append((list_name, v.get("title"), sorted(outside)))
            mods -= outside
        if not mods:
            continue
        cl = g.closure(mods)
        rows.append(
            {
                "list": list_name,
                "id": key,
                "title": v.get("title"),
                "decls": " ".join(decls),
                "modules": " ".join(sorted(mods)),
                "own_file_lines": sum(g.lines[m] for m in mods),
                "closure_files": len(cl),
                "closure_lines": sum(g.lines[m] for m in cl),
            }
        )

# A theorem on both lists counts once; sorting puts the 100-list entry first.
df = pd.DataFrame(rows).sort_values("list").drop_duplicates("decls")
df = df.sort_values("closure_lines").reset_index(drop=True)
df.to_csv(OUT / "famous-theorems.csv", index=False)

print(f"Mathlib total: {g.total_lines:,} lines")
print(f"{len(df)} theorems; {len(missing)} entries with unresolved decls")
for m in missing + upstream:
    print("  skipped:", m)
print(df.closure_lines.describe().round())
