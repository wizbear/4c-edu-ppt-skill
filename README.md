# 4C 교육 구조 기반 PPT 제작 Skill

Markdown으로 쓴 교육 콘텐츠를 4C 구조(Connect - Concept - Concrete Practice - Conclusion)의 PowerPoint로 변환합니다. 4C는 Sharon Bowman의 *Training From the Back of the Room!* 설계 틀이며, 이 스킬은 그 원칙(학습자 행동 중심, 10분 규칙, 관찰 가능한 학습 성과)을 검증기와 활동 카탈로그로 지원합니다.

## 🚀 빠른 링크

| 사용자 | 제작자 |
|--------|--------|
| 📥 **[설치 가이드](INSTALLATION.md)** | 📦 **[배포 가이드](DISTRIBUTION.md)** |
| 👉 [빠른 시작](docs/getting-started/QUICK_START.md) | 🎨 [템플릿 제작](docs/templates/TEMPLATE_RULES.md) |
| 🤖 [AI로 콘텐츠 생성](docs/ai-guides/AI_CONTENT_PROMPT.md) | 📚 [활동 카탈로그](references/activities.md) |

## 필수 설치

```bash
pip install python-pptx
```

## 3단계 사용법

```bash
# 1. 콘텐츠 작성 — examples/example_course.md 를 복사해서 시작하거나 AI 프롬프트로 생성
# 2. 검증 — error 0 이 될 때까지. warning은 설계 권고
python .claude/skills/4c-edu-ppt/scripts/validate_markdown_v3.py --md my_course.md

# 3. 빌드
python .claude/skills/4c-edu-ppt/scripts/generate_with_master_layout.py \
  --md my_course.md \
  --template .claude/skills/4c-edu-ppt/pptx-templates/default_4c_template.pptx \
  --output my_course.pptx
```

빌드 결과: `my_course.pptx` + (handout 필드가 있으면) `my_course_handout.md`

## 4C 구조 — 학습자가 무엇을 하는가

| 단계 | 학습자가 하는 것 | 하지 말 것 |
|---|---|---|
| **Connect** | 주제·동료·목표와 연결. 말하거나 쓴다 | 강사의 수사적 질문 하나로 끝내기, 주제 무관 아이스브레이커 |
| **Concept** | need-to-know 를 듣고·보고·쓰고·말한다. 10분 단위 | 15분 연속 강의, 슬라이드 복사본 배포 |
| **Review** | 10분 강의 사이 1~2분 전원 복습 | 생략 |
| **Concrete Practice** | 전원이 직접 한다 | 강사 시연 관람 |
| **Conclusion** | 학습자가 요약·평가·실행 계획 | 강사가 "오늘 배운 것" 정리 |

## Markdown 형식

```markdown
---
course: Python 프로그래밍 기초
audience: 비전공 신입사원
total_time: 170분
outcome: 조건문으로 20줄 프로그램을 작성한다
mode: offline
---

# 모듈 1: 변수
outcome: 변수를 선언하고 값을 출력하는 코드를 작성한다

## Module Start
Python의 첫걸음

## Connect
time: 5분
title: 기계에 명령해 본 적 있나요?
main: 리모컨, 내비게이션, 알람
pattern: standing-survey
params:
  question: 오늘 아침 기계에 내린 명령 1가지는?
  debrief: 공통 답 2개를 칠판에
alt: turn-and-talk, wall-writing

## Concept
time: 8분
title: 변수란
main: 변수는 값에 붙이는 이름표
sub: |
  name = "홍길동"
activity: |
  강의 중 2번 멈춤: 옆 사람과 답 맞추기
handout: |
  Python 역사 (슬라이드에 넣지 않음)

## Review
time: 2분
title: 잠깐 정리
pattern: turn-and-talk
params:
  question: 변수를 한 문장으로?

## Concrete Practice
time: 15분
title: 나를 소개하는 프로그램
main: 변수 3개를 만들어 출력
pattern: paired-practice
params:
  task: name, age, food 변수 → f-string 출력
  half: 5
notes: |
  관찰 포인트: 따옴표 누락

## Conclusion
time: 4분
title: 내가 배운 것
main: 카드에 배운 것 3가지
pattern: learning-log
params:
  topic: 변수
action_plan: 다음 주 적용할 것 1가지를 쓰고 옆 사람에게 말한다

## Break
time: 10분
sub: 다음 모듈 예고
```

### 필드

| 필드 | 어디에 | 설명 |
|---|---|---|
| `time`, `title`, `main`, `sub` | 4C | v1.0과 동일 |
| `activity` | 4C 전부, Review | 학습자가 하는 것. 슬라이드 하단 "▶ 활동" 블록 |
| `pattern` + `params` | 4C 전부, Review | 활동 카탈로그 ID. `activity` 가 없으면 템플릿으로 생성 |
| `alt` | 4C 전부 | 교환 후보 ID (쉼표 구분) |
| `notes` | 모든 슬라이드 | 강사 노트 (슬라이드 노트로 들어감) |
| `handout` | 4C | nice-to-know. `<output>_handout.md` 로 분리 |
| `action_plan` | Conclusion | 실행 계획 블록. 과정 마지막에 권고 |
| `outcome` | 프론트매터, 모듈 | 관찰 가능한 동사 + 개념 |

