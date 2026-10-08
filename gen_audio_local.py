#!/usr/bin/env python3
"""
Generate audio files using local TTS engine (XTTS v2)
This script replaces the edge_tts-based gen_audio.py
"""

import os
import sys
import argparse
from pathlib import Path

# Add the TTS engine to path (one level up from Java_OOP_Foundations)
tts_engine_lib = Path(__file__).parent.parent / '.claude' / 'skills' / 'tts-engine' / 'lib'
sys.path.insert(0, str(tts_engine_lib.resolve()))

from tts_engine import TTS_AVAILABLE, XTTSv2Engine, get_device_name

from pydub import AudioSegment
import tempfile


def wav_to_mp3(wav_path, mp3_path, bitrate='128k'):
    """Convert WAV to MP3 using pydub."""
    try:
        audio = AudioSegment.from_wav(wav_path)
        audio.export(mp3_path, format='mp3', bitrate=bitrate)
        return True
    except Exception as e:
        print(f"  Conversion error: {e}")
        return False


def generate_audio_local(narration_dir='narration', output_dir='courseware_player/audio',
                          speaker=None, start=1, end=120, convert_to_mp3=True, force=False):
    """Generate audio files using local TTS engine."""

    if not TTS_AVAILABLE:
        print("ERROR: TTS library not available")
        print("Install with: pip install TTS")
        return False

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Device: {get_device_name()}")
    print(f"Output directory: {output_dir}")
    print(f"Processing slides {start} to {end}")
    print()

    tts = XTTSv2Engine()

    success_count = 0
    skip_count = 0
    fail_count = 0

    for i in range(start, end + 1):
        txt_file = Path(narration_dir) / f"{i:03d}.txt"

        if not txt_file.exists():
            print(f"[{i}] Skipped - no narration file")
            skip_count += 1
            continue

        text = txt_file.read_text(encoding='utf-8').strip()
        # Remove Chinese annotation section (starts with --- Chinese Annotation ---)
        if '--- Chinese Annotation ---' in text:
            text = text.split('--- Chinese Annotation ---')[0].strip()

        if not text:
            print(f"[{i}] Skipped - empty narration")
            skip_count += 1
            continue

        # Generate WAV file
        wav_path = Path(tempfile.gettempdir()) / f"tts_{i:03d}.wav"
        mp3_path = output_path / f"{i:03d}.mp3"

        # Skip if MP3 already exists and is reasonable size (unless force=True)
        if not force and mp3_path.exists() and mp3_path.stat().st_size > 10000:
            print(f"[{i}] Skipped - existing file > 10KB")
            skip_count += 1
            continue

        try:
            print(f"[{i}] Generating...")
            tts.synthesize(text, str(wav_path), speaker=speaker)

            if convert_to_mp3 and wav_path.exists():
                if wav_to_mp3(str(wav_path), str(mp3_path)):
                    size_kb = mp3_path.stat().st_size / 1024
                    print(f"[{i}] Done - {size_kb:.1f} KB")
                    success_count += 1
                else:
                    print(f"[{i}] Failed - MP3 conversion")
                    fail_count += 1
            elif wav_path.exists():
                # Just copy wav to output if not converting
                size_kb = wav_path.stat().st_size / 1024
                print(f"[{i}] Done (WAV) - {size_kb:.1f} KB")
                success_count += 1

            # Clean up temp
            if wav_path.exists():
                wav_path.unlink()

        except Exception as e:
            print(f"[{i}] FAILED - {e}")
            fail_count += 1

    print()
    print(f"Results: {success_count} generated, {skip_count} skipped, {fail_count} failed")

    # Summary stats
    total_size = sum(f.stat().st_size for f in output_path.glob('*.mp3')) if output_path.exists() else 0
    print(f"Total audio size: {total_size / 1024 / 1024:.1f} MB")

    return fail_count == 0


def main():
    parser = argparse.ArgumentParser(description='Generate local TTS audio for slides')
    parser.add_argument('--narration-dir', default='narration', help='Narration text directory')
    parser.add_argument('--output-dir', default='courseware_player/audio', help='Output audio directory')
    parser.add_argument('--speaker', default=None, help='Speaker name for XTTS')
    parser.add_argument('--start', type=int, default=1, help='Start slide number')
    parser.add_argument('--end', type=int, default=120, help='End slide number')
    parser.add_argument('--no-convert', action='store_true', help='Keep WAV files, don\'t convert to MP3')
    parser.add_argument('--force', action='store_true', help='Force regenerate all files')

    args = parser.parse_args()

    print("=" * 50)
    print("Local TTS Audio Generator")
    print("=" * 50)
    print()

    success = generate_audio_local(
        narration_dir=args.narration_dir,
        output_dir=args.output_dir,
        speaker=args.speaker,
        start=args.start,
        end=args.end,
        convert_to_mp3=not args.no_convert,
        force=args.force
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()