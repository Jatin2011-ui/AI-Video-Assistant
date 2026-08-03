# 🎙️ VidMind AI — AI Video Assistant

> Paste a YouTube link. Get a transcript, summary, action items, key decisions, and a chat interface — powered by Whisper + LLaMA + RAG.

[Python]
[Streamlit]
[LangChain]
[Groq]
[Whisper]

---

## 🚀 What it does

VidMind AI takes any YouTube video or local audio/video file and runs it through a full AI pipeline:

1. **Downloads** audio via `yt-dlp`
2. **Transcribes** speech using OpenAI Whisper (local, offline)
3. **Summarizes** the content using LLaMA 3.1 via Groq
4. **Extracts** action items, key decisions, and open questions
5. **Builds a RAG system** over the transcript using ChromaDB + HuggingFace embeddings
6. **Chat with the video** — ask anything about its content

Supports both **English** and **Hinglish** (via Sarvam AI STT).

---

## 🖥️ UI Preview

| Hero & Input | Results & Chat |
|---|---|
| Dark purple theme, gradient accents | 3-tab layout: Insights / Chat / Transcript |

Built with a custom Streamlit UI — `Syne` display font, card-based layout, live pipeline status.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Audio Download | `yt-dlp` |
| Audio Processing | `pydub` + `ffmpeg` |
| Transcription (English) | OpenAI `Whisper` (local) |
| Transcription (Hinglish) | Sarvam AI `saaras:v2.5` |
| LLM | `LLaMA 3.1 8B` via `Groq` |
| Orchestration | `LangChain` |
| Embeddings | `HuggingFace` — `all-MiniLM-L6-v2` |
| Vector Store | `ChromaDB` |
| UI | `Streamlit` |

---

## 📁 Project Structure

```
ai-video-assistant/
├── app.py                  # Streamlit UI
├── main.py                 # CLI entry point
├── core/
│   ├── transcriber.py      # Whisper + Sarvam transcription
│   ├── summarizer.py       # LangChain summarization chain
│   ├── extractor.py        # Action items, decisions, questions
│   ├── rag_engine.py       # RAG chain + Q&A
│   └── vector_store.py     # ChromaDB vector store
├── utils/
│   └── audio_processor.py  # yt-dlp download + pydub chunking
├── .streamlit/
│   └── config.toml         # Streamlit config
├── requirements.txt
└── .env                    # API keys (not committed)
```

---

## ⚡ Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/Jatin2011-ui/ai-video-assistant.git
cd ai-video-assistant
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key
SARVAM_API_KEY=your_sarvam_api_key        # only needed for Hinglish
WHISPER_MODEL=small                        # tiny / base / small / medium
```

Get your keys:
- **Groq** → [console.groq.com](https://console.groq.com)
- **Sarvam** → [sarvam.ai](https://sarvam.ai) (optional, Hinglish only)

### 5. Install ffmpeg (required for audio processing)

```bash
# Windows (via winget)
winget install ffmpeg

# Mac
brew install ffmpeg
```

### 6. Run the app
```bash
streamlit run app.py
```

---

## 🖥️ CLI Usage

If you prefer the terminal over the UI:

```bash
python main.py
```

```
Enter youtube video URL or local file path: https://youtube.com/watch?v=...
Language (English/Hinglish): English
```

---

## 🔧 Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | — | Required. Groq API key for LLaMA |
| `SARVAM_API_KEY` | — | Optional. Only for Hinglish transcription |
| `WHISPER_MODEL` | `small` | Whisper model size (`tiny`/`base`/`small`/`medium`) |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace embedding model |

**Whisper model tradeoff:** `tiny` is fastest, `medium` is most accurate. `small` is the recommended balance for CPU.

---

## 📦 Requirements

```
yt-dlp
pydub
openai-whisper
langchain
langchain-groq
langchain-huggingface
langchain-chroma
langchain-text-splitters
langchain-core
chromadb
sentence-transformers
python-dotenv
streamlit
requests
```

---

## 👨‍💻 Author

**Jatin Prabhakar**
B.Tech CSE, Batch 2027 — Bharati Vidyapeeth's College of Engineering, New Delhi
