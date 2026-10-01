# 4c-edu-ppt 스킬 개선 제안서 (v1.1 후보)

- 작성일: 2026-09-30
- 이론 근거: Sharon L. Bowman, *Training From the Back of the Room!* (4 Cs)
- 대상 버전: 현재 v1.0.0 → 다음 릴리스
- 진행 순서: 현황 진단 → 브레인스토밍(40건) → 3회 비판 검증 → 통합 → MoSCoW 분류 → 릴리스 단계 제안

---

## 0. 요약

현재 스킬은 4C를 **슬라이드 4종의 순서**로 구현했다. Bowman의 4C는 **각 단계에서 학습자가 무엇을 하는가**로 정의된다. 이 간극이 가장 크고, 다른 개선점 대부분이 여기서 파생된다.

3회 검증 후 살아남은 아이디어는 28건이며, MoSCoW 결과는 다음과 같다.

| 분류 | 건수 | 핵심 |
|---|---|---|
| Must | 7 | 학습자 행동 필드, 학습 성과 필드, 10분 규칙, SKILL.md 정합성, 예제·프롬프트 재작성 |
| Should | 10 | 활동 카탈로그, 시간 리포트, 강사 노트, need-to-know 분리, 활동 패턴 참조 + 교환 제어 |
| Could | 12 | Warm-Up, 온라인 모드, 다양성 검사, 덱 분리, 테스트, 일괄 교환 |
| Won't (이번 주기) | 5 | 자동 분할, 라운드트립, docx 핸드아웃, 별도 평가 모듈, 디자인 자동화 |

---

## 1. 현황 진단

### 1.1 스킬이 지금 하는 것

- Markdown(`## Connect` 등 섹션 + `time/title/main/sub/activity` 필드) → python-pptx로 PPTX 생성
- Module Start, Image, Video, Break, End 슬라이드 지원
- 형식 검증(`validate_markdown_v2.py`), 자동 수정(`fix_markdown.py`)
- 문서: AI 프롬프트 가이드, 단계별 생성 프롬프트, 검토 체크리스트, 최종화 가이드

### 1.2 Bowman 원전과의 간극

| Bowman 원칙 | 현재 스킬 상태 | 간극 |
|---|---|---|
| 4C는 **학습자 행동**으로 정의 | 필드가 `main/sub` = 강사가 말할 내용 | 학습자가 무엇을 하는지 기록할 자리가 없음 |
| Whoever explains, learns | Concept는 불릿 3~5개 강의 | 강의 슬라이드 그 자체 |
| 10분 규칙 | 예제에 Concept 12분, 15분 존재. 검증 없음 | 규칙 위반을 스킬이 권장하는 셈 |
| 학습 성과 = 관찰 가능 동사 + 개념 | 성과 필드 없음. 구조 템플릿에 자유 텍스트만 | "이해한다" 같은 금지 동사를 거를 장치 없음 |
| Connections ≠ 아이스브레이커, 주제 관련 활동 먼저 | Connect가 수사적 질문 1개("~해본 적 있나요?") | 학습자 활동이 아니라 강사의 도입 멘트 |
| Practice 3요소(전원 참여·상호의존·개인 책임) | `activity:` 자유 서술 | 감사 기준 없음 |
| Conclusion 4요소(학습자 요약·평가·액션플랜·축하) | 예제가 강사 요약("오늘 배운 내용 ✓") | 학습자가 요약해야 하는데 강사가 함 |
| Need-to-know 필터, 슬라이드 복사본 배포 금지 | 모든 내용이 슬라이드로 | nice-to-know를 분리할 곳 없음 |
| Primacy-Recency: 하우스키핑은 중간 | Module Start(소개)가 Connect 앞 | 소개 슬라이드가 20자 이내 분리자라면 문제 없음. 문서에 명시 필요 |

### 1.3 이론 외 문제

- SKILL.md가 `generate_from_md.py`, `generate_4c_ppt.py`를 안내하지만 finalization_guide와 CHANGELOG는 `generate_with_master_layout.py`를 메인으로 지목. 진입점 불일치.
- 생성 스크립트 3종, 검증 스크립트 2종 공존. 어느 것을 쓸지 문서마다 다름.
- `validate_markdown_v2.py`가 Connect에 `sub`를 필수로 요구. Connect에 `activity`를 쓰면 오류.
- 슬라이드 노트에 `#Skill #SlideType #Time` 태그만 있음. 강사가 실제로 필요한 진행 정보 없음.

---

## 2. 브레인스토밍 (40건)

### A. 이론 충실도 (Bowman → 스킬)

