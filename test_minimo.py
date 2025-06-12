import telegram

TOKEN = "8127716556:AAHw6rmaFCb-yd63spmW5dwXIGXqcolqJBU"  # Reemplaza con tu token
CHAT_ID = "7934822888"  # Reemplaza con tu chat ID

bot = telegram.Bot(token=TOKEN)
response = bot.get_me()
print("Bot info:", response)

# Enviar mensaje
bot.send_message(chat_id=CHAT_ID, text="Hola desde mi IA bursátil")
print("✅ Mensaje enviado")