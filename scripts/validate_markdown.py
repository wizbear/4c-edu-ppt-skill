#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 파일 형식 검증 스크립트

사용법:
    python validate_markdown.py --md "파일경로.md"
"""

import argparse
import re
import sys

def safe_print(text):
    """Windows 콘솔에서 안전하게 출력"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 유니코드 문자를 ASCII로 변환
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
    line_num = 0

    # 섹션별 필드 검사
    in_4c_section = False
    current_section = None

    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()

        # 4C 섹션 감지
        if line_stripped.startswith('## ') and line_stripped.split()[1] in ['Connect', 'Concept', 'Concrete', 'Conclusion']:
            in_4c_section = True
            current_section = line_stripped.split()[1]
            continue

        # 다음 섹션으로 넘어가면 4C 섹션 종료
        if line_stripped.startswith('## ') and in_4c_section:
            in_4c_section = False
            current_section = None

        # 4C 섹션 내에서 필드 검사
        if in_4c_section:
            # 한 줄에 여러 필드가 있는지 검사
            field_count = 0
            if 'time:' in line:
                field_count += 1
            if 'title:' in line:
                field_count += 1
            if 'main:' in line:
                field_count += 1
            if 'sub:' in line and not line.strip().startswith('sub:'):
                # sub: 뒤에 다른 내용이 한 줄에 있으면 (리스트 제외)
                pass
            if 'activity:' in line:
                field_count += 1

            if field_count > 1:
                errors.append({
                    'line': i,
                    'section': current_section,
                    'content': line.strip()[:80],
                    'message': f"한 줄에 {field_count}개의 필드가 합쳐져 있습니다"
                })

    # 결과 출력
    safe_print("\n" + "="*60)

    if errors:
        safe_print(f"[ERROR] {len(errors)}개의 오류 발견\n")
        for error in errors:
            safe_print(f"  라인 {error['line']} ({error['section']} 섹션):")
            safe_print(f"    {error['message']}")
            safe_print(f"    내용: {error['content']}")
            safe_print("")

    if warnings:
        safe_print(f"[WARNING] {len(warnings)}개의 경고\n")
        for warning in warnings:
            safe_print(f"  라인 {warning['line']}: {warning['message']}")
            safe_print("")

    if not errors and not warnings:
        safe_print("[SUCCESS] 검증 통과! 형식이 올바릅니다.")
        safe_print("="*60)
        return True
    else:
        safe_print("="*60)
        safe_print("\n[FIX] 수정 방법:")
        safe_print("  각 필드(time:, title:, main:, sub:)를 별도의 줄에 작성하세요.")
        safe_print("\n  [X] 잘못된 예:")
        safe_print("    time: 20분 title: 제목 main: 내용")
        safe_print("\n  [O] 올바른 예:")
        safe_print("    time: 20분")
        safe_print("    title: 제목")
        safe_print("    main: 내용")
        safe_print("")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='4C 교육 Markdown 파일 형식을 검증합니다.'
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
