import os
import random
import asyncio
import holidays
from datetime import datetime
from telethon import TelegramClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# === Config ===
API_ID = int(os.getenv("22214965"))          # my.telegram.org → API ID
API_HASH = os.getenv("4b90be3a11a5eda7ddf5d5da33ae6769")           # my.telegram.org → API HASH
BOT_TOKEN = os.getenv("7392701650:AAEdH9i_AoaRLQjvtSMp3kH0D9bxj5I4gXc")         # @BotFather → token
CHANNEL_ID = os.getenv("https://t.me/Akramov_WDev")       # @channel_username yoki kanal ID

# === Telethon client ===
client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# === Kontent manbalari (demo uchun) ===
fun_facts = [   
    "🐍 Python’da list comprehensions tez va qulay!",
    "🤖 Transformer arxitekturasi AI’da inqilob qildi.",
    "🚀 FastAPI — backend uchun juda tez va mashhur framework.",
    "💡 Linux terminal buyruqlarini o‘rganish — developer uchun kuchli skill.",
]

# === Scheduler funksiyalari ===
async def send_daily_content():
    msg = random.choice(fun_facts)
    await client.send_message(CHANNEL_ID, f"📌 Kunlik fakt:\n\n{msg}")

async def send_friday_greeting():
    today = datetime.now().strftime("%d-%m-%Y")
    msg = f"🌙 Assalomu alaykum! Juma muborak! ({today})"
    await client.send_message(CHANNEL_ID, msg)

async def send_holiday_greeting():
    uz_holidays = holidays.CountryHoliday("UZ")
    today = datetime.now().date()
    if today in uz_holidays:
        msg = f"🎉 Bayram muborak: {uz_holidays[today]}!"
        await client.send_message(CHANNEL_ID, msg)

# === Scheduler setup ===
scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
scheduler.add_job(send_daily_content, "cron", hour=9)        # Har kuni 09:00
scheduler.add_job(send_friday_greeting, "cron", day_of_week="fri", hour=10)
scheduler.add_job(send_holiday_greeting, "cron", hour=8)     # Har kuni tekshiradi
scheduler.start()

# === Run bot ===
print("✅ Bot ishga tushdi...")
client.loop.run_forever()
