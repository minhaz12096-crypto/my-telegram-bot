import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

# --- Render-এর জন্য Flask সার্ভার (বটকে সচল রাখতে) ---
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is Running 24/7!"

def run_flask():
    # Render সাধারণত পোর্টের জন্য environment variable ব্যবহার করে
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

# --- আপনার দেওয়া বটের কনফিগারেশন ---
API_ID = 35558637
API_HASH = "93bb67b4c3c1d5553d191fea10fdd591"
BOT_TOKEN = "8459525108:AAFZtir5YVHyiJQ9rAjCo9_oOOYAr9y2O2U"

# আপনার মনিট্যাগ লিঙ্কটি নিচের কোটেশনের ভেতর বসিয়ে দিন
MONETAG_LINK = "https://omg10.com/4/10794334" 

bot = Client("my_pro_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ১. জয়েন রিকোয়েস্ট অটো এক্সেপ্ট
@bot.on_chat_join_request()
async def auto_accept(client, request):
    try:
        await client.approve_chat_join_request(request.chat.id, request.from_user.id)
    except Exception as e:
        print(f"Join Accept Error: {e}")

# ২. কেউ লিভ নিলে অটো ব্যান এবং ইউজারনেমসহ পোস্ট
@bot.on_message(filters.left_chat_member)
async def auto_ban_on_left(client, message):
    user = message.left_chat_member
    chat_id = message.chat.id
    username = f"@{user.username}" if user.username else user.first_name
    
    try:
        await client.ban_chat_member(chat_id, user.id)
        msg = (f"👋 **Bye Bye!** {username}\n"
               f"গ্রুপ ছেড়ে চলে যাওয়ায় তোমাকে পার্মানেন্ট ব্যান করা হলো।\n\n"
               f"📢 **Our Offer:** {MONETAG_LINK}")
        await client.send_message(chat_id, msg)
    except Exception as e:
        print(f"Ban Error: {e}")

# ৩. অটো রিঅ্যাকশন (নতুন মেসেজ আসলে)
@bot.on_message(filters.group & ~filters.service)
async def auto_reaction(client, message):
    try:
        # মেসেজে রিঅ্যাকশন দিবে (👍 ইমোজি)
        await message.react("👍")
    except:
        pass

# ৪. ২৪ ঘণ্টা পর পর অটো মেসেজ (Good Morning + Monetag)
async def daily_greeting():
    while True:
        # ২৪ ঘণ্টা (৮৬৪০০ সেকেন্ড) অপেক্ষা করবে
        await asyncio.sleep(86400) 
        
        greeting_msg = (f"☀️ **Good Morning Everyone!** 🌅\n"
                        f"আশা করি সবার দিনটি ভালো যাবে।\n\n"
                        f"💰 **Earn from here:** {MONETAG_LINK}")
        
        # বট যে যে গ্রুপে আছে সবগুলোতে পাঠানোর চেষ্টা করবে
        async for dialog in bot.get_dialogs():
            if dialog.chat.type in ["group", "supergroup"]:
                try:
                    await bot.send_message(dialog.chat.id, greeting_msg)
                except:
                    continue

# ৫. রান করা
if __name__ == "__main__":
    # Flask সার্ভার আলাদা থ্রেডে চালু
    threading.Thread(target=run_flask, daemon=True).start()
    
    # বট চালু
    print("বটটি আপনার দেওয়া টোকেন দিয়ে চালু হচ্ছে...")
    bot.run()
