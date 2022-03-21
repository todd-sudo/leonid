import easyocr
import pytesseract
from PIL import Image


def image_to_text_tess(image: str, lang: str):
    img = Image.open(image)
    custom_config = r'--oem --psm 13'
    text = pytesseract.image_to_string(
        image=img, config=custom_config, lang=lang
    ).strip()
    return text


def text_recognition(file_path, gpu: bool):
    reader = easyocr.Reader(["ru", "en"], gpu=gpu)
    result = reader.readtext(file_path, detail=0, paragraph=True)
    return result
