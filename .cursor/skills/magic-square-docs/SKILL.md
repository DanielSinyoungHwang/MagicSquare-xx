---
name: magic-square-docs
description: >-
  MagicSquare_xx 세션 Report·Transcript Export 워크플로. Use when exporting
  sessions, writing Report or Transcript, running /export-session, Phase repeat,
  ARRR 1-cycle completion reports, or session N reports (세션 N 보고서).
disable-model-invocation: true
---

# MagicSquare Docs — Session Export

**SSOT 형식:** `Report/05.REPORT.md`, `Prompting/05.Export-Transcript.md` (구조·메타)  
**연동:** `/export-session` Command — **Export 요청 시 magic-square-docs Skill 로드 후 checklist 수행**

**템플릿:** [report-template.md](report-template.md) · [transcript-template.md](transcript-template.md) · [phase-checklist.md](phase-checklist.md)

**금지:** git commit 임의 · `UPDATE_GOLDEN` 임의 · 채팅·터미널에 **없는** pytest 결과 기재

---

## 파일명 규칙

```
Report/NN.<주제>-Report.md
Prompting/NN.<주제>-Transcript.md
```

| 항목 | 규칙 |
|------|------|
| `NN` | 2자리 — `max(Report, Prompting)` + 1 |
| `<주제>` | kebab-case (`Session3-TDD-GREEN`, `ARRR-Cycle1-REFACTOR`) |
| 쌍 | Report·Transcript **동일 NN** |

---

## 워크플로 개요

```
Step A  입력 수집 (git, pytest, Phase, Test ID, Command)
Step B  NN 확정
Step C  Report 작성 (Phase별 STEP)
Step D  Transcript 작성 (User/Cursor, 메타)
Step E  README 문서 표 갱신
Step F  완료 보고 (경로 2개)
```

---

## Step A — 입력 수집 (실행 필수)

**추정 금지.** 아래를 **터미널·채팅에서 실제 수집**한다.

| 항목 | 수집 방법 |
|------|-----------|
| **git status** | `git status --short` |
| **pytest** | `python -m pytest tests/ -v` (또는 세션에서 마지막 실행과 동일 명령) |
| **Phase** | `red` \| `green` \| `refactor` \| `repeat` |
| **Test ID** | `T-…` / S1·S2·S3 — 채팅·Command 보고 |
| **Command** | 사용한 `/red-test-plan` … `/export-session` 목록 |

수집 실패 시 pytest 줄은 **「미실행」** 으로 명시 — 숫자 조작 금지.

---

## Step B — NN 확정

1. `Report/NN.*` · `Prompting/NN.*` 목록에서 **최대 NN** 조회
2. `NN = max + 1` (2자리: `03`, `04`, …)
3. `<주제>` — 세션·Phase·ARRR 사이클에서 kebab-case 결정

**현재 예:** Report·Prompting 최대 `02` → 다음 `03`

---

## Step C — Report 작성

[report-template.md](report-template.md) 복사 후 채운다.

**필수 섹션:**

1. 세션 목표  
2. **ARRR · Phase STEP** — RED / GREEN / REFACTOR / repeat 행  
3. 산출물 표  
4. 핵심 결정  
5. 검증 결과 — **Step A git·pytest 실측**  
6. 다음 액션  
7. 관련 문서  

**메타 필드:**

- `_Exported on:` ISO8601 (KST 권장)
- `_Source uuid:` 채팅 ID·`N/A`

**Phase별 STEP (해당만):**

| Phase | STEP 행 예 |
|-------|------------|
| red | `/red-test-plan` · `/red-skeleton` · `/tdd-red` |
| green | `/green-minimal` · `/golden-master` |
| refactor | `/refactor-smell` · `/refactor-safe` |
| repeat | `/export-session` — ARRR 1사이클 완료 |

---

## Step D — Transcript 작성

[transcript-template.md](transcript-template.md) 복사 후 채운다.

**발화자:** `User` / `Cursor` (Agent 아님 **Cursor** 표기)

**필수:**

- Turn 단위 요약 (원문 과다 복붙 지양)
- **Commands 사용 목록** 표
- `Session State` · `Prompting Context (재개용)`
- `_Exported on` · `_Source uuid`

Command Turn 예:

```markdown
## Turn 12 — Cursor

> Phase: green | Layer: entity | Track: Logic
> Command: `/green-minimal`
> pytest: PASSED — test_complete_grid_all_ten_lines_pass
```

---

## Step E — README 갱신

`README.md` `## 문서` 표에 신규 2행 추가:

```markdown
| [`Report/NN.<주제>-Report.md`](Report/NN.<주제>-Report.md) | <한 줄> |
| [`Prompting/NN.<주제>-Transcript.md`](Prompting/NN.<주제>-Transcript.md) | <한 줄> |
```

NN 순·기존 행 유지.

---

## Step F — 완료 보고

사용자에게 **경로 2개**만 명확히:

```
Export 완료

- Report/NN.<주제>-Report.md
- Prompting/NN.<주제>-Transcript.md

pytest: <Step A 요약 1줄>
다음: <Prompting Context 한 줄>
```

---

## Phase: repeat (ARRR 1사이클 완료)

**트리거:** Ask(RED) → Respond(GREEN) → Refine(REFACTOR) 한 바퀴 종료 후 Export.

Report STEP 표에 **전 Phase 요약** + `repeat` 행.  
Transcript Commands 표에 사이클 전 Command 나열.

[phase-checklist.md](phase-checklist.md) `Phase: repeat` 절 확인.

---

## /export-session 연동

`/export-session` 실행 시:

1. **magic-square-docs** Skill 로드
2. [phase-checklist.md](phase-checklist.md) **공통 + 해당 Phase** 체크
3. Step A → F 순서 고정
4. git commit **하지 않음**

---

## ARRR · Phase 매핑 (Report STEP용)

| ARRR | Phase | 대표 Command |
|------|-------|--------------|
| Ask | red | red-test-plan → red-skeleton → tdd-red |
| Respond | green | green-minimal → golden-master |
| Refine | refactor | refactor-smell → refactor-safe |
| (마감) | repeat | export-session |

---

## 검증 결과 기재 규칙

| 허용 | 금지 |
|------|------|
| Step A에서 **실행한** pytest stdout 요약 | 이전 세션·기억·추정 pass/fail 수 |
| 실패 테스트명·메시지 **1줄** | 전체 로그 무단 붙여넣기 (요약 권장) |
| git status **실제 출력** | 변경 없다고 가정 |

golden: Export 시 `matched YES/N/A` — `UPDATE_GOLDEN`은 Export Skill **범위 밖**.

---

## 완료 체크리스트 (요약)

→ 상세: [phase-checklist.md](phase-checklist.md)

- [ ] Step A 실측 완료
- [ ] NN 중복 없음
- [ ] Report + Transcript 저장
- [ ] Phase STEP · Commands 표
- [ ] README 갱신
- [ ] 경로 2개 보고
- [ ] git commit 없음

---

## 관련 Skill·Command

| 리소스 | 용도 |
|--------|------|
| `magic-square-tdd` | Phase·Test ID·pytest 패턴 |
| `/export-session` | Export 진입점 |
| `.cursorrules` | 도메인·TDD 규칙 |
| `docs/PRD.md` | S1~S3·FR |
