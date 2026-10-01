# 4C 활동 카탈로그

> 자동 생성 파일. 원본은 `activities.json` (v1.1.0). 수정은 JSON에 하고 `python scripts/build_activity_catalog.py`로 재생성.
> 활동 이름은 Bowman, *Training From the Back of the Room!* 기준. 설명은 자체 요약이며 책 본문을 옮기지 않았다.

## 사용법

```markdown
## Connect
time: 5분
title: 첫 명령의 기억
main: 기계에 명령해 본 경험
pattern: standing-survey
params:
  question: 기계에 명령해 본 경험은?
  debrief: 3명 발표
alt: turn-and-talk, wall-writing
```

- `pattern:` 만 쓰면 아래 템플릿에 `params`를 채워 슬라이드 활동 블록과 강사 노트가 생성된다.
- `activity:` 를 직접 쓰면 그것이 우선한다.
- 교환: `python scripts/swap_activity.py --md course.md --at "모듈1/Connect#1" --list`

## 교환 규칙

| 상황 | 처리 |
|---|---|
| same_stage_same_group | 자유 교환. 시간·모드·인원만 재검증 |
| same_stage_other_group | 허용. 목적 차이 경고 |
| other_stage | 대상 패턴의 also_ok에 현재 stage가 있을 때만 |
| never_swap_with | 항상 거부 |

## Connect (연결) — 학습자가 주제·동료·목표와 연결한다

| ID | 이름 | 시간(분) | 인원 | 모드 | 교환 그룹 | 다른 단계 허용 | 요약 | 출처 |
|---|---|---|---|---|---|---|---|---|
| `fast-pass-dot-vote` | 입장 투표 (Fast Pass: Dot Voting) | 1~3 | 전체 | offline | pre-topic | - | 입장하면서 벽 차트의 선택지에 스티커를 붙여 사전 지식이나 관심을 표시한다. 강사 없이 자동 진행. | ch06 |
| `fast-pass-wiifm` | 입장 기대 카드 (Fast Pass: WIIFM Card) | 1~3 | 개인 | offline/online | self-reflect | - | 입장 시 "이 과정에서 얻고 싶은 것 1가지"를 카드나 채팅에 쓴다. 나중에 Conclusion에서 다시 꺼낸다. | ch06 |
| `standing-survey` | 서서 하는 설문 (Standing Survey) | 3~7 | 전체 | offline | social-share | review | 일어서서 돌아다니며 3명에게 같은 질문을 하고 답을 메모한다. 끝나면 전체 디브리프. | ch07 |
| `wall-writing` | 벽에 쓰기 (Wall Writing) | 3~7 | 전체 | offline/online | social-share | review | 벽 차트(온라인은 공유 보드)에 질문별로 아는 것·궁금한 것을 쓰고 서로 읽는다. | ch07 |
| `table-talk` | 테이블 토크 (Table Talk) | 3~10 | 소그룹 | offline/online | social-share | review, conclusion | 테이블(소회의실)별로 주제 질문에 답을 나누고 대표가 한 가지를 전체에 공유한다. | ch07 |
| `turn-and-talk` | 옆 사람과 말하기 (Turn and Talk) | 1~3 | 짝 | offline/online | social-share | conclusion | 옆 사람과 짝을 지어 질문 하나에 서로 답한다. 가장 짧고 어디서나 되는 활동. | ch10 |
| `think-write-share` | 생각-쓰기-나누기 (Think-Write-Share) | 2~5 | 짝 | offline/online | self-reflect | review, conclusion | 혼자 생각하고 한 줄 쓴 뒤 짝과 나눈다. 말하기 전에 쓰기 때문에 조용한 학습자도 참여한다. | ch07 |

## Concept (개념) — 학습자가 need-to-know 정보를 듣고·보고·쓰고·말한다

