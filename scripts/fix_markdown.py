#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 파일 형식 자동 수정 스크립트

사용법:
    python fix_markdown.py --md "파일경로.md" --output "수정본.md"
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

def fix_markdown(md_path, output_path):
    """Markdown 파일의 형식 문제를 자동으로 수정합니다."""

    safe_print(f"[INFO] 파일 읽기: {md_path}")

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
    fixed_lines = []
    fixes_count = 0

    in_4c_section = False
    current_section = None

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # 4C 섹션 감지
        if line_stripped.startswith('## ') and line_stripped.split()[1] in ['Connect', 'Concept', 'Concrete', 'Conclusion']:
            in_4c_section = True
            current_section = line_stripped.split()[1]
            fixed_lines.append(line)
            continue

        # 다음 섹션으로 넘어가면 4C 섹션 종료
        if line_stripped.startswith('## ') and in_4c_section:
            in_4c_section = False
            current_section = None
            fixed_lines.append(line)
            continue

        # 4C 섹션 내에서 필드가 합쳐진 줄 감지 및 수정
        if in_4c_section and line_stripped:
            # 한 줄에 여러 필드가 있는지 확인
            field_patterns = [
                (r'(time:\s*[^t]+?)\s+(title:)', r'\1\n\2'),
                (r'(title:\s*[^m]+?)\s+(main:)', r'\1\n\2'),
                (r'(main:\s*[^s]+?)\s+(sub:)', r'\1\n\2'),
                (r'(main:\s*[^a]+?)\s+(activity:)', r'\1\n\2'),
                (r'(sub:\s*[^a]+?)\s+(activity:)', r'\1\n\2'),
            ]

            modified = False
            for pattern, replacement in field_patterns:
                if re.search(pattern, line):
                    # 필드가 합쳐진 줄 발견
                    fixed_line = line
                    # 각 필드를 분리
                    parts = []

                    # time: 추출
                    time_match = re.search(r'(time:\s*[^\s]+)', line)
                    if time_match:
                        parts.append(time_match.group(1))

                    # title: 추출
                    title_match = re.search(r'title:\s*([^m]+?)(?:\s+main:|$)', line)
                    if title_match:
                        parts.append('title: ' + title_match.group(1).strip())

                    # main: 추출
                    main_match = re.search(r'main:\s*([^s]+?)(?:\s+sub:|$)', line)
                    if main_match:
                        parts.append('main: ' + main_match.group(1).strip())

                    # sub: 추출
                    sub_match = re.search(r'sub:\s*(.+?)(?:\s+activity:|$)', line)
                    if sub_match:
                        sub_content = sub_match.group(1).strip()
                        if sub_content:
                            parts.append('sub: ' + sub_content)
                        else:
                            parts.append('sub:')

                    # activity: 추출
                    activity_match = re.search(r'activity:\s*(.+?)$', line)
                    if activity_match:
                        activity_content = activity_match.group(1).strip()
                        if activity_content:
                            parts.append('activity: ' + activity_content)
                        else:
                            parts.append('activity: |')

                    if len(parts) > 1:
                        # 여러 필드가 합쳐져 있었음
                        fixed_lines.extend(parts)
                        fixes_count += 1
                        modified = True
                        safe_print(f"  [FIX] 라인 {i+1}: {len(parts)}개 필드 분리")
                        break

            if not modified:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    # 결과 저장
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(fixed_lines))
        safe_print(f"\n[SUCCESS] 수정된 파일 저장: {output_path}")
        safe_print(f"  총 {fixes_count}개 라인 수정됨")
        return True
    except Exception as e:
        safe_print(f"[ERROR] 파일 저장 실패: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='4C 교육 Markdown 파일의 형식 문제를 자동으로 수정합니다.'
    )
    parser.add_argument(
        '--md',
        required=True,
        help='수정할 Markdown 파일 경로'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='수정된 파일을 저장할 경로'
    )

    args = parser.parse_args()

    success = fix_markdown(args.md, args.output)

    if success:
        safe_print("\n[INFO] 수정 완료! 이제 다음 명령으로 검증하세요:")
        safe_print(f'  python validate_markdown.py --md "{args.output}"')

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
