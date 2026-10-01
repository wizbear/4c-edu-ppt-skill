# 4c-edu-ppt 사용 가이드 (v1.1)

교육 콘텐츠를 Markdown으로 쓰고, 검증하고, 4C 구조의 PowerPoint로 만드는 전체 흐름입니다.
처음 쓰는 분은 1장부터 순서대로, 이미 v1.0을 쓰던 분은 7장 "v1.0에서 달라진 것"부터 보세요.

---

## 1. 준비

```bash
pip install python-pptx
```

스킬이 설치된 경로를 확인합니다. 보통 프로젝트의 `.claude/skills/4c-edu-ppt/` 입니다. 아래 명령은 모두 이 경로를 `SKILL`로 줄여 씁니다.

```bash
# 예: Windows
set SKILL=.claude\skills\4c-edu-ppt
# 예: macOS / Linux
SKILL=.claude/skills/4c-edu-ppt
```

한글 출력이 깨지면 `chcp 65001` (Windows) 또는 `export PYTHONIOENCODING=utf-8`.

---

## 2. 전체 흐름 (한눈에)

```
① 설계      outcome 정하기 → 실습 → 개념 → 연결 → 정리 (templates/structure_template.md)
② 작성      course.md 작성 (직접 또는 AI 프롬프트)
③ 검증      validate_markdown_v3.py  → error 0 될 때까지
④ 다듬기    swap_activity.py 로 활동 교체, review_checklist.md 로 검토
⑤ 빌드      generate_with_master_layout.py → .pptx + _handout.md
⑥ 확인      PowerPoint에서 넘침·노트 확인, run_sheet.md 로 진행
```

가장 짧은 경로는 ② → ③ → ⑤ 세 단계입니다.

---

## 3. Markdown 작성

### 3.1 시작하는 법

`examples/example_course.md` 를 복사해서 내용만 바꾸는 것이 가장 빠릅니다.

```bash
cp $SKILL/examples/example_course.md my_course.md
```

### 3.2 파일 구조

```markdown
---                                  ← 프론트매터 (과정 정보)
course: 과정명
audience: 대상
total_time: 120분
outcome: 과정 전체 성과
mode: offline
---

# 모듈 1: 제목                       ← 모듈
outcome: 모듈 성과

## Module Start                      ← 슬라이드들
한 줄 소개

## Connect
...
## Concept
...
## Review
...
## Concrete Practice
...
## Conclusion
...
## Break
...

# 모듈 2: 제목
...
```

### 3.3 슬라이드 타입

| 타입 | 역할 | 필수 필드 |
|---|---|---|
| `## Module Start` | 모듈 구분 슬라이드 | 본문 한 줄 (20자 이내) |
| `## Connect` | 학습자가 주제와 연결 | time, title, main |
| `## Concept` | 핵심 개념 (10분 이하) | time, title, main |
| `## Review` | 강의 사이 1~2분 복습 | time, title, activity 또는 pattern |
| `## Concrete Practice` | 전원 실습 | time, title, main, activity 또는 pattern |
| `## Conclusion` | 학습자가 정리 | time, title, main |
| `## Break` | 휴식 | (time, sub 선택) |
| `## Image` | 이미지 | image (caption 선택) |
| `## Video` | 영상 안내 | video (description, duration 선택) |

### 3.4 필드

```markdown
## Connect
time: 5분                      # 숫자 + 분
title: 슬라이드 제목
main: 강사가 보여줄 한 줄
sub: |                         # 여러 줄은 | 뒤에 두 칸 들여쓰기
  보조 설명
  - 불릿도 가능
activity: |                    # 학습자가 하는 것. 슬라이드 하단 "▶ 활동" 블록
  옆 사람과 1분씩 말하기
pattern: turn-and-talk         # 활동 카탈로그 ID. activity 없으면 템플릿으로 생성
params:                        # 템플릿 변수
  question: 질문 내용
alt: wall-writing, table-talk  # 교환 후보
notes: |                       # 강사 노트 → 슬라이드 노트
  준비물, 디브리프 질문, 시간 큐
handout: |                     # 슬라이드에 안 넣을 참고 내용 → <output>_handout.md
  배경 지식, 출처
action_plan: 다음 주 적용할 것  # Conclusion 전용. "✍ 실행 계획" 블록
```