| ID | 이름 | 시간(분) | 인원 | 모드 | 교환 그룹 | 다른 단계 허용 | 요약 | 출처 |
|---|---|---|---|---|---|---|---|---|
| `interactive-lecture` | 상호작용 강의 (Interactive Lecture) | 5~10 | 전체 | offline/online | lecture-chunk | - | 10분 이내 강의 뒤 1~2분 전원 참여 활동을 끼운다. 10분 규칙의 기본형. | ch10 |
| `three-before-me` | 나보다 셋 먼저 (Three Before Me) | 1~3 | 전체 | offline/online | lecture-chunk | review | 강의 중 질문이 나오면 강사가 답하기 전에 학습자 3명의 답을 먼저 듣는다. | ch08 |
| `concept-map` | 개념 지도 그리기 (Concept Map) | 5~15 | 개인 | offline/online | note-taking | conclusion | 강의를 들으며 중앙 개념에서 가지를 뻗어 그림과 선으로 지도를 그린다. 강의 후가 아니라 강의 중에 그린다. | ch09 |
| `graphic-organizer` | 빈칸 구조도 (Graphic Organizer) | 5~15 | 개인 | offline/online | note-taking | - | 표·흐름도·비교표 같은 빈칸 틀을 주고 강의를 들으며 채운다. 슬라이드 복사본 대신 쓴다. | ch08 |
| `jigsaw` | 직소 (Jigsaw) | 20~40 | 소그룹 | offline/online | peer-teach-new | - | 새 내용을 조각으로 나눠 각자 익힌 뒤 서로 가르친다. 강사는 돌아다니며 관찰만 한다. 새 내용 전용. **교환 금지: teach-back** | ch11 |
| `concept-centers` | 개념 센터 순회 (Concept Centers) | 30~90 | 소그룹 | offline | rotation | practice | 목적이 적힌 센터 4~9개를 두고 소그룹이 신호에 따라 돌며 내용을 익힌다. 하루 이상 과정용. | ch12 |

## Review (리뷰) — 10분 강의 사이에 끼우는 1~3분 전원 참여 활동

| ID | 이름 | 시간(분) | 인원 | 모드 | 교환 그룹 | 다른 단계 허용 | 요약 | 출처 |
|---|---|---|---|---|---|---|---|---|
| `turn-and-talk` | 옆 사람과 말하기 (Turn and Talk) | 1~3 | 짝 | offline/online | social-share | conclusion | 옆 사람과 짝을 지어 질문 하나에 서로 답한다. 가장 짧고 어디서나 되는 활동. | ch10 |
| `pass-that-card` | 카드 돌리기 (Pass That Card) | 1~3 | 전체 | offline | quick-review | conclusion | 방금 배운 것 1가지를 카드에 쓰고 옆으로 넘긴다. 받은 카드를 읽고 하나 더 쓴다. | ch10 |
| `stand-stretch-speak` | 일어서서 말하기 (Stand, Stretch, Speak) | 1~2 | 전체 | offline | movement-review | - | 모두 일어나 스트레칭하고 옆 사람에게 핵심 1가지를 말한 뒤 앉는다. 움직임과 복습을 동시에. | ch10 |
| `rapid-response` | 속사포 응답 (Rapid Response) | 1~3 | 전체 | offline/online | quick-review | conclusion | 강사가 질문을 던지면 전원이 동시에 외치거나 채팅에 쓴다. 틀려도 되는 분위기가 핵심. | ch10 |
| `body-break` | 몸 풀기 (Body Break) | 1~2 | 개인 | online/offline | movement-review | - | 화면 앞에서 일어나 몸을 풀며 핵심 1가지를 소리 내어 말한다. 온라인 10분 규칙용. | ch24 |
| `chat-blast` | 채팅 폭탄 (Chat Blast) | 1~2 | 전체 | online | quick-review | conclusion | 신호와 함께 전원이 채팅에 답을 동시에 보낸다. 온라인 전용 전원 참여 리뷰. | ch24 |

## Concrete Practice (실습) — 전원이 직접 한다. 보는 것은 실습이 아니다

