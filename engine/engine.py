from detector.voice import speak


class Engine:
    def __init__(self):
        self.clicked = False
        self.show_debug = True
        self.last_spoken = None

    def set_click(self):
        self.clicked = True

    def toggle_debug(self):
        self.show_debug = not self.show_debug

    def process(self, data):

        if not self.clicked:
            return

        self.clicked = False

        if not data:
            return

        color = data.get("color")
        obj = data.get("object")
        shape = data.get("shape")

        sentence = self.build_sentence(obj, color, shape)

        if sentence and sentence != self.last_spoken:
            speak(sentence)
            self.last_spoken = sentence

    def build_sentence(self, obj, color, shape):

        # priorité logique
        main = obj or shape

        parts = []

        if main:
            parts.append(main)

        if color:
            parts.append(color)

        if parts:
            return " ".join(parts)

        return None