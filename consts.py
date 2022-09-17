import os

PROFILE_PATH = r".\bin"

BASE_URL = "https://www.yad2.co.il/products/"
ELECTRIC_GUITARS_URL = os.path.join(BASE_URL, "musical-instruments?category=4&item=20&type=454")

# builtins.lower doesn't change non-ascii characters
FENDER_TOKENS = ("fender", "telecaster", "stratocaster") + ("פנדר", "טלקסטר", "סטראטוקסטר", "סטראט")
