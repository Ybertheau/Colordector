import cv2
import time

from detector.camera import init_camera, get_frame
from detector.color import get_center_color, get_color_name
from engine.engine import Engine
from utils.config import CAMERA_INDEX

# Engine = logique centrale
engine = Engine()


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("CLICK OK")
        engine.set_click()


def main():
    cap = init_camera(CAMERA_INDEX)

    if cap is None:
        print("Programme arrêté.")
        return

    cv2.namedWindow("ColorDetector")
    cv2.setMouseCallback("ColorDetector", on_mouse)

    print("Clique dans la fenêtre pour entendre la couleur")

    engine.speak("Application prête")

    while True:
        frame = get_frame(cap)

        if frame is None:
            time.sleep(1)
            continue

        # Analyse couleur
        rgb, h, s, v = get_center_color(frame)

        current_color = get_color_name(
            rgb,
            h,
            s,
            v
        )

        # Engine gère la logique
        engine.process(current_color)

        # Point central visuel
        cv2.circle(
            frame,
            (frame.shape[1] // 2, frame.shape[0] // 2),
            5,
            (0, 255, 0),
            -1
        )

        # Texte debug couleur
        cv2.putText(
            frame,
            f"Couleur: {current_color}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Debug RGB
        cv2.putText(
            frame,
            f"RGB: {rgb}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        # Debug HSV
        cv2.putText(
            frame,
            f"HSV: {(h, s, v)}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow("ColorDetector", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()