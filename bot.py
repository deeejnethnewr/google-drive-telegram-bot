#!/usr/bin/env python3
import os
import re
import tempfile
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message

# Load credentials from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID    = int(os.getenv("API_ID") or 0)
API_HASH  = os.getenv("API_HASH")

app = Client(
    "gdrive_downloader",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)

# Catch Google Drive file IDs in links
GDRIVE_REGEX = r"https://drive\.google\.com/(?:file/d/|open\?id=)([A-Za-z0-9_-]+)"

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(_, msg: Message):
    await msg.reply_text(
        "👋 Google Drive link එකක් එවන්න, video download කර ගන්නම්."
    )

@app.on_message(filters.private & filters.regex(GDRIVE_REGEX))
async def download_gdrive(_, msg: Message):
    link = msg.text.strip()
    m = re.search(GDRIVE_REGEX, link)
    if not m:
        return await msg.reply_text("❌ ඒක හරි Google Drive link එකක් නොවේ.")
    file_id = m.group(1)

    status = await msg.reply_text("⬇️ Downloading...")
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            "gdown",
            "--id", file_id,
            "--output", f"{tmp}/video"
        ]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode != 0:
            return await status.edit("❌ Download failed:\n" + res.stderr.decode())

        await status.edit("📤 Uploading...")
        await app.send_document(
            chat_id=msg.chat.id,
            document=f"{tmp}/video",
            caption=f"Downloaded from: {link}"
        )
        await status.delete()

@app.on_message(filters.private)
async def unknown(_, msg: Message):
    await msg.reply_text("Google Drive link එකක් එවන්න.")

if __name__ == "__main__":
    app.run()

