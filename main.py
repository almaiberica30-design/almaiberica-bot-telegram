import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# Token guardado en las variables de entorno de Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Dispatcher gestiona los mensajes
dispatcher = Dispatcher(bot, None, workers=0)

# Diccionario para contar mensajes de cada usuario (demo gratis)
user_messages = {}

# Mensaje inicial
def start(update, context):
    user_id = update.message.from_user.id
    user_messages[user_id] = 0
    update.message.reply_text(
        "Hola, soy Alma Ibérica 😈\n"
        "Tienes 3 mensajes gratis conmigo... después tendrás que suscribirte 💋"
    )

# Chat básico
def chat(update, context):
    user_id = update.message.from_user.id
    text = update.message.text
    
    # Contar mensajes
    if user_id not in user_messages:
        user_messages[user_id] = 0
    user_messages[user_id] += 1

    if user_messages[user_id] <= 3:
        # Respuestas calientes de ejemplo
        reply = f"Alma: mmm… me gusta que me digas '{text}', sigue… 😏"
    else:
        reply = "Tus mensajes gratis se han acabado 😈.\nPara seguir jugando conmigo tendrás que suscribirte 🔥."
    
    update.message.reply_text(reply)

# Handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

# Endpoint del webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Página de prueba
@app.route("/")
def index():
    return "Alma Bot está vivo 💋"

# Iniciar servidor en Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
