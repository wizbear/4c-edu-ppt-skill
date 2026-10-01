---
name: 4c-edu-ppt
description: 4C 교육 구조(Connect-Concept-Concrete Practice-Conclusion)로 교육용 PowerPoint 프레젠테이션 생성. 교육 자료, PPT, 프레젠테이션, 강의 자료 작성 시 사용. Bowman의 "Training From the Back of the Room!" 원칙(학습자 행동 중심, 10분 규칙, 관찰 가능한 학습 성과)을 검증기와 활동 카탈로그로 지원.
allowed-tools: Read, Bash, Write
---

# 4C 교육 구조 기반 PPT 제작

Markdown으로 쓴 교육 콘텐츠를 4C 구조의 PowerPoint로 변환한다. 4C는 Sharon Bowman의 *Training From the Back of the Room!* 에서 온 설계 틀이며, 각 단계는 **학습자가 무엇을 하는가**로 정의된다.

## 4C 교육 구조

| 단계 | 학습자가 하는 것 | 시간 감각 |
|---|---|---|
| **Connect** | 주제·동료·학습 목표와 연결한다. 말하거나 쓴다. 아이스브레이커가 아니라 주제 관련 활동 | 짧게, 맨 앞 |
| **Concept** | need-to-know 정보를 듣고·보고·쓰고·말한다 | 10분 단위. 사이에 Review |
| **Concrete Practice** | 전원이 직접 한다. 시연을 보는 것은 실습이 아니다 | 넉넉히 |
| **Conclusion** | 학습자가 요약·평가·실행 계획·축하한다. 강사가 요약하지 않는다 | 마지막 시간은 학습자 몫 |

철칙: 설명하는 사람이 배운다. 학습 성과는 관찰 가능한 동사로 쓴다("이해한다" 금지). 직접 강의는 10분을 넘기지 않는다.

## 작업 순서

1. 콘텐츠 Markdown 작성 (아래 규격). AI로 생성하려면 `docs/ai-guides/AI_CONTENT_PROMPT.md` 프롬프트 사용
2. 검증: `python scripts/validate_markdown_v3.py --md course.md` → error 0이 될 때까지 수정. warning은 설계 권고
3. 빌드: `python scripts/generate_with_master_layout.py --md course.md --template pptx-templates/default_4c_template.pptx --output result.pptx`
4. 활동 교체가 필요하면 `python scripts/swap_activity.py --md course.md --at "모듈1/Connect#1" --list`

스크립트 경로는 스킬 설치 위치 기준 (예: `.claude/skills/4c-edu-ppt/scripts/...`). `pip install python-pptx` 필요.

## Markdown 규격

```markdown
---
course: Python 프로그래밍 기초
audience: 비전공 신입사원
total_time: 170분
outcome: 조건문으로 20줄 프로그램을 작성한다      # 관찰 가능한 동사
mode: offline                                     # offline | online
---

# 모듈 1: 변수
outcome: 변수를 선언하고 값을 출력하는 코드를 작성한다

## Module Start
Python의 첫걸음                                   # 20자 이내

## Connect
time: 5분
title: 기계에 명령해 본 적 있나요?
main: 강사가 보여줄 한 줄
pattern: standing-survey                          # 활동 카탈로그 ID
params:
  question: 오늘 아침 기계에 내린 명령 1가지는?
  debrief: 공통 답 2개를 칠판에
alt: turn-and-talk, wall-writing                  # 교환 후보
notes: |                                          # 강사 노트 (슬라이드 노트로)
  준비물: 없음

## Concept
time: 8분
title: 변수란
main: 변수는 값에 붙이는 이름표
sub: |
  name = "홍길동"
activity: |                                       # 학습자가 하는 것 (직접 서술)
  강의 중 2번 멈춤: 옆 사람과 답 맞추기
handout: |                                        # nice-to-know → <output>_handout.md
  Python 역사 ...

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

## Conclusion
time: 4분
title: 내가 배운 것
main: 카드에 배운 것 3가지
pattern: learning-log
params:
  topic: 변수
action_plan: 다음 주 적용할 것 1가지를 쓰고 옆 사람에게 말한다   # 과정 마지막 Conclusion에 권고

## Break
time: 10분
sub: 다음 모듈 예고

## Image            # image:, caption:
## Video            # video:, description:, duration:
```

