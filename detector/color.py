from collections import deque, Counter
import cv2
import numpy as np
import webcolors

from utils.config import ZONE_SIZE, COLOR_BUFFER_SIZE

color_buffer = deque(maxlen=COLOR_BUFFER_SIZE)

CSS_COLORS = {
    name: webcolors.name_to_rgb(name)
    for name in webcolors.names("css3")
}

CSS_NAMES = list(CSS_COLORS.keys())
CSS_VALUES = np.array(list(CSS_COLORS.values()))


def get_center_color(frame):

    height, width, _ = frame.shape
    size = ZONE_SIZE

    y1 = max(0, height // 2 - size)
    y2 = min(height, height // 2 + size)

    x1 = max(0, width // 2 - size)
    x2 = min(width, width // 2 + size)

    zone_bgr = frame[y1:y2, x1:x2]

    if zone_bgr.size == 0:
        return (0, 0, 0), 0, 0, 0

    avg_bgr = np.median(zone_bgr, axis=(0, 1)).astype(int)

    rgb = (int(avg_bgr[2]), int(avg_bgr[1]), int(avg_bgr[0]))

    hsv = cv2.cvtColor(np.uint8([[avg_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

    return rgb, hsv[0], hsv[1], hsv[2]


def closest_color(rgb):

    rgb_array = np.array(rgb)

    distances = np.sum((CSS_VALUES - rgb_array) ** 2, axis=1)

    return CSS_NAMES[np.argmin(distances)]


def simplify_color(name):

    name = name.lower()

    if "blue" in name: return "bleu"
    if "red" in name: return "rouge"
    if "green" in name: return "vert"
    if "yellow" in name: return "jaune"
    if "purple" in name or "violet" in name: return "violet"
    if "pink" in name: return "rose"
    if "orange" in name: return "orange"
    if "brown" in name: return "marron"
    if "black" in name: return "noir"
    if "white" in name: return "blanc"
    if "gray" in name or "grey" in name: return "gris"

    return "couleur inconnue"


def get_color_name(rgb, h, s, v):

    if v < 35:
        color = "noir"

    elif v > 220 and s < 25:
        color = "blanc"

    else:
        color = simplify_color(closest_color(rgb))

    color_buffer.append(color)

    return Counter(color_buffer).most_common(1)[0][0]