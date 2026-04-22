import cv2

def init_camera(index=0):
    backends = [
        cv2.CAP_DSHOW,
        cv2.CAP_MSMF,
        cv2.CAP_ANY
    ]

    for backend in backends:
        cap = cv2.VideoCapture(index, backend)

        if cap.isOpened():
            print(f"Caméra connectée (backend={backend})")
            return cap

    print("Caméra introuvable")
    return None


def get_frame(cap):
    if cap is None:
        return None

    ret, frame = cap.read()

    if not ret or frame is None:
        print("Impossible de lire l'image")
        return None

    return frame