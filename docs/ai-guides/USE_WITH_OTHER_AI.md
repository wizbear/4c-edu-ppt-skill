# 다른 AI 플랫폼에서 사용하기

> Gemini, ChatGPT, Claude Web 등에서 이 시스템을 사용하는 방법

---

## 🎯 핵심 이해

### ✅ 사용 가능한 것
- ✅ **AI 콘텐츠 생성** - Gemini, ChatGPT, Claude Web 모두 가능
- ✅ **구조 템플릿** - 모든 AI에서 동일하게 사용
- ✅ **프롬프트** - 모든 AI에 적용 가능
- ✅ **워크플로우** - AI 플랫폼 무관

### ❌ Claude Code 전용인 것
- ❌ **Skill 자동 실행** - Claude Code CLI에서만
- ❌ **파일 자동 읽기/쓰기** - Claude Code CLI에서만

### ⚙️ 로컬 실행 (AI 무관)
- ⚙️ **Python 스크립트** - AI와 상관없이 로컬에서 실행
- ⚙️ **PPT 생성** - 명령줄에서 직접 실행

---

## 🚀 사용 방법 비교

### Claude Code에서 (현재)
```
사용자: "Python 기초 과정 콘텐츠 만들어줘"
  ↓
Claude Code: 파일 읽기/쓰기, AI 생성, 스크립트 실행 자동 처리
  ↓
결과: PPT 파일 자동 생성
```

### Gemini/ChatGPT에서 (수동)
```
사용자: [프롬프트 붙여넣기]
  ↓
AI: Markdown 콘텐츠 생성
  ↓
사용자: 복사 → 파일 저장 → 스크립트 수동 실행
  ↓
결과: PPT 파일 생성
```

**차이점**: 파일 저장과 스크립트 실행을 **사용자가 직접** 해야 함

---

## 📋 Step-by-Step: Gemini/ChatGPT 사용법

### 준비물
- ✅ Google Gemini 또는 ChatGPT 계정
- ✅ 텍스트 에디터 (VS Code, 메모장)
- ✅ Python 환경 (이미 설치됨)

---

### Step 1: AI 프롬프트 준비

#### 1-1. 프롬프트 파일 열기

**Windows:**
```bash
notepad "C:\Users\wizbear\OneDrive\02_프로젝트\25-12-04 AX 컨설턴트 양성과정 개발\.claude\skills\4c-edu-ppt\AI_CONTENT_PROMPT.md"
```

**또는 VS Code:**
```bash
code "C:\Users\wizbear\OneDrive\02_프로젝트\25-12-04 AX 컨설턴트 양성과정 개발\.claude\skills\4c-edu-ppt\AI_CONTENT_PROMPT.md"
```

#### 1-2. 기본 프롬프트 복사

파일에서 **"기본 프롬프트"** 섹션 전체를 복사:

```markdown
당신은 교육 콘텐츠 전문가입니다. 아래 4C 교수법 구조에 맞춰 교육 자료를 작성해주세요.

## 주제
[여기에 교육 주제를 입력하세요]

## 4C 구조 설명
- **Connect (연결)**: 학습자의 경험, 관심사와 주제를 연결
- **Concept (개념)**: 핵심 개념을 명확하고 간결하게 설명
- **Concrete Practice (구체화)**: 실습, 예제, 활동을 통한 적용
- **Conclusion (정리)**: 요약 및 다음 학습 예고

## 출력 형식
다음 Markdown 형식으로 작성해주세요:

# 모듈 1: [모듈 제목]

## Module Start
[모듈 시작 인사 또는 개요]

## Connect
time: [소요 시간 (예: 3분)]
title: [슬라이드 제목]
main: [주요 메시지 - 질문이나 학습자와 연결되는 내용]
sub: [부가 설명 - 구체적 예시나 일상 사례]

## Concept
time: [소요 시간 (예: 5분)]
title: [슬라이드 제목]
main: [핵심 개념 설명]
sub: [개념의 세부 내용, 불릿 포인트로]

## Concrete Practice
time: [소요 시간 (예: 10분)]
title: [슬라이드 제목]
main: [실습 설명]
activity: |
  실습 단계:
  1. [첫 번째 단계]
  2. [두 번째 단계]
  3. [세 번째 단계]

## Conclusion
time: [소요 시간 (예: 2분)]
title: [슬라이드 제목]
main: [요약 내용]
sub: [다음 학습 내용 예고]

## Break

---

## 작성 가이드
1. **Connect**: 질문으로 시작하여 호기심 유발
2. **Concept**: 전문 용어는 쉽게 풀어서 설명
3. **Concrete Practice**: 구체적이고 실행 가능한 활동
4. **Conclusion**: 핵심 내용 3-5개 요약

총 [원하는 모듈 수]개 모듈을 작성해주세요.
```

