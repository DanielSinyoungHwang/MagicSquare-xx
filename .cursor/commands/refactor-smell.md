# Refactor Smell — ARRR R단계 (Refine ⑦)

> **Phase: refactor**  
> **Scope: src/ tests/**  
> **Track: Logic + UI**  
> 코드 **스멜 탐지만** 수행한다. **수정·commit 금지.**

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** (스멜 분류·Change Budget·ECB 규칙 SSOT).

---

## 목적

ARRR **R(Refine)** 단계 **⑦** — 전체 테스트 GREEN 상태에서 **리팩터 후보만** 식별한다.

- `src/`·`tests/`·`entity/`·`magicxx/` **읽기 전용** 분석
- 스멜 표(P0/P1/P2) + `/refactor-safe` 에 넘길 후보 **1~3개**
- 실제 변경은 **`/refactor-safe`** (P0 **1개**만) 에서

---

## 전제 (미충족 시 중단)

```bash
python -m pytest tests/ -v
```

| 조건 | 미충족 시 |
|------|-----------|
| **전체 PASS** | **즉시 중단** — 실패 목록만 보고, 스멜 분석 **하지 않음** |
| **골든 matched** | golden 사용 중이면 `UPDATE_GOLDEN` 없이 approval PASS 권장 |

중단 메시지: `pytest 실패 — /green-minimal 또는 회귀 수정 후 재실행`

---

## 입력 (추가 프롬프트 없이)

| 소스 | 사용 |
|------|------|
| **`src/`·`entity/`·`tests/`·`magicxx/`** | 스멜 후보 탐색 |
| **`.cursorrules`·PRD** | ECB·상수 SSOT·Out of Scope 경계 |
| **직전 GREEN·golden 보고** | 최근 수정 파일·Test ID 우선 검토 |
| **`magic-square-tdd` Skill** | 있으면 스멜 정의·우선순위 우선 |

---

## 수행 절차

| 단계 | 할 일 |
|------|--------|
| **1** | `python -m pytest tests/ -v` 실행 → **전부 PASS** 확인 |
| **2** | Scope 내 파일 스캔 — 스멜 유형별 후보 수집 |
| **3** | P0/P1/P2·Change Budget 적합성 평가 |
| **4** | 스멜 표 출력 + `/refactor-safe` 후보 **1~3개** (P0 우선) |
| **5** | 다음 안내: **P0 1개** 골라 `/refactor-safe` 실행 |

**코드 수정·파일 생성·삭제·git commit — 금지.**

---

## 스멜 유형 (탐지 대상)

| 유형 | 설명 | MagicSquare_xx 예시 |
|------|------|---------------------|
| **Long Method** | 한 함수가 Arrange·Act·Assert·포맷·IO를 과다 담당 | `_format_golden_output` + assert 혼재 |
| **Duplicated Code** | 동일 10선 합산·격자 복사·상수 리터럴 반복 | `validate_lines` vs `verify_grid` 중복 |
| **Mysterious Name** | `f`, `md`, `flag`, `v1` 등 의도 불명 | golden `int[6]` 필드명 미설명 |
| **Magic Number** | `34`·`16`·`4`·`0` 리터럴 (constants 미사용) | 테스트·`src/` 잔존 리터럴 |
| **ECB 위반** | entity→boundary import, Condition에 Event/E00x, conftest 검증 로직 | `src/`에서 `magicxx.cli` 참조 |
| **Feature Envy** | A가 B의 데이터·필드를 과다 조작 | 테스트가 `result` 내부를 깊게 파고듦 |

---

## 우선순위 (P0 / P1 / P2)

| 등급 | 기준 | 예 |
|------|------|-----|
| **P0** | 테스트 깨질 위험·ECB 침범·회귀(S3) 위협·Magic Number SSOT 위반 | entity가 E001 emit, `34` 하드코딩 in `src/` |
| **P1** | Duplicated Code·Long Method — 동작은 맞으나 유지보수 부담 | 10선 루프 이중 구현 |
| **P2** | Mysterious Name·미세 정리·주석 부족 | 변수명만 모호 |

---

## Change Budget (`/refactor-safe` 예산 — 탐지 시 참고)

한 번의 safe refactor 에 **넘길 후보 1건**이 이 예산에 들어가야 한다.

| 항목 | 상한 |
|------|------|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

예산 초과 후보는 표에 기재하되 `/refactor-safe` 후보에서 **제외** 또는 분할 제안.

---

## 스멜 표 (출력 필수)

| P | 스멜 | 위치 (파일:심볼) | 근거 1줄 | Budget OK? | /refactor-safe 후보 |
|---|------|------------------|----------|------------|---------------------|
| P0 | Magic Number | `src/validate_lines.py` | `34` 리터럴, `entity.constants` 미사용 | ✅ 파일1·메서드1 | **#1** |
| P1 | Duplicated Code | `src/` ↔ `magicxx/verify.py` | 10선 합산 로직 중복 | ❌ 파일4 | — |
| P2 | Mysterious Name | `tests/…::test_*` | `flag` 의미 불명 | ✅ | #2 |

- 행 수: 발견분 전부 (보통 3~10)
- **후보 열:** `/refactor-safe` 에 넘길 항목만 **#1~#3** (P0 우선, Budget OK 우선)

---

## `/refactor-safe` 후보 (1~3개)

각 후보 블록:

```
### 후보 #1 (P0 · Magic Number)
- 위치: src/validate_lines.py :: validate_lines
- 스멜: Magic Number
- 제안 방향: MAGIC_SUM 등 entity.constants import (동작 변경 없음)
- Change Budget: 파일 1 · 클래스 0 · 메서드 1
- 회귀: python -m pytest tests/ -v
```

후보는 **1~3개**. P0가 없으면 P1에서 1개 — **수정은 하지 않음**.

---

## 보고 형식

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## pytest 전제
- PASSED — python -m pytest tests/ -v (N passed)

## 스멜 표
| P | 스멜 | 위치 | 근거 | Budget OK? | 후보 |
...

## /refactor-safe 후보
- #1 …
- #2 … (있으면)
- #3 … (있으면)

## 다음
- P0 후보 #1 (또는 표시한 번호) 1개만 골라 `/refactor-safe` 실행
- 코드 수정·commit은 본 Command에서 하지 않음
```

---

## 금지 (본 Command)

| 금지 | 이유 |
|------|------|
| **코드·테스트·golden 수정** | 탐지만 — Refine ⑦ |
| **git commit·push** | `/refactor-safe` 이후·사용자 요청 시 |
| **assert 완화·skip·xfail** | 스멜 우회 |
| **pytest 실패 상태에서 스멜 분석** | 전제 위반 |
| **Out of Scope 리팩터 제안** | Solver·n×n·GUI 등 |
| **한 번에 P0 여러 개 수정 제안을 실행** | `/refactor-safe` = P0 **1개** |

---

## Refactor Smell 체크리스트

- [ ] 응답 첫 줄: `Phase: refactor | Scope: src/ tests/ | Track: Logic+UI`
- [ ] `python -m pytest tests/ -v` **전부 PASS** (아니면 중단)
- [ ] 스멜 표 — P0/P1/P2 · 6유형 반영
- [ ] Change Budget 열 또는 후보에 예산 명시
- [ ] `/refactor-safe` 후보 **1~3개** (P0 우선)
- [ ] 다음: **P0 1개** 골라 `/refactor-safe`
- [ ] **코드 수정·commit 없음**

---

## Command 흐름

| 순서 | Command | 산출 |
|------|---------|------|
| ⑥ | `/green-minimal` | PASS |
| ⑦ | `/golden-master` | matched (선택) |
| ⑧ | **`/refactor-smell`** | 스멜 표 · safe 후보 (읽기만) |
| ⑨ | `/refactor-safe` | P0 1개 · Budget 내 수정 · pytest PASS |
