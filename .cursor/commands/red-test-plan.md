# RED Test Plan — ARRR A단계 (Ask = RED ③)

> **Phase: red**  
> **Layer: entity** *(Track A boundary 시 `boundary`로만 교체)*  
> **Track: Logic** *(UI 경계 테스트 시 `UI`로 교체)*  
> C2C 설계표·테스트 플랜만 작성한다. **`tests/`·`src/` 파일 생성·수정 금지.**

---

## 목적

ARRR **A(Ask)** 단계에서 다음 RED 사이클의 **설계만** 고정한다.

- PRD 기능 요구(FR) → C2C 매핑 → Test ID·Given/When/Then
- Track B(Logic) 실패 시나리오 표
- pytest 실행 계획(경로·픽스처·명령·RED 묶음)
- ECB·Mock 점검

구현·테스트 코드 작성은 **`/red-skeleton`** 에서 한다.

---

## 입력 (추가 프롬프트 없이 자동 추출)

`/red-test-plan` 만 실행해도 동작한다. 아래 SSOT·채팅 맥락에서 **직접 읽어** 채운다.

| 소스 | 추출 항목 |
|------|-----------|
| **채팅·세션 Report/Transcript** | 세션 주제, 진행 중 Test Loop, 다음 RED 대상(S1/S2/S3·FR-T2 케이스) |
| **`docs/PRD.md`** | FR-R*·FR-C*·FR-S*·FR-T*, 성공 기준 S1~S3, Must Fix 시나리오 |
| **`.cursorrules`** | 4×4·34·10선(R1~R4,C1~C4,D1,D2)·`validate_lines` API·ECB·TDD 금지 |
| **기존 `tests/`·`src/`·`magicxx/`** | 이미 있는 테스트 ID·픽스처·함수명(중복·범위 creep 방지) |

**Test ID 명명:** `T-<기준>-<순번>` 또는 PRD 기준 `S1`/`S2`/`S3`/`FR-T2-<케이스>` — 채팅·PRD에서 **아직 RED가 없는** 항목 1건(또는 이번 RED 묶음)을 우선한다.

**기본값 (세션 3·명시 없을 때):**

| 항목 | 기본 |
|------|------|
| Layer | `entity` |
| Track | `Logic` |
| 대상 API | `validate_lines(grid)` |
| 겨냥 기준 | S1 → S2 → S3 순 (이미 RED된 항목은 스킵) |

---

## Track A / Track B

| Track | Layer | 범위 | 이 Command |
|-------|-------|------|------------|
| **B — Logic** | `entity` | 도메인·Skill (`validate_lines`, `verify_grid`, rules) | **기본** — 본문 그대로 사용 |
| **A — boundary** | `boundary` | CLI·입출력·exit code (`verify`, `format_failures`) | **Layer만 `boundary`로 바꾸면 재사용** — C2C는 FR-C*·FR-T2 인용, Track 표는 CLI/IO 함수 대상 |

---

## 수행 절차

1. SSOT·채팅에서 **세션 주제**·**다음 Test ID** 확정
2. 응답 **첫 줄**에 필수 선언 3종 출력
3. 아래 **출력 4블록**을 표 형식으로 작성 (코드 파일 생성 없음)
4. ECB·Mock 점검 통과 확인
5. 마지막 줄: `/red-skeleton 으로 넘길 준비됐다`

---

## 출력 4블록 (필수)

### 블록 1 — C2C (Rule1~3)

PRD FR을 **한 행 = 한 RED** 로 매핑한다.

| Rule | 열 | 내용 |
|------|-----|------|
| **Rule1** | PRD FR 인용 | `FR-R*` / `FR-S*` / `FR-T*` / S1~S3 중 해당 문구·ID |
| **Rule2** | To-Do 1개 | 이번 RED에서 검증할 **단일 행동** (동사 1문장) |
| **Rule3** | Test ID · Given / When / Then | ID + GWT 3줄 (격자·호출·기대 status·failed_lines) |

**예시 (S3·entity·Logic):**

| Rule1 (PRD FR) | Rule2 (To-Do) | Rule3 (Test ID · GWT) |
|----------------|---------------|------------------------|
| FR-R5 10개 조건 검증 · **S3** Must Fix · FR-T2 행·열 OK 주대각 NG | `validate_lines`가 D1 합 불일치를 `failed_lines`에 명시한다 | **T-S3-01** · **Given** 행·열 합 34·D1 합 31 격자 · **When** `validate_lines(grid)` · **Then** `status=="fail"`, `failed_lines`에 `line=="D1"`, `actual==31`, `expected==34` |

---

### 블록 2 — Track B 표 (Logic · entity)

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| (블록1과 동일 ID) | `validate_lines` 등 | 격자 조건 → 반환 키·값 | 변경 금지 계약 (API 시그니처, 10선 명명, MAGIC_SUM=34, status 3값) | pytest **FAILED** 유형 1줄 (`TypeError`, `AssertionError`, `KeyError` 등) |

