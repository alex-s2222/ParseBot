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

START_ROUTES, CHECK_INPUT_ROUTES = range(2)
ONE, TWO, THREE, FOUR = range(4)


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
    """вставляем ссылку в базу данных и выводим главную клавиатуру """
    id = update.message.from_user.id
    message = update.message.text

    DB.insert_user_url_in_arr(user_id=id,insert_user_url=message)

    await update.message.reply_text(f"ссылка внесена", reply_markup=view.main_keyboard)
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
    #TODO white routes this place >>
    
    #   >>

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

            },
            fallbacks=[CommandHandler("start", ... )],
        )
    return task_handler

