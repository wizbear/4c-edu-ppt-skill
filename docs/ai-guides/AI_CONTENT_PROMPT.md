# 4C 교육 콘텐츠 생성 프롬프트

생성형 AI(Claude, ChatGPT, Gemini)로 4C 구조 교육 콘텐츠를 만들기 위한 프롬프트입니다.
출력은 `scripts/validate_markdown_v3.py` 로 검증하고 `scripts/generate_with_master_layout.py` 로 PPT를 만듭니다.

---

## 📋 기본 프롬프트 (복사해서 사용)

```
당신은 교육 설계자입니다. Sharon Bowman의 4C 구조(Training From the Back of the Room!)로 교육 콘텐츠를 작성해주세요.
4C의 각 단계는 "학습자가 무엇을 하는가"로 정의됩니다. 강사가 말할 내용이 아닙니다.

## 주제
[여기에 교육 주제를 입력하세요]

## 대상과 시간
- 대상: [누구, 사전 지식 수준]
- 총 시간: [분]
- 모듈 수: [n]
- 모드: [offline / online]

## 4C 구조
- Connect: 학습자가 주제·동료·목표와 연결한다. 말하거나 쓴다. 아이스브레이커가 아니라 주제 관련 활동
- Concept: 학습자가 need-to-know 정보를 듣고·보고·쓰고·말한다. 한 슬라이드 10분 이하
- Review: 10분 강의 사이에 끼우는 1~2분 전원 참여 복습
- Concrete Practice: 전원이 직접 한다. 시연을 보는 것은 실습이 아니다
- Conclusion: 학습자가 요약·평가·실행 계획을 쓴다. 강사가 요약하지 않는다

## 설계 규칙 (반드시 지킬 것)
1. outcome은 관찰 가능한 동사로 쓴다. "이해한다/안다/배운다/숙지한다" 금지.
   사용: 설명한다, 작성한다, 시연한다, 나열한다, 구분한다, 적용한다, 남에게 가르친다
2. Concept 한 슬라이드는 10분 이하. 넘으면 나누고 사이에 ## Review 를 넣는다
3. Connect, Concept, Conclusion에도 학습자 활동(activity: 또는 pattern:)을 넣는다
4. Concrete Practice는 전원 참여 + 짝/소그룹 상호의존 + 각자 결과물
5. Conclusion은 학습자가 요약한다. 과정 마지막 Conclusion에는 action_plan: 을 넣는다
6. need-to-know만 슬라이드에. nice-to-know는 handout: 에
7. 활동은 아래 카탈로그 ID를 pattern: 에 쓴다. 없으면 activity: 에 직접 서술

## 활동 카탈로그 (pattern: 에 쓸 ID)
- Connect: standing-survey, wall-writing, table-talk, turn-and-talk, think-write-share, fast-pass-wiifm
- Concept: interactive-lecture, concept-map, graphic-organizer, three-before-me, jigsaw(새 내용, 20분+)
- Review: turn-and-talk, pass-that-card, rapid-response, stand-stretch-speak, body-break(온라인), chat-blast(온라인)
- Concrete Practice: paired-practice, skills-rounds, teach-back(배운 내용), improv-scenario, learner-created-game
- Conclusion: learning-log, card-exchange, where-do-you-stand, four-square-feedback, public-action-plan, email-blast
(온라인이면 standing-survey, pass-that-card, stand-stretch-speak, card-exchange, learner-created-game 은 쓰지 않는다)

## 출력 형식 (정확히 지킬 것)

---
course: [과정명]
audience: [대상]
total_time: [분]분
outcome: [관찰 가능한 동사 + 개념]
mode: [offline/online]
---

# 모듈 1: [모듈 제목]
outcome: [관찰 가능한 동사 + 개념]

## Module Start
[20자 이내 한 줄]

## Connect
time: [3~5분]
title: [제목]
main: [강사가 보여줄 한 줄]
pattern: [카탈로그 ID]
params:
  question: [학습자가 서로 나눌 질문]
  debrief: [디브리프 방식]
alt: [대체 활동 ID 1~2개]

## Concept
time: [≤10분]
title: [제목]
main: [핵심 한 문장]
sub: |
  - [포인트 1]
  - [포인트 2]
  - [포인트 3]
pattern: [concept-map / graphic-organizer / interactive-lecture]
params:
  [키]: [값]
handout: |
  [슬라이드에서 뺀 nice-to-know]

## Review
time: 2분
title: [제목]
pattern: [Review 활동 ID]
params:
  question: [질문]

## Concrete Practice
time: [10~20분]
title: [제목]
main: [과제 한 줄]
pattern: [Practice 활동 ID]
params:
  [키]: [값]
activity: |
  1. [단계 — 누가 무엇을, 몇 분]
  2. [역할 교대]
  3. [결과 비교]
notes: |
  관찰 포인트: [강사가 볼 것]

## Conclusion
time: [3~5분]
title: [제목]
main: [학습자에게 줄 지시 한 줄]
pattern: [Conclusion 활동 ID]
params:
  topic: [모듈 주제]
action_plan: [과정 마지막 모듈만. 기한 + 행동 + 누구에게 말할지]

## Break
time: [분]
sub: [다음 모듈 예고 15자 이내]

---

# 모듈 2: [제목]
[같은 구조 반복]

🚨 형식 규칙
- 각 필드는 별도의 줄. 한 줄에 두 필드 금지
- 여러 줄 값은 `|` 뒤에 두 칸 들여쓰기
- 필드명을 바꾸지 않는다 (time, title, main, sub, activity, pattern, params, alt, notes, handout, action_plan)
- Module Start는 20자 이내

총 [n]개 모듈을 작성해주세요.
```

