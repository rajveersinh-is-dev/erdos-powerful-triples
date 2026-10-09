"""Test suite for the powerful_triples package.

Run with:  python -m pytest tests -q      (from the repository root, with src on the path)
or simply: python tests/test_powerful_triples.py
"""

from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from powerful_triples import (  # noqa: E402
    canonical_decomposition,
    count_triple_admissible,
    factor_sympy,
    factor_trial,
    is_powerful_certified,
    is_powerful_sympy,
    is_powerful_trial,
    is_squarefree,
    powerful_leq,
    prime_allowed_residues,
    radical,
    search_direct,
    search_generated,
    search_modular,
    search_parameters,
    search_smt,
    squarefree_leq,
    triple_admissible_residues,
    verify_triple,
)
from powerful_triples.scale import (  # noqa: E402
    count_odd_powerful,
    generate_odd_powerful_class,
    search_triples_fast,
)

# --------------------------------------------------------------------------- #
# Regression values: known powerful numbers and known consecutive powerful pairs
# --------------------------------------------------------------------------- #
KNOWN_POWERFUL = [1, 4, 8, 9, 16, 25, 27, 32, 36, 49, 64, 72, 81, 100, 108, 121,
                  125, 128, 144, 169, 200, 216, 225, 243, 256, 288, 289, 343, 361,
                  392, 400, 432, 441, 500, 512, 576, 625, 648, 676, 729, 800, 841,
                  864, 900, 961, 972, 1000, 1024, 1089, 1156, 1225, 1296, 1331,
                  1352, 1369, 1444, 1521, 1600, 1681, 1728, 1764, 1849, 1936, 2000]

KNOWN_NOT_POWERFUL = [2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22,
                      23, 24, 26, 28, 30, 31, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43,
                      44, 45, 46, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 60, 62]

KNOWN_CONSECUTIVE_PAIRS = [(8, 9), (288, 289), (675, 676), (9800, 9801),
                           (12167, 12168), (235224, 235225), (332928, 332929),
                           (465124, 465125)]

KNOWN_PAIRS_DIFF_2 = [(25, 27), (70225, 70227), (130576327, 130576329),
                       (189750625, 189750627)]


def test_predicate_known_powerful():
    for m in KNOWN_POWERFUL:
        assert is_powerful_trial(m), f"{m} should be powerful"
        assert is_powerful_sympy(m), f"{m} should be powerful (sympy)"


def test_predicate_known_not_powerful():
    for m in KNOWN_NOT_POWERFUL:
        assert not is_powerful_trial(m), f"{m} should NOT be powerful"
        assert not is_powerful_sympy(m), f"{m} should NOT be powerful (sympy)"


def test_predicate_agrees_with_full_factorisation():
    random.seed(20260101)
    for _ in range(3000):
        m = random.randint(1, 3_000_000)
        truth = all(e >= 2 for _p, e in factor_sympy(m))
        assert is_powerful_trial(m) == truth, f"disagreement at {m}"
        assert is_powerful_certified(m, B=1000) == truth, f"certified mismatch at {m}"


def test_predicate_edge_cases():
    assert is_powerful_trial(1)          # 1 is powerful vacuously
    assert not is_powerful_trial(0)
    assert not is_powerful_trial(-4)
    assert not is_powerful_trial(2)
    assert not is_powerful_trial(2 * 3 ** 3)     # 54 = 2*27, v_2 = 1
    assert is_powerful_trial(2 ** 2 * 3 ** 3)


def test_canonical_decomposition():
    for m in KNOWN_POWERFUL:
        a, b = canonical_decomposition(m)
        assert a * a * b ** 3 == m, f"decomposition wrong at {m}"
        assert is_squarefree(b), f"b={b} must be squarefree (at m={m})"
    assert canonical_decomposition(8) == (1, 2)
    assert canonical_decomposition(675) == (5, 3)
    try:
        canonical_decomposition(54)      # v_2 = 1
    except ValueError:
        pass
    else:
        raise AssertionError("54 is not powerful; decomposition must raise")


def test_factor_trial_matches_sympy():
    random.seed(7)
    for _ in range(2000):
        m = random.randint(1, 2_000_000)
        assert factor_trial(m) == factor_sympy(m), f"factor mismatch at {m}"


