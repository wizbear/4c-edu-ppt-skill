#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
활동 교환 (swap) — 슬라이드의 pattern: 을 카탈로그의 다른 활동으로 바꾼다

사용법:
    # 교환 후보와 허용/불허 사유
    python swap_activity.py --md course.md --at "모듈1/Connect#1" --list

    # 교환 실행 (파일 수정, diff 출력)
    python swap_activity.py --md course.md --at "모듈1/Connect#1" --to turn-and-talk
    python swap_activity.py --md course.md --at "모듈1/Connect#1" --to turn-and-talk --dry-run

    # 일괄: 모드 전환 (offline 전용 활동을 online 가능 활동으로)
    python swap_activity.py --md course.md --mode online

--at 형식:  "<모듈>/<단계>[#n]"
    모듈: 번호(1, 모듈1, 모듈 1) 또는 제목 일부
    단계: Connect | Concept | Review | Practice | Conclusion
    #n  : 그 단계의 n번째 슬라이드 (기본 1)

교환 규칙 (references/activities.json _meta.swap_rules):
    같은 단계 + 같은 swap_group  → ✓ 자유
    같은 단계 + 다른 swap_group  → △ 허용, 목적 차이 경고
    다른 단계                     → 대상의 also_ok 에 있을 때만 ✓/△, 아니면 ✗
    never_swap_with               → ✗
    모드 불일치                   → ✗
    시간 범위 밖                  → 경고
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md4c import (parse_course, load_catalog, safe_print, pattern_allowed_in,  # noqa: E402
                  missing_params, LEARNER_SLIDES)

STAGE_ALIAS = {
    'connect': 'Connect', 'concept': 'Concept', 'review': 'Review',
    'practice': 'Concrete Practice', 'concrete practice': 'Concrete Practice',
    'concrete': 'Concrete Practice', 'conclusion': 'Conclusion',
}


# ------------------------------------------------------------- locate

def locate(course, at):
    """'모듈1/Connect#2' → (module, slide)"""
    if '/' not in at:
        raise ValueError("--at 형식: '<모듈>/<단계>[#n]' 예: 모듈1/Connect#1")
    mod_part, slide_part = at.split('/', 1)
    mod_part = mod_part.strip()
    slide_part = slide_part.strip()

    modules = [m for m in course.modules if m.slides]
    module = None
    mnum = re.search(r'(\d+)', mod_part)
    if mnum and (mod_part.replace(' ', '').startswith(('모듈', 'module', 'Module')) or mod_part.isdigit()):
        idx = int(mnum.group(1)) - 1
        if 0 <= idx < len(modules):
            module = modules[idx]
    if module is None:
        for m in modules:
            if mod_part.lower() in m.title.lower():
                module = m
                break
    if module is None:
        raise ValueError(f"모듈을 찾을 수 없습니다: '{mod_part}'. 모듈 수 {len(modules)}")

    n = 1
    m2 = re.match(r'(.+?)#(\d+)$', slide_part)
    if m2:
        slide_part, n = m2.group(1).strip(), int(m2.group(2))
    stype = STAGE_ALIAS.get(slide_part.lower())
    if stype is None:
        raise ValueError(f"단계명 오류: '{slide_part}'. 허용: Connect, Concept, Review, Practice, Conclusion")

    cands = [s for s in module.slides if s.slide_type == stype]
    if not cands:
        raise ValueError(f"'{module.title}' 에 {stype} 슬라이드가 없습니다")
    if n < 1 or n > len(cands):
        raise ValueError(f"'{module.title}' 의 {stype} 슬라이드는 {len(cands)}개. #{n} 없음")
    return module, cands[n - 1]


# ------------------------------------------------------------- classify

def classify_candidate(course, slide, current_entry, cand, catalog):
    """
    → (mark, reasons)  mark: '✓' | '△' | '✗'
    """
    reasons = []
    stage = slide.stage
    mode = course.mode
    mins = slide.minutes

    # never_swap_with (양방향)
    if current_entry:
        if cand['id'] in current_entry.get('never_swap_with', []) or current_entry['id'] in cand.get('never_swap_with', []):
            return '✗', [f"교환 금지쌍: {current_entry['id']} ↔ {cand['id']}"]
        if cand['id'] == current_entry['id']:
            return '✗', ['현재 패턴과 동일']

    allowed = pattern_allowed_in(cand, stage)
    if allowed is None:
        return '✗', [f"{stage} 단계 불허 (허용: {', '.join(cand.get('stages', []) + cand.get('also_ok', []))})"]

    if mode in ('online', 'offline') and mode not in cand.get('mode', []):
        return '✗', [f"{mode} 모드 미지원 (지원: {'/'.join(cand.get('mode', []))})"]

    mark = '✓'
    if allowed == 'also_ok':
        mark = '△'
        reasons.append(f"본래 {'/'.join(cand['stages'])} 단계 활동. {stage}에서 교차 사용 허용")
    if current_entry and cand.get('swap_group') != current_entry.get('swap_group'):
        mark = '△'
        reasons.append(f"교환 그룹 다름: {current_entry.get('swap_group')} → {cand.get('swap_group')} (목적 차이 확인)")
    if not reasons:
        reasons.append(f"같은 단계, 같은 그룹({cand.get('swap_group')})")

    tr = cand.get('time')
    if mins is not None and tr:
        if mins < tr[0]:
            reasons.append(f"시간 부족: 슬롯 {mins}분 < 최소 {tr[0]}분 → time 조정 필요")
            if mark == '✓':
                mark = '△'
        elif mins > tr[1]:
            reasons.append(f"슬롯 {mins}분 > 권장 {tr[1]}분 (여유 {mins - tr[1]}분)")

    alts = slide.get('alt') or []
    if cand['id'] in alts:
        reasons.insert(0, 'alt 후보')
    return mark, reasons