규칙 세 가지만 기억하세요.
- 한 줄에 필드 하나. `time: 5분 title: 제목` 처럼 붙이면 error.
- 여러 줄 값은 `|` 다음 줄부터 두 칸 들여쓰기.
- `activity` 와 `pattern` 둘 다 있으면 `activity` 가 우선.

### 3.5 activity 와 pattern 중 무엇을 쓰나

| 상황 | 선택 |
|---|---|
| 카탈로그에 맞는 활동이 있고 지시문을 직접 쓰기 귀찮다 | `pattern:` + `params:` |
| 지시문을 내 말로 쓰고 싶다 | `activity:` |
| 카탈로그 활동을 쓰되 지시문은 내 말로 | `pattern:` + `activity:` (교환 후보 추적용으로 pattern 유지) |

카탈로그 목록: `references/activities.md`

---

## 4. AI로 콘텐츠 생성

### 4.1 Claude Code 안에서

프로젝트에 스킬이 설치돼 있으면 이렇게 요청합니다.

```
4C 구조로 "Excel 피벗 테이블 기초" 교육 PPT를 만들어줘.
대상은 사무직 신입, 90분, 오프라인.
```

Claude가 SKILL.md를 읽고 Markdown 작성 → 검증 → 빌드까지 진행합니다. 중간 산출물(`.md`)을 꼭 받아 두세요. 수정은 Markdown에서 합니다.

### 4.2 ChatGPT / Gemini / Claude 웹

`docs/ai-guides/AI_CONTENT_PROMPT.md` 의 "기본 프롬프트"를 복사해 주제만 바꿔 붙여넣습니다. 결과를 `course.md` 로 저장한 뒤 3단계(검증)로.

한 번에 전체를 만들면 품질이 떨어집니다. 모듈이 3개를 넘으면 `templates/phased_prompt.md` 의 단계별 생성(성과 → 실습 → 개념 → 연결 → 정리)을 권합니다.

### 4.3 기존 자료 변환

PPT나 강의 노트가 이미 있으면 `docs/ai-guides/CONVERT_TO_4C_PROMPT.md`.

---

## 5. 검증

```bash
python $SKILL/scripts/validate_markdown_v3.py --md my_course.md
```

출력은 세 묶음입니다.

| 묶음 | 의미 | 조치 |
|---|---|---|
| `[ERROR]` | 형식 문제. 빌드가 깨지거나 엉뚱하게 나옴 | 반드시 수정 |
| `[WARNING]` | 교수설계 권고 (10분 규칙, 활동 없음, outcome 동사 등) | 읽고 수정하거나 의도적 예외로 판단 |
| `[시간 리포트]` | 모듈별 합계, 강사 발화 비율, 버퍼 | 계획과 비교 |

자주 보는 메시지와 뜻:

| 규칙 | 메시지 | 뜻 |
|---|---|---|
| D02 | outcome에 관찰 불가 동사 | "이해한다" → "작성한다/설명한다/시연한다" 로 |
| D03 | Concept 12분. 10분 규칙 초과 | 둘로 나누고 사이에 `## Review` |
| D04 | 활동 없는 Concept 연속 18분 | 사이에 Review 또는 activity |
| D06 | Connect에 학습자 활동 없음 | 질문만 던지지 말고 `pattern: turn-and-talk` 등 |
| D07 | Conclusion을 강사가 요약 | `pattern: learning-log` 등 학습자 요약으로 |
| D09 | 마지막 Conclusion에 action_plan 없음 | 과정 끝에 실행 계획 |
| F06/F07 | pattern이 카탈로그에 없음 / 단계 불허 | `references/activities.md` 에서 ID와 허용 단계 확인 |

