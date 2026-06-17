# 🎙️ Eduport Whisper Pipeline

<p align="center">
  <img src="https://img.shields.io/badge/OpenAI-Whisper_large--v3-412991?style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/faster--whisper-SYSTRAN-00B4D8?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google_Translate-deep--translator-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Language-Malayalam_→_EN_|_HI_|_TA-FF6B35?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Runs_on-CPU_only-34A853?style=for-the-badge&logo=linux&logoColor=white"/>
</p>

> Convert Malayalam lecture audio into multi-language subtitle files (`.srt`) using OpenAI Whisper — runs fully local, zero paid API.

---

## 🗺️ Full Pipeline

```mermaid
flowchart TD
    A([🎵 lecture.mp3\nMalayalam Audio\n25 min]):::input

    A --> B

    subgraph STAGE1 ["⚡ STAGE 1 — Speech Recognition & Translation"]
        B[/"faster-whisper\nmodel: large-v3\ntask: translate\ndevice: CPU · int8"\]:::model
        B --> C([📄 English SRT\n1056 subtitle blocks\nwith timestamps]):::output
        B --> D([📝 English TXT\nPlain transcript]):::output
    end

    C --> E

    subgraph STAGE2 ["🌐 STAGE 2 — Multi-Language Translation"]
        E[/"deep-translator\nGoogle Translate\nFree · No API key"\]:::model
        E --> F([🇮🇳 Hindi SRT\nlecture_translate_ml_hi.srt]):::output
        E --> G([🇮🇳 Tamil SRT\nlecture_translate_ml_ta.srt]):::output
    end

    F --> H([🎬 VLC Media Player\nSubtitle → Add Subtitle File]):::vlc
    G --> H
    C --> H

    classDef input fill:#FF6B35,stroke:#FF6B35,color:#fff,font-weight:bold
    classDef model fill:#412991,stroke:#412991,color:#fff,font-weight:bold
    classDef output fill:#00B4D8,stroke:#0096C7,color:#fff
    classDef vlc fill:#34A853,stroke:#2D9144,color:#fff,font-weight:bold
```

---

## 🔬 Why These Tools?

```mermaid
flowchart LR
    subgraph WHISPER ["🧠 Why faster-whisper over openai-whisper?"]
        W1["openai-whisper\n❌ Slow on CPU\n❌ High RAM\n✅ Original"]:::bad
        W2["faster-whisper\n✅ 4× faster\n✅ Lower RAM\n✅ Same models\n✅ int8 quantized"]:::good
    end

    subgraph MODEL ["📦 Why large-v3?"]
        M1["base · 74M\n⭐ Poor\nFailed for Malayalam"]:::bad
        M2["large-v3 · 1.5B\n⭐⭐⭐⭐⭐ Best\nHandles Malayalam well"]:::good
    end

    subgraph TRANSLATE ["🌐 Why deep-translator?"]
        T1["Whisper translate\n→ English ONLY\n❌ No Hindi/Tamil"]:::bad
        T2["deep-translator\n→ Any language\n✅ Free\n✅ No API key"]:::good
    end

    classDef bad fill:#FF4444,stroke:#CC0000,color:#fff
    classDef good fill:#00C851,stroke:#007E33,color:#fff
```

---

## 🧠 How Whisper Works Internally

```mermaid
flowchart LR
    A([🎵 Audio Input]):::node --> B[Split into\n30s chunks]:::process
    B --> C[Convert to\nMel Spectrogram\nvisual sound repr.]:::process
    C --> D[Transformer\nEncoder reads\nspectrogram]:::process
    D --> E{Task?}:::decision
    E -->|transcribe| F([Original Language\nMalayalam text]):::out1
    E -->|translate| G([English text\n+ timestamps]):::out2

    classDef node fill:#412991,color:#fff,stroke:#412991
    classDef process fill:#00B4D8,color:#fff,stroke:#0096C7
    classDef decision fill:#FF6B35,color:#fff,stroke:#E55A24
    classDef out1 fill:#6C63FF,color:#fff,stroke:#5A52D5
    classDef out2 fill:#34A853,color:#fff,stroke:#2D9144
```

