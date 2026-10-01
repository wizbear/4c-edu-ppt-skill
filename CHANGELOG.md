# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-01

Bowman(*Training From the Back of the Room!*) 원칙 정렬 릴리스. 4C를 "슬라이드 순서"가 아니라 "학습자 행동"으로 다룬다.
새 필드는 모두 선택이며 v1.0 Markdown은 그대로 빌드된다 (`examples/legacy_example_v1.md`).

### Added
- `scripts/md4c.py` — 공용 파서·카탈로그 모듈 (프론트매터, 모듈 outcome, 새 필드, Review 타입)
- `scripts/validate_markdown_v3.py` — 형식 lint(F01~F10) + 교수설계 lint(D01~D13) + 시간 리포트 + `--report` 진행표
- `scripts/swap_activity.py` — 활동 교환 (`--list`, `--to`, `--mode online`), 교환 규칙(단계·그룹·also_ok·금지쌍·모드·시간)
- `references/activities.json` / `activities.md` — 활동 카탈로그 31개 (단계·시간·인원·모드·교환 그룹·템플릿)
- `scripts/build_activity_catalog.py` — JSON → MD 생성
- Markdown 필드: 프론트매터(`course/audience/total_time/outcome/mode/group_size/strict`), 모듈 `outcome:`, `activity:`(4C 전 단계), `pattern:`/`params:`/`alt:`, `notes:`, `handout:`, `action_plan:`
- `## Review` 슬라이드 타입 (10분 규칙용 1~2분 전원 활동). 레이아웃 없으면 Concept 레이아웃 사용
- 빌드: 프론트매터 → Title_Page 슬라이드, End 슬라이드, 모듈 outcome → Module Start, 활동 블록("▶ 활동"), 실행 계획 블록, 강사 노트(활동·notes·교환 후보), `<output>_handout.md`
- `examples/example_course.md` 를 Bowman 준수 버전으로 재작성. 기존 예제는 `legacy_example_v1.md`
- `docs/proposals/2026-09-30_4c_improvement_proposal.md` — 개선 제안서 (브레인스토밍, 3회 검증, MoSCoW)

### Changed
- `SKILL.md`, `README.md` — 메인 스크립트를 `generate_with_master_layout.py` 하나로 명시. 4C 정의를 학습자 행동으로 재작성. 레거시 CLI 안내 제거
- `generate_with_master_layout.py` — md4c 파서 사용. Concept처럼 본문 placeholder가 하나인 레이아웃에서 `sub`가 누락되던 문제 수정
- AI 프롬프트(`AI_CONTENT_PROMPT.md`, `phased_prompt.md`, `CONVERT_TO_4C_PROMPT.md`, `GEMINI_CHATGPT_QUICK.md`) — 설계 규칙 블록, 활동 카탈로그 ID, 역방향 설계 순서(성과 → 실습 → 개념 → 연결 → 정리). "activity: 금지" 문구 제거
- `review_checklist.md` — 2단계를 Bowman 철칙(성과 동사, 10분 규칙, Practice 3요소, Conclusion 학습자 요약)으로 교체. 철칙 통과표 추가
- `structure_template.md`, `finalization_guide.md` — outcome, 검증 단계 반영

### Kept (legacy)
- `generate_4c_ppt.py`, `generate_from_md.py`, `validate_markdown.py`, `validate_markdown_v2.py`, `fix_markdown.py` — 파일 유지, 문서에서만 제외

## [1.0.0] - 2026-01-07

### Added
- 초기 릴리스
- 4C 교육 구조 자동 생성 (Connect-Concept-Concrete Practice-Conclusion)
- Markdown 형식 기반 컨텐츠 작성
- PowerPoint 자동 생성 스크립트
- 기본 4C 템플릿 포함 (default_4c_template.pptx)
- 슬라이드 노트 자동 생성 (#Skill, #SlideType, #Time 태그)
- Break 슬라이드 지원 (time, sub message 필드)
- Module Start 슬라이드 지원
- End 슬라이드 지원

### Documentation
- 설치 가이드 (INSTALLATION.md)
- 배포 가이드 (DISTRIBUTION.md)
- 상세 사용 설명서 (docs/)
  - 빠른 시작 가이드
  - AI 도구 가이드 (Gemini/ChatGPT/Claude Web)
  - 기존 컨텐츠 변환 프롬프트
  - 템플릿 커스터마이징 가이드
- 예제 파일 포함

### Features
- Master Layout 지원
- Title_Page, Module_Divider 레이아웃
- Connect, Concept, Concrete Practice, Conclusion 레이아웃
- Break, End 레이아웃
- 자동 시간 배치
- 다국어 지원 (한국어, 영어)

### Tools
- generate_with_master_layout.py - 메인 생성 스크립트
- validate_markdown_v2.py - Markdown 검증 도구
- auto_fix_markdown.py - 자동 수정 도구