필드 규칙
- 모든 새 필드(outcome, activity, pattern, params, alt, notes, handout, action_plan, 프론트매터)는 **선택**. v1.0 파일은 그대로 빌드된다.
- `activity:` 는 네 단계 모두 허용. 있으면 슬라이드 본문 하단에 "▶ 활동" 블록으로 들어간다.
- `pattern:` 만 쓰면 카탈로그 템플릿 + `params` 로 활동 텍스트가 생성된다. `activity:` 가 있으면 그것이 우선.
- `## Review` 는 10분 강의 사이에 끼우는 1~2분 전원 참여 활동. `main/sub` 없이 `activity` 또는 `pattern` 만.
- 각 필드는 한 줄에 하나. 여러 줄 값은 `|` 뒤에 들여쓰기.

## 활동 카탈로그와 교환

`references/activities.md` (사람용) / `references/activities.json` (스크립트용). 단계별 활동 31개, 각각 시간·인원·모드·교환 그룹·템플릿을 가진다.

교환 규칙
- 같은 단계·같은 교환 그룹 → 자유. 시간·모드만 재검증
- 같은 단계·다른 그룹 → 허용, 목적 차이 경고
- 다른 단계 → 대상 활동의 `also_ok` 에 있을 때만
- `jigsaw`(새 내용) ↔ `teach-back`(배운 내용) 은 어느 방향으로도 교환 금지

```bash
python scripts/swap_activity.py --md course.md --at "모듈1/Connect#1" --list      # 후보와 사유
python scripts/swap_activity.py --md course.md --at "모듈1/Connect#1" --to turn-and-talk
python scripts/swap_activity.py --md course.md --mode online                      # 일괄 모드 전환
```

## 검증기가 보는 것

- 형식(error): 한 줄 다중 필드, 모르는 슬라이드 타입, time 형식, 카탈로그에 없는 pattern, 단계·모드 불일치
- 설계(warning): outcome 없음 또는 관찰 불가 동사, Concept 10분 초과(20분은 error), 활동 없는 Concept 연속 10분 초과, 활동 없는 Connect, 강사가 요약하는 Conclusion, 마지막 Conclusion에 action_plan 없음, 같은 pattern 3회 연속, total_time과 15% 이상 차이
- 시간 리포트: 모듈별 합계, 강사 발화 vs 학습자 활동 근사 비율, 버퍼. `--report run_sheet.md` 로 진행표 저장

`--strict` 또는 프론트매터 `strict: true` 면 warning도 실패.

## 참고 파일

- `examples/example_course.md` — Bowman 준수 예제. 복사해서 시작
- `examples/legacy_example_v1.md` — v1.0 형식 (하위 호환 확인용)
- `templates/review_checklist.md` — 생성 콘텐츠 검토 체크리스트
- `templates/phased_prompt.md` — 단계별 AI 생성 (성과 → 실습 → 개념 → 연결 → 정리 역방향 설계)
- `docs/` — 설치, 템플릿 제작, 다른 AI 도구 사용법

## 템플릿 레이아웃 이름

`Title_Page`, `Module_Divider`, `Connect`, `Concept`, `Review`(없으면 Concept 사용), `Concrete Practice`, `Conclusion`, `Break`, `End`, `Blank`. "4C - " 접두사도 인식.

## 문제 해결

- python-pptx 미설치: `pip install python-pptx`
- 한글 깨짐: 콘솔 `chcp 65001` 또는 `PYTHONIOENCODING=utf-8`
- 슬라이드 텍스트 넘침: `sub`/`activity` 를 줄이거나 `handout:` 으로 옮긴다
- pattern 오류: `references/activities.md` 에서 ID와 허용 단계 확인