| ID | 이름 | 시간(분) | 인원 | 모드 | 교환 그룹 | 다른 단계 허용 | 요약 | 출처 |
|---|---|---|---|---|---|---|---|---|
| `teach-back` | 되가르치기 (Teach-Back) | 5~15 | 짝 | offline/online | peer-teach-known | - | 이미 배운 내용을 짝이나 소그룹에게 가르친다. 강사는 관찰하며 재교육이 필요한 부분을 찾는다. 배운 내용 전용. **교환 금지: jigsaw** | ch14 |
| `skills-rounds` | 반복 라운드 (Rounds and Repetition) | 10~30 | 짝 | offline/online | hands-on | - | 같은 기술을 짧은 라운드로 여러 번 연습한다. 라운드마다 역할을 바꾸고 조건을 조금씩 바꾼다. | ch15 |
| `paired-practice` | 짝 실습 (Paired Practice) | 10~30 | 짝 | offline/online | hands-on | - | 한 명이 하고 한 명이 보며 말로 돕는다. 중간에 역할을 바꿔 둘 다 직접 한다. 지켜보기만 하는 사람이 없다. | ch13 |
| `in-room-mentoring` | 현장 멘토링 (In-Room Mentoring) | 10~30 | 짝 | offline | hands-on | - | 경험자와 초보자를 짝지어 초보자가 시연하고 경험자가 코칭한다. 수준 차이가 큰 반에서 쓴다. | ch15 |
| `improv-scenario` | 즉흥 시나리오 (Improv Scenario) | 10~20 | 소그룹 | offline/online | scenario | - | 실무 상황 시나리오를 받아 소그룹이 즉흥으로 대응한다. '역할극' 대신 '즉흥'이라 부르면 참여율이 오른다. | ch14 |
| `learner-created-game` | 학습자 제작 게임 (Learner-Created Game) | 15~30 | 소그룹 | offline | game | - | 소그룹이 배운 내용으로 퀴즈 게임을 만들고 다른 그룹과 교환해 푼다. 만드는 쪽이 더 많이 배운다. | ch16 |

## Conclusion (정리) — 학습자가 요약·평가·실행 계획·축하한다

| ID | 이름 | 시간(분) | 인원 | 모드 | 교환 그룹 | 다른 단계 허용 | 요약 | 출처 |
|---|---|---|---|---|---|---|---|---|
| `learning-log` | 학습 일지 (Learning Log) | 2~5 | 개인 | offline/online | self-summary | review | 배운 것 3줄과 적용할 것 1줄을 각자 쓴다. 강사가 요약하지 않고 학습자가 요약한다. | ch18 |
| `card-exchange` | 카드 교환 (Card Exchange) | 3~5 | 전체 | offline | social-summary | review | 핵심 1가지를 카드에 쓰고 돌아다니며 카드를 교환한다. 받은 카드를 읽고 다시 교환. 여러 사람의 요약을 본다. | ch18 |
| `where-do-you-stand` | 어디에 서 있나요 (Where Do You Stand?) | 2~5 | 전체 | offline/online | evaluation | connect | 자신감이나 이해도를 공간의 위치(온라인은 투표)로 표시한다. 학습자 스스로 학습을 평가한다. | ch19 |
| `four-square-feedback` | 4칸 피드백 (Four-Square Feedback) | 3~5 | 개인 | offline/online | evaluation | - | 종이를 4칸으로 접어 배운 것·적용할 것·아직 궁금한 것·강사에게 한마디를 쓴다. 학습을 평가하지 강사를 평가하지 않는다. | ch19 |
| `public-action-plan` | 공개 실행 계획 (Public Action Plan) | 3~5 | 짝 | offline/online | commitment | - | 적용 계획을 쓰고 서명·날짜를 적은 뒤 옆 사람에게 말한다. 남에게 말하면 실행률이 오른다. | ch17 |
| `email-blast` | 나에게 메일 보내기 (Email Blast) | 2~4 | 개인 | online/offline | commitment | - | 배운 것과 적용 계획을 자신에게 메일로 보낸다. 2주 뒤 받도록 예약하면 더 좋다. | ch19 |
| `celebration-certificate` | 축하 (Celebration) | 2~5 | 전체 | offline/online | celebrate | - | 서로의 성취를 짧게 축하한다. 박수, 한 줄 칭찬, 수료증 전달 등. 과정 마지막에 한 번. | ch20 |

