#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4C Markdown 검증 v3 — 형식 lint + 교수설계 lint + 시간 리포트

사용법:
    python validate_markdown_v3.py --md course.md
    python validate_markdown_v3.py --md course.md --report run_sheet.md
    python validate_markdown_v3.py --md course.md --strict          # warning도 실패
    python validate_markdown_v3.py --md course.md --format-only
    python validate_markdown_v3.py --md course.md --design-only

종료 코드: error가 있으면 1. --strict(또는 프론트매터 strict: true)면 warning도 1.

규칙 (F=형식, D=설계)
  F01 한 줄에 필드 2개 이상            error
  F02 알 수 없는 슬라이드 타입          error
  F03 time 형식 (숫자+분)              error
  F04 4C 필수 필드(time/title/main)     warning
  F05 Practice에 activity/sub/pattern 없음  warning
  F06 pattern ID가 카탈로그에 없음       error
  F07 pattern이 이 단계에서 허용 안 됨   error
  F08 pattern 모드가 과정 mode와 불일치  error
  F09 pattern params 누락               warning
  F10 pattern 시간 범위 밖              warning/info
  D01 모듈 outcome 없음                 warning
  D02 outcome에 관찰 불가 동사           warning
  D03 Concept 10분 초과 / 20분 초과      warning / error
  D04 연속 강의(활동 없는 Concept 누적) 10분 초과  warning
  D05 Concept에 학습자 활동 없음         info
  D06 Connect에 학습자 활동 없음         warning
  D07 Conclusion에 학습자 활동 없음      warning
  D08 Conclusion 2분 미만               warning
  D09 과정 마지막 Conclusion에 action_plan 없음  warning
  D10 총 시간이 프론트매터 total_time과 15% 이상 차이  warning
  D11 같은 pattern 3회 연속 (습관화)     warning
  D12 Module Start 본문 20자 초과        info
  D13 슬라이드 본문(main+sub+활동) 400자 초과 — 넘침 가능  info
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md4c import (parse_course, load_catalog, parse_minutes, safe_print,  # noqa: E402
                  pattern_allowed_in, missing_params, render_activity,
                  FOUR_C, LEARNER_SLIDES, KNOWN_SLIDE_TYPES, ALL_FIELDS)

FIELD_RE = re.compile(r'(?:^|\s)(' + '|'.join(sorted(ALL_FIELDS)) + r'):')

FORBIDDEN_VERBS = [
    (re.compile(r'이해(한다|할|하|를|가|도)'), '이해하다'),
    (re.compile(r'(알게\s*된다|알게\s*됨|안다|알\s*수\s*있|알아본다|알아보)'), '알다'),
    (re.compile(r'배(운다|울|우게|움|우)'), '배우다'),
    (re.compile(r'숙지'), '숙지하다'),
    (re.compile(r'인식(한다|할|하)'), '인식하다'),
    (re.compile(r'파악(한다|할|하)'), '파악하다'),
    (re.compile(r'\b(know|understand|learn)s?\b', re.I), 'know/understand/learn'),
]
SUGGEST_VERBS = '설명한다 / 작성한다 / 시연한다 / 나열한다 / 구분한다 / 적용한다 / 남에게 가르친다'


class Issue:
    def __init__(self, level, rule, line, section, message):
        self.level = level      # error | warning | info
        self.rule = rule
        self.line = line
        self.section = section
        self.message = message


class Lint:
    def __init__(self):
        self.issues = []

    def add(self, level, rule, line, section, message):
        self.issues.append(Issue(level, rule, line, section, message))

    def error(self, *a):
        self.add('error', *a)

    def warning(self, *a):
        self.add('warning', *a)

    def info(self, *a):
        self.add('info', *a)

    def count(self, level):
        return sum(1 for i in self.issues if i.level == level)


# ------------------------------------------------------------- 형식 규칙

