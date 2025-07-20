# Google Drive Downloader Bot

මෙම Telegram බොට්ය Google Drive වීඩියෝ download කර Telegram වෙත upload කරයි.

---

## 🚀 Run on Google Cloud Shell

```bash
# 1) Clone කරන්න
git clone https://github.com/YOUR_USERNAME/gdrive-downloader-bot.git
cd gdrive-downloader-bot

# 2) Virtualenv සකසන්න
python3 -m venv venv
source venv/bin/activate

# 3) Dependencies install කරන්න
pip install --upgrade pip
pip install -r requirements.txt

# 4) Env vars setzen කරන්න
export BOT_TOKEN="ඔයාගේ_BOT_TOKEN"
export API_ID="ඔයාගේ_API_ID"
export API_HASH="ඔයාගේ_API_HASH"

# 5) Bot run කරන්න
nohup python bot.py &