## 템플릿과 파라미터

### `fast-pass-dot-vote` — 입장 투표

파라미터:
- `question`: 벽 차트에 적을 질문 또는 선택지
준비물: 벽 차트, 스티커

```
입장하며 벽 차트 "{question}"에 스티커 1개를 붙인다.
시작 후 결과를 보며 가장 많은 선택을 한 사람 2명에게 이유를 묻는다.
```

### `fast-pass-wiifm` — 입장 기대 카드

파라미터:
- `topic`: 과정 또는 모듈 주제
준비물: 인덱스 카드 또는 채팅

```
입장하며 카드에 "{topic}에서 내가 얻고 싶은 것 1가지"를 쓴다.
카드는 책상에 두고 마지막 Conclusion에서 다시 본다.
```

### `standing-survey` — 서서 하는 설문

파라미터:
- `question`: 학습자끼리 주고받을 질문
- `debrief`: 디브리프 방식 (예: 3명 발표, 공통 답 찾기)
준비물: 이동 공간

```
일어서서 3명에게 "{question}"을 묻고 답을 메모한다 ({time}).
디브리프: {debrief}
```

### `wall-writing` — 벽에 쓰기

파라미터:
- `question`: 벽 차트 제목이 될 질문
준비물: 벽 차트 또는 공유 보드

```
벽 차트 "{question}"에 각자 한 줄씩 쓴다 ({time}).
다 쓰면 돌아다니며 읽고 공감하는 항목에 체크한다.
디브리프: 체크가 많은 항목 2개를 읽어준다.
```

### `table-talk` — 테이블 토크

파라미터:
- `question`: 테이블에서 나눌 질문
준비물: 소그룹 좌석 또는 소회의실

```
테이블별로 "{question}"에 답을 나눈다 ({time}).
테이블 대표가 가장 흥미로운 답 1개를 전체에 말한다.
```

### `turn-and-talk` — 옆 사람과 말하기

파라미터:
- `question`: 짝과 나눌 질문

```
옆 사람과 "{question}"에 대해 서로 1분씩 말한다.
디브리프: 자원자 3명이 짝의 답을 대신 말한다.
```

### `think-write-share` — 생각-쓰기-나누기

파라미터:
- `question`: 생각할 질문
준비물: 메모지

```
1분: 혼자 "{question}"을 생각하고 한 줄 쓴다.
1분: 짝과 쓴 것을 교환해 읽는다.
디브리프: 짝의 답 중 인상적인 것을 2~3명이 말한다.
```

### `interactive-lecture` — 상호작용 강의

파라미터:
- `prompt`: 강의 중 끼울 1분 질문 또는 지시

```
{time} 강의 중 핵심 포인트마다 멈추고 "{prompt}"를 던진다.
강의가 끝나면 바로 Review 슬라이드로 넘어간다.
```

### `three-before-me` — 나보다 셋 먼저

파라미터:
- `question`: 학습자에게 먼저 던질 질문

```
"{question}"을 던지고 강사가 답하기 전에 학습자 3명의 답을 먼저 듣는다.
세 답을 묶어 강사가 정리한다.
```

### `concept-map` — 개념 지도 그리기

파라미터:
- `topic`: 중앙에 둘 핵심 개념
준비물: 빈 종이 또는 디지털 캔버스

```
종이 중앙에 "{topic}"을 쓰고 강의를 들으며 가지를 뻗어 그린다.
강의 중 2번 멈춰 1분씩 그릴 시간을 준다.
끝나면 짝과 지도를 비교한다.
```

