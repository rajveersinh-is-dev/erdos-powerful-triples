# erdos-powerful-triples

An autonomous investigation of the **Erdős–Mollin–Walsh conjecture**:

> There is no positive integer $n$ for which $n$, $n+1$ and $n+2$ are all
> **powerful** (squarefull), where $m$ is powerful iff $p\mid m \Rightarrow p^2\mid m$.

## Bottom line

**The conjecture is not solved here.** The literature review confirms it is open as of
October 2026; this repository does not change that. What it does contain:

| | Result | Label |
| --- | --- | --- |
| 1 | **No purely congruence argument can ever prove this conjecture** — the locally admissible residue classes are non-empty at *every* modulus | PROVED |
| 2 | Exact count of admissible classes: $1,3,39,1209$ mod $4,9,900,44100$; Beckon's constraint $n\equiv7,27,35\pmod{36}$ | PROVED + COMPUTATIONALLY VERIFIED |
| 3 | Structural theorems on a hypothetical triple ($n\equiv3\bmod4$; $b\equiv3$, $f\equiv1\bmod4$; $b,d,f$ pairwise coprime; at most one square / one cube) | PROVED |
| 4 | An exact reformulation as **two generalised Pell equations sharing the middle term** | PROVED |
| 5 | **No triple whose middle term is $2^{2^m}$** (Fermat numbers are pairwise coprime) | PROVED |
| 6 | Complete necessary condition for $2^k-1$ to be powerful (prime divides $k$, or is Wieferich to base 2) | PROVED |
| 7 | **The strategy "$d_3$ is even" is FALSE**: $(343,392,441)=(7^3,\,2^3 7^2,\,3^2 7^2)$ has odd common difference $49$ | PROVED FALSE |
| 8 | $abc$ with $\epsilon<1/3$ ⟹ **finitely many** triples — and an explicit explanation of why that is *not* nonexistence | CONDITIONAL |
| 9 | No triple below $10^{16}$ | COMPUTATIONALLY VERIFIED |
| 10 | Reproduction, from source, of the key claims of Chan 2025, She 2025, Ma 2026, Sayim 2026, Bajpai–Bennett–Chan 2024 | cross-checked |

## The single most useful structural fact

EMW is equivalent to a one-line statement (Bajpai–Bennett–Chan, §7):

$$d_m=\min\{d:\ \exists N \text{ with } N,N+d,\dots,N+(m-1)d \text{ powerful}\},\qquad \text{EMW}\iff d_3>1.$$

That looks promising — ruling out *parity classes* of $d$ would settle it. But it
does not work: odd common differences occur, e.g. $d=49$. So the promising-looking
route is closed, and that is recorded as a proved negative result rather than quietly
dropped.

## Why congruence methods cannot work (Theorem 2.2)

For a modulus $M=\prod p^{k_p}$, a class $r$ is *triple-admissible* if for every prime
$p$ with $p^2\mid M$ and every $i\in\{0,1,2\}$, $p\mid r+i$ implies $p^2\mid r+i$.
Then

$$\#\{\text{admissible classes mod }M\}=\frac{M}{\prod_{p^2\mid M}p^2}\prod_{p^2\mid M}c_p,
\qquad c_2=1,\; c_3=3,\; c_p=p^2-3p+3\ (p\ge5),$$

and **this is always $>0$** (for $p\ge5$, $c_p=(p-1)(p-2)+1\ge1$; the $p=2$ and $p=3$
cases are computed directly). Since a congruence argument only ever sees $n\bmod M$,
and one admissible class always survives, **no purely congruence argument in $n$
can prove the conjecture.** Global input is unavoidable. (Sayim's Remark 14 makes an
analogous point for one specific equation; the statement above is about the original
conjecture and is proved elementarily.)

## Why $abc$ gives only finiteness

$(n+1)^2=1+n(n+2)$ is an $abc$ relation, and for powerful $m=a^2b^3$,
$\operatorname{rad}(m)\le ab=\sqrt{m/b}\le\sqrt m$. Since $n,n+1,n+2$ are pairwise
coprime, $\operatorname{rad}(n(n+1)(n+2))\le\sqrt{n(n+1)(n+2)}$, so

$$(n+1)^2\ \le\ \kappa(\epsilon)\,(n+2)^{3(1+\epsilon)/2},$$

