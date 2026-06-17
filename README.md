# 🎙️ Eduport Whisper Transcription & Translation Pipeline

> Automatically transcribe Malayalam lecture audio and generate subtitles in English, Hindi, and Tamil using OpenAI Whisper and Google Translate — fully local, no paid API required.

---

## 📌 Overview

This pipeline was built for **Eduport** to convert Malayalam lecture recordings into multi-language subtitle files (`.srt`) for use in VLC Media Player or any video player.

```
┌─────────────────────────────────────────────────────────────────┐
│                    EDUPORT WHISPER PIPELINE                     │
│                                                                 │
│   lecture.mp3  ──►  [Whisper large-v3]  ──►  English SRT/TXT   │
│                                                    │            │
│                              ┌─────────────────────┤            │
│                              ▼                     ▼            │
│                         Hindi SRT            Tamil SRT          │
│                     [Google Translate]   [Google Translate]     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 How It Works

### Stage 1 — Speech to Text (Whisper)

```
┌──────────────┐     ┌─────────────────────────────────────┐
│  lecture.mp3  │────►│         faster-whisper              │
│  (Malayalam)  │     │                                     │
└──────────────┘     │  1. Splits audio into 30s chunks    │
                     │  2. Converts to mel spectrogram      │
                     │  3. Transformer model reads it       │
                     │  4. Outputs English text + timestamps│
                     └──────────────┬──────────────────────┘
                                    │
                     ┌──────────────▼──────────────────────┐
                     │  lecture_translate_ml.srt  (English) │
                     │  lecture_translate_ml.txt  (English) │
                     └─────────────────────────────────────┘
```

### Stage 2 — Translation (Google Translate)

```
┌──────────────────────────┐
│  lecture_translate_ml.srt │  (English subtitles, 1056 blocks)
└────────────┬─────────────┘
             │
     ┌───────┴────────┐
     ▼                ▼
┌─────────┐      ┌─────────┐
│  Hindi  │      │  Tamil  │
│   (hi)  │      │   (ta)  │
└────┬────┘      └────┬────┘
     │                │
     ▼                ▼
lecture_translate_ml_hi.srt
lecture_translate_ml_ta.srt
```

---

## 🔧 Tools & Models Used

### faster-whisper
| Property | Detail |
|---|---|
| **Library** | `faster-whisper` by SYSTRAN |
| **Based on** | OpenAI Whisper |
| **Model used** | `large-v3` |
| **Model size** | ~3GB, 1.5 billion parameters |
| **Why faster-whisper?** | 4× faster than original Whisper, lower RAM usage |
| **Why large-v3?** | Best accuracy for Indian languages, 99 language support |
| **Runs on** | CPU (no GPU required) |
| **Internet needed?** | Only for first model download |
| **Model source** | [HuggingFace — Systran/faster-whisper-large-v3](https://huggingface.co/Systran/faster-whisper-large-v3) |
| **Original Whisper** | [github.com/openai/whisper](https://github.com/openai/whisper) |

### deep-translator
| Property | Detail |
|---|---|
| **Library** | `deep-translator` |
| **Backend** | Google Translate (free tier) |
| **API key needed?** | No |
| **Why this library?** | Free, no signup, handles batch subtitle translation |
| **Limitation** | Whisper `translate` task only outputs English — this covers Hindi/Tamil |

### Whisper Model Comparison
| Model | Size | Quality | Speed on CPU |
|---|---|---|---|
| `tiny` | 39M params | ⭐ | Very fast |
| `base` | 74M params | ⭐⭐ | Fast |
| `small` | 244M params | ⭐⭐⭐ | Moderate |
| `medium` | 769M params | ⭐⭐⭐⭐ | Slow |
| `large-v3` | 1.5B params | ⭐⭐⭐⭐⭐ | ~30–60 min for 25min audio |

> **We use `large-v3`** — best accuracy for Malayalam, worth the wait.

---

## 📁 Project Structure

```
eduport-whisper/
│
├── transcribe.py          # Stage 1: Audio → English SRT + TXT
├── translate_srt.py       # Stage 2: English SRT → Hindi/Tamil SRT
│
├── whisper-env/           # Python virtual environment (not committed)
│
├── lecture.mp3            # Input audio (not committed)
├── lecture_translate_ml.srt     # English subtitles (generated)
├── lecture_translate_ml.txt     # English transcript (generated)
├── lecture_translate_ml_hi.srt  # Hindi subtitles (generated)
└── lecture_translate_ml_ta.srt  # Tamil subtitles (generated)
```

---

## 🚀 Setup & Usage

### 1. Create Python Virtual Environment

```bash
python3 -m venv whisper-env
```

### 2. Install Dependencies

```bash
whisper-env/bin/pip install faster-whisper deep-translator
```

### 3. Transcribe & Translate to English

```bash
whisper-env/bin/python transcribe.py lecture.mp3 --task translate --model large-v3
```

**Output:**
- `lecture_translate_ml.srt` — English subtitles for VLC
- `lecture_translate_ml.txt` — English plain transcript

### 4. Generate Hindi Subtitles

```bash
whisper-env/bin/python translate_srt.py lecture_translate_ml.srt --lang hi
```

### 5. Generate Tamil Subtitles

```bash
whisper-env/bin/python translate_srt.py lecture_translate_ml.srt --lang ta
```

### Other Supported Languages

```bash
# Telugu
whisper-env/bin/python translate_srt.py lecture_translate_ml.srt --lang te