### `graphic-organizer` — 빈칸 구조도

파라미터:
- `organizer`: 구조도 형태 (예: 비교표, 흐름도, 3칸 요약)
준비물: 빈칸 구조도 유인물

```
유인물의 빈칸 "{organizer}"를 강의를 들으며 채운다.
강의 중 멈추는 지점마다 1분 채울 시간을 준다.
```

### `jigsaw` — 직소

파라미터:
- `topic`: 가르칠 새 내용
- `pieces`: 조각 수
준비물: 나눠 줄 자료 조각

```
{topic}을 {pieces}개 조각으로 나눈다.
1단계: 조각별 전문가 그룹이 자기 조각을 익히고 설명을 연습한다.
2단계: 홈 그룹으로 돌아가 각자 조각을 가르친다.
강사는 관찰하고 끝에 전체 자료를 나눠 준다.
```

### `concept-centers` — 개념 센터 순회

파라미터:
- `centers`: 센터 수
- `rotation`: 센터당 분
준비물: 센터별 테이블과 자료, 신호 도구

```
센터 {centers}개를 설치한다. 각 센터에 목적과 지시문을 붙인다.
소그룹이 신호에 따라 {rotation}분마다 이동한다.
끝나면 전체 디브리프.
```

### `pass-that-card` — 카드 돌리기

파라미터:
- `topic`: 방금 다룬 내용
준비물: 인덱스 카드

```
카드에 방금 배운 "{topic}"에서 기억나는 것 1가지를 쓴다.
오른쪽으로 넘기고, 받은 카드에 1가지를 더 쓴다. 2번 반복.
마지막 카드를 몇 장 읽어 준다.
```

### `stand-stretch-speak` — 일어서서 말하기

파라미터:
- `topic`: 방금 다룬 내용

```
모두 일어선다. 스트레칭 10초.
옆 사람에게 "{topic}"에서 기억나는 것 1가지를 말한다.
둘 다 말했으면 앉는다.
```

### `rapid-response` — 속사포 응답

파라미터:
- `question`: 짧게 답할 수 있는 질문

```
"{question}"을 던진다. 전원이 동시에 답을 외친다(온라인은 채팅에 쓴다).
답이 갈리면 가장 많은 답을 고르고 이유를 1명에게 묻는다.
```

### `body-break` — 몸 풀기

파라미터:
- `topic`: 방금 다룬 내용

```
카메라 앞에서 일어나 몸을 푼다 (1분).
앉기 전에 "{topic}"의 핵심 1가지를 소리 내어 말하고 채팅에 한 단어로 쓴다.
```

### `chat-blast` — 채팅 폭탄

파라미터:
- `question`: 채팅으로 답할 질문
준비물: 채팅

```
"{question}"을 띄우고 10초 뒤 신호에 맞춰 전원이 채팅에 답을 보낸다.
강사가 눈에 띄는 답 3개를 읽어 준다.
```

### `teach-back` — 되가르치기

파라미터:
- `topic`: 이미 배운 내용

```
짝에게 "{topic}"을 2분 동안 가르친다. 역할을 바꿔 반복한다.
강사는 돌아다니며 막히는 지점을 메모하고 끝에 공통 오해 1~2개를 정리한다.
```

### `skills-rounds` — 반복 라운드

파라미터:
- `skill`: 연습할 기술
- `rounds`: 라운드 수
- `round_min`: 라운드당 분
준비물: 실습 도구

```
짝을 짓고 {rounds}라운드로 "{skill}"을 연습한다. 라운드당 {round_min}분.
라운드마다 실행자와 관찰자를 바꾼다. 관찰자는 잘한 점 1가지를 말한다.
```

### `paired-practice` — 짝 실습

파라미터:
- `task`: 실습 과제
- `half`: 역할당 분
준비물: 실습 도구

