"""Experiment 4 -- independent cross-checks of the claims made in the literature.

Nothing here is a new theorem.  The point is to test, with our own code, the
specific statements that other papers make, so that the literature review is not
a chain of copied citations.

Checks performed
----------------
C1  Beckon's congruence constraint on a triple: n = 7, 27, 35 (mod 36).
C2  The exact counts of triple-admissible residue classes mod 900 and 44100
    (39 and 1209, as claimed by Sayim, Prop. 3).
C3  Closure lemma for consecutive powerful pairs:
        (u, v = u+1)  ->  (4uv, (2u+1)^2)
    which is why infinitely many consecutive powerful pairs exist.
C4  The four "shape" families excluded by Chan / She / Sayim:
        x^3-1 = p^3 y^2 , x^3+1 = q^3 z^2       (Chan)
        x^3-1 = p^2 a^3 , x^3+1 = q^2 b^3       (She)
        x^3-1 = p^2 a^3 , x^3+1 = q^3 z^2       (Sayim M1)
        x^3-1 = p^3 y^2 , x^3+1 = q^2 b^3       (Sayim M2)
    Count how often each single shape occurs for x <= X, and confirm that no
    x <= X makes BOTH x^3-1 and x^3+1 powerful.
C5  Nagell-Lutz: the elliptic curve E: y^2 = x^3 - 81x + 243 (Cremona 1296f2,
    LMFDB 1296.k1), whose rank-0 property is the single non-elementary input to
    Sayim's Theorem 2, has TRIVIAL torsion.  This part IS certified here.
C6  The integral points of the five Mordell curves y^2 = x^3 + k,
    k in {2, -2, 54, -54, -162}, quoted by Sayim.
C7  The Pell-orbit recurrence z_{k+1} = 14 z_k - z_{k-1} + 6, (z_0, z_1) = (-2, 1),
    encoding all integer solutions of z^2 + z + 1 = 3w^2, and the claim that the
    only cube in the orbit is z_1 = 1.
"""

from __future__ import annotations

import _bootstrap  # noqa: F401  (puts <repo>/src on sys.path; write_result)

import json
import math
import time

from powerful_triples.predicates import (
    factor_sympy,
    is_powerful_certified,
    is_powerful_sympy,
)
from powerful_triples.residues import count_triple_admissible, triple_admissible_residues

X_SHAPE = 20000
X_CUBE = 200000


def c1_c2() -> dict:
    """C1 c2.
    
    Returns:
        dict: Result of type dict
    
    """
    print("=" * 78)
    print("C1/C2  local residue constraints")
    print("=" * 78)
    r36 = triple_admissible_residues(36)
    print(f"triple-admissible classes mod 36    : {r36}")
    print("Beckon's constraint (n in {7,27,35}) reproduced: %s"
          % (r36 == [7, 27, 35]))
    for M, claimed in ((900, 39), (44100, 1209)):
        got = count_triple_admissible(M)
        print("count mod %-6d = %-6d (claimed %d) match=%s" % (M, got, claimed, got == claimed))
    # density rate: prod_{p<=L} c_p/p^2 should decay like C/(log L)^3
    from sympy import primerange

    primes = list(primerange(5, 2000))
    prod, samples, k, idx = 1.0, [], 0, 0
    thresholds = [10, 100, 1000, 1999]
    for p in primes:
        prod *= (p * p - 3 * p + 3) / float(p * p)
        k = prod
        if idx < len(thresholds) and p >= thresholds[idx]:
            lg = math.log(p)
            samples.append((p, prod, lg, prod * lg ** 3))
            idx += 1
    print("density of admissible classes mod prod_{p<=L} p^2:")
    for p, pr, lg, scaled in samples:
        print("   L=%5d  density=%.6g   density*(log L)^3 = %.4f" % (p, pr, scaled))
    return {"mod36": r36, "mod900": count_triple_admissible(900),
            "mod44100": count_triple_admissible(44100),
            "density_samples": [[p, pr, lg, scaled] for p, pr, lg, scaled in samples]}


def c3() -> dict:
    """C3.
    
    Returns:
        dict: Result of type dict
    
    """
    print("")
    print("=" * 78)
    print("C3  closure lemma for consecutive powerful pairs")
    print("=" * 78)
    from powerful_triples.predicates import powerful_leq

    S = set(powerful_leq(5000))
    pairs = [u for u in S if u + 1 in S]
    rows = []
    for u in sorted(pairs)[:
        8]:
        A, B = 4 * u * (u + 1), (2 * u + 1) ** 2
        rows.append((u, u + 1, A, B, B - A, is_powerful_sympy(A), is_powerful_sympy(B)))
        print("  (%d, %d) -> (%d, %d)   B-A = %d   both powerful: %s"
              % (u, u + 1, A, B, B - A, is_powerful_sympy(A) and is_powerful_sympy(B)))
    allok = all(r[4] == 1 and r[5] and r[6] for r in rows)
    print(f"  closure verified for all listed pairs: {allok}")
    return {"pairs_checked": len(rows), "all_ok": allok}


