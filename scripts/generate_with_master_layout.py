#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 파일로부터 4C 구조 기반 PowerPoint 생성 (메인 빌드 스크립트)

레이아웃 이름 규칙 (템플릿):
- "Title_Page"            : 과정 제목 (프론트매터 course가 있을 때)
- "Module_Divider"        : 모듈 시작
- "4C - Connect" / "Connect"
- "4C - Concept" / "Concept"
- "4C - Review" / "Review"           (없으면 Concept 레이아웃으로 대체)
- "4C - Concrete Practice" / "Concrete Practice"
- "4C - Conclusion" / "Conclusion"
- "Break", "End", "Blank"

v1.1 추가
- 프론트매터(course/audience/total_time/outcome/mode) → Title_Page 슬라이드
- 모듈 outcome → Module Start 본문과 노트
- activity: 를 4C 전 단계에서 렌더 (본문 하단 "▶ 활동" 블록)
- pattern: + params: → references/activities.json 템플릿으로 활동 텍스트 생성
- ## Review 슬라이드
- notes: → 강사 노트, handout: → <output>_handout.md
- action_plan: → Conclusion "✍ 실행 계획" 블록
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md4c import (parse_course, load_catalog, render_activity, safe_print,  # noqa: E402
                  FOUR_C, LEARNER_SLIDES)

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
except ImportError:
    print("Error: python-pptx 라이브러리가 설치되어 있지 않습니다.")
    print("다음 명령으로 설치하세요: pip install python-pptx")
    sys.exit(1)


# v1.0 호환 심볼
from md4c import SlideContent, parse_markdown  # noqa: E402,F401


# ------------------------------------------------------------- helpers

def find_layout_by_name(prs, name_pattern):
    """레이아웃 이름에 name_pattern(대소문자 무시)이 포함된 첫 레이아웃"""
    for layout in prs.slide_layouts:
        if name_pattern.lower() in layout.name.lower():
            return layout
    return None


def find_first_layout(prs, *names):
    for n in names:
        l = find_layout_by_name(prs, n)
        if l is not None:
            return l
    return None


def blank_layout(prs):
    l = find_layout_by_name(prs, 'Blank')
    if l is not None:
        return l
    return prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]


def body_placeholders(slide):
    """BODY(2)/OBJECT(7) placeholder를 idx 순으로"""
    phs = []
    for shape in slide.shapes:
        if shape.is_placeholder and shape.placeholder_format.type in (2, 7):
            phs.append(shape)
    phs.sort(key=lambda s: s.placeholder_format.idx)
    return phs


def set_title(slide, text):
    if text and slide.shapes.title is not None:
        slide.shapes.title.text = text
        return True
    return False


def add_fallback_textbox(slide, prs, text, top_in=1.5, size=18):
    left, top, width, height = Inches(0.8), Inches(top_in), prs.slide_width - Inches(1.6), Inches(4.5)
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = text
    for p in tf.paragraphs:
        p.font.size = Pt(size)
    return tb


def set_notes(slide, lines):
    """강사 노트 설정. lines: 문자열 리스트 (빈 항목 제외)"""
    text = '\n'.join([l for l in lines if l])
    slide.notes_slide.notes_text_frame.text = text


def activity_block(slide_content, catalog):
    """'▶ 활동' 블록 텍스트. 없으면 ''"""
    text = render_activity(slide_content, catalog)
    if not text:
        return ''
    t = slide_content.get('time')
    head = f'▶ 활동 ({t})' if t else '▶ 활동'
    return f'{head}\n{text}'


def tag_line(slide_content):
    tag = slide_content.slide_type.replace(' ', '')
    parts = ['#Skill', f'#{tag}']
    if slide_content.get('time'):
        parts.append(f"#{slide_content.get('time')}")
    if slide_content.get('pattern'):
        parts.append(f"#Pattern:{slide_content.get('pattern')}")
    return ' '.join(parts)


# ------------------------------------------------------------- slide builders

