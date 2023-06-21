from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ContextTypes,
)

from telegram import (
    Update,
    ReplyKeyboardMarkup,
)

from model.data import DB
from .view import MENUKEYBOARD

markup = ReplyKeyboardMarkup(MENUKEYBOARD, one_time_keyboard=True, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start message from user and output keyboard"""
    #TODO Delete this, for testing or no 
    # id = update.message.from_user.id
    # DB.insert_default_user(user_id=id)

    await update.message.reply_text(
        'Добро пожаловать в \n <<MyParseAvito>>',
        reply_markup=markup,
    )


async def account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """выводит информацию о аккаунте"""
    user_id = update.message.from_user.id

<<<<<<< HEAD
    #TODO придумать реализацию (время подписки) && (кол-во активных задач ...придумать логику реализацию)
    answer_message = f"Ваш ID {user_id}\n"+\
                        "Подписка доступно до ...\n" +\
                         "Количестнов активных задач ..."
=======
    active_urls = len(DB.get_urls(user_id=user_id))
    end_subs = DB.get_user_subsctription(user_id=user_id).date()

    answer_message = f"Ваш ID: {user_id}\n"+\
                        f"Подписка доступно до: {end_subs.day}.{end_subs.month}.{end_subs.year}\n" +\
                         f"Количестнов активных задач: {active_urls}/5"
    
    logger.log('USER', f'User:{user_id} check info account')
>>>>>>> f11ddcb (v2.1)
    
    await update.message.reply_text(answer_message)
