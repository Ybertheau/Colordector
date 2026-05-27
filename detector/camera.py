import cv2

def init_camera(index=0):
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]

    for backend in backends:
        cap = cv2.VideoCapture(index, backend)

        if cap.isOpened():
            ret, frame = cap.read()

            if ret and frame is not None:
                print(f"Caméra connectée (backend={backend})")
                return cap

        cap.release()

    print("Caméra introuvable")
    return None


def get_frame(cap):
    if cap is None:
        return None

    ret, frame = cap.read()

    if not ret or frame is None:
        return None

    return frame