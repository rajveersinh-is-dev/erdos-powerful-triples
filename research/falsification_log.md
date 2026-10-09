# Falsification log

Every lemma, conjecture and "obvious" claim proposed during this investigation was
first attacked with a counterexample search. This file records each attempt, the
obstruction found, why the original reasoning failed, whether the statement can be
repaired, and what remains useful.

Format: **F<n> — claim tested** / **obstruction** / **why the reasoning failed** /
**repair** / **residue**.

---

## F1 — "the intersection test finds triples" (MY OWN BUG, caught by falsification)

**Claim tested (implicit in the first version of `scale.search_triples_fast`).**
"Generate the two forced residue classes $P_3=\{m\text{ powerful}: m\equiv3\bmod4\}$
and $P_1=\{m\text{ powerful}: m\equiv1\bmod4\}$; a triple exists iff
$P_3\cap(P_1-2)\ne\emptyset$."

**Obstruction.** The first run reported
`triples=[130576327, 13837575261123]`, i.e. it claimed two counterexamples to
Erdős–Mollin–Walsh, at $N=10^{10}$.

**Why the reasoning failed.** $n+1$ is **even**, so it is neither in $P_1$ nor in
$P_3$. Membership in $P_3$ certifies that $n$ is powerful, and membership of $n+2$
in $P_1$ certifies that $n+2$ is powerful — but nothing certifies the **middle
term**. The intersection detects *pairs at distance 2*, which is exactly OEIS
A076445, not triples. Indeed $130576327$ and $13837575261123$ are the 3rd and 5th
terms of A076445, and $130576328$ is not powerful.

**Repair.** `scale.search_triples_fast` now applies `is_powerful(n+1)` to every
intersection element. Regression test
`tests/test_powerful_triples.py::test_fast_triple_search_rejects_the_A076445_pairs`
pins this: the candidate $130576327$ still exists as a distance-2 pair, yet the
search reports no triple. All reported table entries were regenerated after the fix.

**Residue.** The structural insight (split by $n\bmod4$, which makes the search
$O(\sqrt X)$ instead of $O(X)$) is intact and is what makes $10^{16}$ reachable.

---

## F2 — "$d_3$ is even, so EMW follows" (FALSE, with an explicit counterexample)

**Claim tested.** Since EMW is equivalent to $d_3>1$ (BBC §7), it would suffice to
show that every 3-term arithmetic progression of powerful numbers has *even* common
difference; then $d_3\ge2$.

**Obstruction.**
$$343=7^3,\qquad 392=2^3\cdot7^2,\qquad 441=3^2\cdot7^2,$$
an arithmetic progression with common difference $d=49$, which is **odd**.
A second example: $(169,256,343)=(13^2,2^8,7^3)$ with $d=87$.

**Why the reasoning failed.** The mod-4 argument that forces $n\equiv3\pmod4$
relies on $d=1$, i.e. on the three terms being *consecutive*. For general odd $d$
the only forced statement is Theorem 2.5 ($N$ odd, $4\mid N+d$), and that is
satisfiable — indeed $(7,8,9)$ has $N=7$ odd and $8\equiv0\bmod4$, and
$49\cdot(7,8,9)=(343,392,441)$ is powerful because the extra factor $7$ lifts
$v_7$ from 1 to 3 in $7\cdot49$, while $49$ already supplies $v_7\ge2$ for the
other two terms.

**Repair.** None possible — the statement is false. What survives is Theorem 2.5,
which is the correct general necessary condition and is proved.

**Search for the least odd $d$.** No 3-term AP of powerful numbers with odd
$d<49$ has $N\le10^{10}$ (COMPUTATIONALLY VERIFIED; 214 122 powerful numbers
scanned, 0.79 s). This sharpens the picture but does not help the $d=1$ case.

**Residue.** EMW $\iff d_3>1$ remains valid; only the parity route is closed.

---

## F3 — "quadruples are killed by mod 4, so triples are too" (FALSE, and the failure is instructive)

**Claim tested.** "A powerful number is never $2\bmod4$; hence four consecutive
powerful numbers are impossible; the same idea should handle three."

**Obstruction.** It handles length 4 but not length 3.

