# Literature review — the Erdős–Mollin–Walsh conjecture on three consecutive powerful numbers

Status of this document: every bibliographic item below was **retrieved and checked**
during this investigation (arXiv abstract + full text, Zenodo record + PDF, OEIS entry,
Erdős Problems database entry, LMFDB). Items that could not be fully verified are
marked **[UNVERIFIED]** together with what exactly is missing. Claims quoted from
other papers are marked as *claims*: they have not been re-proved here, only
cross-checked computationally where that is possible (see §7).

---

## 1. The conjecture

**Conjecture (Erdős–Mollin–Walsh; EMW).** There is no positive integer $n$ for which
$n$, $n+1$ and $n+2$ are all *powerful*, where a positive integer is powerful
(squarefull) if $p \mid n \Rightarrow p^2 \mid n$ for every prime $p$.

Attribution chain (verified, and *corrected* relative to the commonly repeated version):

| Step | Statement | Verified source |
| --- | --- | --- |
| Origin | A remark of **S. W. Golomb**, *Powerful numbers*, Amer. Math. Monthly **77** (1970), 848–852 | BBC [B] §7: "which appears to originate in a remark of Golomb [12]" |
| Raised by Erdős | **P. Erdős**, *Problems and results on number theoretic properties of consecutive integers and related questions*, Proc. Fifth Manitoba Conf. (1975), **Congress. Numer. XVI** (1976), 25–44, p. 31 | Erdős Problems entry cites "ErGr80, p. 68"; Sayim [S] v1.3 documents the correction |
| Independent formulation | **R. A. Mollin and P. G. Walsh**, *A note on powerful numbers, quadratic fields and the Pellian*, C. R. Math. Rep. Acad. Sci. Canada **8** (1986), 109–114 | BBC [B] ref. [18] |
| Also | **R. A. Mollin and P. G. Walsh**, *On powerful numbers*, Internat. J. Math. & Math. Sci. **9**(4) (1986), 801–806 | Chan [C], She [H] reference lists |

**Bibliographic caution.** The frequently repeated citation
"Erdős, *Publ. Math. Debrecen* **23** (1976), 271–282" is **wrong** for the
three-consecutive-powerful question; that paper (Erdős, *Problems and results on
consecutive integers*) discusses consecutive *pairs*. The correct reference is the
*Congressus Numerantium* paper above (p. 31). Sayim [S] v1.3 §"Version 1.3"
documents this, noting the misattribution also appears in
Bajpai–Bennett–Chan [B] §7. The `erdosproblems.com/364` entry lists both
"Er76d" and "ErGr80, p. 68" without disambiguation.

### 1.1 The $d_m$ reformulation (the cleanest way to state the problem)

BBC [B] §7 define, for $m \ge 2$,
$$ d_m=\min\{\,d:\ \exists N \text{ such that } N, N+d, \dots, N+(m-1)d \text{ are all powerful}\,\}, $$
with $d_2=1$. Then

> **EMW is exactly the statement $d_3>1$.**

BBC report (from computation) that they *suspect* $d_3 = 24$, realised by
$N=1$: $(1, 25, 49)$. We reproduce this: see `experiments/exp02_aps_parity.py`,
which finds $\min d = 24$ over its scan range. BBC also prove unconditionally
that $\prod_{p \le m/2} p \mid d_m$ for $m \ge 4$ (hence $m \ll \log d_m \ll m$),
and that $d_m \le \prod_{p \le m} p^2$ by the classical construction.

**Our addition (§6 below):** $d_3$ can be *odd* — $(343,392,441)$ is a
3-term AP of powerful numbers with $d=49$. This kills a natural sufficient
condition for EMW ("$d_3$ is even") that is not, as far as we can determine,
recorded anywhere.

---

## 2. Pairs are easy; triples are the hard part

