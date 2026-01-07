# Gemini/ChatGPT 빠른 사용 가이드

> 복사 → 붙여넣기 → 저장 → 실행

---

## 🚀 3분 요약

### 1️⃣ AI에게 요청 (5분)
```
Gemini 또는 ChatGPT 접속
↓
아래 프롬프트 복사/붙여넣기
↓
주제 입력 후 전송
```

### 2️⃣ 결과 저장 (2분)
```
AI 응답 복사
↓
메모장에 붙여넣기
↓
파일명.md로 저장 (UTF-8)
```

### 3️⃣ PPT 생성 (1분)
```bash
python 스크립트 실행
↓
PPT 파일 생성 완료!
```

---

## 📋 복사해서 사용할 프롬프트

### Gemini/ChatGPT에 붙여넣을 내용

```
당신은 교육 콘텐츠 전문가입니다. 4C 교수법으로 교육 자료를 작성해주세요.

## 주제
Python 기초 - 변수와 함수

## 대상 및 목표
- 대상: 프로그래밍 초보자
- 목표: 변수와 함수의 기본 개념 이해 및 실습
- 총 시간: 60분

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

# 모듈 1: [제목]

## Module Start

⚠️ 중요: Module Start는 20자 이내의 짧은 문장으로 작성하세요!
예: "변수와 함수의 기초를 배웁니다"

## Connect
time: 3분
title: [제목]
main: [질문이나 주요 메시지]
sub:
- [구체적 예시 1]
- [구체적 예시 2]

## Concept
time: 5분
title: [제목]
main: [핵심 개념]
sub:
- [포인트 1]
- [포인트 2]
- [포인트 3]

## Concrete Practice
time: 10분
title: [제목]
main: [실습 설명]
sub:
- [단계 1]
- [단계 2]
- [단계 3]

⚠️ 중요: Concrete Practice도 sub:를 사용하세요! activity:를 사용하지 마세요!

## Conclusion
time: 2분
title: [제목]
main: [요약]
sub:
- [핵심 정리]
- [다음 학습 예고]

## Break
time: [소요 시간 (예: 15분)]
sub: [참여자들의 기운을 북돋을 15자 이내의 메시지 (예: "짧은 쉬는 시간이지만 푹 쉬세요")]

---

총 3개 모듈을 위 형식으로 작성해주세요.

🚨 다시 한번 강조:
1. 필드명(time:, title:, main:, sub:)을 절대 바꾸지 마세요!
2. 각 필드는 반드시 별도의 줄에 작성하세요!
3. 한 줄에 여러 필드를 합치지 마세요!
4. Module Start는 20자 이내로 짧게 작성하세요!
5. Concrete Practice에서도 sub:를 사용하세요! (activity: 금지)
```

**사용법:**
1. 위 텍스트 전체 복사
2. Gemini 또는 ChatGPT에 붙여넣기
3. "주제" 부분만 원하는 주제로 변경
4. 전송!

---

## 💾 파일 저장 방법

### Windows 메모장 사용

**1. 메모장 열기**
```
Win + R → notepad → Enter
```

**2. AI 응답 복사**
- `# 모듈 1:` 부터 끝까지 전체 선택
- Ctrl+C 복사

**3. 메모장에 붙여넣기**
- Ctrl+V

**4. 저장**
```
파일 → 다른 이름으로 저장
파일명: Python기초과정_2026-01-06.md
파일 형식: 모든 파일 (*.*)
인코딩: UTF-8
위치: C:\Users\wizbear\OneDrive\02_프로젝트\25-12-04 AX 컨설턴트 양성과정 개발\courses\
```

**⚠️ 중요:**
- 확장자 `.md` 필수!
- 인코딩 UTF-8 선택!

---

## ⚙️ PPT 생성 명령어

### 명령 프롬프트 열기
```
Win + R → cmd → Enter
```

### 프로젝트 폴더로 이동
```bash
cd "C:\Users\wizbear\OneDrive\02_프로젝트\25-12-04 AX 컨설턴트 양성과정 개발"
```

### PPT 생성 실행

**포함된 기본 템플릿 사용 (권장):**
```bash
python .claude/skills/4c-edu-ppt/scripts/generate_with_master_layout.py --md "courses/Python기초과정_2026-01-06.md" --template ".claude/skills/4c-edu-ppt/pptx-templates/default_4c_template.pptx" --output "courses/Python기초과정_최종.pptx"
```

