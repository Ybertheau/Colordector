from detector.voice import speak


class Engine:
    def __init__(self):
        self.clicked = False

    def set_click(self):
        self.clicked = True

    def process(self, color):
        if not self.clicked:
            return

        # reset immédiat
        self.clicked = False

        if color is None:
            return

        speak(f"Je vois du {color}")

    def speak(self, text):
        speak(text)