---

### Step 2: AI 플랫폼에서 실행

#### 2-1. Gemini 사용하기

**A. Gemini 접속**
```
https://gemini.google.com
```

**B. 프롬프트 붙여넣기 및 수정**
```
당신은 교육 콘텐츠 전문가입니다. 아래 4C 교수법 구조에 맞춰 교육 자료를 작성해주세요.

## 주제
Python 기초 - 변수와 함수

## 4C 구조 설명
[위 프롬프트 내용]

...

총 3개 모듈을 작성해주세요.
```

**C. 전송 및 대기**

**D. 결과 확인**
- Markdown 형식이 맞는지 확인
- 필드명 정확한지 확인 (`time:`, `title:`, `main:`, `sub:`)

---

#### 2-2. ChatGPT 사용하기

**A. ChatGPT 접속**
```
https://chat.openai.com
```

**B. 같은 방식으로 프롬프트 붙여넣기**

**권장: GPT-4 이상 사용**
- GPT-3.5: 형식을 잘 안 지킬 수 있음
- GPT-4: 형식 준수 우수

**C. 형식 강조 추가 (필요시)**
```
⚠️ 매우 중요: 반드시 위 Markdown 형식을 정확히 지켜주세요.
특히 다음 필드명을 그대로 사용:
- time: (시간 뒤에 "분" 붙이기)
- title:
- main:
- sub: 또는 activity:

절대 필드명을 바꾸거나 생략하지 마세요!
```

---

#### 2-3. Claude Web 사용하기

**A. Claude 접속**
```
https://claude.ai
```

**B. 프롬프트 붙여넣기**

**장점**: 형식 준수가 가장 우수

**C. 대화 컨텍스트 유지**
```
[첫 메시지]
나는 "Python 기초" 과정을 만들 거야.
대상: 초보자
목표: 변수와 함수 이해

[두 번째 메시지]
위 프롬프트에 맞춰 모듈 1을 작성해줘.

[세 번째 메시지]
좋아, 같은 톤으로 모듈 2도 작성해줘.
```

---

### Step 3: 결과 저장

#### 3-1. AI 응답 복사

**A. Markdown 부분만 선택 복사**

ChatGPT/Gemini 응답:
```
네, 작성했습니다!

# 모듈 1: 변수란 무엇인가

## Module Start
...
```

→ `# 모듈 1:` 부터 끝까지 복사

**B. 코드 블록 제거**

만약 AI가 코드 블록으로 감쌌다면:
````markdown
```markdown
# 모듈 1: ...
```
````

