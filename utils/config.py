# utils/config.py

# ======================
#  CAMÉRA
# ======================
CAMERA_INDEX = 0  # 0 = webcam, 1/2 = autre source

FRAME_WIDTH = 640
FRAME_HEIGHT = 480


# ======================
#  VOIX
# ======================
VOICE_ENABLED = True

#  délai minimum entre deux annonces (anti spam)
SPEAK_DELAY = 1.0  # secondes

#  autoriser répétition même couleur après délai
ALLOW_REPEAT_AFTER_DELAY = True


# ======================
#  DÉTECTION COULEUR
# ======================

# Taille de la zone analysée (autour du centre)
ZONE_SIZE = 20

#  seuil saturation (gris vs couleur)
SATURATION_MIN = 50

#  seuil luminosité (noir)
VALUE_DARK_MAX = 50

#  seuil luminosité (blanc)
VALUE_LIGHT_MIN = 200


# ======================
#  STABILISATION
# ======================

# Nombre de frames pour stabiliser la couleur
COLOR_BUFFER_SIZE = 5


# ======================
#  DEBUG
# ======================

DEBUG = True
PRINT_HSV = False