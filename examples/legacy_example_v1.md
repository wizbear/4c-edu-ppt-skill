# Python 프로그래밍 기초

---

# 모듈 1: Python 시작하기

## Module Start
Python 프로그래밍의 세계에 오신 것을 환영합니다!
이번 모듈에서는 Python의 기초를 배웁니다.

## Connect
time: 5분
title: 프로그래밍과의 첫 만남
main: 여러분은 컴퓨터에게 명령을 내려본 적이 있나요?
sub: 게임, 앱, 웹사이트 모두 프로그래밍으로 만들어집니다.

## Connect
time: 3분
title: Python은 어디에 사용될까?
main: YouTube, Instagram, Spotify... 모두 Python으로 만들어졌습니다!
sub: 데이터 분석, 인공지능, 웹 개발 등 다양한 분야에서 활용됩니다.

## Image
image: ./images/python_everywhere.png
caption: Python이 사용되는 곳들

## Concept
time: 10분
title: Python이란?
main: Python은 배우기 쉽고 강력한 프로그래밍 언어입니다
sub: |
  - 1991년 귀도 반 로섬이 개발
  - 읽기 쉬운 문법
  - 방대한 라이브러리
  - 활발한 커뮤니티

## Concept
time: 8분
title: 변수의 개념
main: 변수는 데이터를 저장하는 이름표입니다
sub: |
  name = "홍길동"
  age = 25

  변수명 = 값

## Video
video: ./videos/python_intro.mp4
description: Python 소개 영상 - 기본 개념과 역사
duration: 5분

## Concrete Practice
time: 15분
title: 첫 Python 프로그램 작성하기
main: "Hello, World!"를 출력해봅시다
activity: |
  실습 단계:
  1. Python 설치 확인
  2. 에디터 열기 (VS Code, PyCharm 등)
  3. 다음 코드 작성:
     print("Hello, World!")
  4. 실행하기 (F5 또는 Run 버튼)
  5. 결과 확인

## Concrete Practice
time: 20분
title: 변수 실습
main: 직접 변수를 만들고 사용해봅시다
activity: |
  과제:
  1. 자신의 이름을 name 변수에 저장
  2. 나이를 age 변수에 저장
  3. 좋아하는 음식을 food 변수에 저장
  4. print() 함수로 모두 출력하기

  예시 코드:
  name = "김코딩"
  age = 20
  food = "피자"
  print(f"이름: {name}, 나이: {age}, 좋아하는 음식: {food}")

## Conclusion
time: 5분
title: 모듈 1 정리
main: Python의 기초를 배웠습니다!
sub: |
  오늘 배운 내용:
  ✓ Python이 무엇인지
  ✓ 변수의 개념
  ✓ Hello World 출력
  ✓ 변수 선언과 사용

## Break

---

# 모듈 2: 데이터 타입

## Module Start
다양한 데이터 타입을 배워봅시다

## Connect
time: 5분
title: 숫자와 문자
main: 컴퓨터는 다양한 종류의 데이터를 다룹니다
sub: 숫자, 문자, 참/거짓... 각각 다르게 처리됩니다

## Concept
time: 12분
title: 기본 데이터 타입
main: Python의 주요 데이터 타입들
sub: |
  1. 정수 (int): 1, 2, 3, -10
  2. 실수 (float): 3.14, 2.5, -0.5
  3. 문자열 (str): "안녕", 'Hello'
  4. 불린 (bool): True, False

## Concept
time: 10분
title: 리스트와 딕셔너리
main: 여러 데이터를 한 번에 저장하기
sub: |
  리스트: [1, 2, 3, 4, 5]
  딕셔너리: {"이름": "홍길동", "나이": 25}

## Image
image: ./images/data_types.png
caption: Python 데이터 타입 정리

## Concrete Practice
time: 25분
title: 데이터 타입 실습
main: 다양한 데이터 타입을 사용해봅시다
activity: |
  실습 과제:
  1. 정수 변수 만들기
  2. 실수 변수 만들기
  3. 문자열 변수 만들기
  4. 리스트 만들고 요소 추가하기
  5. 딕셔너리 만들고 값 조회하기

  각 타입의 type() 함수로 확인하기

## Conclusion
time: 5분
title: 데이터 타입 마스터!
main: 다양한 데이터를 다룰 수 있게 되었습니다
sub: |
  다음 시간 예고:
  → 조건문으로 프로그램 제어하기
  → if, elif, else 배우기

## Break

---

# 모듈 3: 조건문

## Module Start
조건에 따라 다른 동작을 하는 프로그램을 만들어봅시다

## Connect
time: 5분
title: 선택의 순간
main: 비가 오면 우산을 쓰고, 안 오면 그냥 걷습니다
sub: 프로그램도 조건에 따라 다르게 행동할 수 있습니다

## Concept
time: 15분
title: if 문의 구조
main: 조건이 참이면 실행, 거짓이면 건너뜁니다
sub: |
  if 조건:
      실행할 코드

  예시:
  if age >= 18:
      print("성인입니다")

## Concrete Practice
time: 30분
title: 조건문 실습
main: 성적 등급 프로그램 만들기
activity: |
  과제: 점수에 따라 등급 출력하기

  90점 이상: A
  80점 이상: B
  70점 이상: C
  60점 이상: D
  60점 미만: F

  if-elif-else 사용하기

## Conclusion
time: 5분
title: 조건문 완료
main: 이제 프로그램이 스스로 판단할 수 있습니다!

## Break