| # | 아이디어 | 근거 |
|---|---|---|
| A1 | 모듈 프론트매터에 `outcome:` 필수화. 금지 동사(알다·이해하다·배우다·숙지하다·인식하다) lint | ch22 성과 공식 |
| A2 | 4C 전 단계에 `activity:` 필드 허용. "학습자가 하는 것"을 기록. Concept에도 허용 | 4C 정의, Whoever explains learns |
| A3 | Concept `time` > 10분 경고, > 20분 오류 | ch02, ch08 10분 규칙 |
| A4 | 새 슬라이드 타입 `## Review`: 1~2분 전원 참여 리뷰(Turn and Talk, Pass That Card, Stand-Stretch-Speak) | ch10 Interactive Lecture |
| A5 | Connect에 `type: fast-pass \| start-up \| warm-up` 태그, 주제 관련성 검증 항목 | ch05~07 Time-Layered Openers |
| A6 | Practice에 `participation:` `accountability:` 필드 또는 체크리스트(3요소 감사) | ch13 |
| A7 | Conclusion에 `summary/evaluate/action_plan/celebrate` 4개 서브필드 | ch17 |
| A8 | `handout:` 필드로 nice-to-know 분리 → 부록 MD 생성 | ch03 Need-to-know |
| A9 | Concept 항목별 `mode: hear \| learn` 태그. learn이면 활동 필수 | ch01 Hear-it-or-learn-it |
| A10 | Bowman 활동 카탈로그(C별, 시간, 인원, 준비물, 온/오프) 참조 파일 | ch05~20 |
| A11 | 강사 노트 강화: 진행 스크립트, 디브리프 질문, 준비물, 타이밍 큐 | ch07 debrief 필수 |
| A12 | 학습자 핸드아웃(그래픽 오거나이저·빈 컨셉맵) 생성 | ch08~09, 슬라이드 복사본 금지 |
| A13 | 과정 레벨 `## Warm-Up` 섹션: 사전 과제 텍스트 + 책임 장치 | ch05 |
| A14 | Kirkpatrick 1~3 학습자 중심 평가 슬라이드 | ch19 |
| A15 | 같은 활동 유형 연속 시 경고(습관화 방지) | ch02 habituation |
| A16 | Conclusion 최소 시간 규칙, 하우스키핑은 Connect 뒤 | ch04, ch17 Primacy-Recency |
| A17 | Practice 활동 유형 태그(teach-back/skills/game), Jigsaw는 Concept에만 | ch11, ch14 |
| A18 | 강사 발화 vs 학습자 활동 시간 비율 추정(2/3 규칙) | ch01 |
| A19 | 학습자 중심 평가 문항("무엇을 배웠고 무엇을 할 것인가") 생성 | ch19 |

### B. 도구·자동화

| # | 아이디어 |
|---|---|
| B1 | validate v3: 형식 lint와 교수설계 lint 분리, 심각도(error/warn/info) |
| B2 | 시간 리포트: 모듈별·총합·버퍼·강사/학습자 비율 |
| B3 | 아젠다 슬라이드 + 강사용 run-sheet(MD/CSV) 자동 생성 |
| B4 | 텍스트 넘침 휴리스틱(글자수·줄수 기준 경고) |
| B5 | YAML 프론트매터(과정명, 대상, 총시간, 성과, 모드) |
| B6 | 단일 진입점 CLI: `4c validate / build / fix / report` |
| B7 | pytest + 골든 파일 회귀 테스트 |
| B8 | PPTX → MD 역추출(라운드트립) |
| B9 | SKILL.md 슬림화, 메인 스크립트 단일 명시, 레거시 스크립트 정리 |
| B10 | 활동 추천 도우미(시간·인원·모드 입력 → 활동 제안) |

### C. 콘텐츠 생성 워크플로

| # | 아이디어 |
|---|---|
| C1 | AI 프롬프트에 Bowman 철칙 주입(학습자 행동 동사, 활동 명시 강제) |
| C2 | 설계 순서 역방향: 성과 → Practice → Concept → Connect → Conclusion(인덱스카드 설계) |
| C3 | 대상자 프로파일 필드 → 예시·난이도 조정 |
| C4 | 온라인/오프라인 모드(body break, 채팅 활동, e-learning bracket) |
| C5 | review_checklist에 철칙 10개 반영, 점수화 |
| C6 | 예제 파일을 Bowman 준수 버전으로 재작성 |

### D. 템플릿·출력

| # | 아이디어 |
|---|---|
| D1 | Review/Activity 레이아웃 추가, 타이머 표시 영역 |
| D2 | 학습자 지시문 전용 placeholder |
| D3 | 강사 덱 vs 학습자 배포 덱 분리 출력 |
| D4 | 접근성 최소치(대비, 폰트 크기) 검사 |
| D5 | 이미지 자동 생성·디자인 자동화 |