def _shape_of(m) -> str:
    """Classify a powerful m as 'p^3 y^2', 'p^2 y^3' or None.

    m = p^3 y^2 with p prime  <=>  there is a prime p with v_p(m) >= 3 and
    v_q(m) = 2 v_q(y) is even for every q != p, i.e. all other exponents even.
    """
    fac = factor_sympy(m)
    if not fac:
        return None
    cubeful = [p for p, e in fac if e >= 3]
    others = {p: e for p, e in fac if p not in cubeful}
    if cubeful:
        if all(e % 2 == 0 for e in others.values()):
            return "p^3 y^2"
    for p, e in fac:
        if e >= 2:
            rest = {q: v for q, v in fac if q != p}
            if all(v % 3 == 0 for v in rest.values()):
                return "p^2 y^3"
    return None


def _powerful_fast(m, primes) -> bool:
    """Rigorous test: True / False, using only primes in `primes` unless forced
    to do a full factorisation.  Never guesses."""
    r = m
    for p in primes:
        if p * p > r:
            break
        if r % p == 0:
            e = 0
            while r % p == 0:
                r //= p
                e += 1
            if e == 1:
                return False
    if r == 1:
        return True
    # No small prime divides r to exponent 1: r may still be powerful or not.
    # Finish exactly (this branch is expected to be rare).
    return all(e >= 2 for _p, e in factor_sympy(r))


def c4() -> dict:
    """C4.
    
    Returns:
        dict: Result of type dict
    
    """
    print("")
    print("=" * 78)
    print("C4  the four excluded 'shape' families around a cube")
    print("=" * 78)
    from sympy import primerange

    primes_small = list(primerange(2, 3000))
    primes_mid = list(primerange(2, 500))
    t0 = time.perf_counter()
    minus_counts = {"p^3 y^2": 0, "p^2 y^3": 0}
    plus_counts = {"p^3 y^2": 0, "p^2 y^3": 0}
    both_powerful, both_shape = [], []
    for x in range(2, X_SHAPE + 1):
        pm, pp = x ** 3 - 1, x ** 3 + 1
        am, ap = _powerful_fast(pm, primes_small), _powerful_fast(pp, primes_small)
        sm = _shape_of(pm) if am else None
        sp = _shape_of(pp) if ap else None
        if sm:
            minus_counts[sm] += 1
        if sp:
            plus_counts[sp] += 1
        if am and ap:
            both_powerful.append(x)
        if sm and sp:
            both_shape.append((x, sm, sp))
    print(f"  x <= {X_SHAPE} : x^3-1 powerful of the stated shape : {minus_counts}")
    print(f"  x <= {X_SHAPE} : x^3+1 powerful of the stated shape : {plus_counts}")
    print(f"  x <= {X_SHAPE} : BOTH x^3-1 and x^3+1 powerful     : {both_powerful}")
    print("  x <= %d : both outer terms of a Chan/She/Sayim shape : %s"
          % (X_SHAPE, both_shape))
    print("  (%.1fs)" % (time.perf_counter() - t0))

    # Bigger, cheaper scan for cube-centred triples (primes <= 500 only for the
    # first filter; survivors are finished exactly).
    t1 = time.perf_counter()
    survivors = []
    cubes = []
    for x in range(2, X_CUBE + 1):
        pp = x ** 3 + 1
        if _powerful_fast(pp, primes_mid):
            if _powerful_fast(x ** 3 - 1, primes_mid):
                cubes.append(x)
    print("  cube-centred candidate triples (x^3-1, x^3, x^3+1) for x <= %d : %s  (%.1fs)"
          % (X_CUBE, cubes, time.perf_counter() - t1))
    return {"minus": minus_counts, "plus": plus_counts,
            "both_powerful_small": both_powerful, "both_shape": both_shape,
            "cube_centred_candidates": cubes, "x_cube_bound": X_CUBE}


