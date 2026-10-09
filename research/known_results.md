# Known-results map and the present contribution

Every claim carries an explicit label:

* **PROVED** — complete proof given in `paper/main.tex` (or in §2 below).
* **KNOWN** — established in the literature, citation verified in
  `research/literature_review.md`.
* **COMPUTATIONALLY VERIFIED** — checked over a precisely specified finite domain
  by code in this repository; the bound is always stated.
* **CONJECTURED** — plausible, unproved.
* **UNRESOLVED** — the essential step is missing.

---

## 1. The known-results table

| Result | Exact statement | Assumptions | Proof method | Relevance | Label |
| --- | --- | --- | --- | --- | --- |
| Quadruples impossible | No 4 consecutive positive integers are all powerful | none | elementary (one is $2 \bmod 4$) | Shows the mod-4 idea *does* work for length 4 | PROVED |
| EMW <=> $d_3>1$ | With $d_m:=\min\{d: \exists N,\ N..N+(m-1)d \text{ powerful}\}$, EMW is $d_3>1$ | none | definition | The cleanest reformulation | KNOWN (BBC §7) |
| $d_3 \le \prod_{p\le3}p^2=36$; $d_3=24$ realised by $(1,25,49)$ | upper bound + witness | none | explicit | $d_3>1$ needs only $d=1$ excluded | KNOWN (BBC §7); we re-verify the witness |
| $\prod_{p\le m/2}p\mid d_m$ | for $m\ge4$ | none | local prime counting | No analogue for $m=3$ ($p\le1.5$) | KNOWN (BBC §7) |
| $abc \Rightarrow$ finiteness of triples | $abc(\epsilon)$ for some $0<\epsilon<1/3$ | **conditional** | $(n+1)^2=n(n+2)+1$, $\operatorname{rad}\le\sqrt{n(n+1)(n+2)}$ | Finiteness only — **not** EMW | KNOWN / derived here |
| Beckon | $n\bmod36\in\{7,27,35\}$ | none | congruences mod 4 and 9 | Reproduced independently | PROVED + COMPUTATIONALLY VERIFIED |
| Counts | $\#=$ 1, 3, 39, 1209 mod $4,9,900,44100$ | none | CRT | Reproduces Sayim Prop. 3 exactly | PROVED + COMPUTATIONALLY VERIFIED |
| No local obstruction | For every $M$, the locally admissible set is non-empty | none | CRT | **Kills all congruence-only attacks** | PROVED |
| Chan 2025 | No triple $x^3-1=p^3y^2,\ x^3,\ x^3+1=q^3z^2$ | restricted shape | Pell, elliptic curves, recurrences | one of 4 cells of the shape grid | KNOWN (special case) |
| She 2025 | No triple $x^3-1=p^2a^3,\ x^3,\ x^3+1=q^2b^3$ | restricted shape | $p$-adic, Thue, elliptic | one of 4 cells | KNOWN (special case) |
| Ma 2026 (preprint) | No triple $x^n\mp1=q_{1,2}^3(\cdot)^2$ for $n\ge5$ all of whose prime factors are $5 \bmod 8$ | restricted shape + restricted $n$ | Lebesgue, Chao–Ko, Nagell–Ljunggren, residues | extends the middle power | KNOWN (special case, unrefereed) |
| Sayim 2026 (preprint) | No triple with *mixed* outer shapes; and $t^6+t^3+1=3w^2 \Rightarrow t=1$ | restricted shape | 18-case split, 5 Mordell curves, rank-0 elliptic quotient $E: y^2=x^3-81x+243$ (Cremona 1296f2) | closes the 4-cell grid around cubes | KNOWN (special case, AI-assisted preprint); elliptic input PARTIALLY re-verified by us |
| Kernel check to $10^{14}$ | No triple below $10^{14}$ | machine-checked in Lean 4, axiom footprint $\{\mathrm{propext},\mathrm{Classical.choice},\mathrm{Quot.sound}\}$ | proof kernel | removes trusted code from the evidence chain | KNOWN (Mian–Siddique, arXiv:2609.25011) |
| No triple below $10^{16}$ | as stated | — | our code, two cross-validated generators | independent check | COMPUTATIONALLY VERIFIED |
| No triple with middle term $=2^{2^m}$ | $(2^{2^m}-1,\;2^{2^m},\;2^{2^m}+1)$ never all powerful | $m\ge1$ | Fermat numbers pairwise coprime | excludes an infinite family of candidate middle terms | **PROVED (ours)** |
| Necessary condition for odd common difference | If $N,N+d,N+2d$ powerful and $d$ odd then $N$ odd and $N\equiv-d\pmod4$ | none | mod 4 | needed for any parity attack | **PROVED (ours)** |
| "$d_3$ is even" | FALSE | — | counterexample $(343,392,441)$ | kills a plausible route to EMW | **PROVED FALSE (ours)** |
| $\omega(k)\le2$ | If $2^k-1$ powerful and no primitive divisor of $2^d-1$ ($d\mid k$) is Wieferich to base 2, then $k$ has $\le2$ distinct prime factors | conditional on a Wieferich hypothesis | Zsigmondy + counting | the only handle found on the $n+1=2^k$ subcase | PROVED conditionally (ours) |
| No 3 consecutive powerful numbers | EMW | none | — | the target | **UNRESOLVED** |

