# 4C 교육 구조 기반 PPT 제작 Skill

이 Skill은 4C 교육 구조(Connect - Concept - Concrete Practice - Conclusion)를 기반으로 체계적인 교육용 PowerPoint 프레젠테이션을 자동 생성합니다.

## 🚀 빠른 링크

| 사용자 | 제작자 |
|--------|--------|
| 📥 **[설치 가이드](INSTALLATION.md)** | 📦 **[배포 가이드](DISTRIBUTION.md)** |
| 처음부터 끝까지 설치 방법 | 다른 사람에게 공유하는 방법 |

## 빠른 시작

**처음 사용하시나요?** 👉 [설치 가이드](INSTALLATION.md) 먼저 읽기

**Claude Code 사용법** 👉 [빠른 시작 가이드](docs/getting-started/QUICK_START.md)

**다른 AI 도구 사용?** 👉 [Gemini/ChatGPT 가이드](docs/ai-guides/GEMINI_CHATGPT_QUICK.md)

**기존 자료 변환?** 👉 [컨텐츠 변환 가이드](docs/ai-guides/CONVERT_TO_4C_PROMPT.md)

## 필수 설치

```bash
pip install python-pptx
```

## 포함된 템플릿

스킬에는 바로 사용할 수 있는 기본 4C 템플릿이 포함되어 있습니다:

```
.claude/skills/4c-edu-ppt/pptx-templates/default_4c_template.pptx
```

이 템플릿은 다음 레이아웃을 포함합니다:
- Title_Page (제목 페이지)
- Module_Divider (모듈 구분)
- Connect, Concept, Concrete Practice, Conclusion (4C 단계)
- Break (휴식 시간)
- End (종료 페이지)

## 사용 방법

### 🌟 방법 1: Markdown 파일 사용 (권장!)

**전문적인 교육 콘텐츠 제작에 최적!**

Markdown 파일로 콘텐츠를 작성하면:
- ✅ 모듈 단위로 체계적 구성
- ✅ 각 4C 단계를 원하는 만큼 반복
- ✅ 이미지, 동영상, Break 슬라이드 자유롭게 추가
- ✅ Git으로 버전 관리 가능
- ✅ 팀원과 협업하기 쉬움

#### Markdown 파일 작성:

`my_course.md` 파일 생성:

```markdown
# 모듈 1: Python 기초

## Module Start
Python 프로그래밍의 세계에 오신 것을 환영합니다!

## Connect
time: 5분
title: 프로그래밍과의 첫 만남
main: 여러분은 컴퓨터에게 명령을 내려본 적이 있나요?
sub: 게임, 앱, 웹사이트 모두 프로그래밍으로 만들어집니다.

## Connect
time: 3분
title: Python은 어디에?
main: YouTube, Instagram 모두 Python으로!
sub: 데이터 분석, AI, 웹 개발 등에 활용

## Concept
time: 10분
title: 변수란?
main: 변수는 데이터를 저장하는 이름표입니다
sub: |
  예시:
  name = "홍길동"
  age = 25

## Image
image: ./images/variable_example.png
caption: 변수의 개념 도해

## Concrete Practice
time: 15분
title: 변수 실습
main: 직접 변수를 만들어봅시다
activity: |
  실습 단계:
  1. 이름을 name 변수에 저장
  2. 나이를 age 변수에 저장
  3. print()로 출력하기

## Video
video: ./videos/coding_demo.mp4
description: 실제 코딩 시연
duration: 5분

## Conclusion
time: 5분
title: 정리
main: 변수의 개념을 배웠습니다!
sub: 다음 시간: 데이터 타입 배우기

## Break

---

# 모듈 2: 데이터 타입
...
```

#### PPT 생성:

**포함된 기본 템플릿 사용 (권장):**
```bash
python .claude/skills/4c-edu-ppt/scripts/generate_with_master_layout.py \
  --md my_course.md \
  --template .claude/skills/4c-edu-ppt/pptx-templates/default_4c_template.pptx \
  --output python_course.pptx
```

**자신만의 템플릿 사용:**
```bash
python .claude/skills/4c-edu-ppt/scripts/generate_with_master_layout.py \
  --md my_course.md \
  --template my_company_template.pptx \
  --output python_course.pptx
```

**예제 파일 참고**: `.claude/skills/4c-edu-ppt/examples/example_course.md`

### 방법 2: Claude Code에서 직접 요청

간단한 PPT가 필요할 때:

