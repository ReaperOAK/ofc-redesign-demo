#!/usr/bin/env python3
"""Verify design token contrast ratios against WCAG 2.x.

Exits 1 if any pair fails its required level. Run after any token change.
"""
import sys


def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# (foreground, background, required_ratio, label)
PAIRS = [
    ("#A16207", "#FAFAF9", 4.5, "accent on light surface"),
    ("#F59E0B", "#1C1917", 4.5, "accent on dark surface"),
    ("#0C0A09", "#F59E0B", 4.5, "text on amber button"),
    ("#0C0A09", "#FAFAF9", 4.5, "body on light surface"),
    ("#FAFAF9", "#1C1917", 4.5, "body on dark surface"),
    # Interactive boundaries (form inputs) are UI components under WCAG 1.4.11
    # and require 3:1. Decorative dividers are exempt and are NOT listed here.
    ("#78716C", "#FAFAF9", 3.0, "interactive border on light surface"),
]

# Pairs that MUST NOT be used together, reported so anyone reaching for the
# wrong accent on a dark background sees why it is forbidden.
FORBIDDEN = [
    ("#A16207", "#1C1917", "amber-700 on dark — use #F59E0B"),
    ("#D6D3D1", "#FAFAF9", "decorative border on a form control — use #78716C"),
]

failed = False

for fg, bg, required, label in PAIRS:
    r = ratio(fg, bg)
    ok = r >= required
    if not ok:
        failed = True
    print(f"{'PASS' if ok else 'FAIL'}  {r:6.2f}:1  (needs {required}:1)  {label}")

for fg, bg, why in FORBIDDEN:
    r = ratio(fg, bg)
    print(f"NOTE  {r:6.2f}:1  forbidden pairing — {why}")

if failed:
    print("\nContrast gate FAILED", file=sys.stderr)
    sys.exit(1)

print("\nContrast gate passed")
