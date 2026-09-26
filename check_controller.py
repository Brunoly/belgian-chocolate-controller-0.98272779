#!/usr/bin/env python3
"""Exact verifier for the rational Belgian Chocolate controller.

No third-party packages are used. All arithmetic affecting acceptance is
integer or fractions.Fraction arithmetic.
"""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Iterable

sys.set_int_max_str_digits(1_000_000)


def trim(p: list[int]) -> list[int]:
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def poly_add(a: Iterable[int], b: Iterable[int]) -> list[int]:
    aa, bb = list(a), list(b)
    out = [0] * max(len(aa), len(bb))
    for i, value in enumerate(aa):
        out[i] += value
    for i, value in enumerate(bb):
        out[i] += value
    return trim(out)


def poly_mul(a: Iterable[int], b: Iterable[int]) -> list[int]:
    aa, bb = list(a), list(b)
    out = [0] * (len(aa) + len(bb) - 1)
    for i, x in enumerate(aa):
        for j, y in enumerate(bb):
            out[i + j] += x * y
    return trim(out)


def routh_first_column(coeff_ascending: Iterable[int]) -> list[Fraction]:
    """Return the exact Routh first column.

    Input coefficients are ordered from s^0 upward. The leading coefficient
    is normalized to be positive. A strict Hurwitz polynomial has one
    strictly positive entry for every row.
    """
    polynomial = trim([int(value) for value in coeff_ascending])
    if not polynomial or polynomial[-1] == 0:
        raise ValueError("zero leading coefficient")
    if polynomial[-1] < 0:
        polynomial = [-value for value in polynomial]

    degree = len(polynomial) - 1
    if degree == 0:
        return [Fraction(polynomial[0])]

    columns = degree // 2 + 1
    even_row = [
        Fraction(polynomial[degree - 2 * j]) if degree - 2 * j >= 0 else Fraction(0)
        for j in range(columns)
    ]
    odd_row = [
        Fraction(polynomial[degree - 1 - 2 * j])
        if degree - 1 - 2 * j >= 0
        else Fraction(0)
        for j in range(columns)
    ]
    table = [even_row, odd_row]
    first = [even_row[0], odd_row[0]]

    if even_row[0] <= 0 or odd_row[0] <= 0:
        return first

    for _ in range(2, degree + 1):
        previous = table[-1]
        previous2 = table[-2]
        pivot = previous[0]
        if pivot == 0:
            first.append(Fraction(0))
            return first

        row: list[Fraction] = []
        for j in range(columns):
            upper_next = previous2[j + 1] if j + 1 < columns else Fraction(0)
            lower_next = previous[j + 1] if j + 1 < columns else Fraction(0)
            value = (pivot * upper_next - previous2[0] * lower_next) / pivot
            row.append(value)

        if all(value == 0 for value in row):
            first.append(Fraction(0))
            return first
        table.append(row)
        first.append(row[0])
        if row[0] <= 0:
            return first

    return first


def is_strict_hurwitz(coeff_ascending: Iterable[int]) -> tuple[bool, list[Fraction]]:
    polynomial = trim([int(value) for value in coeff_ascending])
    if len(polynomial) == 1:
        return polynomial[0] != 0, [Fraction(abs(polynomial[0]))]
    first = routh_first_column(polynomial)
    return len(first) == len(polynomial) and all(value > 0 for value in first), first


def load_controller(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("coefficient_order") != "ascending powers of s":
        raise ValueError("unsupported coefficient order")
    return data


def integral_polynomial(obj: dict) -> list[int]:
    denominator = int(obj["common_denominator"])
    if denominator != 1:
        raise ValueError("expected an integral polynomial")
    return [int(value) for value in obj["numerators"]]


def verify(path: Path, verbose: bool = True) -> None:
    data = load_controller(path)
    p = int(data["delta"]["numerator"])
    q = int(data["delta"]["denominator"])
    if not (q > 0 and 0 < p < q):
        raise AssertionError("delta is not in (0,1)")
    delta = Fraction(p, q)

    polynomials = data["polynomials"]
    x = integral_polynomial(polynomials["x"])
    y = integral_polynomial(polynomials["y"])
    z_denominator = int(polynomials["z"]["common_denominator"])
    z_numerator = [int(value) for value in polynomials["z"]["numerators"]]
    if z_denominator != q:
        raise AssertionError("stored z denominator differs from delta denominator")

    if len(y) - 1 > len(x) - 1:
        raise AssertionError("degree condition deg(y) <= deg(x) fails")

    # Multiply the required identity by q:
    # q*z = [q,-2p,q]*x + [-q,0,q]*y.
    expected_z_numerator = poly_add(
        poly_mul([q, -2 * p, q], x),
        poly_mul([-q, 0, q], y),
    )
    if trim(expected_z_numerator) != trim(z_numerator):
        raise AssertionError("exact polynomial identity failed")

    results = {}
    for name, polynomial in (("x", x), ("y", y), ("q*z", z_numerator)):
        passed, first = is_strict_hurwitz(polynomial)
        results[name] = (passed, first)
        if not passed:
            bad_row = next((i for i, value in enumerate(first) if value <= 0), None)
            raise AssertionError(f"{name} is not strict Hurwitz; failed Routh row {bad_row}")

    benchmark = Fraction(98272779, 100000000)
    if not delta > benchmark:
        raise AssertionError("delta does not exceed the advertised short decimal")

    if verbose:
        print("PASS exact identity")
        print(
            f"PASS degree condition: deg x={len(x)-1}, "
            f"deg y={len(y)-1}, deg z={len(z_numerator)-1}"
        )
        for name, (_, first) in results.items():
            max_numerator_bits = max(abs(value.numerator).bit_length() for value in first)
            max_denominator_bits = max(value.denominator.bit_length() for value in first)
            print(
                f"PASS strict Hurwitz {name}: {len(first)} positive exact Routh entries "
                f"(max numerator bits={max_numerator_bits}, "
                f"max denominator bits={max_denominator_bits})"
            )
        print(f"PASS delta = {p}/{q}")
        print("PASS delta > 0.98272779")
        print("ALL EXACT CHECKS PASSED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "controller",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "controller" / "controller.json",
    )
    arguments = parser.parse_args()
    verify(arguments.controller)


if __name__ == "__main__":
    main()
