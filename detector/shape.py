import cv2
import numpy as np


def detect_shape(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapes = []

    for cnt in contours:

        area = cv2.contourArea(cnt)

        # filtre bruit
        if area < 1000:
            continue

        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        sides = len(approx)

        if sides == 3:
            shapes.append("triangle")

        elif sides == 4:
            shapes.append("rectangle")

        else:
            # meilleure détection cercle
            perimeter = cv2.arcLength(cnt, True)
            circularity = 4 * np.pi * area / (perimeter * perimeter + 1e-6)

            if circularity > 0.75:
                shapes.append("circle")

    return shapes