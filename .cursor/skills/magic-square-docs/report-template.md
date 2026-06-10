# Report 템플릿 — magic-square-docs

**SSOT 참조 형식:** `Report/05.REPORT.md` (구조·메타 필드)

파일명: `Report/NN.<주제>-Report.md`

---

```markdown
# MagicSquare_xx — <주제> 보고서

**작성일:** YYYY-MM-DD
**프로젝트:** MagicSquare_xx
**세션:** <세션 N · 단계>
**Phase:** <red | green | refactor | repeat>
**ARRR:** <Ask | Respond | Refine>
**상태:** <완료 / 진행 중>
**_Exported on:** YYYY-MM-DDTHH:MM:SS+09:00
**_Source uuid:** <채팅·세션 식별자 또는 N/A>

---

## 1. 세션 목표

<한 단락>

---

## 2. ARRR · Phase STEP

| STEP | Phase | Command | Test ID | 결과 |
|------|-------|---------|---------|------|
| RED | red | /red-test-plan | T-… | 설계 완료 |
| RED | red | /red-skeleton | T-… | pytest.fail |
| RED | red | /tdd-red | T-… | FAILED |
| GREEN | green | /green-minimal | T-… | PASS |
| GREEN | green | /golden-master | T-… | matched |
| REFACTOR | refactor | /refactor-smell | — | 스멜 표 |
| REFACTOR | refactor | /refactor-safe | #1 | PASS |
| repeat | repeat | /export-session | — | Export |

> 해당 없는 행은 삭제. `repeat` = ARRR 1사이클 완료 후 Export.

---

## 3. 산출물

| 파일 | 설명 |
|------|------|
| `Report/NN.<주제>-Report.md` | 본 보고서 |
| `Prompting/NN.<주제>-Transcript.md` | Transcript |
| … | … |

---

## 4. 핵심 결정

| 항목 | 결정 |
|------|------|
| … | … |

---

## 5. 검증 결과

### 5.1 git status (Export 시점)

```
<git status --short 실제 출력>
```

### 5.2 pytest (Export 시점 · **실행 결과만**)

```bash
python -m pytest tests/ -v
```

| 구분 | 통과 | 실패 | 스킵 | 합계 |
|------|------|------|------|------|
| 전체 | N | N | N | N |

| 테스트 (실패·이번 사이클 관련만) | 결과 | 메시지 1줄 |
|----------------------------------|------|------------|

**겨냥 Test ID / 기준:** T-… / S1·S2·S3

### 5.3 golden (해당 시)

| Test ID | 경로 | matched |
|---------|------|---------|
| T-… | `tests/golden/T-….approved.txt` | YES / N/A |

---

## 6. 다음 액션

- [ ] …

---

## 7. 관련 문서

- `Prompting/NN.<주제>-Transcript.md`
- `docs/PRD.md`
- `.cursorrules`
- `.cursor/skills/magic-square-tdd/SKILL.md`
```
