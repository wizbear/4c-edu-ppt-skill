#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 파일로부터 4C 구조 기반 PowerPoint 생성
모듈 구조, 반복 가능한 4C, 이미지/비디오 슬라이드 지원
"""

import argparse
import sys
import re
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.dml.color import RGBColor
except ImportError:
    print("Error: python-pptx 라이브러리가 설치되어 있지 않습니다.")
    print("다음 명령으로 설치하세요: pip install python-pptx")
    sys.exit(1)


# 4C 타입별 아이콘
ICONS = {
    'Connect': '🔗',
    'Concept': '💡',
    'Concrete Practice': '✏️',
    'Conclusion': '🎯'
}

# 4C 타입별 색상 (RGB)
COLORS = {
    'Connect': (46, 125, 50),      # Green
    'Concept': (25, 118, 210),     # Blue
    'Concrete Practice': (251, 140, 0),  # Orange
    'Conclusion': (123, 31, 162)   # Purple
}


class SlideContent:
    """슬라이드 내용을 담는 클래스"""
    def __init__(self, slide_type, **kwargs):
        self.slide_type = slide_type
        self.data = kwargs

    def __repr__(self):
        return f"SlideContent({self.slide_type}, {self.data})"


def parse_markdown(md_file):
    """
    Markdown 파일을 파싱하여 슬라이드 구조 추출

    Returns:
        list: 모듈 리스트, 각 모듈은 슬라이드 리스트를 포함
    """
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

        # 모듈 시작 (# 모듈 X: ...)
        if line.startswith('# ') and not line.startswith('## '):
            if current_module is not None:
                # 이전 슬라이드 저장
                if current_slide:
                    if current_field and multiline_value:
                        current_slide.data[current_field] = '\n'.join(multiline_value).strip()
                    current_module['slides'].append(current_slide)
                modules.append(current_module)

            module_title = line[2:].strip()
            current_module = {
                'title': module_title,
                'slides': []
            }
            current_slide = None
            current_field = None
            multiline_value = []

        # 슬라이드 타입 감지 (## ...)
        elif line.startswith('## '):
            # 이전 슬라이드 저장
            if current_slide:
                if current_field and multiline_value:
                    current_slide.data[current_field] = '\n'.join(multiline_value).strip()
                if current_module:
                    current_module['slides'].append(current_slide)

            slide_type = line[3:].strip()
            current_slide = SlideContent(slide_type)
            current_field = None
            multiline_value = []

        # 필드 값 파싱 (key: value)
        elif current_slide and ':' in line and not line.startswith(' ') and not line.startswith('\t'):
            # 이전 multiline 필드 저장
            if current_field and multiline_value:
                current_slide.data[current_field] = '\n'.join(multiline_value).strip()
                multiline_value = []

            parts = line.split(':', 1)
            if len(parts) == 2:
                field_name = parts[0].strip()
                field_value = parts[1].strip()

                # | 로 시작하면 다음 줄부터 multiline
                if field_value == '|':
                    current_field = field_name
                    multiline_value = []
                else:
                    current_slide.data[field_name] = field_value
                    current_field = None

        # multiline 값 수집
        elif current_field and (line.startswith('  ') or line.startswith('\t') or line.strip() == ''):
            multiline_value.append(line.lstrip())

        # 빈 줄이나 구분선
        elif line.strip() in ['', '---']:
            # multiline 필드 종료
            if current_field and multiline_value:
                current_slide.data[current_field] = '\n'.join(multiline_value).strip()
                current_field = None
                multiline_value = []

        # Module Start의 본문
        elif current_slide and current_slide.slide_type == 'Module Start' and line.strip():
            if 'content' not in current_slide.data:
                current_slide.data['content'] = []
            current_slide.data['content'].append(line.strip())

        i += 1

    # 마지막 슬라이드 및 모듈 저장
    if current_slide:
        if current_field and multiline_value:
            current_slide.data[current_field] = '\n'.join(multiline_value).strip()
        if current_module:
            current_module['slides'].append(current_slide)
    if current_module:
        modules.append(current_module)

    # Module Start의 content를 문자열로 변환
    for module in modules:
        for slide in module['slides']:
            if slide.slide_type == 'Module Start' and 'content' in slide.data:
                slide.data['content'] = '\n'.join(slide.data['content'])

    return modules


def add_module_start_slide(prs, module_title, content=''):
    """모듈 시작 슬라이드 추가"""
    slide = prs.slides.add_slide(prs.slide_layouts[0])  # Title Slide

    title_shape = slide.shapes.title
    title_shape.text = module_title

    # 제목 스타일
    title_frame = title_shape.text_frame
    title_frame.paragraphs[0].font.size = Pt(44)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(0, 51, 102)

    # 내용 추가 (있으면)
    if content and len(slide.placeholders) > 1:
        subtitle_shape = slide.placeholders[1]
        subtitle_shape.text = content

    return slide


def add_4c_slide(prs, slide_type, time_str='', title='', main='', sub=''):
    """
    4C 슬라이드 추가
    상단에 아이콘 + 시간, Title, Main Message, Sub Message
    """
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank layout

    color = COLORS.get(slide_type, (0, 102, 204))
    icon = ICONS.get(slide_type, '•')

    # 아이콘 + 시간 (상단 좌측)
    if time_str or icon:
        left = Inches(0.5)
        top = Inches(0.3)
        width = Inches(9)
        height = Inches(0.4)

        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.word_wrap = False

        p = text_frame.paragraphs[0]
        p.text = f"{icon} {slide_type}"
        if time_str:
            p.text += f"  |  ⏱ {time_str}"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(*color)
        p.font.bold = True

    # Title (큰 제목)
    if title:
        left = Inches(0.5)
        top = Inches(1.0)
        width = Inches(9)
        height = Inches(1.0)

        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame

        p = text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0, 0, 0)

    # Main Message
    if main:
        left = Inches(0.5)
        top = Inches(2.2)
        width = Inches(9)
        height = Inches(1.5)

        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.word_wrap = True

        p = text_frame.paragraphs[0]
        p.text = main
        p.font.size = Pt(24)
        p.font.color.rgb = RGBColor(60, 60, 60)

    # Sub Message / Activity Guide
    if sub:
        left = Inches(0.5)
        top = Inches(4.0)
        width = Inches(9)
        height = Inches(3.0)

        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame
        text_frame.word_wrap = True

        p = text_frame.paragraphs[0]
        p.text = sub
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(80, 80, 80)
        p.line_spacing = 1.3

    return slide


def add_image_slide(prs, image_path, caption=''):
    """이미지 슬라이드 추가"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

    # 이미지 추가 (중앙 배치)
    try:
        left = Inches(1)
        top = Inches(1)
        width = Inches(8)

        pic = slide.shapes.add_picture(image_path, left, top, width=width)

        # 이미지 중앙 정렬
        slide_width = prs.slide_width
        slide_height = prs.slide_height
        pic.left = int((slide_width - pic.width) / 2)
        pic.top = int((slide_height - pic.height) / 2)

        # 캡션 추가
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
        # 오류 시 텍스트로 대체
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
    """비디오 슬라이드 추가 (비디오 파일 대신 설명 표시)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

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

    # 비디오 설명
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


def add_break_slide(prs):
    """Break 슬라이드 추가"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

    # 배경색 (연한 회색)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)

    # "Break" 텍스트
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

    return slide