def format_rules(md_path, course, catalog, lint):
    with open(md_path, 'r', encoding='utf-8') as f:
        raw = f.read().split('\n')

    # F01: 한 줄 다중 필드 (슬라이드 영역 내 비들여쓰기 줄)
    in_slide = False
    for i, line in enumerate(raw, 1):
        if line.startswith('## '):
            in_slide = True
            continue
        if line.startswith('# '):
            in_slide = False
            continue
        if in_slide and not line.startswith((' ', '\t', '-')):
            n = len(FIELD_RE.findall(line))
            if n > 1:
                lint.error('F01', i, '', f"한 줄에 {n}개의 필드가 합쳐져 있습니다: {line.strip()[:60]}")

    for module in course.modules:
        for s in module.slides:
            st = s.slide_type
            sec = f'{module.title} / {st}'

            # F02
            if st not in KNOWN_SLIDE_TYPES:
                lint.error('F02', s.line_no, sec, f"알 수 없는 슬라이드 타입 '{st}'. 허용: {', '.join(KNOWN_SLIDE_TYPES)}")
                continue

            if st in LEARNER_SLIDES or st == 'Break':
                t = s.get('time')
                if t and parse_minutes(t) is None:
                    lint.error('F03', s.line_no, sec, f"time 형식 오류 '{t}'. 예: 5분")

            if st in FOUR_C:
                for f in ('time', 'title', 'main'):
                    if not s.get(f):
                        lint.warning('F04', s.line_no, sec, f"필드 '{f}:' 가 없습니다")
                if st == 'Concrete Practice' and not (s.get('activity') or s.get('sub') or s.get('pattern')):
                    lint.warning('F05', s.line_no, sec, "실습 내용(activity: 또는 pattern:)이 없습니다")

            if st == 'Review':
                if not (s.get('activity') or s.get('pattern')):
                    lint.warning('F05', s.line_no, sec, "Review에 activity: 또는 pattern: 이 없습니다")

            # pattern 검사
            pid = s.get('pattern')
            if pid:
                if not catalog:
                    lint.warning('F06', s.line_no, sec, "카탈로그를 찾지 못해 pattern을 검증할 수 없습니다 (--catalog)")
                elif pid not in catalog:
                    lint.error('F06', s.line_no, sec, f"pattern '{pid}' 가 카탈로그에 없습니다")
                else:
                    entry = catalog[pid]
                    stage = s.stage
                    allowed = pattern_allowed_in(entry, stage) if stage else None
                    if stage and allowed is None:
                        lint.error('F07', s.line_no, sec,
                                   f"pattern '{pid}' 는 {stage} 단계에서 허용되지 않습니다 (허용: {', '.join(entry.get('stages', []) + entry.get('also_ok', []))})")
                    mode = course.mode
                    if mode in ('online', 'offline') and mode not in entry.get('mode', []):
                        lint.error('F08', s.line_no, sec,
                                   f"pattern '{pid}' 는 {mode} 모드를 지원하지 않습니다 (지원: {'/'.join(entry.get('mode', []))}). swap_activity.py --mode {mode} 로 대체하세요")
                    mp = missing_params(entry, s.get('params') or {})
                    if mp:
                        lint.warning('F09', s.line_no, sec, f"pattern '{pid}' params 누락: {', '.join(mp)}")
                    mins = s.minutes
                    tr = entry.get('time')
                    if mins is not None and tr:
                        if mins < tr[0]:
                            lint.warning('F10', s.line_no, sec, f"슬롯 {mins}분 < pattern 최소 {tr[0]}분")
                        elif mins > tr[1]:
                            lint.info('F10', s.line_no, sec, f"슬롯 {mins}분 > pattern 권장 최대 {tr[1]}분")


# ------------------------------------------------------------- 설계 규칙

def check_outcome(text, line, sec, lint, label):
    hits = []
    for rx, name in FORBIDDEN_VERBS:
        if rx.search(text):
            hits.append(name)
    if hits:
        lint.warning('D02', line, sec, f"{label} outcome에 관찰 불가 동사({', '.join(hits)}): \"{text[:40]}\" → 대체: {SUGGEST_VERBS}")


