from detector.camera import init_camera, get_frame
from detector.color import get_center_color, get_color_name
from detector.voice import speak
from utils.config import CAMERA_INDEX
import cv2
import time

cap = init_camera(CAMERA_INDEX)

# Stop direct si pas de caméra
if cap is None:
    print("Programme arrêté.")
    exit()

last_color = None

while True:
    frame = get_frame(cap)

    # Si pas d'image → attendre au lieu de spam
    if frame is None:
        print("En attente de la caméra...")
        time.sleep(1)
        continue

    h, s, v = get_center_color(frame)
    color = get_color_name(h, s, v)

    # Parler seulement si changement
    if color != last_color:
        print("", color)
        speak(color)
        last_color = color

    # Affichage point central
    cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 5, (0,255,0), -1)
    cv2.imshow("ColorDetector", frame)

    # Quitter avec ESC
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()