#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md4c - 4C 교육 Markdown 공용 모듈

generate_with_master_layout.py, validate_markdown_v3.py, swap_activity.py 가 공유한다.

제공 기능
- parse_course(path)      : 프론트매터 + 모듈 + 슬라이드 파싱
- load_catalog(path=None) : references/activities.json 로드
- render_activity(slide, catalog) : activity 텍스트 또는 pattern 템플릿 렌더
- parse_minutes("5분")    : 분 단위 정수

Markdown 규격 (v1.1)
---
course: 과정명
audience: 대상
total_time: 120분
outcome: 과정 성과(관찰 가능한 동사)
mode: offline | online | hybrid
group_size: 20
strict: false
---

# 모듈 1: 제목
outcome: 모듈 성과

## Module Start
소개 문장 (20자 이내 권장)

## Connect | Concept | Review | Concrete Practice | Conclusion
time: 5분
title: ...
main: ...
sub: |
  ...
activity: |            # 학습자가 하는 것. 모든 단계에서 선택
  ...
pattern: turn-and-talk  # 카탈로그 ID (선택)
params:                 # 패턴 템플릿 변수 (선택)
  question: ...
alt: wall-writing, standing-survey   # 교환 후보 (선택)
notes: |                # 강사 노트 (선택)
  ...
handout: |              # nice-to-know → 부록 파일 (선택)
  ...
action_plan: ...        # Conclusion 전용 (선택)

## Image / Video / Break 는 v1.0과 동일
"""

import json
import re
import sys
from pathlib import Path

FOUR_C = ['Connect', 'Concept', 'Concrete Practice', 'Conclusion']
LEARNER_SLIDES = FOUR_C + ['Review']
KNOWN_SLIDE_TYPES = LEARNER_SLIDES + ['Module Start', 'Image', 'Video', 'Break']

# 슬라이드 타입 → 카탈로그 stage 키
STAGE_OF = {
    'Connect': 'connect',
    'Concept': 'concept',
    'Review': 'review',
    'Concrete Practice': 'practice',
    'Conclusion': 'conclusion',
}

SCALAR_FIELDS = {'time', 'title', 'main', 'pattern', 'alt', 'action_plan',
                 'image', 'caption', 'video', 'description', 'duration'}
BLOCK_FIELDS = {'sub', 'activity', 'notes', 'handout', 'params'}
ALL_FIELDS = SCALAR_FIELDS | BLOCK_FIELDS

FRONTMATTER_KEYS = {'course', 'audience', 'total_time', 'outcome', 'mode',
                    'group_size', 'strict', 'title', 'subtitle'}


def safe_print(text):
    """Windows 콘솔에서 안전하게 출력"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode('ascii'))