# Kannada
whisper-env/bin/python translate_srt.py lecture_translate_ml.srt --lang kn

# Malayalam (back-translate)
whisper-env/bin/python translate_srt.py lecture_translate_ml.srt --lang ml
```

---

## 🎬 Using Subtitles in VLC

```
Method 1 (Auto):
  • Rename .srt to match your video filename
  • Place in same folder → VLC loads automatically

Method 2 (Manual):
  • Open VLC → Subtitle menu
  • → Add Subtitle File
  • → Select your .srt file
```

---

## ⚙️ CLI Reference

### transcribe.py

```
Usage: whisper-env/bin/python transcribe.py <audio> [options]

Options:
  --model     Whisper model: tiny, base, small, medium, large-v3 (default: base)
  --task      transcribe (keep original language) | translate (→ English)
  --language  Force source language: hi, ta, ml, en ...
  --output    Custom output file path
```

### translate_srt.py

```
Usage: whisper-env/bin/python translate_srt.py <srt_file> --lang <code>

Language codes:
  hi → Hindi
  ta → Tamil
  te → Telugu
  ml → Malayalam
  kn → Kannada
  bn → Bengali
  fr → French
  de → German
```

---

## 🗑️ Cleanup

Everything is inside the virtual environment. To remove all installed packages:

```bash
rm -rf whisper-env/
```

No system packages are affected.

---

## 📊 Performance (Tested on Intel i5, Ubuntu)

| Task | Model | Time |
|---|---|---|
| 25 min Malayalam audio → English | `base` | ~8 min |
| 25 min Malayalam audio → English | `large-v3` | ~45 min |
| English SRT → Hindi (1056 blocks) | Google Translate | ~3 min |
| English SRT → Tamil (1056 blocks) | Google Translate | ~3 min |

---

## 🏗️ Architecture Diagram

```
                        ┌──────────────┐
                        │  lecture.mp3  │
                        │  (Malayalam)  │
                        └──────┬───────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │    faster-whisper       │
                  │    model: large-v3      │
                  │    task: translate      │
                  │    device: CPU          │
                  │    compute: int8        │
                  └────────────┬───────────┘
                               │
               ┌───────────────┼───────────────┐
               ▼               ▼               ▼
        ┌────────────┐  ┌────────────┐        ...
        │ English    │  │ English    │
        │ .srt       │  │ .txt       │
        └─────┬──────┘  └────────────┘
              │
    ┌─────────┴──────────┐
    │   deep-translator   │
    │  (Google Translate) │
    └─────────┬──────────┘
              │
    ┌─────────┴──────────┐
    │                     │
    ▼                     ▼
┌────────┐          ┌────────┐
│ Hindi  │          │ Tamil  │
│  .srt  │          │  .srt  │
└────────┘          └────────┘
```

---

## 📦 Dependencies

```txt
faster-whisper==1.2.1
deep-translator==1.11.4
```

---

## 🔗 References

- [OpenAI Whisper](https://github.com/openai/whisper)
- [faster-whisper by SYSTRAN](https://github.com/SYSTRAN/faster-whisper)
- [Whisper large-v3 on HuggingFace](https://huggingface.co/Systran/faster-whisper-large-v3)
- [deep-translator](https://github.com/nidhaloff/deep-translator)

---

*Built for Eduport — converting Malayalam lecture recordings into accessible multi-language subtitles.*
