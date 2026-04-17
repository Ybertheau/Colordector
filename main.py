from detector.camera import init_camera, get_frame
from detector.color import get_center_color, get_color_name
from detector.voice import speak
from utils.config import CAMERA_INDEX
import cv2
import time

clicked = False

def on_mouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True


cap = init_camera(CAMERA_INDEX)

if cap is None:
    print("Programme arrêté.")
    exit()

cv2.namedWindow("ColorDetector")
cv2.setMouseCallback("ColorDetector", on_mouse)

print("Clique dans la fenêtre pour entendre la couleur")
speak("Application prête")

current_color = None

while True:
    frame = get_frame(cap)

    if frame is None:
        print("En attente de la caméra...")
        time.sleep(1)
        continue

    # Toujours calculer la couleur en continu
    h, s, v = get_center_color(frame)
    current_color = get_color_name(h, s, v)

    # CLIC = lecture de la couleur actuelle
    if clicked and current_color is not None:
        print("Couleur détectée :", current_color)
        speak(f"{current_color}")
        clicked = False  # reset IMPORTANT

    # Affichage
    cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 5, (0,255,0), -1)
    cv2.imshow("ColorDetector", frame)

    key = cv2.waitKey(1)

    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()