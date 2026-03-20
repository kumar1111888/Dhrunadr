import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

# 🔥 TERA DATA (DIRECT SET KIYA)
CHANNEL_USERNAME = "Tmkocc_backup"   # force sub
DB_CHANNEL_ID = -1003746827406       # source channel

bot = Client("MovieBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

users_list = set()

# --- START ---
@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    users_list.add(user_id)

    # ADMIN
    if user_id == ADMIN_ID:
        await message.reply_text(f"**Namaste Admin! 👋\nTotal Users: {len(users_list)}**")
        return await send_movie_files(client, message)

    # 🔥 FORCE SUB CHECK (USERNAME BASED)
    try:
        member = await client.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        if member.status in ["kicked", "left"]:
            raise UserNotParticipant
    except:
        return await message.reply_text(
            "**⚠️ Pehle channel join karo!**",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")
            ]])
        )

    await send_movie_files(client, message)


# --- SEND MOVIES ---
async def send_movie_files(client, message):
    intro = await message.reply_text(
        "**🎬 Dhurandhar 2 Movie Bot\n\n⚡ 480p | 720p | 1080p bhej raha hoon...\nPlease wait...**"
    )

    sent_ids = [intro.id]
    count = 0

    try:
        async for msg in client.get_chat_history(DB_CHANNEL_ID, limit=50):
            if msg.caption and "Dhurandhar The Revenge 2026" in msg.caption:
                if msg.video or msg.document:
                    file_msg = await msg.copy(chat_id=message.chat.id)
                    sent_ids.append(file_msg.id)
                    count += 1

                    if count == 3:
                        break

        if count == 0:
            warn = await message.reply_text("❌ Movie nahi mili channel me!")
            sent_ids.append(warn.id)

    except Exception as e:
        print("ERROR:", e)
        err = await message.reply_text("⚠️ Error aa gaya bhai!")
        sent_ids.append(err.id)

    # WARNING
    warning = await message.reply_text(
        "**⚠️ 5 minute me delete ho jayegi!\n👉 Saved Messages me forward kar lo**"
    )
    sent_ids.append(warning.id)

    await asyncio.sleep(300)

    try:
        await client.delete_messages(chat_id=message.chat.id, message_ids=sent_ids)
    except:
        pass


# --- STATS ---
@bot.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def stats_cmd(client, message):
    await message.reply_text(f"Users: {len(users_list)}")


bot.run()
