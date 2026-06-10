# Phase Checklist — magic-square-docs

Export 전·후 확인. `/export-session` + `phase-checklist.md` 동시 적용.

---

## 공통 (모든 Export)

- [ ] `magic-square-docs` Skill 로드됨
- [ ] Step A: `git status`, `pytest`, Phase, Test ID, Command **실제 수집**
- [ ] Step B: `NN = max(Report, Prompting) + 1` — 중복 없음
- [ ] Report·Transcript **동일 NN**
- [ ] `_Exported on` · `_Source uuid` 메타 포함
- [ ] **git commit 하지 않음** (사용자 요청 시만)
- [ ] **UPDATE_GOLDEN 임의 실행 금지**
- [ ] **채팅·터미널에 없는 pytest 결과 기재 금지**
- [ ] Step E: README `## 문서` 표 갱신
- [ ] Step F: 경로 2개 사용자 보고

---

## Phase: red (Ask)

| 체크 | 내용 |
|------|------|
| Command | `/red-test-plan`, `/red-skeleton`, `/tdd-red` 중 해당 |
| 산출 | C2C 표 · `pytest.fail` 또는 assert RED |
| pytest | FAILED 기대 (GREEN 전) |
| 금지 | `src/` 수정 (red-test-plan) |

**Report STEP 행:** RED — test-plan / skeleton / tdd-red

---

## Phase: green (Respond)

| 체크 | 내용 |
|------|------|
| Command | `/green-minimal`, `/golden-master` |
| 산출 | PASS Test ID · golden 경로 |
| pytest | 대상 + 회귀 PASSED |
| golden | `UPDATE_GOLDEN` 없이 matched (또는 ISS 재승인 완료 명시) |

**Report STEP 행:** GREEN — green-minimal / golden-master

---

## Phase: refactor (Refine)

| 체크 | 내용 |
|------|------|
| Command | `/refactor-smell`, `/refactor-safe` |
| 전제 | `pytest tests/ -v` 전부 PASS |
| 산출 | 스멜 표 · safe 후보 · 변경 요약 |
| golden | matched 유지 또는 롤백·ISS 기록 |

**Report STEP 행:** REFACTOR — smell / safe

---

## Phase: repeat (ARRR 1사이클 완료)

| 체크 | 내용 |
|------|------|
| 의미 | Ask→Respond→Refine 한 바퀴 종료 또는 세션 마감 Export |
| Report | STEP 표에 RED·GREEN·REFACTOR 요약 행 |
| Transcript | Commands 사용 목록 표 완비 |
| 다음 | `/red-test-plan` (다음 사이클) 또는 세션 종료 |

**Report STEP 행:** repeat — /export-session

---

## README 갱신 (Step E)

`README.md` `## 문서` 표에 추가:

```markdown
| [`Report/NN.<주제>-Report.md`](Report/NN.<주제>-Report.md) | <한 줄 설명> |
| [`Prompting/NN.<주제>-Transcript.md`](Prompting/NN.<주제>-Transcript.md) | <한 줄 설명> |
```

기존 행 유지 · NN 오름차순 권장.

---

## NN 산출 예

| Report 최대 | Prompting 최대 | 다음 NN |
|-------------|----------------|---------|
| 02 | 02 | **03** |
| 03 | 02 | **04** |
| 02 | 05 | **06** |

파일명 숫자 prefix 기준 (`01.` `02.` …).