def design_rules(course, catalog, lint):
    fm = course.frontmatter
    if fm.get('outcome'):
        check_outcome(fm['outcome'], 1, '프론트매터', lint, '과정')
    elif fm:
        lint.info('D01', 1, '프론트매터', "과정 outcome: 이 없습니다")

    last_conclusion = None
    prev_patterns = []

    for module in course.modules:
        if not module.slides:
            continue
        sec_m = module.title

        # D01, D02
        if not module.outcome:
            lint.warning('D01', module.line_no, sec_m, "모듈 outcome: 이 없습니다 (관찰 가능한 동사 + 개념)")
        else:
            check_outcome(module.outcome, module.line_no, sec_m, lint, '모듈')

        lecture_run = 0
        lecture_start = None

        for s in module.slides:
            st = s.slide_type
            sec = f'{module.title} / {st}'
            mins = s.minutes or 0

            if st == 'Module Start':
                c = s.get('content', '')
                if len(c.replace('\n', '')) > 20:
                    lint.info('D12', s.line_no, sec, f"Module Start 본문이 {len(c)}자. 20자 이내 권장")
                continue

            if st not in LEARNER_SLIDES:
                if st == 'Break':
                    lecture_run, lecture_start = 0, None
                continue

            has_action = s.has_learner_action

            # D13 넘침 휴리스틱
            body_len = len(s.get('main', '')) + len(s.get('sub', '')) + len(render_activity(s, catalog)) + len(s.get('action_plan', ''))
            if body_len > 400:
                lint.info('D13', s.line_no, sec, f"본문 {body_len}자. 슬라이드에서 넘칠 수 있습니다. sub/activity 를 줄이거나 handout: 으로")

            # D03
            if st == 'Concept':
                if mins > 20:
                    lint.error('D03', s.line_no, sec, f"Concept {mins}분. 20분을 넘는 직접 강의는 금지. 분할하고 사이에 ## Review 를 넣으세요")
                elif mins > 10:
                    lint.warning('D03', s.line_no, sec, f"Concept {mins}분. 10분 규칙 초과. 분할하거나 activity:/## Review 를 추가하세요")

            # D04 연속 강의
            if st == 'Concept' and not has_action:
                if lecture_start is None:
                    lecture_start = s.line_no
                lecture_run += mins
                if lecture_run > 10 and lecture_run - mins <= 10:
                    lint.warning('D04', s.line_no, sec,
                                 f"활동 없는 Concept 연속 {lecture_run}분 (L{lecture_start}~). 사이에 ## Review(1~2분) 또는 activity: 를 넣으세요")
            else:
                lecture_run, lecture_start = 0, None

            # D05~D07
            if st == 'Concept' and not has_action:
                lint.info('D05', s.line_no, sec, "학습자 활동 없음(듣기만). 학습(learn)이 목적이면 activity:/pattern: 추가")
            if st == 'Connect' and not has_action:
                lint.warning('D06', s.line_no, sec, "Connect에 학습자 활동이 없습니다. 질문만 던지지 말고 학습자가 말하거나 쓰게 하세요 (예: pattern: turn-and-talk)")
            if st == 'Conclusion':
                if not has_action and not s.get('action_plan'):
                    lint.warning('D07', s.line_no, sec, "Conclusion을 강사가 요약하고 있습니다. 학습자가 요약하게 하세요 (예: pattern: learning-log)")
                if mins and mins < 2:
                    lint.warning('D08', s.line_no, sec, f"Conclusion {mins}분. 최소 2분 권장")
                last_conclusion = (s, sec)

            # D11 습관화
            pid = s.get('pattern')
            if pid:
                prev_patterns.append((pid, s.line_no, sec))
                if len(prev_patterns) >= 3 and len({p for p, _, _ in prev_patterns[-3:]}) == 1:
                    lint.warning('D11', s.line_no, sec, f"pattern '{pid}' 3회 연속. 형식을 바꾸세요 (습관화 방지)")
            else:
                prev_patterns.append((None, s.line_no, sec))

    # D09
    if last_conclusion:
        s, sec = last_conclusion
        pid = s.get('pattern')
        is_commit = pid and catalog.get(pid, {}).get('swap_group') == 'commitment'
        if not s.get('action_plan') and not is_commit:
            lint.warning('D09', s.line_no, sec, "과정 마지막 Conclusion에 action_plan: 이 없습니다 (마지막 5분은 학습자의 실행 계획)")

    # D10
    total_decl = parse_minutes(fm.get('total_time'))
    if total_decl:
        total = sum(mins for _, mins, _ in iter_minutes(course))
        if abs(total - total_decl) > total_decl * 0.15:
            lint.warning('D10', 1, '프론트매터', f"슬라이드 시간 합계 {total}분 vs total_time {total_decl}분 (15% 이상 차이)")


