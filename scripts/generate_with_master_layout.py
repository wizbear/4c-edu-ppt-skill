#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 파일로부터 4C 구조 기반 PowerPoint 생성
슬라이드 마스터의 커스텀 레이아웃 사용 버전

커스텀 레이아웃 이름 규칙:
- "4C - Connect"
- "4C - Concept"
- "4C - Concrete Practice"
- "4C - Conclusion"
"""

import argparse
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
except ImportError:
    print("Error: python-pptx 라이브러리가 설치되어 있지 않습니다.")
    print("다음 명령으로 설치하세요: pip install python-pptx")
    sys.exit(1)


def safe_print(text):
    """Windows 콘솔에서 안전하게 출력"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 유니코드 문자를 ASCII로 변환
        ascii_text = text.encode('ascii', 'replace').decode('ascii')
        print(ascii_text)


class SlideContent:
    """슬라이드 내용을 담는 클래스"""
    def __init__(self, slide_type, **kwargs):
        self.slide_type = slide_type
        self.data = kwargs

    def __repr__(self):
        return f"SlideContent({self.slide_type}, {self.data})"


def parse_markdown(md_file):
    """Markdown 파일을 파싱하여 슬라이드 구조 추출"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    modules = []
    current_module = None
    current_slide = None
    current_field = None
    multiline_value = []

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # 모듈 시작
        if line.startswith('# ') and not line.startswith('## '):
            if current_module is not None:
                if current_slide:
                    if current_field and multiline_value:
                        current_slide.data[current_field] = '\n'.join(multiline_value).strip()
                    current_module['slides'].append(current_slide)
                modules.append(current_module)

            module_title = line[2:].strip()
            current_module = {'title': module_title, 'slides': []}
            current_slide = None
            current_field = None
            multiline_value = []

        # 슬라이드 타입
        elif line.startswith('## '):
            if current_slide:
                if current_field and multiline_value:
                    current_slide.data[current_field] = '\n'.join(multiline_value).strip()
                if current_module:
                    current_module['slides'].append(current_slide)

            slide_type = line[3:].strip()
            current_slide = SlideContent(slide_type)
            current_field = None
            multiline_value = []

        # 필드 값 (리스트 항목 제외)
        elif current_slide and ':' in line and not line.startswith(' ') and not line.startswith('\t') and not line.startswith('-'):
            if current_field and multiline_value:
                current_slide.data[current_field] = '\n'.join(multiline_value).strip()
                multiline_value = []

            parts = line.split(':', 1)
            if len(parts) == 2:
                field_name = parts[0].strip()
                field_value = parts[1].strip()

                if field_value == '|' or field_value == '':
                    # multiline 모드 시작 (| 또는 빈 값)
                    current_field = field_name
                    multiline_value = []
                else:
                    current_slide.data[field_name] = field_value
                    current_field = None

        # multiline 값
        elif current_field and (line.startswith('  ') or line.startswith('\t') or line.startswith('-') or line.strip() == ''):
            multiline_value.append(line.lstrip())

        # 빈 줄
        elif line.strip() in ['', '---']:
            if current_field and multiline_value:
                current_slide.data[current_field] = '\n'.join(multiline_value).strip()
                current_field = None
                multiline_value = []

        # Module Start 본문
        elif current_slide and current_slide.slide_type == 'Module Start' and line.strip():
            if 'content' not in current_slide.data:
                current_slide.data['content'] = []
            current_slide.data['content'].append(line.strip())

        i += 1

    # 마지막 처리
    if current_slide:
        if current_field and multiline_value:
            current_slide.data[current_field] = '\n'.join(multiline_value).strip()
        if current_module:
            current_module['slides'].append(current_slide)
    if current_module:
        modules.append(current_module)

    # Module Start content 문자열 변환
    for module in modules:
        for slide in module['slides']:
            if slide.slide_type == 'Module Start' and 'content' in slide.data:
                slide.data['content'] = '\n'.join(slide.data['content'])

    return modules


def find_layout_by_name(prs, name_pattern):
    """
    레이아웃 이름으로 레이아웃 찾기

    Args:
        prs: Presentation 객체
        name_pattern: 레이아웃 이름 패턴

    Returns:
        레이아웃 객체 또는 None
    """
    for layout in prs.slide_layouts:
        if name_pattern.lower() in layout.name.lower():
            return layout
    return None


def add_4c_slide_with_layout(prs, slide_type, time_str='', title='', main='', sub=''):
    """
    마스터 레이아웃을 사용하여 4C 슬라이드 추가

    레이아웃 이름 규칙:
    - "4C - Connect"
    - "4C - Concept"
    - "4C - Concrete Practice"
    - "4C - Conclusion"
    """

    # 레이아웃 찾기 (예: "Connect" → "4C - Connect")
    layout_name = f"4C - {slide_type}"
    layout = find_layout_by_name(prs, layout_name)

    if layout is None:
        # 대체: 단순히 slide_type으로 검색
        layout = find_layout_by_name(prs, slide_type)

    if layout is None:
        print(f"[WARNING] Layout '{layout_name}' not found in template.")
        print(f"[INFO] Available layouts:")
        for idx, l in enumerate(prs.slide_layouts):
            print(f"  [{idx}] {l.name}")
        print(f"[INFO] Using blank layout instead.")
        # Blank layout 사용
        layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

    print(f"[INFO] Creating '{slide_type}' slide using layout: {layout.name}")
    slide = prs.slides.add_slide(layout)

    # 자리표시자 채우기
    # placeholder type: 1=Title, 2=Body, 7=Content/Object, etc.

    title_filled = False
    content_count = 0

    for shape in slide.shapes:
        if not shape.is_placeholder:
            continue

        placeholder = shape.placeholder_format
        ph_type = placeholder.type

        # Title placeholder
        if ph_type == 1:  # PP_PLACEHOLDER.TITLE
            if title:
                shape.text = title
                title_filled = True
                print(f"  - Filled title: {title[:30]}...")

        # Content/Text placeholders
        elif ph_type in [2, 7]:  # BODY or OBJECT
            if content_count == 0 and main:
                shape.text = main
                content_count += 1
                print(f"  - Filled main message: {main[:30]}...")
            elif content_count == 1 and sub:
                shape.text = sub
                content_count += 1
                print(f"  - Filled sub message: {sub[:30]}...")

    # 시간 텍스트박스 업데이트 (비활성화 - 사용자가 직접 관리)
    # if time_str:
    #     for shape in slide.shapes:
    #         # 자리표시자는 제외 (일반 텍스트박스만)
    #         if shape.is_placeholder:
    #             continue
    #
    #         if shape.has_text_frame:
    #             text = shape.text_frame.text
    #             # "<시간>" 텍스트가 정확히 있으면 대체
    #             if '<시간>' in text:
    #                 # 위치가 우측 상단인지 확인
    #                 if shape.left > Inches(7):  # 우측
    #                     shape.text = time_str
    #                     print(f"  - Updated time: {time_str}")
    #                     break

    # 슬라이드 노트에 태그 추가
    slide_tag = slide_type.replace(' ', '')  # "Concrete Practice" -> "ConcretePractice"
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame

    # time 정보가 있으면 추가
    if time_str:
        text_frame.text = f"#Skill #{slide_tag} #{time_str}"
    else:
        text_frame.text = f"#Skill #{slide_tag}"

    return slide


def add_module_start_slide(prs, module_title, content=''):
    """모듈 시작 슬라이드 추가"""
    # Module_Divider 레이아웃 우선 찾기
    layout = find_layout_by_name(prs, "Module_Divider")
    if layout is None:
        layout = find_layout_by_name(prs, "Module Divider")
    if layout is None:
        layout = find_layout_by_name(prs, "Title Slide")
    if layout is None:
        layout = find_layout_by_name(prs, "Title")
    if layout is None:
        layout = prs.slide_layouts[0]

    slide = prs.slides.add_slide(layout)

    # 제목 채우기
    if slide.shapes.title:
        slide.shapes.title.text = module_title

    # 부제목 채우기 (content)
    if content:
        for shape in slide.shapes:
            if shape.is_placeholder:
                ph_type = shape.placeholder_format.type
                if ph_type == 2:  # Subtitle
                    shape.text = content
                    break

    return slide


def add_image_slide(prs, image_path, caption=''):
    """이미지 슬라이드 추가"""
    layout = find_layout_by_name(prs, "Blank")
    if layout is None:
        layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

    slide = prs.slides.add_slide(layout)

    try:
        # 이미지 추가
        left = Inches(1)
        top = Inches(1)
        width = Inches(8)

        pic = slide.shapes.add_picture(image_path, left, top, width=width)

        # 중앙 정렬
        slide_width = prs.slide_width
        slide_height = prs.slide_height
        pic.left = int((slide_width - pic.width) / 2)
        pic.top = int((slide_height - pic.height) / 2)

        # 캡션
        if caption:
            left = Inches(0.5)
            top = Inches(6.5)
            width = Inches(9)
            height = Inches(0.8)

            textbox = slide.shapes.add_textbox(left, top, width, height)
            text_frame = textbox.text_frame
            p = text_frame.paragraphs[0]
            p.text = caption
            p.font.size = Pt(16)
            p.font.italic = True
            p.alignment = PP_ALIGN.CENTER
            p.font.color.rgb = RGBColor(100, 100, 100)

    except Exception as e:
        print(f"[WARNING] Failed to add image '{image_path}': {e}")
        # 텍스트로 대체
        left = Inches(1)
        top = Inches(3)
        width = Inches(8)
        height = Inches(2)

        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        p = text_frame.paragraphs[0]
        p.text = f"[Image: {image_path}]\n{caption}"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(20)
        p.font.color.rgb = RGBColor(150, 150, 150)

    return slide


def add_video_slide(prs, video_path, description='', duration=''):
    """비디오 슬라이드 추가"""
    layout = find_layout_by_name(prs, "Blank")
    if layout is None:
        layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

    slide = prs.slides.add_slide(layout)

    # 비디오 아이콘
    left = Inches(4)
    top = Inches(2.5)
    width = Inches(2)
    height = Inches(1.5)

    textbox = slide.shapes.add_textbox(left, top, width, height)
    text_frame = textbox.text_frame
    p = text_frame.paragraphs[0]
    p.text = "▶️\nVIDEO"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(48)
    p.font.bold = True

    # 설명
    info_text = f"Video: {video_path}"
    if description:
        info_text += f"\n\n{description}"
    if duration:
        info_text += f"\n\n재생 시간: {duration}"

    left = Inches(1.5)
    top = Inches(4.5)
    width = Inches(7)
    height = Inches(2)

    textbox = slide.shapes.add_textbox(left, top, width, height)
    text_frame = textbox.text_frame
    text_frame.word_wrap = True
    p = text_frame.paragraphs[0]
    p.text = info_text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(100, 100, 100)

    return slide


def add_break_slide(prs, time_str='', sub_message=''):
    """Break 슬라이드 추가"""
    # 템플릿에서 Break 레이아웃 찾기
    layout = find_layout_by_name(prs, "Break")

    if layout is not None:
        # Break 레이아웃이 있으면 그대로 사용
        slide = prs.slides.add_slide(layout)

        # Title placeholder에 시간 채우기
        if time_str and slide.shapes.title:
            slide.shapes.title.text = time_str

        # Sub message placeholder 채우기
        if sub_message:
            for shape in slide.shapes:
                if shape.is_placeholder:
                    ph_type = shape.placeholder_format.type
                    if ph_type in [2, 7]:  # BODY or OBJECT
                        shape.text = sub_message
                        break

        safe_print("  [OK] Added Break slide (using template layout)")
        return slide

    # Break 레이아웃이 없으면 Blank 사용
    layout = find_layout_by_name(prs, "Blank")
    if layout is None:
        layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

    slide = prs.slides.add_slide(layout)

    # 배경색
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)

    # Break 텍스트
    left = Inches(3)
    top = Inches(3)
    width = Inches(4)
    height = Inches(1.5)

    textbox = slide.shapes.add_textbox(left, top, width, height)
    text_frame = textbox.text_frame
    p = text_frame.paragraphs[0]
    p.text = "☕ Break"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(100, 100, 100)

    safe_print("  [OK] Added Break slide (using Blank layout)")
    return slide


def create_presentation_from_markdown(md_file, template_file, output_file='output.pptx'):
    """Markdown 파일로부터 프레젠테이션 생성 (마스터 레이아웃 사용)"""

    # Markdown 파싱
    print(f"[INFO] Parsing markdown file: {md_file}")
    modules = parse_markdown(md_file)
    print(f"[INFO] Found {len(modules)} modules")

    # 템플릿 로드
    try:
        prs = Presentation(template_file)
        print(f"[INFO] Using template: {template_file}")
        print(f"[INFO] Available layouts in template:")
        for idx, layout in enumerate(prs.slide_layouts):
            print(f"  [{idx}] {layout.name}")
    except Exception as e:
        print(f"[ERROR] Failed to load template '{template_file}': {e}")
        sys.exit(1)

    # 슬라이드 생성
    total_slides = 0

    for module in modules:
        print(f"\n[INFO] Processing module: {module['title']}")

        for slide in module['slides']:
            slide_type = slide.slide_type
            data = slide.data

            if slide_type == 'Module Start':
                content = data.get('content', '')
                add_module_start_slide(prs, module['title'], content)
                total_slides += 1
                try:
                    print(f"  ✓ Added Module Start slide")
                except UnicodeEncodeError:
                    print(f"  [OK] Added Module Start slide")

            elif slide_type in ['Connect', 'Concept', 'Concrete Practice', 'Conclusion']:
                time_str = data.get('time', '')
                title = data.get('title', '')
                main = data.get('main', '')
                sub = data.get('sub', data.get('activity', ''))

                # 디버그: sub 값 확인
                safe_print(f"  [DEBUG] slide_type={slide_type}, sub length={len(sub) if sub else 0}")
                if sub:
                    safe_print(f"  [DEBUG] sub preview: {sub[:50]}...")

                add_4c_slide_with_layout(prs, slide_type, time_str, title, main, sub)
                total_slides += 1

            elif slide_type == 'Image':
                image_path = data.get('image', '')
                caption = data.get('caption', '')
                if image_path:
                    add_image_slide(prs, image_path, caption)
                    total_slides += 1
                    print(f"  [OK] Added Image slide")

            elif slide_type == 'Video':
                video_path = data.get('video', '')
                description = data.get('description', '')
                duration = data.get('duration', '')
                if video_path:
                    add_video_slide(prs, video_path, description, duration)
                    total_slides += 1
                    print(f"  [OK] Added Video slide")

            elif slide_type == 'Break':
                time_str = data.get('time', '')
                sub_message = data.get('sub', '')
                add_break_slide(prs, time_str, sub_message)
                total_slides += 1
                print(f"  [OK] Added Break slide")

    # 저장
    prs.save(output_file)

    try:
        print(f"\n✅ PowerPoint 파일이 생성되었습니다: {output_file}")
        print(f"   총 {total_slides} 슬라이드가 생성되었습니다.")
    except UnicodeEncodeError:
        print(f"\n[SUCCESS] PowerPoint file created: {output_file}")
        print(f"   Total {total_slides} slides generated.")


def main():
    parser = argparse.ArgumentParser(
        description='Markdown 파일로부터 4C 교육 구조 기반 PowerPoint 생성 (마스터 레이아웃 사용)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
템플릿 요구사항:
  템플릿에는 다음 레이아웃들이 있어야 합니다:
  - "4C - Connect" (또는 "Connect")
  - "4C - Concept" (또는 "Concept")
  - "4C - Concrete Practice" (또는 "Concrete Practice")
  - "4C - Conclusion" (또는 "Conclusion")

예제:
  python generate_with_master_layout.py \\
    --md course.md \\
    --template 4c_custom_template.pptx \\
    --output result.pptx
        """
    )

    parser.add_argument('--md', required=True, help='Markdown 콘텐츠 파일 경로')
    parser.add_argument('--template', required=True, help='4C 커스텀 레이아웃이 포함된 템플릿 파일 경로')
    parser.add_argument('--output', default='output.pptx', help='출력 파일명 (기본: output.pptx)')

    args = parser.parse_args()

    # 파일 존재 확인
    if not Path(args.md).exists():
        print(f"[ERROR] Markdown 파일을 찾을 수 없습니다: {args.md}")
        sys.exit(1)

    if not Path(args.template).exists():
        print(f"[ERROR] 템플릿 파일을 찾을 수 없습니다: {args.template}")
        sys.exit(1)

    # PPT 생성
    create_presentation_from_markdown(
        md_file=args.md,
        template_file=args.template,
        output_file=args.output
    )


if __name__ == '__main__':
    main()
