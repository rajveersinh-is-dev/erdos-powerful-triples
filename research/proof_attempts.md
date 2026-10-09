# Proof attempts: six independent attacks

For each attack: exact target, known results used, intermediate lemmas required,
strongest result obtained, exact obstruction, whether it is genuinely new.

---

## Attack 1 — Elementary congruences

**Target.** Find a modulus $M$ (or a family of moduli) such that every residue class
mod $M$ is excluded, proving EMW.

**Known results used.** None (self-contained).

**Lemmas developed.**
1. A powerful number is never $\equiv2\pmod4$. (Hence no *four* consecutive ones.)
2. If $n,n+1,n+2$ are powerful then $n\equiv3\pmod4$.
3. **Exact local-admissibility theory.** For $M=\prod p^{k_p}$ and
   $S(M)=\prod_{p^2\mid M}p^2$: the number of triple-admissible classes mod $M$ is
   $\frac{M}{S(M)}\prod_{p^2\mid M}c_p$ with $c_2=1$, $c_3=3$, $c_p=p^2-3p+3$.
4. **Non-emptiness theorem.** For every $M$, at least one triple-admissible class
   survives.

**Strongest result.** Theorem 2.2 (non-emptiness) — a *negative* theorem: **no
purely congruence argument in $n$ can prove EMW.** Plus the positive recovery of
Beckon's constraint $n\equiv7,27,35\pmod{36}$ and the counts $39$ (mod 900) and
$1209$ (mod 44100), which match Sayim's Prop. 3 exactly.

**Obstruction.** The sieve thins but never empties: density
$\asymp(\log L)^{-3}$. Local conditions are satisfiable simultaneously at every
modulus, so the triple hypothesis is locally consistent *for all $M$*.

**Novelty.** The non-emptiness statement for the original conjecture is, as far as
we can determine, not in the literature (Sayim's Remark 14 makes an analogous point
for one specific equation; Ma and Sayim state the mod-36 constraint and the counts
without the non-emptiness theorem). We state this conservatively: independently
derived, not claimed to be new.

---

## Attack 2 — Algebraic reformulation via squarefree decomposition

**Target.** Turn the squarefree parameters $b,d,f$ into bounded objects.

**Known results used.** Golomb's $m=a^2b^3$ with $b$ squarefree (unique).

**Lemmas developed.**
1. **Lemma 2.5 (proof in the package):** $m$ is powerful $\iff m=st^2$ with $s$
   squarefree and $s\mid t$. Proof: from $m=a^2b^3$ take $s=b$, $t=ab$;
   conversely from $m=st^2$, $s\mid t$, put $a=t/s$, $b=s$.
2. **Reformulation (equivalence, not just necessity).** A triple exists iff there
   are squarefree $b,d,f$ and integers $U,V,W>0$ with
   $$ bV^2+1 = dU^2,\qquad fW^2-dU^2=1, \qquad b\mid V,\ d\mid U,\ f\mid W.$$
   This is a pair of **generalized Pell equations sharing the middle term**
   $dU^2=n+1$.
3. Structural constraints: $b\equiv3\bmod4$ (so $b\ge3$), $f\equiv1\bmod4$,
   $b,d,f$ pairwise coprime, $n$ and $n+2$ odd.

**Strongest result.** The exact reformulation, proved to be an equivalence, and the
parameter constraints. These are what make the vectorised search of Attack 5
complete, and they are used to prune Method C.

