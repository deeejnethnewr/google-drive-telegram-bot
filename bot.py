import os
import subprocess
from pyrogram import Client, filters

API_ID = 15647296
API_HASH = "0cb3f4a573026b56ea80e1c8f039ad6a"
BOT_TOKEN = "7957029233:AAF8rZln5PZ8OayNufB38CDi18sOFuw_EKQ"
CHANNEL_ID = -1002513282073

app = Client("gdrive_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_FOLDER = "DownloadedVideos"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_from_gdrive(url):
    # yt-dlp වලින් Google Drive link එකෙන් video download කරන function එක
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
        await message.reply_text(f"✅ Downloaded: {filename} ({size_mb:.2f} MB)\n📤 Channel එකට upload කරනවා...")
        try:
            await client.send_document(CHANNEL_ID, document=path, caption=f"🎬 {filename}")
            await message.reply_text("✅ Upload සාර්ථකයි!")
        except Exception as e:
            await message.reply_text(f"❌ Upload කිරීමට නොහැකි විය: {e}")

if __name__ == "__main__":
    app.run()