---

## 3. 비판 검증 3회

### 3.1 검증 1회차: 이론 정합성 — "Bowman이 정말 그렇게 말했나? 과잉 해석은 없나?"

| # | 판정 | 근거 |
|---|---|---|
| A1 | 유지 | ch22 원문 그대로. 한국어 금지 동사 목록은 스킬의 해석이므로 warning 수준으로 |
| A2 | 유지·강화 | 4C 정의의 핵심. 이것 없이는 "4C 스킬"이라 부르기 어려움 |
| A3 | 유지 | 10분(최대 20분)은 원문 수치 |
| A4 | 유지 | Interactive Lecture의 micro-activity 그대로 |
| A5 | 수정 | Warm-Up은 과정 전 1~2주, 슬라이드가 아님. Connect 태그는 fast-pass/start-up만. Warm-Up은 A13으로 분리 |
| A6 | 유지 | 3요소 감사는 ch13 원문 |
| A7 | 수정 | 4요소는 맞으나 4개 필수 필드는 과잉. 매 모듈 Conclusion마다 축하까지 넣으면 형식화됨. 과정 마지막 Conclusion에만 4요소 권고, 모듈 Conclusion은 요약+액션 2요소 |
| A8 | 유지 | Need-to-know 필터 원문 |
| A9 | 병합 | A2와 중복. `activity`가 있으면 learn, 없으면 hear로 간주하면 됨. 별도 태그 불필요 |
| A10 | 유지·조건 | 활동 절차를 책 원문 그대로 옮기면 저작권 문제. 활동명 + 자체 요약 1~2줄 + 출처 챕터만 기록 |
| A11 | 유지 | Start-Up은 "반드시 디브리프로 끝난다"(ch07). 노트 없이는 디브리프 질문이 사라짐 |
| A12 | 축소 | 컨셉맵은 학습자가 강의 중 직접 그리는 것. 스킬이 만들 수 있는 것은 빈 오거나이저 골격뿐. 핸드아웃 MD로 축소 |
| A13 | 유지 | ch05 |
| A14 | 병합 | 평가는 Conclusion의 evaluate 요소. 별도 슬라이드 타입은 과잉 → A7에 흡수 |
| A15 | 유지 | habituation은 ch02 핵심 |
| A16 | 수정 | "마지막 5분"은 과정 전체 기준. 20분 모듈에 5분 강제는 과잉. 모듈 Conclusion ≥ 2분 또는 ≥ 10%로 완화 |
| A17 | 유지·축소 | 태그는 유용하나 검증까지는 과잉. 카탈로그(A10)에서 Jigsaw를 Concept 활동으로만 분류하면 충분 |
| A18 | 유지·주의 | 2/3 규칙은 원문. 다만 시간 추정은 근사치임을 명시 |
| A19 | 병합 | A7 evaluate 요소로 흡수 |
| B~D | 이론 검증 대상 아님 | 2·3회차에서 검증 |
| Module Start 순서 | 문서화만 | Module Start가 20자 이내 분리자라면 Primacy를 해치지 않음. "아젠다·하우스키핑은 Connect 뒤"만 가이드에 명시 |

1회차 결과: A9, A14, A19 병합. A5, A7, A16 수정. 나머지 유지.

### 3.2 검증 2회차: 실현 가능성·비용 — "python-pptx와 마크다운 포맷으로 가능한가? 유지보수 부담은?"

