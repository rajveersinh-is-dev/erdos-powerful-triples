# Reproducing every result in this repository

Everything reported in `README.md`, `research/*.md` and `paper/main.tex` can be
regenerated with the commands below. All numbers in those documents were produced
by the code here; nothing is quoted from memory.

---

## 0. Environment

| Component | Version used |
| --- | --- |
| Python | 3.14.6 (Windows) |
| numpy | 2.4.6 |
| sympy | 1.14.0 |
| z3-solver | 5.0.0 |
| PARI/GP, SageMath | **not available** (this is why one claim is marked "not re-verified") |

```powershell
python -m pip install "numpy>=1.24" "sympy>=1.12" "z3-solver>=4.12"
```

The library itself has **no** required dependencies; `numpy`, `sympy` and `z3` are
needed only for the experiments.

**No environment variable is needed.** Every script bootstraps `sys.path` itself
(`tests/crossvalidate_generators.py` and the four experiment scripts insert
`<repo>/src`), and experiment output is written to `<repo>/results/` regardless of the
working directory you invoke them from. The commands below are shown from the
repository root for convenience only.

```powershell
git clone https://github.com/rajveersinh-is-dev/erdos-powerful-triples.git
cd erdos-powerful-triples
```

---

## 1. Test suite (35 tests)

```powershell
python tests\test_powerful_triples.py
```

Expected final line:

```
35/35 tests passed
```

With `pytest`:

```powershell
python -m pytest tests -q
```

The test suite covers: three independent powerfulness predicates agreeing with full
factorisation; the canonical $a^2b^3$ decomposition; the two generators agreeing
with brute force; the local-admissibility counts; the mod-36 constraint; the
closure lemma; the regression pairs from OEIS A076445 / A060355; the Mordell point
lists used in the literature; and a regression test pinning the middle-term bug
described in `research/falsification_log.md` §F1.

---

## 2. Cross-validation of the two powerful-number generators

```powershell
python tests\crossvalidate_generators.py 3000000
```

Expected output:

```
limit=3000000: |odd powerful|=1338 ... |P1|=1024 |P3|=314 closed-form-count=1338
CROSS-VALIDATION: PASS
```

This compares a pure-Python generator, a numpy-vectorised generator, and a
closed-form counting function, and additionally checks that the residue class of an
odd powerful number agrees with that of its canonical squarefree parameter.

---

## 3. Exhaustive search to $10^{16}$ (main computational result)

```powershell
python experiments\exp01_scale_search.py 1e9 1e10 1e11 1e12 1e13 1e14 1e15 1e16
```

Reproduced output (wall-clock times vary by machine):

```
N = 10^9   |P3| =        6,014  |P1| =       19,005  total =       25,019  candidates =   1  TRIPLES = []
N = 10^10  |P3| =       19,196  |P1| =       60,291  total =       79,487  candidates =   1  TRIPLES = []
N = 10^11  |P3| =       61,102  |P1| =      191,061  total =      252,163  candidates =   1  TRIPLES = []
N = 10^12  |P3| =      194,090  |P1| =      605,048  total =      799,138  candidates =   1  TRIPLES = []
N = 10^13  |P3| =      615,589  |P1| =    1,915,166  total =    2,530,755  candidates =   1  TRIPLES = []
N = 10^14  |P3| =    1,950,636  |P1| =    6,060,286  total =    8,010,922  candidates =   2  TRIPLES = []
N = 10^15  |P3| =    6,177,077  |P1| =   19,172,862  total =   25,349,939  candidates =   2  TRIPLES = []
N = 10^16  |P3| =   19,552,057  |P1| =   60,648,440  total =   80,200,497  candidates =   2  TRIPLES = []
```

* Method: complete within the stated bound, by Theorem 3.1 of the paper (a triple
  forces $n\equiv3\bmod4$, and for odd powerful $m=a^2b^3$ one has $m\equiv b\bmod4$).
* `candidates` = integers $n$ with $n$ **and** $n+2$ powerful but not checked for the
  middle term. At $10^{14}$ and above these are $130576327$ and $13837575261123$ — the
  3rd and 5th terms of OEIS A076445 — and in both cases $n+1$ is **not** powerful.
* Raw output with checksums: `results/scale_search.json`.

---

## 4. Three-term arithmetic progressions and the parity strategy

```powershell
python experiments\exp02_aps_parity.py
```