def list_candidates(course, slide, catalog):
    cur_id = slide.get('pattern')
    cur = catalog.get(cur_id) if cur_id else None
    rows = []
    alts = slide.get('alt') or []
    for cand in catalog.values():
        mark, reasons = classify_candidate(course, slide, cur, cand, catalog)
        rows.append((cand, mark, reasons))
    order = {'✓': 0, '△': 1, '✗': 2}
    rows.sort(key=lambda r: (0 if r[0]['id'] in alts else 1, order[r[1]], r[0]['id']))
    return cur, rows


# ------------------------------------------------------------- edit

def slide_line_range(lines, slide):
    """슬라이드 헤더 줄 인덱스(0-based)와 끝(exclusive)"""
    start = slide.line_no - 1
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith('## ') or lines[i].startswith('# '):
            end = i
            break
    return start, end


def apply_swap(lines, slide, new_id, entry):
    """lines(list) 수정. 반환: 변경 요약 리스트"""
    start, end = slide_line_range(lines, slide)
    changes = []
    pat_idx = None
    title_idx = None
    time_idx = None
    params_idx = None
    for i in range(start + 1, end):
        l = lines[i]
        if l.startswith('pattern:'):
            pat_idx = i
        elif l.startswith('title:'):
            title_idx = i
        elif l.startswith('time:'):
            time_idx = i
        elif l.startswith('params:'):
            params_idx = i

    if pat_idx is not None:
        changes.append(f"pattern: {lines[pat_idx].split(':', 1)[1].strip()} → {new_id}")
        lines[pat_idx] = f'pattern: {new_id}'
        insert_at = pat_idx + 1
    else:
        anchor = title_idx if title_idx is not None else (time_idx if time_idx is not None else start)
        lines.insert(anchor + 1, f'pattern: {new_id}')
        changes.append(f"pattern: {new_id} 추가")
        insert_at = anchor + 2
        end += 1
        if params_idx is not None and params_idx > anchor:
            params_idx += 1

    # params 보완
    need = missing_params(entry, slide.get('params') or {})
    if need:
        if params_idx is None:
            block = ['params:'] + [f'  {k}: <입력: {entry.get("params", {}).get(k, k)}>' for k in need]
            lines[insert_at:insert_at] = block
            changes.append(f"params 추가 (입력 필요): {', '.join(need)}")
        else:
            # params 블록 끝 찾기
            j = params_idx + 1
            while j < end and (lines[j].startswith(('  ', '\t')) or lines[j].strip() == ''):
                if lines[j].strip() == '':
                    break
                j += 1
            lines[j:j] = [f'  {k}: <입력: {entry.get("params", {}).get(k, k)}>' for k in need]
            changes.append(f"params 보완 (입력 필요): {', '.join(need)}")
    return changes


def show_diff(old_lines, new_lines, name):
    diff = difflib.unified_diff(old_lines, new_lines, fromfile=f'{name} (before)', tofile=f'{name} (after)', lineterm='', n=2)
    for d in diff:
        safe_print(d)