- **Invariant:** RED에서도 흔들리면 안 되는 계약. assert 완화·시그니처 변경 금지 근거.
- **Expected RED Failure:** 현재 `src/`가 `...`/미구현일 때 **기대되는** 실패 (GREEN 목표 아님).

---

### 블록 3 — 테스트 플랜

| 항목 | 값 |
|------|-----|
| **파일 경로** | 예: `tests/test_validate_lines.py` (신규 시 **경로만** 기재, 파일 생성은 `/red-skeleton`) |
| **함수명** | 예: `test_s3_rows_cols_ok_main_diagonal_fail` |
| **conftest 픽스처** | 필요 시 이름·역할만 (예: `complete_magic`, `s3_main_diag_ng`). **검증 로직은 conftest 금지** |
| **공유 상수** | `MAGIC_SUM = 34` — 테스트 파일 또는 이후 `src/rules.py` SSOT (플랜만 명시) |
| **pytest 명령** | `python -m pytest <경로>::<함수명> -v` |
| **RED 묶음 범위** | 이번에 추가할 테스트 **1개(또는 1 시나리오)** · 겨냥 S1/S2/S3·FR-T2 케이스 ID |

---

### 블록 4 — ECB · Mock 점검

| 계층 | Logic Track (`entity`) | boundary Track (`boundary`) |
|------|------------------------|----------------------------|
| **Event** | 테스트에서 CLI·stdin·파일 IO **직접 호출 금지** | CLI·IO Mock **허용** (도메인 Mock 아님) |
| **Condition** | `validate_lines` / `verify_grid` **실제 호출** | 경계는 Skill을 stub 할 수 있음 — **Domain 전체 Mock 금지** |
| **Behavior** | `status`·`failed_lines` (또는 `VerifyResult`) **실값 assert** | exit code·stdout 포맷 assert |
| **Domain Mock** | **금지** — 격자·합 34·10선은 **픽스처 리터럴** | Skill 일부 stub 시에도 **10선 합산 로직 Mock 금지** |
| **E001~E005 emit** | **금지** — 구조 오류 Event 코드를 Logic 테스트에서 기대·발생시키지 않음 | boundary 전용 입력 오류 테스트에서만 해당 (별도 Test ID) |

**E001~E005 (Event · 입력 오류 — Logic Track에서 emit·assert 금지):**

| 코드 | 의미 | Logic Track |
|------|------|-------------|
| E001 | 격자 크기 ≠ 4×4 | emit 금지 |
| E002 | 1~16 중복 | emit 금지 |
| E003 | 빈칸(`0`) 3개 이상 | emit 금지 |
| E004 | 1~16 범위 밖 값 | emit 금지 |
| E005 | 파싱·입력 형식 오류 | emit 금지 |

> 구조 오류는 `validate_lines` **입력 전** 별도 검증(`.cursorrules`). Logic RED는 **유효 격자** 위 10선 판정만 겨냥한다.

---

## 보고 형식 (응답 전체 골격)

```
Phase: red | Layer: entity | Track: Logic

## 1. C2C (Rule1~3)
| Rule1 | Rule2 | Rule3 |
...

## 2. Track B
| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
...

## 3. 테스트 플랜
| 항목 | 값 |
...

## 4. ECB · Mock 점검
(표 + E001~E005 Logic 금지 확인)

/red-skeleton 으로 넘길 준비됐다
```

---

## 금지 (본 Command)

| 금지 | 이유 |
|------|------|
| `tests/`·`src/` **파일 생성·수정** | Ask 단계는 설계만 |
| **GREEN / REFACTOR** 진행 | `/red-skeleton`·`/tdd-red` 이후 |
| `assert` 완화·**skip**·**xfail**·테스트 삭제 제안 | RED 요구사항 희석 |
| Solver·힌트·n×n·GUI 등 **Out of Scope** | PRD·`.cursorrules` |
| Logic Track **Domain Mock** | Condition 실검증 원칙 |
| Logic Track **E001~E005 emit** | Event 계층은 boundary 입력 오류 전용 |

---

## RED Test Plan 체크리스트

- [ ] 응답 첫 줄: `Phase: red | Layer: … | Track: …`
- [ ] 세션 주제·Test ID를 채팅·PRD에서 추출 (추가 질문 없이)
- [ ] 블록 1~4 표 **4개** 모두 작성
- [ ] C2C 행 = RED 1건(또는 명시한 묶음) — To-Do 1개씩
- [ ] Track B **Expected RED Failure** 명시
- [ ] pytest 명령·RED 묶음 범위 포함
- [ ] ECB·Mock 점검 — Logic 시 Domain Mock·E001~E005 금지 확인
- [ ] `tests/`·`src/` **미생성** 확인
- [ ] 마지막 줄: `/red-skeleton 으로 넘길 준비됐다`

---

## 다음

| Command | 역할 |
|---------|------|
| **`/red-skeleton`** | 블록 3 플랜대로 `tests/` 스켈레ton·RED 테스트 **코드** 작성 |
| **`/tdd-red`** | RED 실행·pytest FAILED 확인·보고 |
