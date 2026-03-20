import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# --- CONFIGURATION (Railway Variables) ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))
DB_CHANNEL_ID = int(os.environ.get("DB_CHANNEL_ID"))

bot = Client("MovieBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

users_list = set()

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    users_list.add(user_id)
    
    # Admin Bypass
    if user_id == ADMIN_ID:
        await message.reply_text(f"**Namaste Admin! 👋\n\nTotal Users: {len(users_list)}**")
        return await send_movie_files(client, message)

    # Force Subscribe Check
    try:
        await client.get_chat_member(CHANNEL_ID, user_id)
    except UserNotParticipant:
        # Join button for user
        await message.reply_text(
            "**⚠️ Hamare channel ko join karein tabhi movie milegi! 📢**",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/c/{str(CHANNEL_ID).replace('-100','')}/1")
            ]])
        )
        return

    await send_movie_files(client, message)

async def send_movie_files(client, message):
    intro = await message.reply_text(
        "**Hello! I am Dhurandhar 2 movie bot. 🤖\nI am sending you 3 quality movies (480p, 720p, 1080p). Please wait...**"
    )
    
    sent_ids = [intro.id]
    count = 0
    # Private channel se files dhundna
    async for msg in client.get_chat_history(DB_CHANNEL_ID, limit=30):
        if (msg.video or msg.document) and "Dhurandhar" in (msg.caption or ""):
            file_msg = await msg.copy(chat_id=message.chat.id)
            sent_ids.append(file_msg.id)
            count += 1
            if count == 3: break

    warning = await message.reply_text(
        "**⚠️ WARNING: Copyright issues ke karan ye files 5 minute mein delete ho jayengi! ⏳\nKripya ise 'Saved Messages' mein forward kar lein.**"
    )
    sent_ids.append(warning.id)

    # 5 Minute Wait
    await asyncio.sleep(300)
    
    # Delete All
    await client.delete_messages(chat_id=message.chat.id, message_ids=sent_ids)

@bot.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def stats_cmd(client, message):
    await message.reply_text(f"**📊 Total Bot Users: {len(users_list)}**")

bot.run()
