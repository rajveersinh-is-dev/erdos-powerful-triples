"""Vectorised, complete generation of powerful numbers up to a large bound.

Key facts used (both proved in the accompanying paper):

  (F1) m is powerful  <=>  m = a^2 b^3 with b squarefree (unique), and then
         a is odd and b is odd whenever m is odd;
  (F2) for odd m, m mod 4 = b mod 4, because a is odd so a^2 = 1 (mod 8);
  (F3) if n, n+1, n+2 are all powerful then n = 3 (mod 4).

Combining (F1)-(F3): a triple exists  <=>  there is n with
    n = a^2 b^3,  a odd, b odd squarefree, b = 3 (mod 4),
    n+2 = e^2 f^3, e odd, f odd squarefree, f = 1 (mod 4).
So it suffices to intersect two explicit sets.  This is what makes very large
bounds reachable: only O(sqrt(X)/2) numbers per set are generated, not O(X).
"""

from __future__ import annotations

from dataclasses import dataclass
import time

from .predicates import is_powerful_trial, squarefree_leq
import numpy as np




__all__ = [
    "ScaleResult",
    "count_odd_powerful",
    "generate_odd_powerful_class",
    "search_triples_fast",
    "pairs_diff2_fast",
]


@dataclass
class ScaleResult:
    found: list[int]
    bound: int
    runtime_s: float
    size_p3: int
    size_p1: int
    notes: str


def _cube_root_floor(x: int) -> int:
    """Cube root floor.
    
    Args:
        x:
    
    Returns:
        The computed result
    
    """
    lo, hi = 0, 1
    while hi ** 3 <= x:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** 3 <= x:
            lo = mid
        else:
            hi = mid
    return lo


def count_odd_powerful(limit: int) -> int:
    """Number of odd powerful numbers <= limit (closed form, exact)."""
    bmax = _cube_root_floor(limit)
    total = 0
    for b in squarefree_leq(bmax):
        if b % 2 == 0:
            continue
        b3 = b ** 3
        if b3 > limit:
            continue
        a_max = int((limit // b3) ** 0.5)
        while (a_max + 1) ** 2 * b3 <= limit:
            a_max += 1
        total += (a_max + 1) // 2  # odd a in 1..a_max
    return total


def generate_odd_powerful_class(limit: int, bmod: int) -> np.ndarray:
    """All powerful m <= limit with m = 4t+bmod; returned sorted, as int64.

    Such m are exactly a^2 b^3 with a odd, b odd squarefree, b = bmod (mod 4).
    Completeness: by (F1)-(F2) every odd powerful m with m = bmod (mod 4) has this
    form, and b^3 <= limit bounds b <= limit^{1/3}.
    """
    limit = int(limit)
    bmax = _cube_root_floor(limit)
    chunks: list[np.ndarray] = []
    for b in squarefree_leq(bmax):
        if b % 4 != bmod:
            continue
        b3 = b ** 3
        a_max = int((limit // b3) ** 0.5)
        while (a_max + 1) ** 2 * b3 <= limit:
            a_max += 1
        # odd a <= a_max
        n_odd = (a_max + 1) // 2
        if n_odd == 0:
            continue
        a = np.arange(1, 2 * n_odd, 2, dtype=np.int64)
        chunks.append(a * a * np.int64(b3))
    if not chunks:
        return np.empty(0, dtype=np.int64)
    arr = np.concatenate(chunks)
    arr.sort()
    return arr


def search_triples_fast(limit: int, chunk_log: int = 24) -> ScaleResult:
    """Search for n <= limit with n, n+1, n+2 all powerful, using (F1)-(F3).

    IMPORTANT: the middle term n+1 is EVEN and is *not* a member of P1 or P3, so
    being in P3 with n+2 in P1 is NOT sufficient -- one must additionally test
    n+1.  (This was the first version of this function, and it wrongly reported
    the members of OEIS A076445 as triples; see research/falsification_log.md.)

    Completeness *within the bound*: if such n exists with n <= limit then
    n in P3 and n+2 in P1, so n is a member of the intersection and is then
    tested.  No statement is made about n > limit.
    """
    t0 = time.perf_counter()
    p3 = generate_odd_powerful_class(limit + 2, 3)
    p1 = generate_odd_powerful_class(limit + 2, 1)
    cand = np.intersect1d(p3, p1 - 2, assume_unique=True)
    found = [int(v) for v in cand if is_powerful_trial(int(v) + 1)]
    return ScaleResult(
        found=found,
        bound=int(limit),
        runtime_s=time.perf_counter() - t0,
        size_p3=int(p3.size),
        size_p1=int(p1.size),
        notes=(
            f"Intersection gave {int(cand.size)} candidate(s) with n and n+2 powerful; "
            f"after testing the middle term n+1, {len(found)} survive.  |P3|+|P1| is the "
            "number of odd powerful numbers up to limit+2."
        ),
    )


def pairs_diff2_fast(limit: int) -> tuple[list[tuple[int, int]], float]:
    """All odd powerful pairs (u, u+2) with u+2 <= limit (i.e. OEIS A076445 style)."""
    t0 = time.perf_counter()
    p3 = generate_odd_powerful_class(limit, 3)
    p1 = generate_odd_powerful_class(limit, 1)
    # pair (u, u+2): u in P1 and u+2 in P3, or u in P3 and u+2 in P1.
    common1 = np.intersect1d(p1, p3 - 2, assume_unique=True)
    common2 = np.intersect1d(p3, p1 - 2, assume_unique=True)
    pairs = sorted({(int(u), int(u) + 2) for u in common1} | {(int(u), int(u) + 2) for u in common2})
    return pairs, time.perf_counter() - t0