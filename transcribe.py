#!/usr/bin/env python3
"""
Transcribe and translate audio using faster-whisper (OpenAI Whisper model).
Usage:
    python transcribe.py lecture.mp3                        # transcribe in original language
    python transcribe.py lecture.mp3 --task translate       # translate to English
    python transcribe.py lecture.mp3 --language hi          # force Hindi transcription
    python transcribe.py lecture.mp3 --model large-v3       # use a larger model
"""

import argparse
import os
from faster_whisper import WhisperModel

SUPPORTED_TASKS = ["transcribe", "translate"]


def format_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def run(audio_path: str, model_name: str, task: str, language: str | None, output_file: str | None):
    print(f"Loading model '{model_name}' ...")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")

    print(f"Running {task} on '{audio_path}' ...")
    segments, info = model.transcribe(
        audio_path,
        task=task,
        language=language,
        beam_size=5,
    )

    detected = info.language
    print(f"Detected language: {detected} (probability {info.language_probability:.2f})")
    print(f"Duration: {info.duration:.1f}s\n")

    collected = []
    for seg in segments:
        line = f"[{seg.start:6.1f}s -> {seg.end:6.1f}s]  {seg.text.strip()}"
        print(line)
        collected.append((seg.start, seg.end, seg.text.strip()))

    # Plain text output
    if output_file is None:
        base = os.path.splitext(audio_path)[0]
        suffix = f"_{task}_{detected}"
        output_file = f"{base}{suffix}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(text for _, _, text in collected))
    print(f"\nSaved plain text: {output_file}")

    # SRT subtitle output (same name, .srt extension)
    srt_file = os.path.splitext(output_file)[0] + ".srt"
    with open(srt_file, "w", encoding="utf-8") as f:
        for i, (start, end, text) in enumerate(collected, 1):
            f.write(f"{i}\n")
            f.write(f"{format_srt_time(start)} --> {format_srt_time(end)}\n")
            f.write(f"{text}\n\n")
    print(f"Saved SRT subtitles: {srt_file}")


def main():
    parser = argparse.ArgumentParser(description="Whisper transcription / translation")
    parser.add_argument("audio", help="Path to audio file (mp3, wav, m4a, …)")
    parser.add_argument(
        "--model", default="base",
        help="Whisper model: tiny, base, small, medium, large-v2, large-v3 (default: base)"
    )
    parser.add_argument(
        "--task", default="transcribe", choices=SUPPORTED_TASKS,
        help="'transcribe' keeps original language; 'translate' converts to English (default: transcribe)"
    )
    parser.add_argument(
        "--language", default=None,
        help="Force source language code, e.g. 'hi' (Hindi), 'ta' (Tamil), 'en' (English). "
             "Leave blank to auto-detect."
    )
    parser.add_argument("--output", default=None, help="Output .txt file path (auto-named if omitted)")
    args = parser.parse_args()

    run(args.audio, args.model, args.task, args.language, args.output)


if __name__ == "__main__":
    main()
