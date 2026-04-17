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
    # 🎯 Gestion gris / noir / blanc
    if s < SATURATION_MIN:
        if v < 50:
            return "noir"
        elif v > 200:
            return "blanc"
        else:
            return "gris"

    rgb = hsv_to_rgb(h, s, v)
    name = closest_color(rgb)

    # Simplification intelligente
    return simplify_color(name)