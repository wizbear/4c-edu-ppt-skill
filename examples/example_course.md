---
course: Python 프로그래밍 기초
audience: 프로그래밍 경험이 없는 신입사원
total_time: 170분
outcome: 변수·데이터 타입·조건문을 사용해 20줄 이내의 Python 프로그램을 작성하고 옆 사람에게 설명한다
mode: offline
group_size: 20
strict: false
---

# 모듈 1: Python 시작하기
outcome: 변수를 선언하고 값을 출력하는 코드를 직접 작성한다

## Module Start
Python의 첫걸음

## Connect
time: 5분
title: 기계에 명령해 본 적 있나요?
main: 리모컨, 내비게이션, 알람. 우리는 이미 기계에 명령을 내리고 있습니다.
pattern: standing-survey
params:
  question: 오늘 아침 기계에 내린 명령 1가지는?
  debrief: 공통 답 2개를 칠판에 적고 "프로그래밍도 같은 것"으로 연결
alt: turn-and-talk, wall-writing
notes: |
  준비물: 없음. 이동 공간 확보
  디브리프 질문: "그 명령을 기계가 어떻게 알아들었을까요?"
  시간 큐: 3분 경과 시 "1분 남았습니다"

## Concept
time: 8분
title: Python과 변수
main: 변수는 값에 붙이는 이름표입니다
sub: |
  name = "홍길동"
  age = 25

  변수명 = 값
pattern: concept-map
params:
  topic: 변수
handout: |
  Python 역사: 1991년 귀도 반 로섬이 개발. 이름은 코미디 그룹 Monty Python에서 따옴.
  주요 활용: 데이터 분석, 인공지능, 웹 백엔드, 자동화 스크립트.
  참고: python.org/about

## Review
time: 2분
title: 잠깐 정리
pattern: turn-and-talk
params:
  question: 변수를 한 문장으로 설명하면?

## Concept
time: 7분
title: 값을 화면에 보여주기
main: print() 는 괄호 안의 값을 화면에 출력합니다
sub: |
  print("안녕")
  print(name)
  print(f"이름: {name}, 나이: {age}")
activity: |
  강의 중 2번 멈춤:
  1. "print(age) 는 무엇을 출력할까요?" 옆 사람과 답 맞추기 (30초)
  2. f-string 예시를 보고 자기 이름으로 바꿔 적기 (30초)

## Concrete Practice
time: 15분
title: 나를 소개하는 프로그램
main: 이름·나이·좋아하는 음식을 변수에 담아 출력합니다
pattern: paired-practice
params:
  task: 변수 3개를 만들고 f-string으로 한 줄 소개 출력
  half: 5
activity: |
  짝 실습 (전원 참여):
  1. A가 입력, B가 말로 돕기 (5분): name, age, food 변수 만들고 print로 출력
  2. 역할 교대 (5분): B가 입력. 이번엔 f-string 한 줄로 출력
  3. 둘이 결과를 비교하고 다른 점 1가지 메모 (2분)
  4. 막힌 짝은 손들기. 강사가 순회
notes: |
  준비물: Python 설치 확인, 에디터 열기
  관찰 포인트: 따옴표 누락, 변수명 띄어쓰기
  막히는 짝이 3팀 이상이면 전체 멈추고 1분 시연

## Conclusion
time: 4분
title: 내가 배운 것
main: 카드에 오늘 배운 것 3가지를 씁니다
pattern: learning-log
params:
  topic: 변수와 print
notes: |
  강사가 요약하지 않는다. 학습자가 쓴 것 중 2~3개를 읽어 주는 것으로 마무리.

## Break
time: 10분
sub: 다음 모듈에서는 숫자와 문자를 구분합니다

---

# 모듈 2: 데이터 타입
outcome: 정수·실수·문자열·불린 값을 구분하고 type()으로 확인한다

## Module Start
데이터의 종류

## Connect
time: 4분
title: 같은 숫자, 다른 쓰임
main: 전화번호 010-1234-5678 은 숫자일까요, 문자일까요?
pattern: think-write-share
params:
  question: 전화번호에 1을 더하면 무슨 일이 생길까?
alt: turn-and-talk, rapid-response

## Concept
time: 10분
title: 기본 데이터 타입 4가지
main: 값의 종류에 따라 할 수 있는 일이 다릅니다
sub: |
  정수 int   : 1, 2, -10
  실수 float : 3.14, -0.5
  문자열 str : "안녕", '010-1234'
  불린 bool  : True, False
pattern: graphic-organizer
params:
  organizer: 4칸 비교표 (타입 / 예시 / 할 수 있는 연산 / 못 하는 것)