| # | 판정 | 근거 |
|---|---|---|
| A1 | 유지 | 정규식 lint. 한국어 활용형 때문에 오탐 있음 → warning. 비용 낮음 |
| A2 | 유지 | 파서는 이미 임의 필드를 dict로 받음. 생성기에서 `activity`를 Connect/Concept/Conclusion에도 렌더링하도록 분기 추가. validate의 필수 필드 표만 바꾸면 됨. 비용 낮음 |
| A3 | 유지 | `time:` 파싱 후 비교. 비용 매우 낮음 |
| A4 | 유지·조건 | 새 슬라이드 타입은 Break와 같은 패턴으로 추가 가능. 템플릿에 `4C - Review` 레이아웃이 없으면 Concept 레이아웃 폴백. D1과 연결 |
| A6 | 수정 | 필드 2개 추가보다 체크리스트·프롬프트로 유도하는 편이 저렴. 스크립트 변경 없이 문서로 해결 |
| A7 | 유지(수정판) | `action_plan:` 필드 1개만 추가. 나머지는 `sub` 안에서 프롬프트로 유도 |
| A8 | 유지 | `handout:` 필드를 모아 `<output>_handout.md`로 쓰기. 30줄 내외 |
| A10 | 유지 | 참조 MD 1개. 스크립트 변경 없음. 단, SKILL.md에 통째로 넣으면 컨텍스트 폭증 → 별도 파일 + 필요 시 읽기 |
| A11 | 유지 | notes_slide 쓰기는 이미 구현됨. `notes:` 필드를 노트에 추가만 하면 됨 |
| A12 | 축소 유지 | MD 핸드아웃만. 별도 렌더링 없음 |
| A13 | 유지 | `## Warm-Up` 섹션 → 슬라이드 아님, 핸드아웃 MD로 출력. A8과 같은 경로 |
| A15 | 보류→Could | 활동 유형을 알아야 함. A10 카탈로그의 활동명 매칭이 전제. 후순위 |
| A16 | 유지 | 시간 비교 한 줄 |
| A18 | 보류→Could | 슬라이드 타입 + activity 유무로 근사. 정확도 낮음. 리포트(B2)에 참고값으로만 |
| B1 | 유지 | validate v2 리팩터. 규칙을 함수 목록으로 분리하면 확장 쉬움 |
| B2 | 유지 | 파서 재사용. 비용 낮음 |
| B3 | 축소 | 아젠다 슬라이드는 쉬움. run-sheet는 B2 리포트를 MD로 저장하면 사실상 동일 → B2에 병합 |
| B4 | 유지·주의 | python-pptx는 텍스트 크기 측정 불가. 글자수·줄수 휴리스틱만. 오탐 감수하고 warning |
| B5 | 유지 | 파서 상단에 `---` 블록 처리 추가. PyYAML 의존성 추가 대신 `key: value` 단순 파싱 |
| B6 | 유지·조건 | 스크립트 3+2개를 하나로 합치는 것이 본질. 기존 스크립트는 deprecated 래퍼로 1버전 유지 |
| B7 | 유지 | 예제 MD → 슬라이드 수·타입 순서·노트 태그 검증. 골든 PPTX 비교는 바이너리라 불안정 → 구조 비교만 |
| B8 | 제외 | 노트 태그로 가능은 하나 수요 불명. 이미지·비디오 경로 복원 불가 |
| B9 | 유지 | 문서 작업. 즉시 가능 |
| B10 | 보류→Could | A10이 있으면 AI가 프롬프트로 대신함. 별도 도구 불필요 |
| C1, C2, C5, C6 | 유지 | 문서·예제 작업. 비용 낮고 효과 큼 |
| C3 | 병합 | B5 프론트매터의 `audience:`로 충분 |
| C4 | 보류→Could | 프론트매터 `mode: online`이 있으면 프롬프트·카탈로그 필터로 대응. 생성기 변경은 Break→Body Break 문구 정도 |
| D1 | 유지·조건 | 기본 템플릿 pptx 편집 필요. 레이아웃 폴백이 있으니 없어도 동작 |
| D2 | 병합 | A2 `activity`를 어느 placeholder에 넣을지의 문제. 별도 placeholder는 템플릿 의존. Concept 레이아웃 body에 구분선 넣고 렌더 |
| D3 | 보류→Could | `--audience learner` 플래그로 notes·handout 제거 덱 생성. 가능하나 A8·A12 이후 |
| D4 | 제외→Won't | 템플릿 책임. 스킬이 검사하기엔 python-pptx 정보 부족 |
| D5 | 제외→Won't | 범위 밖 |

2회차 결과: B8, D4, D5 제외. A6, A12, B3, C3, D2 축소·병합. A15, A18, B10, C4, D3는 Could로 강등.

### 3.3 검증 3회차: 사용자 가치·사용성 — "강사가 실제로 쓰는가? 마찰이 늘지 않는가? 기존 파일이 깨지는가?"

