import pyttsx3
import time

engine = pyttsx3.init()
last_spoken = ""
last_time = 0

def speak(text, delay=2):
    global last_spoken, last_time

    current_time = time.time()

    if text != last_spoken or (current_time - last_time) > delay:
        engine.say(text)
        engine.runAndWait()
        last_spoken = text
        last_time = current_time