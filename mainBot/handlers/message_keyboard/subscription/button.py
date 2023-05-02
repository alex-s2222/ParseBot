from telegram.ext import (
    ConversationHandler,
    filters,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ReplyKeyboardMarkup
)

from . import view

INPUT = range(1)


async def __send_time_subs(update: Update, context:ContextTypes.DEFAULT_TYPE):
    """выводим кнопки с временем для для продления подписки """
    reply_markup = InlineKeyboardMarkup(view.time_subs_keyboard)
    
    await update.message.reply_text("Выберите время продления", reply_markup=reply_markup)
    return INPUT


async def __send_qiwi_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    time_url = query.data

    await query.message.edit_text(text=f'{time_url}')



def subscription():
    ONE, TWO, THREE= range(3)

    subscription_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^💳 Продлить подписку$"), __send_time_subs)],
        states={
            INPUT:[
                CallbackQueryHandler(__send_qiwi_url),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^💳 Продлить подписку$"), __send_time_subs)],
    )

    return subscription_handler