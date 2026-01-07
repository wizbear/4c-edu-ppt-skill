#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4C 교육 구조 기반 PowerPoint 생성 스크립트
Connect - Concept - Concrete Practice - Conclusion 구조로 교육용 PPT 생성
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


def add_title_slide(prs, title):
    """제목 슬라이드 추가"""
    slide = prs.slides.add_slide(prs.slide_layouts[0])  # Title Slide layout

    title_shape = slide.shapes.title
    subtitle_shape = slide.placeholders[1]

    title_shape.text = title
    subtitle_shape.text = "4C 교육 구조 기반 학습"

    # 제목 스타일링
    title_frame = title_shape.text_frame
    title_frame.paragraphs[0].font.size = Pt(44)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(0, 51, 102)

    return slide


def add_content_slide(prs, title, content, color_rgb=(0, 102, 204)):
    """내용 슬라이드 추가"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content layout

    title_shape = slide.shapes.title
    title_shape.text = title

    # 제목 스타일링
    title_frame = title_shape.text_frame
    title_frame.paragraphs[0].font.size = Pt(40)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(*color_rgb)

    # 내용 추가
    body_shape = slide.placeholders[1]
    text_frame = body_shape.text_frame
    text_frame.clear()

    # 내용을 줄바꿈으로 분리하여 추가
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()

        p.text = line.strip()
        p.font.size = Pt(20)
        p.level = 0
        p.space_before = Pt(12)

    return slide


def add_4c_slide(prs, phase, title, content, icon):
    """4C 각 단계별 슬라이드 추가"""
    colors = {
        'Connect': (46, 125, 50),      # Green
        'Concept': (25, 118, 210),     # Blue
        'Concrete': (251, 140, 0),     # Orange
        'Conclusion': (123, 31, 162)   # Purple
    }

    color = colors.get(phase, (0, 102, 204))

    slide = prs.slides.add_slide(prs.slide_layouts[1])

    # 제목: 아이콘 + 단계명
    title_shape = slide.shapes.title
    title_shape.text = f"{icon} {title}"

    # 제목 스타일링
    title_frame = title_shape.text_frame
    title_frame.paragraphs[0].font.size = Pt(40)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(*color)

    # 내용 추가
    body_shape = slide.placeholders[1]
    text_frame = body_shape.text_frame
    text_frame.clear()

    # 내용을 줄바꿈으로 분리
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()

        p.text = line.strip()
        p.font.size = Pt(22)
        p.space_before = Pt(12)

        # 불릿 포인트가 아닌 경우에만 추가
        if line.strip().startswith('-') or line.strip().startswith('•'):
            p.text = line.strip()[1:].strip()
            p.level = 0
        else:
            p.level = 0

    return slide


def add_thank_you_slide(prs):
    """감사 슬라이드 추가"""
    slide = prs.slides.add_slide(prs.slide_layouts[0])

    title_shape = slide.shapes.title
    subtitle_shape = slide.placeholders[1]

    title_shape.text = "감사합니다"
    subtitle_shape.text = "Questions?"

    # 스타일링
    title_frame = title_shape.text_frame
    title_frame.paragraphs[0].font.size = Pt(54)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(0, 51, 102)

    return slide


def create_4c_presentation(title, connect, concept, practice, conclusion, output_file, template_file=None):
    """4C 구조 기반 프레젠테이션 생성"""
    # 템플릿 파일이 제공되면 템플릿 로드, 아니면 빈 프레젠테이션 생성
    if template_file:
        try:
            prs = Presentation(template_file)
            print(f"[INFO] Using template: {template_file}")
        except Exception as e:
            print(f"[WARNING] Failed to load template '{template_file}': {e}")
            print("[INFO] Creating presentation without template")
            prs = Presentation()
            prs.slide_width = Inches(10)
            prs.slide_height = Inches(7.5)
    else:
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)

    # 1. 제목 슬라이드
    add_title_slide(prs, title)

    # 2. Connect 슬라이드
    add_4c_slide(prs, 'Connect', '1. Connect (연결)', connect, '🔗')

    # 3. Concept 슬라이드
    add_4c_slide(prs, 'Concept', '2. Concept (개념)', concept, '💡')

    # 4. Concrete Practice 슬라이드
    add_4c_slide(prs, 'Concrete', '3. Concrete Practice (구체화)', practice, '✏️')

    # 5. Conclusion 슬라이드
    add_4c_slide(prs, 'Conclusion', '4. Conclusion (정리)', conclusion, '🎯')

    # 6. 감사 슬라이드
    add_thank_you_slide(prs)

    # 저장
    prs.save(output_file)
    try:
        print(f"✅ PowerPoint 파일이 생성되었습니다: {output_file}")
        print(f"   총 {len(prs.slides)} 슬라이드가 생성되었습니다.")
    except UnicodeEncodeError:
        # Windows 콘솔 인코딩 문제 대응
        print(f"[SUCCESS] PowerPoint file created: {output_file}")
        print(f"   Total {len(prs.slides)} slides generated.")


def main():
    parser = argparse.ArgumentParser(
        description='4C 교육 구조 기반 PowerPoint 생성',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  python generate_4c_ppt.py --title "Python 기초" \\
    --connect "프로그래밍을 배워본 적이 있나요?" \\
    --concept "Python은 배우기 쉬운 프로그래밍 언어입니다" \\
    --practice "Hello World를 출력해봅시다" \\
    --conclusion "오늘 Python의 기초를 배웠습니다" \\
    --output python_basics.pptx
        """
    )

    parser.add_argument('--title', required=True, help='프레젠테이션 제목')
    parser.add_argument('--connect', required=True, help='Connect: 학습자와 연결할 내용')
    parser.add_argument('--concept', required=True, help='Concept: 핵심 개념')
    parser.add_argument('--practice', required=True, help='Concrete Practice: 실습/예제')
    parser.add_argument('--conclusion', required=True, help='Conclusion: 요약/정리')
    parser.add_argument('--template', help='사용할 PPTX 템플릿 파일 경로')
    parser.add_argument('--output', default='4c_presentation.pptx', help='출력 파일명 (기본: 4c_presentation.pptx)')

    args = parser.parse_args()

    # PPT 생성
    create_4c_presentation(
        title=args.title,
        connect=args.connect,
        concept=args.concept,
        practice=args.practice,
        conclusion=args.conclusion,
        output_file=args.output,
        template_file=args.template
    )


if __name__ == '__main__':
    main()
