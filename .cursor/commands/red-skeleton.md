# RED Skeleton — ARRR A단계 (RED ④)

> **Phase: red**  
> **Layer: entity** *(Track A boundary 시 `boundary`로만 교체)*  
> **Track: Logic** *(UI 경계 테스트 시 `UI`로 교체)*  
> `/red-test-plan` 설계표 기준 **`pytest.fail` 스켈레톤만** 작성한다. **`tests/`만** 수정.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** (상수·픽스처·명명·RED 규칙 SSOT).

---

## 목적

ARRR **A(Ask)** 단계 **RED ④** — 설계표를 **실행 가능한 실패 스켈레톤**으로 옮긴다.

- C2C·블록 3 테스트 플랜 → `tests/` 코드 (함수·AAA 주석·`pytest.fail` 한 줄)
- **assert 본문 없음** — GREEN(`/tdd-red` 이후)에서 assert로 교체
- `src/` 미구현 상태에서도 **의도적 RED** 유지

```python
validate_lines(grid) -> {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}
```

---

## 입력 (추가 프롬프트 없이)

| 소스 | 사용 |
|------|------|
| **직전 `/red-test-plan` 출력** | Test ID, GWT, 파일 경로, 함수명, conftest, pytest 명령, RED 묶음 |
| **채팅·PRD·`.cursorrules`** | 플랜 없을 때 동일 규칙으로 Test ID 1건 추론 |
| **`magic-square-tdd` Skill** | 있으면 픽스처·상수·금지 규칙 우선 적용 |

플랜이 없으면 먼저 `/red-test-plan` 권장. 단독 실행 시 S1→S2→S3 중 **아직 스켈레톤 없는** 1건.

---

## 수행 절차

1. 설계표에서 **Test ID 1건**(또는 플랜의 RED 묶음) 확정
2. 필요 시 `entity/constants.py`·`tests/conftest.py` **최소 추가** (`tests/`·`entity/constants.py`만 — `src/` 금지)
3. 테스트 파일에 **AAA 주석 + `pytest.fail` 한 줄** 스켈레톤 작성
4. `python -m pytest <경로>::<함수명> -v` 실행
5. 보고 (아래 형식)

---

## 스켈레톤 규칙

| 항목 | 규칙 |
|------|------|
| **AAA 주석** | `# Given` / `# When` / `# Then` — 설계표 GWT와 1:1 |
| **Then** | `pytest.fail("RED: {Test ID} — <Then 기대 한 줄>")` **한 줄만** |
| **Act** | When에 호출이 있으면 `result = validate_lines(grid)` 등 **허용** — 단 Then은 fail만 |
| **상수** | `34`·`16`·`4` 리터럴 **금지** → `entity.constants` import (`MAGIC_SUM`, `GRID_SIZE`, `CELL_MAX` 등) |
| **격자 데이터** | 픽스처·모듈 상수·`grid_g1` — **리터럴 2차원 배열만** 허용 |
| **conftest** | `tests/conftest.py` — `grid_g1`: 빈칸 `0` **2개**, row-major 4×4. **검증 로직 금지** |
| **RED 묶음** | 한 번에 테스트 **1개(또는 1 시나리오)** |

---

## conftest — `grid_g1`

```python
# tests/conftest.py
import pytest

@pytest.fixture
def grid_g1():
    """빈칸 0 두 개, row-major 4×4 (부분 마방진 중간판)."""
    return [
        [0, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ]
```

- 좌표: row-major → `(row, col)` = `(0,0)`, `(3,3)` 에 `0`
- 검증·합산·`validate_lines` 호출 **금지**

---

## 상수 — `entity/constants.py`

```python
# entity/constants.py
GRID_SIZE = 4
MAGIC_SUM = 34
CELL_MIN = 1
CELL_MAX = 16
BLANK = 0
MAX_BLANKS = 2
```

- 테스트: `from entity.constants import MAGIC_SUM, GRID_SIZE, CELL_MAX, BLANK`
- **격자 셀 값 배열만** 테스트 파일·conftest에 둔다

---

## 템플릿 예시 — `test_d_loc_01_blank_coords_row_major`

설계표 Test ID **T-D-LOC-01** (빈칸 좌표·row-major) 기준:

