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
        'Добро пожаловать в \n<<MyParseAvito>> \n\nВам дана тестовая подписка на 1 день',
        reply_markup=markup)

        out_message = __create_message()
        await update.message.reply_text(out_message)
        
    #если пользователь есть в базе данных    
    else:
        await update.message.reply_text(
            'Добро пожаловать в \n<<MyParseAvito>>',
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


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    out_message = __create_message()

    await update.message.reply_text(out_message)


def __create_message() -> str:
    MY_ACCOUNT = '@Juzorai'
    BOT_ACCOUNT = '@My_parse_avito_bot'
    GROUP_ACCOUNT = 'https://t.me/+Sj_NseMkPHU5NDAy'

    out_message =  f'Новости, улучшения, дополнения, перерывы \n👉{GROUP_ACCOUNT}\n\n' +\
                    f'Бот для получения уведомлений \n👉{BOT_ACCOUNT}\n\n' +\
                     f'Если возникли вопросы по использованию или есть пожелания пишите \n👉{MY_ACCOUNT}'
    
    return out_message