def add_title_slide(prs, course):
    layout = find_first_layout(prs, 'Title_Page', 'Title Slide', 'Title')
    if layout is None:
        return None
    slide = prs.slides.add_slide(layout)
    set_title(slide, course.title)
    phs = body_placeholders(slide)
    fm = course.frontmatter
    line1 = ' · '.join([v for v in [fm.get('subtitle'), fm.get('audience')] if v])
    line2 = ' · '.join([v for v in [fm.get('total_time'), fm.get('outcome')] if v])
    if phs:
        if line1:
            phs[0].text = line1
        if len(phs) > 1 and line2:
            phs[1].text = line2
        elif len(phs) == 1 and line2:
            phs[0].text = (line1 + '\n' + line2).strip()
    set_notes(slide, ['#Skill #TitlePage',
                      f"[과정 성과] {fm.get('outcome')}" if fm.get('outcome') else '',
                      f"[대상] {fm.get('audience')}" if fm.get('audience') else '',
                      f"[모드] {fm.get('mode')}" if fm.get('mode') else ''])
    safe_print(f"  [OK] Title slide: {course.title}")
    return slide


def add_module_start_slide(prs, module_title, content='', outcome=''):
    layout = find_first_layout(prs, 'Module_Divider', 'Module Divider', 'Title Slide', 'Title')
    if layout is None:
        layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(layout)
    set_title(slide, module_title)
    phs = body_placeholders(slide)
    body = content or ''
    if outcome:
        body = (body + '\n' if body else '') + f'학습 성과: {outcome}'
    if phs and body:
        phs[0].text = body
    set_notes(slide, ['#Skill #ModuleStart',
                      f'[학습 성과] {outcome}' if outcome else ''])
    return slide


def add_4c_slide_with_layout(prs, slide_content, catalog=None, time_str=None, title=None, main=None, sub=None):
    """
    4C/Review 슬라이드 추가.
    v1.0 호환: add_4c_slide_with_layout(prs, 'Connect', time, title, main, sub) 형태도 허용.
    """
    if isinstance(slide_content, str):   # v1.0 시그니처
        sc = SlideContent(slide_content, time=time_str or '', title=title or '', main=main or '', sub=sub or '')
    else:
        sc = slide_content
    slide_type = sc.slide_type

    layout = find_first_layout(prs, f'4C - {slide_type}', slide_type)
    if layout is None and slide_type == 'Review':
        layout = find_first_layout(prs, '4C - Concept', 'Concept')
        if layout is not None:
            safe_print("  [INFO] 'Review' layout not found. Using Concept layout.")
    if layout is None:
        safe_print(f"[WARNING] Layout for '{slide_type}' not found in template. Using blank layout.")
        layout = blank_layout(prs)

    slide = prs.slides.add_slide(layout)
    set_title(slide, sc.get('title'))

    main_text = sc.get('main', '')
    sub_text = sc.get('sub', '')
    act = activity_block(sc, catalog)
    plan = sc.get('action_plan', '')
    plan_text = f'✍ 실행 계획\n{plan}' if plan else ''

    # Review: main/sub 없이 활동만
    if slide_type == 'Review' and not main_text:
        main_text = act
        act = ''

    tail = '\n\n'.join([t for t in [act, plan_text] if t])
    phs = body_placeholders(slide)

    if len(phs) >= 2:
        if main_text:
            phs[0].text = main_text
        second = '\n\n'.join([t for t in [sub_text, tail] if t])
        if second:
            phs[1].text = second
    elif len(phs) == 1:
        combined = '\n\n'.join([t for t in [main_text, sub_text, tail] if t])
        if combined:
            phs[0].text = combined
    else:
        combined = '\n\n'.join([t for t in [main_text, sub_text, tail] if t])
        if combined:
            add_fallback_textbox(slide, prs, combined)

    # 강사 노트
    notes = [tag_line(sc)]
    act_full = render_activity(sc, catalog)
    if act_full:
        notes.append(f'[활동]\n{act_full}')
    if plan:
        notes.append(f'[실행 계획] {plan}')
    if sc.get('notes'):
        notes.append(f"[강사 노트]\n{sc.get('notes')}")
    if sc.get('handout'):
        notes.append('[부록] 이 슬라이드의 handout 내용은 *_handout.md 참고')
    if sc.get('alt'):
        notes.append(f"[교환 후보] {', '.join(sc.get('alt'))}")
    set_notes(slide, notes)

    safe_print(f"  [OK] {slide_type}: {sc.get('title', '')[:30]}")
    return slide


