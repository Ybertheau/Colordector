import cv2

def get_center_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, w, _ = hsv.shape
    return hsv[h//2, w//2]

def get_color_name(h, s, v):
    if s < 50:
        return "gris/blanc/noir"

    if h < 10 or h > 170:
        return "rouge"
    elif 20 < h < 35:
        return "jaune"
    elif 35 < h < 85:
        return "vert"
    elif 90 < h < 130:
        return "bleu"
    elif 130 < h < 160:
        return "violet"
    else:
        return "inconnu"