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

## 성공 기준

| ID | 기준 |
|----|------|
| **S1** | 행4 + 열4 + 대각2 = **10개 조건 일괄 점검** |
| **S2** | 실패 시 `main_diagonal sum=31 expected=34`처럼 **조건명·실제합·기대합** 출력 |
| **S3** | **행·열 OK + 대각선 NG** → 즉시 FAIL (Mom Test 회귀 케이스) |

---

## 상태 (v0.2)

| 트랙 | 구현 | S1 | S2 | S3 | 테스트 |
|------|------|----|----|-----|--------|
| **CLI** `magicxx verify` | ✅ | ✅ | ✅ | ✅ | `test_verify.py` 10/10 |
| **Skill** `validate_lines` | 🔄 TDD RED | — | — | — | `test_validate_lines.py` 0/1 |

- **지금 쓸 수 있는 것:** `python -m magicxx verify` — S1~S3 충족
- **진행 중:** `src/validate_lines.py` — 세션 3 TDD 대상 (Canonical API)

---

## 빠른 시작

### 설치

```bash
pip install -e ".[dev]"
```

- Python 3.10+
- 런타임: stdlib만 / 개발: pytest

### 사용 예 — S3 (행·열 OK, 대각선 NG)

격자 파일 `grid.txt`:

```text
13  3  2 16
 8 10 11  5
 9  6  7 12
 4 15 14  1
```

```bash
python -m magicxx verify grid.txt
```

**출력:**

```text
FAIL main_diagonal sum=31 expected=34
FAIL anti_diagonal sum=37 expected=34
```

완성 마방진이면 `OK`, exit code `0`. 합 불일치는 `1`, 입력 오류는 `2`.

stdin 입력 (bash):

```bash
python -m magicxx verify << 'EOF'
16  3  2 13
 5 10 11  8
 9  6  7 12
 4 15 14  1
EOF
```

### Python API

```python
from magicxx.verify import verify_grid, format_failures

result = verify_grid([[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]])
print(result.ok)  # True
```

세션 3 Canonical API (TDD 진행 중):

```python
from src.validate_lines import validate_lines

result = validate_lines(grid)  # {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}
```

---

## 도메인 규칙

| 규칙 | 값 |
|------|-----|
| 격자 | 4×4 고정 |
| 마법상수 | 34 |
| 숫자 | 1~16, 각 1회 |
| 빈칸 | `0`, 최대 2개 |
| 검증 대상 | 행 4 + 열 4 + 대각 2 = **10선** |
| 빈칸 포함 선 | 합 검증 skip → `incomplete` |

자동 풀이·Solver·힌트·n×n 일반화는 **Out of Scope**.

---

## 8계층 스코프 (세션 3)

```
Rule → Command → Skill → Test Loop
```

| 계층 | v0.2 | 산출물 |
|------|------|--------|
| Rule | ✅ | `magicxx/rules.py` |
| Command | ✅ | `magicxx/cli.py` — `verify` |
| Skill | 🔄 | `verify_grid` ✅ · `validate_lines` RED |
| Test Loop | 🔄 | `test_verify` 10/10 · `test_validate_lines` 0/1 |
| UI / Workflow / Agent / Product | — | 이후 세션 |

---

## 프로젝트 구조

```text
magicxx/          # CLI + verify_grid (사용 가능)
src/              # validate_lines (TDD 대상)
tests/            # pytest
docs/PRD.md       # 제품 요구사항 (SSOT)
Report/           # 세션 보고서
Prompting/        # 세션 Transcript
```

---

## 테스트

```bash
python -m pytest tests/ -v
```

---

## 문서

| 문서 | 설명 |
|------|------|
| [`docs/PRD.md`](docs/PRD.md) | 제품 요구사항 (v0.2, SSOT) |
| [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md) | 문제 정의·R-G-I-O·성공 기준 |
| [`Report/01.Mom-Test-STEP1-Report.md`](Report/01.Mom-Test-STEP1-Report.md) | Mom Test STEP 1 인터뷰 보고서 |
| [`Report/02.Session3-TDD-RED-Report.md`](Report/02.Session3-TDD-RED-Report.md) | `validate_lines` TDD RED 세션 |
| [`Prompting/01.Mom-Test-STEP1-Transcript.md`](Prompting/01.Mom-Test-STEP1-Transcript.md) | Mom Test Transcript |
| [`Prompting/02.Session3-TDD-RED-Transcript.md`](Prompting/02.Session3-TDD-RED-Transcript.md) | 세션 3 TDD Transcript |
