---
name: magic-square-tdd
description: >-
  MagicSquare_xx 4×4 마방진 검증 TDD 워크플로(ARRR·Dual-Track·C2C·ECB).
  Use when Phase is red, green, or refactor; when running Commands
  /red-test-plan, /red-skeleton, /green-minimal, /refactor-safe (or
  /refactor-smell, /golden-master, /tdd-red); or when the user mentions
  TDD, RED, GREEN, REFACTOR, Dual-Track, C2C, or pytest.fail.
disable-model-invocation: true
---

# MagicSquare TDD

**SSOT:** `.cursorrules`, `docs/PRD.md` — 충돌 시 이 둘을 우선한다.

**범위:** 4×4 검증만. Solver·힌트·n×n·GUI Out of Scope.

**API:**

```python
validate_lines(grid) -> {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}
```

- `failed_lines` 항목: `line`(R1~R4,C1~C4,D1,D2), `actual`, `expected`
- 구조 오류는 `validate_lines` **입력 전** 별도 검증

---

## 1. ARRR ↔ TDD 매핑

| ARRR | TDD | Command | 산출 |
|------|-----|---------|------|
| **Ask** | RED ③④⑤ | `/red-test-plan` → `/red-skeleton` → `/tdd-red` | 설계표 · `pytest.fail` · assert RED |
| **Respond** | GREEN | `/green-minimal` → `/golden-master` | 최소 구현 · PASS · approval snapshot |
| **Refine** | REFACTOR | `/refactor-smell` → `/refactor-safe` | 스멜 탐지 · safe refactor 1건 |

**Test Loop:** RED → GREEN → REFACTOR 고정. 한 RED 묶음씩.

**성공 기준 (PRD):** S1(10선 일괄) → S2(실패 선 상세) → S3(행·열 OK + 대각 FAIL).

---

## 2. Phase 선언 (응답 첫 줄)

| Phase | 형식 |
|-------|------|
| RED 설계 | `Phase: red \| Layer: entity \| Track: Logic` |
| GREEN | `Phase: green \| Layer: entity \| Track: Logic` |
| REFACTOR 탐지 | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |
| REFACTOR 실행 | `Phase: refactor \| Layer: entity \| Track: Logic` |

- `Layer`: `entity` \| `boundary`
- `Track`: `Logic` \| `UI`
- boundary Track A: `Layer: boundary`만 교체, 나머지 동일

---

## 3. C2C Rule 1~3

한 행 = RED 1묶음.

| Rule | 내용 |
|------|------|
| **Rule1** | PRD FR 인용 — `FR-R*`·`FR-S*`·`FR-T*` 또는 S1~S3 |
| **Rule2** | To-Do **1개** — 검증할 단일 행동 (동사 1문장) |
| **Rule3** | Test ID + **Given / When / Then** (격자·호출·`status`·`failed_lines`) |

**Test ID:** `T-<기준>-<순번>` 또는 `S1`/`S2`/`S3`. 아직 RED 없는 항목 우선.

---

## 4. RED 절대 금지

| 금지 | RED 단계 |
|------|----------|
| **`src/` 수정** | `/red-test-plan`(③), `/red-skeleton`(④), `/tdd-red`(⑤) |
| **`tests/`·`src/` 생성** | `/red-test-plan` — 설계만 |
| **`assert` 본문** (초기) | `/red-skeleton` — `pytest.fail` 한 줄만 |
| **`assert` 완화** | 모든 RED |
| **`skip` / `xfail` / 테스트 삭제** | 모든 RED |
| **Logic Track Domain Mock** | Condition 실호출·픽스처 리터럴만 |
| **E001~E005 emit·assert** | entity Logic — Event 전용 |
| **GREEN / REFACTOR 선행** | 순서 위반 |

**E001~E005:** E001 크기≠4×4 · E002 중복 · E003 빈칸≥3 · E004 범위밖 · E005 파싱오류

---

## 5. GREEN 규칙

| 규칙 | 내용 |
|------|------|
| **범위** | RED 묶음 **1건**만 PASS |
| **구현** | `src/`·`entity/` 최소 코드 — 다음 S2/S3 선행 금지 |
| **테스트** | `pytest.fail` 제거 → 설계표 Then **엄격 assert** |
| **상수 SSOT** | `34`·`16`·`4`·`0` 리터럴 금지 → `entity/constants.py` |
| **ECB** | entity → `boundary`/`control` import 금지 |
| **E001~E005** | entity에서 raise/return/emit 금지 |
| **커밋** | **1 커밋 = 1 RED 묶음** · 사용자 요청 시만 |
| **golden** | `/golden-master`: `UPDATE_GOLDEN=1`로만 생성 · 수동 편집 금지 |

---

## 6. REFACTOR 규칙

**전제:** `python -m pytest tests/ -v` 전부 PASS (실패 시 중단).

| 항목 | 내용 |
|------|------|
| **탐지** | `/refactor-smell` — 수정·commit 금지 |
| **실행** | `/refactor-safe` — 표에서 **스멜 1개**만 |
| **Change Budget** | 파일≤3 · 클래스≤1 · 메서드≤3 |
| **불변** | 입출력·예외·`int[6]` 1-index·E00x 문자열 |
| **금지** | 기능 추가·버그 수정 (→ `/green-minimal`) |
| **golden** | `UPDATE_GOLDEN` 없이 matched 유지; 의도적 diff만 ISS+재승인; 비의도→롤백 |

**스멜 6유형:** Long Method · Duplicated Code · Mysterious Name · Magic Number · ECB 위반 · Feature Envy