옵션:
- `--report run_sheet.md` 강사용 진행표 저장 (시각, 분, 단계, 활동, 노트)
- `--strict` warning도 실패로. 프론트매터 `strict: true` 와 같음
- `--format-only` / `--design-only`

---

## 6. 활동 교환

활동을 바꾸고 싶을 때 지시문을 다시 쓰는 대신 pattern만 교체합니다.

```bash
# 후보 보기 (✓ 자유 / △ 조건부 / ✗ 불가, 사유 포함)
python $SKILL/scripts/swap_activity.py --md my_course.md --at "모듈1/Connect#1" --list

# 교환 (diff 보여주고 저장)
python $SKILL/scripts/swap_activity.py --md my_course.md --at "모듈1/Connect#1" --to turn-and-talk

# 저장 없이 미리보기
python $SKILL/scripts/swap_activity.py --md my_course.md --at "모듈1/Connect#1" --to turn-and-talk --dry-run

# 온라인 과정으로 일괄 전환 (오프라인 전용 활동을 모두 대체)
python $SKILL/scripts/swap_activity.py --md my_course.md --mode online
```

`--at` 쓰는 법: `모듈1/Connect#1` = 모듈 1의 첫 번째 Connect. `2/Practice` = 모듈 2의 첫 Practice. 모듈은 번호 또는 제목 일부.

교환 규칙:
- 같은 단계, 같은 교환 그룹 → 자유
- 같은 단계, 다른 그룹 → 허용하되 목적 차이 경고
- 다른 단계 → 그 활동의 "다른 단계 허용" 목록에 있을 때만
- `jigsaw` ↔ `teach-back` 은 금지 (새 내용용 vs 배운 내용용)
- 과정 mode와 안 맞는 활동 → 불가

교환 후 새 pattern에 필요한 params가 없으면 `<입력: …>` 자리를 넣어 줍니다. 채운 뒤 다시 검증하세요.

---

## 7. 빌드

```bash
python $SKILL/scripts/generate_with_master_layout.py \
  --md my_course.md \
  --template $SKILL/pptx-templates/default_4c_template.pptx \
  --output my_course.pptx
```

생성물:
- `my_course.pptx` — 제목 슬라이드(프론트매터) → 모듈별 슬라이드 → End
- `my_course_handout.md` — `handout:` 필드가 하나라도 있을 때

옵션: `--no-title`, `--no-end`, `--handout 경로`, `--catalog 경로`

슬라이드에 들어가는 것:
- 4C 슬라이드 하단에 "▶ 활동 (N분)" 블록
- Conclusion에 "✍ 실행 계획" 블록
- 슬라이드 노트에 `#Skill #Connect #5분 #Pattern:…` 태그 + 활동 전문 + 강사 노트 + 교환 후보

자기 템플릿을 쓰려면 레이아웃 이름을 `Connect`, `Concept`, `Concrete Practice`, `Conclusion`, `Module_Divider`, `Break` 로 맞추면 됩니다. `Review` 레이아웃은 없으면 Concept를 씁니다. 자세한 건 `docs/templates/TEMPLATE_RULES.md`.

---

## 8. 빌드 후 확인

PowerPoint에서:
1. Concept 슬라이드 — 상자가 하나라 main + sub + 활동이 함께 들어갑니다. 넘치면 `sub` 를 줄이거나 `handout:` 으로 옮기세요. 검증기가 400자 넘는 슬라이드를 D13으로 알려 줍니다.
2. 발표자 보기 — 노트에 활동 지시문과 강사 노트가 있는지.
3. `run_sheet.md` — 인쇄해서 강의 중 시간 관리에.

사람 검토는 `templates/review_checklist.md` 2단계(Bowman 철칙)와 철칙 통과표를 쓰세요.

---

## 9. v1.0에서 달라진 것