| # | 판정 | 근거 |
|---|---|---|
| 필드 추가 전반 (A1, A2, A7, A8, A11, B5) | 조건부 유지 | **모두 선택 필드**. 없으면 warning, error 아님. 기존 v1.0 MD 파일은 그대로 빌드되어야 함. 이것이 깨지면 채택률 0 |
| A1 금지 동사 | 유지·완화 | 강사가 "이해한다"를 습관적으로 씀. error면 짜증. warning + 대체 동사 제안 메시지("→ 설명한다, 시연한다, 나열한다") |
| A2 activity 전 단계 | 유지 | 가장 가치 큼. 다만 "매 슬라이드 활동"은 현실적으로 무리. 프롬프트에서는 "Concept 10분당 Review 1개" 정도로 안내 |
| A3 10분 규칙 | 유지·완화 | 12분 Concept를 error로 막으면 반발. 10분 초과 warning, 20분 초과만 error. 메시지에 "Review 슬라이드를 사이에 넣으세요" 제안 |
| A4 Review 슬라이드 | 유지 | 강사가 활동을 잊지 않게 하는 물리적 장치. 슬라이드 하나가 노트보다 효과 큼 |
| A7 action_plan | 유지 | 과정 마지막에만 권고. 20분 모듈마다 액션플랜은 형식화 |
| A8 handout | 유지 | "슬라이드에 다 못 넣어서 빼는 내용"을 버리지 않고 모아준다는 점에서 강사 체감 가치 높음 |
| A10 카탈로그 | 유지 | 강사가 "무슨 활동을 넣지?"에서 막힘. 가장 자주 쓰일 참조 파일 |
| A11 강사 노트 | 유지 | 노트 없는 PPT는 다른 강사가 재사용 불가. 배포 가치 직결 |
| A13 Warm-Up | Could 유지 | 사전 과제를 쓰는 강사가 소수 |
| A16 Conclusion 최소 시간 | 유지 | 완화된 기준(≥2분)이면 마찰 없음 |
| B1 lint 분리 | 유지 | 형식 오류(빌드 실패)와 설계 경고(빌드는 됨)를 구분해야 사용자가 무시할 수 있음 |
| B2 시간 리포트 | 유지 | 강사가 가장 먼저 보는 숫자 |
| B4 넘침 경고 | 유지 | 오탐 있어도 "이 슬라이드 확인하세요"는 유용. PPT 열어 확인하는 시간 절약 |
| B6 CLI 통합 | 유지·주의 | 기존 명령을 문서에서 쓰는 사용자 있음. 1버전 동안 래퍼 유지 + deprecation 메시지 |
| B7 테스트 | Could | 사용자 가치보다 유지보수 가치. 스크립트 통합(B6) 시 회귀 방지용으로 필요 |
| B9 SKILL.md | 유지·최우선 | 지금 SKILL.md대로 따라 하면 메인 스크립트가 아닌 구 스크립트가 실행됨. 버그 수준 |
| C1 프롬프트 | 유지 | 사용자 대부분이 AI로 콘텐츠를 생성함. 프롬프트가 곧 품질 |
| C2 역방향 설계 | 유지·주의 | phased_prompt를 성과→Practice 순으로 바꾸되, 기존 순차 방식도 남김. 초보자는 순차가 편함 |
| C5 체크리스트 | 유지 | 이미 있는 문서에 항목 추가 |
| C6 예제 재작성 | 유지·최우선 | 사용자는 예제를 복사해서 시작함. 예제가 강사 중심이면 모든 산출물이 강사 중심 |
| D1 Review 레이아웃 | Should | 폴백이 있으니 없어도 됨. 있으면 시각적 구분이 명확 |
| D3 덱 분리 | Could | 학습자 배포용을 원하는 수요는 있으나 후순위 |

3회차 결과: 제외 없음. 전반에 "선택 필드·warning 우선·하위 호환" 원칙 부여. A13, B7, D3는 Could 확정.

### 3.4 검증 후 통합 목록 (28건)

