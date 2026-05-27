import cv2
import time

from detector.camera import init_camera, get_frame
from detector.color import get_center_color, get_color_name
from detector.shape import detect_shape
from detector.object import detect_objects
from detector.voice import speak
from engine.engine import Engine
from utils.config import CAMERA_INDEX

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

    print("Clique dans la fenêtre pour entendre la scène")
    speak("Application prête")

    while True:

        frame = get_frame(cap)

        if frame is None:
            time.sleep(1)
            continue

        # =========================
        # COULEUR
        # =========================
        rgb, h, s, v = get_center_color(frame)
        color = get_color_name(rgb, h, s, v)

        # =========================
        # FORME
        # =========================
        shapes = detect_shape(frame)
        shape = shapes[0] if shapes else None

        # =========================
        # OBJET
        # =========================
        objects = detect_objects(frame)
        obj = objects[0]["name"] if objects else None

        # =========================
        # DATA ENGINE
        # =========================
        data = {
            "color": color,
            "shape": shape,
            "object": obj
        }

        engine.process(data)

        # =========================
        # UI
        # =========================
        cv2.circle(frame,
                   (frame.shape[1] // 2, frame.shape[0] // 2),
                   5, (0, 255, 0), -1)

        cv2.putText(frame, f"Couleur: {color}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if shape:
            cv2.putText(frame, f"Forme: {shape}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 200, 0), 2)

        if obj:
            cv2.putText(frame, f"Objet: {obj}", (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 255), 2)

        cv2.imshow("ColorDetector", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()