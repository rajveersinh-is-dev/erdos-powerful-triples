"""Cross-validation of the two independent powerful-number generators.

`predicates.powerful_leq` is pure Python (iterating squarefree b, then a).
`scale.generate_odd_powerful_class` is numpy-vectorised and uses the *additional*
structural restriction a odd, b = bmod (mod 4) coming from Theorem 3.1.

If both are correct then, for the odd powerful numbers up to L,
    {powerful_leq(L)} = P1 union P3   (disjoint union, odd part only)
and we additionally check that every odd powerful number is 1 or 3 mod 4 and that
its canonical b parameter is 1 or 3 mod 4 respectively.
"""

from __future__ import annotations

import sys
import time

from powerful_triples.predicates import canonical_decomposition, is_powerful_trial, powerful_leq
from powerful_triples.scale import count_odd_powerful, generate_odd_powerful_class


def main(limit: int = 2_000_000) -> int:
    t0 = time.perf_counter()
    ref = [m for m in powerful_leq(limit) if m % 2 == 1]
    t_ref = time.perf_counter() - t0

    p1 = generate_odd_powerful_class(limit, 1).tolist()
    p3 = generate_odd_powerful_class(limit, 3).tolist()

    failures = 0
    # 1. every generated value is powerful
    for m in p1 + p3:
        if not is_powerful_trial(m):
            print(f"FAIL: {m} generated but not powerful")
            failures += 1
            break
    # 2. union equals the reference odd powerful numbers
    union = sorted(set(p1) | set(p3))
    if union != ref:
        print(f"FAIL: union != reference (|union|={len(union)}, |ref|={len(ref)})")
        only_u = set(union) - set(ref)
        only_r = set(ref) - set(union)
        print("  only in union:", sorted(only_u)[:10])
        print("  only in ref  :", sorted(only_r)[:10])
        failures += 1
    # 3. disjointness
    if set(p1) & set(p3):
        print("FAIL: P1 and P3 overlap")
        failures += 1
    # 4. residue classes
    if any(m % 4 != 1 for m in p1):
        print("FAIL: element of P1 not = 1 mod 4")
        failures += 1
    if any(m % 4 != 3 for m in p3):
        print("FAIL: element of P3 not = 3 mod 4")
        failures += 1
    # 5. closed-form count agrees
    closed = count_odd_powerful(limit)
    if closed != len(ref):
        print(f"FAIL: count_odd_powerful={closed} != {len(ref)}")
        failures += 1
    # 6. canonical decomposition is consistent with the residue class
    for m in ref[:2000]:
        a, b = canonical_decomposition(m)
        if (a * a * b ** 3) != m:
            print(f"FAIL: decomposition mismatch at {m}")
            failures += 1
            break
        if m % 4 != b % 4:
            print(f"FAIL: m mod 4 != b mod 4 at {m} (b={b})")
            failures += 1
            break
    # 7. all P3 values have b = 3 mod 4 forced
    for m in p3[:2000]:
        _a, b = canonical_decomposition(m)
        if b % 4 != 3:
            print(f"FAIL: P3 element {m} has b={b} not = 3 mod 4")
            failures += 1
            break

    print(
        f"limit={limit}: |odd powerful|={len(ref)} (ref {t_ref:.2f}s) |P1|={len(p1)} "
        f"|P3|={len(p3)} closed-form-count={closed}"
    )
    print("CROSS-VALIDATION:", "PASS" if failures == 0 else f"FAIL ({failures} problems)")
    return 1 if failures else 0


if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    raise SystemExit(main(lim))