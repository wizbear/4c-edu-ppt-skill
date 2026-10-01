# 단계별 AI 콘텐츠 생성 프롬프트

> 전체를 한번에 생성하면 품질이 떨어집니다. 단계별로 나눠 생성하고 검토하세요.
> 두 가지 경로가 있습니다. **역방향(권장)** 은 Bowman의 "끝에서 시작하기" 설계 순서이고, **순차** 는 전달 순서 그대로입니다.
> 어느 경로든 최종 Markdown은 전달 순서(Connect → Concept → Practice → Conclusion)로 배열합니다.

---

## 공통 설계 규칙 (모든 프롬프트 앞에 붙이기)

```
## 설계 규칙 (반드시 지킬 것)
1. 각 단계는 "학습자가 하는 행동"으로 쓴다. 강사가 말할 내용이 아니다.
2. outcome은 관찰 가능한 동사로 쓴다. "이해한다 / 안다 / 배운다 / 숙지한다" 금지.
   예: 설명한다, 작성한다, 시연한다, 나열한다, 구분한다, 남에게 가르친다
3. Concept 한 슬라이드는 10분 이하. 10분이 넘으면 나누고 사이에 ## Review (1~2분 전원 활동)를 넣는다.
4. Connect는 질문만 던지지 않는다. 학습자가 말하거나 쓰는 활동(activity: 또는 pattern:)을 넣는다.
5. Concrete Practice는 전원이 직접 한다. 시연을 보는 것은 실습이 아니다. 역할 교대로 모두 하게 한다.
6. Conclusion은 학습자가 요약한다. 강사가 "오늘 배운 것" 을 정리하지 않는다.
7. need-to-know만 슬라이드에 넣는다. nice-to-know는 handout: 에 넣는다.
8. 활동은 가능하면 카탈로그 ID(pattern:)로 지정한다. 목록: references/activities.md
```

---

## 경로 A: 역방향 설계 (권장)

### Phase 0: 성과와 대상 정하기

```
다음 과정의 프론트매터와 모듈별 outcome을 작성해주세요.

- 과정명: [주제]
- 대상: [누구, 사전 지식]
- 총 시간: [분]
- 모듈 수: [n]

출력:
---
course: ...
audience: ...
total_time: ...분
outcome: [관찰 가능한 동사 + 개념]
mode: offline
---

# 모듈 1: [제목]
outcome: [관찰 가능한 동사 + 개념]

# 모듈 2: ...
```

**검토 포인트:** 제3자가 보고 "했다/못 했다"를 판정할 수 있는가? "이해한다"가 없는가?

### Phase 1: Concrete Practice 먼저

```
모듈 1의 outcome "[outcome]"을 달성했는지 드러나는 실습을 설계해주세요.

조건
- 전원 참여, 상호의존(짝 또는 소그룹), 개인 책임(각자 결과물)
- 시간: [분]
- 모드: [offline/online]
- 가능하면 pattern: paired-practice | skills-rounds | teach-back | improv-scenario 중 선택

출력 형식
## Concrete Practice
time: [분]
title: [제목]
main: [한 줄 과제 설명]
pattern: [ID]
params:
  [키]: [값]
activity: |
  1. ...
  2. ...
notes: |
  관찰 포인트: ...
```

**검토 포인트:** 지켜보기만 하는 사람이 있는가? 실습 결과로 outcome 달성 여부를 알 수 있는가?

### Phase 2: Concept — 실습에 필요한 것만

```
위 실습을 하기 위해 학습자가 반드시 알아야 하는 것(need-to-know)만 Concept로 작성해주세요.
"시간이 절반이면 무엇을 자르겠는가"를 기준으로 거릅니다. 잘라낸 것은 handout: 에.

조건
- Concept 하나당 10분 이하. 넘으면 둘로 나누고 사이에 ## Review
- 각 Concept에 학습자가 듣기 외에 하는 것 1가지 (activity: 또는 pattern: concept-map / graphic-organizer / interactive-lecture)

출력 형식
## Concept
time: [≤10분]
title:
main: [한 문장]
sub: |
  - 포인트 (3~5개)
pattern: [ID] 또는 activity: |
handout: |
  [nice-to-know]

## Review
time: 2분
title:
pattern: turn-and-talk | pass-that-card | rapid-response | stand-stretch-speak
params:
  question: ...
```

**검토 포인트:** 이 Concept 없이 실습이 불가능한가? 아니면 handout으로.

### Phase 3: Connect

```
모듈 1의 주제 "[주제]"와 학습자의 경험을 연결하는 Connect를 작성해주세요.
아이스브레이커가 아니라 주제와 직접 관련된 활동이어야 합니다.

조건
- 학습자가 말하거나 쓴다. 강사의 수사적 질문만으로 끝나지 않는다
- 시간: 3~5분
- pattern: standing-survey | turn-and-talk | wall-writing | think-write-share | table-talk 중 선택
- 디브리프 방식을 params 또는 notes에

출력 형식
## Connect
time:
title:
main: [강사가 보여줄 한 줄]
pattern:
params:
  question:
  debrief:
alt: [대체 활동 1~2개]
```

### Phase 4: Conclusion

```
모듈 1의 Conclusion을 작성해주세요. 학습자가 요약합니다.

조건
- pattern: learning-log | card-exchange | where-do-you-stand | four-square-feedback 중 선택
- 과정 마지막 모듈이면 action_plan: 추가 (기한 + 행동 + 누구에게 말할지)
- 시간: 3~5분

출력 형식
## Conclusion
time:
title:
main: [학습자에게 줄 지시 한 줄]
pattern:
params:
action_plan: [마지막 모듈만]
notes: |
  강사가 요약하지 않는다. ...
```

### Phase 5: 조립과 검증

Module Start(20자 이내) → Connect → Concept(Review 포함) → Concrete Practice → Conclusion → Break 순으로 배열한 뒤:

```bash
python scripts/validate_markdown_v3.py --md course.md
```

warning이 뜨면 해당 Phase로 돌아가 수정.

---

## 경로 B: 순차 생성 (초보자용)

전달 순서대로 Module Start → Connect → Concept → Practice → Conclusion 을 생성합니다. 각 Phase의 출력 형식과 검토 포인트는 경로 A와 같고, 순서만 다릅니다. 단, 시작 전에 Phase 0(outcome)은 반드시 먼저 합니다. 성과 없이 Connect부터 쓰면 need-to-know를 거를 기준이 없습니다.

---

## 모듈 2, 3… 반복

각 모듈마다 Phase 0~5 반복. 모듈 간 연결은 Break 슬라이드의 `sub:` 에 다음 모듈 예고 한 줄.

## 자주 생기는 문제

| 증상 | 수정 요청 |
|---|---|
| Connect가 "~해본 적 있나요?" 로 끝남 | "학습자가 옆 사람에게 답을 말하는 활동으로 바꿔줘. pattern: turn-and-talk" |
| Concept 15분 | "두 개로 나누고 사이에 ## Review 2분을 넣어줘" |
| Practice가 "강사 시연을 봅니다" | "전원이 직접 하도록 짝 실습으로 바꿔줘. 역할 교대 포함" |
| Conclusion에 "오늘 배운 내용 ✓ ..." | "학습자가 카드에 쓰는 learning-log로 바꿔줘" |
| outcome에 "이해한다" | "관찰 가능한 동사로 바꿔줘: 작성한다, 설명한다, 시연한다" |
