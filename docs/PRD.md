# MagicSquare_xx — PRD (Product Requirements Document)

**버전:** 0.2  
**작성일:** 2026-06-10  
**상태:** 세션 3 — Rule·Command·Skill·Test Loop (Dual-Track)  
**SSOT:** 본 문서 + `.cursorrules` (충돌 시 이 둘 우선)

**근거 문서**

| 문서 | 역할 |
|------|------|
| `Report/01.Mom-Test-STEP1-Report.md` | Mom Test STEP 1 인터뷰 |
| `Report/01.MagicSquare_ProblemDefinition_Report.md` | 문제 정의·R-G-I-O |
| `Report/02.Session3-TDD-RED-Report.md` | `validate_lines` TDD RED 세션 |
| `Prompting/01.Mom-Test-STEP1-Transcript.md` | 인터뷰 원문 |
| `Prompting/02.Session3-TDD-RED-Transcript.md` | 세션 3 TDD Transcript |

---

## 1. 개요

### 1.1 한 줄 요약

4×4 부분 마방진(빈칸 2, 합 34) 학습자가 풀이 후 **행·열·대각선 10개 조건**을 빠짐없이 검증하고, **어느 조건이 실패했는지** 즉시 알 수 있는 **검증 도구**를 만든다.

> **풀기가 아니라, 풀었는지 — 특히 대각선까지 — 맞는지 확인한다.**

### 1.2 배경 (Mom Test STEP 1)

| 항목 | 내용 |
|------|------|
| 페르소나 | 4×4 **부분 마방진**을 손·코드·ECB로 다루는 **학습자** (빈칸 2·합 34) |
| 표면 문제 | “4×4 부분 마방진이 어려워서 **자동 풀이·Solver 앱·34 계산기·검증 CLI**가 있으면 좋겠다” — 솔루션을 문제로 착각 |
| 진짜 문제 | 빈칸 2개를 채우고 행·열은 맞다고 믿은 뒤, **주대각선 검증을 마지막에야** 하다가 틀림을 알아 **약 20분짜리 작업 전체를 늦게 재판정·수정**해야 했다 |
| 증거 ① | "사진처럼 ECB 작업을 했는데 **어려움이 있었어**." |
| 증거 ② | "**대각선 1개 확인을 놓쳤었고**, **20분 뒤 마지막에** 알았어." |
| 증거 ③ | "주대각선 확인 전까지 **행·열은 다 맞다고 생각**했고, **검증하다가** 틀렸다는 걸 알았어." |

### 1.3 보조 사실 (인터뷰)

| 사실 | 프로젝트 범위 |
|------|---------------|
| 풀이+ECB+검증 **합쳐 약 20분** | 검증 늦은 재판정 비용의 근거 |
| 알게 된 뒤 **고쳐서 맞춤** (당일 포기 아님) | 검증 도구가 **수정 전**에 개입해야 함 |
| 행·열 OK + 대각선 NG 패턴 **이번이 처음** | S3 회귀 케이스 우선순위 |
| 20분 중 **가장 긴 구간: 빈칸 채우기** (합 34 손계산) | **Out of Scope** — 본 프로젝트는 검증만 다룸 |

### 1.4 이번 버전에서 하지 않음

- 자동 풀이, Solver, 힌트, 34 맞추기 계산기
- 튜토리얼·설명 UI·강의 앱
- n×n 일반화, 문제 생성, 게임화
- GUI, 공유·저장, SNS

---

## 2. 목표 및 성공 기준

### 2.1 제품 목표

학습자가 채운 4×4 격자에 대해 **모든 마방진 조건(10개)** 을 한 번에 점검하고, **어느 조건이 실패했는지** 즉시 파악한다. 특히 **행·열 OK + 대각선 NG** 패턴을 늦게 발견하지 않도록 한다.

### 2.2 성공 기준

| ID | 기준 | Mom Test 연결 | 검증 방법 |
|----|------|---------------|-----------|
| **S1** | 10개 조건(행4+열4+대각2) **일괄 점검** | 증거 ① — ECB·확인 단계 **어려움** | 단일 호출 1회 |
| **S2** | 실패 시 **조건명 + 실제합 + 기대합(34)** 출력 | 증거 ② — **20분 뒤** 알았던 대각선 → 조건별 즉시 식별 | `failed_lines` / `format_failures` 테스트 |
| **S3** | 행·열 OK + **주대각(또는 부대각) NG** → **즉시 FAIL** | 증거 ③ — 행·열 OK 착각 후 **검증 중** 발견 → 즉시 차단 | 회귀 테스트 케이스 |

**세션 3 Done:** S1·S2·S3을 Test Loop로 자동 검증 가능할 때.

### 2.3 구현 현황 (2026-06-10)

