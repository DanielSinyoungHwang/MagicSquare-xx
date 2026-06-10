# Refactor Safe — ARRR R단계 (Refine ⑨)

> **Phase: refactor**  
> **Layer: entity** *(Track A boundary 시 `boundary`로만 교체)*  
> **Track: Logic** *(UI 경계 시 `UI`로 교체)*  
> `/refactor-smell` 표에서 **선택한 스멜 1개만** Safe Refactor 실행한다.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** (Budget·ECB·golden·롤백 규칙 SSOT).

---

## 목적

ARRR **R(Refine)** 단계 **⑨** — 스멜 **1건**을 Change Budget 내에서 제거한다.

- **동작 동일** — 입출력·예외·golden 포맷 불변
- **기능 추가·버그 수정 금지** — 새 요구는 `/green-minimal` (별도 GREEN)
- 완료 후 **pytest 전체 PASS** + **golden matched** (`UPDATE_GOLDEN` 없음)

---

## 입력

| 소스 | 사용 |
|------|------|
| **직전 `/refactor-smell` 표** | 후보 **#1~#3** 중 **1개** (사용자 지정 또는 P0 #1 기본) |
| **후보 블록** | 위치·스멜 유형·제안 방향·Change Budget |
| **채팅** | `#2` 등 명시 선택 — 없으면 **P0 후보 #1** |
| **`magic-square-tdd` Skill** | 있으면 Safe Refactor 허용 목록 우선 |

**한 번에 스멜 1개만.** 표에 여러 P0가 있어도 이번 실행은 **1건**.

---

## 전제 (미충족 시 중단)

```bash
python -m pytest tests/ -v
```

| 조건 | 미충족 시 |
|------|-----------|
| **전체 PASS** | 중단 — `/green-minimal` 또는 회귀 수정 |
| **후보 Budget OK** | 예산 초과 후보 선택 시 중단 — `/refactor-smell` 재실행·분할 |
| **golden (사용 시)** | refactor **전** `UPDATE_GOLDEN` 없이 approval PASS 권장 |

---

## Safe Refactor 원칙

| 원칙 | 내용 |
|------|------|
| **입출력 불변** | `validate_lines` 반환 키·값·`status` 3값·`failed_lines` 구조 동일 |
| **예외 불변** | 새 raise·삼킨 예외·E001~E005 **emit 금지** |
| **`int[6]` 1-index** | golden 직렬화 포맷·1-index 좌표 **변경 금지** |
| **에러 코드 문자열** | `E001`~`E005` 문자열 포맷 고정 |
| **ECB** | entity → boundary/control import 추가 금지 |
| **기능·버그** | 새 분기·S2/S3 선행 구현·버그픽스 금지 → **GREEN** |
| **assert** | 완화·삭제·skip·xfail 금지 |

---

## Change Budget (필수 준수)

| 항목 | 상한 | 초과 시 |
|------|------|---------|
| **파일** | ≤ 3 | 중단 또는 더 작은 분할로 `/refactor-smell` 재등록 |
| **클래스** | ≤ 1 | 동일 |
| **메서드** | ≤ 3 | 동일 |

예: Magic Number 제거 = 파일 1 · 메서드 1 · `entity.constants` import만.

---

## 수행 절차

| 단계 | 할 일 |
|------|--------|
| **1** | 선택 후보 확인 (스멜·위치·Budget) |
| **2** | refactor **전** `python -m pytest tests/ -v` → PASS |
| **3** | Budget 내 **최소 diff** 수정 (`src/`·`entity/`·`tests/` 이름·상수·추출만) |
| **4** | `python -m pytest tests/ -v` → **전부 PASS** |
| **5** | golden approval 테스트 `UPDATE_GOLDEN` **없이** → **matched** 확인 |
| **6** | golden diff 처리 (아래) |
| **7** | 보고 |

---

## golden diff 처리

refactor 후 approval 테스트가 mismatch 일 때:

| 구분 | 판단 | 조치 |
|------|------|------|
| **의도적** | 포맷 함수 시그니처·변수명만 변경, **의미·int[6]·status·errors 동일** | ISS(이슈/메모)에 **의도·diff 요약** 문서화 → `UPDATE_GOLDEN=1 pytest <대상>` 재승인 → 다시 `UPDATE_GOLDEN` 없이 matched |
| **비의도** | `int[6]` 값·status·failed_lines·errors 내용 변경 | **즉시 롤백** (git checkout 또는 수동 revert) → pytest PASS 복구 → refactor 방향 재검토 |

**금지:** golden `.approved.txt` **수동 편집**으로 matched 우회.

**ISS 문서화 예 (의도적):**