새 필드는 모두 선택입니다. v1.0 파일은 그대로 빌드됩니다 (`examples/legacy_example_v1.md`).

## 활동 카탈로그와 교환

31개 활동이 `references/activities.md` 에 단계·시간·인원·모드·교환 그룹과 함께 있습니다.

```bash
# 교환 후보와 허용/불허 사유
python scripts/swap_activity.py --md my_course.md --at "모듈1/Connect#1" --list

# 교환 (diff 출력 후 저장)
python scripts/swap_activity.py --md my_course.md --at "모듈1/Connect#1" --to turn-and-talk

# 온라인 과정으로 일괄 전환
python scripts/swap_activity.py --md my_course.md --mode online
```

규칙: 같은 단계·같은 그룹은 자유, 다른 단계는 `also_ok` 에 있을 때만, `jigsaw` ↔ `teach-back` 은 금지.

## 검증기

```bash
python scripts/validate_markdown_v3.py --md my_course.md [--strict] [--report run_sheet.md]
```

- **형식 (error, 빌드 막음)**: 한 줄 다중 필드, 모르는 슬라이드 타입, time 형식, 없는 pattern, 단계·모드 불일치
- **설계 (warning, 빌드는 됨)**: outcome 없음 또는 "이해한다" 류 동사, Concept 10분 초과, 활동 없는 Connect/Conclusion, 마지막 action_plan 없음, 같은 활동 3회 연속, total_time 불일치
- **시간 리포트**: 모듈별 합계, 강사 발화 vs 학습자 활동 근사 비율, 버퍼. `--report` 로 진행표 저장

## 포함된 템플릿

`pptx-templates/default_4c_template.pptx` 레이아웃: Title_Page, Module_Divider, Connect, Concept, Concrete Practice, Conclusion, Break, End, Blank. `Review` 레이아웃이 없으면 Concept 레이아웃을 씁니다. 자신의 템플릿은 같은 이름의 레이아웃을 만들면 됩니다 ([템플릿 규칙](docs/templates/TEMPLATE_RULES.md)).

## 문제 해결

| 증상 | 조치 |
|---|---|
| python-pptx 설치 오류 | `python -m venv venv` 후 설치 |
| 한글 깨짐 | `chcp 65001` 또는 `PYTHONIOENCODING=utf-8` |
| 슬라이드 텍스트 넘침 | `sub`/`activity` 줄이기, `handout:` 으로 이동 |
| pattern 오류 | `references/activities.md` 에서 ID·허용 단계 확인 |
| Review 레이아웃 없음 | 정상. Concept 레이아웃으로 대체됨 |

## 📚 문서

- 시작: [빠른 시작](docs/getting-started/QUICK_START.md) · [상세 가이드](docs/getting-started/HOW_TO_USE.md) · [워크플로우](docs/reference/WORKFLOW_GUIDE.md)
- AI 생성: [프롬프트](docs/ai-guides/AI_CONTENT_PROMPT.md) · [단계별 생성](templates/phased_prompt.md) · [기존 자료 변환](docs/ai-guides/CONVERT_TO_4C_PROMPT.md) · [Gemini/ChatGPT](docs/ai-guides/GEMINI_CHATGPT_QUICK.md) · [Claude Web](docs/ai-guides/CLAUDE_WEB_GUIDE.md)
- 검토: [검토 체크리스트](templates/review_checklist.md) · [최종화 가이드](templates/finalization_guide.md)
- 템플릿: [규칙](docs/templates/TEMPLATE_RULES.md) · [커스터마이징](docs/templates/TEMPLATE_CUSTOMIZATION.md) · [마스터 레이아웃](docs/templates/MASTER_LAYOUT_GUIDE.md)
- 참고: [활동 카탈로그](references/activities.md) · [개선 제안서](docs/proposals/2026-09-30_4c_improvement_proposal.md)

## 스크립트

| 스크립트 | 용도 |
|---|---|
| `generate_with_master_layout.py` | 빌드 (메인) |
| `validate_markdown_v3.py` | 검증 + 시간 리포트 + 진행표 |
| `swap_activity.py` | 활동 교환 |
| `build_activity_catalog.py` | activities.json → activities.md |
| `md4c.py` | 공용 파서·카탈로그 모듈 |
| `generate_4c_ppt.py`, `generate_from_md.py`, `validate_markdown.py`, `validate_markdown_v2.py`, `fix_markdown.py` | v1.0 레거시. 유지되지만 문서에서는 다루지 않음 |

## 라이선스

이 Skill은 자유롭게 수정하고 배포할 수 있습니다.