| 트랙 | API / 진입점 | S1 | S2 | S3 | pytest |
|------|--------------|----|----|-----|--------|
| **Track B — Logic** | `src/validate_lines.validate_lines` | RED (1건 실패) | 미착수 | 미착수 | `test_validate_lines.py` 0/1 |
| **Track A — Command** | `magicxx.verify.verify_grid` + CLI | ✅ | ✅ | ✅ | `test_verify.py` 10/10 |

- **Canonical API (SSOT):** `validate_lines(grid)` — 세션 3 TDD 대상
- **기존 구현:** `magicxx/` 패키지 — S1~S3 충족, CLI `verify` 동작
- **다음:** `validate_lines` GREEN → S2·S3 RED 추가 → 필요 시 `magicxx`와 명명·동작 정렬

---

## 3. 사용자 및 시나리오

### 3.1 Primary User

4×4 부분 마방진을 **손으로 풀거나 코드·ECB로 다루는 학습자**

### 3.2 핵심 시나리오

1. 학습자가 빈칸 2개를 채운(또는 채우는 중인) 4×4 격자를 준비한다.
2. `verify` Command 또는 `validate_lines` / `verify_grid`로 격자를 입력한다.
3. **행 4 + 열 4 + 대각선 2** 조건 각각 pass/fail/incomplete를 확인한다.
4. fail이 있으면 **어느 행·열·대각선**인지 보고 수정한다.
5. 전부 pass면 풀이 완료로 판단한다.

### 3.3 대표 실패 시나리오 (Must Fix — S3)

- 행·열 합은 모두 34이나 **주대각선 또는 부대각선** 합이 34가 아님  
  → **즉시** NG, 해당 대각선 명시 (Mom Test: 20분 뒤가 아닌 **검증 즉시**)

**S3 픽스처 (공통):**

```text
13  3  2 16
 8 10 11  5
 9  6  7 12
 4 15 14  1
```

- 행·열: pass (합 34)
- 주대각선(D1 / `main_diagonal`): actual=31, expected=34 → **FAIL**
- 부대각선(D2 / `anti_diagonal`): actual=37, expected=34 → **FAIL**

---

## 4. R-G-I-O

| | 요구사항 |
|---|----------|
| **Role** | 학습자 — ECB·손풀이 후 self-check |
| **Goal** | 10개 조건 전수 검증 + 실패 위치 식별 |
| **Input** | 4×4 정수 배열. 값域: `0`(빈칸, 최대 2) 또는 `1~16`(각 1회) |
| **Output** | 전체 OK/NG/incomplete, 조건별 상세 (이름, pass/fail/incomplete, sum, expected=34) |

---

## 5. 도메인 규칙 (Rule)

| ID | 규칙 | 상수·비고 |
|----|------|-----------|
| **FR-R1** | 4×4 격자만 지원 | `GRID_SIZE = 4` |
| **FR-R2** | Magic constant = **34** | `MAGIC_SUM = 34` |
| **FR-R3** | 사용 숫자: **1~16**, 각 숫자 최대 1회 | `MIN_VALUE=1`, `MAX_VALUE=16` |
| **FR-R4** | 빈칸: **`0`**, 최대 **2개** | `BLANK=0`, `MAX_BLANKS=2` |
| **FR-R5** | 검증 대상 **10선** (아래 표) | — |
| **FR-R6** | `0`이 포함된 선은 합 검증 **skip** → `incomplete` | 빈칸 있는 선은 fail 아님 |

### 5.1 10선 명명 (Dual-Track)

| # | `validate_lines` (SSOT) | `magicxx` (기존) | 방향 |
|---|-------------------------|------------------|------|
| 1 | R1 | row_0 | ↘ 행 |
| 2 | R2 | row_1 | |
| 3 | R3 | row_2 | |
| 4 | R4 | row_3 | |
| 5 | C1 | col_0 | ↓ 열 |
| 6 | C2 | col_1 | |
| 7 | C3 | col_2 | |
| 8 | C4 | col_3 | |
| 9 | D1 | main_diagonal | 주대각 ↘ |
| 10 | D2 | anti_diagonal | 부대각 ↙ |

### 5.2 구조 오류 (validate_lines 입력 전 별도 검증)

`validate_lines` / `verify_grid` 호출 **전** 또는 **내부 1차**에서 처리. 합 검증과 분리.

| 코드 | 조건 | `magicxx` 메시지 예 |
|------|------|---------------------|
| E001 | 크기 ≠ 4×4 | `grid must be 4×4` |
| E002 | 1~16 중복 | `duplicate values: …` |
| E003 | 빈칸 ≥ 3 | `too many blanks: …` |
| E004 | 값 범위 밖 | `value … out of range 1..16` |
| E005 | 파싱 오류 (CLI) | `ERROR expected 16 integers, …` |