```python
# tests/test_blank_coords.py

import pytest

from entity.constants import BLANK, GRID_SIZE


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given — grid_g1: 빈칸 0 두 개, row-major (0,0)·(3,3)
    grid = grid_g1
    blank_cells = [
        (r, c)
        for r in range(GRID_SIZE)
        for c in range(GRID_SIZE)
        if grid[r][c] == BLANK
    ]

    # When — 빈칸 좌표를 row-major 순으로 수집
    # (스켈레톤: 도메인 함수 연결 전 — 좌표만 확정)

    # Then
    pytest.fail(
        "RED: T-D-LOC-01 — row-major 빈칸 좌표 [(0,0),(3,3)] 검증 미구현"
    )
```

**`validate_lines` 대상 스켈레톤 예시 (S3):**

```python
# tests/test_validate_lines.py

import pytest

from entity.constants import MAGIC_SUM
from src.validate_lines import validate_lines

ROWS_COLS_OK_MAIN_DIAG_NG = [
    [13, 3, 2, 16],
    [8, 10, 11, 5],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def test_s3_rows_cols_ok_main_diagonal_fail():
    # Given — 행·열 합 34, D1 합 31 (Mom Test S3)
    grid = ROWS_COLS_OK_MAIN_DIAG_NG

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail(
        f"RED: T-S3-01 — status=fail, failed_lines D1 actual=31 expected={MAGIC_SUM}"
    )
```

> 스켈레톤 Then은 **항상** `pytest.fail` 한 줄. `assert result[...]` 는 `/tdd-red`·GREEN 단계.

---

## pytest 실행

```bash
python -m pytest <블록3 경로>::<함수명> -v
```

**기대:** `FAILED` — 메시지에 `RED: {Test ID}` 포함 (`pytest.fail` 의도적 실패).

---

## 보고 형식

```
Phase: red | Layer: entity | Track: Logic

## Test ID
- {Test ID}

## pytest 결과
- FAILED — RED: {Test ID} — …

## 변경 파일 (tests/만)
- tests/conftest.py (grid_g1 추가/유지 시)
- tests/<파일>.py :: test_<함수명>
- entity/constants.py (최초 1회·상수 SSOT)

## 다음
- /tdd-red: pytest.fail → assert 본문으로 RED 확정
- GREEN: src/ 최소 구현
```

---

## 금지 (본 Command)

| 금지 | 이유 |
|------|------|
| **`src/` 수정** | 스켈레톤은 tests·entity/constants만 |
| **`assert` 본문** (status·failed_lines 등) | RED ④는 fail 스텁만 — assert는 `/tdd-red` |
| **`@pytest.mark.skip` / `xfail`** | 실패 숨김 |
| **통과 더미** (`pass`, `return`, 빈 assert) | RED 회피 |
| **34·16·4 리터럴** (상수 자리) | `entity.constants` SSOT |
| **conftest 검증 로직** | 구현 누수 |
| **GREEN / REFACTOR** | 이후 Command |
| **Domain Mock** | `red-test-plan` ECB 점검과 동일 |

---

## RED Skeleton 체크리스트

- [ ] 응답 첫 줄: `Phase: red | Layer: … | Track: …`
- [ ] `/red-test-plan` 블록 3·Test ID와 일치
- [ ] AAA 주석 Given/When/Then
- [ ] Then = `pytest.fail("RED: {Test ID} — …")` **한 줄만**
- [ ] 상수는 `entity.constants` import
- [ ] `grid_g1` conftest (0 두 개, row-major)
- [ ] `magic-square-tdd` Skill 있으면 적용
- [ ] `src/` **미수정**
- [ ] `python -m pytest` 실행 → **FAILED** + `RED:` 메시지
- [ ] 보고: Test ID · FAIL 한 줄 · 변경 파일(`tests/`만)

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| ③ | `/red-test-plan` | C2C·테스트 플랜 (코드 없음) |
| ④ | **`/red-skeleton`** | `pytest.fail` 스켈레톤 (`tests/`만) |
| ⑤ | `/tdd-red` | assert 본문 RED · pytest FAILED 확정 |
| ⑥ | GREEN | `src/` 최소 구현 |
