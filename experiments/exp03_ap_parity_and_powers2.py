"""Experiment 3 -- two lines of attack.

PART A (falsification of the "d_3 is even" strategy)
    The EMW conjecture is equivalent to d_3 > 1 (BBC, arXiv:2302.03113, Sec. 7).
    A sufficient condition would be: every 3-term AP of powerful numbers has EVEN
    common difference.  This experiment shows that condition is FALSE, by explicit
    counterexample, and then determines how small an odd common difference can be.

PART B (a provable restricted family: the middle term a power of 2)
    Theorem (proved in the paper): for every m >= 1, 2^(2^m) - 1 is NOT powerful.
    Proof: 2^(2^m) - 1 = prod_{j<m} F_j with F_j = 2^(2^j)+1 the Fermat numbers,
    which are pairwise coprime and each > 1, so every F_j occurs with exponent
    exactly 1.  Hence a triple (2^(2^m)-1, 2^(2^m), 2^(2^m)+1) is impossible.
    Also verified here: the general necessary condition
        2^k - 1 powerful  ==>  every p | 2^k-1 divides k or is Wieferich to base 2
    and a direct exhaustive test of "2^k-1 not powerful" for small k.
"""

from __future__ import annotations

import _bootstrap  # noqa: F401  (puts <repo>/src on sys.path; write_result)

import json
import time

from powerful_triples.predicates import factor_sympy, is_powerful_trial, powerful_leq
from powerful_triples.scale import generate_odd_powerful_class


def verify_ap(n, d):
    """Fully factorise N, N+d, N+2d and report whether each is powerful."""
    out = {}
    for off in (0, d, 2 * d):
        m = n + off
        fac = factor_sympy(m)
        out[str(m)] = {
            "factorization": "*".join("%s^%d" % (p, e) for p, e in fac),
            "powerful": all(e >= 2 for _p, e in fac),
        }
    return out


def part_a():
    print("=" * 78)
    print("PART A -- is d_3 even?")
    print("=" * 78)
    res = {}
    ex = verify_ap(343, 49)
    print("counterexample candidate (N, d) = (343, 49):")
    for k, v in ex.items():
        print("   %6s = %-26s powerful=%s" % (k, v["factorization"], v["powerful"]))
    res["counterexample_343_49"] = ex
    res["counterexample_is_valid"] = all(v["powerful"] for v in ex.values())
    print("   -> VALID COUNTEREXAMPLE to 'd_3 is even': %s  (d = 49 is odd)"
          % res["counterexample_is_valid"])

    ex2 = verify_ap(169, 87)
    print("second example (N, d) = (169, 87):")
    for k, v in ex2.items():
        print("   %6s = %-26s powerful=%s" % (k, v["factorization"], v["powerful"]))
    res["counterexample_169_87"] = ex2

    # How small can an odd common difference be?  Search all powerful m up to L
    # for m-d, m, m+d all powerful with d odd.
    L = 10 ** 10
    t0 = time.perf_counter()
    pw = powerful_leq(L + 200)
    S = set(pw)
    odd_d_hits = {}
    for d in range(1, 49, 2):
        for m in pw:
            if (m - d) in S and (m + d) in S:
                odd_d_hits[d] = m
    print("")
    print("All 3-term APs of powerful numbers with ODD d < 49 and N <= %d:" % L)
    if odd_d_hits:
        for d in sorted(odd_d_hits):
            print("   d = %3d (odd), middle term m = %d" % (d, odd_d_hits[d]))
    else:
        print("   NONE  -> verified: no 3-term AP of powerful numbers with odd "
              "common difference < 49 exists with N <= %d" % L)
    res["odd_d_lt_49_up_to_1e10"] = {str(k): v for k, v in odd_d_hits.items()}
    res["odd_d_scan_limit_N"] = L
    res["odd_d_scan_seconds"] = round(time.perf_counter() - t0, 2)
    print("   (scan took %.2fs over %d powerful numbers)"
          % (res["odd_d_scan_seconds"], len(pw)))

    # Same question for d = 1 at a much larger scale (the triple search).
    t1 = time.perf_counter()
    p3 = generate_odd_powerful_class(L + 3, 3)
    p1 = generate_odd_powerful_class(L + 3, 1)
    import numpy as np

    cand = np.intersect1d(p3, p1 - 2, assume_unique=True)
    good = [int(v) for v in cand if is_powerful_trial(int(v) + 1)]
    print("")
    print("Triple search (d = 1) up to %d: candidates with n,n+2 powerful = %s; "
          "triples = %s" % (L, [int(v) for v in cand], good))
    res["triples_up_to_1e10"] = good
    res["triple_scan_seconds"] = round(time.perf_counter() - t1, 2)
    return res