구조 오류 시 `validate_lines`는 호출하지 않거나, `verify_grid`는 `grid_valid=False` 반환.

---

## 6. API 명세

### 6.1 Skill — `validate_lines` (Canonical, Track B)

```python
validate_lines(grid: list[list[int]]) -> dict
# 반환:
# {
#   "status": "pass" | "fail" | "incomplete",
#   "failed_lines": [
#     {"line": "R1"|"R2"|…|"D2", "actual": int, "expected": 34},
#     ...
#   ]
# }
```

| `status` | 조건 |
|----------|------|
| `pass` | 10선 모두 합 34 (빈칸 없는 완성판) |
| `fail` | 1선 이상 합 ≠ 34. `failed_lines`에 불일치 선만 |
| `incomplete` | 빈칸 때문에 일부 선 skip. `failed_lines`는 합 불일치 선만 |

- **구현 위치:** `src/validate_lines.py` (현재 시그니처만, GREEN 대기)
- **테스트:** `tests/test_validate_lines.py`

### 6.2 Skill — `verify_grid` (기존, Track B 병행)

```python
verify_grid(grid) -> VerifyResult
# VerifyResult: grid_valid, ok, conditions, errors
# ConditionResult: name, status(PASS|FAIL|INCOMPLETE), actual_sum, expected_sum
```

- **구현 위치:** `magicxx/verify.py`, 상수 `magicxx/rules.py`
- **테스트:** `tests/test_verify.py` — S1~S3 **통과**

### 6.3 Command — CLI `verify` (Track A)

| ID | 요구 |
|----|------|
| **FR-C1** | 진입: `magicxx verify` 또는 `python -m magicxx verify` |
| **FR-C2** | 입력: 파일 경로 또는 stdin (`-` 생략 시 stdin). 16개 정수, 공백/쉼표 구분 |
| **FR-C3** | 출력: `OK` 또는 `FAIL {condition} sum={actual} expected=34` (한 줄씩) |
| **FR-C4** | Exit code: `0`=OK, `1`=FAIL(합·구조), `2`=입력·파싱 오류 |

**사용 예 (S3):**

```bash
python -m magicxx verify << 'EOF'
13  3  2 16
 8 10 11  5
 9  6  7 12
 4 15 14  1
EOF
```

**기대 출력:**

```text
FAIL main_diagonal sum=31 expected=34
FAIL anti_diagonal sum=37 expected=34
```

---

## 7. ECB 패턴

| 계층 | 책임 | 산출물 | 구현 |
|------|------|--------|------|
| **Event** | 격자 입력·검증 호출 | CLI / 테스트 픽스처 | `magicxx/cli.py`, `tests/*` |
| **Condition** | 10선 합 = 34?, 빈칸 skip? | `validate_lines` / `verify_grid` 판정 | `src/validate_lines.py`, `magicxx/verify.py` |
| **Behavior** | OK / FAIL 목록 / incomplete | `{status, failed_lines}` 또는 `VerifyResult` | 출력·assert |

- Mom Test **S3** 회귀: 행·열 PASS + D1(또는 D2) FAIL → `status=fail`, 실패 선 명시

---

## 8. Test Loop (TDD)

### 8.1 원칙

1. **RED** → **GREEN** → **REFACTOR** 순서 고정
2. RED: **`tests/`만** 수정. `src/` 구현 금지
3. **금지:** `assert` 완화, `skip`, `xfail`, 테스트 삭제로 GREEN 만들기
4. RED 1묶음 → GREEN 최소 구현 → REFACTOR (동작 유지)

### 8.2 필수 테스트 케이스

| 케이스 | 기대 | Mom Test | `test_verify` | `test_validate_lines` |
|--------|------|----------|---------------|----------------------|
| 완성 마방진 (빈칸 없음) | pass / OK | — | ✅ | RED (S1) |
| **행·열 OK, 주대각 NG** | fail + D1/main_diagonal | **S3** | ✅ | — |
| 행·열 OK, 부대각 NG | fail + D2/anti_diagonal | S3 확장 | ✅ | — |
| 1~16 중복 | 구조 오류 | — | ✅ | — |
| `0` 3개 이상 | 구조 오류 | — | ✅ | — |
| 빈칸 2개 중간판 | incomplete (0 포함 선 skip) | — | ✅ | — |
| S2 출력 포맷 | `sum=… expected=34` | **S2** | ✅ | RED 예정 |

### 8.3 Dual-Track 매핑

| | **Track B — Logic** | **Track A — UI (boundary)** |
|---|---------------------|----------------------------|
| 대상 | `validate_lines`, `verify_grid` | CLI `verify`, stdin/stdout |
| C2C Rule1 | FR-R*, FR-S*, S1~S3 | FR-C*, FR-T2 |
| 테스트 | 도메인 실호출 | IO·exit code |

