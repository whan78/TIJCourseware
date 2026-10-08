#!/usr/bin/env python3
"""
Build courseware player for both Java OOP Foundations and Java Advanced Topics.
Creates:
  - courseware_player/index.html (Foundations - 120 slides)
  - courseware_advanced/index.html (Advanced - 139 slides)
  - index.html (course selection menu)
"""

import json
import re
from pathlib import Path

HERE = Path(__file__).parent

def load_narration(nar_dir, count):
    """Load bilingual narration files."""
    narr_en = []
    narr_zh = []
    for i in range(1, count + 1):
        f = Path(nar_dir) / f'{i:03d}.txt'
        if not f.exists():
            narr_en.append('')
            narr_zh.append('')
            continue
        content = f.read_text(encoding='utf-8').strip()
        m = re.split(r'\n\n--- Chinese Annotation ---\n', content, maxsplit=1)
        en = m[0].strip()
        zh = m[1].strip() if len(m) > 1 else ''
        narr_en.append(en)
        narr_zh.append(zh)
    return narr_en, narr_zh


def build_player(narr_en, narr_zh, output_file,
                 title, header_tag, overlay_title, overlay_subtitle,
                 total_slides, course_name):
    """Build the HTML player for a course."""

    template = (HERE / 'player_template.html').read_text(encoding='utf-8')

    html = template
    html = html.replace('__NARRATIONS_EN__', json.dumps(narr_en, ensure_ascii=False))
    html = html.replace('__NARRATIONS_ZH__', json.dumps(narr_zh, ensure_ascii=False))
    html = html.replace('__TITLE__', title)
    html = html.replace('__HEADER_TAG__', header_tag)
    html = html.replace('__OVERLAY_TITLE__', overlay_title)
    html = html.replace('__OVERLAY_SUBTITLE__', overlay_subtitle)
    html = html.replace('const N = 120;', f'const N = {total_slides};')
    html = html.replace('max="120"', f'max="{total_slides}"')
    html = html.replace('1 / 120', f'1 / {total_slides}')
    html = html.replace('120 slides', f'{total_slides} slides')
    html = html.replace('all 120 slides', f'all {total_slides} slides')

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')
    print(f'Built: {output_file} ({len(html)} bytes, {total_slides} slides)')


def build_menu():
    """Build the course selection menu."""
    menu = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Java Programming Courses</title>
<style>
  :root {
    --primary: #1E4FA8; --deep: #0E3F8C; --bg: #F4F7FB; --ink: #1A2233;
    --muted: #8B97A8; --panel: #FFFFFF; --line: #D6DCE5;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { height: 100%; background: var(--bg); font-family: 'Segoe UI', sans-serif; color: var(--ink); overflow: hidden; }
  #stage { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; gap: 40px; flex-wrap: wrap; }
  .course-card { background: #fff; border-radius: 16px; box-shadow: 0 8px 40px rgba(14,63,140,.15); width: 320px; padding: 32px 28px; text-align: center; transition: transform .3s, box-shadow .3s; cursor: pointer; }
  .course-card:hover { transform: translateY(-8px); box-shadow: 0 16px 60px rgba(14,63,140,.25); }
  .course-card .icon { font-size: 64px; margin-bottom: 16px; }
  .course-card h1 { font-size: 28px; font-weight: 600; margin-bottom: 12px; color: var(--ink); }
  .course-card p { color: var(--muted); font-size: 15px; line-height: 1.5; margin-bottom: 24px; }
  .course-card .btn { display: inline-block; padding: 12px 32px; background: var(--primary); color: #fff; border-radius: 8px; font-size: 16px; font-weight: 600; text-decoration: none; transition: background .2s; }
  .course-card .btn:hover { background: var(--deep); }
  #footer { position: fixed; bottom: 24px; width: 100%; text-align: center; color: var(--muted); font-size: 13px; }
</style>
</head>
<body>
<div id="stage">
  <div class="course-card" onclick="location.href='courseware_player/index.html'">
    <div class="icon">📚</div>
    <h1>Java OOP Foundations</h1>
    <p>Object-Oriented Programming Basics — Classes, Inheritance, Polymorphism, and Design Patterns</p>
    <div class="btn">Start Course →</div>
  </div>
  <div class="course-card" onclick="location.href='courseware_advanced/index.html'">
    <div class="icon">🔧</div>
    <h1>Java Advanced Topics</h1>
    <p>Inner Classes, Collections, Exceptions, Generics, I/O, and Concurrency</p>
    <div class="btn">Start Advanced →</div>
  </div>
</div>
<div id="footer">Thinking in Java 4e • 120 slides Foundations • 139 slides Advanced</div>
</body>
</html>'''

    (HERE / 'index.html').write_text(menu, encoding='utf-8')
    print('Built course selection menu: index.html')


def main():
    # Build Foundations course (120 slides)
    en, zh = load_narration('narration', 120)
    build_player(en, zh, 'courseware_player/index.html',
                 'Java Programming: Object-Oriented Foundations',
                 'Java Programming · Object-Oriented Foundations · Thinking in Java 4e (Ch 1–9)',
                 'Java Programming:<br>Object-Oriented Foundations',
                 'Narrated courseware · 120 slides · ≈ 80 minutes · auto-plays with voice-over',
                 120, 'Foundations')

    # Build Advanced course (139 slides)
    en2, zh2 = load_narration('narration_advanced', 139)
    build_player(en2, zh2, 'courseware_advanced/index.html',
                 'Java Advanced Topics',
                 'Java Advanced Topics · Thinking in Java 4e (Ch 10–22)',
                 'Java Advanced Topics',
                 'Narrated courseware · 139 slides · auto-plays with voice-over',
                 139, 'Advanced')

    # Build course selection menu
    build_menu()

    print('\nDone! Open index.html to select a course.')


if __name__ == '__main__':
    main()