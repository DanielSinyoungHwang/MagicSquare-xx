"""격자 검증 Skill — verify_grid API."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from magicxx.rules import (
    BLANK,
    CONDITION_NAMES,
    GRID_SIZE,
    MAGIC_SUM,
    MAX_BLANKS,
    MAX_VALUE,
    MIN_VALUE,
)


class ConditionStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    INCOMPLETE = "incomplete"


@dataclass(frozen=True)
class ConditionResult:
    name: str
    status: ConditionStatus
    actual_sum: int | None
    expected_sum: int = MAGIC_SUM


@dataclass(frozen=True)
class VerifyResult:
    grid_valid: bool
    ok: bool
    conditions: tuple[ConditionResult, ...]
    errors: tuple[str, ...]


def _line_cells(grid: Sequence[Sequence[int]], name: str) -> list[int]:
    if name.startswith("row_"):
        return list(grid[int(name.split("_")[1])])
    if name.startswith("col_"):
        col = int(name.split("_")[1])
        return [grid[r][col] for r in range(GRID_SIZE)]
    if name == "main_diagonal":
        return [grid[i][i] for i in range(GRID_SIZE)]
    if name == "anti_diagonal":
        return [grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)]
    raise ValueError(f"unknown condition: {name}")


def validate_grid_structure(grid: Sequence[Sequence[int]]) -> list[str]:
    errors: list[str] = []
    if len(grid) != GRID_SIZE or any(len(row) != GRID_SIZE for row in grid):
        errors.append("grid must be 4×4")
        return errors

    blanks = 0
    seen: dict[int, int] = {}
    for row in grid:
        for value in row:
            if value == BLANK:
                blanks += 1
                continue
            if value < MIN_VALUE or value > MAX_VALUE:
                errors.append(f"value {value} out of range {MIN_VALUE}..{MAX_VALUE}")
            seen[value] = seen.get(value, 0) + 1

    if blanks > MAX_BLANKS:
        errors.append(f"too many blanks: {blanks} (max {MAX_BLANKS})")

    duplicates = [v for v, count in seen.items() if count > 1]
    if duplicates:
        dup = ", ".join(str(v) for v in sorted(duplicates))
        errors.append(f"duplicate values: {dup}")

    return errors


def _evaluate_condition(grid: Sequence[Sequence[int]], name: str) -> ConditionResult:
    cells = _line_cells(grid, name)
    if BLANK in cells:
        return ConditionResult(name=name, status=ConditionStatus.INCOMPLETE, actual_sum=None)
    total = sum(cells)
    if total == MAGIC_SUM:
        return ConditionResult(name=name, status=ConditionStatus.PASS, actual_sum=total)
    return ConditionResult(
        name=name,
        status=ConditionStatus.FAIL,
        actual_sum=total,
        expected_sum=MAGIC_SUM,
    )


def verify_grid(grid: Sequence[Sequence[int]]) -> VerifyResult:
    errors = validate_grid_structure(grid)
    if errors:
        return VerifyResult(grid_valid=False, ok=False, conditions=(), errors=tuple(errors))

    conditions = tuple(_evaluate_condition(grid, name) for name in CONDITION_NAMES)

    has_fail = any(c.status == ConditionStatus.FAIL for c in conditions)
    has_incomplete = any(c.status == ConditionStatus.INCOMPLETE for c in conditions)
    ok = not has_fail and not has_incomplete
    return VerifyResult(grid_valid=True, ok=ok, conditions=conditions, errors=())


def format_failures(result: VerifyResult) -> list[str]:
    lines: list[str] = []
    for c in result.conditions:
        if c.status == ConditionStatus.FAIL:
            lines.append(f"FAIL {c.name} sum={c.actual_sum} expected={c.expected_sum}")
    return lines
