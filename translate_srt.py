#!/usr/bin/env python3
"""
Translate an existing SRT file to another language.
Usage:
    python translate_srt.py lecture_translate_ml.srt --lang hi   # Hindi
    python translate_srt.py lecture_translate_ml.srt --lang ta   # Tamil
    python translate_srt.py lecture_translate_ml.srt --lang te   # Telugu
    python translate_srt.py lecture_translate_ml.srt --lang ml   # Malayalam
"""

import argparse
import os
import re
import time
from deep_translator import GoogleTranslator

LANG_NAMES = {
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "bn": "Bengali",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
}

SRT_BLOCK = re.compile(
    r"(\d+)\n"
    r"(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n"
    r"([\s\S]*?)(?=\n\n|\Z)",
    re.MULTILINE
)


def translate_srt(input_srt: str, target_lang: str):
    with open(input_srt, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = SRT_BLOCK.findall(content)
    if not blocks:
        print("No subtitle blocks found. Make sure the file is a valid SRT.")
        return

    translator = GoogleTranslator(source="en", target=target_lang)
    lang_name = LANG_NAMES.get(target_lang, target_lang)

    base = os.path.splitext(input_srt)[0]
    out_file = f"{base}_{target_lang}.srt"

    print(f"Translating {len(blocks)} subtitle blocks to {lang_name} ...")

    out_lines = []
    for i, (index, timestamp, text) in enumerate(blocks, 1):
        text = text.strip()
        if text:
            try:
                translated = translator.translate(text)
            except Exception as e:
                print(f"  Block {index} failed: {e} — keeping original")
                translated = text
            time.sleep(0.05)  # avoid rate limiting
        else:
            translated = text

        out_lines.append(f"{index}\n{timestamp}\n{translated}\n")

        if i % 50 == 0:
            print(f"  {i}/{len(blocks)} done ...")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    print(f"\nSaved: {out_file}")
    print(f"Load in VLC: Subtitle → Add Subtitle File → select {os.path.basename(out_file)}")


def main():
    parser = argparse.ArgumentParser(description="Translate SRT subtitles to another language")
    parser.add_argument("srt", help="Input .srt file (English)")
    parser.add_argument(
        "--lang", required=True,
        help="Target language code: hi (Hindi), ta (Tamil), te (Telugu), ml (Malayalam), kn (Kannada) ..."
    )
    args = parser.parse_args()
    translate_srt(args.srt, args.lang)


if __name__ == "__main__":
    main()