---

## 📊 Model Comparison

```mermaid
xychart-beta
    title "Whisper Model — Parameters vs Quality"
    x-axis ["tiny 39M", "base 74M", "small 244M", "medium 769M", "large-v3 1.5B"]
    y-axis "Quality Score (1-5)" 1 --> 5
    bar [1, 2, 3, 4, 5]
```

| Model | Params | Malayalam Quality | CPU Time (25 min audio) | Used? |
|---|---|---|---|---|
| `tiny` | 39M | ⭐ | ~3 min | ❌ |
| `base` | 74M | ⭐⭐ | ~8 min | ❌ First test, bad output |
| `small` | 244M | ⭐⭐⭐ | ~15 min | ❌ |
| `medium` | 769M | ⭐⭐⭐⭐ | ~30 min | ❌ |
| `large-v3` | 1.5B | ⭐⭐⭐⭐⭐ | ~45 min | ✅ **Final choice** |

---

## ⏱️ Performance (Intel i5, Ubuntu, CPU only)

```mermaid
gantt
    title Pipeline Execution Time
    dateFormat  mm:ss
    axisFormat  %M min

    section Stage 1
    Model download large-v3 ~3GB   :00:00, 10m
    Audio transcription 25min      :10:00, 45m

    section Stage 2
    Translate to Hindi 1056 blocks :55:00, 3m
    Translate to Tamil 1056 blocks :58:00, 3m
```

| Task | Tool | Time |
|---|---|---|
| Download `large-v3` model | HuggingFace (one time) | ~5–10 min |
| Transcribe + translate 25 min audio | faster-whisper CPU | ~45 min |
| Generate Hindi SRT (1056 blocks) | deep-translator | ~3 min |
| Generate Tamil SRT (1056 blocks) | deep-translator | ~3 min |
| **Total end-to-end** | | **~51 min** |

---

## 📤 Output Files

```mermaid
flowchart LR
    A([lecture.mp3]):::input --> B([lecture_translate_ml.srt\n🇬🇧 English\n1056 blocks · 25:23 duration]):::en
    A --> C([lecture_translate_ml.txt\n🇬🇧 English plain text\n1055 lines]):::en
    B --> D([lecture_translate_ml_hi.srt\n🇮🇳 Hindi\n1056 blocks]):::hi
    B --> E([lecture_translate_ml_ta.srt\n🇮🇳 Tamil\n1051 blocks translated\n5 blocks kept in English]):::ta

    classDef input fill:#FF6B35,stroke:#E55A24,color:#fff
    classDef en fill:#412991,stroke:#3A2480,color:#fff
    classDef hi fill:#FF9933,stroke:#E08020,color:#fff
    classDef ta fill:#138808,stroke:#0F6A06,color:#fff
```

---

## 🔗 Model & Library References

| Tool | Repository | Purpose |
|---|---|---|
| **OpenAI Whisper** | [github.com/openai/whisper](https://github.com/openai/whisper) | Original model creator |
| **faster-whisper** | [github.com/SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Faster reimplementation used here |
| **large-v3 weights** | [huggingface.co/Systran/faster-whisper-large-v3](https://huggingface.co/Systran/faster-whisper-large-v3) | Model downloaded from here |
| **deep-translator** | [github.com/nidhaloff/deep-translator](https://github.com/nidhaloff/deep-translator) | Hindi/Tamil translation |

---

## 🗂️ Repository Structure

```
whisper_eduport_testing/
│
├── 📄 transcribe.py          # Stage 1: Audio → English SRT + TXT
├── 📄 translate_srt.py       # Stage 2: English SRT → Hindi / Tamil SRT
├── 📄 .gitignore             # Excludes venv, audio, generated files
└── 📄 README.md              # This file
```

> Audio files, generated `.srt`/`.txt` outputs, and `whisper-env/` are excluded from this repo.

---

<p align="center">
  <i>Built for Eduport · Malayalam lecture transcription pipeline</i>
</p>