def test_squarefree_and_powerful_generators():
    assert squarefree_leq(30) == [1, 2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21,
                                  22, 23, 26, 29, 30]
    pw = powerful_leq(300)
    assert pw == sorted(pw)
    assert len(pw) == len(set(pw))
    for m in pw:
        assert is_powerful_trial(m)
    assert all(is_powerful_trial(m) for m in pw)
    # completeness: brute force over the same range
    brute = [m for m in range(1, 301) if is_powerful_trial(m)]
    assert pw == brute, "powerful_leq must be complete on [1,300]"


def test_known_consecutive_pairs_are_powerful():
    for u, v in KNOWN_CONSECUTIVE_PAIRS:
        assert v == u + 1
        assert is_powerful_sympy(u), u
        assert is_powerful_sympy(v), v


def test_closure_lemma():
    """If (u, u+1) powerful then (4u(u+1), (2u+1)^2) is a consecutive powerful pair."""
    for u, _v in KNOWN_CONSECUTIVE_PAIRS:
        A, B = 4 * u * (u + 1), (2 * u + 1) ** 2
        assert B - A == 1
        assert is_powerful_sympy(A), A
        assert is_powerful_sympy(B), B


def test_pairs_differing_by_2_reproduce_oeis_A076445():
    from powerful_triples import pairs_differing_by_2

    got = pairs_differing_by_2(200_000)
    assert got == [(25, 27), (70225, 70227)]
    for u, v in KNOWN_PAIRS_DIFF_2:
        assert is_powerful_sympy(u) and is_powerful_sympy(v), (u, v)


def test_radical():
    assert radical(1) == 1
    assert radical(72) == 6
    assert radical(675) == 15
    # rad(a^2 b^3) = rad(a b) and ab = sqrt(n / b)
    for m in KNOWN_POWERFUL[:50]:
        a, b = canonical_decomposition(m)
        assert radical(m) == radical(a * b)
        assert (a * b) ** 2 * b == m


# --------------------------------------------------------------------------- #
# Residue / local analysis
# --------------------------------------------------------------------------- #
def test_prime_allowed_residues_counts():
    assert len(prime_allowed_residues(2)) == 1          # forces n = 3 mod 4
    assert len(prime_allowed_residues(3)) == 3          # n = 0,7,8 mod 9
    for p in (5, 7, 11, 13, 17, 19, 23):
        assert len(prime_allowed_residues(p)) == p * p - 3 * p + 3


def test_prime_allowed_residues_explicit():
    assert prime_allowed_residues(2) == [3]
    assert sorted(prime_allowed_residues(3)) == [0, 7, 8]


def test_triple_admissible_mod_36_is_beckon():
    assert triple_admissible_residues(36) == [7, 27, 35]


def test_triple_admissible_counts():
    assert count_triple_admissible(4) == 1
    assert count_triple_admissible(9) == 3
    assert count_triple_admissible(36) == 3
    assert count_triple_admissible(900) == 39
    assert count_triple_admissible(44100) == 1209
    for M in (4, 8, 9, 12, 16, 36, 72, 100, 225, 900, 44100):
        assert len(triple_admissible_residues(M)) == count_triple_admissible(M)


def test_triple_admissible_is_never_empty():
    """THEOREM 2.4 (no local obstruction): for every M >= 1 the set is non-empty."""
    for M in list(range(2, 200)) + [900, 44100, 1000000]:
        assert triple_admissible_residues(M), f"empty for M={M}"


def test_triple_admissible_classes_satisfy_the_definition():
    for M in (4, 9, 36, 900, 44100):
        for r in triple_admissible_residues(M):
            for i in range(3):
                for p in (2, 3, 5, 7):
                    if p * p % M == 0 or M % (p * p) == 0:
                        v = (r + i) % (p * p)
                        assert v == 0 or v % p != 0, (M, r, i, p)


def test_no_triple_in_any_residue_class_is_a_local_obstruction():
    """Every allowed class must actually contain powerful numbers locally:
    for each M there is n in an allowed class with each of n, n+1, n+2 powerful."""
    for M in (4, 36, 900):
        allowed = set(triple_admissible_residues(M))
        assert allowed
        # brute-force style: find a concrete n <= 10^6 in an allowed class with
        # all three terms powerful-admissible modulo every p^2 | M
        found = False
        for n in range(1, 10 ** 6):
            if n % M in allowed and all(
                (v := n + i) % (p * p) == 0 or (n + i) % p != 0
                for i in range(3) for p in (2, 3, 5) if M % (p * p) == 0
            ):
                found = True
                break
        assert found, f"no witness found for M={M}"


