"""Lean lines in the large single-result formalization projects.

Usage: large_efforts.py REPOS_DIR

REPOS_DIR holds shallow clones of each repo below (named after the repo) plus
mathlib4. The list is the theorem-targeted subset of the Lean community's
"Lean projects" page (leanprover-community.github.io/lean_projects.html);
libraries, courses, tooling and definition-only projects on that page are left
out. For each project we report its own .lean lines and, for Lean 4 projects,
its own lines plus the Mathlib import closure of everything it imports.
"""

import sys
from pathlib import Path

import pandas as pd

from leanlines import MathlibGraph, lean_files, read_lean

PROJECTS = [
    # repo, short name, what it targets (from the projects page), lean version
    ("ImperialCollegeLondon/FLT", "Fermat's Last Theorem", "Fermat's Last Theorem (ongoing)", 4),
    ("AlexKontorovich/PrimeNumberTheoremAnd", "PNT+", "Prime number theorem and strong forms", 4),
    ("teorth/equational_theories", "Equational theories", "Full implication graph of 4694 magma laws", 4),
    ("teorth/pfr", "PFR conjecture", "Polynomial Freiman–Ruzsa conjecture", 4),
    ("fpvandoorn/carleson", "Carleson", "Carleson's theorem", 4),
    ("thefundamentaltheor3m/Sphere-Packing-Lean", "Sphere packing (dim 8)", "Viazovska's sphere packing in dimension 8", 4),
    ("leanprover-community/flt-regular", "FLT for regular primes", "Kummer's FLT for regular primes", 4),
    ("RemyDegenne/brownian-motion", "Brownian motion", "Construction of Brownian motion", 4),
    ("leanprover-community/sphere-eversion", "Sphere eversion", "Existence of sphere eversions (h-principle)", 4),
    ("Ivan-Sergeyev/seymour", "Seymour decomposition", "Seymour's decomposition of regular matroids", 4),
    ("math-xmum/Brouwer", "Brouwer / Nash", "Brouwer fixed point and Nash equilibria via Scarf", 4),
    ("YaelDillies/apap", "Kelley–Meka", "Kelley–Meka bound on 3-AP-free sets", 4),
    ("YaelDillies/chandra-furst-lipton", "Chandra–Furst–Lipton", "Corner-free sets and communication complexity", 4),
    ("Paul-Lez/PersistentDecomp", "Persistence modules", "Structure theorem for persistence modules", 4),
    ("leanprover-community/con-nf", "Consistency of NF", "Consistency of Quine's New Foundations", 4),
    ("leanprover-community/lean-liquid", "Liquid Tensor Experiment", "Scholze's main theorem of liquid modules", 3),
    ("flypitch/flypitch", "Flypitch", "Independence of the continuum hypothesis", 3),
    ("b-mehta/unit-fractions", "Unit fractions", "Bloom's density result for unit fractions", 3),
]

repos = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[2] / "static/data/lean-proof-lengths"
g = MathlibGraph(repos / "mathlib4")

rows = []
for repo, name, proves, lean in PROJECTS:
    root = repos / repo.split("/")[1]
    own, mathlib_imports = 0, set()
    for f in lean_files(root):
        n, imps = read_lean(f)
        own += n
        mathlib_imports.update(i for i in imps if i == "Mathlib" or i.startswith("Mathlib."))
    closure = g.closure_lines(mathlib_imports) if lean == 4 else None
    rows.append(
        {
            "repo": repo,
            "name": name,
            "proves": proves,
            "lean_version": lean,
            "own_lines": own,
            "imports_all_mathlib": "Mathlib" in mathlib_imports,
            "mathlib_closure_lines": closure,
            "total_lines": own + closure if closure is not None else None,
        }
    )

df = pd.DataFrame(rows).sort_values("own_lines", ascending=False)
df.to_csv(OUT / "large-efforts.csv", index=False)
print(df[["name", "lean_version", "imports_all_mathlib", "own_lines", "mathlib_closure_lines", "total_lines"]].to_string(index=False))
