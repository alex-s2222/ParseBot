from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
    )

from SETTINGS import TOKEN
from handlers.main_keyboard import main
from handlers.message_keyboard.task.buttton import tasks
from handlers.message_keyboard.subscription.button import subscription

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning


def run():
    app = Application.builder().token(TOKEN).build()
    
    
    # disabling warning
    filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
    
    # app.persistence
    app.add_handler(CommandHandler("start", main.start))
    app.add_handler(MessageHandler(filters.Regex('^😎Аккаунт$'),main.account))
    app.add_handler(MessageHandler(filters.Regex("^📱Поддержка$"), ...))

    # button for tasks
    app.add_handler(tasks())

    # button for subs 
    app.add_handler(subscription())



    app.run_polling()
    