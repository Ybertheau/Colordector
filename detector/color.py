import cv2
import numpy as np
import webcolors
from utils.config import ZONE_SIZE, SATURATION_MIN

# Pré-calcul des couleurs CSS (optimisation)
CSS_COLORS = {
    name: webcolors.name_to_rgb(name)
    for name in webcolors.names("css3")
}


def get_center_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, w, _ = hsv.shape

    size = ZONE_SIZE

    zone = hsv[
        h//2 - size : h//2 + size,
        w//2 - size : w//2 + size
    ]

    avg_color = np.mean(zone, axis=(0, 1))
    return avg_color  # H, S, V


def hsv_to_rgb(h, s, v):
    hsv_pixel = np.uint8([[[h, s, v]]])
    bgr = cv2.cvtColor(hsv_pixel, cv2.COLOR_HSV2BGR)[0][0]
    return (int(bgr[2]), int(bgr[1]), int(bgr[0]))  # RGB


def closest_color(rgb):
    r, g, b = rgb
    min_distance = float("inf")
    closest_name = "inconnu"

    for name, (cr, cg, cb) in CSS_COLORS.items():
        distance = (cr - r)**2 + (cg - g)**2 + (cb - b)**2

        if distance < min_distance:
            min_distance = distance
            closest_name = name

    return closest_name


# Simplification FR 
COLOR_MAP_FR = {
    "red": "rouge",
    "darkred": "rouge foncé",
    "blue": "bleu",
    "lightblue": "bleu clair",
    "green": "vert",
    "darkgreen": "vert foncé",
    "yellow": "jaune",
    "black": "noir",
    "white": "blanc",
    "gray": "gris",
    "grey": "gris",
    "purple": "violet",
    "pink": "rose",
    "orange": "orange",
    "brown": "marron"
}


def get_color_name(h, s, v):
    if s < SATURATION_MIN:
        return "gris/blanc/noir"

    rgb = hsv_to_rgb(h, s, v)
    name = closest_color(rgb)

    # Traduction FR
    return COLOR_MAP_FR.get(name, name)