```markdown
## ISS — golden 재승인 (refactor-safe #1)
- 날짜: YYYY-MM-DD
- 스멜: Magic Number → entity.constants
- diff: (없음 | whitespace만 | 주석 줄만)
- UPDATE_GOLDEN: tests/golden/T-S1-01.approved.txt 재생성 완료
```

---

## 스멜 유형별 허용·금지

| 스멜 | 허용 | 금지 |
|------|------|------|
| **Magic Number** | `entity.constants` import 치환 | 상수값 변경 |
| **Mysterious Name** | 변수·함수 **rename** (호출부 동시) | 공개 API 시그니처 변경 |
| **Long Method** | **extract** ≤3 메서드 (동일 파일) | 새 책임·IO 추가 |
| **Duplicated Code** | 공통 헬퍼 추출 (Budget 내) | `magicxx`↔`src` 대규모 통합 (Budget 초과) |
| **ECB 위반** | import 제거·계층 분리 | Event 로직을 entity에 추가 |
| **Feature Envy** | 테스트 헬퍼 추출 | assert 완화로 envy 숨김 |

---

## pytest · golden 명령

**회귀 (필수):**

```bash
python -m pytest tests/ -v
```

**golden matched (approval 사용 시, UPDATE_GOLDEN 없음):**

```bash
python -m pytest tests/ -v
```

**의도적 golden 재승인 (ISS 후 1회만):**

```bash
# PowerShell
$env:UPDATE_GOLDEN="1"; python -m pytest tests/test_validate_lines.py::test_complete_grid_all_ten_lines_pass -v
Remove-Item Env:UPDATE_GOLDEN

# Unix
UPDATE_GOLDEN=1 python -m pytest tests/test_validate_lines.py::test_complete_grid_all_ten_lines_pass -v
```

이후 반드시 `UPDATE_GOLDEN` 없이 전체 suite **matched** 재확인.

---

## git

| 규칙 | 내용 |
|------|------|
| **커밋** | 사용자 **명시 요청 시만** |
| **메시지** | `refactor: {스멜} — {위치 한 줄}` (한국어) |
| **1 커밋 = 스멜 1건** | 여러 후보 동시 커밋 금지 |

---

## 보고 형식

```
Phase: refactor | Layer: entity | Track: Logic

## 선택 후보
- #1 (P0 · Magic Number) — src/validate_lines.py :: validate_lines

## 변경 요약
- (한 줄: 무엇을 어떻게 — 동작 동일 명시)
- 파일: … (≤3)

## pytest
- PASSED — python -m pytest tests/ -v (N passed)

## golden matched
- YES — UPDATE_GOLDEN 없이 approval PASSED
- NO → (의도적: ISS + UPDATE_GOLDEN 재승인 완료 여부 / 비의도: 롤백 완료)

## diff 요약 (golden)
- (해당 시만) 변경 줄·필드 1~3줄

## 다음
- 남은 스멜: /refactor-smell 재실행
- 기능 요구: /red-test-plan (GREEN)
```

**pytest 또는 golden matched 실패 상태로 종료 금지** (비의도 시 롤백 후 보고).

---

## 금지 (본 Command)

| 금지 | 이유 |
|------|------|
| **스멜 2건 이상** 동시 수정 | 1 safe refactor = 1 스멜 |
| **Change Budget 초과** | 안전성 |
| **기능 추가·버그 수정** | GREEN 범위 |
| **입출력·예외·int[6]·E00x 포맷 변경** | Safe Refactor 원칙 |
| **E001~E005 emit** | ECB |
| **assert 완화·skip·xfail** | 회귀 누락 |
| **golden 수동 편집** | Approval 무력화 |
| **비의도 diff 유지** | 롤백 필수 |
| **git commit** (묵시적) | 사용자 요청 시만 |

---

## Refactor Safe 체크리스트

- [ ] 응답 첫 줄: `Phase: refactor | Layer: … | Track: …`
- [ ] `/refactor-smell` 후보 **1개**만 선택·실행
- [ ] Change Budget **준수** (파일≤3 · 클래스≤1 · 메서드≤3)
- [ ] 입출력·예외·`int[6]` 1-index·E00x **불변**
- [ ] 기능 추가·버그 수정 **없음**
- [ ] `python -m pytest tests/ -v` **전부 PASS**
- [ ] golden **matched** (`UPDATE_GOLDEN` 없음) 또는 의도적 ISS+재승인 / 비의도 롤백
- [ ] 보고: 변경 요약 · pytest · golden matched

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| ⑧ | `/refactor-smell` | 스멜 표 · 후보 #1~#3 |
| ⑨ | **`/refactor-safe`** | 스멜 1건 제거 · PASS · matched |
| — | `/refactor-smell` | 남은 스멜 재탐지 (반복) |
| — | `/red-test-plan` | 새 기능 (GREEN 루프) |
