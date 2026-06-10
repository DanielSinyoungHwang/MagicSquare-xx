# GREEN Minimal — ARRR R단계 (Respond = GREEN)

> **Phase: green**  
> **Layer: entity** *(Track A boundary 시 `boundary`로만 교체)*  
> **Track: Logic** *(UI 경계 테스트 시 `UI`로 교체)*  
> **RED 1묶음**당 `src/` **최소 구현**만 한다. **1 커밋 = 1 RED 묶음.**

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** (상수·ECB·최소 구현 규칙 SSOT).

---

## 목적

ARRR **R(Respond)** 단계 — 직전 RED 묶음 **1건**을 **PASS**로 만든다.

- `pytest.fail` 스켈레톤 → **assert 본문** 교체
- `src/`(또는 `entity/`)에 **이번 Test ID만** 통과시키는 최소 코드
- 다른 Test ID·REFACTOR·범위 creep **금지**

```python
validate_lines(grid) -> {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}
```

---

## 입력 (추가 프롬프트 없이)

| 소스 | 사용 |
|------|------|
| **직전 RED 묶음** | `/red-test-plan` Test ID · `/red-skeleton`·`/tdd-red` 함수명·GWT |
| **실패 pytest 출력** | `RED: {Test ID}` 메시지·AssertionError·TypeError |
| **`entity/constants.py`** | `MAGIC_SUM`, `GRID_SIZE`, `CELL_MAX` 등 SSOT |
| **`magic-square-tdd` Skill** | 있으면 GREEN 범위·ECB·상수 규칙 우선 |

**RED 묶음:** 설계표·플랜에서 정한 Test ID **1개**(또는 1 시나리오). S1 → S2 → S3 순서 유지.

---

## 수행 절차

| 단계 | 할 일 | 수정 범위 |
|------|--------|-----------|
| **1. RED 재확인** | 대상 Test ID·함수·`pytest.fail`/`assert` 상태 확인. `python -m pytest <경로>::<함수> -v` → **FAILED** 재현 | — |
| **2. 최소 구현** | 이번 GWT·Then만 만족하는 **가장 짧은** `src/`·`entity/` 코드 | `src/`, `entity/` (필요 최소) |
| **3. assert 교체** | `pytest.fail("RED: …")` **제거** → 설계표 Then에 맞는 **엄격한 assert** | `tests/` |
| **4. PASS 확인** | 단일 테스트 PASS → **파일 전체** → 기존 회귀 suite PASS | — |
| **5. 보고** | Test ID · 변경 파일 · pytest 결과 (회귀 실패 시 **즉시 수정** 후 재보고) | — |

---

## 구현 규칙

| 항목 | 규칙 |
|------|------|
| **최소 구현** | 이번 Test ID PASS에 **필요한 분기·로직만**. 다음 S2/S3 미리 구현 금지 |
| **상수 SSOT** | `34`·`16`·`4`·`0` 리터럴 **금지** → `entity.constants` import |
| **10선 명명** | R1~R4, C1~C4, D1, D2 (`.cursorrules` 고정) |
| **API 계약** | `status` 3값·`failed_lines` 키(`line`, `actual`, `expected`) 변경 금지 |
| **assert** | 설계표 Then **그대로** — 완화·삭제·skip 금지 |

---

## ECB · 계층 격리 (entity · Logic)

| 계층 | entity GREEN 허용 | 금지 |
|------|-------------------|------|
| **Condition** | 10선 합산·`validate_lines` 판정 | — |
| **Behavior** | `{status, failed_lines}` 반환 | Event 메시지·exit code |
| **Event E001~E005** | **raise·return·emit 금지** | E001~E005는 boundary 입력 오류 전용 |
| **import** | `entity.constants`, 동일 계층 모듈 | **`boundary`·`control`·CLI·`magicxx.cli` import 금지** |

**E001~E005 (entity에서 사용 금지):**

