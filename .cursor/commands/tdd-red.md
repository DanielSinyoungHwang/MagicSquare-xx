# TDD RED — `validate_lines` 전용

> **Phase: RED**  
> `src/validate_lines.py`는 시그니처만 유지. **`tests/`만** 수정한다.

---

## 목적

`validate_lines(grid)` 계약을 **실패하는 테스트**로 먼저 고정한다.  
구현은 GREEN까지 미룬다.

```python
validate_lines(grid) -> {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}
```

---

## AAA 절차

| 단계 | 할 일 |
|------|--------|
| **Arrange** | 4×4 격자 픽스처 준비. 도메인 상수 34는 테스트에서도 **리터럴 대신** `MAGIC_SUM` 등 SSOT import(정의 후) 또는 주석으로 의도 명시. |
| **Act** | `result = validate_lines(grid)` 호출. |
| **Assert** | `status`, `failed_lines` 구조·값을 **엄격히** 검증. 선 이름은 R1~R4, C1~C4, D1, D2 체계. |

RED는 **한 번에 테스트 1개(또는 1개 시나리오)** 만 추가한다.

---

## pytest 예시

```python
# tests/test_validate_lines.py

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

    # Assert
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
```

```python
def test_s3_rows_cols_ok_main_diagonal_fail():
    # Arrange — 행·열 OK, D1 NG (Mom Test S3)
    grid = [
        [13, 3, 2, 16],
        [8, 10, 11, 5],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert any(
        f["line"] == "D1" and f["actual"] == 31 and f["expected"] == MAGIC_SUM
        for f in result["failed_lines"]
    )
```

**실행:**

```bash
python -m pytest tests/test_validate_lines.py -v
```

**기대:** `FAILED` — `validate_lines` 미구현 또는 `...` 본문 때문에 RED 확인.

---

## 보고 형식

RED 완료 시 아래 형식으로 보고한다.

```
Phase: RED

## 추가한 테스트
- tests/test_validate_lines.py :: test_<이름>

## 시나리오
- <한 줄: 무엇을 검증하는지>

## pytest 결과
- <FAILED / PASSED — RED에서는 FAILED 기대>
- <실패 메시지 한 줄>

## 다음
- GREEN: src/validate_lines.py 최소 구현
```

---

## 금지 (RED)

| 금지 | 이유 |
|------|------|
| `src/` **수정** (구현·로직 추가) | RED는 테스트만 |
| `assert` **완화** (`==` → `in`, 범위 넓히기 등) | 요구사항 희석 |
| `@pytest.mark.skip` / `xfail` | 실패 숨김 |
| 실패 테스트 **삭제** | RED 회피 |
| `conftest`에 검증 로직 | 구현 누수 |
| API 시그니처·반환 키 변경 | 계약 고정 후 진행 |

---

## RED 체크리스트

- [ ] 응답 첫 줄: `Phase: RED`
- [ ] 수정 파일이 `tests/` 안에만 있음
- [ ] `python -m pytest` 실행 결과 **FAILED**
- [ ] S1/S2/S3 중 이번 RED가 겨냥하는 기준 1개 명시
