# 기존 컨텐츠를 4C 형식으로 변환하기

> 이미 가지고 있는 교육 자료를 4C Markdown 형식으로 변환하는 프롬프트

---

## 🎯 이럴 때 사용하세요

- 기존 PPT 자료를 4C 형식으로 재구성하고 싶을 때
- 강의 노트나 문서를 구조화된 교육 자료로 만들 때
- 교육 컨텐츠를 4C 교수법으로 개선하고 싶을 때

---

## 📋 복사해서 사용할 프롬프트

### Gemini/ChatGPT/Claude에 붙여넣을 내용

```
당신은 교육 컨텐츠 전문가입니다. 제가 제공하는 기존 교육 자료를 4C 교수법(Connect-Concept-Concrete Practice-Conclusion) 구조로 재구성해주세요.

⚠️ 매우 중요: 아래 Markdown 형식을 정확히 지켜주세요!

🚨 CRITICAL: 각 필드(time, title, main, sub)는 **반드시 별도의 줄**에 작성하세요!

❌ 잘못된 예:
time: 3분 title: 제목 main: 내용 sub: 내용

✅ 올바른 예:
time: 3분
title: 제목
main: 내용
sub: 내용

---

## 변환 시 고려사항

1. **Connect (연결)**: 기존 내용 중 도입부나 예시를 활용해 학습자와 연결
2. **Concept (개념)**: 핵심 개념을 명확하고 간결하게 정리
3. **Concrete Practice (구체화)**: 실습이나 예제 부분을 구체적 단계로 구성
4. **Conclusion (정리)**: 핵심 내용 요약 및 다음 내용 예고

## 출력 형식

# 모듈 1: [제목]

## Module Start

[20자 이내의 짧은 문장]
예: "4C 교수법의 기초를 배웁니다"

## Connect
time: [소요 시간 (예: 3분)]
title: [제목]
main: [질문이나 주요 메시지]
sub:
- [구체적 예시 1]
- [구체적 예시 2]

## Concept
time: [소요 시간 (예: 5분)]
title: [제목]
main: [핵심 개념]
sub:
- [포인트 1]
- [포인트 2]
- [포인트 3]

## Concrete Practice
time: [소요 시간 (예: 10분)]
title: [제목]
main: [실습 설명]
sub:
- [단계 1]
- [단계 2]
- [단계 3]

⚠️ 중요: Concrete Practice도 sub:를 사용하세요! activity:를 사용하지 마세요!

## Conclusion
time: [소요 시간 (예: 2분)]
title: [제목]
main: [요약]
sub:
- [핵심 정리]
- [다음 학습 예고]

## Break
time: [소요 시간 (예: 15분)]
sub: [참여자들의 기운을 북돋을 15자 이내의 메시지 (예: "짧은 쉬는 시간이지만 푹 쉬세요")]

------

🚨 다시 한번 강조:
1. 필드명(time:, title:, main:, sub:)을 절대 바꾸지 마세요!
2. 각 필드는 반드시 별도의 줄에 작성하세요!
3. 한 줄에 여러 필드를 합치지 마세요!
4. Module Start는 20자 이내로 짧게 작성하세요!
5. 학습자가 하는 활동은 activity: 에 쓰세요. Concrete Practice는 activity: 필수, Connect/Concept/Conclusion도 가능하면 넣으세요!
6. Concept 한 슬라이드는 10분 이하. 넘으면 나누고 사이에 ## Review (time, title, activity) 를 넣으세요!
7. 모듈 제목 아래에 outcome: [관찰 가능한 동사 + 개념] 을 쓰세요. "이해한다/안다/배운다" 금지!
8. Conclusion은 학습자가 요약하는 활동으로. 강사가 "오늘 배운 것"을 정리하지 마세요!

---

## 제공할 기존 컨텐츠

[여기에 기존 PPT 슬라이드 내용, 강의 노트, 문서 내용 등을 붙여넣으세요]

---

## 추가 요구사항

- 총 시간: [원하는 총 교육 시간, 예: 60분]
- 모듈 개수: [원하는 모듈 수, 예: 3개]
- 대상 학습자: [예: 프로그래밍 초보자, 중급 관리자 등]
- 특별히 강조할 내용: [있다면 적어주세요]

---

변환을 시작해주세요!
```

