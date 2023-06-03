from telegram.ext import (
    ContextTypes,
)

from telegram import (
    Update,
    ReplyKeyboardMarkup,
)

from model.data import DB
from .view import MENUKEYBOARD

from loguru import logger 
import sys

markup = ReplyKeyboardMarkup(MENUKEYBOARD, one_time_keyboard=True, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start message from user and output keyboard"""
    user_id = update.message.from_user.id


    # проверка что пользователя нет в базе данных
    if not DB.check_user_from_db(user_id=user_id):
        DB.insert_default_user(user_id=user_id)
        logger.log('USER', f'User:{user_id} add DB')

    
    await update.message.reply_text(
        'Добро пожаловать в \n <<MyParseAvito>>',
        reply_markup=markup,
    )


async def account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """выводит информацию о аккаунте"""
    user_id = update.message.from_user.id

    active_urls = len(DB.get_urls(user_id=user_id))

    #TODO придумать реализацию (время подписки)
    answer_message = f"Ваш ID {user_id}\n"+\
                        "Подписка доступно до ...\n" +\
                         f"Количестнов активных задач {active_urls}"
    
    logger.log('USER', f'User:{user_id} check info account')
    
    await update.message.reply_text(answer_message)