```
4C 구조로 "머신러닝 기초" 교육 PPT를 만들어주세요.

- Connect: AI가 일상생활에 어떻게 사용되는지 아시나요?
- Concept: 머신러닝은 데이터로부터 학습하는 알고리즘입니다.
- Practice: 간단한 분류 모델을 만들어봅시다.
- Conclusion: 머신러닝의 기본 개념과 응용을 배웠습니다.
```

### 방법 3: 기존 스크립트 사용

```bash
python .claude/skills/4c-edu-ppt/scripts/generate_4c_ppt.py \
  --title "Python 기초 - 변수와 데이터 타입" \
  --connect "여러분은 일상에서 정보를 어떻게 기억하나요? 이름표를 붙여 기억하시죠?
Python에서는 변수라는 이름표를 사용합니다." \
  --concept "변수는 데이터를 저장하는 이름표입니다.
- 숫자형 (int, float)
- 문자열 (str)
- 리스트 (list)
- 딕셔너리 (dict)" \
  --practice "실습 과제:
1. 자신의 이름을 name 변수에 저장하기
2. 나이를 age 변수에 저장하기
3. print()로 출력하기

예시:
name = '홍길동'
age = 25
print(f'제 이름은 {name}이고, {age}살입니다.')" \
  --conclusion "오늘 배운 내용:
- 변수는 데이터를 저장하는 이름표
- Python의 주요 데이터 타입
- 변수 선언과 출력 방법

다음 시간: 조건문과 반복문을 배워봅시다!" \
  --output python_basics.pptx
```

## 생성되는 슬라이드 구조

1. **제목 슬라이드**: 교육 주제
2. **Connect 슬라이드** (🔗): 학습자와의 연결
3. **Concept 슬라이드** (💡): 핵심 개념 설명
4. **Concrete Practice 슬라이드** (✏️): 실습 및 예제
5. **Conclusion 슬라이드** (🎯): 요약 및 정리
6. **감사 슬라이드**: 마무리 인사

## 커스텀 템플릿 사용하기

자신만의 PPTX 템플릿을 사용하여 회사나 학교의 브랜드 아이덴티티를 유지할 수 있습니다.

### 템플릿 준비

1. PowerPoint에서 원하는 디자인의 템플릿 파일(`.pptx`) 준비
2. 마스터 슬라이드 설정:
   - 레이아웃 0번: 제목 슬라이드 (Title Slide)
   - 레이아웃 1번: 제목과 내용 (Title and Content)

### 템플릿 적용 예시

```bash
python .claude/skills/4c-edu-ppt/scripts/generate_4c_ppt.py \
  --template "templates/company_template.pptx" \
  --title "데이터 분석 기초" \
  --connect "엑셀로 데이터를 정리하다 지친 경험이 있나요?" \
  --concept "Python pandas로 대용량 데이터를 쉽게 처리할 수 있습니다" \
  --practice "CSV 파일을 읽고 필터링해봅시다" \
  --conclusion "pandas의 기본 기능을 배웠습니다" \
  --output "data_analysis_course.pptx"
```

### 템플릿 사용 시 장점

- **브랜드 일관성**: 회사/학교 로고, 색상, 폰트 자동 적용
- **시간 절약**: 매번 디자인 설정할 필요 없음
- **전문성**: 통일된 디자인으로 전문적인 인상

### 템플릿 관리 팁

**포함된 기본 템플릿:**
```
.claude/skills/4c-edu-ppt/pptx-templates/default_4c_template.pptx
```
- 바로 사용 가능한 기본 4C 템플릿
- 모든 필수 레이아웃 포함

**자신만의 템플릿 추가:**
```
프로젝트/
├── .claude/skills/4c-edu-ppt/
│   └── pptx-templates/
│       └── default_4c_template.pptx  # 포함된 기본 템플릿
└── my-templates/                      # 자신의 템플릿 폴더
    ├── corporate_template.pptx        # 기업 교육용
    ├── academic_template.pptx         # 학술 발표용
    └── workshop_template.pptx         # 워크샵용
```

**템플릿 파일 위치 옵션:**
- 포함된 템플릿: `.claude/skills/4c-edu-ppt/pptx-templates/default_4c_template.pptx`
- 절대 경로: `C:\Users\username\templates\my_template.pptx`
- 상대 경로: `my-templates/corporate_template.pptx` (프로젝트 기준)
- 같은 폴더: `my_template.pptx`

### 주의사항