→ 코드 블록 표시(```)는 제거하고 내용만 복사

---

#### 3-2. 파일로 저장

**A. 메모장 또는 VS Code 열기**
```bash
notepad
# 또는
code
```

**B. 붙여넣기**

**C. 다른 이름으로 저장**
```
파일명: Python기초과정_2026-01-06_v1.0.md
위치: C:\Users\wizbear\OneDrive\02_프로젝트\25-12-04 AX 컨설턴트 양성과정 개발\courses\Python기초과정\
형식: 모든 파일 (*.*)
인코딩: UTF-8
```

**⚠️ 중요:**
- 확장자 반드시 `.md`
- 인코딩 UTF-8 (한글 깨짐 방지)

---

### Step 4: 검토 및 수정

#### 4-1. 형식 확인

**체크리스트 열기:**
```bash
code "C:\Users\wizbear\OneDrive\02_프로젝트\25-12-04 AX 컨설턴트 양성과정 개발\.claude\skills\4c-edu-ppt\templates\review_checklist.md"
```

**파일 열어서 대조:**
```bash
code "Python기초과정_2026-01-06_v1.0.md"
```

**확인 사항:**
- [ ] `# 모듈 1:` 형식?
- [ ] `## Module Start` 있음?
- [ ] `time:`, `title:`, `main:`, `sub:` 필드 정확?

---

#### 4-2. 내용 검토 및 수정

**문제 발견 시:**

**Option 1: AI에게 다시 요청**
```
위 내용에서 다음을 수정해줘:
1. 모듈 1 Concept의 sub를 3개로 줄여줘
2. 모듈 2 Practice를 더 쉽게
```

→ 수정된 부분만 복사 → 파일에 교체

**Option 2: 직접 수정**
- VS Code나 메모장에서 직접 편집
- 저장

---

### Step 5: PPT 생성 (로컬 스크립트)

**⚠️ 중요: 이 단계는 AI 플랫폼과 무관하게 로컬에서 실행합니다**

#### 5-1. 명령 프롬프트 열기

**Windows:**
```
Win + R → cmd → Enter
```

#### 5-2. 프로젝트 폴더로 이동

```bash
cd "C:\Users\wizbear\OneDrive\02_프로젝트\25-12-04 AX 컨설턴트 양성과정 개발"
```

#### 5-3. PPT 생성 명령 실행

```bash
python .claude/skills/4c-edu-ppt/scripts/generate_with_master_layout.py --md "courses/Python기초과정/Python기초과정_2026-01-06_v1.0.md" --template "26-01-06_my_template.pptx" --output "courses/Python기초과정/Python기초과정_최종.pptx"
```

#### 5-4. 결과 확인

```
[SUCCESS] PowerPoint file created: ...
   Total 12 slides generated.
```

**✅ 완료!**

---

## 📊 플랫폼별 비교

| 기능 | Claude Code | Gemini | ChatGPT | Claude Web |
|------|-------------|--------|---------|------------|
| **콘텐츠 생성** | ✅ 자동 | ✅ 수동 | ✅ 수동 | ✅ 수동 |
| **파일 저장** | ✅ 자동 | ❌ 수동 | ❌ 수동 | ❌ 수동 |
| **PPT 생성** | ✅ 자동 | ⚙️ 로컬 | ⚙️ 로컬 | ⚙️ 로컬 |
| **형식 준수** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **속도** | 빠름 | 중간 | 중간 | 중간 |
| **편의성** | 최고 | 중간 | 중간 | 중간 |

---

## 💡 각 플랫폼별 팁

### Gemini 사용 팁

**장점:**
- 무료 버전도 괜찮음
- 한국어 이해 우수
- 긴 텍스트 생성 가능

**단점:**
- 형식을 가끔 안 지킴
- 재생성 필요할 수 있음

**권장 사용법:**
```
1. 전체를 한번에 요청하지 말고
2. 모듈별로 나눠서 요청
3. 형식 강조를 여러 번
```

---

### ChatGPT 사용 팁

**장점:**
- 형식 준수 우수 (GPT-4)
- 일관성 좋음
- 수정 요청 잘 따름

**단점:**
- 무료 버전(GPT-3.5)은 부족
- GPT-4 필요 (유료)

**권장 사용법:**
```
1. GPT-4 사용 (Plus 구독 필요)
2. Custom Instructions 설정:
   "항상 Markdown 형식을 정확히 지켜주세요"
3. 한번에 요청 가능
```

**Custom Instructions 설정:**
```
Settings → Personalization → Custom Instructions

What would you like ChatGPT to know about you?
→ "I create educational content using 4C framework"

How would you like ChatGPT to respond?
→ "Always follow Markdown format exactly as specified.
    Never change field names like 'time:', 'title:', 'main:', 'sub:'"
```

---

### Claude Web 사용 팁

**장점:**
- 형식 준수 최고
- 긴 대화 컨텍스트
- 수정 능력 우수

**단점:**
- 무료 버전 제한적
- Pro 필요 (유료)

**권장 사용법:**
```
1. Projects 기능 사용
2. 프롬프트를 Project Knowledge에 추가
3. 대화 컨텍스트 유지하며 순차 생성
```

**Projects 설정:**
```
1. New Project 생성: "4C 교육 콘텐츠"
2. Add Knowledge → AI_CONTENT_PROMPT.md 업로드
3. 매번 프롬프트 입력 불필요
```

---

## 🔄 워크플로우 정리

### Claude Code 워크플로우 (자동화)
```
1. Claude Code에 요청
   ↓
2. 자동 파일 생성
   ↓
3. 자동 PPT 생성
   ↓
완료 (10분)
```

### Gemini/ChatGPT 워크플로우 (수동)
```
1. AI 플랫폼에서 프롬프트 입력
   ↓
2. 응답 복사
   ↓
3. 파일로 수동 저장 (.md)
   ↓
4. 검토 및 수정
   ↓
5. 명령줄에서 스크립트 실행
   ↓
6. PPT 생성
   ↓
완료 (30-60분)
```

**추가 시간**: 파일 저장 및 수동 작업으로 약 20-50분 더 소요

---

## 📝 빠른 실행 템플릿

### Gemini/ChatGPT에 붙여넣을 최종 프롬프트

```markdown
당신은 교육 콘텐츠 전문가입니다. 4C 교수법으로 교육 자료를 작성해주세요.

## 주제
[여기에 주제 입력]

## 대상 및 목표
- 대상: [학습자]
- 목표: [학습 목표]
- 총 시간: [분]

⚠️ 매우 중요: 아래 Markdown 형식을 정확히 지켜주세요!

## 출력 형식

# 모듈 1: [제목]

## Module Start
[모듈 소개]

## Connect
time: 3분
title: [제목]
main: [질문이나 주요 메시지]
sub: [구체적 예시]

## Concept
time: 5분
title: [제목]
main: [핵심 개념]
sub: |
  - [포인트 1]
  - [포인트 2]
  - [포인트 3]

## Concrete Practice
time: 10분
title: [제목]
main: [실습 설명]
activity: |
  실습:
  1. [단계 1]
  2. [단계 2]
  3. [단계 3]

## Conclusion
time: 2분
title: [제목]
main: [요약]
sub: [다음 학습]

## Break

---

총 [숫자]개 모듈을 작성해주세요.

필드명(time:, title:, main:, sub:, activity:)을 절대 바꾸지 마세요!
```

---

## ✅ 체크리스트: Gemini/ChatGPT 사용

### 콘텐츠 생성 단계
- [ ] AI 플랫폼 접속
- [ ] 프롬프트 붙여넣기 및 주제 입력
- [ ] AI 응답 확인
- [ ] 형식 맞는지 검증

### 파일 저장 단계
- [ ] Markdown 내용만 복사
- [ ] 메모장/VS Code에 붙여넣기
- [ ] `.md` 확장자로 저장
- [ ] UTF-8 인코딩 확인

### 검토 단계
- [ ] review_checklist.md 참고
- [ ] 형식 검증
- [ ] 내용 검토
- [ ] 필요시 수정

### PPT 생성 단계
- [ ] 명령 프롬프트 열기
- [ ] 프로젝트 폴더로 이동
- [ ] Python 스크립트 실행
- [ ] 결과 확인

---

## 🎯 결론

### 어느 것을 사용해야 할까?

**Claude Code (권장)**
- 자동화된 워크플로우
- 빠른 속도
- 파일 관리 자동

**Gemini (무료 옵션)**
- 비용 부담 없음
- 한국어 우수
- 약간의 수동 작업 필요

**ChatGPT (품질 우선)**
- GPT-4로 최고 품질
- 형식 준수 우수
- 유료 구독 필요

**Claude Web (균형)**
- 형식 준수 최고
- 긴 컨텍스트
- 유료 구독 필요

### 추천 조합

**무료로 시작:**
```
Gemini (콘텐츠 생성) + 로컬 스크립트 (PPT 생성)
```

**품질 중시:**
```
ChatGPT GPT-4 (콘텐츠 생성) + 로컬 스크립트 (PPT 생성)
```

**최고 효율:**
```
Claude Code (전체 자동화)
```

---

모든 플랫폼에서 **핵심 시스템(4C 구조 + Python 스크립트)**은 동일하게 작동합니다!
