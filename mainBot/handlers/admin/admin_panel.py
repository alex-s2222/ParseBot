from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    filters,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
)

from telegram import (
    InlineKeyboardMarkup,
    Update,
)

from model.data import DB

from SETTINGS import USER_ID
from . import view

START_ROUTES, INPUT_DATA = range(2)


async def __admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Введите пароль для входа """
    user_id = update.message.from_user.id

    time_subs = InlineKeyboardMarkup(view.time_subs_keyboard)
    # проверяем id user
    if user_id == USER_ID:
        await update.message.reply_text(text='Админ', reply_markup=view.back_menu)
        await update.message.reply_text(text='Выберете дейсвие', reply_markup=time_subs)

        return START_ROUTES
    else:
        return ConversationHandler.END


async def __add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    back_button = InlineKeyboardMarkup(view.back_button)
    await query.edit_message_text(text='введите id  время 12 mwd', reply_markup=back_button)

    return INPUT_DATA


async def __input_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_from_user = update.message.text.split()
    try:
        user_id, number_time, string_time = message_from_user

        if DB.admin_set(user_id=int(user_id), number_time=int(number_time), string_time=string_time):

            await update.message.reply_text('Данные обновленны')
            await update.message.reply_text(text='Переход в главное меню', reply_markup=view.main_keyboard)
            return ConversationHandler.END
        else:
            await update.message.reply_text('Ошибка')
    except:
        await update.message.reply_text('Ошибка')


async def __back_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    time_subs = InlineKeyboardMarkup(view.time_subs_keyboard)

    await query.edit_message_text(text='Выберете дейсвие', reply_markup=time_subs)

    return START_ROUTES


async def __back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """выводим клавиатуру меню и завершаем диалог"""
    await update.message.reply_text(text='Переход в главное меню', reply_markup=view.main_keyboard)

    return ConversationHandler.END


def admin_panel() -> ConversationHandler:
    ONE, TWO, THREE = range(3)

    admin_handlers = ConversationHandler(
        entry_points=[CommandHandler('admin_panel', __admin_panel)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(__add_user, pattern="^" + str(ONE) + "$"),
            ],
            INPUT_DATA: [
                CallbackQueryHandler(
                    __back_button, pattern="^" + str(ONE) + "$"),
                MessageHandler(filters.TEXT, __input_data)
            ],

        },
        fallbacks=[MessageHandler(filters.Regex("^⬅️ Назад в главное меню$"), __back_to_main_menu),
                   ],
    )

    return admin_handlers
