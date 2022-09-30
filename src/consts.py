import os
import pathlib


PROJECT_DIR = pathlib.Path(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
SECRETS_DIR = PROJECT_DIR / "secrets"
PROFILE_PATH = PROJECT_DIR / "bin"

BASE_URL = "https://www.yad2.co.il/products/"
ELECTRIC_GUITARS_URL = os.path.join(BASE_URL, "musical-instruments?category=4&item=20&type=454")

# builtins.lower doesn't change non-ascii characters
FENDER_TOKENS = ("fender", "telecaster", "stratocaster") + ("פנדר", "טלקסטר", "סטראטוקסטר", "סטראט")

ITEM_MESSAGE = "היי ראיתי את המודעה שלך על {} במחיר {} זה עדיין אקטואלי?"