| ID | 통합 아이디어 | 출처 |
|---|---|---|
| P01 | SKILL.md 정합성 수정: 메인 스크립트 단일 명시, 구 스크립트 안내 제거, 슬림화 | B9 |
| P02 | `outcome:` 필드(모듈·과정) + 금지 동사 warning + 대체 동사 제안 | A1 |
| P03 | `activity:` 필드를 Connect/Concept/Conclusion에도 허용, 렌더·검증 반영 | A2, A9, D2 |
| P04 | 10분 규칙 lint: Concept >10분 warning, >20분 error, Review 삽입 제안 | A3 |
| P05 | `## Review` 슬라이드 타입(1~2분 전원 리뷰) | A4 |
| P06 | 예제 파일 Bowman 준수 재작성(학습자 활동, 10분 chunk, 학습자 주도 Conclusion) | C6 |
| P07 | AI 프롬프트·phased_prompt에 Bowman 철칙 주입, 역방향 설계 순서 병기 | C1, C2 |
| P08 | 활동 카탈로그 `references/activities.md`(C별·시간·인원·모드·출처 챕터, 자체 요약) | A10, A17 |
| P09 | 시간 리포트(모듈별·총합·버퍼·강사/학습자 근사 비율) + run-sheet MD | B2, B3, A18 |
| P10 | `notes:` 필드 → 강사 노트(진행 스크립트·디브리프 질문·준비물) | A11 |
| P11 | `handout:` 필드 → `<output>_handout.md` 부록 생성 | A8, A12 |
| P12 | 프론트매터(과정명·대상·총시간·성과·mode) 단순 파싱 | B5, C3 |
| P13 | 텍스트 넘침 휴리스틱 warning | B4 |
| P14 | validate v3: 형식 lint / 설계 lint 분리, 심각도 | B1 |
| P15 | 단일 CLI + 레거시 래퍼 + deprecation | B6 |
| P16 | review_checklist에 철칙 10개·3요소·4요소 반영 | C5, A6, A7 |
| P17 | Conclusion `action_plan:` 필드(과정 마지막 권고) + 최소 시간 warning | A7, A14, A16, A19 |
| P18 | Connect `type: fast-pass \| start-up` 태그, 주제 관련성 체크 항목 | A5 |
| P19 | Module Start 뒤 아젠다·하우스키핑 배치 가이드(Primacy) | 진단 1.2 |
| P20 | `## Warm-Up` 섹션 → 사전 과제 핸드아웃 | A13 |
| P21 | 온라인 모드(`mode: online` → Body Break 문구, 카탈로그 필터) | C4 |
| P22 | 활동 다양성 검사(연속 동일 활동 warning) | A15 |
| P23 | 기본 템플릿에 `4C - Review` 레이아웃 추가 | D1 |
| P24 | 강사 덱 / 학습자 덱 분리 출력 플래그 | D3 |
| P25 | pytest 구조 테스트 | B7 |
| P26 | 아젠다 슬라이드 자동 생성(프론트매터 기반) | B3 |
| P27 | 강사 발화 비율 근사값을 리포트에 참고 표기 | A18 |
| P28 | 활동 추천은 카탈로그 + 프롬프트로 대체(별도 도구 없음) | B10 |
| P29 | 활동 패턴 참조: `pattern:` + `params:` + `alt:` 필드, 카탈로그에 교환 메타(stages/also_ok/swap_group/never_swap_with) | 사용자 요청(§7) |
| P30 | 교환 제어 규칙(단계 내 자유·교차 조건부·금지쌍) + `swap --list / --to` 명령, 교환 후 재검증·diff | 사용자 요청(§7) |
| P31 | 일괄 교환(`--mode online`, 시간 축소) + 교환 제안 트리거(습관화·인원·시간) | 사용자 요청(§7), A15 |