---

## 9. 비기능 요구사항

| ID | 요구 |
|----|------|
| NFR-1 | Python 3.10+ |
| NFR-2 | 외부 의존성 최소 (stdlib + pytest dev) |
| NFR-3 | 단일 격자 검증 < 1초 |
| NFR-4 | README에 사용 예 1개 |
| NFR-5 | 응답·주석·커밋 메시지 한국어 (AI 작업 규칙) |

---

## 10. 8계층 로드맵

```
[세션 3]  Rule → Command → Skill → Test Loop
[이후]    UI → Workflow → Agent → Product
```

| 계층 | v0.2 | 산출물 |
|------|------|--------|
| **Rule** | ✅ | `magicxx/rules.py` — 4×4, 합 34, 1~16, 빈칸 0 최대 2 |
| **Command** | ✅ | `magicxx/cli.py` — `verify` |
| **Skill** | 🔄 | `verify_grid` ✅ · `validate_lines` RED |
| **Test Loop** | 🔄 | `test_verify` 10/10 · `test_validate_lines` 0/1 |
| UI | — | 세션 4+ |
| Workflow | — | — |
| Agent | — | — |
| Product | — | — |

---

## 11. 마일스톤

| 단계 | 산출물 | Done 조건 | 상태 |
|------|--------|-----------|------|
| M0 | Mom Test STEP 1 · 문제 정의 | 증거 3줄·R-G-I-O | ✅ |
| M1 | Rule + 테스트 스켈레ton | 10선 이름·expected sum 정의 | ✅ |
| M2 | verify Command MVP | **S1** (`verify_grid`) | ✅ |
| M3 | fail 메시지 상세화 | **S2** (`format_failures`) | ✅ |
| M4 | 행·열 OK + 대각선 NG 회귀 | **S3** (`test_verify`) | ✅ |
| M5 | `validate_lines` S1 GREEN | `test_complete_grid_all_ten_lines_pass` PASS | 🔄 RED |
| M6 | `validate_lines` S2·S3 RED→GREEN | `failed_lines` 상세 + D1 FAIL 회귀 | ⏳ |
| M7 | API 정렬·REFACTOR | 명명·동작 SSOT 통일 (선택) | ⏳ |

---

## 12. 프로젝트 구조

```text
MagicSquare_xx/
├── docs/PRD.md              # 본 문서 (SSOT)
├── magicxx/                 # Track A+B — 패키지 (S1~S3 완료)
│   ├── rules.py             # 도메인 상수
│   ├── verify.py            # verify_grid Skill
│   └── cli.py               # verify Command
├── src/
│   └── validate_lines.py    # Track B — Canonical Skill (TDD 대상)
├── tests/
│   ├── test_verify.py       # magicxx 회귀 (10건)
│   └── test_validate_lines.py  # validate_lines TDD (1건 RED)
├── Report/                  # 세션 보고서
├── Prompting/               # 세션 Transcript
└── .cursorrules             # 도메인·TDD·AI 규칙
```

**설치·테스트:**

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v
```

---

## 13. 리스크 및 가정

| 리스크 | 대응 |
|--------|------|
| `validate_lines` vs `verify_grid` 이중 API | PRD에서 Canonical=`validate_lines` 명시; 점진적 정렬 |
| 빈칸 있는 중간판 정책 | `incomplete` + 0 포함 선 skip — `test_verify`로 확정 |
| 10선 명명 불일치 (R1 vs row_0) | §5.1 매핑표 유지; REFACTOR 시 통일 검토 |
| 범위 creep (자동 풀이·Solver 등) | §1.4 Out of Scope 고정 |
| Mom Test 표본 1명 | v0.2는 본인 학습자 페르소나·STEP 1 증거 검증용 |

**가정:** 학습자는 4×4 마방진 규칙(합 34)을 이미 알고 있다.

---

## 14. 참고 문서

| 문서 | 설명 |
|------|------|
| `README.md` | 프로젝트 소개·사용 예·상태 |
| `Report/01.MagicSquare_ProblemDefinition_Report.md` | 문제 정의·8계층 |
| `Report/01.Mom-Test-STEP1-Report.md` | Mom Test 인터뷰 보고서 |
| `Report/02.Session3-TDD-RED-Report.md` | TDD RED 세션 Export |
| `Prompting/01.Mom-Test-STEP1-Transcript.md` | Mom Test Transcript |
| `Prompting/02.Session3-TDD-RED-Transcript.md` | 세션 3 TDD Transcript |
| `.cursorrules` | 도메인·API·ECB·TDD 규칙 |
| `.cursor/skills/magic-square-tdd/SKILL.md` | TDD·Dual-Track·Command 체인 |
| `.cursor/skills/magic-square-docs/SKILL.md` | Report·Transcript Export |
