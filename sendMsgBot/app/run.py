from telegram.ext import (
    Application,
    CommandHandler,
)
import os 

from handlers.start import start


def run():
    TOKEN = os.environ['TOKEN']
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.run_polling()
