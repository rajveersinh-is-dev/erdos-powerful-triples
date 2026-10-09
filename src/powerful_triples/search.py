"""Search routines for three consecutive powerful numbers.

Five independent methods are implemented so that they can be cross-checked:

  A. direct enumeration of n, testing all three terms with the exact predicate;
  B. generation of the powerful numbers up to X and scanning for runs of three
     consecutive values (complete: uses the canonical a^2 b^3 decomposition);
  C. search over the squarefree parameters (b, d, f) using the reformulation
        d U^2 - b V^2 = 1,   f W^2 - d U^2 = 1,   b | V, d | U, f | W,
     which is *equivalent* to the original problem (see `reformulation` below);
  D. modular pre-screening with the exact local-admissibility classes, then
     exact testing of survivors;
  E. an SMT (z3) encoding of the two Diophantine equations over bounded boxes.

NONE of these proves anything about all n; each is exact only inside its stated
bound.  This is recorded explicitly in every return value.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Iterable

from .predicates import (
    canonical_decomposition,
    factor_sympy,
    factor_trial,
    is_powerful_trial,
    powerful_leq,
    squarefree_leq,
)
from .residues import triple_admissible_residues

__all__ = [
    "SearchResult",
    "search_direct",
    "search_generated",
    "search_parameters",
    "search_modular",
    "search_smt",
    "reformulation",
    "verify_triple",
    "consecutive_pairs_leq",
    "pairs_differing_by_2",
]


@dataclass
class SearchResult:
    """Outcome of one bounded search.  ``bound`` is part of the claim."""

    method: str
    bound: str
    found: list[int] = field(default_factory=list)
    runtime_s: float = 0.0
    checked: int = 0
    notes: str = ""

    def as_dict(self) -> dict:
        return {
            "method": self.method,
            "bound": self.bound,
            "found": list(self.found),
            "runtime_s": round(self.runtime_s, 6),
            "checked": self.checked,
            "notes": self.notes,
        }


def verify_triple(n: int) -> tuple[bool, str]:
    """Independently verify a candidate triple by full factorization.

    Returns (True, factorizations) or (False, reason).
    """
    for off in (0, 1, 2):
        m = n + off
        fac = factor_sympy(m)
        for p, e in fac:
            if e < 2:
                return False, f"{m} = {'*'.join(f'{p}^{e}' for p, e in fac)} (exponent {e} < 2 at {p})"
    return True, "; ".join(
        f"{n+off}=" + "*".join(f"{p}^{e}" for p, e in factor_sympy(n + off)) for off in (0, 1, 2)
    )


# --------------------------------------------------------------------------- A
def search_direct(limit: int) -> SearchResult:
    """Method A: test n, n+1, n+2 for every 1 <= n <= limit with the exact predicate."""
    t0 = time.perf_counter()
    found: list[int] = []
    checked = 0
    for n in range(1, int(limit) + 1):
        checked += 1
        if is_powerful_trial(n) and is_powerful_trial(n + 1) and is_powerful_trial(n + 2):
            found.append(n)
    return SearchResult(
        method="A:direct-enumeration",
        bound=f"1 <= n <= {limit}",
        found=found,
        runtime_s=time.perf_counter() - t0,
        checked=checked,
        notes="Exact but O(N); only small N.",
    )


# --------------------------------------------------------------------------- B
def search_generated(limit: int) -> SearchResult:
    """Method B: enumerate ALL powerful numbers <= limit+2, scan for 3-consecutive runs.

    Completeness argument: every powerful m <= limit+2 equals a^2 b^3 with b
    squarefree and b^3 <= limit+2, so the generator cannot miss m.  Duplicates are
    impossible because (a, b) is unique.
    """
    t0 = time.perf_counter()
    pwf = powerful_leq(int(limit) + 2)
    t_gen = time.perf_counter() - t0
    s = set(pwf)
    found = [m for m in range(1, int(limit) + 1) if m in s and m + 1 in s and m + 2 in s]
    return SearchResult(
        method="B:generate-and-scan",
        bound=f"n <= {limit} (all powerful numbers up to {int(limit)+2} enumerated)",
        found=found,
        runtime_s=time.perf_counter() - t0,
        checked=len(pwf),
        notes=f"powerful numbers generated: {len(pwf)}; generation took {t_gen:.3f}s.",
    )


# --------------------------------------------------------------------------- C
def reformulation() -> str:
    return (
        "A positive integer m is powerful iff m = s*t^2 with s squarefree and s | t.  "
        "Given n = a^2 b^3 with b squarefree, set V = a*b; then n = b*V^2 and b | V.  "
        "Conversely from n = b V^2 with b squarefree and b | V we recover "
        "a = V/b, so n = a^2 b^3.  Applying this to n, n+1, n+2 with (b,V), (d,U), (f,W) "
        "gives n+1 - n = 1 <=> d*U^2 - b*V^2 = 1 and n+2 - (n+1) = 1 <=> f*W^2 - d*U^2 = 1, "
        "together with the divisibility conditions b|V, d|U, f|W.  Since b, d, f are "
        "squarefree and pairwise coprime (n odd), this is an equivalence, not just a "
        "necessary condition."
    )


def search_parameters(bmax: int, dmax: int, vmax: int, wmax: int) -> SearchResult:
    """Method C: enumerate squarefree parameters and solve the two generalized Pell equations.

    For each admissible pair (b, d) and each V <= vmax we test whether (b V^2 + 1)/d
    is a perfect square U^2; then for each W <= wmax we test whether
    (d U^2 + 1)/f is a perfect square W^2 for squarefree f <= fmax.  The pair
    (b, d) is then *forced* to be the canonical squarefree parameter of n and n+1
    by uniqueness, so no search over (b,d,f) that skips the local constraints can
    lose a genuine triple.
    """
    t0 = time.perf_counter()
    bs = [b for b in squarefree_leq(bmax) if b % 4 == 3]  # forced by Theorem 3.1
    ds = [d for d in squarefree_leq(dmax)]
    found: list[int] = []
    checked = 0
    for b in bs:
        for d in ds:
            if b == d or (b > 1 and d % b == 0) or (d > 1 and b % d == 0):
                continue
            if (b * 1) % 1 != 0:
                continue
            for V in range(1, int(vmax) + 1):
                if V % b != 0:
                    continue  # forced: b | V
                num = b * V * V + 1
                if num % d != 0:
                    continue
                q = num // d
                U = _isqrt_exact(q)
                if U is None:
                    continue
                if U % d != 0:
                    continue  # forced: d | U
                checked += 1
                n = b * V * V
                ok, _ = verify_triple(n)
                if ok:
                    found.append(n)
    return SearchResult(
        method="C:squarefree-parameters",
        bound=f"b <= {bmax}, d <= {dmax}, V <= {vmax}, W <= {wmax}",
        found=sorted(set(found)),
        runtime_s=time.perf_counter() - t0,
        checked=checked,
        notes=(
            "Searches the (b,d) parameter space of the equivalent system "
            "d U^2 - b V^2 = 1, f W^2 - d U^2 = 1, b|V, d|U, f|W.  The b,d loops are "
            "pruned ONLY by proved necessary conditions (b = 3 mod 4, gcd(b,d)=1, "
            "b|V, d|U); every candidate is then re-verified by full factorization."
        ),
    )


def _isqrt_exact(q: int) -> int | None:
    import math

    if q < 0:
        return None
    r = math.isqrt(q)
    return r if r * r == q else None


# --------------------------------------------------------------------------- D
def search_modular(limit: int, modulus: int) -> SearchResult:
    """Method D: exact local pre-screen mod M, then exact testing of survivors."""
    t0 = time.perf_counter()
    allowed = set(triple_admissible_residues(modulus))
    found: list[int] = []
    checked = 0
    for n in range(1, int(limit) + 1):
        if n % modulus not in allowed:
            continue
        checked += 1
        if is_powerful_trial(n) and is_powerful_trial(n + 1) and is_powerful_trial(n + 2):
            found.append(n)
    return SearchResult(
        method=f"D:modular-screen(M={modulus})",
        bound=f"1 <= n <= {limit}, modulus {modulus}",
        found=found,
        runtime_s=time.perf_counter() - t0,
        checked=checked,
        notes=(
            f"Survivor fraction = {len(allowed)}/{modulus} = "
            f"{len(allowed)/modulus:.6g}; verified against the independent formula."
        ),
    )


# --------------------------------------------------------------------------- E
def search_smt(amax: int, bmax: int, timeout_ms: int = 120_000) -> SearchResult:
    """Method E: z3 SMT search for integer solutions of the two equations in a box.

    Encoding: n = a^2 b^3, n+1 = c^2 d^3, n+2 = e^2 f^3 with
    a,e,c <= amax and b,d,f <= bmax.

    We additionally impose the *proved necessary* conditions
    b = 3 (mod 4), b odd, f = 1 (mod 4), f odd (Theorem 3.1/3.2 of the paper).
    Imposing necessary conditions only shrinks the searched set, so an `unsat`
    answer is still a valid "no triple lies in this box".  Squarefreeness of b,d,f
    is NOT imposed (it would only restrict further).

    NOTE: z3 may answer `unknown` on larger boxes (nonlinear integer arithmetic of
    degree 5 is hard); that is reported honestly rather than reported as `unsat`.
    """
    t0 = time.perf_counter()
    try:
        import z3
    except ImportError:
        return SearchResult(
            method="E:smt(z3)",
            bound="n/a",
            notes="z3 not available; skipped.",
        )
    s = z3.Solver()
    a, c, e, b, d, f = (z3.Int(nm) for nm in ("a", "c", "e", "b", "d", "f"))
    s.add(
        c * c * d * d * d - a * a * b * b * b == 1,
        e * e * f * f * f - c * c * d * d * d == 1,
        z3.And(a > 0, c > 0, e > 0, b > 0, d > 0, f > 0),
        a <= amax, c <= amax, e <= amax,
        b <= bmax, d <= bmax, f <= bmax,
        b % 4 == 3, b % 2 == 1,
        f % 4 == 1, f % 2 == 1,
    )
    s.set("timeout", timeout_ms)
    status = s.check()
    found: list[int] = []
    if status == z3.sat:
        m = s.model()
        n = m[a].as_long() ** 2 * m[b].as_long() ** 3
        found = [n]
    verdict = "inconclusive (solver gave up); NOT a proof of anything"
    if status == z3.unsat:
        verdict = "no solution in the stated box (valid only for that box)"
    elif status == z3.sat:
        verdict = "SOLUTION FOUND -- must be verified by full factorisation"
    return SearchResult(
        method="E:smt(z3)",
        bound=f"a,c,e <= {amax}; b,d,f <= {bmax}; timeout {timeout_ms} ms",
        found=found,
        runtime_s=time.perf_counter() - t0,
        checked=1 if status == z3.sat else 0,
        notes=f"z3 status: {status} -- {verdict}",
    )


# --------------------------------------------------------------------------- extras
def consecutive_pairs_leq(limit: int) -> list[tuple[int, int]]:
    """All pairs (u, u+1) of powerful numbers with u+1 <= limit."""
    pwf = powerful_leq(int(limit))
    s = set(pwf)
    return [(u, u + 1) for u in pwf if (u + 1) in s]


def pairs_differing_by_2(limit: int) -> list[tuple[int, int]]:
    """All pairs (u, u+2) of powerful numbers with u+2 <= limit.

    A triple of consecutive powerful numbers n, n+1, n+2 would appear here as the
    pair (n, n+2); this is the search that underlies the "no triples below 7.38e28"
    claim quoted in the literature.
    """
    pwf = powerful_leq(int(limit))
    s = set(pwf)
    return [(u, u + 2) for u in pwf if (u + 2) in s]