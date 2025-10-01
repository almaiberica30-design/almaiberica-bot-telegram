import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot, None, workers=0)
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

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/")
def index():
    return "Alma Bot está vivo 💋"

# Render necesita gunicorn en producción, pero dejamos esto por si corres localmente
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render usa PORT automáticamente
    app.run(host="0.0.0.0", port=port)
