# test_telegram.py

import os
from dotenv import load_dotenv
import telegram

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

print(f"Token: {token}")
print(f"Chat ID: {chat_id}")

if not token or not chat_id:
    print("❌ Faltan credenciales en .env")
else:
    try:
        bot = telegram.Bot(token=token)
        bot.send_message(chat_id=chat_id, text="✅ ¡Prueba de notificación exitosa!")
        print("✅ Mensaje enviado correctamente")
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")