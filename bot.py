import os
import time
import requests
import subprocess
from pyrogram import Client, filters

API_ID = 12345678  # Replace with your API ID
API_HASH = "your_api_hash"  # Replace with your API HASH
BOT_TOKEN = "7957029233:AAF8rZln5PZ8OayNufB38CDi18sOFuw_EKQ"
CHANNEL_ID = -1002513282073

app = Client("gdrive_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_FOLDER = "DownloadedVideos"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_from_gdrive(url):
    cmd = f"yt-dlp -f best '{url}' -o '{DOWNLOAD_FOLDER}/%(title)s.%(ext)s'"
    subprocess.run(cmd, shell=True)

def get_file_name(path):
    return os.path.basename(path)

@app.on_message(filters.private & filters.text & filters.regex(r'https://drive\.google\.com/'))
async def handle_gdrive(client, message):
    url = message.text.strip()
    await message.reply_text("📥 Downloading from Google Drive...")
    before_files = set(os.listdir(DOWNLOAD_FOLDER))
    download_from_gdrive(url)
    after_files = set(os.listdir(DOWNLOAD_FOLDER))
    new_files = after_files - before_files

    if not new_files:
        await message.reply_text("❌ Download failed.")
        return

    for filename in new_files:
        path = os.path.join(DOWNLOAD_FOLDER, filename)
        size = os.path.getsize(path) / (1024 * 1024)
        await message.reply_text(f"✅ Downloaded: {filename} ({size:.2f} MB)
📤 Uploading to channel...")
        try:
            await client.send_document(CHANNEL_ID, document=path, caption=f"🎬 {filename}")
            await message.reply_text("✅ Uploaded successfully!")
        except Exception as e:
            await message.reply_text(f"❌ Upload failed: {e}")

app.run()