**자신의 템플릿 사용:**
```bash
python .claude/skills/4c-edu-ppt/scripts/generate_with_master_layout.py --md "courses/Python기초과정_2026-01-06.md" --template "your_template.pptx" --output "courses/Python기초과정_최종.pptx"
```

**성공 메시지:**
```
[SUCCESS] PowerPoint file created: ...
   Total 12 slides generated.
```

**✅ 완료!** → PPT 파일 열어서 확인

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
sub: [내용]

정확히 이 필드명(time:, title:, main:, sub:)을 사용해야 해!
```

### ❌ 파일 저장이 안 됨

**체크:**
- [ ] 확장자 `.md` 붙였나?
- [ ] 파일명에 특수문자 없나?
- [ ] 폴더 경로가 맞나?

### ❌ PPT 생성 오류

**체크:**
```bash
# 1. 파일이 있나?
dir "courses\Python기초과정_2026-01-06.md"

# 2. 템플릿이 있나?
dir "26-01-06_my_template.pptx"

# 3. Python 작동하나?
python --version
```

---

## 📊 플랫폼 선택 가이드

### Gemini (무료)
```
장점:
✅ 완전 무료
✅ 한국어 우수
✅ 빠른 응답

단점:
❌ 형식을 가끔 안 지킴
❌ 재시도 필요할 수 있음

→ 비용 걱정 없이 시작하기 좋음
```

### ChatGPT (유료 권장)
```
장점:
✅ 형식 준수 우수 (GPT-4)
✅ 일관성 높음
✅ 수정 요청 잘 따름

단점:
❌ GPT-4는 유료 (Plus $20/월)
❌ 무료(3.5)는 품질 부족

→ 품질 중시하면 GPT-4 사용
```

### Claude Web (유료 권장)
```
장점:
✅ 형식 준수 최고
✅ 긴 대화 가능
✅ 세밀한 수정

단점:
❌ Pro 필요 ($20/월)
❌ 무료는 제한적

→ 복잡한 과정 만들 때 좋음
```

---

## ✅ 체크리스트

### AI 사용
- [ ] Gemini/ChatGPT 접속
- [ ] 프롬프트 붙여넣기
- [ ] 주제 변경
- [ ] 전송
- [ ] 응답 확인

### 파일 저장
- [ ] `# 모듈 1:` 부터 전체 복사
- [ ] 메모장 열기
- [ ] 붙여넣기
- [ ] `.md` 확장자로 저장
- [ ] UTF-8 인코딩 확인

### PPT 생성
- [ ] cmd 열기
- [ ] 프로젝트 폴더 이동
- [ ] 명령어 복사/붙여넣기
- [ ] 실행
- [ ] 결과 확인

---

## 🎯 시간 비교

| 방식 | 소요 시간 | 난이도 |
|------|----------|--------|
| Claude Code | 10분 | ⭐ 쉬움 |
| Gemini/ChatGPT | 30-60분 | ⭐⭐ 보통 |

**차이**: 파일 저장과 스크립트 실행을 직접 해야 함

---

## 💡 Pro Tips

### Tip 1: 모듈별로 나눠서 요청
```
❌ 나쁜 방법: "모듈 5개 한번에"
→ 품질 떨어짐, 형식 안 지킴

✅ 좋은 방법: "모듈 1만 먼저"
→ 품질 좋음, 검토 후 다음 모듈
```

### Tip 2: 형식 강조는 여러 번
```
프롬프트 맨 위에:
⚠️ 형식을 정확히 지켜주세요

중간에:
위 형식을 그대로 사용하세요

마지막에:
필드명을 절대 바꾸지 마세요!
```

### Tip 3: 예시 제공
```
"이런 스타일로:"

## Connect
time: 3분
title: 정보를 어떻게 기억하나요?
main: 중요한 전화번호를 어떻게 기억하시나요?
sub: 메모장이나 포스트잇을 사용하죠? 프로그래밍도 마찬가지입니다.

"이렇게 작성해줘"
```

---

**시작하세요!**

1. Gemini 또는 ChatGPT 접속
2. 위 프롬프트 복사/붙여넣기
3. 주제만 변경
4. 전송!
