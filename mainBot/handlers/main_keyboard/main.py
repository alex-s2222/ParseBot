from telegram.ext import (
    ContextTypes,
)

from telegram import (
    Update,
    ReplyKeyboardMarkup,
)

from loguru import logger
from datetime import datetime, timedelta

from model.data import DB
from .view import MENUKEYBOARD


markup = ReplyKeyboardMarkup(MENUKEYBOARD, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start message from user and output keyboard"""
    user_id = update.message.from_user.id

    # проверка что пользователя нет в базе данных
    if not DB.check_user_from_db(user_id=user_id):
        # добавляем нового пользователя с тестовым днем
        now = datetime.now()
        end = now + timedelta(hours=24)
    
        DB.insert_default_user(user_id=user_id, date_now=now, date_end=end)
        logger.log('USER', f'User:{user_id} add DB')

        await update.message.reply_text(
        'Добро пожаловать в \n <<MyParseAvito>>',
        reply_markup=markup)
    #если пользователь есть в базе данных    
    else:
        await update.message.reply_text(
            'Добро пожаловать в \n <<MyParseAvito>>',
            reply_markup=markup,
        )


async def account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """выводит информацию о аккаунте"""
    user_id = update.message.from_user.id

    active_urls = len(DB.get_urls(user_id=user_id))
    end_subs = DB.get_user_subsctription(user_id=user_id).date()

    answer_message = f"Ваш ID: {user_id}\n"+\
                        f"Подписка доступно до: {end_subs.day}.{end_subs.month}.{end_subs.year}\n" +\
                         f"Количестнов активных задач: {active_urls}"
    
    logger.log('USER', f'User:{user_id} check info account')
    
    await update.message.reply_text(answer_message)
