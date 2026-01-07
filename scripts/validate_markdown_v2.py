#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 파일 형식 검증 스크립트 v2 (강화 버전)

사용법:
    python validate_markdown_v2.py --md "파일경로.md"
"""

import argparse
import re
import sys

def safe_print(text):
    """Windows 콘솔에서 안전하게 출력"""
    try:
        print(text)
    except UnicodeEncodeError:
        ascii_text = text.encode('ascii', 'replace').decode('ascii')
        print(ascii_text)

def validate_markdown(md_path):
    """Markdown 파일 형식을 검증합니다."""

    safe_print(f"[INFO] 파일 검증 중: {md_path}")

    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        safe_print(f"[ERROR] 파일을 찾을 수 없습니다: {md_path}")
        return False
    except Exception as e:
        safe_print(f"[ERROR] 파일 읽기 실패: {e}")
        return False

    lines = content.split('\n')
    errors = []
    warnings = []

    # 섹션별 검증
    in_4c_section = False
    current_section = None
    section_start_line = 0
    section_fields = {}

    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()

        # 4C 섹션 시작 감지
        if line_stripped.startswith('## ') and line_stripped.split()[1] in ['Connect', 'Concept', 'Concrete', 'Conclusion']:
            # 이전 섹션 검증
            if in_4c_section and current_section:
                validate_section(current_section, section_fields, section_start_line, errors, warnings)

            # 새 섹션 시작
            in_4c_section = True
            current_section = line_stripped.split()[1]
            section_start_line = i
            section_fields = {}
            continue

        # 다음 섹션으로 넘어가면 4C 섹션 종료
        if line_stripped.startswith('## ') and in_4c_section:
            # 이전 섹션 검증
            validate_section(current_section, section_fields, section_start_line, errors, warnings)
            in_4c_section = False
            current_section = None
            section_fields = {}
            continue

        # 4C 섹션 내에서 필드 수집
        if in_4c_section:
            # 한 줄에 여러 필드가 있는지 검사
            field_count = sum([
                1 if 'time:' in line else 0,
                1 if 'title:' in line else 0,
                1 if 'main:' in line else 0,
                1 if 'sub:' in line else 0,
                1 if 'activity:' in line else 0,
            ])

            if field_count > 1:
                errors.append({
                    'line': i,
                    'section': current_section,
                    'content': line.strip()[:80],
                    'message': f"한 줄에 {field_count}개의 필드가 합쳐져 있습니다"
                })

            # 필드 파싱
            if line.startswith('time:'):
                section_fields['time'] = i
            elif line.startswith('title:'):
                section_fields['title'] = i
            elif line.startswith('main:'):
                section_fields['main'] = i
            elif line.startswith('sub:'):
                section_fields['sub'] = i
            elif line.startswith('activity:'):
                section_fields['activity'] = i
            # 고아 리스트 체크 (sub: 또는 activity: 없이 - 시작)
            elif line.strip().startswith('-') and 'sub' not in section_fields and 'activity' not in section_fields:
                warnings.append({
                    'line': i,
                    'section': current_section,
                    'message': f"리스트 항목이 있지만 'sub:' 또는 'activity:' 필드가 없습니다"
                })

    # 마지막 섹션 검증
    if in_4c_section and current_section:
        validate_section(current_section, section_fields, section_start_line, errors, warnings)

    # 결과 출력
    safe_print("\n" + "="*60)

    if errors:
        safe_print(f"[ERROR] {len(errors)}개의 오류 발견\n")
        for error in errors:
            safe_print(f"  라인 {error['line']} ({error['section']} 섹션):")
            safe_print(f"    {error['message']}")
            if 'content' in error:
                safe_print(f"    내용: {error['content']}")
            safe_print("")

    if warnings:
        safe_print(f"[WARNING] {len(warnings)}개의 경고\n")
        for warning in warnings:
            safe_print(f"  라인 {warning['line']} ({warning['section']} 섹션):")
            safe_print(f"    {warning['message']}")
            safe_print("")

    if not errors and not warnings:
        safe_print("[SUCCESS] 검증 통과! 형식이 올바릅니다.")
        safe_print("="*60)
        return True
    else:
        safe_print("="*60)
        if errors:
            safe_print("\n[FIX] 수정 방법:")
            safe_print("  각 필드(time:, title:, main:, sub:)를 별도의 줄에 작성하세요.")
            safe_print("\n  [X] 잘못된 예:")
            safe_print("    time: 20분 title: 제목 main: 내용")
            safe_print("\n  [O] 올바른 예:")
            safe_print("    time: 20분")
            safe_print("    title: 제목")
            safe_print("    main: 내용")
            safe_print("")
        if warnings:
            safe_print("\n[TIP] 리스트 항목은 sub: 또는 activity: 필드 아래에 작성하세요.")
            safe_print("")
        return False

def validate_section(section_type, fields, start_line, errors, warnings):
    """섹션별 필수 필드 체크"""
    required_fields = {
        'Connect': ['time', 'title', 'main', 'sub'],
        'Concept': ['time', 'title', 'main', 'sub'],
        'Concrete': ['time', 'title', 'main', 'activity'],
        'Conclusion': ['time', 'title', 'main', 'sub'],
    }

    section_name = section_type
    if section_type.startswith('Concrete'):
        section_name = 'Concrete'

    if section_name in required_fields:
        for field in required_fields[section_name]:
            if field not in fields:
                warnings.append({
                    'line': start_line,
                    'section': section_type,
                    'message': f"필수 필드 '{field}:'가 누락되었습니다"
                })

def main():
    parser = argparse.ArgumentParser(
        description='4C 교육 Markdown 파일 형식을 검증합니다 (강화 버전).'
    )
    parser.add_argument(
        '--md',
        required=True,
        help='검증할 Markdown 파일 경로'
    )

    args = parser.parse_args()

    success = validate_markdown(args.md)

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
