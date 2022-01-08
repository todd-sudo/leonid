import json


def get_hello_message():
    with open("src/data/strings.json", "r") as file:
        json_data = json.load(file)
    return json_data.get("hello")


def get_stickers_texts():
    return ["python", "js", "ios", "thanks", "windows"]


def get_python():
    with open("src/data/stickers.json", "r") as file:
        json_data = json.load(file)
    return json_data.get("python")


def get_ios():
    with open("src/data/stickers.json", "r") as file:
        json_data = json.load(file)
    return json_data.get("ios")


def get_windows():
    with open("src/data/stickers.json", "r") as file:
        json_data = json.load(file)
    return json_data.get("windows")


def get_js():
    with open("src/data/stickers.json", "r") as file:
        json_data = json.load(file)
    return json_data.get("js")


def get_thanks():
    with open("src/data/stickers.json", "r") as file:
        json_data = json.load(file)
    return json_data.get("thanks")