* **Mahler** (reported by Erdős Problems #364 and #365, and by BBC [B]):
  the Pell equation $x^2 = 8y^2+1$ has infinitely many solutions, and
  $8y^2$ and $x^2$ are then consecutive powerful numbers. First: $(8,9)$,
  then $(288,289)$, $(12240,12241)$, $\dots$
* **Golomb [G]** gave $(12167, 12168) = (23^3,\; 2^3 3^2 13^2)$, a consecutive
  powerful pair in which **neither** term is a square. This refutes the natural
  guess that all consecutive powerful pairs come from Pell equations.
* **Walker** (1976, cited on Erdős Problems #365) proved
  $7^3 x^2 = 3^3 y^2 + 1$ has infinitely many solutions, giving infinitely many
  counterexamples to that guess. *This reference is taken from the Erdős Problems
  entry; I did not retrieve the original paper. [UNVERIFIED]*
* OEIS **A060355** lists the $n$ with $n, n+1$ both powerful.
* **Aktas & Murty**, *Fundamental units and consecutive squarefull numbers*,
  Int. J. Number Th. **13** (2017), 243–252. *Cited by BBC [B] ref. [1]; not
  retrieved. [UNVERIFIED]*

**Why this matters for the triple problem.** Golomb's example shows that a
Pell-type parameterisation of *one* consecutive powerful pair does **not**
parametrise all of them, and therefore any attack that reduces the triple
problem to a single Pell equation must justify why no Pell-type families are
missed. BBC [B] Theorem 1.2 handles the related $k$-full analogues.

### 2.1 A closure lemma for pairs (ours, elementary, verified)

If $(u, u+1)$ are both powerful then so are
$$ A = 4u(u+1),\qquad B = (2u+1)^2,\qquad B-A = 1. $$
*Proof.* The product of powerful numbers is powerful (exponents add), and $4$ is
powerful, so $A$ is powerful; $B$ is a square. $B-A=4u^2+4u+1-4u^2-4u=1$. ∎
Verified numerically in `tests/test_powerful_triples.py::test_closure_lemma`:
$(8,9)\mapsto(288,289)\mapsto(332928,332929)$ and so on. (This was also pointed
out informally on the Erdős Problems #364 discussion thread, so it is not
claimed as new.)

---

## 3. Local (congruence) results

| Result | Statement | Status |
| --- | --- | --- |
| Quadruples | There are no 4 consecutive powerful numbers: among any 4 consecutive integers one is $\equiv 2 \pmod 4$, and a powerful number is never $\equiv 2 \pmod 4$ (a powerful $m$ has $v_2(m) \ne 1$). | **PROVED** (elementary, in the present paper as Prop. 3.3) |
| $n \bmod 4$ | If $n,n+1,n+2$ are powerful then $n \equiv 3 \pmod 4$ | **PROVED** (Prop. 3.1) |
| Beckon | $n \bmod 36 \in \{7,27,35\}$ | **PROVED** by us independently (Thm. 2.6); also credited by Ma [M] and Sayim [S] to "Beckon". *The original Beckon source is not identified in any of the papers we read. [UNVERIFIED]* |
| Counts mod $p^2$ | exactly $1$, $3$, $p^2-3p+3$ admissible classes for $p=2,3,p\ge5$ | **PROVED** (Cor. 2.5); matches Sayim [S] Prop. 3 |
| Counts mod 900, 44100 | 39 and 1209 | **PROVED + COMPUTATIONALLY VERIFIED** by us; identical to Sayim [S] Prop. 3 |
| No local obstruction | For every $M\ge1$ the set of locally admissible classes is non-empty | **PROVED** (Thm. 2.4) — so no congruence-only argument can work. See §6.3 |

The last two rows of the table are the main reason a purely congruence-based
attack cannot succeed, and they are proved in the present paper rather than
asserted.

---

## 4. Conditional results: the $abc$ conjecture

Erdős Problems #364: "The abc conjecture implies there are only finitely many such
triples." BBC [B] Theorem 1.1 makes this precise and stronger.

**The mechanism (ours, made explicit; it is the $\ell=2$ case of BBC Lemma 3.1).**
Assume there are no such triples and let $n$ be a hypothetical one. Then
$$ (n+1)^2 = n(n+2) + 1 $$
is an $abc$ triple $(A,B,C) = (n(n+2),\,1,\,(n+1)^2)$. For any powerful $m$
with $m=a^2b^3$ ($b$ squarefree),
$$ \operatorname{rad}(m)=\operatorname{rad}(ab)\ \le\ ab=\sqrt{m/b}\ \le \sqrt m,$$
so, since $n,n+1,n+2$ are pairwise coprime,
$$ \operatorname{rad}\big(n(n+1)(n+2)\big)\le\sqrt{n(n+1)(n+2)}. $$
Hence $abc$ with exponent $\epsilon$ gives
$$ (n+1)^2 \le \kappa(\epsilon)\,\big(n(n+1)(n+2)\big)^{(1+\epsilon)/2},
$$
i.e. $2\log n \le \frac{3(1+\epsilon)}{2}\log n + O_\epsilon(1)$. For
$\epsilon<1/3$ this is impossible for large $n$.

> **Conditional Theorem.** $abc(\epsilon)$ for some $0<\epsilon<1/3$ implies that
> **only finitely many** triples $n,n+1,n+2$ of powerful numbers exist.

(The same identity with $\ell=2$ in BBC Lemma 3.1 reads
$(N+d)^2 = N^2 + d(2N+d)$; setting $d=1$ gives exactly the above. BBC's
inequality (1.3) specialised to $(m,k)=(3,2)$ reads $d \gg N^{2/5-\epsilon}$,
which for $d=1$ likewise bounds $N$; our exponent is sharper because we keep
only the three radicals.)

### 4.1 Finiteness is NOT nonexistence — the exact logic

**This is the single most important logical point in this document.**

$f =$ "the set $\mathcal{T}$ of triples is finite" does **not** entail
$|\mathcal{T}| = 0$. So $abc$ does **not**, on its own, prove EMW. What EMW
requires is that *every* element of $\mathcal{T}$ is excluded. Concretely:

* $abc(\epsilon<1/3)$ gives $\mathcal{T}$ finite — compatible with $\mathcal{T}\ne\emptyset$.
* To finish one would need **either** an explicit form of $abc$ (with a known
  $\kappa(\epsilon)$), so that the bound above can be searched, **or** an
  unconditional argument excluding the finitely many survivors.
* Note in particular that the general AP statement of BBC Thm. 1.1 is
  *vacuous* for $(m,k)=(3,2)$: the exponent in their (1.2) becomes
  $\frac{3(1-\frac12)-2}{3(1-\frac14)-2} = -2$, i.e. a trivial lower bound.

**Relationship with Erdős Problems #137.** If $n,n+1,n+2$ were all powerful
then $n(n+1)(n+2)$ would be powerful, i.e. no prime would divide it to exponent
exactly 1. Erdős [Er82c] conjectured that for fixed $k$ and large $n$ some prime
always divides $m(m+1)\cdots(m+k)$ to the first power only. Thus
**a counterexample to EMW would be a counterexample to Erdős's #137 conjecture
at $k=3$**. The converse fails: a product being powerful is much weaker than
each factor being powerful.

---

## 5. Restricted-family results (all unconditional except where noted)

### 5.1 Cube-centred triples

The most active line of work in 2025–2026. Write the triple as
$(x^3-1,\, x^3,\, x^3+1)$; $x^3$ is automatically powerful. Two "shapes" for the
outer terms:

* **Chan [C]** — T. H. Chan, *A note on three consecutive powerful numbers*,
  **Integers 25** (2025), Paper A7, 7 pp (arXiv:2503.21485). Proves there are
  no consecutive powerful numbers of the form
  $x^3-1=p^3y^2,\; x^3,\; x^3+1=q^3z^2$ for primes $p,q$ and $x,y,z>0$.
  Methods: Pell equations, elliptic curves, second-order recurrences.
  **Claim status: theorem (special case).**
* **She [H]** — J. She, *Nonexistence of Consecutive Powerful Triplets Around
  Cubes with Prime-Square Factors*, arXiv:2507.16828 (v3, 24 Sep 2025);
  published as **Integers 25** (2025), Paper **A103**. Proves there are no
  triples $x^3-1=p^2a^3,\; x^3,\; x^3+1=q^2b^3$ for primes $p,q$ and integers
  $a,b,x$ (no positivity needed). Also a Corollary 1 on
  $x^6-1=p^2q^2a^3$. Methods: modular arithmetic, $p$-adic valuations, Thue
  equations, elliptic curves. **Claim status: theorem (special case).**
* **Ma [M]** — W. Ma, *An elementary note on three consecutive powerful numbers*,
  arXiv:2608.23418 (24 Aug 2026), preprint v1, no journal reference.
  **Theorem 1.2 (verbatim):** "There are no three consecutive powerful numbers
  of the form $x^{n}-1=q_{1}^{3}y^{2},\quad x^{n},\quad x^{n}+1=q_{2}^{3}z^{2},$
  where $q_{1},q_{2}$ are primes, $x,y,z\in\mathbb{Z}$ and $n\ge 5$ is an
  integer that only contains prime factors belonging to
  $S:=\{\text{prime } p\ge 5 \mid p\equiv 5 \bmod 8\}$."
  Relies on Lebesgue ($x^m-y^2=1$ has no solution for $m\ge2$ — reproved in
  the paper), Chao–Ko ($x^n-y^2=-1$ has no solution for $n>3$ — reproved),
  Nagell–Ljunggren ($\frac{x^n-1}{x-1}$ a square only for $(n,x)=(4,7),(5,3)$ —
  only a proof *sketch* is given), Catalan/Mihăilescu.
  No computational component beyond a single hand check ($x=3,n=5$: $242$ not
  powerful). **Claim status: theorem (special case), unrefereed preprint; the
  Nagell–Ljunggren input is quoted from memory of the literature and only
  sketched.**
* **Sayim [S]** — B. Y. Sayim, *Nonexistence of consecutive powerful triplets
  around cubes with mixed prime factorizations*, Zenodo
  **10.5281/zenodo.22699364** (v1.3, 11 Sep 2026), CC BY 4.0; code at
  `github.com/berkay-yueksel-sayim/emw-mixed-powerful-triplets`.
  **Theorem 1 (verbatim):** "There are no integers $x\ge 2$, primes $p,q$, and
  integers $a,b,y,z$ such that either (M1) $x^3-1=p^2a^3$ and $x^3+1=q^3z^2$,
  (M2) $x^3-1=p^3y^2$ and $x^3+1=q^2b^3$." This closes the 2×2 grid of
  shapes $\{p^3\cdot\square,\ p^2\cdot\mathrm{cube}\}^2$ around a cube.
  **Theorem 2 (verbatim):** "The only solutions of $t^6+t^3+1=3w^2$ in rational
  numbers are $(t,w)=(1,\pm1)$."
  **Claim status: preprint, self-declared, AI-assisted, no refereeing. The single
  non-elementary input is computer-certified.** We verified this input as far as
  possible (§7).

### 5.2 What is still open

None of Chan, She, Ma or Sayim addresses the general conjecture; each covers a
restricted "shape". Ma states explicitly: *"It appears to be very hard and remains
open."* Sayim states: *"The conjecture remains open; under the abc-conjecture at
most finitely many triples exist."* All four results concern $x^3$ as the middle
term; nothing is known for a general middle term.

---

## 6. Other relevant literature

* **BBC [B]** — P. Bajpai, M. A. Bennett, T. H. Chan, *Arithmetic progressions in
  squarefull numbers*, arXiv:2302.03113; journal version
  **Int. J. Number Theory 20** (2024). Theorem 1.1 (conditional $abc$ size
  constraints on $m$-term APs of $k$-full numbers), Theorem 1.2 (unconditional
  infinite families with $\gcd(d,N)=1$ for $(m,k)\in\{(3,2),(3,3),(4,2)\}$),
  Corollary 1.3 ($abc$ implies $A^\infty(2)=4$, $A^\infty(3)=3$,
  $A^\infty(k)=2$ for $k\ge4$), and §7 (the $d_m$ reformulation).
  The $(4,2)$ construction uses the elliptic curve
  $y^2-128xy-3360y=x^3-2612x^2+149568x$ and the divisibility sequence
  $\psi_n$ with period $2628=36\cdot 73$ mod $73$.
* **van Doorn [V]** — W. van Doorn, *Three-term arithmetic progressions of
  consecutive powerful numbers*, arXiv:2605.06697 (4 May 2026), preprint.
  Shows infinitely many 3-term APs $N, N+d, N+2d$ of powerful numbers with
  $d = 2\sqrt N + 1$, and **conjectures** that infinitely many of these consist
  of three consecutive terms of the sequence of powerful numbers — which would
  answer Erdős Problems **#938** ("are there only finitely many three-term
  progressions of consecutive terms $n_k,n_{k+1},n_{k+2}$?") in the negative.
  Note this is about *consecutive powerful numbers* (gaps), which is strictly
  more general than EMW ($d=1$).
* **Mian & Siddique [MS]** — I. Mian, S. Siddique, *A Kernel-Certified
  Verification of the Erdős-Mollin-Walsh Conjecture below $10^{14}$*,
  arXiv:2609.25011 (29 Jul 2026), preprint (math.GM / cs.LO). Machine-checked
  Lean 4 theorems that no triple exists below $10^{12}$ and below $10^{14}$,
  with axiom footprint exactly $\{\mathrm{propext},\ \mathrm{Classical.choice},\
  \mathrm{Quot.sound}\}$ — no `sorry`, no `native_decide`. The proof reduces to
  odd numbers via a mod-4 argument, represents odd powerful numbers as
  $a^2b^3$ with $a,b$ odd and $b$ squarefree, enumerates them with a
  kernel-reducible fuelled generator, and eliminates the **seven** surviving
  distance-2 pairs below $10^{14}$ (the members of A076445 below $10^{14}$) by
  explicit non-powerfulness witnesses. They state: "Larger uncertified
  computations exist (exhaustive to $10^{22}$; conditionally to about
  $7.38\times10^{28}$); our contribution is not a computational record."
* **Erdős & Selfridge [ES]** (1975): the product of $k\ge3$ consecutive
  positive integers is never a perfect power. Relevant to #137, hence to EMW.
* **Erdős–Szekeres (1934)**: $P_2(x)=\frac{\zeta(3/2)}{\zeta(3)}x^{1/2}+O(x^{1/3})$.
  We use $\zeta(3/2)/\zeta(3)\approx 2.1732$ when discussing sieve densities.
* **Beckon** — a "mod-36 constraint on consecutive powerful triples", cited by
  Ma [M] and Sayim [S]. Original source not identified. **[UNVERIFIED]**
  (we reproduce the constraint independently, §3).
* **OEIS A076445** — "The smaller of a pair of powerful numbers that differ by 2",
  i.e. it is **not** a table of search bounds. Erdős Problems #364 says "By OEIS
  A076445 there are no such $n$ for $n<7.38\times10^{28}$", i.e. the largest
  known such pair is $73840550964522899559001927225\approx 7.38\cdot10^{28}$.
  A commenter (Yuchen Li, 21 Dec 2025) gives the same bound explicitly as
  $\le 73840550964522899559001927226$. We verified the first four terms of
  A076445 ourselves (see §7, test `test_pairs_differing_by_2_reproduce_oeis_A076445`).
  Note the OEIS entry itself carries a "Max Alekseyev, Conjectured table of
  n, a(n) for n=1..33" link, so the list is **not** certified complete; the
  $7.38\cdot10^{28}$ figure should be read as a *search* result, not a theorem.

---

## 7. What we checked ourselves

Full details, commands and outputs are in `docs/reproducibility.md`; raw numbers
in `results/`.

1. **Beckon's mod-36 constraint** re-derived and verified: triple-admissible
   classes mod 36 are exactly $\{7,27,35\}$.
2. **Counts 39 and 1209** mod 900 and 44100 — exactly matching Sayim Prop. 3.
3. **Density rate.** $\prod_{5\le p\le L}(p^2-3p+3)/p^2 \cdot(\log L)^3$ is
   computed to be $3.41, 4.59, 4.84, 4.85$ at $L = 11, 101, 1009, 1999$,
   converging — i.e. the rate is indeed $\asymp(\log L)^{-3}$, as Sayim claims.
4. **First terms of A076445** reproduced: $25, 70225, 130576327$ below $2\cdot10^8$.
5. **First terms of A060355 reproduced**: consecutive powerful pairs below
   $5\cdot10^5$ are $(8,9),(288,289),(675,676),(9800,9801),(12167,12168),
   (235224,235225),(332928,332929),(465124,465125)$ — including Golomb's
   $(12167,12168)$ and the "non-square" example $(465124,465125)
   =(682^2,\;5^3\cdot61^2)$ predicted from the negative Pell equation
   $x^2-125y^2=-1$.
6. **Mordell integral points.** The five lists used by Sayim are confirmed:
   $y^2=x^3+k$ has, for $k = 2,-2,54,-54,-162$, exactly
   $\{(-1,\pm1)\}$, $\{(3,\pm5)\}$, $\{(3,\pm9)\}$, $\{(7,\pm17)\}$, $\varnothing$
   (we searched $|x|\le 2\cdot10^6$; *completeness* of these lists rests on the
   cited tables of Gebel–Pethő–Zimmer and Bennett–Ghadermarzi, which we did not
   re-derive).
7. **The load-bearing elliptic curve of Sayim's Theorem 2.**
   $E: y^2=x^3-81x+243$ is Cremona **1296f2** / LMFDB **1296.k1**. We
   **certified** that $E(\mathbb Q)_{\mathrm{tors}}=\{\mathcal O\}$ by a complete
   Nagell–Lutz check ($4A^3+27B^2=-3^{12}$, so $y\in\{\pm3^j:0\le j\le6\}$ or
   $y=0$; no integral solutions). We **did not** re-verify the rank-0
   computation (no PARI/GP or SageMath available in this environment); it is
   corroborated by the LMFDB record (rank 0, analytic rank 0, trivial torsion,
   0 integral points), independently fetched.
8. **The Pell orbit behind Sayim's Theorem 2.** We reproduced the recurrence
   $z_{k+1}=14z_k-z_{k-1}+6$, $(z_0,z_1)=(-2,1)$, cross-checked it against the
   closed form $z_j=\frac{3c_j-1}{2}$ where $(2+\sqrt3)^{2j-1}=b_j+c_j\sqrt3$,
   at 8 consecutive indices (all agree), and confirmed that the only cube in the
   orbit for $j\le 2000$ is $z_1=1$ (matching Sayim's reported scan, whose
   "more than 2200 decimal digits" we reproduce as 2287).
9. **Chan/She/Sayim/Ma shape families.** For $x\le 2\cdot10^4$ we counted how
   often $x^3-1$ or $x^3+1$ is powerful in either of the two shapes, and
   confirmed that **no** $x\le2\cdot10^5$ makes both $x^3-1$ and $x^3+1$
   powerful — so there is no cube-centred candidate triple in that range,
   consistent with all four papers.
10. **Exhaustive triple search to $10^{16}$** — see §8 and `results/scale_search.json`.

---

## 8. Computation

Our own exhaustive search (two independent generators, cross-validated) finds
**no** triple of consecutive powerful numbers with $n \le 10^{16}$.

| $N$ | powerful numbers generated (odd, both classes) | candidates with $n,n+2$ powerful | triples |
| --- | --- | --- | --- |
| $10^9$ | 25 019 | 1 | none |
| $10^{10}$ | 79 487 | 1 | none |
| $10^{11}$ | 252 163 | 1 | none |
| $10^{12}$ | 799 138 | 1 | none |
| $10^{13}$ | 2 530 755 | 1 | none |
| $10^{14}$ | 8 010 922 | 2 | none |
| $10^{15}$ | 25 349 939 | 2 | none |
| $10^{16}$ | 80 200 497 | 2 | none |

The two candidates that appear at $10^{14}$ and above are $130576327$ and
$13837575261123$ — precisely the 3rd and 5th terms of A076445. In both cases the
**middle** term is not powerful, which is why they are not triples.

This is *weaker* than the $7.38\cdot10^{28}$ figure in the literature but is a
fully self-contained, independently cross-validated verification, and it is
*stronger* than the $10^{14}$ kernel-certified bound in one sense only: no proof
kernel is involved, so it is an uncertified computation. **A finite search is not
a proof of a universal statement.**

---

## 9. Summary of the current state

* The general conjecture is **open**. No unconditional proof or disproof exists
  as of this investigation.
* The best unconditional results are restricted-family theorems around a cube
  middle term (Chan 2025; She 2025; Ma 2026 preprint; Sayim 2026 preprint).
* $abc$ gives finiteness only.
* Purely local/congruence methods cannot possibly work (proved here).
* The most promising remaining structural reformulation is $d_3>1$; but the
  natural parity route to it is false (proved here by counterexample).

## References

- **[B]** P. Bajpai, M. A. Bennett, T. H. Chan, *Arithmetic progressions in squarefull numbers*, arXiv:2302.03113; Int. J. Number Theory 20 (2024).
- **[C]** T. H. Chan, *A note on three consecutive powerful numbers*, arXiv:2503.21485; Integers 25 (2025), Paper A7.
- **[ES]** P. Erdős, J. L. Selfridge (1975), on products of consecutive integers being perfect powers.
- **[G]** S. W. Golomb, *Powerful numbers*, Amer. Math. Monthly 77 (1970), 848–852.
- **[H]** J. She, *Nonexistence of Consecutive Powerful Triplets Around Cubes with Prime-Square Factors*, arXiv:2507.16828; Integers 25 (2025), Paper A103.
- **[M]** W. Ma, *An elementary note on three consecutive powerful numbers*, arXiv:2608.23418.
- **[MS]** I. Mian, S. Siddique, *A Kernel-Certified Verification of the Erdős-Mollin-Walsh Conjecture below $10^{14}$*, arXiv:2609.25011.
- **[S]** B. Y. Sayim, *Nonexistence of consecutive powerful triplets around cubes with mixed prime factorizations*, Zenodo 10.5281/zenodo.22699364 (v1.3).
- **[V]** W. van Doorn, *Three-term arithmetic progressions of consecutive powerful numbers*, arXiv:2605.06697.
- Erdős Problems database: #137, #364, #365, #938 (erdosproblems.com).
- OEIS: A001694, A060355, A076445.