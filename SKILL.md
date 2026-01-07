---
name: 4c-edu-ppt
description: 4C 교육 구조(Connect-Concept-Concrete Practice-Conclusion)로 교육용 PowerPoint 프레젠테이션 생성. 교육 자료, PPT, 프레젠테이션, 강의 자료 작성 시 사용.
allowed-tools: Read, Bash, Write
---

# 4C 교육 구조 기반 PPT 제작

4C 교육 구조(Connect - Concept - Concrete Practice - Conclusion)를 활용하여 체계적인 교육용 PowerPoint 프레젠테이션을 자동 생성합니다.

## 4C 교육 구조란?

- **Connect (연결)**: 학습자의 사전 경험과 새로운 학습 내용을 연결
- **Concept (개념)**: 핵심 개념과 원리를 명확하게 제시
- **Concrete Practice (구체화)**: 실제 적용 가능한 연습과 예시 제공
- **Conclusion (정리)**: 학습 내용을 요약하고 성찰

## 사용 방법

### 방법 1: Markdown 파일 사용 (권장)

**가장 쉽고 유연한 방법입니다!** 콘텐츠를 Markdown 파일로 작성하면:
- 모듈 구조로 체계적 구성
- 4C 슬라이드 반복 가능
- 이미지, 비디오, Break 슬라이드 추가 가능
- 버전 관리 및 협업 용이

#### Markdown 파일 구조:

```markdown
# 모듈 1: Python 기초

## Module Start
모듈 소개 내용

## Connect
time: 5분
title: 연결하기
main: 학습자와 연결할 내용
sub: 보조 설명

## Concept
time: 10분
title: 개념 설명
main: 핵심 개념
sub: 상세 설명

## Concrete Practice
time: 15분
title: 실습
main: 실습 설명
activity: |
  1. 단계 1
  2. 단계 2

## Conclusion
time: 5분
title: 정리
main: 요약 내용
sub: 다음 학습 예고

## Break
```

#### 실행 방법:

```bash
python .claude/skills/4c-edu-ppt/scripts/generate_from_md.py \
  --md course_content.md \
  --template my_template.pptx \
  --output result.pptx
```

**예제 파일**: `.claude/skills/4c-edu-ppt/examples/example_course.md` 참고

### 방법 2: 명령줄 인자 사용 (간단한 PPT)

간단한 1회성 PPT 생성 시 사용:

#### 필수 요구사항:

```bash
pip install python-pptx
```

#### PPT 생성 요청:

사용자에게 다음 정보를 요청합니다:

1. **교육 주제/제목**: 프레젠테이션의 메인 주제
2. **Connect (연결)**: 학습자와 연결할 내용 (질문, 경험, 상황 등)
3. **Concept (개념)**: 가르칠 핵심 개념과 내용
4. **Concrete Practice (구체화)**: 실습, 예제, 활동 내용
5. **Conclusion (정리)**: 요약 및 마무리 내용

### 3. PPT 생성 프로세스

다음 단계로 PowerPoint 파일을 생성합니다:

1. 사용자로부터 각 단계별 내용 수집
2. `scripts/generate_4c_ppt.py` 스크립트 실행
3. 생성된 `.pptx` 파일 확인 및 전달

### 4. 실행 예시

```bash
python .claude/skills/4c-edu-ppt/scripts/generate_4c_ppt.py \
  --title "Python 기초 - 변수와 데이터 타입" \
  --connect "여러분은 일상에서 정보를 어떻게 기억하나요? 이름표를 붙여 기억하시죠?" \
  --concept "변수는 데이터를 저장하는 이름표입니다. Python에는 숫자, 문자열, 리스트 등 다양한 데이터 타입이 있습니다." \
  --practice "실습: 자신의 이름과 나이를 변수에 저장하고 출력해봅시다." \
  --conclusion "오늘 배운 변수와 데이터 타입은 모든 프로그래밍의 기초입니다." \
  --output "python_basics.pptx"
```

### 5. 커스텀 템플릿 사용

자신만의 PPTX 템플릿을 사용하려면 `--template` 옵션을 추가하세요:

```bash
python .claude/skills/4c-edu-ppt/scripts/generate_4c_ppt.py \
  --template "내_템플릿.pptx" \
  --title "교육 주제" \
  --connect "연결 내용" \
  --concept "개념 내용" \
  --practice "실습 내용" \
  --conclusion "정리 내용" \
  --output "결과물.pptx"
```

**템플릿 사용 시 참고사항:**
- 템플릿의 슬라이드 레이아웃(마스터 슬라이드)이 유지됩니다
- 색상 테마, 폰트, 배경 디자인이 템플릿을 따릅니다
- 레이아웃 0번(제목 슬라이드)과 1번(제목+내용)을 사용합니다
- 템플릿 파일이 없거나 오류 시 기본 프레젠테이션으로 생성됩니다

## 생성되는 슬라이드 구조

1. **제목 슬라이드**: 교육 주제
2. **Connect 슬라이드**: 학습자와의 연결
3. **Concept 슬라이드**: 핵심 개념 설명
4. **Concrete Practice 슬라이드**: 실습 및 예제
5. **Conclusion 슬라이드**: 요약 및 정리
6. **감사 슬라이드**: 마무리 인사

## 커스터마이징

생성된 PPT는 다음과 같이 커스터마이징할 수 있습니다:

- 디자인 템플릿 변경
- 색상 테마 조정
- 글꼴 스타일 변경
- 이미지 및 도표 추가

## 주의사항

- 각 단계의 내용은 명확하고 구체적으로 작성
- Connect는 학습자의 관심을 끌 수 있는 질문이나 상황으로 시작
- Concept은 핵심 내용만 간결하게 정리
- Practice는 실제로 해볼 수 있는 구체적인 활동 제시
- Conclusion은 학습 목표 달성 여부를 확인할 수 있도록 작성

## 문제 해결

- **python-pptx 미설치**: `pip install python-pptx` 실행
- **한글 깨짐**: UTF-8 인코딩 확인
- **스크립트 권한 오류**: 스크립트 실행 권한 확인
