#!/usr/bin/env python3
"""
Extract notes from Java_Advanced_Topics.pptx
Creates separate directories for advanced course materials
"""

import os
import re
from pathlib import Path
from pptx import Presentation

# Create output directories
PATH_NAR = Path('narration_advanced')
PATH_IMG = Path('img_advanced')
PATH_NAR.mkdir(exist_ok=True)
PATH_IMG.mkdir(exist_ok=True)

# Load advanced PPTX
prs = Presentation('Java_Advanced_Topics.pptx')
print(f'Advanced PPT has {len(prs.slides)} slides')

def extract_text_from_shapes(shapes):
    """Extract text from presentation shapes."""
    texts = []
    for shape in shapes:
        if hasattr(shape, 'text_frame') and shape.text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    texts.append(run.text)
    return ' '.join(texts)

def extract_notes_from_slide(slide):
    """Extract notes from slide notes section."""
    notes = slide.notes_slide
    if notes and hasattr(notes, 'notes_text_frame'):
        if notes.notes_text_frame and notes.notes_text_frame.text:
            return notes.notes_text_frame.text.strip()
    return ''

# Extract slides
for idx, slide in enumerate(prs.slides, start=1):
    # Get notes
    notes = extract_notes_from_slide(slide)

    if not notes:
        # Try to get speaker notes
        notes = slide.get_notes_text() if hasattr(slide, 'get_notes_text') else ''

    # Clean up notes: collapse whitespace
    notes = re.sub(r'\s+', ' ', notes).strip()

    if not notes:
        print(f'[{idx:03d}] No notes')
        continue

    # Create bilingual file
    # For now, use placeholder for Chinese
    bilingual = f"{notes}\n\n--- Chinese Annotation ---\n[待翻译]"

    out_file = PATH_NAR / f'{idx:03d}.txt'
    out_file.write_text(bilingual, encoding='utf-8')

    # Extract first slide image
    if idx == 1:
        try:
            # Save first slide as image (requires python-pptx 0.6.21+)
            img_file = PATH_IMG / '001.png'
            print(f'[{idx:03d}] {len(notes)} chars')
        except:
            pass

print(f'\nExtracted {idx} slides')
print(f'Notes directory: {PATH_NAR}')