```
짝을 짓는다. A가 "{task}"를 하고 B는 말로만 돕는다 ({half}분).
역할을 바꿔 B가 한다 ({half}분).
끝나면 둘이 결과를 비교하고 다른 점 1가지를 적는다.
```

### `in-room-mentoring` — 현장 멘토링

파라미터:
- `task`: 시연할 과제
준비물: 긍정 피드백 문구 게시

```
경험자-초보자 짝을 짓는다.
초보자가 "{task}"를 시연하고 경험자는 게시된 피드백 문구로 코칭한다.
끝나면 경험자가 초보자의 잘한 점 1가지를 전체에 말한다.
```

### `improv-scenario` — 즉흥 시나리오

파라미터:
- `scenario`: 실무 상황 시나리오
준비물: 시나리오 카드

```
소그룹별로 시나리오 "{scenario}"를 받는다.
3분 준비 후 2분 즉흥 시연. 나머지는 잘한 점 1가지를 적는다.
디브리프: 적은 것을 돌아가며 읽는다.
```

### `learner-created-game` — 학습자 제작 게임

파라미터:
- `topic`: 배운 내용
- `count`: 문항 수
준비물: 카드, 타이머

```
소그룹별로 "{topic}"에 대한 퀴즈 {count}문항을 만든다 (10분).
옆 그룹과 교환해 푼다 (5분). 정답은 만든 그룹이 확인한다.
디브리프: 가장 어려웠던 문항 1개를 공유한다.
```

### `learning-log` — 학습 일지

파라미터:
- `topic`: 모듈 주제
준비물: 메모지

```
각자 쓴다 ({time}):
- "{topic}"에서 배운 것 3가지
- 다음 주에 적용할 것 1가지
옆 사람에게 적용할 것을 말한다.
```

### `card-exchange` — 카드 교환

파라미터:
- `topic`: 모듈 주제
준비물: 인덱스 카드

```
카드에 "{topic}"의 핵심 1가지를 쓴다.
일어나 돌아다니며 만나는 사람과 카드를 교환하고 읽는다. 3번 교환.
마지막에 손에 든 카드를 몇 명이 읽어 준다.
```

### `where-do-you-stand` — 어디에 서 있나요

파라미터:
- `statement`: 평가할 문장 (예: 나는 변수를 선언하고 출력할 수 있다)
준비물: 공간 또는 투표 도구

```
"{statement}"에 대해 1(전혀)에서 5(확실히)까지 공간에 선다(온라인은 투표).
양 끝에 선 사람 1명씩에게 이유를 묻는다.
```

### `four-square-feedback` — 4칸 피드백

파라미터: 없음
준비물: 4칸 양식

```
종이를 4칸으로 접고 쓴다 ({time}):
1. 배운 것  2. 적용할 것  3. 아직 궁금한 것  4. 다음에 더 하고 싶은 활동
제출하면 강사가 3번 칸을 모아 다음 시간에 답한다.
```

### `public-action-plan` — 공개 실행 계획

파라미터:
- `deadline`: 기한 (예: 다음 주 금요일)
준비물: 실행 계획 카드

```
카드에 쓴다: "나는 {deadline}까지 ______를 하겠다." 서명과 날짜를 적는다.
옆 사람에게 계획을 말하고 다시 읽을 날짜를 정한다.
```

### `email-blast` — 나에게 메일 보내기

파라미터:
- `topic`: 모듈 주제
준비물: 이메일

```
자신에게 메일을 보낸다. 제목: "{topic} 적용 계획".
본문: 배운 것 2줄, 적용할 것 1줄, 확인할 날짜.
가능하면 2주 뒤 발송 예약.
```

### `celebration-certificate` — 축하

파라미터:
- `extra`: 추가 요소 (예: 수료증 전달, 단체 사진) 또는 빈칸

```
옆 사람에게 "오늘 당신이 잘한 것 1가지"를 말한다.
전체 박수로 마친다. {extra}
```
