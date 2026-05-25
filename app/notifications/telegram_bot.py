from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing in .env")

bot = Bot(token=TOKEN)


async def send_telegram_message(alert):
    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=alert
    )
