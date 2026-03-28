import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters

# --- Flask Server for Render ---
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

# --- কনফিগারেশন ---
API_ID = 35558637
API_HASH = "93bb67b4c3c1d5553d191fea10fdd591"
BOT_TOKEN = "8459525108:AAFZtir5YVHyiJQ9rAjCo9_oOOYAr9y2O2U"
MONETAG_LINK = "https://omg10.com/4/10794334" 

bot = Client("my_pro_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# জয়েন রিকোয়েস্ট এক্সেপ্ট
@bot.on_chat_join_request()
async def auto_accept(client, request):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
    except:
        pass

# কেউ লিভ নিলে ব্যান এবং মেসেজ
@bot.on_message(filters.left_chat_member)
async def auto_ban_on_left(client, message):
    user = message.left_chat_member
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.send_message(message.chat.id, f"👋 Bye! {user.first_name}\n📢 Check: {MONETAG_LINK}")
    except:
        pass

# অটো রিঅ্যাকশন
@bot.on_message(filters.group & ~filters.service)
async def auto_reaction(client, message):
    try:
        await message.react("👍")
    except:
        pass

# ডেইলি গুড মর্নিং পোস্ট
async def daily_greeting():
    while True:
        await asyncio.sleep(86400)
        async for dialog in bot.get_dialogs():
            if dialog.chat.type in ["group", "supergroup"]:
                try:
                    await bot.send_message(dialog.chat.id, f"☀️ Good Morning Everyone! 🌅\n💰 Earn: {MONETAG_LINK}")
                except:
                    continue

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    loop = asyncio.get_event_loop()
    loop.create_task(daily_greeting())
    print("Bot is Starting...")
    bot.run()
