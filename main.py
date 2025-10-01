import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Token desde las variables de entorno de Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Diccionario para mensajes gratis
user_messages = {}

def start(update, context):
    user_id = update.message.from_user.id
    user_messages[user_id] = 0
    update.message.reply_text(
        "Hola, soy Alma Ibérica 😈\n"
        "Tienes 3 mensajes gratis conmigo… después tendrás que suscribirte 💋"
    )

def chat(update, context):
    user_id = update.message.from_user.id
    text = update.message.text
    
    if user_id not in user_messages:
        user_messages[user_id] = 0
    user_messages[user_id] += 1

    if user_messages[user_id] <= 3:
        reply = f"Alma: mmm… me calienta que me digas '{text}' 😏"
    else:
        reply = "Tus mensajes gratis se han acabado 😈.\nPara seguir conmigo tendrás que suscribirte 🔥."
    
    update.message.reply_text(reply)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    # Inicia el bot en modo polling (más fácil en Render)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
