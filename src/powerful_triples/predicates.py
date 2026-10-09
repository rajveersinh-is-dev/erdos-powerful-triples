"""Exact predicates and canonical decompositions for powerful (squarefull) numbers.

A positive integer m is *powerful* iff every prime p dividing m satisfies p^2 | m.
Equivalently m has a UNIQUE representation m = a^2 * b^3 with b squarefree
(Golomb, Amer. Math. Monthly 77 (1970), 848-852).

Two independent implementations of `is_powerful` are provided so that they can be
cross-checked against each other on overlapping ranges:

  * `is_powerful_trial`   -- pure-Python trial division (no third-party deps).
  * `is_powerful_sympy`   -- delegates to sympy's factorint (Pollard-rho/ECM).

All arithmetic is exact Python integer arithmetic.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Iterator

__all__ = [
    "PrimeFactorization",
    "factor_trial",
    "factor_sympy",
    "is_powerful_trial",
    "is_powerful_sympy",
    "is_powerful_certified",
    "is_powerful",
    "canonical_decomposition",
    "radical",
    "is_squarefree",
    "squarefree_leq",
    "powerful_leq",
    "iter_powerful",
    "next_powerful",
]

# A factorization, stored as a tuple of (prime, exponent) pairs sorted by prime.
PrimeFactorization = tuple[tuple[int, int], ...]


def factor_trial(n: int) -> PrimeFactorization:
    """Factor ``n >= 1`` by trial division.  Exact, but O(n^{1/2}) worst case."""
    if n < 1:
        raise ValueError(f"factor_trial requires n >= 1, got {n}")
    n = int(n)
    factors: list[tuple[int, int]] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            factors.append((d, e))
        d = 3 if d == 2 else d + 2
    if n > 1:
        factors.append((n, 1))
    return tuple(factors)


def factor_sympy(n: int) -> PrimeFactorization:
    """Factor ``n >= 1`` using sympy (fast for large inputs)."""
    if n < 1:
        raise ValueError(f"factor_sympy requires n >= 1, got {n}")
    from sympy import factorint  # local import: keeps the pure-Python path standalone

    return tuple(sorted((int(p), int(e)) for p, e in factorint(int(n)).items()))


def is_powerful_trial(n: int) -> bool:
    """Return True iff every prime exponent in ``n`` is >= 2.  ``n >= 1``.

    The number 1 is powerful (the condition is vacuous).
    """
    if n < 1:
        return False
    n = int(n)
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            if e == 1:
                return False
        d = 3 if d == 2 else d + 2
    # Whatever remains is either 1 or a single prime to the first power.
    return n <= 1


def is_powerful_sympy(n: int) -> bool:
    """Return True iff every prime exponent in ``n`` is >= 2.  ``n >= 1``."""
    if n < 1:
        return False
    return all(e >= 2 for _, e in factor_sympy(int(n)))


def is_powerful_certified(n: int, B: int = 10 ** 5) -> bool:
    """Certified ``is_powerful`` for ``n <= B**3``, using trial division to ``B``.

    Why this is a *decision procedure* and not a heuristic:
      * remove from n, with full multiplicity, every prime factor <= B; call the
        remaining cofactor c.  Every prime factor of c is then > B;
      * if c == 1 then every prime exponent of n has been checked and is >= 2;
      * if c != 1, all its prime factors exceed B.  Since n <= B^3 we get
        c <= B^3, so c cannot have three prime factors (counted with
        multiplicity) above B: hence c = p or c = p^2 for a single prime p > B;
      * therefore n is powerful iff c == 1 or c is the square of a prime > B.
    The primality of sqrt(c) is itself certified by trial division to its square
    root (cheap because sqrt(c) <= B).

    For ``n > B**3`` this raises ValueError rather than guessing.
    """
    import math

    n = int(n)
    if n < 1:
        return False
    if n > B ** 3:
        raise ValueError(
            f"is_powerful_certified is only certified for n <= B**3 = {B**3}; got {n}"
        )
    m = n
    # trial division by odd numbers up to min(B, sqrt(m))
    d = 2
    while d <= B and d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d
                e += 1
            if e == 1:
                return False
        d = 3 if d == 2 else d + 2
    # now m is coprime to every prime <= min(B, sqrt(m_original))
    if m <= B:
        # fully factored; any remaining prime factor of the ORIGINAL n was >= 1
        # and we divided out everything <= B, so m must be 1 or a prime > B.
        # (m <= B and coprime to all primes <= B forces m == 1.)
        return m == 1
    r = math.isqrt(m)
    if r * r != m or r <= B:
        return False
    # r must be prime for m = r^2 to be powerful; trial divide r.
    d = 2
    while d * d <= r:
        if r % d == 0:
            return False
        d = 3 if d == 2 else d + 2
    return True


def is_powerful(n: int) -> bool:
    """Default predicate.  Correct for all ``n >= 1``; fast for ``n`` up to ~1e14."""
    return is_powerful_trial(n)


def canonical_decomposition(n: int) -> tuple[int, int]:
    """Return the unique ``(a, b)`` with ``n = a^2 * b^3`` and ``b`` squarefree.

    Proof that this exists and is unique.  Write n = prod_p p^{e_p}.  We must
    split e_p = 2*alpha_p + 3*beta_p with beta_p in {0, 1} and alpha_p >= 0; the
    condition that b is squarefree is exactly beta_p in {0,1}.  Every e_p >= 0 has
    a unique such decomposition, obtained from e_p mod 2:
      e_p even -> beta_p = 0, alpha_p = e_p/2;
      e_p odd  -> beta_p = 1, alpha_p = (e_p-3)/2, which requires e_p >= 3.
    Therefore beta_p = 1 forces e_p odd AND e_p >= 3, i.e. e_p in {3,5,7,...}.
    Consequently `n` is powerful iff no e_p equals 1, which is precisely the
    definition.  The exponents e_p are determined by unique factorization, so
    (a, b) is unique.
    """
    if n < 1:
        raise ValueError("canonical_decomposition requires n >= 1")
    n = int(n)
    a, b = 1, 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            if e % 2 == 1:
                # e is odd; for a powerful n we have e >= 3, so (e-3) is even >= 0.
                if e < 3:
                    raise ValueError(f"{n} is not powerful (exponent {e} at prime {d})")
                b *= d
                e -= 3
            a *= d ** (e // 2)
        d = 3 if d == 2 else d + 2
    if n > 1:
        # n is now prime with exponent 1.
        raise ValueError(f"input is not powerful (prime factor {n} to exponent 1)")
    return a, b


def radical(n: int) -> int:
    """Return rad(n) = product of the distinct primes dividing ``n`` (rad(1) = 1)."""
    if n < 1:
        raise ValueError("radical requires n >= 1")
    r = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            r *= d
            while n % d == 0:
                n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        r *= n
    return r


def is_squarefree(n: int) -> bool:
    """Return True iff no prime square divides ``n``."""
    if n < 1:
        return False
    n = int(n)
    d = 2
    while d * d <= n:
        if n % (d * d) == 0:
            return False
        d = 3 if d == 2 else d + 2
    return True


def squarefree_leq(limit: int) -> list[int]:
    """All squarefree positive integers <= ``limit``, in increasing order."""
    limit = int(limit)
    if limit < 1:
        return []
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = 0
    p = 2
    while p * p <= limit:
        if sieve[p]:
            pp = p * p
            sieve[pp::pp] = bytearray(len(sieve[pp::pp]))
        p += 1
    return [i for i in range(1, limit + 1) if sieve[i]]


def powerful_leq(limit: int) -> list[int]:
    """All powerful positive integers <= ``limit``, in increasing order.

    Complete and duplicate-free by construction: every powerful number has a unique
    form a^2 b^3 with b squarefree, and b^3 <= limit forces b <= limit^{1/3}.
    """
    limit = int(limit)
    if limit < 1:
        return []
    out: list[int] = []
    for b in squarefree_leq(int(limit ** (1 / 3)) + 2):
        b3 = b * b * b
        if b3 > limit:
            continue
        a_max = int((limit // b3) ** 0.5)
        while (a_max + 1) * (a_max + 1) * b3 <= limit:
            a_max += 1
        while a_max > 0 and a_max * a_max * b3 > limit:
            a_max -= 1
        out.extend(a * a * b3 for a in range(1, a_max + 1))
    out.sort()
    return out


def iter_powerful(limit: int) -> Iterator[int]:
    """Iterate powerful numbers <= ``limit`` in increasing order."""
    yield from powerful_leq(limit)


@lru_cache(maxsize=None)
def next_powerful(n: int) -> int:
    """Smallest powerful integer >= ``n`` (or None if it exceeds 10**30)."""
    if n <= 1:
        return 1
    cap = 10**30
    x = int(n)
    while x < cap:
        if is_powerful_trial(x):
            return x
        x += 1
    return None