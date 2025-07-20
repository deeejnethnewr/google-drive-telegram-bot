# Google Drive Downloader Bot

මෙම Telegram බොට්ය Google Drive වීඩියෝ download කර Telegram වෙත upload කරයි.

---

## 🚀 Run on Google Cloud Shell

```bash
git clone https://github.com/deeejnethnewr/google-drive-telegram-bot.git
cd google-drive-telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
export BOT_TOKEN="ඔයාගේ_BOT_TOKEN"
export API_ID="ඔයාගේ_API_ID"
export API_HASH="ඔයාගේ_API_HASH"
nohup python bot.py &