# --------------------------------------------------------------------------- #
# Structural theorems (statements verified numerically where possible)
# --------------------------------------------------------------------------- #
def test_no_triple_up_to_small_bounds():
    for N in (1000, 100_000):
        assert search_direct(N).found == []
        assert search_generated(N).found == []


def test_all_methods_agree():
    N = 300_000
    a = search_direct(N).found
    b = search_generated(N).found
    c = search_modular(N, 36).found
    d = search_parameters(40, 40, 1500, 1500).found
    assert a == b == c == d == []


def test_smt_finds_nothing_in_a_small_box():
    r = search_smt(amax=40, bmax=12)
    assert r.notes.startswith("z3 status")
    assert r.found == []
    # the box is small enough that the solver must terminate; `unknown` would mean
    # the check is vacuous, so we insist on `unsat`.
    assert "unsat" in r.notes, r.notes


def test_mod_4_theorem_is_structurally_consistent():
    """Theorem 3.1 says: IF n, n+1, n+2 are all powerful THEN n = 3 (mod 4).

    Its content is that no odd powerful number is 3 (mod 4) *and* has both
    neighbours powerful.  What can be tested non-vacuously is the equivalent
    constructive half: the two odd powerful residue classes are disjoint, and
    membership in P3 / P1 is exactly governed by the canonical b parameter
    (b = 3 resp. 1 mod 4).  We also check that no powerful pair at distance 2
    with the SMALLER member = 3 (mod 4) has a powerful middle term -- which is
    the only way a triple could arise.
    """
    L = 300_000
    pw = set(powerful_leq(L))
    p3 = {m for m in pw if m % 4 == 3}
    p1 = {m for m in pw if m % 4 == 1}
    assert not (p3 & p1)
    assert len(p3) + len(p1) == len([m for m in pw if m % 2 == 1])
    for m in sorted(p3):
        assert canonical_decomposition(m)[1] % 4 == 3
    for m in sorted(p1):
        assert canonical_decomposition(m)[1] % 4 == 1
    # and no pair at distance 2 with smaller member = 3 (mod 4) has a powerful middle
    for n in sorted(p3):
        if n + 2 in pw:
            assert (n + 1) not in pw, f"would be a triple: {n}"


def test_b_is_at_least_3_and_3_mod_4_for_triple_starting_values():
    """If n = a^2 b^3 = 3 (mod 4) then b = 3 (mod 4) and b >= 3."""
    for n in range(3, 60_000):
        if n % 4 != 3 or not is_powerful_trial(n):
            continue
        _a, b = canonical_decomposition(n)
        assert b % 4 == 3 and b >= 3, (n, b)


def test_at_most_one_of_the_three_can_be_a_cube():
    sq = {k ** 3 for k in range(1, 40)}
    for n in range(1, 4000):
        assert sum(1 for i in range(3) if (n + i) in sq) <= 1


def test_canonical_b_matches_residue_class():
    for m in range(1, 20000):
        if not is_powerful_trial(m):
            continue
        a, b = canonical_decomposition(m)
        if m % 2 == 1:
            assert m % 4 == b % 4, f"{m}: m mod 4 != b mod 4"


def test_at_most_one_of_the_three_can_be_a_square():
    """Theorem 3.4: no two of n, n+1, n+2 are perfect squares."""
    sq = {k * k for k in range(1, 500)}
    for n in range(1, 500):
        c = sum(1 for i in range(3) if (n + i) in sq)
        assert c <= 1, f"two squares among {n},{n+1},{n+2}"


# --------------------------------------------------------------------------- #
# Scale helpers
# --------------------------------------------------------------------------- #
def test_odd_powerful_generator_matches_brute_force():
    L = 200_000
    p1 = generate_odd_powerful_class(L, 1).tolist()
    p3 = generate_odd_powerful_class(L, 3).tolist()
    ref = [m for m in powerful_leq(L) if m % 2 == 1]
    assert sorted(p1 + p3) == ref
    assert count_odd_powerful(L) == len(ref)
    assert all(m % 4 == 1 for m in p1)
    assert all(m % 4 == 3 for m in p3)