which is impossible for large $n$ when $\epsilon<1/3$. **Finiteness is not
emptiness**: a finite non-empty solution set is compatible with $abc$. Turning this
into EMW needs an explicit $abc$ constant (so the bound is searchable) or an
unconditional exclusion of the survivors. We have neither.

## Computational result

Exhaustive, cross-validated search with **no triple below $10^{16}$** (5.3 s for the
largest bound). The search is $O(\sqrt X)$ because a triple forces $n\equiv3\bmod4$
and an odd powerful $m=a^2b^3$ satisfies $m\equiv b\pmod4$, so only two explicit
$O(\sqrt X)$ sets need to be intersected.

The two integers that survive the weaker test "$n$ and $n+2$ powerful" below $10^{16}$
are $130576327$ and $13837575261123$ — the 3rd and 5th terms of OEIS A076445 — and in
both cases the **middle** term is not powerful. Omitting that middle-term test was a
real bug in an early version of the search that produced two apparent
counterexamples to a famous conjecture; it is documented, fixed, and pinned by a
regression test (`research/falsification_log.md` §F1).

## Repository layout

```
erdos-powerful-triples/
├── README.md                     this file
├── pyproject.toml
├── LICENSE                       MIT
├── src/powerful_triples/
│   ├── predicates.py             three powerfulness predicates + a^2 b^3 decomposition
│   ├── residues.py               exact local-admissibility theory
│   ├── search.py                 five independent bounded search methods
│   └── scale.py                  vectorised complete generation; the 10^16 search
├── tests/
│   ├── test_powerful_triples.py  35 tests
│   └── crossvalidate_generators.py
├── experiments/
│   ├── exp01_scale_search.py       exhaustive search to 10^16
│   ├── exp02_aps_parity.py         3-term APs, parity of d, d_3
│   ├── exp03_ap_parity_and_powers2.py   odd-d counterexample; 2^(2^m)-1 theorem
│   └── exp04_literature_checks.py  independent checks of Chan/She/Ma/Sayim/BBC/ABC
├── results/                      raw JSON output of the experiments
├── research/
│   ├── literature_review.md      every source retrieved, quoted, and cross-checked
│   ├── known_results.md          the known-results table + all our theorems
│   ├── proof_attempts.md         six independent attacks, each with its obstruction
│   └── falsification_log.md      11 falsified claims, with counterexamples
├── paper/
│   ├── main.tex                  the write-up
│   └── references.bib
└── docs/
    └── reproducibility.md        exact commands and reproduced outputs
```

## Reproduce

```powershell
python tests\test_powerful_triples.py                                    # 35/35
python tests\crossvalidate_generators.py 3000000                        # PASS
python experiments\exp01_scale_search.py 1e9 1e10 1e11 1e12 1e13 1e14 1e15 1e16
python experiments\exp02_aps_parity.py
python experiments\exp03_ap_parity_and_powers2.py                        # ~10 min
python experiments\exp04_literature_checks.py                            # ~1 min
```

See `docs/reproducibility.md` for the reproduced outputs.

## Bibliographic corrections found during this investigation

1. The three-consecutive-powerful question is raised by Erdős in
   *Congressus Numerantium* **XVI** (1976), 25–44, p. 31 — **not** in
   *Publ. Math. Debrecen* **23** (1976), 271–282, which concerns pairs. The wrong
   citation is widespread.
2. She's paper is **Integers 25 (2025), Paper A103** (preprint arXiv:2507.16828).
3. OEIS A076445 is a list of powerful **pairs at distance 2**, not a table of search
   bounds; the "$7.38\times10^{28}$" figure is a search result, and the OEIS entry
   carries a "conjectured table" link, so completeness of the list is not certified.
4. Erdős's own question was whether infinitely many three-term progressions of
   *consecutive* powerful numbers exist (Erdős Problems #938), which van Doorn
   (arXiv:2605.06697) conjectures; that is strictly stronger than EMW.

## Final verdict

**Category D — computational and structural progress.**

A rigorous negative report is preferable to an inflated paper. The strongest
*new-to-us* results are elementary (Theorem 2.2 and the exclusion of middle terms
$2^{2^m}$); the most valuable outcomes of the investigation are (a) certifying that
the entire congruence approach is structurally impossible, (b) falsifying the
$d_3$-parity route with an explicit counterexample, (c) verifying — and in one case
partially re-verifying — the literature's load-bearing claims, and (d) a fast,
independently validated search to $10^{16}$.

**The Erdős–Mollin–Walsh conjecture remains unsolved by this investigation. No
complete proof has been established.**