from telegram.ext import (
    ConversationHandler,
    filters,
    CallbackQueryHandler,
    MessageHandler, 
    CommandHandler,
    ContextTypes,
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup, 
    Update,
    ReplyKeyboardMarkup
)

from model.data import DB
from . import view

START_ROUTES, CHECK_INPUT_ROUTES, INPUT_TITLE = range(3)



#TODO спросить нельзя ои в отдельный класс для реализации или разбить весь файл на маленькие подмодули
async def __tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reply_markup = InlineKeyboardMarkup(view.task_keyboard)

    await update.message.reply_text("Выберете пункт меню", reply_markup=reply_markup)

    return START_ROUTES


#TODO rewrite output message delete input url 
async def __create_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """просим пользователя ввести ссылку, выводим кноаку назад """
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(view.back_button)
 
    await query.edit_message_text(
        text="Введите ссылку на avito", reply_markup=reply_markup
    ) 
    return CHECK_INPUT_ROUTES


async def __back_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """кнопка назад выводим главную главиатуру """
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(view.task_keyboard)

    await query.edit_message_text(text="Выберете пункт меню", reply_markup=reply_markup)
    return START_ROUTES


async def __insert_url(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """ввод пользователя ссылку на авито и выводим ввод titl """

    #сохраняем url от пользовалеля что бы сделать title
    url = update.message.text
    user_data = context.user_data
    user_data['url'] = url
    
    reply_markup = InlineKeyboardMarkup(view.back_button)
    await update.message.reply_text(text="введите описание для введенной ссылки", reply_markup=reply_markup)

    return INPUT_TITLE


async def __input_title_from_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.message.from_user.id
    title = update.message.text
    user_data = context.user_data

    DB.insert_user_url_in_arr(user_id=id,insert_user_url=user_data['url'])
    DB.set_title_url(user_id=id, user_url=user_data['url'], title=title)

    user_data.clear()

    await update.message.reply_text(f"ссылка и описание внесенны", reply_markup=view.main_keyboard)
    return ConversationHandler.END


async def __check_insert_url(update:Update, context: ContextTypes.DEFAULT_TYPE):
    """пользователь ввел неправильную ссылку на avito"""

    reply_markup = InlineKeyboardMarkup(view.back_button)
    await update.message.reply_text(f"Ошибка, введите корректную ссылку на авито", reply_markup=reply_markup)
    
    return CHECK_INPUT_ROUTES


async def edit_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def information_about_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

def tasks() -> ConversationHandler:
    ONE, TWO, THREE, FOUR = range(4)

    task_handler = ConversationHandler(
            entry_points=[MessageHandler(filters.Regex("^🗃Задачи$"),__tasks)],
            states={
                START_ROUTES: [
                    CallbackQueryHandler(__create_task, pattern="^" + str(ONE) + "$"),
                    CallbackQueryHandler(edit_task, pattern="^" + str(TWO) + "$"),
                    CallbackQueryHandler(delete_task, pattern="^" + str(THREE) + "$"),
                    CallbackQueryHandler(information_about_task, pattern="^" + str(FOUR) + "$"),
                ],
                CHECK_INPUT_ROUTES: [ 
                    CallbackQueryHandler(__back_task, pattern="^" + str(ONE) + "$"),
                    MessageHandler(filters.Regex("^(https://www.avito.ru/|https://www.m.avito.ru)"), __insert_url),
                    MessageHandler(filters.TEXT, __check_insert_url)
                ],
                INPUT_TITLE: [
                    MessageHandler(filters.TEXT, __input_title_from_user)
                ],
                
            },
            fallbacks=[CommandHandler("start", ... )],
        )
    return task_handler