# ------------------------------------------------------------- 시간 리포트

def iter_minutes(course):
    """(slide, minutes, module) — Break 포함"""
    for m in course.modules:
        for s in m.slides:
            if s.slide_type in LEARNER_SLIDES or s.slide_type == 'Break':
                yield s, (s.minutes or 0), m


def split_minutes(s):
    """
    (trainer, learner, break) 근사 배분.
    Concept 활동 없음 → 강사 100%. Concept 활동 있음 → 강사 70% / 학습자 30% (상호작용 강의).
    나머지 학습자 슬라이드 → 학습자 100%.
    """
    mins = s.minutes or 0
    if s.slide_type == 'Break':
        return 0, 0, mins
    if s.slide_type == 'Concept':
        if not s.has_learner_action:
            return mins, 0, 0
        t = int(round(mins * 0.7))
        return t, mins - t, 0
    return 0, mins, 0


def time_report(course, catalog):
    lines = []
    grand = {'trainer': 0, 'learner': 0, 'break': 0}
    for m in course.modules:
        if not m.slides:
            continue
        mt = {'trainer': 0, 'learner': 0, 'break': 0}
        parts = []
        for s in m.slides:
            if s.slide_type not in LEARNER_SLIDES and s.slide_type != 'Break':
                continue
            mins = s.minutes or 0
            t, l, b = split_minutes(s)
            mt['trainer'] += t
            mt['learner'] += l
            mt['break'] += b
            if s.slide_type == 'Break' and not mins:
                continue
            short = {'Connect': 'Connect', 'Concept': 'Concept', 'Review': 'Review',
                     'Concrete Practice': 'Practice', 'Conclusion': 'Conclusion', 'Break': 'Break'}[s.slide_type]
            parts.append(f'{short} {mins}')
        total = mt['trainer'] + mt['learner']
        lines.append(f"{m.title} ({total}분" + (f" + Break {mt['break']}" if mt['break'] else '') + ')')
        lines.append('    ' + ' | '.join(parts))
        if total:
            lines.append(f"    강사 발화(근사) {mt['trainer']}분 {mt['trainer'] * 100 // total}% / 학습자 활동 {mt['learner']}분 {mt['learner'] * 100 // total}%")
        for k in grand:
            grand[k] += mt[k]
    total = grand['trainer'] + grand['learner']
    lines.append('')
    lines.append(f"총 {total}분 + Break {grand['break']}분 = {total + grand['break']}분")
    if total:
        lines.append(f"강사 발화(근사) {grand['trainer'] * 100 // total}% / 학습자 활동 {grand['learner'] * 100 // total}%  (목표: 학습자 2/3 이상. 활동 있는 Concept는 강사 70%로 계산)")
    decl = parse_minutes(course.frontmatter.get('total_time'))
    if decl:
        buf = decl - total - grand['break']
        lines.append(f"total_time {decl}분 → 버퍼 {buf}분 ({buf * 100 // decl if decl else 0}%, 권장 10~15%)")
    return lines


