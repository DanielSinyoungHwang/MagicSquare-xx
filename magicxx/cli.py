"""verify Command — 격자 입력 → 10개 조건 pass/fail."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from magicxx.verify import format_failures, validate_grid_structure, verify_grid

_TOKEN_RE = re.compile(r"-?\d+")


def parse_grid_text(text: str) -> list[list[int]]:
    tokens = [int(m.group()) for m in _TOKEN_RE.finditer(text)]
    if len(tokens) != 16:
        raise ValueError(f"expected 16 integers, got {len(tokens)}")
    return [tokens[i * 4 : (i + 1) * 4] for i in range(4)]


def read_grid(source: str | None) -> list[list[int]]:
    if source and source != "-":
        text = Path(source).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    return parse_grid_text(text)


def run_verify(source: str | None = None) -> int:
    try:
        grid = read_grid(source)
    except (OSError, ValueError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2

    structure_errors = validate_grid_structure(grid)
    if structure_errors and structure_errors == ["grid must be 4×4"]:
        print(f"ERROR {structure_errors[0]}", file=sys.stderr)
        return 2

    result = verify_grid(grid)
    if not result.grid_valid:
        for err in result.errors:
            print(f"FAIL {err}")
        return 1

    if result.ok:
        print("OK")
        return 0

    for line in format_failures(result):
        print(line)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="magicxx verify")
    parser.add_argument(
        "source",
        nargs="?",
        default="-",
        help="grid file path, or omit / '-' for stdin",
    )
    args = parser.parse_args(argv)
    return run_verify(args.source)