---

## 🎯 주제별 맞춤 프롬프트

기본 프롬프트 뒤에 붙입니다.

### 1. 프로그래밍 교육

```
주제: Python 기초 - 변수와 데이터 타입
모듈 3개: 변수의 개념 / 데이터 타입 / 변수 활용

각 모듈마다:
- Connect: 일상의 "이름표 붙이기" 경험을 학습자끼리 나눈다 (standing-survey 또는 turn-and-talk)
- Concept: 코드 예시 포함. 학습자는 concept-map을 그리며 듣는다
- Concrete Practice: paired-practice. 역할 교대로 둘 다 코드를 친다
- Conclusion: learning-log. 마지막 모듈은 action_plan 포함
```

### 2. 비즈니스/업무 교육

```
주제: Excel 피벗 테이블 활용
모듈 2개: 피벗 테이블 기본 / 데이터 분석 실습

각 모듈마다:
- Connect: 데이터 정리에서 겪은 불편을 wall-writing으로 모은다
- Concept: graphic-organizer(비교표)를 채우며 듣는다
- Concrete Practice: skills-rounds. 같은 데이터로 3라운드, 조건을 바꿔가며
- Conclusion: where-do-you-stand로 자신감 자가 평가
```

### 3. 소프트 스킬 교육

```
주제: 효과적인 프레젠테이션 기법
모듈 4개: 청중 분석 / 스토리텔링 / 슬라이드 디자인 / 발표 연습

각 모듈마다:
- Connect: 나쁜 프레젠테이션 경험을 table-talk로 나눈다
- Concept: interactive-lecture. 10분마다 Review
- Concrete Practice: improv-scenario 또는 teach-back
- Conclusion: public-action-plan (다음 발표에 적용할 것 1가지)
```

---

## 🔧 고급 프롬프트 (상세 제어)

```
당신은 교육 설계자입니다. 아래 요구사항과 설계 규칙에 맞춰 4C 교육 콘텐츠를 작성해주세요.

## 기본 정보
- 주제: [주제명]
- 대상: [초급/중급/고급, 사전 지식]
- 과정 outcome: [관찰 가능한 동사 + 개념]
- 총 시간: [분]
- 모드: [offline/online]
- 인원: [n명]

## 구조 요구사항
- 모듈 수: [2~5개]
- 모듈당 시간: [30~50분]
- Concept는 10분 이하 단위, 사이에 Review
- Practice는 전체 시간의 1/3 이상
- 강사 발화는 전체의 1/3 이하

## 톤앤매너
- [전문적 / 친근한 / 격식있는]

## 특별 요청
- [예: 한국 상황에 맞는 예시]
- [예: 기업 교육용]

[기본 프롬프트의 "설계 규칙", "활동 카탈로그", "출력 형식"을 그대로 붙여넣기]
```

---

## ✅ 생성 후 할 일

1. 결과를 `course.md` 로 저장
2. 검증: `python scripts/validate_markdown_v3.py --md course.md`
   - error → 형식 수정
   - warning → 설계 권고. `templates/review_checklist.md` 로 검토
3. 활동 교체: `python scripts/swap_activity.py --md course.md --at "모듈1/Connect#1" --list`
4. 빌드: `python scripts/generate_with_master_layout.py --md course.md --template pptx-templates/default_4c_template.pptx --output result.pptx`

## 💡 수정 요청 예시

| 증상 | 요청 |
|---|---|
| Connect가 질문으로만 끝남 | "Connect에 학습자가 옆 사람과 답을 나누는 pattern: turn-and-talk 를 넣어줘" |
| Concept 15분 | "Concept를 8분·7분으로 나누고 사이에 ## Review 2분(pass-that-card)을 넣어줘" |
| Practice가 시연 관람 | "전원이 직접 하는 paired-practice로 바꾸고 역할 교대를 명시해줘" |
| Conclusion을 강사가 요약 | "학습자가 카드에 쓰는 learning-log로 바꿔줘" |
| outcome에 "이해한다" | "관찰 가능한 동사로 바꿔줘" |
| 슬라이드 글이 너무 많음 | "sub를 3개 포인트로 줄이고 나머지는 handout: 으로 옮겨줘" |
