import asyncio
import edge_tts
import threading
import queue
import tempfile
import os
from playsound import playsound

speech_queue = queue.Queue()

# 🔥 voix française (tu peux changer)
VOICE = "fr-FR-DeniseNeural"


def _play_audio(file_path):
    playsound(file_path)
    os.remove(file_path)


async def _synthesize(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        file_path = f.name

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(file_path)

    _play_audio(file_path)


def _worker():
    while True:
        text = speech_queue.get()

        if text is None:
            break

        try:
            asyncio.run(_synthesize(text))
        except Exception as e:
            print("Erreur TTS:", e)

        speech_queue.task_done()


threading.Thread(target=_worker, daemon=True).start()


def speak(text):
    print("SPEAK:", text)
    speech_queue.put(text)