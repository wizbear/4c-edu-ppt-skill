# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
