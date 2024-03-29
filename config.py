import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
BD_STICKER = "CAACAgIAAxkBAAEDofVh2CcZLyxcEDPTk2jxtzmId7OHPQACGwADwDZPE329ioPLRE1qIwQ"
ADMINS = ["939392408", -672385422, 939392408]