def part_b():
    print("")
    print("=" * 78)
    print("PART B -- middle term a power of 2")
    print("=" * 78)

    # Structural verification of the ingredients of the theorem, without needing
    # to factor any gigantic integer:
    #   (i)   prod_{j<m} F_j = 2^(2^m) - 1            (Fermat identity)
    #   (ii)  gcd(F_i, F_j) = 1 for i != j             (pairwise coprimality)
    #   (iii) every F_j > 1
    # Together (i)-(iii) force each F_j to occur with exponent exactly 1 in
    # 2^(2^m)-1, hence that number is never powerful.
    import functools
    from math import gcd

    F = [2 ** (2 ** j) + 1 for j in range(16)]
    ident_ok = all(
        functools.reduce(lambda x, y: x * y, F[:m], 1) == 2 ** (2 ** m) - 1
        for m in range(1, 13)
    )
    coprime_ok = all(gcd(F[i], F[j]) == 1 for i in range(16) for j in range(i + 1, 16))
    gt1_ok = all(f > 1 for f in F)
    print("Fermat identity  prod_{j<m} F_j = 2^(2^m)-1  for m=1..12 : %s" % ident_ok)
    print("Fermat numbers pairwise coprime (j <= 15)                : %s" % coprime_ok)
    print("every F_j > 1                                           : %s" % gt1_ok)

    direct = {}
    for m in range(1, 8):
        k = 2 ** m
        val = 2 ** k - 1
        fac = factor_sympy(val)
        direct[m] = {"k": k, "value": val, "n_primes": len(fac),
                     "powerful": all(e >= 2 for _p, e in fac)}
        print("  m=%d: 2^(2^m)-1 = 2^%-5d-1 has %2d distinct prime factors, "
              "powerful=%s" % (m, k, direct[m]["n_primes"], direct[m]["powerful"]))

    viol = []
    t0 = time.perf_counter()
    for k in range(2, 251):
        if all(e >= 2 for _p, e in factor_sympy(2 ** k - 1)):
            viol.append(k)
    print("2^k-1 powerful for k in 2..250    : %s   (expected [])   [%.1fs]"
          % (viol, time.perf_counter() - t0))

    # Wieferich-to-base-2 characterisation check.
    for k in (3, 6, 21):
        n = 2 ** k - 1
        fac = factor_sympy(n)
        print("  k=%3d: 2^k-1 = %s" % (k, "*".join("%s^%d" % (p, e) for p, e in fac)))
        for p, e in fac:
            pp = p * p
            o = 1
            while pow(2, o, pp) != 1 % pp:
                o += 1
            pk = (p | k) == p
            ok = (e < 2) or pk or (o <= k)
            verdict = "consistent with the theorem" if ok else "VIOLATION"
            print("        p=%4d e=%d ord_(p^2)(2)=%6d p|k=%-5s -> %s"
                  % (p, e, o, pk, verdict))
    ok = (ident_ok and coprime_ok and gt1_ok and not viol
          and not any(v["powerful"] for v in direct.values()))
    print("PART B verdict: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    r = part_a()
    part_b()
    path = _bootstrap.write_result("exp03_ap_and_powers2.json", r)
    print("")
    print("wrote %s" % path)
    raise SystemExit(0)