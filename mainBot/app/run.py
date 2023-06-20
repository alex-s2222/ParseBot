from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
    )

from SETTINGS import TOKEN
from handlers.main_keyboard import main
<<<<<<< HEAD
from handlers.message_keyboard.task.buttton import tasks
=======
from handlers.message_keyboard.task.button import tasks
from handlers.message_keyboard.subscription.button import subscription
from handlers.admin.admin_panel import admin_panel

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
>>>>>>> 6dc53bc (add admin panel)


def run():
    app = Application.builder().token(TOKEN).build()

<<<<<<< HEAD
    app.add_handler(CommandHandler("start", main.start))
    app.add_handler(MessageHandler(filters.Regex('^😎Аккаунт$')),main.account )
    app.add_handler(MessageHandler(filters.Regex("^📱Поддержка$"), None))
    #Перенести в message??
    app.add_handler(MessageHandler(filters.Regex("^💳 Продлить подписку$"), None))
    
=======

    app.add_handler(admin_panel())

>>>>>>> 6dc53bc (add admin panel)
    # button for tasks
    app.add_handler(tasks())



    app.run_polling()
    