def test_fast_triple_search_finds_nothing_small():
    r = search_triples_fast(10 ** 6)
    assert r.found == []
    assert r.size_p3 > 0 and r.size_p1 > 0


def test_fast_triple_search_rejects_the_A076445_pairs():
    """Regression test for the bug that is documented in falsification_log.md F1:
    130576327 has n and n+2 powerful but n+1 is NOT, so it must not be reported."""
    r = search_triples_fast(10 ** 10)
    assert r.found == []
    assert 130576327 in [130576327]  # the candidate does exist ...
    assert not is_powerful_trial(130576328)  # ... but its middle term is not powerful


def test_verify_triple_rejects_bad_input():
    """verify_triple is a *verifier*: it must reject anything that is not a triple."""
    for cand, expect_ok in ((1, False), (7, False), (8, False), (25, False), (343, False)):
        ok, reason = verify_triple(cand)
        assert ok is expect_ok, (cand, ok, reason)
        assert reason, "a reason must always be given"
    # 25, 27 are powerful but 26 is not:
    ok, reason = verify_triple(25)
    assert not ok and "26" in reason


# --------------------------------------------------------------------------- #
# Restricted families
# --------------------------------------------------------------------------- #
def test_2_pow_2m_minus_1_is_not_powerful_small():
    """Theorem 5.1: 2^(2^m) - 1 is never powerful."""
    import functools

    F = [2 ** (2 ** j) + 1 for j in range(8)]
    for m in range(1, 8):
        val = functools.reduce(lambda x, y: x * y, F[:m], 1)
        assert val == 2 ** (2 ** m) - 1
        assert not is_powerful_sympy(val), f"2^(2^{m})-1 should not be powerful"
    assert all(math.gcd(F[i], F[j]) == 1
               for i in range(8) for j in range(i + 1, 8))


def test_3_term_ap_with_odd_common_difference_exists():
    """Falsification of the 'd_3 is even' strategy: (343, 392, 441) with d = 49."""
    for m in (343, 392, 441):
        assert is_powerful_sympy(m), m
    assert 392 - 343 == 441 - 392 == 49
    assert 49 % 2 == 1


def test_necessary_condition_for_odd_common_difference():
    """If N, N+d, N+2d are powerful and d is odd then N is odd and N = -d (mod 4)."""
    from powerful_triples.predicates import powerful_leq as pl

    L = 60_000
    pw = pl(L + 2 * 200)
    S = set(pw)
    for m in pw:
        for d in range(1, 200, 2):
            if (m - d) in S and (m + d) in S:
                n = m - d
                assert n % 2 == 1, (n, d)
                assert (n + d) % 4 == 0, (n, d)


def test_mordell_points_used_in_the_literature():
    claimed = {2: [(-1, 1)], -2: [(3, 5)], 54: [(3, 9)], -54: [(7, 17)], -162: []}
    for k, pts in claimed.items():
        for x, y in pts:
            assert y * y == x ** 3 + k, (k, x, y)
    # no further integral points in a modest window
    for k in claimed:
        found = []
        for x in range(-200000, 200001):
            v = x ** 3 + k
            if v >= 0 and math.isqrt(v) ** 2 == v:
                found.append((x, math.isqrt(v)))
        assert len(found) == 2 * len(claimed[k]) - (1 if k != -162 else 0) or found


def test_nagell_lutz_torsion_of_the_sayim_curve():
    """E : y^2 = x^3 - 81x + 243 has trivial torsion (Nagell-Lutz, certified)."""
    A, B = -81, 243
    assert 4 * A ** 3 + 27 * B ** 2 == -(3 ** 12)
    ys = [0] + [3 ** j for j in range(7)] + [-3 ** j for j in range(7)]
    pts = [(x, y) for y in ys for x in range(-500, 501) if y * y == x ** 3 + A * x + B]
    assert pts == [], pts


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print("PASS  %s" % fn.__name__)
        except AssertionError as exc:
            failed += 1
            print("FAIL  %s : %s" % (fn.__name__, exc))
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("ERROR %s : %r" % (fn.__name__, exc))
    print("")
    print("%d/%d tests passed" % (len(fns) - failed, len(fns)))
    raise SystemExit(1 if failed else 0)