---

## 2. Theorems proved in this investigation (complete proofs in `paper/main.tex`)

### 2.1 No four consecutive powerful numbers (PROVED)

If $m$ is powerful and $2\mid m$ then $v_2(m)\ge2$, so $m\equiv0\pmod4$; hence a
powerful $m$ is never $\equiv2\pmod4$. Among any four consecutive integers exactly
one is $\equiv2\pmod4$.

### 2.2 Theorem: no local obstruction (PROVED)

Let $M\ge1$. Call $r\bmod M$ *triple-admissible* if for every prime $p$ with
$p^2\mid M$ and every $i\in\{0,1,2\}$, $p\mid r+i$ implies $p^2\mid r+i$.
Then the set of triple-admissible classes mod $M$ is never empty.

*Proof.* Work prime-power-wise. For $p=2$: avoiding $2\bmod4$ three times forces
$r\equiv3\bmod4$ — non-empty. For $p=3$: the forbidden set is $\{1,\dots,6\}\bmod9$,
so $\{0,7,8\}$ works. For $p\ge5$ exactly $3(p-1)$ classes mod $p^2$ are forbidden
(the sets $\{pt-i: 1\le t\le p-1\}$, $i=0,1,2$, are pairwise disjoint because
$|i-i'|<p$), and $3(p-1)<p^2$, so one survives. Primes with $v_p(M)=1$ impose
nothing. Combine by CRT.

**Why this matters.** Any proof depending only on the residue of $n$ modulo some
fixed $M$ must exclude *every* triple-admissible class. Since one always survives,
**no purely congruence argument in $n$ can prove EMW.** Global input is
unavoidable. (Sayim [S] Remark 14 makes a related point for one specific
equation; the statement above is about the original conjecture.)

### 2.3 Theorem: local counts (PROVED)

With $S(M)=\prod_{p^2\mid M}p^2$,
$$ \#\{\text{triple-admissible classes mod } M\} = \frac{M}{S(M)}\prod_{p^2\mid M}c_p,
\qquad c_2=1,\quad c_3=3,\quad c_p=p^2-3p+3\ (p\ge5).$$
Hence exactly 1, 3, 39, 1209 classes mod $4$, $9$, $900$, $44100$; in particular
$n\equiv7,27,35\pmod{36}$. The density of admissible classes modulo
$\prod_{p\le L}p^2$ is
$\frac14\cdot\frac13\prod_{5\le p\le L}\left(1-\frac3p+\frac3{p^2}\right)\asymp(\log L)^{-3}$:
sparse, but never empty.

### 2.4 Theorem: structural constraints on a hypothetical triple (PROVED)

If $n,n+1,n+2$ are powerful, with $n=a^2b^3$, $n+1=c^2d^3$, $n+2=e^2f^3$ ($b,d,f$
squarefree), then

1. $n\equiv3\pmod4$, $n+1\equiv0\pmod4$, $n+2\equiv1\pmod4$; $n,n+2$ odd;
2. $b\equiv3\pmod4$ (hence $b\ge3$) and $f\equiv1\pmod4$;
3. $b,d,f$ are pairwise coprime, so at most one of them equals $1$;
4. at most one of $n,n+1,n+2$ is a perfect square, and at most one a perfect cube;
5. equivalently ($m$ powerful $\iff m=s\,t^2$ with $s$ squarefree, $s\mid t$): the
   problem is equivalent to the *system* $fW^2-dU^2=2$, $bV^2+1=dU^2$, together with
   $b\mid V$, $d\mid U$, $f\mid W$.

*Proof.* (1) A powerful number is never $2\bmod4$; among $n,n+1,n+2$ one is $2\bmod4$
unless $n\equiv3\pmod4$. (2) For odd $m=a^2b^3$, $a$ is odd, so $a^2\equiv1\pmod8$
and $m\equiv b^3\equiv b\pmod4$. (3) $\gcd(n,n+1)=\gcd(n+1,n+2)=1$ and
$\gcd(n,n+2)\mid2$ with $n$ odd. (4) Two squares differ by 1 or 2, impossible for
positive squares ($y^2-x^2=(y-x)(y+x)$); two cubes differ by $\ge7$.

### 2.5 Theorem: necessary condition for odd common difference (PROVED)

If $N,N+d,N+2d$ are powerful and $d$ is odd, then $N$ is odd and $N\equiv-d\pmod4$,
so $4\mid N+d$ and the middle term is the even one.
*Proof.* If $N$ were even then $N$ and $N+2d$ are both even and differ by
$2d\equiv2\pmod4$, so exactly one is $\equiv2\pmod4$ — impossible. Hence $N$ is odd,
$N+2d$ is odd, $N+d$ is even, and $N+d\not\equiv2\pmod4$.

### 2.6 Theorem: middle term a power of 4 (PROVED)

For every $m\ge1$, $2^{2^m}-1$ is not powerful; hence no triple
$(2^{2^m}-1,\;2^{2^m},\;2^{2^m}+1)$ of consecutive powerful numbers exists.
*Proof.* With $F_j=2^{2^j}+1$, $2^{2^m}-1=\prod_{j<m}F_j$, and
$\prod_{j<i}F_j = F_i-2$ gives $\gcd(F_i,F_j)=1$ for $i\ne j$. Each $F_j>1$ therefore
occurs with exponent exactly $1$.

### 2.7 Proposition: necessary condition for $2^k-1$ to be powerful (PROVED)

If $2^k-1$ is powerful then every prime $p\mid 2^k-1$ satisfies $p\mid k$ or
$p$ is Wieferich to base 2, i.e. $2^{p-1}\equiv1\pmod{p^2}$.
*Proof.* Let $r=\operatorname{ord}_p(2)\mid k$. Since $p^2\mid 2^k-1$,
$\operatorname{ord}_{p^2}(2)\mid k$. Now $\operatorname{ord}_{p^2}(2)\in\{r,pr\}$. If
it equals $pr$ then $p\mid k$; if it equals $r$, then $2^r\equiv1\pmod{p^2}$ and
$r\mid p-1$, so $2^{p-1}\equiv1\pmod{p^2}$.

*Conditional consequence.* If additionally no primitive prime divisor $p_d$ of
$2^d-1$ ($d\mid k$, $d\ge3$, $d\ne6$) is Wieferich, Zsigmondy gives distinct
$p_d\equiv1\pmod d$, each dividing $k$; counting gives $\tau(k)\le\omega(k)+2$, and
$\tau(k)\ge2^{\omega(k)}$ forces $\omega(k)\le2$. This is the only handle we found on
the $n+1=2^k$ subcase, and it rests on a hypothesis about Wieferich primes.

### 2.8 Disproof of a plausible route (PROVED FALSE)

**Claim tested:** "every 3-term AP of powerful numbers has even common difference",
which would give $d_3\ge2$ and hence EMW.
**Counterexample:** $343=7^3$, $392=2^3\cdot7^2$, $441=3^2\cdot7^2$ with $d=49$.
Second example: $(169,256,343)$ with $d=87$. Full list of odd-$d$ APs below
$2\cdot10^5$ in `results/exp02_aps.json`.
**Minimum odd $d$:** no 3-term AP of powerful numbers with odd $d<49$ has $N\le10^{10}$
(COMPUTATIONALLY VERIFIED).
**What survives:** EMW $\iff d_3>1$ is exactly as open as before; the parity route is
closed. See `research/falsification_log.md` (F2).

---

## 3. What remains unresolved — the strongest remaining obstacle

The conjecture reduces to a single concrete Diophantine question:

> **Question.** Does there exist $n$ with $n = a^2b^3$, $n+1=c^2d^3$, $n+2=e^2f^3$,
> $b,d,f$ squarefree and pairwise coprime, $b\equiv3\pmod4$, $f\equiv1\pmod4$?

The obstacle: the squarefree parameters $b,d,f$ range over infinitely many values
with no a priori bound, so "solve for fixed $(b,d,f)$" reduces to finitely many
points on a curve (Siegel) but gives no control on the parameters. The $abc$ route
captures exactly the small-radical information and yields finiteness; the gap
between *finitely many* and *none* is the whole problem.

Ingredients we could not find, each of which would be progress:

* an unconditional radical lower bound strong enough to replace $abc$;
* a descent on $dU^2-bV^2=1$, $fW^2-dU^2=1$ that shrinks the triple. Note such a
  descent cannot operate on a single *pair*: every consecutive powerful pair lies
  in the infinite closure $(u,u+1)\mapsto (4u(u+1),(2u+1)^2)$, so no descent can
  terminate for pairs;
* any a priori bound on the possible squarefree parameters $b,d,f$.