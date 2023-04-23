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
    #TODO Delete this, for testing
    id = update.message.from_user.id
    DB.insert_default_user(user_id=id)

    await update.message.reply_text(
        'Добро пожаловать в \n <<MyParseAvito>>',
        reply_markup=markup,
    )


async def account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """выводит информацию о аккаунте"""
    user_id = update.message.from_user.id

    #TODO придумать реализацию (время подписки) && (кол-во активных задач ...придумать логику реализацию)
    answer_message = f"Ваш ID {user_id}\n"+\
                        "Подписка доступно до ...\n" +\
                         "Количестнов активных задач ..."
    
    await update.message.reply_text(answer_message)
