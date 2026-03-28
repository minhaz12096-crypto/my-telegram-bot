import os
import asyncio
from flask import Flask
from pyrogram import Client, filters

# Render সচল রাখতে ছোট সার্ভার
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running!"

# কনফিগারেশন
API_ID = 35558637
API_HASH = "93bb67b4c3c1d5553d191fea10fdd591"
BOT_TOKEN = "8459525108:AAFZtir5YVHyiJQ9rAjCo9_oOOYAr9y2O2U"
MONETAG = "https://omg10.com/4/10794334"

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# জয়েন রিকোয়েস্ট এক্সেপ্ট
@bot.on_chat_join_request()
async def accept(client, request):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
    except:
        pass

# অটো ব্যান ও মেসেজ
@bot.on_message(filters.left_chat_member)
async def auto_ban(client, message):
    try:
        await client.ban_chat_member(message.chat.id, message.left_chat_member.id)
        await client.send_message(message.chat.id, f"👋 Bye Bye!\n📢 Check this: {MONETAG}")
    except:
        pass

# অটো রিঅ্যাকশন
@bot.on_message(filters.group & ~filters.service)
async def react(client, message):
    try:
        await message.react("👍")
    except:
        pass

# মেন ফাংশন
async def start_bot():
    await bot.start()
    print("Bot is Live!")
    # ২৪ ঘণ্টা পর পর মেসেজ লুপ
    while True:
        await asyncio.sleep(86400)
        async for dialog in bot.get_dialogs():
            if dialog.chat.type in ["group", "supergroup"]:
                try: await bot.send_message(dialog.chat.id, f"Good Morning! ☀️\n{MONETAG}")
                except: continue

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))), daemon=True).start()
    asyncio.run(start_bot())
