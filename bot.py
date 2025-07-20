from pyrogram import Client, filters
import os
import requests
import re
import asyncio

API_ID = 15647296
API_HASH = "0cb3f4a573026b56ea80e1c8f039ad6a"
BOT_TOKEN = "8144738030:AAHDWFS8B68PBdbp7ljukTriy-QlA414tV4"

app = Client("gdrive_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to extract file id from Google Drive link
def extract_gdrive_id(url):
    patterns = [
        r"https?://drive\.google\.com/file/d/([^/]+)/?.*",
        r"https?://drive\.google\.com/open\?id=([^&]+)",
        r"https?://drive\.google\.com/uc\?id=([^&]+)&?.*"
    ]
    for pattern in patterns:
        m = re.match(pattern, url)
        if m:
            return m.group(1)
    return None

async def download_file(file_id, filename, message):
    URL = f"https://drive.google.com/uc?export=download&id={file_id}"

    session = requests.Session()

    response = session.get(URL, stream=True)
    token = None

    # Get confirmation token for large files
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    total_size = int(response.headers.get('content-length', 0))
    chunk_size = 1024 * 1024  # 1MB

    downloaded = 0
    with open(filename, "wb") as f:
        async for chunk in async_requests(response, chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = downloaded * 100 / total_size if total_size else 0
                await message.edit(f"📥 Downloading: {percent:.2f}%\n{downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB")

async def async_requests(response, chunk_size):
    loop = asyncio.get_event_loop()
    for chunk in response.iter_content(chunk_size):
        yield await loop.run_in_executor(None, lambda: chunk)

@app.on_message(filters.private & filters.text)
async def handle_private(client, message):
    url = message.text.strip()
    file_id = extract_gdrive_id(url)
    if not file_id:
        await message.reply("❌ මෙය Google Drive link එකක් නොවේ. කරුණාකර Google Drive link එකක් පමණක් එවන්න.")
        return

    await_message = await message.reply("🔄 Google Drive link එක සැකසෙමින් ඇත...")

    filename = f"{file_id}.file"

    try:
        await download_file(file_id, filename, await_message)
        await await_message.edit(f"✅ Download සම්පූර්ණයි!\nගොනුව: `{filename}`")
        # File saved locally - Runway / cloud environment ඉන් පසුව clean-up හොයාගන්න ඕන.
        os.remove(filename)
    except Exception as e:
        await await_message.edit(f"❌ දෝෂයක් සිදු විය: {e}")

app.run()