**Why the reasoning failed.** Among $n,n+1,n+2$ with $n\not\equiv3\pmod4$ one term
is $2\bmod4$, so $n\equiv3\pmod4$ is *necessary* — but $n\equiv3\pmod4$ is
*achievable*. The length-4 argument works because the four residues $0,1,2,3$
mod 4 are all hit, forcing a $2\bmod4$ term; three consecutive residues can avoid 2.

**Repair.** The correct statement, Theorem 2.4(1): $n\equiv3\bmod4$. Proved.

**Residue.** A caution about extrapolating from the quadruple case — the most
common error in discussions of this problem.

---

## F4 — "quadratic reciprocity between the squarefree parameters gives a contradiction" (INCONSISTENT, not contradictory)

**Claim tested.** From $c^2d^3-a^2b^3=1$ and $e^2f^3-c^2d^3=1$, reduce modulo
$q\mid b$, $q\mid d$, $q\mid f$ to extract Legendre-symbol conditions and hope for
a cycle of incompatible signs.

**Obstruction.** The extracted conditions are
$$(d/b)=1,\quad (b/d)=(-1/d),\quad (f/d)=1,\quad (d/f)=(-1/f),\quad (f/b)=(2/b),\quad (b/f)=(-2/f),$$
and they are **mutually consistent**. Writing $\varepsilon(s)=(-1)^{(s-1)/2}$ and
$\chi_2(s)=(2/s)$, reciprocity reduces them to
$1\cdot\varepsilon(d)=\varepsilon(d)\varepsilon(b)$, $\varepsilon(f)=1\Rightarrow f\equiv1\bmod4$, and
$\chi_2(b)\chi_2(f)=1$ — which hold exactly because we already proved
$b\equiv3\bmod4$ and $f\equiv1\bmod4$. The $2$-adic cases ($b\equiv3$ or $7\bmod8$
paired with $f\equiv5$ or $1\bmod8$) satisfy $\chi_2(b)\chi_2(f)=1$ in every case.

**Why the reasoning failed.** Reciprocity closes on itself: the conditions derived
from a *hypothetical* solution must be consistent, because they are necessary
conditions of solutions that may exist. Necessary conditions can only help if they
are *strictly stronger* than what is already known, and here they are equivalent to
Theorem 2.4(2).

**Repair.** None needed; recorded so the approach is not repeated. Legendre-symbol
machinery at prime level gives nothing beyond the mod-8/16 information.

**Residue.** Suggestive for *higher*-power reciprocity (cubic symbols), which was
not developed.

---

## F5 — "$abc$ proves EMW" (FALSE as an inference)

**Claim tested.** "The $abc$ conjecture implies there are only finitely many triples;
hence $abc$ implies EMW."

**Obstruction.** "Finitely many" $\not\Rightarrow$ "none". The set of triples could
be a non-empty finite set.

**Why the reasoning failed.** Conflating a finiteness statement with an emptiness
statement. EMW is an *existence* statement ($\exists n:\ \dots$ is false).

**Repair.** Precise formulation, proved: $abc(\epsilon)$ for $0<\epsilon<1/3$
implies finiteness, via $(n+1)^2=n(n+2)+1$ and $\operatorname{rad}(m)\le\sqrt m$.
To reach EMW one would additionally need an explicit $abc$ constant (so the bound
is searchable) or an unconditional exclusion of the finitely many survivors.

**Residue.** The sharp exponent $\epsilon<1/3$ is derived in the paper; the
"finiteness $\ne$ nonexistence" point is emphasised throughout.

---

## F6 — "purely local congruences can exclude the triple" (PROVED IMPOSSIBLE)

**Claim tested.** There should be a modulus $M$ such that every residue class
mod $M$ is excluded by the requirement "each of $n,n+1,n+2$ is powerful at every
prime $p$ with $p^2\mid M$".

**Obstruction.** Theorem 2.2: for every $M\ge1$ the triple-admissible set is
non-empty. In particular the sieve never empties; it only thins, at rate
$\asymp(\log L)^{-3}$.

**Why any congruence-only proof must fail.** Such a proof would have to show that
every $n$ in some residue class fails; but a congruence argument only ever sees
$n\bmod M$, and there is always a class in which all local conditions hold. Note
this is *not* the statement that a powerful triple exists — only that local
conditions cannot rule it out.

**Residue.** This is a positive structural result: it certifies that a global
argument is required, and it rules out an entire family of approaches.

