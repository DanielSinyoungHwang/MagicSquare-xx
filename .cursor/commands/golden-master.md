# Golden Master — Approval Test (GREEN 후)

> **Phase: green**  
> **Layer: entity** *(Track A boundary 시 `boundary`로만 교체)*  
> **Track: Logic**  
> GREEN **PASS** 직후 대상 Test ID의 **Golden Master(Approval Test)** 를 구축·검증한다.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** (golden 포맷·경로·UPDATE_GOLDEN 규칙 SSOT).

---

## 목적

단위 assert PASS를 **승인 스냅샷**으로 고정해 회귀를 잡는다.

- 실제 출력(직렬화 문자열) ↔ `tests/golden/{id}.approved.txt` **바이트 단위 일치**
- 기준 파일은 **`UPDATE_GOLDEN=1` pytest** 로만 생성·갱신
- golden **수동 편집으로 통과 우회 금지**

---

## 전제

| 항목 | 조건 |
|------|------|
| **대상 Test ID** | `/green-minimal` 완료 · 해당 함수 **pytest PASSED** |
| **입력** | 채팅·직전 GREEN 보고에서 Test ID·함수 경로 추출 |
| **수정 범위** | `tests/_approval.py`, `tests/golden/`, 대상 테스트 **approval hook만** (`src/` 변경 없음) |

전제 미충족 시 **중단** → `/green-minimal` 먼저.

---

## 수행 절차

| 단계 | 할 일 |
|------|--------|
| **1** | `tests/_approval.py`에 `assert_matches_golden` 확인 — **없으면 생성** |
| **2** | 대상 테스트에 golden 연결: `tests/golden/{id}.approved.txt` (`{id}` = Test ID, 예: `T-S1-01`) |
| **3** | **기준 생성:** `UPDATE_GOLDEN=1 pytest <경로>::<함수> -v` |
| **4** | **matched 확인:** `UPDATE_GOLDEN` **없이** 동일 pytest → PASSED |
| **5** | 보고 (golden 경로 · matched · diff 요약) |

---

## `assert_matches_golden`

`tests/_approval.py` — 프로젝트 공통 헬퍼 (1회 정의, 테스트마다 재사용).

```python
# tests/_approval.py
from __future__ import annotations

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def assert_matches_golden(test_id: str, actual: str) -> None:
    """Approval Test — actual vs tests/golden/{id}.approved.txt."""
    golden_path = GOLDEN_DIR / f"{test_id}.approved.txt"
    actual_norm = actual.rstrip() + "\n"

    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual_norm, encoding="utf-8")
        return

    if not golden_path.is_file():
        raise AssertionError(
            f"golden missing: {golden_path} — run UPDATE_GOLDEN=1 pytest …"
        )

    expected = golden_path.read_text(encoding="utf-8")
    if actual_norm != expected:
        raise AssertionError(
            f"golden mismatch: {test_id}\n"
            f"--- expected ({golden_path})\n{expected}"
            f"--- actual\n{actual_norm}"
        )
```

- **검증 로직은 여기만** — conftest·개별 테스트에 비교 분기 중복 금지
- `UPDATE_GOLDEN=1` 일 때만 파일 쓰기

---

## golden 파일 포맷 (고정)

`tests/golden/{id}.approved.txt` — **수동 편집 금지**. 포맷 변경은 테스트·구현 수정 후 `UPDATE_GOLDEN=1` 재생성.

```
# test_id: T-S1-01
# format: v1.0
int[6]: 1,1,4,4,34,0
errors:
status: pass
failed_lines:
```

| 필드 | 규칙 |
|------|------|
| **`int[6]`** | 정수 **6개**, **1-index** (0-index 금지). 쉼표 구분 · 공백 없음. 의미는 Test ID별 GWT에 따름 (예: 빈칸 `(row,col)`×2 + `MAGIC_SUM` + 플래그) |
| **`errors:`** | 다음 줄부터 에러 코드. 없으면 **빈 줄** 유지. 코드는 `E001`~`E005` **문자열 고정** (entity Logic: 보통 빈 줄) |
| **`status:`** | `pass` \| `fail` \| `incomplete` |
| **`failed_lines:`** | JSON 아님 — 한 줄 한 항목: `line=R1 actual=34 expected=34` (없으면 빈 줄) |

**에러 코드 문자열 (고정):**

| 코드 | 문자열 |
|------|--------|
| E001 | `E001` |
| E002 | `E002` |
| E003 | `E003` |
| E004 | `E004` |
| E005 | `E005` |

> boundary Track은 `errors:` 줄에 `E00x` 허용. entity Logic golden은 **유효 격자** 전제 → `errors:` 빈 줄.

---

## 테스트 연결 예시

