import cv2
import numpy as np
import webcolors
from collections import deque
from utils.config import ZONE_SIZE, SATURATION_MIN

#  Buffer pour stabilisation temporelle
color_buffer = deque(maxlen=5)

#  Pré-calcul des couleurs CSS (optimisé)
CSS_COLORS = {
    name: webcolors.name_to_rgb(name)
    for name in webcolors.names("css3")
}

CSS_NAMES = list(CSS_COLORS.keys())
CSS_VALUES = np.array(list(CSS_COLORS.values()))


def get_center_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, w, _ = hsv.shape

    size = ZONE_SIZE

    #  zone sécurisée (évite crash)
    y1 = max(0, h // 2 - size)
    y2 = min(h, h // 2 + size)
    x1 = max(0, w // 2 - size)
    x2 = min(w, w // 2 + size)

    zone = hsv[y1:y2, x1:x2]

    #  médiane → robuste au bruit
    avg_color = np.median(zone, axis=(0, 1)).astype(int)

    return avg_color  # H, S, V


def hsv_to_rgb(h, s, v):
    hsv_pixel = np.uint8([[[h, s, v]]])
    bgr = cv2.cvtColor(hsv_pixel, cv2.COLOR_HSV2BGR)[0][0]
    return (int(bgr[2]), int(bgr[1]), int(bgr[0]))  # RGB


def closest_color(rgb):
    rgb_array = np.array(rgb)

    distances = np.sum((CSS_VALUES - rgb_array) ** 2, axis=1)
    index = np.argmin(distances)

    return CSS_NAMES[index]


def simplify_color(name):
    name = name.lower()

    if "gray" in name or "grey" in name:
        return "gris"

    if "black" in name:
        return "noir"

    if "white" in name:
        return "blanc"

    if "red" in name:
        return "rouge"

    if "blue" in name:
        return "bleu"

    if "green" in name:
        return "vert"

    if "yellow" in name:
        return "jaune"

    if "purple" in name or "violet" in name:
        return "violet"

    if "pink" in name:
        return "rose"

    if "orange" in name:
        return "orange"

    if "brown" in name:
        return "marron"

    return "couleur inconnue"


def get_color_name(h, s, v):
    #  Gestion gris / noir / blanc améliorée
    if s < SATURATION_MIN or v < 40:
        if v < 50:
            color = "noir"
        elif v > 200:
            color = "blanc"
        else:
            color = "gris"
    else:
        rgb = hsv_to_rgb(h, s, v)
        name = closest_color(rgb)
        color = simplify_color(name)

    #  stabilisation temporelle
    color_buffer.append(color)
    stable_color = max(set(color_buffer), key=color_buffer.count)

    return stable_color