---

## F7 — "$2^k-1$ is never powerful" (UNPROVED in general; partial result only)

**Claim tested.** Since $3\mid 2^k-1$ iff $k$ even, and $7 \mid 2^k-1$ iff $3\mid k$,
one might hope to bootstrap: powerfulness forces $3\mid k$, then $7\mid k$, then
$127\mid k$, $337\mid k$, ... and the chain diverges.

**Obstruction.** The bootstrap stalls. From $21\mid k$ we get
$7^2\cdot127\cdot337\mid 2^k-1$, so $127\mid k$ (127 is not Wieferich) and $337\mid k$
if 337 is not Wieferich. But $337$ can be avoided only if it is Wieferich, and the
complete list of Wieferich primes base 2 is unknown. More generally, for a prime $p$
with $\operatorname{ord}_p(2)=d$, the condition $p^2\mid 2^k-1$ is satisfied
whenever $\operatorname{ord}_{p^2}(2)\mid k$, which happens either if $p\mid k$ or
if $p$ is Wieferich.

**Repair.** Two partial results survive:
* **Theorem 2.6** — $2^{2^m}-1$ is never powerful (Fermat numbers are pairwise
  coprime, so no bootstrap is needed). This is unconditional and covers an infinite
  family.
* **Proposition 2.7** — the complete necessary condition "$p\mid k$ or $p$ Wieferich",
  plus the conditional consequence $\omega(k)\le2$.

**COMPUTATIONALLY VERIFIED:** $2^k-1$ is not powerful for every $k$ in $2\le k\le250$
(full factorisation of each $2^k-1$), and $2^{2^m}-1$ is not powerful for
$1\le m\le7$.

**Residue.** An unconditional proof for all $k$ would need control of Wieferich
primes; we see no route.

---

## F8 — "the cube-centred reduction $t^6+t^3+1=3w^2$ can be finished elementarily" (PARTIAL)

**Claim tested.** Sayim's Theorem 2 reduces the mixed-shape cases to
$t^6+t^3+1=3w^2$, proved via a rank-0 elliptic quotient. We attempted an independent
elementary (Eisenstein-integer) descent.

**Work done.** Put $x=t^3$, so $x^2+x+1=3w^2$. Then $v_3(x^2+x+1)=1$ (by LTE, since
$x\equiv1\bmod3$ is forced), hence $3\nmid w$. In $\mathbb Z[\omega]$, with
$\omega^2+\omega+1=0$:
* $(x-\omega)$ and $(x-\omega^2)$ each carry exactly one factor of $(1-\omega)$;
* therefore $\alpha := (x-\omega)/(1-\omega) = \frac{2x+1}{3}+\frac{x-1}{3}\omega$ satisfies
  $\alpha\bar\alpha = w^2$ with $\gcd(\alpha,\bar\alpha)=1$ (indeed
  $\alpha-\bar\alpha = -(x-1)/(1-\omega)$ is a unit);
* hence $\alpha = \varepsilon\gamma^2$ with $\varepsilon$ a unit and $\gamma\in\mathbb Z[\omega]$.

**Obstruction.** Only the unit class $\varepsilon=\pm1$ can be finished.
Modulo squares the units give three cases. For $\varepsilon=1$, writing
$\gamma=u+v\omega$ and comparing the two coefficients of $\alpha$ yields
$u^2-4uv=1$, i.e. $u=\pm1$, $v=0$, hence $t=1$.
The classes $\varepsilon=\omega$ and $\omega^2$ reduce to
$(v+u)^2-3u^2=1$ together with $t^3 = 3s(s-2u)-2$ where $s=(v+u)$ — a genuine
Pell-type cube condition that we could not resolve. Since Sayim's relevant branch
has $t<0$, the unresolved cases are exactly the operative ones.

**Why it matters.** We therefore **cannot** independently certify Sayim's Theorem 2.
We did certify its *torsion* input (Nagell–Lutz: $E:y^2=x^3-81x+243$ has trivial
torsion, checked exhaustively) and its *arithmetic* input (the five Mordell integral
point lists, and the Pell recurrence $z_{k+1}=14z_k-z_{k-1}+6$, cross-checked
against the closed form at 8 consecutive indices). The **rank-0** claim — the single
non-elementary input — we did not re-verify: no PARI/GP or SageMath is available in
this environment (`gp` on this machine is the PowerShell alias
`Get-ItemProperty`). It is corroborated by the LMFDB record for Cremona 1296f2 /
LMFDB 1296.k1 (rank 0, analytic rank 0, trivial torsion, 0 integral points),
independently fetched.