---

## 7. Dual-Track — Track A vs Track B

| | **Track B — Logic** | **Track A — UI (boundary)** |
|---|---------------------|----------------------------|
| **Layer** | `entity` | `boundary` |
| **대상** | `validate_lines`, `verify_grid`, rules | CLI `verify`, stdin/stdout, exit code |
| **C2C Rule1** | `FR-R*`·`FR-S*`·S1~S3 | `FR-C*`·`FR-T2` |
| **테스트** | 도메인 실호출 · Domain Mock **금지** | IO·CLI Mock 허용 (도메인 Mock 금지) |
| **E001~E005** | emit·assert **금지** | 입력 오류 테스트에서만 |
| **전환** | 기본 | `Layer: boundary`만 교체 |

---

## 8. Command 체인

```
/red-test-plan          # ③ 설계표·플랜 (코드 없음)
    ↓
/red-skeleton           # ④ pytest.fail 스켈레톤 (tests/만)
    ↓
/tdd-red                # ⑤ assert RED (선택·프로젝트 관례)
    ↓
/green-minimal          # ⑥ src/ 최소 구현 · PASS
    ↓
/golden-master          # ⑦ approval snapshot · matched
    ↓
/refactor-smell         # ⑧ 스멜 탐지 (읽기만)
    ↓
/refactor-safe          # ⑨ 스멜 1건 · PASS · golden 유지
    ↓
/red-test-plan          # 다음 RED 묶음
```

| Command | 수정 허용 |
|---------|-----------|
| `red-test-plan` | 없음 |
| `red-skeleton` | `tests/`, `entity/constants.py`, `tests/conftest.py` |
| `tdd-red` | `tests/`만 |
| `green-minimal` | `src/`, `entity/`, `tests/` |
| `golden-master` | `tests/_approval.py`, `tests/golden/`, tests hook |
| `refactor-smell` | 없음 |
| `refactor-safe` | Budget 내 `src/`·`entity/`·`tests/` |

---

## 9. pytest 명령 패턴

**단일 Test ID (RED/GREEN):**

```bash
python -m pytest tests/test_validate_lines.py::test_<함수명> -v
```

**파일 전체 회귀:**

```bash
python -m pytest tests/test_validate_lines.py -v
```

**전체 suite (REFACTOR 전제·완료):**

```bash
python -m pytest tests/ -v
```

**스켈레톤 RED (`pytest.fail` 기대):**

```bash
python -m pytest tests/<파일>.py::<함수> -v
# FAILED — 메시지에 "RED: {Test ID}"
```

**golden 기준 생성 (1회·ISS 후):**

```bash
# PowerShell
$env:UPDATE_GOLDEN="1"; python -m pytest tests/<파일>.py::<함수> -v
Remove-Item Env:UPDATE_GOLDEN

# Unix
UPDATE_GOLDEN=1 python -m pytest tests/<파일>.py::<함수> -v
```

**golden matched (상시):** `UPDATE_GOLDEN` unset → PASSED

---

## 10. 완료 보고 형식

### red-test-plan

```
Phase: red | Layer: entity | Track: Logic
## 1. C2C … ## 2. Track B … ## 3. 테스트 플랜 … ## 4. ECB·Mock …
/red-skeleton 으로 넘길 준비됐다
```

### red-skeleton

```
Phase: red | Layer: entity | Track: Logic
## Test ID · pytest FAILED (RED: …) · 변경 파일(tests/만)
```

### green-minimal

```
Phase: green | Layer: entity | Track: Logic
## PASS Test ID · 변경 파일 · pytest PASSED
```

### golden-master

```
Phase: green | Layer: entity | Track: Logic
## golden 경로 · matched YES/NO · diff 요약
```

### refactor-smell

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
## pytest 전제 PASSED · 스멜 표 · /refactor-safe 후보 #1~#3
```

### refactor-safe

```
Phase: refactor | Layer: entity | Track: Logic
## 선택 후보 · 변경 요약 · pytest PASSED · golden matched
```

---

## 부록 — 상수·픽스처·golden

**`entity/constants.py`:**

```python
GRID_SIZE = 4
MAGIC_SUM = 34
CELL_MIN = 1
CELL_MAX = 16
BLANK = 0
MAX_BLANKS = 2
```

**`tests/conftest.py` — `grid_g1`:** 빈칸 `0` 2개, row-major 4×4. 검증 로직 금지.

**golden 포맷 (`tests/golden/{id}.approved.txt`):**

- `int[6]:` — 6정수, **1-index**, 쉼표 구분
- `errors:` — `E001`~`E005` 또는 빈 줄
- `status:` · `failed_lines:` — 고정 레이아웃
- 비교: `tests/_approval.py` · `assert_matches_golden`

**스켈레톤 Then (RED ④):**

```python
pytest.fail("RED: T-S3-01 — status=fail, failed_lines D1 actual=31 expected=34")
```

**ECB 요약:**

| 계층 | entity Logic |
|------|--------------|
| Event | CLI·stdin 직접 호출 금지 |
| Condition | `validate_lines` 실호출 |
| Behavior | `status`·`failed_lines` assert |

---

## 체크리스트 (Command 실행 시)

- [ ] SSOT `.cursorrules`·`docs/PRD.md` 확인
- [ ] 응답 첫 줄 Phase 선언
- [ ] Command별 수정 범위·금지 준수
- [ ] pytest 실행·결과 보고
- [ ] git commit은 사용자 요청 시만
- [ ] 한국어 응답·주석
