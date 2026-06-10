"""MagicSquare_xx verify — Test Loop (S3 회귀 우선)."""

import pytest

from magicxx.verify import (
    MAGIC_SUM,
    ConditionStatus,
    verify_grid,
    format_failures,
)

# 완성 마방진 (빈칸 없음)
COMPLETE_MAGIC = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# S3 — 행·열 OK, 주대각선 NG (Mom Test Must Fix)
ROWS_COLS_OK_MAIN_DIAG_NG = [
    [13, 3, 2, 16],
    [8, 10, 11, 5],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


class TestCompleteMagicSquare:
    def test_ok_all_ten_conditions(self):
        result = verify_grid(COMPLETE_MAGIC)
        assert result.grid_valid
        assert result.ok
        assert len(result.conditions) == 10
        assert all(c.status == ConditionStatus.PASS for c in result.conditions)


class TestS3RowsColsOkMainDiagonalNg:
    """Mom Test S3 — 행·열 OK 착각 후 주대각선 검증에서 발견."""

    def test_not_ok(self):
        result = verify_grid(ROWS_COLS_OK_MAIN_DIAG_NG)
        assert result.grid_valid
        assert not result.ok

    def test_main_diagonal_fail_with_details(self):
        result = verify_grid(ROWS_COLS_OK_MAIN_DIAG_NG)
        md = next(c for c in result.conditions if c.name == "main_diagonal")
        assert md.status == ConditionStatus.FAIL
        assert md.actual_sum == 31
        assert md.expected_sum == MAGIC_SUM

    def test_rows_and_cols_pass(self):
        result = verify_grid(ROWS_COLS_OK_MAIN_DIAG_NG)
        for c in result.conditions:
            if c.name.startswith("row_") or c.name.startswith("col_"):
                assert c.status == ConditionStatus.PASS

    def test_fail_output_format(self):
        result = verify_grid(ROWS_COLS_OK_MAIN_DIAG_NG)
        lines = format_failures(result)
        assert "FAIL main_diagonal sum=31 expected=34" in lines


class TestAntiDiagonalNg:
    def test_anti_diagonal_named_in_failures(self):
        result = verify_grid(ROWS_COLS_OK_MAIN_DIAG_NG)
        anti = next(c for c in result.conditions if c.name == "anti_diagonal")
        assert anti.status == ConditionStatus.FAIL
        lines = format_failures(result)
        assert any("anti_diagonal" in line for line in lines)


class TestInvalidGrid:
    def test_duplicate_number(self):
        grid = [row[:] for row in COMPLETE_MAGIC]
        grid[0][0] = grid[0][1]
        result = verify_grid(grid)
        assert not result.grid_valid
        assert not result.ok
        assert any("duplicate" in e for e in result.errors)

    def test_too_many_blanks(self):
        grid = [row[:] for row in COMPLETE_MAGIC]
        grid[0][0] = 0
        grid[1][1] = 0
        grid[2][2] = 0
        result = verify_grid(grid)
        assert not result.grid_valid
        assert any("blank" in e for e in result.errors)

    def test_wrong_size(self):
        result = verify_grid([[1, 2], [3, 4]])
        assert not result.grid_valid
        assert any("4×4" in e or "4x4" in e for e in result.errors)


class TestIncompleteGrid:
    def test_two_blanks_skip_lines_with_zero(self):
        grid = [row[:] for row in COMPLETE_MAGIC]
        grid[0][0] = 0
        grid[3][3] = 0
        result = verify_grid(grid)
        assert result.grid_valid
        row0 = next(c for c in result.conditions if c.name == "row_0")
        main = next(c for c in result.conditions if c.name == "main_diagonal")
        assert row0.status == ConditionStatus.INCOMPLETE
        assert main.status == ConditionStatus.INCOMPLETE
        col0 = next(c for c in result.conditions if c.name == "col_0")
        col1 = next(c for c in result.conditions if c.name == "col_1")
        assert col0.status == ConditionStatus.INCOMPLETE
        assert col1.status == ConditionStatus.PASS