**Residue.** An honest, reproducible statement of exactly how far we got. The
partial descent is recorded here rather than claimed as a proof.

---

## F9 — "a Pell-equation parametrisation of a pair parametrizes the triple" (FALSE in general)

**Claim tested.** Erdős asked (Erdős Problems #365) whether every consecutive
powerful pair comes from a Pell equation, i.e. whether one of the two terms is a
square. If so, a triple would have one square among its terms and could be attacked
via Pell recurrences.

**Obstruction.** **Golomb (1970):** $12167=23^3$ and $12168=2^3 3^2 13^2$ are both
powerful and **neither is a square**. Walker (1976) proved $7^3x^2=3^3y^2+1$ has
infinitely many solutions, giving infinitely many such pairs. We reproduce the
phenomenon in our own data: $(465124,465125)=(682^2,5^3\cdot61^2)$ — here $682^2$
*is* a square, coming from the negative Pell equation $x^2-125y^2=-1$ (from
$x^2-5y^2=-1$ at $y=305$, which is $5\cdot61$).

**Why the reasoning failed.** The pair structure is genuinely two-parameter; the
"one of them is a square" heuristic is simply false.

**Residue.** Any Pell-based attack must justify why it covers *all* pairs, and it
does not. This is why we do not pursue a Pell-recurrence attack for the triple.

---

## F10 — "a descent on a consecutive powerful pair can terminate" (FALSE)

**Claim tested.** Infinite descent: from a hypothetical triple, produce a smaller
one.

**Obstruction.** The closure $(u,u+1)\mapsto(4u(u+1),(2u+1)^2)$ produces a *new*
consecutive powerful pair from any old one, so the set of pairs is closed upwards
and no descent on a pair can terminate. (Verified numerically: $(8,9)\to(288,289)
\to(332928,332929)\to\cdots$.)

**Residue.** Descent, if it exists, must use the *triple* structure, not the pair.
No such descent is found.

---

## F11 — smaller/factual errors caught during the investigation

1. **Off-by-one display label** in the first scale-search script: the printed
   bound was one decade larger than the bound actually searched. Fixed; the
   regenerated `results/scale_search.json` reports `"N"` explicitly.
2. **Fabricated regression value.** The test file initially asserted that
   $(423132,423133)$ is a pair of consecutive powerful numbers. It is not:
   $423132 = 2^2\cdot3\cdot37\cdot953$. Replaced by the computer-verified list
   $(8,9),(288,289),(675,676),(9800,9801),(12167,12168),(235224,235225),
   (332928,332929),(465124,465125)$.
3. **A wrong test assertion** conflated "$\{n,n+2\}$ powerful" with
   "$n,n+1,n+2$ powerful": the pair $(25,27)$ has $25\equiv1\bmod4$ and is perfectly
   legal — it simply is not the start of a triple. The test was rewritten to check
   the structural content that is actually non-vacuous.
4. **Indexing bug** in the cross-check of Sayim's recurrence: the orbit enumerates
   the *odd* powers of $2+\sqrt3$, so recurrence index $j$ corresponds to power
   $2j-1$; the first version compared index $j$ with power $j$. After the fix all
   eight tested indices agree.
5. **Trial division on huge integers.** Two intermediate scripts called
   `is_powerful` on $2^{2^{24}}$, which is $O(\sqrt{n})$ and hangs forever. Replaced
   by structural checks (Fermat identity + pairwise coprimality) and by exact
   `factorint` where the numbers are small enough.

---

## Summary: what is *not* left in any proof

The final proof in `paper/main.tex` contains only statements labelled **PROVED**,
each with a complete argument. The following were tried and rejected and appear
**nowhere** in the proof: the "middle term is excluded by mod 4" fallacy for
length 3 (F3); Legendre-symbol reciprocity (F4); the parity-of-$d_3$ route (F2);
a $abc$-implies-EMW inference (F5); the assumption that a Pell family covers all
pairs (F9); descent on pairs (F10); and the unpatched triple-search code (F1).