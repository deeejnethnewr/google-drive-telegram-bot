import os
import subprocess
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID", "123456"))  # ඔයාගේ API ID යනුවෙන් මෙහි දාන්න
API_HASH = os.getenv("API_HASH", "your_api_hash_here")  # ඔයාගේ API HASH මෙහි දාන්න
BOT_TOKEN = os.getenv("BOT_TOKEN", "7957029233:AAF8rZln5PZ8OayNufB38CDi18sOFuw_EKQ")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002513282073"))

app = Client("gdrive_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOAD_FOLDER = "DownloadedVideos"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_from_gdrive(url):
    # yt-dlp වලින් ගූගල් ඩ්‍රයිව් වීඩියෝ download කරයි
    cmd = f"yt-dlp -f best '{url}' -o '{DOWNLOAD_FOLDER}/%(title)s.%(ext)s'"
    subprocess.run(cmd, shell=True, check=True)

@app.on_message(filters.private & filters.regex(r"https://drive\.google\.com/"))
async def gdrive_handler(client, message):
    url = message.text.strip()
    await message.reply_text("📥 Google Drive link එකෙන් වීඩියෝ download කරමින්...")
    
    before_files = set(os.listdir(DOWNLOAD_FOLDER))
    try:
        download_from_gdrive(url)
    except subprocess.CalledProcessError:
        await message.reply_text("❌ Download කිරීම අසමත් විය.")
        return

    after_files = set(os.listdir(DOWNLOAD_FOLDER))
    new_files = after_files - before_files

    if not new_files:
        await message.reply_text("❌ Download කරපු file එක හමු නොවීය.")
        return

    for filename in new_files:
        path = os.path.join(DOWNLOAD_FOLDER, filename)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        await message.reply_text(f"✅ Downloaded: {filename} ({size_mb:.2f} MB)\n📤 Uploading to channel...")
        try:
            await client.send_document(
                chat_id=CHANNEL_ID,
                document=path,
                caption=f"🎬 {filename}"
            )
            await message.reply_text("✅ Successfully uploaded to channel!")
        except Exception as e:
            await message.reply_text(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    app.run()