- 템플릿이 없거나 경로가 잘못된 경우 자동으로 기본 디자인으로 생성됩니다
- 레이아웃 번호가 다른 템플릿의 경우 슬라이드 모양이 예상과 다를 수 있습니다
- PowerPoint 2007 이상 형식(`.pptx`)만 지원됩니다

## 4C 구조 작성 가이드

### Connect (연결)
- 학습자의 사전 경험이나 관심사와 연결
- 질문으로 시작하여 호기심 유발
- 일상생활 예시 활용

**좋은 예시:**
- "SNS에서 친구 추천은 어떻게 이루어질까요?"
- "엑셀에서 데이터를 정리할 때 불편했던 경험이 있나요?"

### Concept (개념)
- 핵심 개념을 명확하고 간결하게 설명
- 전문 용어는 쉬운 말로 풀어서 설명
- 불릿 포인트로 정리

**좋은 예시:**
```
API란 무엇인가?
- Application Programming Interface의 약자
- 프로그램 간 소통을 위한 규칙
- 레스토랑의 메뉴판과 같은 역할
```

### Concrete Practice (구체화)
- 실제로 해볼 수 있는 활동 제시
- 단계별로 명확한 지침 제공
- 코드 예시나 실습 과제 포함

**좋은 예시:**
```
실습: 나만의 계산기 만들기
1. 두 숫자를 입력받기
2. 더하기 연산 수행
3. 결과 출력하기
```

### Conclusion (정리)
- 학습 내용 요약
- 학습 목표 달성 확인
- 다음 학습 내용 예고

**좋은 예시:**
```
오늘 배운 내용:
✓ 변수의 개념과 사용법
✓ 데이터 타입의 종류
✓ 실제 코드 작성 경험

다음 시간: 조건문으로 프로그램 제어하기
```

## 커스터마이징

생성된 PPT는 PowerPoint에서 자유롭게 편집할 수 있습니다:

- 색상 테마 변경
- 폰트 스타일 조정
- 이미지/도표 추가
- 애니메이션 효과 추가

## 문제 해결

### python-pptx 설치 오류
```bash
# 가상환경 사용 권장
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install python-pptx
```

### 한글 깨짐 문제
스크립트는 UTF-8 인코딩을 사용합니다. Windows에서 명령 프롬프트 사용 시:
```bash
chcp 65001  # UTF-8 코드페이지로 변경
```

### 스크립트 실행 권한 오류 (Linux/Mac)
```bash
chmod +x .claude/skills/4c-edu-ppt/scripts/generate_4c_ppt.py
```

## 활용 예시

- 기업 교육 자료
- 학교 수업 자료
- 온라인 강의 콘텐츠
- 워크샵 프레젠테이션
- 튜토리얼 가이드

## 📚 문서 및 파일 구조

### 시작하기
- [빠른 시작](docs/getting-started/QUICK_START.md) - 5분 안에 첫 PPT 만들기
- [상세 사용 가이드](docs/getting-started/HOW_TO_USE.md) - 모든 기능 설명

### AI 도구 가이드
- [AI 컨텐츠 생성 프롬프트](docs/ai-guides/AI_CONTENT_PROMPT.md) - 새 과정 만들기
- [기존 컨텐츠 변환](docs/ai-guides/CONVERT_TO_4C_PROMPT.md) - 기존 자료를 4C로 변환
- [Gemini/ChatGPT 빠른 가이드](docs/ai-guides/GEMINI_CHATGPT_QUICK.md) - 복사 & 붙여넣기
- [Claude Web 가이드](docs/ai-guides/CLAUDE_WEB_GUIDE.md) - Claude.ai 사용법
- [다른 AI 도구 활용](docs/ai-guides/USE_WITH_OTHER_AI.md) - 범용 가이드

### 템플릿 문서
- [템플릿 규칙](docs/templates/TEMPLATE_RULES.md) - 템플릿 제작 규칙
- [템플릿 커스터마이징](docs/templates/TEMPLATE_CUSTOMIZATION.md) - 디자인 수정
- [마스터 레이아웃 가이드](docs/templates/MASTER_LAYOUT_GUIDE.md) - 고급 설정

### 템플릿 파일
- [pptx-templates/](pptx-templates/) - 바로 사용 가능한 PPTX 템플릿 파일들
  - `default_4c_template.pptx` - 기본 4C 템플릿 (포함됨)

### 참고 자료
- [워크플로우 가이드](docs/reference/WORKFLOW_GUIDE.md) - 전체 작업 흐름
- [examples/](examples/) - 예제 Markdown 파일들

## 라이선스

이 Skill은 자유롭게 수정하고 배포할 수 있습니다.
