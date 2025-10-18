import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from pyngrok import ngrok, conf
import uvicorn
import os

# 1️⃣ ВСТАВЬ СВОЙ NGROK TOKEN СЮДА (после регистрации на ngrok.com)
NGROK_AUTH_TOKEN = "34EKjunKTT5Eq6MVVCGOnuRtRp2_5ANwxdLKSscUVBqSFPwzM"

# 2️⃣ Добавляем токен в конфигурацию
conf.get_default().auth_token = NGROK_AUTH_TOKEN

# 3️⃣ Открываем публичный туннель для порта 8000
public_url = ngrok.connect(8000)
print(f"🌍 Публичный URL: {public_url}")

# 4️⃣ Запускаем FastAPI
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
