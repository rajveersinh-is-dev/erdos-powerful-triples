"""Scale experiment: exhaustively search for three consecutive powerful numbers
n <= N using the two independent residue classes forced by n = 3 (mod 4).

Method (complete within the stated bound; proof sketch in scale.py):
    P3 = {a^2 b^3 <= N+2 : a odd, b odd squarefree, b = 3 mod 4}
    P1 = {a^2 b^3 <= N+2 : a odd, b odd squarefree, b = 1 mod 4}
    candidates = P3  intersect  (P1 - 2)         [n and n+2 powerful]
    triples     = { n in candidates : n+1 powerful }

The middle term n+1 is EVEN and hence never lies in P1 or P3, so it must be tested
separately.  Omitting that test is a bug that was made and caught; see
research/falsification_log.md entry F1.

Outputs results/scale_search.json with, for each bound, the exact number of
powerful numbers generated and a checksum, so the run is auditable/reproducible.
"""

from __future__ import annotations

import json
import sys
import time

import numpy as np

from powerful_triples.scale import generate_odd_powerful_class
from powerful_triples.predicates import is_powerful_trial

MOD = 1_000_003


def checksum(arr) -> int:
    return int(np.sum(arr % np.int64(MOD)) % np.int64(MOD))


def main(bounds: list[int]) -> int:
    rows = []
    for N in bounds:
        t0 = time.perf_counter()
        p3 = generate_odd_powerful_class(N + 2, 3)
        p1 = generate_odd_powerful_class(N + 2, 1)
        t_gen = time.perf_counter() - t0
        t1 = time.perf_counter()
        cand = np.intersect1d(p3, p1 - 2, assume_unique=True)
        t_hit = time.perf_counter() - t1
        t2 = time.perf_counter()
        triples = [int(v) for v in cand if is_powerful_trial(int(v) + 1)]
        t_mid = time.perf_counter() - t2
        row = {
            "N": N,
            "log10_N": len(str(N)) - 1,
            "n_P3": int(p3.size),
            "n_P1": int(p1.size),
            "odd_powerful_total": int(p3.size + p1.size),
            "checksum_P3": checksum(p3),
            "checksum_P1": checksum(p1),
            "candidates_n_and_n_plus_2": [int(v) for v in cand],
            "triples_found": triples,
            "t_generate_s": round(t_gen, 3),
            "t_intersect_s": round(t_hit, 3),
            "t_middle_test_s": round(t_mid, 3),
        }
        rows.append(row)
        print(
            f"N = 10^{row['log10_N']:<3} |P3| = {row['n_P3']:>12,}  "
            f"|P1| = {row['n_P1']:>12,}  total = {row['odd_powerful_total']:>12,}  "
            f"candidates = {len(cand):>3}  gen = {t_gen:7.2f}s  "
            f"hit = {t_hit:6.2f}s  mid = {t_mid:6.2f}s  TRIPLES = {triples}"
        )
        del p3, p1, cand
    with open("results/scale_search.json", "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=2)
    print("wrote results/scale_search.json")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:] or ["1e9", "1e10", "1e11", "1e12", "1e13", "1e14", "1e15"]
    bounds = [int(float(a)) for a in args]
    raise SystemExit(main(bounds))