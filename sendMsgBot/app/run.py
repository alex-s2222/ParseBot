from telegram.ext import (
    Application,
    CommandHandler,
)


def run():
    app = Application.builder().token().build()
    app.add_handler(CommandHandler("start", ...))

    app.run_polling()