**Obstruction.** $b,d,f$ are unbounded. "Fix $(b,d,f)$ and compute integral points"
(Siegel) gives finitely many points per triple of parameters but **no control over
the parameters**, so the reduction does not terminate. Note also that
$dU^2-bV^2=1$ has infinitely many solutions for fixed $(b,d)$ whenever one exists,
so even a complete Pell analysis of one equation is useless on its own — exactly the
trap flagged in the brief ("do not assume a Pell parametrisation of one pair
parametrizes a triple").

**Novelty.** The reformulation is standard algebra; the pairwise-coprimality and
mod-4 parameter constraints are elementary. Not claimed as new.

---

## Attack 3 — Pell equations and recurrence sequences

**Target.** Exploit the fact that $d=1$ makes the middle term even and the outer
terms odd; use recurrence structure.

**Known results used.** Mahler (Pell $x^2=8y^2+1$), the closure map
$(u,u+1)\mapsto(4u(u+1),(2u+1)^2)$ (ours, proved), BBC's $d_m$ reformulation.

**Lemmas developed.**
1. **Closure lemma (PROVED).** From a consecutive powerful pair, another one.
2. **Theorem (necessary condition for odd $d$, PROVED).** If $N,N+d,N+2d$ are
   powerful and $d$ is odd then $N$ is odd and $N\equiv-d\bmod4$; the middle term
   is the even one.
3. **Conditional $\omega(k)$ bound (PROVED).** If $2^k-1$ powerful and no primitive
   divisor of $2^d-1$ ($d\mid k$) is Wieferich base 2, then $\omega(k)\le2$
   (Zsigmondy + divisor counting).

**Strongest result.** Item 2, and the falsification that motivated it.

**Obstruction (decisive).** The natural plan was: EMW $\iff d_3>1$, so show $d_3$ is
even. This is **false**: $(343,392,441)=(7^3,2^3 7^2,3^2 7^2)$ has $d=49$ odd, and
$(169,256,343)$ has $d=87$. Mod-4 rigidity holds only for $d=1$. Moreover the
closure lemma shows descent on pairs can never terminate (F10). We found no
recurrence that a hypothetical triple must sit in.

**Novelty.** The closure lemma was independently pointed out on the Erdős Problems
thread, so not claimed as new. The odd-$d$ counterexamples and the odd-$d$
necessary condition: as far as we can determine, not recorded in the literature
(BBC discuss $d_3=24$ and $d_m=\prod_{p\le m}p^2$, all even, and do not mention odd
$d$).

---

## Attack 4 — Diophantine geometry and integral-point methods

**Target.** Reduce a hypothetical triple to a rational/integral point on a curve
and use known point sets.

**Known results used.** Sayim's route: 18-case split, five Mordell curves
$y^2=x^3+k$ for $k\in\{2,-2,54,-54,-162\}$ (Gebel–Pethő–Zimmer; Bennett–Ghadermarzi),
and the rank-0 curve $E:y^2=x^3-81x+243$ (Cremona 1296f2 / LMFDB 1296.k1).

**Lemmas developed (all verified computationally by us).**
1. The five Mordell integral-point lists are exactly as quoted (searched
   $|x|\le2\cdot10^6$).
2. $E(\mathbb Q)_{\mathrm{tors}}=\{\mathcal O\}$ — **certified** by a complete
   Nagell–Lutz check ($4A^3+27B^2=-3^{12}$, so $y\in\{\pm3^j:0\le j\le6\}\cup\{0\}$;
   no integral solutions).
3. The Pell recurrence $z_{k+1}=14z_k-z_{k-1}+6$, $(z_0,z_1)=(-2,1)$, equals the
   closed form $z_j=\frac{3c_j-1}{2}$ where $(2+\sqrt3)^{2j-1}=b_j+c_j\sqrt3$
   (8 consecutive indices agree), and the only cube in the orbit for $j\le2000$ is
   $z_1=1$ (largest $|z_j|$ has 2287 digits).

**Strongest result.** A partial, *independent* descent towards Sayim's Theorem 2:
in $\mathbb Z[\omega]$ we reduce $t^6+t^3+1=3w^2$ to
$\alpha=\varepsilon\gamma^2$ with $\alpha=\frac{2t^3+1}{3}+\frac{t^3-1}{3}\omega$,
$\gcd(\alpha,\bar\alpha)=1$, and we **completely solve the unit class
$\varepsilon=\pm1$** (giving $u^2-4uv=1$, hence $t=1$). The classes
$\varepsilon=\omega,\omega^2$ reduce to $(v+u)^2-3u^2=1$ with
$t^3=3s(s-2u)-2$, which we could not resolve — and those are precisely the
operative classes for Sayim's branch.

**Obstruction.** (i) Curve reductions only cover *restricted* families (a fixed
shape for the outer terms, or a cube middle term); they are not injective or
even finite-to-one onto the full triple locus, so nothing here excludes every
possible triple. (ii) The rank-0 input of Sayim's Theorem 2 could **not** be
re-verified here (no PARI/GP or SageMath in this environment); it is corroborated
only by the LMFDB record. (iii) Our own descent stalls in the non-square unit class.

**Novelty.** The unit-class descent is our own and is recorded as **partial only**.

---

## Attack 5 — Computational discovery of structural restrictions

**Target.** Find restrictions that a purely theoretical attack could not see, and
push the search far enough to be a meaningful (if bounded) check.

**Method.** (A) direct enumeration; (B) generate all powerful numbers via the
canonical $a^2b^3$ decomposition and scan for runs; (C) search the $(b,d,f)$
parameter space of the Attack-2 reformulation; (D) exact local pre-screen mod 36;
(E) z3 SMT over a bounded box for the two equations. Plus a sixth, scale-oriented
route: split by the forced residue classes $P_3,P_1$ and intersect (O($\sqrt X$)).

**Strongest results.**
* No triple with $n\le10^{16}$ (two independent generators, cross-validated by
  brute force at $3\cdot10^6$ and by an independent closed-form count).
* **No cube-centred candidate triple for $x\le2\cdot10^5$** — consistent with
  Chan/She/Ma/Sayim, and empirically contextualising those results.
* **Odd-$d$ 3-term APs exist**: $(343,392,441)$ ($d=49$), $(169,256,343)$ ($d=87$),
  and 12 further examples with $N\le2\cdot10^5$; none with odd $d<49$ for
  $N\le10^{10}$.
* Reproduction of the first terms of A076445 and A060355, including the non-square
  pair $(465124,465125)=(682^2,5^3\cdot61^2)$ predicted from the negative Pell
  equation $x^2-125y^2=-1$.
* An **independent certified predicate** `is_powerful_certified(n, B)` for
  $n\le B^3$ (trial division to $B$, then the residual must be $1$ or the square of
  a prime $>B$) — cross-validated against full factorisation on 4073 values with
  zero disagreements.

**Obstruction.** A finite search cannot prove a universal statement. The search also
found **no new restriction**: everything it produced was already implied by
Theorem 2.4, except the odd-$d$ observation.

**Novelty.** The method (F1's residue-class split) is the only way we found to make
$10^{16}$ reachable in seconds; the odd-$d$ counterexample is the only novel output.

---

## Attack 6 — New inequality / descent / incompatibility argument

**Target.** Find an unconditional obstruction that applies to all three terms
simultaneously.

**Ideas pursued.**
1. *$abc$-style radical bound.* Derived the sharp unconditional inequality
   $$\operatorname{rad}\big(n(n+1)(n+2)\big)\le\sqrt{n(n+1)(n+2)},$$
   with the sharp identity $\operatorname{rad}(a^2b^3)=ab=\sqrt{n/b}$ so
   $\operatorname{rad}=\sqrt{n(n+1)(n+2)/(bdf)}$. Combined with
   $(n+1)^2=n(n+2)+1$ this yields the conditional finiteness with $\epsilon<1/3$.
   **Obstruction:** no unconditional lower bound for $\operatorname{rad}$ in terms of
   $n$ of the needed strength exists; this *is* the $abc$ conjecture.
2. *Jacobi-symbol incompatibility.* Derived six symbol conditions and showed they are
   mutually **consistent** (falsification_log F4). Dead.
3. *Descent.* Shown impossible on pairs (closure lemma, F10). Dead.
4. *Parity of the common difference.* Falsified by $(343,392,441)$ (F2). Dead.
5. *Powers of 2 in the middle term.* **Partial positive result:** Theorem 2.6
   ($2^{2^m}-1$ never powerful) and Proposition 2.7 (the Wieferich characterisation),
   the latter leading to a conditional $\omega(k)\le2$.
   **Obstruction:** Wieferich primes; no route without them.

**Strongest result.** Theorems 2.6 and 2.7 — genuine unconditional exclusions of an
infinite family of candidate triples, plus a precise necessary condition.
**Genuinely new?** Theorem 2.6 is an immediate consequence of Fermat-number
coprimality and is very likely folklore; Proposition 2.7 is elementary. We describe
both as *new to us*, not as claimed-new results.

---

## The strongest remaining obstacle, stated once

Every attack above reduces to the same wall:

> The local (congruence) conditions are simultaneously satisfiable at every modulus
> (Theorem 2.2). The squarefree parameters $b,d,f$ are unbounded. Conditional on
> $abc$, the radical inequality is just strong enough to make the solution set
> *finite* — and finiteness is not emptiness. **Any successful unconditional proof
> must produce genuinely global information about the triple that no congruence and
> no finite computation can supply.** We did not find such an input.