---

## 💡 사용 방법

### 1단계: 기존 컨텐츠 준비

**예시 - 기존 PPT 내용:**
```
Python 기초 교육

슬라이드 1: Python이란?
- 1991년 귀도 반 로섬이 개발
- 배우기 쉬운 프로그래밍 언어
- 다양한 분야에서 활용

슬라이드 2: 변수
변수는 값을 저장하는 공간
예: x = 10, name = "홍길동"

슬라이드 3: 실습
1. 변수 선언하기
2. 값 출력하기
```

### 2단계: 프롬프트 복사 & 수정

1. 위의 전체 프롬프트 복사
2. "제공할 기존 컨텐츠" 섹션에 내용 붙여넣기
3. 추가 요구사항 작성 (총 시간, 모듈 수 등)

### 3단계: AI에 제출

- Gemini, ChatGPT, 또는 Claude Web에 붙여넣기
- 전송!

### 4단계: 결과 저장

```
Win + R → notepad → Enter
```

AI 응답 복사 → 메모장에 붙여넣기 → `과정명.md`로 저장 (UTF-8)

### 5단계: PPT 생성

```bash
python .claude/skills/4c-edu-ppt/scripts/generate_with_master_layout.py \
  --md "courses/과정명.md" \
  --template "your_template.pptx" \
  --output "courses/과정명_최종.pptx"
```

---

## 🔍 변환 예시

### 입력 (기존 컨텐츠)

```
API 기초 교육

1. API란?
   - Application Programming Interface
   - 프로그램 간 통신 규칙

2. REST API
   - GET, POST, PUT, DELETE
   - JSON 형식 사용

3. 실습: 날씨 API 호출하기
```

### 출력 (4C 형식)

```markdown
# 모듈 1: API의 이해와 활용

## Module Start

API로 프로그램을 연결합니다

## Connect
time: 5분
title: 프로그램은 어떻게 소통할까요?
main: 카카오톡으로 친구에게 메시지를 보내면, 어떻게 친구 폰까지 전달될까요?
sub:
- 앱과 서버가 서로 대화하는 방법
- 레스토랑의 메뉴판처럼 명확한 규칙이 필요

## Concept
time: 10분
title: API란 무엇인가
main: API는 프로그램 간 소통을 위한 약속된 규칙입니다
sub:
- Application Programming Interface의 약자
- REST API는 웹에서 가장 많이 사용
- GET(조회), POST(생성), PUT(수정), DELETE(삭제)

## Concrete Practice
time: 20분
title: 날씨 API 호출 실습
main: 실제 날씨 API를 호출하여 데이터를 받아봅시다
sub:
- API 키 발급받기
- GET 요청으로 현재 날씨 조회
- JSON 응답 데이터 해석하기

## Conclusion
time: 5분
title: API 마스터의 첫걸음
main: API의 개념과 REST API의 기본 동작을 이해했습니다
sub:
- API는 프로그램 간 소통 규칙
- REST API로 데이터 조회/생성/수정/삭제
- 다음: 실무 API 프로젝트 만들기

## Break
time: 10분
sub: 잠깐 쉬면서 실습 내용을 복습하세요
```

---

## 🔧 문제 해결

### ❌ AI가 형식을 안 지킴

**해결:**
```
위 내용을 다시 작성해줘.
이번에는 반드시 이 형식을 지켜:

## Connect
time: 3분
title: [제목]
main: [내용]
sub:
- [내용]

정확히 이 필드명(time:, title:, main:, sub:)을 사용해야 해!
각 필드는 별도의 줄에 작성해!
```

### ❌ 모듈이 너무 많거나 적음

**해결:**
```
이 내용을 정확히 3개 모듈로 나눠주세요.
각 모듈은 Connect-Concept-Concrete Practice-Conclusion 순서로 구성해주세요.
```

### ❌ 시간 배분이 이상함

**해결:**
```
각 모듈의 총 시간을 40분으로 맞춰주세요.
Connect: 5분, Concept: 10분, Concrete Practice: 20분, Conclusion: 5분
```