| 코드 | 의미 |
|------|------|
| E001 | 격자 크기 ≠ 4×4 |
| E002 | 1~16 중복 |
| E003 | 빈칸 3개 이상 |
| E004 | 1~16 범위 밖 |
| E005 | 파싱·입력 형식 오류 |

> 구조 오류는 `validate_lines` **입력 전** 별도 검증. entity GREEN은 **유효 격자** 위 10선 판정만.

---

## pytest 명령

**단일 테스트 (이번 RED 묶음):**

```bash
python -m pytest tests/test_validate_lines.py::test_complete_grid_all_ten_lines_pass -v
```

**파일 전체 (회귀):**

```bash
python -m pytest tests/test_validate_lines.py -v
```

회귀 범위에 `tests/test_verify.py` 등 기존 suite가 있으면 **함께** 실행해 PASS 확인.

---

## assert 교체 예시

**Before (스켈레톤):**

```python
    # Then
    pytest.fail(
        f"RED: T-S1-01 — status=pass, failed_lines=[]"
    )
```

**After (GREEN):**

```python
    # Then
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
```

---

## git

| 규칙 | 내용 |
|------|------|
| **커밋 시점** | 사용자가 **명시적으로 요청할 때만** |
| **1 커밋 = 1 RED 묶음** | 한 커밋에 Test ID 2건 이상·다음 단계 선행 구현 금지 |
| **메시지** | 한국어 · `green: {Test ID} — <한 줄 요약>` |

---

## 보고 형식

```
Phase: green | Layer: entity | Track: Logic

## PASS Test ID
- {Test ID}

## 변경 파일
- src/validate_lines.py (또는 entity/…)
- tests/test_validate_lines.py :: test_<함수명>
- entity/constants.py (필요 시)

## pytest 결과
- 단일: PASSED — tests/...::test_<함수>
- 파일: PASSED — tests/test_validate_lines.py (N passed)
- 회귀: PASSED / FAILED — <실패 시 즉시 수정 후 재실행>

## 다음
- REFACTOR: /refactor (별도 Command·이번 GREEN 범위 밖)
- 다음 RED: /red-test-plan → /red-skeleton
```

**회귀 실패 시:** 원인 수정 → pytest 재실행 → 보고 갱신. **PASS 확인 전 종료 금지.**

---

## 금지 (본 Command)

| 금지 | 이유 |
|------|------|
| **이번 RED 묶음 외 Test ID 동시 해결** | 1묶음 = 1 GREEN |
| **REFACTOR** (이름 정리·구조 개편·중복 제거) | 별도 단계 |
| **assert 완화** (`==` → `in`, 조건 삭제 등) | 요구사항 희석 |
| **skip / xfail / 테스트 삭제** | GREEN 회피 |
| **하드코딩·매직넘버** | `entity.constants` SSOT |
| **E001~E005 raise/return** | Event는 boundary |
| **entity → boundary/control import** | ECB 계층 침범 |
| **Solver·힌트·n×n·GUI** | Out of Scope |
| **git commit·push** (묵시적) | 사용자 요청 시만 |

---

## GREEN Minimal 체크리스트

- [ ] 응답 첫 줄: `Phase: green | Layer: … | Track: …`
- [ ] 대상 **RED 묶음 1건**만 처리
- [ ] RED 재확인 → 최소 구현 → `pytest.fail` 제거·assert 교체
- [ ] 상수는 `entity.constants` import
- [ ] E001~E005·boundary/control import **없음**
- [ ] 단일 테스트 **PASSED**
- [ ] 파일·회귀 suite **PASSED** (실패 시 즉시 수정)
- [ ] REFACTOR·다음 Test ID 선행 구현 **없음**
- [ ] git commit은 사용자 요청 시만

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| ③ | `/red-test-plan` | 설계표 |
| ④ | `/red-skeleton` | `pytest.fail` 스켈레톤 |
| ⑤ | `/tdd-red` | assert RED (선택·프로젝트에 따라 생략 가능) |
| ⑥ | **`/green-minimal`** | `src/` 최소 구현 · **PASS** |
| ⑦ | REFACTOR | 별도 Command (이번 범위 밖) |
