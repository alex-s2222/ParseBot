from telegram.ext import (
    Application,
    CommandHandler,
)

from handlers.start import start
from SETTINGS import TOKEN
def run():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.run_polling()
