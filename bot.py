import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from gtts import gTTS

TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = FastAPI()

class TelegramUpdate(BaseModel):
    update_id: int
    message: dict | None = None

def send_audio(chat_id, file_path):
    with open(file_path, "rb") as f:
        url = f"{BASE_URL}/sendAudio"  # استفاده از sendAudio ساده
        files = {"audio": f}
        data = {"chat_id": chat_id}
        requests.post(url, data=data, files=files)

@app.post("/")
async def webhook(update: TelegramUpdate):
    if not update.message or "text" not in update.message:
        return {"ok": True}

    chat_id = update.message["chat"]["id"]
    text = update.message["text"]

    # تبدیل متن به صوت
    tts = gTTS(text=text, lang="en")  # برای تست، انگلیسی
    audio_file = "voice.mp3"
    tts.save(audio_file)

    send_audio(chat_id, audio_file)
    return {"ok": True}

@app.get("/")
def home():
    return {"message": "Telegram TTS Bot Running"}
