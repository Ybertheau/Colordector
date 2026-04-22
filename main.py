import cv2
import time

from detector.camera import init_camera, get_frame
from detector.color import get_center_color, get_color_name
from detector.voice import speak
from utils.config import CAMERA_INDEX

#  État global simple
clicked = False
last_spoken = None


def on_mouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        print("CLICK OK")  # debug utile
        clicked = True


def main():
    global clicked, last_spoken

    cap = init_camera(CAMERA_INDEX)

    if cap is None:
        print("Programme arrêté.")
        return

    cv2.namedWindow("ColorDetector")
    cv2.setMouseCallback("ColorDetector", on_mouse)

    print("Clique dans la fenêtre pour entendre la couleur")
    speak("Application prête")

    while True:
        frame = get_frame(cap)

        if frame is None:
            print("En attente de la caméra...")
            time.sleep(1)
            continue

        #  Analyse couleur (continue)
        h, s, v = get_center_color(frame)
        current_color = get_color_name(h, s, v)

        #  Interaction utilisateur
        if clicked:
            clicked = False  # reset immédiat (important)

            if current_color is not None:
                print("Couleur détectée :", current_color)

                #  anti-répétition
                if current_color != last_spoken:
                    speak(current_color)
                    last_spoken = current_color

        #  Feedback visuel minimal (utile debug)
        cv2.circle(
            frame,
            (frame.shape[1] // 2, frame.shape[0] // 2),
            5,
            (0, 255, 0),
            -1
        )

        cv2.imshow("ColorDetector", frame)

        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break

    #  Clean exit
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()