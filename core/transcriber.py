import os
import whisper
import requests
from pydub import AudioSegment

SARVAM_PIECE_SECONDS = 25

WHISPER_MODEL = os.getenv("WHISPER_MODEL","small")

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text-translate"
SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL","saaras:v2.5")

_model = None 

def load_model():
    global _model

    if _model is None:
        print(f"loading whisper model: {WHISPER_MODEL}....")
        _model = whisper.load_model(WHISPER_MODEL)
        print("whisper model loaded successfully.")
    return _model


def transcribe_chunk_whisper(chunk_path: str) -> str:
    model = load_model()
    result = model.transcribe(chunk_path,task="transcribe")
    return result["text"]


def _send_to_sarvam(chunk_path : str) -> str:
    """Sender one <=30 wav file to sarvam model return the transcribed text."""
    headers = {"api-subsription-key": SARVAM_API_KEY}

    with open(chunk_path,"rb") as f:
        files = {"file": (os.path.basename(chunk_path), f,"audio/wav")}
        data = {"model": SARVAM_MODEL, "with_diarization": "false"}
        response = requests.post(
            SARVAM_STT_TRANSLATE_URL,
            headers = headers,
            files = files,
            data = data,
            timeout = 120,
        )

        if not response.ok:
            print(f"\n Sarvam returned {response.status_code}")
            print(f"Response body: {response.text}\n")
            response.raise_for_status()

        return response.json().get("transcript", "")

def transcribe_chunk_sarvam(chunk_path: str) -> str:
    """
    Sarvam sync API only accepts <= 30 audio. we split this chunk into 25 seconds pieces and, send each separately,
    and join the transcrits.
    """
    if not SARVAM_API_KEY:
        raise ValueError("SARVAM_API_KEY is not set in environment / .env")

    audio = AudioSegment.from_wav(chunk_path)
    piece_ms = SARVAM_PIECE_SECONDS * 1000

    full_text = ""
    total_pieces = (len(audio) + piece_ms - 1) //piece_ms

    for i, start in enumerate(range(0,len(audio),piece_ms)):
        piece = audio[start: start + piece_ms]
        piece_path = f"{chunk_path}_sv_{i}.wav"
        piece.export(piece_path, format="wav")

        try:
            print(f" -> sarvam piece{i+1}/{total_pieces}...")
            full_text += _send_to_sarvam(piece_path) + " "
        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return full_text.strip()




def transcribe_chunk(chunk_path: str, language: str ="english") -> str:
    """
    Route one chunk to whisper or sarvam depending on language choice.
    -english -> whisper(local model)
    -hinglish -> sarvam (translates to english while transcribing)
    """ 

    if language.lower() == "hinglish":
        return transcribe_chunk_sarvam(chunk_path)
    return transcribe_chunk_whisper(chunk_path)


def transcribe_all(chunks: list, language: str ="english") -> str:
    full_transcript = ""

    engine = "sarvam AI " if language.lower() == "hinglish" else "whisper"
    print(f"using{engine} for transcription...")

    for i,chunk in enumerate(chunks):
        print(f"Transcribing chunk {i+1}/{len(chunks)}...")

        text = transcribe_chunk(chunk,language=language)

        full_transcript += text + " "

    print("Transcription completed.")

    return full_transcript.strip()
