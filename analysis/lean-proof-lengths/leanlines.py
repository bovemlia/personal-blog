"""Shared helpers: count Lean lines and follow import graphs."""

import re
from pathlib import Path

IMPORT = re.compile(r"^(?:public\s+)?(?:meta\s+)?import\s+(?:all\s+)?([\w.«»'!?]+)")
SKIP_DIRS = {".lake", "lake-packages", "_target", ".git", "build"}


def lean_files(root: Path):
    for f in root.rglob("*.lean"):
        if not SKIP_DIRS.intersection(f.relative_to(root).parts):
            yield f


def read_lean(f: Path):
    """Return (line count, list of imported module names) for one file."""
    text = f.read_text(errors="replace").splitlines()
    imps, in_comment = [], False
    for ln in text:
        s = ln.strip()
        if in_comment:
            in_comment = "-/" not in s
            continue
        if s.startswith("/-"):
            in_comment = "-/" not in s[2:]
            continue
        s = s.split("--", 1)[0].strip()  # trailing line comment
        if not s or s == "module" or s.startswith("prelude"):
            continue
        hit = IMPORT.match(s)
        if not hit:
            break
        imps.append(hit.group(1))
    return len(text), imps


class MathlibGraph:
    """Line counts and import edges for every Mathlib/Archive/Counterexamples file."""

    SRC_DIRS = ["Mathlib", "Archive", "Counterexamples"]

    def __init__(self, mathlib: Path):
        self.root = mathlib
        self.lines, self.imports = {}, {}
        for d in self.SRC_DIRS:
            for f in (mathlib / d).rglob("*.lean"):
                m = self.module_name(f)
                self.lines[m], self.imports[m] = read_lean(f)
        for d in self.SRC_DIRS:  # root files such as Mathlib.lean (`import Mathlib`)
            if (mathlib / f"{d}.lean").exists():
                self.lines[d], self.imports[d] = read_lean(mathlib / f"{d}.lean")

    def module_name(self, path: Path) -> str:
        return ".".join(path.relative_to(self.root).with_suffix("").parts)

    def closure(self, mods):
        """All Mathlib modules reachable from `mods` (inclusive)."""
        seen, stack = set(), list(mods)
        while stack:
            cur = stack.pop()
            if cur in seen or cur not in self.lines:
                continue
            seen.add(cur)
            stack.extend(self.imports[cur])
        return seen

    def closure_lines(self, mods):
        return sum(self.lines[m] for m in self.closure(mods))

    @property
    def total_lines(self):
        return sum(v for m, v in self.lines.items() if m == "Mathlib" or m.startswith("Mathlib."))
