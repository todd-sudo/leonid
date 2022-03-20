import pytesseract
from PIL import Image


def image_to_text(image: str, lang: str):
    img = Image.open(image)
    custom_config = r'--oem --psm 13'
    text = pytesseract.image_to_string(
        image=img, config=custom_config, lang=lang
    ).strip()
    return text