---

## 📊 AI 플랫폼별 특성

### Gemini (무료)
```
장점:
✅ 완전 무료
✅ 한국어 우수
✅ 빠른 변환

단점:
❌ 형식을 가끔 안 지킴
❌ 재요청 필요할 수 있음

→ 빠른 초안 만들기 좋음
```

### ChatGPT (GPT-4 권장)
```
장점:
✅ 형식 준수 우수
✅ 일관성 높음
✅ 컨텍스트 이해 좋음

단점:
❌ GPT-4는 유료
❌ 무료(3.5)는 품질 부족

→ 정확한 변환 필요할 때
```

### Claude (Pro 권장)
```
장점:
✅ 형식 준수 최고
✅ 긴 문서 처리 우수
✅ 세밀한 구조화

단점:
❌ Pro 필요 ($20/월)
❌ 무료는 제한적

→ 복잡한 컨텐츠 변환 시
```

---

## ✅ 체크리스트

### 프롬프트 준비
- [ ] 기존 컨텐츠 복사
- [ ] 프롬프트 붙여넣기
- [ ] "제공할 기존 컨텐츠" 섹션에 내용 입력
- [ ] 총 시간, 모듈 수 등 요구사항 작성

### 변환 실행
- [ ] AI 플랫폼 접속
- [ ] 프롬프트 전송
- [ ] 결과 확인 (형식 준수 여부)
- [ ] 필요시 수정 요청

### 결과 저장
- [ ] `# 모듈 1:` 부터 전체 복사
- [ ] 메모장 열기
- [ ] 붙여넣기
- [ ] `.md` 확장자로 저장
- [ ] UTF-8 인코딩 확인

### PPT 생성
- [ ] 명령 프롬프트 열기
- [ ] 프로젝트 폴더 이동
- [ ] 생성 명령 실행
- [ ] 결과 확인

---

## 💡 Pro Tips

### Tip 1: 단계적 변환

```
❌ 나쁜 방법: "전체 과정 한번에 변환"
→ 품질 떨어짐, 구조 혼란

✅ 좋은 방법: "모듈 1만 먼저 변환"
→ 검토 후 다음 모듈 진행
→ 일관성 유지
```

### Tip 2: 명확한 지시

```
"이 내용을 60분 교육 과정으로 만들어주세요"

보다는:

"이 내용을 3개 모듈로 나눠주세요.
각 모듈은 20분입니다.
Connect 5분, Concept 5분, Practice 8분, Conclusion 2분"
```

### Tip 3: 예시 제공

```
"이런 스타일로 변환해주세요:"

## Connect
time: 5분
title: 코드는 어떻게 실행될까요?
main: 우리가 작성한 코드는 컴퓨터가 어떻게 이해할까요?
sub:
- 컴파일러와 인터프리터의 역할
- Python은 인터프리터 언어입니다
```

---

## 🎯 다음 단계

변환이 완료되면:

1. **검토**: 생성된 md 파일 내용 확인
2. **수정**: 필요시 직접 편집
3. **검증**:
   ```bash
   python .claude/skills/4c-edu-ppt/scripts/validate_md.py courses/파일명.md
   ```
4. **PPT 생성**:

   **포함된 기본 템플릿 사용 (권장):**
   ```bash
   python .claude/skills/4c-edu-ppt/scripts/generate_with_master_layout.py \
     --md "courses/파일명.md" \
     --template ".claude/skills/4c-edu-ppt/pptx-templates/default_4c_template.pptx" \
     --output "courses/output.pptx"
   ```

   **자신의 템플릿 사용:**
   ```bash
   python .claude/skills/4c-edu-ppt/scripts/generate_with_master_layout.py \
     --md "courses/파일명.md" \
     --template "your_template.pptx" \
     --output "output.pptx"
   ```

---

**관련 문서:**
- [새 컨텐츠 생성하기](AI_CONTENT_PROMPT.md)
- [Gemini/ChatGPT 빠른 가이드](GEMINI_CHATGPT_QUICK.md)
- [Claude Web 가이드](CLAUDE_WEB_GUIDE.md)