def parse_minutes(value):
    """'5분', '5 min', '5' → 5. 파싱 불가 시 None"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    m = re.search(r'(\d+(?:\.\d+)?)', str(value))
    if not m:
        return None
    return int(round(float(m.group(1))))


class SlideContent:
    """슬라이드 내용 (v1.0 호환: .slide_type, .data)"""

    def __init__(self, slide_type, line_no=0, **kwargs):
        self.slide_type = slide_type
        self.line_no = line_no
        self.data = kwargs

    def get(self, key, default=''):
        return self.data.get(key, default)

    @property
    def stage(self):
        return STAGE_OF.get(self.slide_type)

    @property
    def minutes(self):
        return parse_minutes(self.data.get('time'))

    @property
    def has_learner_action(self):
        """학습자 행동이 기술되어 있는가 (activity 또는 pattern)"""
        return bool(self.data.get('activity') or self.data.get('pattern'))

    def __repr__(self):
        return f"SlideContent({self.slide_type}, {self.data})"


class Module:
    def __init__(self, title, line_no=0):
        self.title = title
        self.line_no = line_no
        self.meta = {}        # outcome 등 모듈 레벨 key: value
        self.slides = []

    @property
    def outcome(self):
        return self.meta.get('outcome', '')

    def __getitem__(self, key):   # v1.0 dict 호환 (module['title'], module['slides'])
        if key == 'title':
            return self.title
        if key == 'slides':
            return self.slides
        raise KeyError(key)

    def __repr__(self):
        return f"Module({self.title}, {len(self.slides)} slides)"


class Course:
    def __init__(self):
        self.frontmatter = {}
        self.modules = []
        self.source = None

    @property
    def title(self):
        return self.frontmatter.get('course') or self.frontmatter.get('title') or ''

    @property
    def mode(self):
        return (self.frontmatter.get('mode') or 'offline').strip().lower()

    @property
    def strict(self):
        return str(self.frontmatter.get('strict', 'false')).strip().lower() in ('true', '1', 'yes')

    @property
    def group_size(self):
        return parse_minutes(self.frontmatter.get('group_size'))

    def learner_slides(self):
        for m in self.modules:
            for s in m.slides:
                if s.slide_type in LEARNER_SLIDES:
                    yield m, s


def _split_field(line):
    """'key: value' → (key, value) / 아니면 None"""
    if ':' not in line or line.startswith((' ', '\t', '-', '#')):
        return None
    key, value = line.split(':', 1)
    key = key.strip()
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
        return None
    return key, value.strip()


def _parse_params_block(text):
    """params 블록 텍스트 → dict"""
    params = {}
    for raw in text.split('\n'):
        raw = raw.strip()
        if not raw or raw.startswith('#'):
            continue
        if ':' in raw:
            k, v = raw.split(':', 1)
            params[k.strip()] = v.strip()
    return params


def _parse_frontmatter(lines):
    """선두 --- 블록 → (dict, 소비한 줄 수)"""
    if not lines or lines[0].strip() != '---':
        return {}, 0
    fm = {}
    for idx in range(1, len(lines)):
        if lines[idx].strip() == '---':
            return fm, idx + 1
        sf = _split_field(lines[idx].strip())
        if sf:
            fm[sf[0]] = sf[1]
    return {}, 0  # 닫는 --- 없음 → 프론트매터 아님


def parse_course(md_file):
    """Markdown 파일 → Course"""
    path = Path(md_file)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')

    course = Course()
    course.source = path
    course.frontmatter, start = _parse_frontmatter(lines)

    current_module = None
    current_slide = None
    current_field = None
    block_lines = []

    def flush_block():
        nonlocal current_field, block_lines
        if current_slide is not None and current_field:
            text = '\n'.join(block_lines).strip('\n')
            if current_field == 'params':
                current_slide.data['params'] = _parse_params_block(text)
            else:
                current_slide.data[current_field] = text.strip()
        current_field = None
        block_lines = []

    def close_slide():
        nonlocal current_slide
        flush_block()
        if current_slide is not None and current_module is not None:
            current_module.slides.append(current_slide)
        current_slide = None

    for i in range(start, len(lines)):
        line = lines[i]
        line_no = i + 1

        # 모듈 시작
        if line.startswith('# ') and not line.startswith('## '):
            close_slide()
            if current_module is not None:
                course.modules.append(current_module)
            current_module = Module(line[2:].strip(), line_no)
            continue

        # 슬라이드 시작
        if line.startswith('## '):
            close_slide()
            current_slide = SlideContent(line[3:].strip(), line_no)
            continue

        # 블록 필드 내용 (들여쓰기 또는 '-' 또는 빈 줄)
        if current_field and (line.startswith(('  ', '\t', '-')) or line.strip() == ''):
            block_lines.append(line.lstrip() if not line.startswith('-') else line)
            continue

        # 모듈 레벨 메타 (슬라이드 시작 전)
        if current_module is not None and current_slide is None:
            sf = _split_field(line)
            if sf:
                current_module.meta[sf[0]] = sf[1]
            continue

        # 슬라이드 필드
        if current_slide is not None:
            sf = _split_field(line)
            if sf:
                flush_block()
                key, value = sf
                if value in ('', '|'):
                    current_field = key
                    block_lines = []
                else:
                    current_slide.data[key] = value
                continue

            if line.strip() in ('', '---'):
                flush_block()
                continue

            # Module Start 본문
            if current_slide.slide_type == 'Module Start' and line.strip():
                current_slide.data.setdefault('content', [])
                current_slide.data['content'].append(line.strip())
                continue

    close_slide()
    if current_module is not None:
        course.modules.append(current_module)

    # 후처리
    for m in course.modules:
        for s in m.slides:
            if s.slide_type == 'Module Start' and isinstance(s.data.get('content'), list):
                s.data['content'] = '\n'.join(s.data['content'])
            if 'alt' in s.data and isinstance(s.data['alt'], str):
                s.data['alt'] = [a.strip() for a in s.data['alt'].split(',') if a.strip()]
            if 'params' in s.data and isinstance(s.data['params'], str):
                s.data['params'] = _parse_params_block(s.data['params'])

    # 슬라이드 없는 첫 모듈 = 과정 제목 (v1.0 예제 호환)
    if course.modules and not course.modules[0].slides and not course.title:
        course.frontmatter.setdefault('course', course.modules[0].title)

    return course


def parse_markdown(md_file):
    """v1.0 호환: modules 리스트(dict 형태) 반환"""
    course = parse_course(md_file)
    return [{'title': m.title, 'slides': m.slides, 'meta': m.meta} for m in course.modules]


# ---------------------------------------------------------------- catalog

def default_catalog_path():
    return Path(__file__).resolve().parent.parent / 'references' / 'activities.json'


def load_catalog(path=None):
    """activities.json → {id: entry}. 없으면 빈 dict"""
    p = Path(path) if path else default_catalog_path()
    if not p.exists():
        return {}
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    entries = data.get('activities', data) if isinstance(data, dict) else data
    return {e['id']: e for e in entries}


class _SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def render_pattern(entry, params=None, minutes=None):
    """카탈로그 항목 템플릿에 params 채우기"""
    params = dict(params or {})
    if minutes is not None:
        params.setdefault('time', f'{minutes}분')
    template = entry.get('template') or entry.get('summary', '')
    return template.format_map(_SafeDict(params)).strip()


def render_activity(slide, catalog=None):
    """
    슬라이드의 학습자 활동 텍스트.
    activity: 가 있으면 그것, 없고 pattern: 이 있으면 템플릿 렌더. 둘 다 없으면 ''.
    """
    text = slide.data.get('activity', '')
    if text:
        return text
    pid = slide.data.get('pattern')
    if pid and catalog and pid in catalog:
        entry = catalog[pid]
        head = entry.get('name_ko') or entry.get('name', pid)
        body = render_pattern(entry, slide.data.get('params'), slide.minutes)
        return f'{head}\n{body}' if body else head
    return ''


def pattern_allowed_in(entry, stage):
    """패턴이 해당 stage에서 허용되는가 → ('native' | 'also_ok' | None)"""
    if stage in entry.get('stages', []):
        return 'native'
    if stage in entry.get('also_ok', []):
        return 'also_ok'
    return None


def missing_params(entry, params):
    """템플릿에 필요한데 params에 없는 키"""
    needed = set(re.findall(r'\{([A-Za-z_][A-Za-z0-9_]*)\}', entry.get('template', '')))
    needed.discard('time')
    return sorted(needed - set((params or {}).keys()))


if __name__ == '__main__':
    # 간단 덤프
    if len(sys.argv) < 2:
        print('usage: md4c.py course.md')
        sys.exit(1)
    c = parse_course(sys.argv[1])
    safe_print(f'frontmatter: {c.frontmatter}')
    for m in c.modules:
        safe_print(f'# {m.title}  meta={m.meta}')
        for s in m.slides:
            safe_print(f'  ## {s.slide_type} L{s.line_no} {list(s.data.keys())}')
