import os
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from gtts import gTTS

TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = FastAPI()

class TelegramUpdate(BaseModel):
    update_id: int
    message: dict | None = None

def send_voice(chat_id, file_path):
    with open(file_path, "rb") as f:
        url = f"{BASE_URL}/sendVoice"
        files = {"voice": f}
        data = {"chat_id": chat_id}
        requests.post(url, data=data, files=files)

@app.post("/")
async def webhook(update: TelegramUpdate):
    if not update.message:
        return {"ok": True}

    chat_id = update.message["chat"]["id"]

    if "text" in update.message:
        text = update.message["text"]

        # تبدیل متن به صوت
        tts = gTTS(text=text, lang="fa")
        tts.save("voice.mp3")

        # تبدیل mp3 → ogg
        os.system("ffmpeg -i voice.mp3 -c:a libopus voice.ogg -y")

        send_voice(chat_id, "voice.ogg")

    return {"ok": True}

@app.get("/")
def home():
    return {"message": "Telegram TTS Bot Running"}

if __name__ == "__main__":
    uvicorn.run("bot:app", host="0.0.0.0", port=5000)
