"""Local (congruence) analysis of triples of powerful numbers.

Core notion
-----------
Fix M >= 1 with M = prod_p p^{k_p}.  Call a residue r (mod M) *triple-admissible*
if every n with n = r (mod M) satisfies, for each i in {0,1,2} and each prime p
with p^2 | M:

        p | (n + i)   ==>   p^2 | (n + i).

Equivalently: the three residues r, r+1, r+2 (mod p^2) are each congruent to 0 or
to a unit modulo p^2, for every p with p^2 | M.

Why this is the right local notion
----------------------------------
Powerfulness of m implies: for every prime p,  p | m  ==>  p^2 | m.  A congruence
argument in n alone can only ever use the residue of n modulo M; it must rule out
every triple-admissible residue class to have any force.  The functions here
compute those classes exactly (Theorem 2 of the accompanying paper), which lets
us certify, positively, that

  * the class is never empty (so no pure congruence argument in n can work), and
  * how sparse it is (density product).

Exact counts, per prime (proved in the paper):

    c_2 = 1                      if k_2 >= 2   (forces n = 3 mod 4)
    c_3 = 3                      if k_3 >= 2   (n = 0, 7, 8 mod 9)
    c_p = p^2 - 3p + 3 = (p-1)(p-2)+1   if k_p >= 2 and p >= 5

and there is no constraint from primes with k_p = 1.  The classes combine freely by
CRT, so

    #triple-admissible residues mod M = prod_{p : k_p >= 2} c_p.
"""

from __future__ import annotations



__all__ = [
    "factor_modulus",
    "prime_allowed_residues",
    "triple_admissible_residues",
    "count_triple_admissible",
    "powerful_residues_mod",
    "is_triple_admissible",
    "admissible_density_product",
]


def factor_modulus(m: int) -> list[tuple[int, int]]:
    """Return [(p, k_p), ...] for m = prod p^{k_p}, sorted by p."""
    m = int(m)
    if m < 1:
        raise ValueError("factor_modulus requires m >= 1")
    out: list[tuple[int, int]] = []
    p = 2
    while p * p <= m:
        if m % p == 0:
            k = 0
            while m % p == 0:
                m //= p
                k += 1
            out.append((p, k))
        p += 1 if p == 2 else 2
    if m > 1:
        out.append((m, 1))
    return out


def _crt(r1: int, m1: int, r2: int, m2: int) -> tuple[int, int]:
    """Combine r1 (mod m1) and r2 (mod m2) for coprime m1, m2; return (r, lcm)."""
    g, x, _ = _egcd(m1, m2)
    if g != 1:
        raise ValueError("CRT requires coprime moduli")
    t = ((r2 - r1) * x) % m2
    lcm = m1 * m2
    return (r1 + m1 * t) % lcm, lcm


def _egcd(a: int, b: int) -> tuple[int, int, int]:
    """Egcd.
    
    Args:
        a:
        b:
    
    Returns:
        tuple: Result of type tuple
    
    """
    old_r, r = a, b
    old_s, s = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_r, old_s, 0


def prime_allowed_residues(p: int) -> list[int]:
    """Residues r (mod p^2) with r, r+1, r+2 each equal to 0 or a unit mod p^2.

    This is the p-primary condition for the triple n, n+1, n+2.
    """
    p = int(p)
    pp = p * p
    # Forbidden: r = p*t - i  for i in {0,1,2} and t in 1..p-1.
    forbidden = set()
    for i in (0, 1, 2):
        for t in range(1, p):
            forbidden.add((p * t - i) % pp)
    return [r for r in range(pp) if r not in forbidden]


def triple_admissible_residues(m: int) -> list[int]:
    """All triple-admissible residues modulo ``m``, in increasing order."""
    m = int(m)
    if m < 1:
        raise ValueError("triple_admissible_residues requires m >= 1")
    if m == 1:
        return [0]
    facs = factor_modulus(m)
    # Only primes with exponent >= 2 contribute a constraint.
    facs = [(p, k) for p, k in facs if k >= 2]
    if not facs:
        return list(range(m))
    # Sort so that the accumulated modulus grows; handle p = 2 first so the
    # intermediate lists stay small (c_2 = 1).
    facs.sort(key=lambda pk: (pk[0] != 2, pk[0]))
    acc = [(0, 1)]
    for p, _k in facs:
        allowed = prime_allowed_residues(p)
        new: list[tuple[int, int]] = []
        for r1, m1 in acc:
            for r2 in allowed:
                new.append(_crt(r1, m1, r2, p * p))
        acc = new
    # The accumulated modulus (prod of the p^2 involved) divides m, so lifting is
    # well defined: each accumulated class is enumerated inside [0, m).
    seen: set[int] = set()
    for r, mod in acc:
        for t in range(m // mod):
            seen.add(r + t * mod)
    return sorted(seen)


def count_triple_admissible(m: int) -> int:
    """Number of triple-admissible residues mod ``m`` (computed combinatorially).

    Let S = prod_{p : k_p >= 2} p^2 (the "squarefull part" of the modulus).  The
    constraints depend only on residues mod S, and S | m, so each admissible class
    mod S lifts to exactly m / S classes mod m.  Hence

        #classes = (m / S) * prod_{p : k_p >= 2} c_p.
    """
    m = int(m)
    if m < 1:
        raise ValueError("count_triple_admissible requires m >= 1")
    total = 1
    squarefull_part = 1
    for p, k in factor_modulus(m):
        if k >= 2:
            total *= len(prime_allowed_residues(p))
            squarefull_part *= p * p
    return total * (m // squarefull_part)


def powerful_residues_mod(m: int) -> set[int]:
    """Residues mod ``m`` actually attained by a powerful number.

    PROVED characterization (see the paper, Proposition 1):  r mod M is attained
    by some powerful number iff for every prime p with p^2 | M, the residue
    r (mod p^2) is either 0 or a unit.  ("unit" = coprime to p.)

    Sufficiency construction: if the condition holds, put
        s = prod_{p : p^2 | M, p | r} p^{v_p(r)}        (squarefull by the condition)
        m0 = s * (1 + M)^2
    Then m0 is powerful (product of two powerful numbers), and m0 = s (mod M)
    because (1+M)^2 = 1 (mod M) and s = r (mod M) by definition of s.
    """
    m = int(m)
    facs = [(p, k) for p, k in factor_modulus(m) if k >= 2]
    ok = list(range(m))
    for p, _k in facs:
        pp = p * p
        ok = [r for r in ok if r % pp == 0 or r % p != 0]
    return set(ok)


def is_triple_admissible(n: int, m: int) -> bool:
    """True iff n's residue class mod m is triple-admissible."""
    return (int(n) % int(m)) in set(triple_admissible_residues(m))


def admissible_density_product(primes: list[int]) -> float:
    """Product of c_p/p^2 over the given primes (the local sieve density)."""
    prod = 1.0
    for p in primes:
        prod *= len(prime_allowed_residues(p)) / float(p * p)
    return prod