def create_presentation_from_markdown(md_file, template_file=None, output_file='output.pptx'):
    """Markdown 파일로부터 프레젠테이션 생성"""

    # Markdown 파싱
    print(f"[INFO] Parsing markdown file: {md_file}")
    modules = parse_markdown(md_file)
    print(f"[INFO] Found {len(modules)} modules")

    # 프레젠테이션 생성
    if template_file:
        try:
            prs = Presentation(template_file)
            print(f"[INFO] Using template: {template_file}")
        except Exception as e:
            print(f"[WARNING] Failed to load template '{template_file}': {e}")
            print("[INFO] Creating presentation without template")
            prs = Presentation()
    else:
        prs = Presentation()

    # 각 모듈의 슬라이드 생성
    total_slides = 0
    for module in modules:
        print(f"[INFO] Processing module: {module['title']}")

        for slide in module['slides']:
            slide_type = slide.slide_type
            data = slide.data

            if slide_type == 'Module Start':
                content = data.get('content', '')
                add_module_start_slide(prs, module['title'], content)
                total_slides += 1

            elif slide_type in ['Connect', 'Concept', 'Concrete Practice', 'Conclusion']:
                time_str = data.get('time', '')
                title = data.get('title', '')
                main = data.get('main', '')
                sub = data.get('sub', data.get('activity', ''))

                add_4c_slide(prs, slide_type, time_str, title, main, sub)
                total_slides += 1

            elif slide_type == 'Image':
                image_path = data.get('image', '')
                caption = data.get('caption', '')
                if image_path:
                    add_image_slide(prs, image_path, caption)
                    total_slides += 1

            elif slide_type == 'Video':
                video_path = data.get('video', '')
                description = data.get('description', '')
                duration = data.get('duration', '')
                if video_path:
                    add_video_slide(prs, video_path, description, duration)
                    total_slides += 1

            elif slide_type == 'Break':
                add_break_slide(prs)
                total_slides += 1

    # 저장
    prs.save(output_file)

    try:
        print(f"✅ PowerPoint 파일이 생성되었습니다: {output_file}")
        print(f"   총 {total_slides} 슬라이드가 생성되었습니다.")
    except UnicodeEncodeError:
        print(f"[SUCCESS] PowerPoint file created: {output_file}")
        print(f"   Total {total_slides} slides generated.")


def main():
    parser = argparse.ArgumentParser(
        description='Markdown 파일로부터 4C 교육 구조 기반 PowerPoint 생성',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  python generate_from_md.py --md course.md --output presentation.pptx
  python generate_from_md.py --md course.md --template my_template.pptx --output result.pptx
        """
    )

    parser.add_argument('--md', required=True, help='Markdown 콘텐츠 파일 경로')
    parser.add_argument('--template', help='사용할 PPTX 템플릿 파일 경로 (선택)')
    parser.add_argument('--output', default='output.pptx', help='출력 파일명 (기본: output.pptx)')

    args = parser.parse_args()

    # Markdown 파일 존재 확인
    if not Path(args.md).exists():
        print(f"[ERROR] Markdown 파일을 찾을 수 없습니다: {args.md}")
        sys.exit(1)

    # PPT 생성
    create_presentation_from_markdown(
        md_file=args.md,
        template_file=args.template,
        output_file=args.output
    )


if __name__ == '__main__':
    main()
