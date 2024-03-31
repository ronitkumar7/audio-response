from torch.cuda import is_available
from TTS.api import TTS
from os import system, urandom, remove
from os.path import exists
from zipfile import ZipFile

def Generate(yt_url: str, text: str) -> bytes:
    """
    Use YouTube video 'yt_url' as a reference voice.
    Generate audio for 'text' and return it as bytes.
    To play the audio, write the bytes into filename.wav.

    Prerequisites: pip install yt-dlp; have ffmpeg.exe as well.
    """
    fname = urandom(16).hex()
    with ZipFile("ffmpeg.zip", "r") as zf:
        zf.extractall(".")

    system(f"yt-dlp -o {fname} -i {yt_url}")
    if exists(f"{fname}.webm"):
        fin = f"{fname}.webm"
    elif exists(f"{fname}.mp4"):
        fin = f"{fname}.mp4"
    elif exists(f"{fname}.mkv"):
        fin = f"{fname}.mkv"
    system(f"ffmpeg -i {fin} -ss 0 -t 60 {fname}.wav")
    remove(fin)

    device = "cuda" if is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    tts.tts_to_file(
        text=text, speaker_wav=f"{fname}.wav",
        language="en", file_path=f"{fname}.ts.wav"
    )
    remove(f"{fname}.wav")
    remove(f"ffmpeg.exe")