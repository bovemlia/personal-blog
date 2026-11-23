"""Four histograms of proof length, each with the claimed Riemann proof marked."""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "static/data/lean-proof-lengths"
OUT = ROOT / "static/images/lean-proof-lengths"
OUT.mkdir(parents=True, exist_ok=True)

ink, muted, green, gray, grid, accent = "#172b3a", "#607485", "#087f8c", "#9eabb6", "#e7edf1", "#c2410c"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": ink, "axes.labelcolor": ink,
                     "xtick.color": muted, "ytick.color": muted, "svg.fonttype": "none"})

RH_LINES, RH_PAGES = 17_000_000, 250_000
MATHLIB_LINES = 2_382_405  # Mathlib/ total at the commit used, from famous_theorems.py


def human(x, _=None):
    for div, suf in [(1e6, "M"), (1e3, "k")]:
        if x >= div:
            v = x / div
            return f"{v:.0f}{suf}" if v >= 10 or v == int(v) else f"{v:.1f}{suf}"
    return f"{x:.0f}"


def save(fig, name):
    for ext in ["png", "svg"]:
        fig.savefig(OUT / f"{name}.{ext}", dpi=220, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def histogram(values, title, xlabel, name, xlim, marker, marker_label, refs=(), labels=(), notes=(), per_decade=4, verbose=True):
    values = np.asarray(values, dtype=float)
    # Bin edges on a fixed grid (per_decade bins per power of ten) so they line up with the ticks.
    lo, hi = np.log10(xlim)
    k = np.arange(np.floor(lo * per_decade), np.ceil(hi * per_decade) + 1)
    counts, edges = np.histogram(values, 10 ** (k / per_decade))
    if verbose:
        print(name, [(human(a), c) for a, c in zip(edges[:-1], counts) if c and a >= 1e6])

    fig = plt.figure(figsize=(9, 4.8), facecolor="white")
    ax = fig.add_axes([0.08, 0.14, 0.88, 0.70])
    fig.text(0.08, 0.93, title, fontsize=17, weight="bold")
    gap = 10 ** (0.012 / per_decade * 4)  # small fixed gap between bars in log space
    left, right = edges[:-1] * gap, edges[1:] / gap
    ax.bar(left, counts, width=right - left, align="edge", color=green, linewidth=0, zorder=3)
    ymax = max(counts.max(), 1) * 1.32
    for x, label in refs:
        ax.axvline(x, color=gray, lw=1.2, ls=(0, (3, 3)), zorder=2)
        ax.text(x * 0.88, ymax * 0.96, label, ha="right", va="top", fontsize=10, color=muted)
    ax.axvline(marker, color=accent, lw=2, zorder=4)
    ax.text(marker * 1.12, ymax * 0.96, marker_label, ha="left", va="top", fontsize=10.5, color=ink, weight="bold")
    # One label block per bar, centred on it, listing the named items in that bin.
    by_bin = {}
    for x, label in labels:
        by_bin.setdefault(np.searchsorted(edges, x, side="right") - 1, []).append(label)
    for i, names in by_bin.items():
        ax.text(np.sqrt(edges[i] * edges[i + 1]), counts[i] + ymax * 0.02, "\n".join(names),
                ha="center", va="bottom", fontsize=9, color=ink, linespacing=1.15)
    # Free-standing notes: (text, x, y as a fraction of ymax).
    for text, x, yf in notes:
        ax.text(x, ymax * yf, text, ha="left", va="top", fontsize=9, color=ink, linespacing=1.3,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5}, zorder=5)

    ax.set_xscale("log")
    ax.set(xlim=xlim, ylim=(0, ymax), xlabel=xlabel, ylabel="Count")
    ax.xaxis.set_major_locator(LogLocator(base=10, numticks=12))
    ax.xaxis.set_major_formatter(FuncFormatter(human))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.grid(axis="y", color=grid, lw=0.8)
    ax.set_axisbelow(True)
    for k in ["top", "right", "left"]:
        ax.spines[k].set_visible(False)
    ax.spines["bottom"].set_color("#cbd5dd")
    ax.tick_params(axis="y", length=0)
    save(fig, name)


LEAN_XLIM = (1, 4e8)
rh = (RH_LINES, "Claimed Riemann\nproof: 17M lines")
mathlib_ref = [(MATHLIB_LINES, "All of\nMathlib")]

famous = pd.read_csv(DATA / "famous-theorems.csv")
top = famous.nlargest(1, "closure_lines").iloc[0]
histogram(famous.closure_lines, "Famous theorems in Mathlib",
          f"Lean lines in the theorem's Mathlib import closure (n = {len(famous)}, log scale)",
          "famous-theorems-histogram", (1e3, 4e8), *rh, refs=mathlib_ref,
          notes=[(f"Largest:\nprime number\ntheorem, {human(top.closure_lines)}", 2.7e6, 0.3)])

efforts = pd.read_csv(DATA / "large-efforts.csv")
show = {"PNT+": "PNT+", "Equational theories": "Equational\ntheories", "Liquid Tensor Experiment": "Liquid\nTensor",
        "Fermat's Last Theorem": "FLT", "Carleson": "Carleson", "FLT for regular primes": "FLT\nregular\nprimes",
        "Chandra–Furst–Lipton": "Chandra–\nFurst–Lipton"}
histogram(efforts.own_lines, "Large Lean formalization projects",
          f"Lean lines written by the project, excluding Mathlib (n = {len(efforts)}, log scale)",
          "large-efforts-histogram", (1e2, 4e8), *rh, refs=mathlib_ref,
          labels=[(r.own_lines, show[r.name]) for r in efforts.itertuples() if r.name in show], per_decade=2)

res = pd.read_csv(DATA / "reservoir-packages.csv")
res = res[res.lean_lines_est > 0]
histogram(res.lean_lines_est, "Every Lean package on Reservoir",
          f"Estimated Lean lines per package (n = {len(res)}, log scale)",
          "reservoir-histogram", LEAN_XLIM, *rh, refs=mathlib_ref,
          notes=[("Above 17M:\n" + "\n".join(f"{r.repo} {human(r.lean_lines_est)}" for r in res.itertuples()
                                              if r.lean_lines_est > RH_LINES), 2.2e7, 0.62)])

wiki = pd.read_csv(DATA / "wikipedia-long-proofs.csv")
histogram(wiki.pages, "Wikipedia's list of long proofs",
          f"Pages (n = {len(wiki)}, log scale)", "wikipedia-long-proofs-histogram", (50, 1e6),
          RH_PAGES, "Claimed Riemann proof:\n250k pages (text version)",
          labels=[(15000, "Finite simple groups"), (2000, "Deligne")], per_decade=3)
print("Saved four histograms as PNG and SVG.")
