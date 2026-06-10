# Export Session — MagicSquare_xx

세션 종료 시 **Report**·**Prompting**에 `NN.XXX` 형식으로 저장한다.

> **Export 요청 시 magic-square-docs Skill 로드 후 checklist 수행**  
> Skill: `.cursor/skills/magic-square-docs/SKILL.md`  
> Checklist: `phase-checklist.md` · Templates: `report-template.md`, `transcript-template.md`

---

## 파일명 규칙

```
Report/NN.<주제>-Report.md
Prompting/NN.<주제>-Transcript.md
```

| 항목 | 규칙 |
|------|------|
| `NN` | 세션 순번 2자리 (`01`, `02`, …). 기존 최대값 +1 |
| `<주제>` | kebab-case 영문 또는 하이픈 구분 (`Session3-TDD-RED`) |
| 확장자 | Report / Transcript 고정 |

**예시**

- `Report/02.Session3-TDD-RED-Report.md`
- `Prompting/02.Session3-TDD-RED-Transcript.md`

---

## 실행 절차

1. **세션 식별** — 주제·단계·상태(완료/진행 중) 확정
2. **Report 작성** — 산출물·결정·다음 액션 요약
3. **Transcript 작성** — Turn 단위 대화·명령·결과 기록
4. **Session State**·**Prompting Context (재개용)** 블록 포함
5. 저장 후 사용자에게 경로 2개 보고

---

## Report 템플릿

```markdown
# MagicSquare_xx — <주제> 보고서

**작성일:** YYYY-MM-DD
**프로젝트:** MagicSquare_xx
**세션:** <단계>
**상태:** <완료 / 진행 중>

---

## 1. 세션 목표

## 2. 산출물

| 파일 | 설명 |
|------|------|

## 3. 핵심 결정

## 4. 검증 결과

## 5. 다음 액션

- [ ] ...

## 6. 관련 문서
```

---

## Transcript 템플릿

```markdown
# Export Transcript — MagicSquare_xx <주제>

**Exported:** YYYY-MM-DD
**Session:** <단계>

---

## Turn N — User / Agent

> ...

---

## Session State

| 항목 | 값 |
|------|-----|

---

## Prompting Context (재개용)

\```
프로젝트: MagicSquare_xx
단계: ...
다음: ...
\```
```

---

## 체크리스트

`magic-square-docs` Skill · [phase-checklist.md](../skills/magic-square-docs/phase-checklist.md) 기준:

- [ ] Step A: `git status` · `pytest` · Phase · Test ID · Command **실측**
- [ ] Step B: `NN = max(Report, Prompting) + 1` — 중복 없음
- [ ] Step C~D: Report · Transcript (`_Exported on` · `_Source uuid`)
- [ ] Step E: README `## 문서` 표 갱신
- [ ] Step F: 경로 2개 보고
- [ ] Transcript: User/Cursor Turn · Commands 표
- [ ] Report: Phase STEP (RED/GREEN/REFACTOR/repeat) · **실행한 pytest만** 기재
- [ ] **git commit 하지 않음** (사용자 요청 시만)
- [ ] **UPDATE_GOLDEN 임의 실행 금지**