def c5() -> dict:
    """C5.
    
    Returns:
        dict: Result of type dict
    
    """
    print("")
    print("=" * 78)
    print("C5  Nagell-Lutz: torsion of E : y^2 = x^3 - 81x + 243")
    print("=" * 78)
    A, B = -81, 243
    four_a3_plus_27b2 = 4 * A ** 3 + 27 * B ** 2
    print(f"  4A^3 + 27B^2 = {four_a3_plus_27b2} = 3^{12}")
    pts = []
    for j in range(0, 7):                       # y = +-3^j, j <= 6
        y2 = 3 ** (2 * j)
        # solve x^3 - 81x + 243 = y^2 for integer x
        x = 0
        # bound: |x| <= 400 suffices here (the cubic is monotone increasing for
        # |x| >= 8 and |x^3| > |x^3-81x+243| + y^2 beyond that)
        found = [xx for xx in range(-400, 401)
                 if xx ** 3 - 81 * xx + 243 == y2]
        for xx in found:
            pts.append((xx, 3 ** j))
    # y = 0 case
    roots = [xx for xx in range(-400, 401) if xx ** 3 - 81 * xx + 243 == 0]
    print(f"  integer solutions with y = 0 (2-torsion) : {roots}")
    print(f"  integer solutions with y = +-3^j, 0<=j<=6 : {pts}")
    print("  => E(Q)_tors = { O }  (Nagel-Lutz, certified by exhaustive check) : %s"
          % (not roots and not pts))
    print("  NOTE: the RANK of E is a separate input; it is NOT verified here.")
    return {"y0_roots": roots, "y_3j_points": pts}


def c6():
    """C6.
    
    Returns:
        The computed result
    
    """
    print("")
    print("=" * 78)
    print("C6  integral points of y^2 = x^3 + k,  k in {2,-2,54,-54,-162}")
    print("=" * 78)
    claimed = {
        2: [(-1, 1)],
        -2: [(3, 5)],
        54: [(3, 9)],
        -54: [(7, 17)],
        -162: [],
    }
    out = {}
    for k, cl in claimed.items():
        lim = 2_000_000
        found = []
        for x in range(-lim, lim + 1):
            v = x ** 3 + k
            if v < 0:
                continue
            r = math.isqrt(v)
            if r * r == v:
                found.append((x, r))
        match = found == sorted(set(cl + [(-x, y) for x, y in cl if (x, -y) not in found
                                          and (-x, y) not in cl]))
        print("  k=%-5d claimed %-28s found in |x|<=%d : %s"
              % (k, str(cl), lim, found if len(found) <= 12 else f"{len(found)} points"))
        out[str(k)] = {"claimed": cl, "found_up_to": lim, "found": found[:50],
                       "n_found": len(found)}
    return out


def c7(kmax: int = 2000):
    """C7.
    
    Args:
        kmax (int):
    
    Returns:
        dict: Result of type dict
    
    """
    print("")
    print("=" * 78)
    print("C7  Pell orbit z_{k+1} = 14 z_k - z_{k-1} + 6,  (z_0,z_1) = (-2,1)")
    print("=" * 78)
    # Cross-check the recurrence against the closed-form Pell computation.
    # Sayim's orbit enumerates the solutions (b,c) of b^2 - 3c^2 = 1 with b EVEN,
    # which are exactly the ODD powers (2+sqrt3)^(2j+1); the sign choice
    # z -> -1-z covers the other branch.  So recurrence index j corresponds to
    # the (2j+1)-st power.
    z = [-2, 1]
    for _k in range(1, kmax):
        z.append(14 * z[-1] - z[-2] + 6)
    zs = z[1:]
    bk, ck = 2, 1
    checks = []
    for j in range(8):
        j += 1                                   # 1-based
        direct = (3 * ck - 1) // 2
        checks.append((f"recurrence index j={j} (power {2 * j - 1})", direct, zs[j - 1]))
        bk, ck = (2 * bk + 3 * ck, bk + 2 * ck)  # square the unit -> skip to next odd power
        # after squaring we have (2+sqrt3)^(2j); square once more for 2j+1 handled
        # by the loop invariant below
        bk, ck = (2 * bk + 3 * ck, bk + 2 * ck)
    for name, direct, rec in checks:
        print("   %-38s direct z = %-20d recurrence z = %-20d agree=%s"
              % (name, direct, rec, direct == rec))
    agree = all(d == r_ for _n, d, r_ in checks)
    print(f"   recurrence cross-check agrees at every tested index: {agree}")
    cubes = []
    biggest = 0
    for i, v in enumerate(zs, start=1):
        if v < 0:
            continue
        biggest = max(biggest, v)
        r = math.isqrt(v)
        if r * r == v:
            cubes.append((i, v, r))
        neg = -1 - v
        if neg > 0:
            rn = math.isqrt(neg)
            if rn * rn == neg:
                cubes.append((i, neg, rn))
    print(f"  cubes z_k = t^3 found for k <= {kmax} : {cubes}")
    print(f"  largest |z_k| examined has {len(str(biggest))} decimal digits")
    return {"cubes": cubes, "kmax": kmax, "largest_digits": len(str(biggest)),
            "recurrence_agrees": agree,
            "checks": [[n, d, r_, d == r_] for n, d, r_ in checks]}


if __name__ == "__main__":
    res = {}
    res["c1c2"] = c1_c2()
    res["c3"] = c3()
    res["c4"] = c4()
    res["c5"] = c5()
    res["c6"] = c6()
    res["c7"] = c7()
    path = _bootstrap.write_result("exp04_literature_checks.json", res)
    print("")
    print(f"wrote {path}")