제외(Won't): B8 라운드트립, D4 접근성 검사, D5 디자인 자동화, Concept 자동 분할(A3 파생안), docx 핸드아웃(A12 파생안).

---

## 4. MoSCoW 분류

### Must — 이것 없이는 "4C 스킬"이 아니다

| ID | 항목 | 이유 | 변경 범위 |
|---|---|---|---|
| P01 | SKILL.md 정합성 수정 | 현재 안내대로 하면 구 스크립트 실행. 버그 | 문서 |
| P03 | `activity:` 전 단계 허용 | Bowman 4C의 정의 자체. 학습자 행동 없는 4C는 이름만 4C | 파서·생성기·validate |
| P02 | `outcome:` + 금지 동사 warning | "Begin with the end". 성과 없이는 need-to-know 판단 불가 | 파서·validate·프롬프트 |
| P04 | 10분 규칙 lint | 가장 명확한 수치 규칙. 예제가 현재 위반 중 | validate |
| P05 | `## Review` 슬라이드 | 10분 규칙을 지킬 물리적 수단. P04와 한 쌍 | 파서·생성기 |
| P06 | 예제 재작성 | 사용자는 예제를 복사한다. 예제가 기준 | 예제 |
| P07 | 프롬프트에 철칙 주입 | 콘텐츠 대부분이 AI 생성. 프롬프트가 품질 상한 | 문서 |

### Should — 강사 체감 가치가 크고 비용이 낮다

| ID | 항목 | 이유 |
|---|---|---|
| P08 | 활동 카탈로그 | "무슨 활동?"에서 막히는 지점 해소. 스크립트 변경 없음 |
| P09 | 시간 리포트 + run-sheet | 강사가 가장 먼저 확인하는 정보. 파서 재사용 |
| P10 | `notes:` 강사 노트 | 재사용·배포 가치. notes_slide 이미 구현 |
| P11 | `handout:` 부록 | Need-to-know 필터의 실물. 잘라낸 내용을 버리지 않음 |
| P12 | 프론트매터 | P02·P09·P21의 전제. 단순 파싱 |
| P14 | validate v3 lint 분리 | P02·P04·P13·P17을 담을 그릇 |
| P16 | 체크리스트 철칙 반영 | 문서 수정만으로 검토 품질 상승 |
| P17 | `action_plan:` + Conclusion 최소 시간 | 학습자 주도 마무리의 최소 장치 |
| P29 | 활동 패턴 참조 + 카탈로그 교환 메타 | 교환의 전제. P08 카탈로그와 동시 구현 |
| P30 | 교환 제어 규칙 + `swap` 명령 | 활동 교체 시 지시문·노트 자동 재생성. Bowman 금지쌍(Jigsaw↔Teach-Back) 강제 |

### Could — 있으면 좋고, 수요·여력 따라

| ID | 항목 | 비고 |
|---|---|---|
| P13 | 텍스트 넘침 휴리스틱 | 오탐 감수 |
| P15 | 단일 CLI + 레거시 정리 | 가치 크나 하위 호환 작업량 큼. Should 승격 검토 가능 |
| P18 | Connect type 태그 | 카탈로그로 대체 가능 |
| P19 | Primacy 배치 가이드 | 문서 한 단락 |
| P20 | Warm-Up 섹션 | 사전 과제 사용 강사 소수 |
| P21 | 온라인 모드 | 프론트매터 이후 |
| P22 | 활동 다양성 검사 | P08 활동명 매칭 전제 |
| P23 | Review 레이아웃 템플릿 | 폴백 있음 |
| P24 | 덱 분리 출력 | P10·P11 이후 |
| P25 | pytest | P15 착수 시 함께 |
| P26 | 아젠다 슬라이드 | P12 이후 |
| P31 | 일괄 교환 + 교환 제안 트리거 | P30 이후. P22 습관화 검사와 통합 |

### Won't (이번 주기)

| 항목 | 이유 |
|---|---|
| Concept 자동 분할 | 내용 의미를 모르는 스크립트가 자르면 품질 저하. warning + Review 제안으로 충분 |
| PPTX → MD 라운드트립 | 수요 불명, 이미지·비디오 복원 불가 |
| docx 핸드아웃 | 의존성 추가. MD로 충분 |
| 접근성 검사 | 템플릿 책임. python-pptx 정보 부족 |
| 디자인·이미지 자동화 | 범위 밖 |
| 별도 Kirkpatrick 평가 모듈 | Conclusion evaluate 요소로 흡수 |

---

## 5. 릴리스 단계 제안

### v1.1 — 이론 정렬 (Must 7건)

순서: P01 → P12(프론트매터, P02 전제) → P02 → P03 → P04 → P05 → P06 → P07

하위 호환 원칙:
- 새 필드는 모두 선택. 없으면 warning.
- v1.0 예제 MD가 그대로 빌드되어야 함.
- 형식 error는 빌드 실패, 설계 warning은 빌드 진행.

### v1.2 — 강사 도구 (Should 8건)

P14 → P08 → P09 → P10 → P11 → P16 → P17

### v1.3 — 정리·확장 (Could 선별)

P15 + P25(함께), P13, P21, P23

---

## 6. 핵심 설계 결정 (구현 전 확정 필요)

1. **`activity:` 렌더 위치**: Concept 슬라이드 본문 하단 구분선 아래 vs 별도 placeholder. 권고: 하단 구분선. 템플릿 의존 없음.
2. **금지 동사 목록**: 알다·이해하다·배우다·숙지하다·인식하다·파악하다. 활용형 정규식. 오탐은 warning으로 흡수.
3. **10분 기준값**: warning 10분, error 20분. 프론트매터 `strict: true`일 때만 warning을 error로 승격.
4. **Review 슬라이드 필드**: `time`(기본 2분), `title`, `activity`. `main/sub` 없음.
5. **핸드아웃 파일명**: `<output 이름>_handout.md`. 출력 디렉터리 동일.
6. **레거시 스크립트**: v1.1에서는 건드리지 않음. v1.3에서 래퍼화.

---

## 7. 활동 교환 제어 (P29~P31 상세)

### 7.1 문제

활동이 `activity:` 자유 텍스트라서 "Connect의 활동 A를 B로 바꾼다"는 작업이 지시문 전체 재작성이다. 교환을 기계적으로 지원하려면 활동을 **패턴(카탈로그 ID) + 파라미터**로 참조해야 한다.

### 7.2 문법 (P29)

```markdown
## Connect
time: 5분
title: 첫 명령의 기억
pattern: standing-survey          # 카탈로그 ID
params:
  question: 기계에 명령해 본 경험은?
  debrief: 3명 발표
alt: turn-and-talk, wall-writing  # 미리 정한 플랜 B (교환 후보 우선순위)
activity: |                       # 선택. 있으면 이것을 우선, 없으면 패턴 템플릿으로 생성
```

- `pattern` 없음 → v1.0과 동일하게 `activity` 자유 텍스트. 하위 호환.
- `pattern` 있음 + `activity` 없음 → 카탈로그의 지시문 템플릿에 `params`를 채워 슬라이드 활동 블록과 강사 노트를 생성.

### 7.3 카탈로그 교환 메타 (P29)

```yaml
- id: standing-survey
  name: Standing Survey
  stages: [connect]            # 본래 단계
  also_ok: [review]            # 교차 사용 허용
  swap_group: social-share     # 같은 그룹 내 자유 교환
  time: 3-7
  group: whole
  mode: [offline]
  needs: [이동 공간]
  never_swap_with: []
  template: |
    일어서서 3명에게 "{question}"을 묻고 답을 기록한다.
    디브리프: {debrief}
- id: jigsaw
  stages: [concept]
  never_swap_with: [teach-back]   # 새 내용 ↔ 이미 배운 내용. Bowman 철칙
```

### 7.4 교환 규칙 (P30)

| 교환 유형 | 처리 |
|---|---|
| 같은 단계, 같은 swap_group | 자유 교환. 시간·모드·인원만 재검증 |
| 같은 단계, 다른 swap_group | 허용. warning으로 목적 차이 표시(개인 성찰형 ↔ 사회형 등) |
| 다른 단계 | 대상 패턴의 `also_ok`에 현재 단계가 있을 때만 허용. 아니면 error |
| `never_swap_with` 쌍 | 항상 error |
| 시간 초과 | 대상 패턴 최소 시간 > 슬롯 시간이면 warning + 슬롯 시간 조정 제안 |
| 모드 불일치 | 프론트매터 `mode`와 패턴 `mode`가 맞지 않으면 error, 같은 그룹의 대체 패턴 제안 |

### 7.5 명령 (P30, P31)

```bash
# 교환 후보와 사유 조회
python scripts/4c.py swap --md course.md --at "모듈1/Connect#1" --list
#   ✓ turn-and-talk   (alt, 같은 그룹, 2분 → 슬롯 5분 여유 3분)
#   ✓ wall-writing    (alt, 같은 그룹)
#   △ learning-log    (다른 그룹: 개인 성찰형. Connect 목적과 차이 있음)
#   ✗ jigsaw          (Concept 전용, also_ok에 connect 없음)

# 교환 실행 → diff + 시간 리포트 재출력
python scripts/4c.py swap --md course.md --at "모듈1/Connect#1" --to turn-and-talk

# 일괄 교환 (P31)
python scripts/4c.py swap --md course.md --mode online      # offline 전용 → online 대체
python scripts/4c.py swap --md course.md --fit 90분          # 총시간 맞추기: 긴 활동 → 짧은 대체
```

### 7.6 교환 제안 트리거 (P31)

validate가 다음 조건에서 교환 후보를 제안한다.
- 프론트매터 `mode` 변경으로 모드 불일치 발생
- 총시간 초과
- 같은 패턴 3회 연속(습관화, P22와 통합)
- 프론트매터 `group_size`가 패턴 `group` 범위 밖

### 7.7 검증 메모

- 이론: Bowman은 "설계는 순서 없이, 전달은 순서대로"라 했고 활동 교체 자체를 막지 않는다. 다만 Jigsaw↔Teach-Back 금지와 Connect≠아이스브레이커 원칙이 있어, 교차 교환은 화이트리스트(`also_ok`)로 제어하는 편이 맞다.
- 실현: 파서에 `pattern/params/alt` 3필드, 카탈로그 YAML 로더(표준 라이브러리로 단순 파싱 가능한 형태 유지), swap 서브커맨드. P08·P15 CLI 통합과 함께 구현하면 중복이 없다.
- 사용성: `pattern` 없이도 동작하므로 마찰 없음. `--list`가 "왜 안 되는지"를 보여줘야 사용자가 규칙을 배운다.

---

## 부록: Bowman 철칙 ↔ 스킬 장치 매핑 (v1.2 완료 시점)

| 철칙 | 장치 |
|---|---|
| Whoever explains, learns | `activity:` 전 단계, 프롬프트 강제 |
| 10분 규칙 | P04 lint + P05 Review |
| 성과 = 관찰 동사 + 개념 | P02 |
| Primacy-Recency | P19 가이드 + P17 최소 시간 |
| 슬라이드 복사본 배포 금지 | P11 핸드아웃 |
| 전원 참여 실습 | P16 3요소 체크 + 프롬프트 |
| Need-to-know 필터 | P11 `handout:` |
| 마지막 5분은 학습자 | P17 `action_plan:` |
| 학습을 평가, 강사를 평가하지 않음 | P16 체크 + 프롬프트 |
| 방법을 고치지 대상을 탓하지 않음 | 프롬프트 원칙 문구 |
