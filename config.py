import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_CHAT_MODEL = "gemini-2.0-flash"


if not BOT_TOKEN:
    print("Ошибка: BOT_TOKEN не найден.")
if not GEMINI_API_KEY:
    print("Ошибка: GEMINI_API_KEY не найден.")