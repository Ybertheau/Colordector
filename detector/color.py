import cv2
import numpy as np
import webcolors
from collections import deque

from utils.config import (
    ZONE_SIZE,
    COLOR_BUFFER_SIZE
)

color_buffer = deque(maxlen=COLOR_BUFFER_SIZE)

# =========================
# CSS COLORS
# =========================

CSS_COLORS = {
    name: webcolors.name_to_rgb(name)
    for name in webcolors.names("css3")
}

CSS_NAMES = list(CSS_COLORS.keys())
CSS_VALUES = np.array(list(CSS_COLORS.values()))


# =========================
# CENTER COLOR
# =========================

def get_center_color(frame):

    h, w, _ = frame.shape
    size = ZONE_SIZE

    y1 = max(0, h // 2 - size)
    y2 = min(h, h // 2 + size)

    x1 = max(0, w // 2 - size)
    x2 = min(w, w // 2 + size)

    zone_bgr = frame[y1:y2, x1:x2]

    # Couleur réelle webcam
    avg_bgr = np.median(zone_bgr, axis=(0, 1)).astype(int)

    # BGR → RGB
    rgb = (
        int(avg_bgr[2]),
        int(avg_bgr[1]),
        int(avg_bgr[0])
    )

    # HSV uniquement pour luminosité
    hsv = cv2.cvtColor(
        np.uint8([[avg_bgr]]),
        cv2.COLOR_BGR2HSV
    )[0][0]

    h, s, v = hsv

    return rgb, h, s, v


# =========================
# CLOSEST COLOR
# =========================

def closest_color(rgb):

    rgb_array = np.array(rgb)

    distances = np.sum(
        (CSS_VALUES - rgb_array) ** 2,
        axis=1
    )

    index = np.argmin(distances)

    return CSS_NAMES[index]


# =========================
# SIMPLIFY
# =========================

def simplify_color(name):

    name = name.lower()

    if "blue" in name:
        return "bleu"

    if "red" in name:
        return "rouge"

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

    if "black" in name:
        return "noir"

    if "white" in name:
        return "blanc"

    if "gray" in name or "grey" in name:
        return "gris"

    return "couleur inconnue"


# =========================
# FINAL COLOR
# =========================

def get_color_name(rgb, h, s, v):

    # Noir réel
    if v < 35:
        color = "noir"

    # Blanc réel
    elif v > 220 and s < 25:
        color = "blanc"

    else:
        css_name = closest_color(rgb)
        color = simplify_color(css_name)

    # Stabilisation
    color_buffer.append(color)

    stable_color = max(
        set(color_buffer),
        key=color_buffer.count
    )

    return stable_color