# ------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description='4C 활동 교환')
    ap.add_argument('--md', required=True)
    ap.add_argument('--catalog', default=None)
    ap.add_argument('--at', help='"<모듈>/<단계>[#n]"')
    ap.add_argument('--list', action='store_true', help='교환 후보 목록')
    ap.add_argument('--to', help='교환할 pattern ID')
    ap.add_argument('--mode', choices=['online', 'offline'], help='일괄 모드 전환')
    ap.add_argument('--force', action='store_true', help='✗ 판정도 강행 (금지쌍 제외)')
    ap.add_argument('--dry-run', action='store_true', help='파일을 쓰지 않고 diff만')
    args = ap.parse_args()

    md = Path(args.md)
    if not md.exists():
        safe_print(f"[ERROR] 파일 없음: {md}")
        sys.exit(1)
    catalog = load_catalog(args.catalog)
    if not catalog:
        safe_print("[ERROR] 카탈로그를 찾을 수 없습니다 (--catalog references/activities.json)")
        sys.exit(1)
    course = parse_course(md)
    with open(md, 'r', encoding='utf-8') as f:
        original = f.read().split('\n')
    lines = list(original)

    # ---- 일괄 모드 전환
    if args.mode:
        target = args.mode
        course.frontmatter['mode'] = target   # 분류에 반영
        plan = []
        for module, slide in course.learner_slides():
            pid = slide.get('pattern')
            if not pid or pid not in catalog:
                continue
            cur = catalog[pid]
            if target in cur.get('mode', []):
                continue
            # 후보: alt 우선 → 같은 stage native + 같은 group → 같은 stage native
            cands = []
            for cid in (slide.get('alt') or []):
                if cid in catalog:
                    cands.append(catalog[cid])
            for e in catalog.values():
                if e not in cands:
                    cands.append(e)
            chosen = None
            for e in cands:
                mark, _ = classify_candidate(course, slide, cur, e, catalog)
                if mark == '✗':
                    continue
                if slide.stage in e.get('stages', []) and e.get('swap_group') == cur.get('swap_group'):
                    chosen = e
                    break
                if chosen is None and slide.stage in e.get('stages', []):
                    chosen = e
            plan.append((module, slide, cur, chosen))

        if not plan:
            safe_print(f"[OK] {target} 모드로 바꿀 활동이 없습니다")
            sys.exit(0)
        safe_print(f"[PLAN] {target} 모드 전환 — {len(plan)}건")
        # 뒤에서부터 적용해야 줄 번호가 안 흔들림
        for module, slide, cur, chosen in sorted(plan, key=lambda p: -p[1].line_no):
            if chosen is None:
                safe_print(f"  ✗ L{slide.line_no} {module.title}/{slide.slide_type} {cur['id']}: 대체 없음 (수동 처리)")
                continue
            ch = apply_swap(lines, slide, chosen['id'], chosen)
            safe_print(f"  ✓ L{slide.line_no} {module.title}/{slide.slide_type} {cur['id']} → {chosen['id']}  ({'; '.join(ch)})")
        # 프론트매터 mode 갱신
        fm_done = False
        if lines and lines[0].strip() == '---':
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    break
                if lines[i].startswith('mode:'):
                    lines[i] = f'mode: {target}'
                    fm_done = True
        if not fm_done:
            safe_print(f"  [TIP] 프론트매터에 mode: {target} 를 추가하세요")
        show_diff(original, lines, md.name)
        if not args.dry_run:
            with open(md, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            safe_print(f"[OK] 저장: {md}  (검증: validate_markdown_v3.py --md {md})")
        sys.exit(0)

    # ---- 단일 슬라이드
    if not args.at:
        safe_print("[ERROR] --at 또는 --mode 가 필요합니다")
        sys.exit(1)
    try:
        module, slide = locate(course, args.at)
    except ValueError as e:
        safe_print(f"[ERROR] {e}")
        sys.exit(1)

    cur_id = slide.get('pattern')
    safe_print(f"[AT] L{slide.line_no} {module.title} / {slide.slide_type} '{slide.get('title', '')}'  time={slide.get('time', '-')}  pattern={cur_id or '(없음, activity 자유 텍스트)'}")

    if args.list or not args.to:
        cur, rows = list_candidates(course, slide, catalog)
        safe_print(f"\n교환 후보 (모드 {course.mode}):")
        for cand, mark, reasons in rows:
            t = cand.get('time', ['?', '?'])
            safe_print(f"  {mark} {cand['id']:<24} {cand['name_ko']:<12} {t[0]}~{t[1]}분  {'/'.join(cand.get('mode', []))}")
            for r in reasons:
                safe_print(f"      - {r}")
        sys.exit(0)

    new_id = args.to
    if new_id not in catalog:
        safe_print(f"[ERROR] pattern '{new_id}' 가 카탈로그에 없습니다")
        sys.exit(1)
    entry = catalog[new_id]
    cur = catalog.get(cur_id) if cur_id else None
    mark, reasons = classify_candidate(course, slide, cur, entry, catalog)
    for r in reasons:
        safe_print(f"  {mark} {r}")
    if mark == '✗':
        if '금지쌍' in reasons[0] or not args.force:
            safe_print("[REJECT] 교환 불가. --list 로 허용 후보를 확인하세요" + ("" if '금지쌍' in reasons[0] else " (--force 로 강행 가능)"))
            sys.exit(1)
        safe_print("[FORCE] 규칙 위반을 무시하고 진행")

    changes = apply_swap(lines, slide, new_id, entry)
    safe_print(f"\n[SWAP] {cur_id or '(없음)'} → {new_id}")
    for c in changes:
        safe_print(f"  - {c}")
    if slide.get('activity'):
        safe_print("  [주의] activity: 자유 텍스트가 있어 빌드 시 그것이 우선합니다. 패턴 템플릿을 쓰려면 activity: 를 지우세요")
    safe_print('')
    show_diff(original, lines, md.name)
    if args.dry_run:
        safe_print("\n[DRY-RUN] 파일을 수정하지 않았습니다")
        sys.exit(0)
    with open(md, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    safe_print(f"\n[OK] 저장: {md}  (검증: validate_markdown_v3.py --md {md})")


if __name__ == '__main__':
    main()