Key output: 115 three-term APs of powerful numbers with $N\le2\cdot10^5$, $d\le600$;
**14 with odd common difference**, the smallest being $d=49$ at $N=343$; minimum $d$
found is $24$, confirming $d_3\le24$ (the pair $(1,25,49)$).

```powershell
python experiments\exp03_ap_parity_and_powers2.py
```

Key output:

```
   343 = 7^3          powerful=True
   392 = 2^3*7^2      powerful=True
   441 = 3^2*7^2      powerful=True
   -> VALID COUNTEREXAMPLE to 'd_3 is even': True  (d = 49 is odd)
...
All 3-term APs of powerful numbers with ODD d < 49 and N <= 10000000000:
   NONE
Fermat identity  prod_{j<m} F_j = 2^(2^m)-1  for m=1..12 : True
Fermat numbers pairwise coprime (j <= 15)                : True
2^k-1 powerful for k in 2..250    : []   (expected [])
PART B verdict: PASS
```

Note: this run takes about 10 minutes, almost all of it in exact factorisation of
$2^k-1$ for $k$ up to 250.

---

## 5. Independent cross-checks of the literature

```powershell
python experiments\exp04_literature_checks.py
```

Reproduced output (abridged):

```
triple-admissible classes mod 36    : [7, 27, 35]
Beckon's constraint reproduced: True
count mod 900    = 39     (claimed 39) match=True
count mod 44100  = 1209   (claimed 1209) match=True
   L=   11  density=0.247414   density*(log L)^3 = 3.4113
   L=  101  density=0.0466774  density*(log L)^3 = 4.5883
   L= 1009  density=0.0146115  density*(log L)^3 = 4.8350
   L= 1999  density=0.0110406  density*(log L)^3 = 4.8473
  (8, 9) -> (288, 289)   B-A = 1   both powerful: True
  x <= 20000 : BOTH x^3-1 and x^3+1 powerful     : []
  cube-centred candidate triples for x <= 200000 : []  (9.5s)
  4A^3 + 27B^2 = -531441 = 3^12
  => E(Q)_tors = { O }  (Nagel-Lutz, certified by exhaustive check) : True
  NOTE: the RANK of E is a separate input; it is NOT verified here.
  k=2 ... k=-162  claimed lists confirmed for |x|<=2000000
  recurrence cross-check agrees at every tested index: True
  cubes z_k = t^3 found for k <= 2000 : [(1, 1, 1)]
  largest |z_k| examined has 2287 decimal digits
```

Raw output: `results/exp04_literature_checks.json`.

---

## 6. The five independent search methods (small bounds)

```powershell
python -c "import sys; sys.path.insert(0,'src'); import powerful_triples as pt; [print(f().as_dict()) for f in (lambda: pt.search_direct(200000), lambda: pt.search_generated(200000), lambda: pt.search_parameters(60,60,4000,4000), lambda: pt.search_modular(200000,36), lambda: pt.search_smt(40,12))]"
```

Reproduced output (abridged):

```
A:direct-enumeration      found=[]  checked=200000                       0.41 s
B:generate-and-scan      found=[]  886 powerful numbers generated       0.01 s
C:squarefree-parameters  found=[]  b,d <= 60, V,W <= 4000               1.96 s
D:modular-screen(M=36)   found=[]  survivor fraction 3/36 = 0.0833333    0.06 s
E:smt(z3)                found=[]  z3 status: unsat -- no solution in the stated box
                                (a,c,e <= 40; b,d,f <= 12)              9.61 s
```

All five agree: no triple below $2\cdot10^5$.

Note on Method E: the solver is given the *proved necessary* conditions
$b\equiv3\pmod4$, $b$ odd, $f\equiv1\pmod4$, $f$ odd (Theorem 3.1/3.2 of the paper).
Imposing necessary conditions only shrinks the searched set, so `unsat` remains a
valid negative answer for that box. On larger boxes z3 answers `unknown` — degree-5
nonlinear integer arithmetic is hard — and the code reports `unknown` explicitly
rather than dressing it up as a proof.

---

## 7. Known limitation, stated explicitly

There is **no LaTeX toolchain** in this environment, so `paper/main.tex` was checked
only by static analysis (balanced braces, matched `\begin`/`\end` environments,
single `\documentclass`/`\end{document}` pair) and not compiled. The numerical claims
inside the paper were each re-checked by the code above.

There is also **no PARI/GP or SageMath**, so the rank-0 computation underlying
Sayim's Theorem 2 was not re-verified; only its torsion part was certified here.