# Explicit rational certificate for a Belgian Chocolate lower bound

**Not peer reviewed. Not verified by a human expert.**

**Maintainer:** Bruno L Yamamoto

This repository gives an explicit rational controller certificate for the Belgian Chocolate stabilization problem at a parameter strictly larger than

$$
0.98272779.
$$

This controller was found by GPT Astra Pro. The claim can be checked by running the exact-arithmetic checker below. It has not been reviewed by a human expert, and better bounds may already be known.

## Result

Let

$$
a_\delta(s)=s^2-2\delta s+1, \qquad b(s)=s^2-1.
$$

The Belgian Chocolate problem asks for stable real polynomials $x$ and $y$, with $\deg y\leq \deg x$, such that

$$
z=a_\delta x+b y
$$

is also stable.

The exact rational object in `controller/controller.json` has

$$
\deg x=34, \qquad \deg y=34, \qquad \deg z=36,
$$

at the exact rational parameter stored in that file, whose decimal expansion begins

```text
0.982727799178651584209532065539568007233113091155...
```

Thus the finite certificate establishes

$$
\delta_*>0.98272779.
$$

The coefficients are stored in ascending powers of $s$. The polynomials $x$ and $y$ have integer coefficients; $z$ is stored with the same exact denominator as $\delta$.

## Exact verification

Run:

```sh
python checker/check_controller.py
```

Only the Python standard library is required. A successful run ends with:

```text
ALL EXACT CHECKS PASSED
```

The checker verifies, using exact integer and `fractions.Fraction` arithmetic:

1. the stored exact rational value of $\delta$;
2. $\deg y\leq\deg x$;
3. the exact coefficient identity

   $$
   z=(s^2-2\delta s+1)x+(s^2-1)y;
   $$

4. strict Hurwitz stability of $x$, $y$, and $z$ using the exact Routh first-column criterion; and
5. the strict numerical inequality $\delta>0.98272779$.

The mathematical certificate and its verification boundary are explained in [`PROOF.md`](PROOF.md).

## Literature status

A 2018 paper by Zachary Charles and Nigel Boston reported $\delta=0.9808348$ as the largest known value at that time. The certificate here exceeds that published value. This repository does **not** claim that a complete current literature search has established priority, and stronger unpublished or subsequently published constructions may exist.

Reference: Z. Charles and N. Boston, *Exploiting Algebraic Structure in Global Optimization and the Belgian Chocolate Problem*, Journal of Global Optimization 72 (2018), 241–254, DOI: 10.1007/s10898-018-0659-5.

## Review status

The exact checker is intended to make the finite claim independently reproducible, but the repository **has not yet undergone independent peer review or formal external verification**. Corrections, if needed, should be made transparently through later commits and releases.

## Repository contents

- `PROOF.md` — concise statement of the finite certificate and why the checks imply the lower bound.
- `controller/controller.json` — exact rational parameter and polynomial coefficients.
- `checker/check_controller.py` — dependency-free exact verifier.
