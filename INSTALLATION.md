# 4C PPT 스킬 설치 가이드

> 완전히 처음부터 시작하는 분들을 위한 단계별 설치 가이드

---

## 📋 목차

1. [필수 사항 확인](#1-필수-사항-확인)
2. [스킬 다운로드](#2-스킬-다운로드)
3. [Python 라이브러리 설치](#3-python-라이브러리-설치)
4. [스킬 배치](#4-스킬-배치)
5. [설치 확인](#5-설치-확인)
6. [첫 PPT 만들기](#6-첫-ppt-만들기)
7. [문제 해결](#7-문제-해결)

---

## 1. 필수 사항 확인

### 1-1. Claude Code 설치 여부 확인

**명령 프롬프트(Windows) 또는 터미널(Mac/Linux)에서:**

```bash
claude --version
```

**출력 예시:**
```
Claude Code CLI v1.x.x
```

**설치되지 않았다면:**
- 공식 사이트 방문: https://claude.com/claude-code
- 설치 가이드 따라 설치

---

### 1-2. Python 설치 여부 확인

**명령 프롬프트에서:**

```bash
python --version
```

**출력 예시:**
```
Python 3.8.10
```

**Python 3.7 이상이 필요합니다.**

**설치되지 않았다면:**
- Windows: https://www.python.org/downloads/
- Mac: `brew install python3`
- Linux: `sudo apt install python3`

---

## 2. 스킬 다운로드

### 옵션 A: Git으로 클론 (권장)

**저장소가 있는 경우:**

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

스킬이 `.claude/skills/4c-edu-ppt/` 위치에 있습니다.

---

### 옵션 B: ZIP 파일 다운로드

**1. ZIP 파일 받기**
- 제공받은 `4c-edu-ppt.zip` 다운로드

**2. 압축 해제**
```
4c-edu-ppt.zip 우클릭 → 압축 풀기
```

**3. 다음 단계로 진행**

---

## 3. Python 라이브러리 설치

### 3-1. python-pptx 설치

**명령 프롬프트에서:**

```bash
pip install python-pptx
```

**출력 예시:**
```
Successfully installed python-pptx-0.6.21
```

---

### 3-2. 설치 확인

```bash
python -c "import pptx; print('python-pptx 설치 완료')"
```

**성공 메시지:**
```
python-pptx 설치 완료
```

---

## 4. 스킬 배치

### 4-1. 배치 방식 선택

#### 방식 1: 프로젝트 스킬 (권장)

**특정 프로젝트에서만 사용**

**Windows:**
```bash
# 프로젝트 디렉토리로 이동
cd C:\Users\YourName\MyProjects\my-education-project

# .claude/skills 디렉토리 생성
mkdir .claude\skills

# 스킬 복사
xcopy /E /I "C:\Downloads\4c-edu-ppt" ".claude\skills\4c-edu-ppt"
```

**Mac/Linux:**
```bash
# 프로젝트 디렉토리로 이동
cd ~/MyProjects/my-education-project

# .claude/skills 디렉토리 생성
mkdir -p .claude/skills

# 스킬 복사
cp -r ~/Downloads/4c-edu-ppt .claude/skills/
```

---

#### 방식 2: 글로벌 스킬

**모든 프로젝트에서 사용**

**Windows:**
```bash
# 홈 디렉토리에 글로벌 스킬 디렉토리 생성
mkdir %USERPROFILE%\.claude\skills

# 스킬 복사
xcopy /E /I "C:\Downloads\4c-edu-ppt" "%USERPROFILE%\.claude\skills\4c-edu-ppt"
```

**Mac/Linux:**
```bash
# 글로벌 스킬 디렉토리 생성
mkdir -p ~/.claude/skills

# 스킬 복사
cp -r ~/Downloads/4c-edu-ppt ~/.claude/skills/
```

---

### 4-2. 디렉토리 구조 확인

**프로젝트 스킬인 경우:**

```
my-education-project/
└── .claude/
    └── skills/
        └── 4c-edu-ppt/
            ├── SKILL.md
            ├── README.md
            ├── scripts/
            ├── pptx-templates/
            ├── docs/
            └── examples/
```

**글로벌 스킬인 경우:**

```
~/.claude/skills/
└── 4c-edu-ppt/
    ├── SKILL.md
    ├── README.md
    ├── scripts/
    ├── pptx-templates/
    ├── docs/
    └── examples/
```

---

## 5. 설치 확인

### 5-1. Claude Code 시작

**명령 프롬프트에서:**

```bash
# 프로젝트 디렉토리로 이동 (프로젝트 스킬인 경우)
cd C:\Users\YourName\MyProjects\my-education-project

# Claude Code 시작
claude
```

---

### 5-2. 스킬 등록 확인

**Claude Code에서:**

```
What skills are available?
```

**예상 출력:**
```
Available skills:
- 4c-edu-ppt: 4C 교육 구조(Connect-Concept-Concrete Practice-Conclusion)로
  교육용 PowerPoint 프레젠테이션 생성. 교육 자료, PPT, 프레젠테이션, 강의 자료 작성 시 사용.
```

**✅ 이렇게 나오면 설치 성공!**

---

## 6. 첫 PPT 만들기

### 6-1. 간단한 테스트

**Claude Code에서 요청:**

```
Python 기초 - 변수 개념을 4C 구조로 교육용 PPT를 만들어줘.

- 대상: 프로그래밍 초보자
- 시간: 20분
- 모듈: 1개
```

---

### 6-2. 생성 과정

Claude가 자동으로:
1. 4C 구조 Markdown 생성
2. 파일 저장
3. PPT 생성 스크립트 실행
4. PPT 파일 생성

---

### 6-3. 결과 확인

**생성된 파일:**
```
my-education-project/
├── courses/
│   └── Python기초_변수개념_YYYY-MM-DD.pptx
└── .claude/
    └── skills/
        └── 4c-edu-ppt/
```

**PPT 파일 열어서 확인:**
- Title_Page
- Module Start
- Connect
- Concept
- Concrete Practice
- Conclusion
- End

---

## 7. 문제 해결

### 문제 1: "스킬을 찾을 수 없습니다"

**원인**: 스킬 위치가 잘못됨

**해결:**

```bash
# 현재 디렉토리에서 스킬 확인
dir .claude\skills\4c-edu-ppt\SKILL.md       # Windows
ls .claude/skills/4c-edu-ppt/SKILL.md        # Mac/Linux
```

**SKILL.md가 없으면:**
- 스킬 복사 단계를 다시 진행
- 경로가 정확한지 확인

---

### 문제 2: "python-pptx를 찾을 수 없습니다"

**원인**: Python 라이브러리가 설치되지 않음

**해결:**

```bash
pip install python-pptx
```

**여전히 안 되면:**
```bash
python -m pip install python-pptx
```

---

### 문제 3: "템플릿을 찾을 수 없습니다"

**원인**: 기본 템플릿 파일이 없음

**확인:**
```bash
# 템플릿 파일 존재 확인
dir .claude\skills\4c-edu-ppt\pptx-templates\default_4c_template.pptx     # Windows
ls .claude/skills/4c-edu-ppt/pptx-templates/default_4c_template.pptx      # Mac/Linux
```

**파일이 없으면:**
- 스킬을 다시 다운로드하거나
- 자신의 템플릿을 추가

---

### 문제 4: "명령어를 찾을 수 없습니다"

**원인**: PATH 설정 문제

**Windows:**
```bash
# Python 경로 확인
where python

# pip 경로 확인
where pip
```

**Mac/Linux:**
```bash
# Python 경로 확인
which python3

# pip 경로 확인
which pip3
```

**해결**: Python을 재설치하고 "Add to PATH" 옵션 선택

---

### 문제 5: "한글이 깨집니다"

**원인**: 인코딩 문제

**Windows 명령 프롬프트에서:**
```bash
chcp 65001
```

**Python 스크립트 실행 시:**
```bash
python script.py
# 대신
python -X utf8 script.py
```

---

## 8. 다음 단계

### 8-1. 문서 읽기

**빠른 시작:**
```
.claude/skills/4c-edu-ppt/docs/getting-started/QUICK_START.md
```

**다른 AI 도구 사용:**
```
.claude/skills/4c-edu-ppt/docs/ai-guides/GEMINI_CHATGPT_QUICK.md
```

**템플릿 커스터마이징:**
```
.claude/skills/4c-edu-ppt/docs/templates/TEMPLATE_CUSTOMIZATION.md
```

---

### 8-2. 예제 살펴보기

**예제 Markdown 파일:**
```
.claude/skills/4c-edu-ppt/examples/example_course.md
```

**예제로 PPT 생성해보기:**
```bash
cd .claude/skills/4c-edu-ppt

python scripts/generate_with_master_layout.py \
  --md examples/example_course.md \
  --template pptx-templates/default_4c_template.pptx \
  --output test_output.pptx
```

---

## ✅ 설치 완료 체크리스트

- [ ] Claude Code 설치 확인 (`claude --version`)
- [ ] Python 설치 확인 (`python --version`)
- [ ] python-pptx 설치 (`pip install python-pptx`)
- [ ] 스킬 다운로드 (Git clone 또는 ZIP)
- [ ] 스킬 배치 (`.claude/skills/4c-edu-ppt/`)
- [ ] SKILL.md 파일 존재 확인
- [ ] 템플릿 파일 존재 확인
- [ ] Claude Code에서 스킬 확인 (`What skills are available?`)
- [ ] 테스트 PPT 생성 성공
- [ ] 문서 읽기 시작

---

## 🚀 시작하기

설치가 완료되었다면:

```
Claude Code를 열고 다음과 같이 요청하세요:

"4C 구조로 [주제] 교육 PPT를 만들어줘"
```

**예시:**
- "4C 구조로 Excel 피벗 테이블 교육 PPT를 만들어줘"
- "파이썬 리스트 개념을 4C로 설명하는 PPT 만들어줘"
- "비폭력대화 입문 과정을 4C 구조로 만들어줘"

---

## 💬 도움이 필요하신가요?

- README.md - 전체 개요
- docs/getting-started/HOW_TO_USE.md - 상세 사용법
- docs/ai-guides/ - AI 도구 활용 가이드
- GitHub Issues - 문제 신고

**행복한 교육 자료 제작 되세요!** 🎓
