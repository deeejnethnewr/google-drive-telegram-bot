import os
import subprocess
from pyrogram import Client, filters

API_ID = 15647296
API_HASH = "0cb3f4a573026b56ea80e1c8f039ad6a"
BOT_TOKEN = "7957029233:AAF8rZln5PZ8OayNufB38CDi18sOFuw_EKQ"

app = Client("gdrive_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_FOLDER = "DownloadedVideos"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_from_gdrive(url):
    cmd = f"yt-dlp -f best '{url}' -o '{DOWNLOAD_FOLDER}/%(title)s.%(ext)s'"
    subprocess.run(cmd, shell=True, check=True)

@app.on_message(filters.private & filters.regex(r"https://drive\.google\.com/"))
async def gdrive_handler(client, message):
    url = message.text.strip()
    await message.reply_text("📥 Google Drive video download කරනවා...")

    before_files = set(os.listdir(DOWNLOAD_FOLDER))
    try:
        download_from_gdrive(url)
    except subprocess.CalledProcessError:
        await message.reply_text("❌ Video download කිරීම අසමත් විය.")
        return

    after_files = set(os.listdir(DOWNLOAD_FOLDER))
    new_files = after_files - before_files

    if not new_files:
        await message.reply_text("❌ Download වීඩියෝ හමු නොවීය.")
        return

    for filename in new_files:
        path = os.path.join(DOWNLOAD_FOLDER, filename)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        await message.reply_text(f"✅ Downloaded: {filename} ({size_mb:.2f} MB)\n📤 ඔබට file එක upload කරනවා...")
        try:
            await client.send_document(
                chat_id=message.chat.id,  # video එවන්නකොට ඔයාටම (message එවූ chat id)
                document=path,
                caption=f"🎬 {filename}"
            )
            await message.reply_text("✅ File upload සාර්ථකයි!")
        except Exception as e:
            await message.reply_text(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    app.run()