v1.0 파일은 수정 없이 그대로 빌드됩니다. 새 기능은 모두 선택 필드입니다.

| v1.0 | v1.1 |
|---|---|
| `activity` 는 Practice 전용 | 네 단계 모두 + Review |
| 검증은 형식만 (`validate_markdown_v2.py`) | 형식 + 설계 + 시간 (`validate_markdown_v3.py`) |
| 활동은 자유 서술 | 카탈로그 31개, `pattern:` 참조, 교환 명령 |
| 학습 성과 필드 없음 | 프론트매터·모듈 `outcome:` + 동사 검사 |
| 강사 노트는 태그만 | `notes:` 필드, 활동 전문, 교환 후보 |
| Concept 레이아웃에서 `sub` 누락 (버그) | main + sub + 활동 모두 표시 |
| 제목·End 슬라이드 없음 | 프론트매터로 자동 생성 |

v1.0 예제로 검증기를 돌리면 warning 16건이 나옵니다. 그것이 v1.0 설계와 Bowman 원칙의 차이입니다. 하나씩 고쳐 보면 새 방식이 몸에 익습니다.

```bash
python $SKILL/scripts/validate_markdown_v3.py --md $SKILL/examples/legacy_example_v1.md
```

---

## 10. 자주 묻는 것

**Q. 4C마다 꼭 활동을 넣어야 하나요?**
안 넣어도 빌드됩니다. 다만 Bowman의 4C는 "학습자가 하는 것"으로 정의되므로 검증기가 warning을 냅니다. 특히 Connect와 Conclusion은 활동이 없으면 강사 독백이 됩니다.

**Q. Concept가 15분인데 꼭 나눠야 하나요?**
10분 넘으면 warning, 20분 넘으면 error입니다. 나누기 싫으면 `activity:` 로 중간 멈춤 활동을 넣으면 "활동 있는 Concept"로 취급돼 연속 강의 경고가 사라집니다.

**Q. 온라인 과정은요?**
프론트매터 `mode: online` 으로 두고 `swap_activity.py --mode online` 을 돌리면 오프라인 전용 활동이 교체됩니다. 카탈로그의 body-break, chat-blast 는 온라인용입니다.

**Q. 카탈로그에 내 활동을 추가하려면?**
`references/activities.json` 에 항목을 추가하고 `python scripts/build_activity_catalog.py` 로 MD를 재생성합니다. 필수 키: id, name, name_ko, stages, swap_group, time, group, mode, summary, template.

**Q. 레거시 스크립트(generate_4c_ppt.py 등)는?**
남아 있지만 문서에서 뺐습니다. 새 기능은 반영되지 않습니다.

---

## 11. 파일 지도

```
4c-edu-ppt/
├── SKILL.md                      Claude Code가 읽는 스킬 정의
├── README.md                     개요
├── scripts/
│   ├── generate_with_master_layout.py   빌드 (메인)
│   ├── validate_markdown_v3.py          검증 + 시간 리포트 + 진행표
│   ├── swap_activity.py                 활동 교환
│   ├── build_activity_catalog.py        카탈로그 JSON → MD
│   └── md4c.py                          공용 파서
├── references/
│   ├── activities.json           활동 카탈로그 (원본)
│   └── activities.md             활동 카탈로그 (읽기용)
├── examples/
│   ├── example_course.md         v1.1 예제 (복사해서 시작)
│   └── legacy_example_v1.md      v1.0 예제
├── templates/
│   ├── structure_template.md     설계 틀
│   ├── phased_prompt.md          단계별 AI 생성
│   ├── review_checklist.md       검토 체크리스트
│   └── finalization_guide.md     최종화·배포
├── pptx-templates/
│   └── default_4c_template.pptx  기본 템플릿
└── docs/
    ├── getting-started/          이 문서, 빠른 시작
    ├── ai-guides/                AI 프롬프트
    ├── templates/                템플릿 제작
    └── proposals/                개선 제안서
```