def run_sheet(course, catalog):
    """강사용 진행표 MD"""
    out = [f"# {course.title or '교육 과정'} — 진행표", '']
    fm = course.frontmatter
    for k in ('audience', 'total_time', 'outcome', 'mode'):
        if fm.get(k):
            out.append(f"- {k}: {fm[k]}")
    out.append('')
    clock = 0
    for m in course.modules:
        if not m.slides:
            continue
        out.append(f'## {m.title}')
        if m.outcome:
            out.append(f'성과: {m.outcome}')
        out.append('')
        out.append('| 시각 | 분 | 단계 | 제목 | 활동(pattern) | 강사 노트 |')
        out.append('|---|---|---|---|---|---|')
        for s in m.slides:
            if s.slide_type not in LEARNER_SLIDES and s.slide_type != 'Break':
                continue
            mins = s.minutes or 0
            pid = s.get('pattern') or ''
            act = s.get('activity', '').split('\n')[0] if s.get('activity') else (catalog.get(pid, {}).get('name_ko', '') if pid else '')
            note = s.get('notes', '').split('\n')[0] if s.get('notes') else ''
            out.append(f"| {clock // 60:02d}:{clock % 60:02d} | {mins} | {s.slide_type} | {s.get('title', '')} | {act} {('`' + pid + '`') if pid else ''} | {note} |")
            clock += mins
        out.append('')
    out.append('')
    out.extend(['```'] + time_report(course, catalog) + ['```'])
    return '\n'.join(out)


# ------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description='4C Markdown 검증 v3 (형식 + 설계 + 시간)')
    ap.add_argument('--md', required=True)
    ap.add_argument('--catalog', default=None)
    ap.add_argument('--report', default=None, help='진행표 MD 저장 경로')
    ap.add_argument('--strict', action='store_true', help='warning도 실패로 처리')
    ap.add_argument('--format-only', action='store_true')
    ap.add_argument('--design-only', action='store_true')
    ap.add_argument('--quiet-info', action='store_true', help='info 숨김')
    args = ap.parse_args()

    if not Path(args.md).exists():
        safe_print(f"[ERROR] 파일을 찾을 수 없습니다: {args.md}")
        sys.exit(1)

    course = parse_course(args.md)
    catalog = load_catalog(args.catalog)
    lint = Lint()

    if not args.design_only:
        format_rules(args.md, course, catalog, lint)
    if not args.format_only:
        design_rules(course, catalog, lint)

    safe_print(f"[INFO] 검증: {args.md}  (모듈 {len([m for m in course.modules if m.slides])}, 모드 {course.mode})")
    safe_print('=' * 64)
    order = {'error': 0, 'warning': 1, 'info': 2}
    for lv in ('error', 'warning', 'info'):
        items = [i for i in lint.issues if i.level == lv]
        if not items or (lv == 'info' and args.quiet_info):
            continue
        safe_print(f"\n[{lv.upper()}] {len(items)}건")
        for i in sorted(items, key=lambda x: x.line):
            where = f"L{i.line}" + (f" {i.section}" if i.section else '')
            safe_print(f"  {i.rule} {where}\n      {i.message}")

    safe_print('\n' + '-' * 64)
    safe_print('[시간 리포트]')
    for l in time_report(course, catalog):
        safe_print('  ' + l)
    safe_print('=' * 64)

    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            f.write(run_sheet(course, catalog))
        safe_print(f"[OK] 진행표 저장: {args.report}")

    errors = lint.count('error')
    warnings = lint.count('warning')
    strict = args.strict or course.strict
    if errors:
        safe_print(f"[FAIL] error {errors}, warning {warnings}")
        sys.exit(1)
    if strict and warnings:
        safe_print(f"[FAIL] strict 모드: warning {warnings}")
        sys.exit(1)
    safe_print(f"[PASS] error 0, warning {warnings}, info {lint.count('info')}")
    sys.exit(0)


if __name__ == '__main__':
    main()
