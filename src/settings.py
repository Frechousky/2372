import pathlib

import i18n

GAME_NAME = "2372"

# display
WINDOW_SIZE = (1920, 1080)
FPS = 60

# i18n
LOCALES = ["fr", "en"]

# directories
ROOT_DIR = pathlib.Path(__file__).parent.parent
FONTS_DIR = ROOT_DIR / "assets" / "fonts"
I18N_DIR = ROOT_DIR / "assets" / "i18n"
IMAGES_DIR = ROOT_DIR / "assets" / "images"
SOUNDS_DIR = ROOT_DIR / "assets" / "sounds"

# files
LOGS_FILE = ROOT_DIR / "logs.log"
BLANKA_FONT = pathlib.Path("blanka", "Blanka.otf")
CLICK_SOUND = "click.wav"


def init_i18n(locale: str):
    """sets internationalization settings"""
    i18n.set("available_locales", LOCALES)
    # to load files 'fr.json', 'en.json'
    i18n.set("filename_format", "{locale}.{format}")
    i18n.set("locale", locale)
    i18n.load_path.append(I18N_DIR)
