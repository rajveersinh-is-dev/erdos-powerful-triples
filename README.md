# erdos-powerful-triples

> **Status: the conjecture is NOT solved here.**
> An autonomous investigation of the Erdős–Mollin–Walsh conjecture on three
> consecutive powerful numbers. It produces proved partial theorems, a proved
> *impossibility* result for an entire class of approaches, one explicitly
> falsified strategy, a verified literature review, and an exhaustive search to
> $10^{16}$.

---

## The problem

A positive integer $m$ is **powerful** (or *squarefull*) if every prime dividing it
divides it at least twice:

$$p \mid m \;\Longrightarrow\; p^2 \mid m .$$

Equivalently, $m$ has a **unique** representation $m = a^2b^3$ with $b$ squarefree.

> **Conjecture (Erdős–Mollin–Walsh).** There is no positive integer $n$ such that
> $n$, $n+1$ and $n+2$ are all powerful.

This is [Erdős problem #364](https://www.erdosproblems.com/364). It is open. It is
not settled here.

### Why it is hard, in one line

Consecutive *pairs* of powerful numbers are abundant — infinitely many come from the
Pell equation $x^2 = 8y^2 + 1$, giving $(8,9), (288,289), \dots$ — so the
difficulty is entirely in the **simultaneity** of three consecutive terms.

---

## Contents

- [What was proved](#what-was-proved)
- [Two results worth reading even if you ignore the rest](#two-results-worth-reading-even-if-you-ignore-the-rest)
- [Why `abc` does not finish the job](#why-abc-does-not-finish-the-job)
- [A clean reformulation](#a-clean-reformulation)
- [Computational results](#computational-results)
- [Bibliographic corrections](#bibliographic-corrections-found)
- [Reproducing everything](#reproducing-everything)
- [Repository layout](#repository-layout)
- [Limitations](#limitations)
- [References](#references)

---

## What was proved

| # | Result | Label |
| --- | --- | --- |
| 1 | **No purely congruence argument can ever prove this conjecture** — the locally admissible residue classes are non-empty at *every* modulus | PROVED |
| 2 | Exact admissible-class counts: $1,3,39,1209$ mod $4,9,900,44100$; in particular $n \equiv 7,27,35 \pmod{36}$ | PROVED |
| 3 | Structural constraints on a hypothetical triple | PROVED |
| 4 | Exact reformulation as two generalised Pell equations sharing the middle term | PROVED |
| 5 | **No triple whose middle term is $2^{2^m}$** | PROVED |
| 6 | Complete necessary condition for $2^k-1$ to be powerful | PROVED |
| 7 | **The strategy "`$d_3$ is even" is FALSE** — counterexample $(343,392,441)$ | PROVED FALSE |
| 8 | $abc(\varepsilon<1/3)$ $\Rightarrow$ **finitely many** triples | CONDITIONAL |
| 9 | No triple below $10^{16}$ | COMPUTATIONALLY VERIFIED |
| 10 | Reproduction of the load-bearing claims of Chan, She, Ma, Sayim, Bajpai–Bennett–Chan | cross-checked |

### The structural constraints (result 3)

If $n, n+1, n+2$ are powerful, with $n=a^2b^3$, $n+1=c^2d^3$, $n+2=e^2f^3$ and
$b,d,f$ squarefree, then

1. $n \equiv 3 \pmod 4$, $n+1 \equiv 0 \pmod 4$, $n+2 \equiv 1 \pmod 4$; in
   particular $n$ and $n+2$ are odd and $n$ is never a square;
2. $b \equiv 3 \pmod 4$ (so $b \ge 3$) and $f \equiv 1 \pmod 4$;
3. $b, d, f$ are pairwise coprime — so at most one of $n,n+1,n+2$ is a perfect square;
4. at most one of $n,n+1,n+2$ is a perfect cube.

Item 1 generalises the classical "no **four** consecutive powerful numbers" argument
(the four residues $0,1,2,3 \bmod 4$ are all hit, forcing a $2 \bmod 4$ term) — three
consecutive residues can dodge $2 \bmod 4$, which is exactly why the length-4 trick
stops working at length 3.

---

## Two results worth reading even if you ignore the rest

### 1. Congruences are provably powerless here

**Theorem.** Let $M\ge 1$. Call $r \bmod M$ *triple-admissible* if for every prime
$p$ with $p^2 \mid M$ and every $i \in \{0,1,2\}$ we have $p \mid r+i \Rightarrow p^2 \mid r+i$.
Then the set of triple-admissible classes is **never empty**, and its size is

$$\frac{M}{\prod_{p^2\mid M} p^2}\ \prod_{p^2\mid M} c_p,
\qquad c_2 = 1,\quad c_3 = 3,\quad c_p = p^2-3p+3 \ \ (p \ge 5).$$

*Why it matters.* A congruence argument only ever sees $n \bmod M$. To prove the
conjecture it would have to exclude **every** admissible class — and one always
survives. So the entire family of congruence-only attacks is structurally dead, and
any successful proof must use genuinely global input. This is a *positive* result
about a *negative*: it tells you where not to look.

It also explains Beckon's constraint $n \equiv 7, 27, 35 \pmod{36}$, and the sieve
density

$$\delta(L)=\tfrac14\cdot\tfrac13\prod_{5\le p\le L}\Bigl(1-\tfrac3p+\tfrac3{p^2}\Bigr)\asymp(\log L)^{-3},$$

measured numerically as $\delta(L)(\log L)^3 \to 4.85$ at $L=1999$ — sparse, but
never empty.

### 2. A promising route, killed by a five-digit counterexample

The reformulation below turns the conjecture into "`$d_3 > 1$". That invites a parity
attack: *if every 3-term arithmetic progression of powerful numbers had even common
difference, then $d_3 \ge 2$ and we would be done.*

This is false. But **it fails because we tested it first**:

$$343 = 7^3, \qquad 392 = 2^3\cdot 7^2, \qquad 441 = 3^2\cdot 7^2,$$

an arithmetic progression with common difference $d = 49$, which is **odd**. A second
example is $(169,256,343) = (13^2,\,2^8,\,7^3)$ with $d=87$.

The instructive part is *why*: the rigid mod-4 behaviour is a consequence of the
three terms being **consecutive** ($d=1$). For general odd $d$ only
"$N$ odd and $4 \mid N+d$" survives — and that is satisfiable. Concretely
$(7,8,9)$ has exactly that shape; the only defect is that $7$ is not powerful, and
multiplying by $49$ repairs it ($49\cdot7 = 7^3$, and $49\cdot8$, $49\cdot9$ already
are). More generally $(7,8,9)\cdot s$ is powerful exactly when $s$ is powerful and
$49 \mid s$, giving *infinitely many* odd common differences.

---

## Why `abc` does not finish the job

$(n+1)^2 = 1 + n(n+2)$ is an $abc$ relation. For powerful $m=a^2b^3$,

$$\operatorname{rad}(m)=\operatorname{rad}(ab)\le ab=\sqrt{m/b}\le\sqrt m ,$$

and since $n,n+1,n+2$ are pairwise coprime,
$\operatorname{rad}\bigl(n(n+1)(n+2)\bigr)\le\sqrt{n(n+1)(n+2)}$. Hence $abc$ gives

$$(n+1)^2 \;\le\; \kappa(\varepsilon)\,(n+2)^{\,3(1+\varepsilon)/2},$$

which is impossible for large $n$ when $\varepsilon < 1/3$ — the **sharp** threshold.

But this says **finitely many**, and EMW says **none**. *Finiteness is not emptiness:*
a finite non-empty solution set is compatible with $abc$. Converting finiteness into
nonexistence would need **either** an explicit $abc$ constant, so that the bound above
is small enough to search, **or** an unconditional argument eliminating the
survivors. This distinction is the single most common over-claim in the area, and it
is stated explicitly throughout this repository.

*Related:* a counterexample to EMW would also be a counterexample to Erdős's
conjecture in [problem #137](https://www.erdosproblems.com/137). The converse fails.

---

## A clean reformulation

Define

$$d_m=\min\{\,d:\ \exists N \text{ with } N,\, N+d,\, \dots,\, N+(m-1)d \text{ all powerful}\,\}.$$

Then **EMW is exactly $d_3 > 1$** (Bajpai–Bennett–Chan, §7). Note $d_2 = 1$, and
$(1,25,49)$ gives $d_3 \le 24$; they conjecture $d_3 = 24$. Unconditionally they prove
$\prod_{p \le m/2} p \mid d_m$ for $m \ge 4$ — with no analogue at $m=3$.

Equivalently, since $m$ is powerful iff $m = s\,t^2$ with $s$ squarefree and $s\mid t$,
the conjecture is equivalent to the following system having **no** solution in
squarefree $b,d,f$:

$$bV^2 + 1 = dU^2, \qquad fW^2 - dU^2 = 1, \qquad b\mid V,\;\; d\mid U,\;\; f\mid W .$$

This is a genuine **equivalence**, not a necessary condition, and it locates the
difficulty precisely: for fixed $(b,d)$ the first equation has either no solutions or
infinitely many, so it carries no finite information alone. The parameters are
unbounded, and "fix $(b,d,f)$ and compute integral points" gives no control over them.

---

## Computational results

### Exhaustive search to $10^{16}$: no triple

The search is $O(\sqrt X)$ rather than $O(X)$ because a triple forces $n\equiv3\pmod4$
and an odd powerful $m=a^2b^3$ satisfies $m\equiv b \pmod4$. So it suffices to
intersect the two explicit sets

$$P_3=\{a^2b^3 \le X+2 : a \text{ odd},\ b \text{ odd squarefree},\ b\equiv 3 \!\!\pmod 4\},\qquad
P_1=\{\dots : b \equiv 1 \!\!\pmod 4\},$$

and then test the middle term.

| $N$ | powerful numbers generated | triples |
| --- | --- | --- |
| $10^{12}$ | 799 138 | none |
| $10^{14}$ | 8 010 922 | none |
| $10^{16}$ | 80 200 497 | none |

Total wall time at $N=10^{16}$: about 5 s. Two independent generators are
cross-validated against brute force and against a closed-form counting function
(`tests/crossvalidate_generators.py`).

### Other verified facts

- Beckon's constraint reproduced; counts $39$ and $1209$ modulo $900$ and $44100$.
- First terms of **OEIS A076445** (powerful pairs at distance 2): $25, 70225, 130576327$.
- First terms of **OEIS A060355** (consecutive powerful pairs) below $5\cdot10^5$,
  including Golomb's $(12167,12168)=(23^3,\,2^3 3^2 13^2)$ — a pair where **neither**
  term is a square — and $(465124,465125)=(682^2,\,5^3\cdot61^2)$, predicted from the
  negative Pell equation $x^2-125y^2=-1$.
- No cube-centred candidate $(x^3-1,x^3,x^3+1)$ for $x \le 2\cdot10^5$.
- $2^k-1$ is not powerful for every $2 \le k \le 250$ (exact factorisation).
- **Certified** by complete Nagell–Lutz: $y^2 = x^3-81x+243$ (Cremona 1296f2) has
  trivial torsion.

### Two mistakes worth reading about

Both are in `research/falsification_log.md` with full explanations.

**A bug that briefly "disproved" a famous conjecture.** The fast search initially
reported triples at $130576327$ and $13837575261123$ — which are the 3rd and 5th terms
of A076445, i.e. powerful **pairs at distance 2**. The search never tested the
**middle** term, which is even and therefore lies in neither $P_1$ nor $P_3$. Caught,
fixed, and pinned by a regression test.

**Fabricated regression data.** A test initially asserted that $(423132,423133)$ were
consecutive powerful numbers. They are not: $423132 = 2^2\cdot3\cdot37\cdot953$.
Replaced with the computer-verified list.

---

## Bibliographic corrections found

1. **The attribution.** The three-consecutive-powerful question is raised by Erdős in
   *Congressus Numerantium* **XVI** (1976), 25–44, **p. 31** — *not* in
   *Publ. Math. Debrecen* **23** (1976), 271–282, which concerns consecutive *pairs*.
   The wrong citation has spread through the literature (including into
   Bajpai–Bennett–Chan §7).
2. **She's paper** is *Integers* **25** (2025), Paper **A103** (preprint
   arXiv:2507.16828).
3. **OEIS A076445 is not a table of search bounds** — it is a list of powerful *pairs
   at distance 2*, and it carries an uncertified "conjectured table" link. The widely
   quoted "$7.38\times10^{28}$" figure is therefore a *search result*, not a theorem.
4. **What Erdős actually asked** was whether infinitely many three-term progressions of
   *consecutive* powerful numbers exist ([#938](https://www.erdosproblems.com/938)),
   which van Doorn (arXiv:2605.06697) conjectures. That is strictly **stronger** than
   EMW.
5. The question originates in a **remark of Golomb** (1970), and was independently
   formulated by **Mollin and Walsh** (1986).

---

## Reproducing everything

```powershell
python -m pip install "numpy>=1.24" "sympy>=1.12" "z3-solver>=4.12"

python tests\test_powerful_triples.py                                   # 35/35 passed
python tests\crossvalidate_generators.py 3000000                       # PASS
python experiments\exp01_scale_search.py 1e9 1e10 1e11 1e12 1e13 1e14 1e15 1e16
python experiments\exp02_aps_parity.py                                  # ~1 s
python experiments\exp03_ap_parity_and_powers2.py                      # ~10 min
python experiments\exp04_literature_checks.py                          # ~1 min
```

The library itself has **no** required dependencies; `numpy`/`sympy`/`z3` are only
needed for the experiments. Exact reproduced outputs are in
[`docs/reproducibility.md`](docs/reproducibility.md), and raw JSON in `results/`.

---

## Repository layout

```
erdos-powerful-triples/
├── README.md                  this file
├── pyproject.toml  LICENSE  .gitignore
├── src/powerful_triples/
│   ├── predicates.py          three powerfulness predicates + the a²b³ decomposition
│   ├── residues.py            the exact local-admissibility theory
│   ├── search.py              five independent bounded search methods
│   └── scale.py               vectorised complete generation (the 10^16 search)
├── tests/
│   ├── test_powerful_triples.py       35 tests
│   └── crossvalidate_generators.py
├── experiments/
│   ├── exp01_scale_search.py           exhaustive search to 10^16
│   ├── exp02_aps_parity.py             3-term APs, parity of d, d₃
│   ├── exp03_ap_parity_and_powers2.py  the odd-d counterexample; the Fermat theorem
│   └── exp04_literature_checks.py      independent checks of the literature
├── results/                   raw JSON output
├── research/
│   ├── literature_review.md   every source retrieved, quoted, cross-checked
│   ├── known_results.md       the results table + all our theorems
│   ├── proof_attempts.md      six independent attacks, each with its obstruction
│   └── falsification_log.md   eleven falsified claims, with counterexamples
├── paper/
│   ├── main.tex               the write-up (12 sections, complete proofs)
│   └── references.bib
└── docs/
    └── reproducibility.md     exact commands and reproduced outputs
```

---

## Limitations

Stated plainly, because a rigorous negative report beats an inflated paper.

- The conjecture is **not** solved. The strongest new-to-us results are elementary.
- No LaTeX toolchain was available, so `paper/main.tex` was checked by static
  analysis only (balanced braces, matched environments) and **not compiled**. Every
  numerical claim inside it was re-verified by the code.
- No PARI/GP or SageMath, so the **rank-0** input to Sayim's Theorem 2 was *not*
  re-verified — only its torsion part. It is corroborated by the LMFDB record.
- A finite search is not a proof of a universal statement. $10^{16}$ bounds the
  search, not the conjecture.
- Every experiment was actually executed; no performance number in this repository is
  estimated.

---

## References

Full bibliography with verified identifiers in
[`paper/references.bib`](paper/references.bib) and detailed notes in
[`research/literature_review.md`](research/literature_review.md).

- Bajpai, Bennett, Chan — *Arithmetic progressions in squarefull numbers*,
  [arXiv:2302.03113](https://arxiv.org/abs/2302.03113), *Int. J. Number Theory* **20** (2024)
- Chan — *A note on three consecutive powerful numbers*,
  [arXiv:2503.21485](https://arxiv.org/abs/2503.21485), *Integers* **25** (2025), A7
- She — *Nonexistence of Consecutive Powerful Triplets Around Cubes with Prime-Square
  Factors*, [arXiv:2507.16828](https://arxiv.org/abs/2507.16828), *Integers* **25** (2025), A103
- Ma — *An elementary note on three consecutive powerful numbers*,
  [arXiv:2608.23418](https://arxiv.org/abs/2608.23418) (preprint)
- Sayim — *Nonexistence of consecutive powerful triplets around cubes with mixed prime
  factorizations*, [10.5281/zenodo.22699364](https://doi.org/10.5281/zenodo.22699364) (preprint)
- van Doorn — *Three-term arithmetic progressions of consecutive powerful numbers*,
  [arXiv:2605.06697](https://arxiv.org/abs/2605.06697) (preprint)
- Mian, Siddique — *A Kernel-Certified Verification of the Erdős–Mollin–Walsh Conjecture
  below $10^{14}$*, [arXiv:2609.25011](https://arxiv.org/abs/2609.25011)
- Golomb — *Powerful numbers*, *Amer. Math. Monthly* **77** (1970), 848–852
- Erdős — *Congressus Numerantium* **XVI** (1976), 25–44
- Mollin, Walsh — *C. R. Math. Rep. Acad. Sci. Canada* **8** (1986), 109–114;
  *IJMMS* **9**(4) (1986), 801–806
- Erdős Problems: [#137](https://www.erdosproblems.com/137),
  [#364](https://www.erdosproblems.com/364),
  [#365](https://www.erdosproblems.com/365),
  [#938](https://www.erdosproblems.com/938)
- OEIS: [A001694](https://oeis.org/A001694),
  [A060355](https://oeis.org/A060355),
  [A076445](https://oeis.org/A076445)

---

## License

MIT — see [`LICENSE`](LICENSE).