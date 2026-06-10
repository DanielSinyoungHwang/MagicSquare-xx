from src.validate_lines import validate_lines

MAGIC_SUM = 34  # GREEN 이후 src/rules.py SSOT로 이전 예정

COMPLETE_MAGIC = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def test_complete_grid_all_ten_lines_pass():
    # Arrange
    grid = COMPLETE_MAGIC

    # Act
    result = validate_lines(grid)

    # Assert — S1: 10선 일괄 pass
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
