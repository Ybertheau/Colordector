import pyttsx3
import threading
import queue

engine = pyttsx3.init()
speech_queue = queue.Queue()

def _speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break

        engine.say(text)
        engine.runAndWait()

        speech_queue.task_done()

#  Thread unique qui tourne en boucle
threading.Thread(target=_speech_worker, daemon=True).start()


def speak(text):
    speech_queue.put(text)