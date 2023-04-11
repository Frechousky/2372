import os

import i18n

# display
WINDOW_SIZE = (1920, 1080)
FPS = 60

# i18n
LOCALES = ["fr", "en"]

# directories
ROOT_DIR = os.getcwd()
FONTS_DIR = os.path.join(ROOT_DIR, "assets", "fonts")
I18N_DIR = os.path.join(ROOT_DIR, "assets", "i18n")
IMAGES_DIR = os.path.join(ROOT_DIR, "assets", "images")
SOUNDS_DIR = os.path.join(ROOT_DIR, "assets", "sounds")

# files
LOGS_FILE = os.path.join(ROOT_DIR, "logs.log")
BLANKA_FONT = os.path.join(FONTS_DIR, "blanka", "Blanka.otf")
CLICK_SOUND = os.path.join(SOUNDS_DIR, "click.wav")


def init_i18n(locale: str):
    i18n.set("available_locales", LOCALES)
    # to load files 'fr.json', 'en.json'
    i18n.set("filename_format", "{locale}.{format}")
    i18n.set("locale", locale)
    i18n.load_path.append(I18N_DIR)
