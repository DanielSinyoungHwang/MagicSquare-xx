# MagicSquare_xx

4×4 **부분 마방진**(빈칸 2개, 합 34) 학습자가 풀이 후 **행·열·대각선 10개 조건**을 빠짐없이 검증하는 도구.

> **풀기가 아니라, 풀었는지 — 특히 대각선까지 — 맞는지 확인한다.**

---

## 왜 이 프로젝트인가 (Mom Test)

| | |
|---|---|
| **페르소나** | 4×4 부분 마방진을 손·코드·ECB로 다루는 **학습자** |
| **진짜 문제** | 빈칸 2개를 채우고 행·열은 맞다고 믿은 뒤, **주대각선 검증을 마지막에야** 하다가 틀림을 알아 **약 20분짜리 작업 전체를 늦게 재판정·수정**해야 했다 |
| **하지 않는 것** | 자동 풀이, Solver, 34 계산기, 튜토리얼 앱 (표면 문제) |

**증거 3줄**

1. "사진처럼 ECB 작업을 했는데 **어려움이 있었어**."
2. "**대각선 1개 확인을 놓쳤었고**, **20분 뒤 마지막에** 알았어."
3. "주대각선 확인 전까지 **행·열은 다 맞다고 생각**했고, **검증하다가** 틀렸다는 걸 알았어."

---

## 성공 기준 (v0.1)

| ID | 기준 |
|----|------|
| **S1** | 행4 + 열4 + 대각2 = **10개 조건 일괄 점검** |
| **S2** | 실패 시 `main_diagonal sum=32 expected=34`처럼 **조건명·실제합·기대합** 출력 |
| **S3** | **행·열 OK + 대각선 NG** → 즉시 FAIL (Mom Test 회귀 케이스) |

---

## 문서

| 문서 | 설명 |
|------|------|
| [`docs/PRD.md`](docs/PRD.md) | 제품 요구사항 (v0.1) |
| [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md) | 문제 정의·R-G-I-O·성공 기준 |
| [`Report/01.Mom-Test-STEP1-Report.md`](Report/01.Mom-Test-STEP1-Report.md) | Mom Test STEP 1 인터뷰 보고서 |
| [`Prompting/01.Mom-Test-STEP1-Transcript.md`](Prompting/01.Mom-Test-STEP1-Transcript.md) | 인터뷰 Transcript |

---

## 8계층 스코프 (세션 3)

```
Rule → Command → (Skill) → Test Loop
```

| 계층 | v0.1 | 내용 |
|------|------|------|
| Rule | ✅ | 4×4, 합 34, 1~16 각 1회, 빈칸 `0` 최대 2 |
| Command | ✅ | `verify` — 격자 입력 → 10개 조건 pass/fail |
| Skill | ✅ | `verify_grid(...)` 재사용 API |
| Test Loop | ✅ | pytest, S3 회귀 우선 |
| UI / Workflow / Agent / Product | — | 이후 세션 |

---

## 사용 예 (계획)

구현 전 예상 인터페이스. Mom Test **S3** 시나리오: 행·열은 34인데 주대각선만 틀린 격자.

```bash
# stdin으로 4×4 격자 입력 (S3 — 행·열 OK, 주대각선 NG)
python -m magicxx verify << 'EOF'
13  3  2 16
 8 10 11  5
 9  6  7 12
 4 15 14  1
EOF
```

**기대 출력 (S2·S3):**

```
FAIL main_diagonal sum=31 expected=34
FAIL anti_diagonal sum=37 expected=34
```

완성 마방진이면:

```
OK
```

---

## 요구 사항

- Python 3.10+
- 외부 의존성 최소 (stdlib 우선)

---

## 설치·테스트

```bash
pip install -e ".[dev]"   # 또는: pip install pytest && pip install -e .
pytest
```

## 상태

**v0.1** — Rule + Command + Skill + Test Loop (S1·S2·S3) 구현 완료.
