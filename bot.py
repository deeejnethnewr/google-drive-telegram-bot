from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os
import asyncio
import yt_dlp

API_ID = 15647296
API_HASH = "0cb3f4a573026b56ea80e1c8f039ad6a"
BOT_TOKEN = "8144738030:AAHDWFS8B68PBdbp7ljukTriy-QlA414tV4"

bot = Client("media_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

active_downloads = {}

# Download progress hook
def progress_hook(d):
    message = active_downloads.get(d.get("info_dict", {}).get("id"))
    if message and d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        total = d.get("_total_bytes_str", "").strip()
        downloaded = d.get("_downloaded_bytes_str", "").strip()
        text = f"📥 Downloading: `{percent}`\n💾 Downloaded: `{downloaded} / {total}`"
        asyncio.create_task(message.edit_text(text))

# Format selection
def build_format_keyboard(formats):
    buttons = []
    for fmt in formats:
        label = f"{fmt['format_note']} - {fmt['ext']} - {fmt['filesize'] // 1024 // 1024 if fmt.get('filesize') else '?'}MB"
        buttons.append([InlineKeyboardButton(label, callback_data=fmt['format_id'])])
    return InlineKeyboardMarkup(buttons)

# Start
@bot.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    await message.reply("👋 Send me a YouTube / Google Drive / Dailymotion link to download.")

# URL Handler
@bot.on_message(filters.private & filters.text)
async def url_handler(client, message: Message):
    url = message.text.strip()
    if not any(site in url for site in ["youtube.com", "youtu.be", "drive.google.com", "dailymotion.com"]):
        return await message.reply("❌ Unsupported URL")

    temp_msg = await message.reply("🔎 Fetching video info...")

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        return await temp_msg.edit(f"⚠️ Error: {e}")

    video_id = info.get("id")
    formats = [f for f in info.get("formats", []) if f.get("filesize")]
    formats = sorted(formats, key=lambda x: x["filesize"] if x.get("filesize") else 0, reverse=True)[:10]

    if not formats:
        return await temp_msg.edit("❌ No downloadable formats found.")

    active_downloads[video_id] = temp_msg
    await temp_msg.edit("🔻 Select a format to download:", reply_markup=build_format_keyboard(formats))

    # Store info for callback use
    temp_msg.video_info = info

# Format button callback
@bot.on_callback_query()
async def format_button(client, callback_query):
    format_id = callback_query.data
    message = callback_query.message
    info = getattr(message, 'video_info', None)
    if not info:
        return await callback_query.answer("❌ Video info missing", show_alert=True)

    await message.edit_text("⏬ Starting download...")

    ydl_opts = {
        'format': format_id,
        'outtmpl': f"{info['id']}.%(ext)s",
        'progress_hooks': [progress_hook],
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([info['webpage_url']])
    except Exception as e:
        return await message.edit_text(f"❌ Download failed: {e}")

    await message.edit_text("✅ Download complete (not uploaded or saved as per settings).")

bot.run()
