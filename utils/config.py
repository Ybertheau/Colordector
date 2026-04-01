# utils/config.py

# Caméra
CAMERA_INDEX = 0  # 0 = webcam, 1 ou 2 = téléphone

# Voix
VOICE_ENABLED = True
SPEAK_DELAY = 2  # secondes entre chaque annonce

# Détection
USE_CENTER_PIXEL = True
ZONE_SIZE = 20  # taille zone si on améliore plus tard

# Seuils HSV (tu pourras les ajuster)
COLOR_RANGES = {
    "rouge": [(0, 10), (170, 180)],
    "jaune": [(20, 35)],
    "vert": [(35, 85)],
    "bleu": [(90, 130)],
    "violet": [(130, 160)]
}

SATURATION_MIN = 50