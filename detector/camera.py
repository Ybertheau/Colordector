import cv2

def init_camera(index=0):
    cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        print("Caméra introuvable")
        return None

    print("Caméra connectée")
    return cap


def get_frame(cap):
    if cap is None:
        return None

    ret, frame = cap.read()

    if not ret or frame is None:
        print("Impossible de lire l'image")
        return None

    return frame