handout: |
  그 밖의 타입: list(여러 값), dict(키-값), tuple(바꿀 수 없는 list), set(중복 없는 모음)
  형 변환: int("3") → 3, str(3) → "3", float("3.5") → 3.5

## Review
time: 2분
title: 속사포 퀴즈
pattern: rapid-response
params:
  question: 다음 값의 타입은? "3", 3, 3.0, True

## Concept
time: 8분
title: 리스트와 딕셔너리
main: 여러 값을 한 변수에 담습니다
sub: |
  foods = ["피자", "김밥", "라면"]
  person = {"이름": "홍길동", "나이": 25}
activity: |
  각자 노트에: 내가 좋아하는 음식 3개로 리스트 쓰기, 내 정보로 딕셔너리 쓰기 (2분)
  옆 사람과 교환해 문법 오류 찾아주기 (1분)

## Concrete Practice
time: 20분
title: 타입 탐정
main: 값을 만들고 type()으로 정체를 밝힙니다
pattern: skills-rounds
params:
  skill: 값 만들기 → type() 확인 → 예측과 비교
  rounds: 3
  round_min: 5
activity: |
  3라운드, 라운드마다 역할 교대:
  R1 (5분): 정수·실수·문자열 각 1개 만들고 type() 출력. 관찰자는 출력 전 예측을 말한다
  R2 (5분): 리스트 만들고 요소 추가(append), 딕셔너리에서 값 꺼내기
  R3 (5분): "3" + 3 을 실행해 오류 메시지를 읽고 원인을 한 줄로 쓴다
  마무리 (5분): 라운드마다 예측이 틀린 것 1개씩 짝과 정리

## Conclusion
time: 5분
title: 카드 교환
main: 가장 헷갈렸던 타입 1가지와 구분법을 카드에 씁니다
pattern: card-exchange
params:
  topic: 데이터 타입
notes: |
  마지막에 손에 든 카드 3장을 읽어 준다. 다음 모듈 예고는 Break 슬라이드에.

## Break
time: 10분
sub: 다음 모듈: 프로그램이 스스로 판단하기

---

# 모듈 3: 조건문
outcome: if-elif-else로 입력값에 따라 다른 결과를 출력하는 프로그램을 작성한다

## Module Start
프로그램의 선택

## Connect
time: 4분
title: 비가 오면 우산
main: 우리는 하루에도 수십 번 "~하면 ~한다"를 실행합니다
pattern: wall-writing
params:
  question: 오늘 내가 한 "~하면 ~한다" 결정 1가지
alt: standing-survey, table-talk

## Concept
time: 10분
title: if 문의 구조
main: 조건이 참이면 들여쓴 블록을 실행하고, 거짓이면 건너뜁니다
sub: |
  if age >= 18:
      print("성인")
  elif age >= 13:
      print("청소년")
  else:
      print("어린이")
pattern: interactive-lecture
params:
  prompt: 이 코드에 age = 15 를 넣으면? 옆 사람과 답 맞추기

## Review
time: 2분
title: 일어서서 말하기
pattern: stand-stretch-speak
params:
  topic: if / elif / else 의 차이

## Concrete Practice
time: 20분
title: 성적 등급 프로그램
main: 점수를 입력받아 A~F 등급을 출력합니다
pattern: paired-practice
params:
  task: 점수 → 등급 변환 프로그램 (90 A / 80 B / 70 C / 60 D / 그 외 F)
  half: 8
activity: |
  1. A가 입력, B가 돕기 (8분): if-elif-else 로 등급 출력
  2. 교대 (8분): B가 입력. 경계값(90, 89, 60, 59)으로 테스트
  3. 짝끼리 다른 짝과 프로그램 교환해 경계값 테스트 (4분)
notes: |
  관찰 포인트: 비교 순서(큰 값부터), 들여쓰기, elif 와 if 혼동
  모든 짝이 끝나기 전에 멈추지 않는다. 빠른 짝에게는 "점수가 100 초과면 오류 메시지" 추가 과제

## Conclusion
time: 6분
title: 어디에 서 있나요
main: 오늘의 성과 문장에 대해 1(전혀)에서 5(확실히)까지 자리에 섭니다
pattern: where-do-you-stand
params:
  statement: 나는 if-elif-else 로 조건에 따라 다른 결과를 출력하는 프로그램을 작성할 수 있다
action_plan: 다음 주에 내 업무에서 "~하면 ~한다"를 코드로 바꿀 것 1가지를 카드에 쓰고 옆 사람에게 말한다
notes: |
  마지막 5분은 학습자 몫. 강사 요약 없음.
  양 끝에 선 사람에게 이유를 묻고, 1~2에 선 사람은 다음 회차 전에 짝 복습을 권한다.
  모듈 1에서 쓴 Fast Pass 카드가 있다면 지금 다시 보게 한다.