```python
# tests/test_validate_lines.py

from tests._approval import assert_matches_golden
from src.validate_lines import validate_lines
from entity.constants import MAGIC_SUM, BLANK, GRID_SIZE


def _format_golden_output(test_id: str, grid, result) -> str:
    blanks = [
        (r + 1, c + 1)  # 1-index
        for r in range(GRID_SIZE)
        for c in range(GRID_SIZE)
        if grid[r][c] == BLANK
    ]
    while len(blanks) < 2:
        blanks.append((0, 0))
    (r1, c1), (r2, c2) = blanks[0], blanks[1]
    flag = 0 if result["status"] == "pass" else 1

    lines = [
        f"# test_id: {test_id}",
        "# format: v1.0",
        f"int[6]: {r1},{c1},{r2},{c2},{MAGIC_SUM},{flag}",
        "errors:",
        f"status: {result['status']}",
        "failed_lines:",
    ]
    for f in result["failed_lines"]:
        lines.append(
            f"line={f['line']} actual={f['actual']} expected={f['expected']}"
        )
    if not result["failed_lines"]:
        lines.append("")
    return "\n".join(lines)


def test_complete_grid_all_ten_lines_pass():
    test_id = "T-S1-01"
    grid = COMPLETE_MAGIC
    result = validate_lines(grid)

    assert result["status"] == "pass"
    assert result["failed_lines"] == []

    assert_matches_golden(test_id, _format_golden_output(test_id, grid, result))
```

- **단위 assert 유지** + 마지막에 `assert_matches_golden` — assert 완화·삭제 금지
- `{id}` = `test_id` 와 파일명 일치: `tests/golden/T-S1-01.approved.txt`

---

## pytest 명령

**기준 파일 생성 (1회·갱신 시만):**

```bash
# Windows PowerShell
$env:UPDATE_GOLDEN="1"; python -m pytest tests/test_validate_lines.py::test_complete_grid_all_ten_lines_pass -v

# Unix
UPDATE_GOLDEN=1 python -m pytest tests/test_validate_lines.py::test_complete_grid_all_ten_lines_pass -v
```

**matched 확인 (상시·CI):**

```bash
python -m pytest tests/test_validate_lines.py::test_complete_grid_all_ten_lines_pass -v
```

`UPDATE_GOLDEN` **unset** 상태에서 PASSED = **matched**.

---

## 금지

| 금지 | 이유 |
|------|------|
| **golden 수동 편집**으로 pytest PASS | Approval Test 무력화 |
| **`UPDATE_GOLDEN` 없이** golden 파일 직접 작성 | 기준 출처 불명 |
| **assert 완화**·golden 비교 skip | 회귀 누락 |
| **포맷 임의 변경** (`int[5]`, 0-index, 에러 문자열 변형) | diff 불가·교차 Test ID 비교 깨짐 |
| **`src/` 수정** (golden 단계) | 스냅샷만 고정 |
| **이번 Test ID 외** golden 일괄 갱신 | 1묶음 = 1 golden |

---

## 보고 형식

```
Phase: green | Layer: entity | Track: Logic

## Test ID
- {Test ID}

## golden 경로
- tests/golden/{id}.approved.txt

## matched
- YES — UPDATE_GOLDEN 없이 pytest PASSED
- NO — (diff 요약 아래, 구현·포맷 수정 후 재실행)

## diff 요약
- (mismatch 시) 변경 줄·필드만 1~3줄 — 전체 덤프 생략 가능

## 변경 파일
- tests/_approval.py (최초 생성 시)
- tests/golden/{id}.approved.txt (UPDATE_GOLDEN=1 생성)
- tests/<파일>.py (assert_matches_golden 연결)

## 다음
- 다음 RED: /red-test-plan
- REFACTOR: 별도 Command (golden 포맷 변경 시 UPDATE_GOLDEN=1 재승인)
```

**mismatch 시:** golden 수동 수정 **하지 말고** `_format_golden_output`·구현·단위 assert를 맞춘 뒤 `UPDATE_GOLDEN=1` 재생성.

---

## Golden Master 체크리스트

- [ ] 응답 첫 줄: `Phase: green | Layer: … | Track: …`
- [ ] 대상 Test ID **이미 pytest PASS**
- [ ] `tests/_approval.py` · `assert_matches_golden` 존재
- [ ] `tests/golden/{id}.approved.txt` 연결
- [ ] `int[6]` **1-index** · `E001`~`E005` 문자열 포맷 준수
- [ ] `UPDATE_GOLDEN=1` 로 기준 생성
- [ ] `UPDATE_GOLDEN` 없이 **matched** (PASSED)
- [ ] golden 수동 편집 **없음**
- [ ] 보고: golden 경로 · matched · diff 요약

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| ⑥ | `/green-minimal` | 단위 assert **PASS** |
| ⑦ | **`/golden-master`** | Approval snapshot · **matched** |
| ⑧ | REFACTOR | 별도 (golden 변경 시 재승인) |
