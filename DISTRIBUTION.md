# 4C PPT 스킬 배포 가이드

> 스킬 제작자를 위한 배포 및 공유 가이드

---

## 📋 목차

1. [배포 전 체크리스트](#1-배포-전-체크리스트)
2. [배포 방식 선택](#2-배포-방식-선택)
3. [Git 저장소로 배포](#3-git-저장소로-배포)
4. [ZIP 파일로 배포](#4-zip-파일로-배포)
5. [업데이트 관리](#5-업데이트-관리)
6. [버전 관리](#6-버전-관리)
7. [사용자 지원](#7-사용자-지원)

---

## 1. 배포 전 체크리스트

### 1-1. 필수 파일 확인

```bash
cd .claude/skills/4c-edu-ppt
```

**필수 파일:**
- [ ] `SKILL.md` - 스킬 정의 파일
- [ ] `README.md` - 스킬 개요 및 사용법
- [ ] `INSTALLATION.md` - 설치 가이드
- [ ] `scripts/` - 실행 스크립트
- [ ] `pptx-templates/default_4c_template.pptx` - 기본 템플릿
- [ ] `examples/` - 예제 파일

**선택 파일:**
- [ ] `docs/` - 상세 문서
- [ ] `LICENSE` - 라이선스 파일
- [ ] `.gitignore` - Git 제외 파일

---

### 1-2. SKILL.md 검증

**SKILL.md 필수 필드 확인:**

```yaml
---
name: 4c-edu-ppt                    # 스킬 이름 (소문자, 하이픈만)
description: 4C 교육 구조...        # 명확한 설명
allowed-tools: Read, Bash, Write   # 사용할 도구
---
```

**검증:**
```bash
# SKILL.md 첫 줄과 끝 줄이 '---'인지 확인
head -n 1 SKILL.md
grep -n "^---$" SKILL.md
```

---

### 1-3. 테스트

**로컬에서 테스트:**

```bash
# Claude Code 시작
claude

# 스킬 확인
> What skills are available?

# 테스트 실행
> 4C 구조로 간단한 테스트 PPT를 만들어줘
```

**✅ 정상 작동 확인 후 배포**

---

## 2. 배포 방식 선택

### 비교표

| 방식 | 장점 | 단점 | 추천 대상 |
|------|------|------|-----------|
| **Git 저장소** | 버전 관리, 쉬운 업데이트 | Git 지식 필요 | 팀, 오픈소스 |
| **ZIP 파일** | 간단, 빠름 | 업데이트 어려움 | 개인, 일회성 |
| **플러그인** | 여러 저장소 공유 가능 | 복잡한 설정 | 대규모 조직 |

---

## 3. Git 저장소로 배포

### 3-1. 저장소 준비

#### 옵션 A: 기존 프로젝트에 포함

**현재 프로젝트가 Git 저장소인 경우:**

```bash
# 현재 상태 확인
git status

# 스킬 파일 추가
git add .claude/skills/4c-edu-ppt/

# 커밋
git commit -m "Add: 4C 교육 PPT 생성 스킬

- 4C 구조 자동 생성
- 기본 템플릿 포함
- 다양한 AI 도구 가이드 포함
"

# 푸시
git push origin main
```

---

#### 옵션 B: 별도 저장소 생성 (권장)

**독립적인 스킬 저장소:**

```bash
# 새 디렉토리 생성
mkdir 4c-edu-ppt-skill
cd 4c-edu-ppt-skill

# Git 초기화
git init

# 스킬 파일 복사
cp -r ../your-project/.claude/skills/4c-edu-ppt/* .

# README.md 수정 (저장소 설명 추가)
# INSTALLATION.md 경로 업데이트

# 첫 커밋
git add .
git commit -m "Initial commit: 4C 교육 PPT 스킬"

# GitHub 저장소 생성 후
git remote add origin https://github.com/your-username/4c-edu-ppt-skill.git
git branch -M main
git push -u origin main
```

---

### 3-2. README.md 업데이트

**저장소 README에 추가:**

```markdown
# 4C 교육 PPT 생성 스킬

Claude Code 스킬로 4C 교수법 기반 교육 PPT를 자동 생성합니다.

## 설치

### 1. 저장소 클론

\`\`\`bash
git clone https://github.com/your-username/4c-edu-ppt-skill.git
cd 4c-edu-ppt-skill
\`\`\`

### 2. 스킬 배치

**프로젝트 스킬:**
\`\`\`bash
mkdir -p your-project/.claude/skills
cp -r . your-project/.claude/skills/4c-edu-ppt
\`\`\`

**글로벌 스킬:**
\`\`\`bash
mkdir -p ~/.claude/skills
cp -r . ~/.claude/skills/4c-edu-ppt
\`\`\`

### 3. Python 라이브러리 설치

\`\`\`bash
pip install python-pptx
\`\`\`

## 사용법

[INSTALLATION.md](INSTALLATION.md) 참조

## 라이선스

MIT
```

---

### 3-3. .gitignore 추가

**불필요한 파일 제외:**

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# 테스트 결과물
test_output.pptx
courses/*.pptx
*.pptx
!pptx-templates/*.pptx
EOF
```

---

### 3-4. 태그 및 릴리스

**버전 태그 생성:**

```bash
# 버전 1.0.0 태그
git tag -a v1.0.0 -m "Release v1.0.0

Features:
- 4C 구조 자동 생성
- 기본 템플릿 포함
- Markdown 형식 지원
- 슬라이드 노트 자동 생성
"

# 태그 푸시
git push origin v1.0.0
```

**GitHub Release 생성:**
1. GitHub 저장소 → "Releases" → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `4C PPT Skill v1.0.0`
4. Description: 주요 기능 설명
5. "Publish release"

---

## 4. ZIP 파일로 배포

### 4-1. 배포용 ZIP 생성

**불필요한 파일 제외:**

```bash
cd .claude/skills

# ZIP 파일 생성 (Windows)
powershell Compress-Archive -Path 4c-edu-ppt -DestinationPath 4c-edu-ppt-v1.0.0.zip

# ZIP 파일 생성 (Mac/Linux)
zip -r 4c-edu-ppt-v1.0.0.zip 4c-edu-ppt \
  -x "4c-edu-ppt/__pycache__/*" \
  -x "4c-edu-ppt/*.pyc" \
  -x "4c-edu-ppt/test_output.pptx"
```

---

### 4-2. ZIP 파일 배포

**배포 채널:**

1. **이메일**
   - ZIP 파일 첨부
   - INSTALLATION.md 내용 이메일 본문에 요약

2. **공유 드라이브**
   - Google Drive, Dropbox, OneDrive
   - 공유 링크 생성

3. **웹 다운로드**
   - GitHub Release에 ZIP 파일 첨부
   - 자체 웹사이트에서 다운로드 제공

---

### 4-3. 사용자 안내 메시지

**이메일/메시지 템플릿:**

```
안녕하세요,

4C 교육 PPT 생성 스킬을 공유합니다.

## 다운로드
첨부 파일: 4c-edu-ppt-v1.0.0.zip

## 설치 방법

1. ZIP 파일 압축 해제
2. 프로젝트 디렉토리로 이동
3. 스킬 복사:
   Windows: xcopy /E /I 4c-edu-ppt .claude\skills\4c-edu-ppt
   Mac/Linux: cp -r 4c-edu-ppt .claude/skills/

4. Python 라이브러리 설치:
   pip install python-pptx

5. Claude Code 시작:
   claude

6. 스킬 확인:
   What skills are available?

자세한 설치 가이드는 압축 파일 내 INSTALLATION.md를 참조하세요.

문제가 있으면 연락주세요!
```

---

## 5. 업데이트 관리

### 5-1. Git 저장소 업데이트

**변경사항 커밋:**

```bash
# 변경 파일 추가
git add .

# 커밋
git commit -m "Update: Break 슬라이드 기능 추가

- time 필드 지원
- sub message 표시
- 슬라이드 노트에 태그 추가
"

# 푸시
git push origin main
```

**사용자에게 업데이트 안내:**

```bash
# 릴리스 노트 작성
git tag -a v1.1.0 -m "Release v1.1.0

New Features:
- Break 슬라이드 개선
- 슬라이드 노트 자동 태그

Bug Fixes:
- 템플릿 경로 오류 수정
"

git push origin v1.1.0
```

---

### 5-2. 사용자가 업데이트 받는 방법

**Git 사용자:**

```bash
cd your-project/.claude/skills/4c-edu-ppt
git pull origin main
```

**ZIP 사용자:**
- 새 버전 다운로드
- 기존 파일 백업
- 새 파일로 교체

---

### 5-3. 변경 로그 관리

**CHANGELOG.md 작성:**

```markdown
# Changelog

## [1.1.0] - 2026-01-07

### Added
- Break 슬라이드 time, sub 필드 지원
- 슬라이드 노트 자동 태그 (#Skill, #SlideType, #Time)
- 기존 컨텐츠 변환 프롬프트 (CONVERT_TO_4C_PROMPT.md)

### Changed
- 문서 구조 정리 (docs/ 디렉토리)
- README.md 개선

### Fixed
- 템플릿 경로 오류 수정

## [1.0.0] - 2026-01-05

### Added
- 초기 릴리스
- 4C 구조 자동 생성
- 기본 템플릿 포함
```

---

## 6. 버전 관리

### 6-1. 버전 번호 규칙

**Semantic Versioning (MAJOR.MINOR.PATCH):**

```
v1.2.3
│ │ │
│ │ └─ PATCH: 버그 수정
│ └─── MINOR: 기능 추가 (하위 호환)
└───── MAJOR: 주요 변경 (하위 호환 안됨)
```

**예시:**
- `v1.0.0` → `v1.0.1`: 버그 수정
- `v1.0.0` → `v1.1.0`: 새 기능 추가
- `v1.0.0` → `v2.0.0`: API 변경 (기존 사용법 안 맞음)

---

### 6-2. 버전 정보 파일

**VERSION 파일 추가:**

```bash
echo "1.1.0" > VERSION
git add VERSION
git commit -m "Bump version to 1.1.0"
```

**SKILL.md에 버전 추가:**

```yaml
---
name: 4c-edu-ppt
version: 1.1.0
description: 4C 교육 구조...
---
```

---

## 7. 사용자 지원

### 7-1. 문서화

**필수 문서:**
- [ ] README.md - 개요, 빠른 시작
- [ ] INSTALLATION.md - 설치 가이드
- [ ] DISTRIBUTION.md - 배포 가이드 (이 문서)
- [ ] docs/ - 상세 가이드

---

### 7-2. 이슈 관리

**GitHub Issues 활용:**

1. **Issues 탭 활성화**
2. **Issue 템플릿 생성**

`.github/ISSUE_TEMPLATE/bug_report.md`:
```markdown
---
name: 버그 리포트
about: 스킬 사용 중 발생한 문제
---

## 문제 설명
[문제를 명확하게 설명]

## 재현 방법
1. [단계 1]
2. [단계 2]
3. [오류 발생]

## 예상 동작
[정상 동작 설명]

## 환경
- OS: [Windows/Mac/Linux]
- Python 버전: [3.x]
- Claude Code 버전: [x.x.x]
- 스킬 버전: [1.x.x]

## 추가 정보
[스크린샷, 로그 등]
```

---

### 7-3. FAQ 문서

**docs/FAQ.md:**

```markdown
# 자주 묻는 질문 (FAQ)

## Q1: 스킬이 인식되지 않습니다
A: SKILL.md가 올바른 위치(.claude/skills/4c-edu-ppt/)에 있는지 확인하세요.

## Q2: python-pptx 오류가 발생합니다
A: `pip install python-pptx` 실행 후 재시도하세요.

## Q3: 템플릿을 커스터마이징하려면?
A: docs/templates/TEMPLATE_CUSTOMIZATION.md를 참조하세요.
```

---

## 8. 배포 체크리스트

### 배포 전

- [ ] 모든 파일 테스트 완료
- [ ] SKILL.md 검증
- [ ] README.md 업데이트
- [ ] INSTALLATION.md 경로 확인
- [ ] 버전 번호 업데이트
- [ ] CHANGELOG.md 작성
- [ ] .gitignore 설정

### Git 배포

- [ ] 저장소 생성/업데이트
- [ ] 커밋 및 푸시
- [ ] 태그 생성
- [ ] Release 작성
- [ ] 사용자 공지

### ZIP 배포

- [ ] 불필요한 파일 제거
- [ ] ZIP 파일 생성
- [ ] 압축 파일 테스트
- [ ] 배포 채널 업로드
- [ ] 사용자 안내 메시지 발송

---

## 9. 라이선스

**LICENSE 파일 추가 (선택):**

MIT License 예시:
```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 📞 문의

배포 과정에서 문제가 발생하면:
- GitHub Issues: https://github.com/your-username/4c-edu-ppt-skill/issues
- Email: your-email@example.com

**성공적인 배포를 응원합니다!** 🚀
