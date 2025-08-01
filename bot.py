# bot.py
import asyncio
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN
from plugins import all_handlers

app = Client(
    "renamer_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

if __name__ == "__main__":
    all_handlers.load(app)
    print("✅ Renamer Bot Started Successfully!")
    app.run()
