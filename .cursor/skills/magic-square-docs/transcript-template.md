# Transcript 템플릿 — magic-square-docs

**SSOT 참조 형식:** `Prompting/05.Export-Transcript.md` (구조·메타 필드)

파일명: `Prompting/NN.<주제>-Transcript.md`

---

```markdown
# Export Transcript — MagicSquare_xx <주제>

**Exported:** YYYY-MM-DD
**_Exported on:** YYYY-MM-DDTHH:MM:SS+09:00
**_Source uuid:** <채팅·세션 식별자 또는 N/A>
**Session:** <세션 N · 단계>
**Phase:** <red | green | refactor | repeat>
**User role:** 4×4 부분 마방진 학습자 / 프로젝트 오너
**Cursor role:** TDD·문서·구현 보조 Agent

---

## Turn 1 — User

> <요청 원문 요약>

---

## Turn 2 — Cursor

> <응답·산출 요약>
> Command: `/…` (해당 시)
> Phase: <red | green | refactor>

---

## Turn N — User

> …

---

## Turn N+1 — Cursor

> …

<!-- Turn 패턴 반복. Command 실행 Turn에는 Command명·pytest 결과 1줄 필수 -->

---

## Commands 사용 목록

| Command | Turn | 결과 |
|---------|------|------|
| /red-test-plan | N | C2C·플랜 |
| /red-skeleton | N | pytest.fail |
| /green-minimal | N | PASS |
| /golden-master | N | matched |
| /refactor-smell | N | 스멜 표 |
| /refactor-safe | N | safe refactor |
| /export-session | N | Report·Transcript |

---

## Session State

| 항목 | 값 |
|------|-----|
| Phase | … |
| Test ID | T-… |
| ARRR 사이클 | Ask / Respond / Refine / repeat |
| pytest (전체) | N PASS / N FAILED |
| golden matched | YES / N/A |
| git commit | 없음 / <해시> (사용자 요청 시만) |
| Export NN | NN.<주제> |

---

## Prompting Context (재개용)

\```
프로젝트: MagicSquare_xx
세션: …
Phase: …
Test ID: …
API: validate_lines(grid) -> {status, failed_lines}
pytest: <실제 마지막 실행 요약>
다음: …
참고: Report/NN.<주제>-Report.md
\```
```

---

## Turn 작성 규칙

| 발화자 | 표기 |
|--------|------|
| 사용자 | `## Turn N — User` |
| Agent | `## Turn N — Cursor` |

- Command 실행 Turn: `Command: /…` 한 줄
- pytest 언급: **실제 실행 출력만** (추정 금지)
- 긴 코드는 경로·함수명으로 대체