def add_image_slide(prs, image_path, caption=''):
    slide = prs.slides.add_slide(blank_layout(prs))
    try:
        pic = slide.shapes.add_picture(image_path, Inches(1), Inches(1), width=Inches(8))
        pic.left = int((prs.slide_width - pic.width) / 2)
        pic.top = int((prs.slide_height - pic.height) / 2)
        if caption:
            tb = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.8))
            p = tb.text_frame.paragraphs[0]
            p.text = caption
            p.font.size = Pt(16)
            p.font.italic = True
            p.alignment = PP_ALIGN.CENTER
            p.font.color.rgb = RGBColor(100, 100, 100)
    except Exception as e:
        safe_print(f"[WARNING] Failed to add image '{image_path}': {e}")
        tb = slide.shapes.add_textbox(Inches(1), Inches(3), Inches(8), Inches(2))
        p = tb.text_frame.paragraphs[0]
        p.text = f"[Image: {image_path}]\n{caption}"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(20)
        p.font.color.rgb = RGBColor(150, 150, 150)
    set_notes(slide, ['#Skill #Image'])
    return slide


def add_video_slide(prs, video_path, description='', duration=''):
    slide = prs.slides.add_slide(blank_layout(prs))
    tb = slide.shapes.add_textbox(Inches(4), Inches(2.5), Inches(2), Inches(1.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "▶\nVIDEO"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(48)
    p.font.bold = True

    info = f"Video: {video_path}"
    if description:
        info += f"\n\n{description}"
    if duration:
        info += f"\n\n재생 시간: {duration}"
    tb = slide.shapes.add_textbox(Inches(1.5), Inches(4.5), Inches(7), Inches(2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = info
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(100, 100, 100)
    set_notes(slide, ['#Skill #Video', f'#{duration}' if duration else ''])
    return slide


def add_break_slide(prs, time_str='', sub_message=''):
    layout = find_layout_by_name(prs, "Break")
    if layout is not None:
        slide = prs.slides.add_slide(layout)
        if time_str:
            set_title(slide, time_str)
        phs = body_placeholders(slide)
        if sub_message and phs:
            phs[0].text = sub_message
    else:
        slide = prs.slides.add_slide(blank_layout(prs))
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(245, 245, 245)
        tb = slide.shapes.add_textbox(Inches(3), Inches(3), Inches(4), Inches(1.5))
        p = tb.text_frame.paragraphs[0]
        p.text = "☕ Break"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(54)
        p.font.bold = True
        p.font.color.rgb = RGBColor(100, 100, 100)
    set_notes(slide, ['#Skill #Break', f'#{time_str}' if time_str else ''])
    safe_print("  [OK] Break slide")
    return slide


def add_end_slide(prs):
    layout = find_layout_by_name(prs, 'End')
    if layout is None:
        return None
    slide = prs.slides.add_slide(layout)
    set_notes(slide, ['#Skill #End'])
    safe_print("  [OK] End slide")
    return slide


# ------------------------------------------------------------- handout

def write_handout(course, items, out_path):
    """items: [(module_title, slide_type, slide_title, text)]"""
    lines = [f"# {course.title or '교육 과정'} — 참고 자료 (부록)", '']
    fm = course.frontmatter
    if fm.get('audience'):
        lines.append(f"- 대상: {fm['audience']}")
    if fm.get('outcome'):
        lines.append(f"- 과정 성과: {fm['outcome']}")
    lines.append('')
    lines.append('> 슬라이드에 넣지 않은 nice-to-know 내용입니다. 강의 중 배포하지 말고 끝난 뒤 또는 사전 자료로 쓰세요.')
    lines.append('')
    current = None
    for mod_title, stype, stitle, text in items:
        if mod_title != current:
            current = mod_title
            lines.append(f'## {mod_title}')
            lines.append('')
        head = stitle or stype
        lines.append(f'### {head}  ({stype})')
        lines.append('')
        lines.append(text)
        lines.append('')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    safe_print(f"[OK] Handout written: {out_path} ({len(items)} items)")


# ------------------------------------------------------------- main build

def create_presentation_from_markdown(md_file, template_file, output_file='output.pptx',
                                      catalog_path=None, add_title=True, add_end=True,
                                      handout_path=None):
    safe_print(f"[INFO] Parsing markdown file: {md_file}")
    course = parse_course(md_file)
    catalog = load_catalog(catalog_path)
    safe_print(f"[INFO] Found {len(course.modules)} modules, catalog {len(catalog)} activities")

    try:
        prs = Presentation(template_file)
        safe_print(f"[INFO] Using template: {template_file}")
    except Exception as e:
        safe_print(f"[ERROR] Failed to load template '{template_file}': {e}")
        sys.exit(1)

    total = 0
    handout_items = []

    if add_title and course.title:
        if add_title_slide(prs, course) is not None:
            total += 1

    for module in course.modules:
        if not module.slides:
            continue
        safe_print(f"\n[INFO] Module: {module.title}")
        for sc in module.slides:
            st = sc.slide_type
            data = sc.data

            if st == 'Module Start':
                add_module_start_slide(prs, module.title, data.get('content', ''), module.outcome)
                total += 1
                safe_print("  [OK] Module Start")

            elif st in LEARNER_SLIDES:
                add_4c_slide_with_layout(prs, sc, catalog)
                total += 1

            elif st == 'Image':
                if data.get('image'):
                    add_image_slide(prs, data['image'], data.get('caption', ''))
                    total += 1
                    safe_print("  [OK] Image slide")

            elif st == 'Video':
                if data.get('video'):
                    add_video_slide(prs, data['video'], data.get('description', ''), data.get('duration', ''))
                    total += 1
                    safe_print("  [OK] Video slide")

            elif st == 'Break':
                add_break_slide(prs, data.get('time', ''), data.get('sub', ''))
                total += 1

            else:
                safe_print(f"  [WARNING] Unknown slide type '{st}' (line {sc.line_no}) skipped")

            if data.get('handout'):
                handout_items.append((module.title, st, data.get('title', ''), data['handout']))

    if add_end:
        if add_end_slide(prs) is not None:
            total += 1

    prs.save(output_file)
    safe_print(f"\n[SUCCESS] PowerPoint file created: {output_file}")
    safe_print(f"   Total {total} slides generated.")

    if handout_items:
        hp = Path(handout_path) if handout_path else Path(output_file).with_name(Path(output_file).stem + '_handout.md')
        write_handout(course, handout_items, hp)

    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Markdown 파일로부터 4C 교육 구조 기반 PowerPoint 생성',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  python generate_with_master_layout.py --md course.md \\
    --template pptx-templates/default_4c_template.pptx --output result.pptx

빌드 전 검증:
  python validate_markdown_v3.py --md course.md
        """
    )
    parser.add_argument('--md', required=True, help='Markdown 콘텐츠 파일')
    parser.add_argument('--template', required=True, help='4C 레이아웃이 포함된 템플릿 .pptx')
    parser.add_argument('--output', default='output.pptx', help='출력 파일명 (기본: output.pptx)')
    parser.add_argument('--catalog', default=None, help='활동 카탈로그 JSON (기본: references/activities.json)')
    parser.add_argument('--handout', default=None, help='부록 MD 경로 (기본: <output>_handout.md)')
    parser.add_argument('--no-title', action='store_true', help='과정 제목 슬라이드 생략')
    parser.add_argument('--no-end', action='store_true', help='End 슬라이드 생략')
    args = parser.parse_args()

    if not Path(args.md).exists():
        safe_print(f"[ERROR] Markdown 파일을 찾을 수 없습니다: {args.md}")
        sys.exit(1)
    if not Path(args.template).exists():
        safe_print(f"[ERROR] 템플릿 파일을 찾을 수 없습니다: {args.template}")
        sys.exit(1)

    create_presentation_from_markdown(
        md_file=args.md,
        template_file=args.template,
        output_file=args.output,
        catalog_path=args.catalog,
        add_title=not args.no_title,
        add_end=not args.no_end,
        handout_path=args.handout,
    )


if __name__ == '__main__':
    main()
