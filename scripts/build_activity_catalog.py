#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
references/activities.json → references/activities.md (사람용 표) 생성

사용법:
    python scripts/build_activity_catalog.py
    python scripts/build_activity_catalog.py --json references/activities.json --out references/activities.md
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md4c import safe_print  # noqa: E402

STAGE_TITLE = {
    'connect': 'Connect (연결) — 학습자가 주제·동료·목표와 연결한다',
    'concept': 'Concept (개념) — 학습자가 need-to-know 정보를 듣고·보고·쓰고·말한다',
    'review': 'Review (리뷰) — 10분 강의 사이에 끼우는 1~3분 전원 참여 활동',
    'practice': 'Concrete Practice (실습) — 전원이 직접 한다. 보는 것은 실습이 아니다',
    'conclusion': 'Conclusion (정리) — 학습자가 요약·평가·실행 계획·축하한다',
}

GROUP_KO = {'individual': '개인', 'pair': '짝', 'small': '소그룹', 'whole': '전체'}


def build(json_path, out_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    acts = data['activities']
    meta = data.get('_meta', {})

    lines = []
    lines.append('# 4C 활동 카탈로그')
    lines.append('')
    lines.append(f"> 자동 생성 파일. 원본은 `activities.json` (v{meta.get('version', '?')}). 수정은 JSON에 하고 `python scripts/build_activity_catalog.py`로 재생성.")
    lines.append('> 활동 이름은 Bowman, *Training From the Back of the Room!* 기준. 설명은 자체 요약이며 책 본문을 옮기지 않았다.')
    lines.append('')
    lines.append('## 사용법')
    lines.append('')
    lines.append('```markdown')
    lines.append('## Connect')
    lines.append('time: 5분')
    lines.append('title: 첫 명령의 기억')
    lines.append('main: 기계에 명령해 본 경험')
    lines.append('pattern: standing-survey')
    lines.append('params:')
    lines.append('  question: 기계에 명령해 본 경험은?')
    lines.append('  debrief: 3명 발표')
    lines.append('alt: turn-and-talk, wall-writing')
    lines.append('```')
    lines.append('')
    lines.append('- `pattern:` 만 쓰면 아래 템플릿에 `params`를 채워 슬라이드 활동 블록과 강사 노트가 생성된다.')
    lines.append('- `activity:` 를 직접 쓰면 그것이 우선한다.')
    lines.append('- 교환: `python scripts/swap_activity.py --md course.md --at "모듈1/Connect#1" --list`')
    lines.append('')
    lines.append('## 교환 규칙')
    lines.append('')
    lines.append('| 상황 | 처리 |')
    lines.append('|---|---|')
    for k, v in meta.get('swap_rules', {}).items():
        lines.append(f'| {k} | {v} |')
    lines.append('')

    for stage in meta.get('stages', ['connect', 'concept', 'review', 'practice', 'conclusion']):
        lines.append(f'## {STAGE_TITLE.get(stage, stage)}')
        lines.append('')
        lines.append('| ID | 이름 | 시간(분) | 인원 | 모드 | 교환 그룹 | 다른 단계 허용 | 요약 | 출처 |')
        lines.append('|---|---|---|---|---|---|---|---|---|')
        for a in acts:
            if stage not in a['stages']:
                continue
            t = a.get('time', [0, 0])
            mode = '/'.join(a.get('mode', []))
            also = ', '.join(a.get('also_ok', [])) or '-'
            never = a.get('never_swap_with')
            summary = a['summary'].replace('|', '\\|')
            if never:
                summary += f" **교환 금지: {', '.join(never)}**"
            lines.append(f"| `{a['id']}` | {a['name_ko']} ({a['name']}) | {t[0]}~{t[1]} | {GROUP_KO.get(a['group'], a['group'])} | {mode} | {a['swap_group']} | {also} | {summary} | {a['source']} |")
        lines.append('')

    lines.append('## 템플릿과 파라미터')
    lines.append('')
    for a in acts:
        lines.append(f"### `{a['id']}` — {a['name_ko']}")
        lines.append('')
        params = a.get('params') or {}
        if params:
            lines.append('파라미터:')
            for k, v in params.items():
                lines.append(f'- `{k}`: {v}')
        else:
            lines.append('파라미터: 없음')
        if a.get('needs'):
            lines.append(f"준비물: {', '.join(a['needs'])}")
        lines.append('')
        lines.append('```')
        lines.append(a.get('template', ''))
        lines.append('```')
        lines.append('')

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    safe_print(f'[OK] {out_path} ({len(acts)} activities)')


def main():
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description='활동 카탈로그 MD 생성')
    ap.add_argument('--json', default=str(root / 'references' / 'activities.json'))
    ap.add_argument('--out', default=str(root / 'references' / 'activities.md'))
    args = ap.parse_args()
    build(Path(args.json), Path(args.out))


if __name__ == '__main__':
    main()
