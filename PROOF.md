# Exact finite certificate for the Belgian Chocolate problem

**Maintainer:** Bruno L Yamamoto

**Status:** checkable by exact computation; not peer reviewed.

This controller was found by GPT Astra Pro. The claim can be checked by running the exact-arithmetic checker below. It has not been reviewed by a human expert, and better bounds may already be known.

## 1. Problem and claim

For $0<\delta<1$, define

$$
a_\delta(s)=s^2-2\delta s+1, \qquad b(s)=s^2-1.
$$

A value $\delta$ is admissible if there exist stable real polynomials $x$ and $y$, with $\deg y\leq\deg x$, for which

$$
z(s)=a_\delta(s)x(s)+b(s)y(s)
$$

is also stable. Here *stable* means that every zero lies in the open left half-plane.

The repository stores an exact rational value $\delta_0$ and exact rational polynomials $x,y,z$ satisfying these conditions. In particular,

$$
\delta_0>0.98272779.
$$

Therefore the critical Belgian Chocolate parameter satisfies

$$
\boxed{\delta_*>0.98272779}.
$$

## 2. Exact stored object

The file `controller/controller.json` is the certificate. Coefficients are listed in ascending powers of $s$.

The stored degrees are

$$
\deg x=34, \qquad \deg y=34, \qquad \deg z=36.
$$

The exact rational $\delta_0=p/q$ is stored by its numerator and denominator. Its decimal expansion begins

```text
0.982727799178651584209532065539568007233113091155...
```

The files do not require floating-point root calculations to establish the claim.

## 3. Exact polynomial identity

With $\delta_0=p/q$, the required identity is

$$
z=(s^2-2\delta_0 s+1)x+(s^2-1)y.
$$

The checker multiplies this identity by $q$ and verifies coefficient-by-coefficient that

$$
qz=(q-2ps+qs^2)x+(-q+qs^2)y.
$$

All arithmetic in this step is integer arithmetic.

## 4. Exact Hurwitz verification

For each of $x$, $y$, and $qz$, the checker constructs the Routh table using exact `fractions.Fraction` arithmetic.

For a real polynomial with positive leading coefficient and no singular Routh case, strict positivity of every entry in the first column of the Routh table is equivalent to all roots lying strictly in the open left half-plane. The checker requires every first-column entry to be strictly positive and rejects a zero pivot or zero row.

For the stored object it verifies:

- 35 positive exact Routh first-column entries for $x$;
- 35 positive exact Routh first-column entries for $y$;
- 37 positive exact Routh first-column entries for $qz$.

Multiplication by the positive scalar $q$ does not change the roots of $z$, so this proves strict Hurwitz stability of $z$ as well.

## 5. Degree and lower-bound checks

The checker also verifies

$$
\deg y\leq\deg x
$$

and compares the exact rational $\delta_0$ with $98272779/10^8$, establishing

$$
\delta_0>0.98272779.
$$

Thus the stored finite object is an admissible controller at a parameter strictly above the advertised decimal lower bound.

## 6. Reproduction

From the repository root, run

```sh
python checker/check_controller.py
```

A successful run ends with

```text
ALL EXACT CHECKS PASSED
```

The acceptance calculation uses no third-party Python packages.

## 7. Certification boundary

This repository certifies only the explicit finite controller stored in `controller/controller.json` and the consequent lower bound $\delta_*>0.98272779$.

It does not certify optimality, a matching upper bound, or literature priority. It also does not rely on any stronger analytic or numerical construction not included in this repository.
