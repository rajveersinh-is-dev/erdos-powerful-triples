"""Experiment 2 -- the d_3 route to the Erdos-Mollin-Walsh conjecture.

Key reformulation (Bajpai-Bennett-Chan, arXiv:2302.03113, Section 7):  define

    d_m = min { d : there exist N with N, N+d, ..., N+(m-1)d all powerful }.

Then the Erdos-Mollin-Walsh conjecture is *exactly* the statement d_3 > 1.

This experiment asks a sharper question:

    (Q)  Is d_3 EVEN?

If (Q) has answer "yes" then d_3 >= 2 and the EMW conjecture follows
immediately.  So (Q) is a genuine sufficient condition for the conjecture, and a
clean attack: it replaces "no consecutive powerful triple" by the structural
statement "a 3-term AP of powerful numbers always has even common difference".

What is actually computed here (all bounded, none of it a proof):
  (1) all 3-term APs of powerful numbers with N <= X and d <= D, split by parity
      of d -- searched two independent ways (forward from N, and from pairs);
  (2) the minimum d found (should reproduce d_3 = 24 from N = 1);
  (3) explicit check of the elementary necessary condition proved in the paper:
      if d is odd then N is odd and N = -d (mod 4).
"""

from __future__ import annotations

import json
import time

from powerful_triples.predicates import powerful_leq
import _bootstrap  # noqa: F401  (puts <repo>/src on sys.path; write_result)





def search_aps(limit_n: int, max_d: int) -> dict:
    """All (N, d) with N, N+d, N+2d powerful, N <= limit_n, d <= max_d."""
    # Method 1: forward scan over every powerful N.
    pwf = powerful_leq(limit_n + 2 * max_d)
    s = set(pwf)
    forward: list[tuple[int, int]] = []
    for n in pwf:
        if n > limit_n:
            break
        for d in range(1, max_d + 1):
            if (n + d) in s and (n + 2 * d) in s:
                forward.append((n, d))

    # Method 2: independent scan -- pick the middle term and use its two
    # symmetric neighbours.  (N, N+d, N+2d) is recovered as
    # (m - d, d) with m = N + d.
    middle: list[tuple[int, int]] = []
    for m in pwf:
        for d in range(1, max_d + 1):
            if (m - d) in s and (m + d) in s and m - d >= 1:
                middle.append((m - d, d))
    forward_set = set(forward)
    middle_set = set(middle)
    return {
        "limit_n": limit_n,
        "max_d": max_d,
        "method1": sorted(forward_set),
        "method2": sorted(middle_set),
        "agree": forward_set == middle_set,
        "odd_d": sorted(x for x in forward_set if x[1] % 2 == 1),
        "even_d": sorted(x for x in forward_set if x[1] % 2 == 0),
        "min_d": min((d for _n, d in forward_set), default=None),
    }


def main() -> int:
    """Entry point — parse arguments and run the main computation.
    
    Returns:
        int: Result of type int
    
    """
    out = {}
    t0 = time.perf_counter()
    # 1. Small bound, both methods, generous d  -> find d_3 and look for odd d.
    r1 = search_aps(limit_n=200_000, max_d=600)
    out["small"] = r1
    print(f"[limit_n=200000, max_d=600]  methods agree: {r1['agree']}")
    print(f"  number of 3-term APs found : {len(r1['method1'])}")
    print(f"  with EVEN d               : {len(r1['even_d'])}")
    print(f"  with ODD  d               : {len(r1['odd_d'])}   {r1['odd_d'][:20]}")
    print(f"  minimal d found           : d_3 <= {r1['min_d']}")

    # 2. Larger N with moderate d, to push on the odd-d question.
    for lim, md in [(2_000_000, 200), (20_000_000, 100)]:
        t = time.perf_counter()
        r = search_aps(limit_n=lim, max_d=md)
        print(
            f"[limit_n={lim}, max_d={md}]  methods agree: {r['agree']}  "
            f"APs: {len(r['method1'])}  even-d: {len(r['even_d'])}  "
            f"odd-d: {len(r['odd_d'])}  min d: {r['min_d']}  ({time.perf_counter()-t:.1f}s)"
        )
        if r["odd_d"]:
            print(f"    ODD-d examples: {r['odd_d'][:10]}")
        out[f"scan_{lim}"] = {k: v for k, v in r.items() if k != "method1" or len(v) < 200}

    # 3. Verify the necessary condition for odd d:  N odd and N = -d (mod 4).
    bad = [
        (n, d)
        for n, d in r1["method1"]
        if d % 2 == 1 and not (n % 2 == 1 and (n + d) % 4 == 0)
    ]
    print(f"odd-d APs violating the necessary condition (expect 0): {len(bad)}")

    out["elapsed_s"] = round(time.perf_counter() - t0, 2)
    path = _bootstrap.write_result("exp02_aps.json", out)
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())