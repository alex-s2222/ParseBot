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

from .. import view

INPUT = range(1)


async def __send_time_subs(update: Update, context:ContextTypes.DEFAULT_TYPE):
    """выводим кнопки с временем для для продления подписки """
    reply_markup = InlineKeyboardMarkup(view.time_subs_keyboard)
    await update.message.reply_markdown_v2(text='Переход в Подписки', reply_markup=view.back_menu)
    await update.message.reply_text("Выберите время продления", reply_markup=reply_markup)
    return INPUT


async def __send_qiwi_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #TODO нет риализации 
    query = update.callback_query
    await query.answer()
    
    time_url = query.data

    MY_ACCOUNT = '@Juzorai'
    out_message = f'Для оплаты и выбора лимита пишите\n👉{MY_ACCOUNT}'

    await query.message.edit_text(text=out_message)

    
async def __back_to_main_menu(update: Update, context:ContextTypes.DEFAULT_TYPE):
    """выводим клавиатуру меню и завершаем диалог"""
    await update.message.reply_text(text='Переход в главное меню', reply_markup=view.main_keyboard)
    return ConversationHandler.END



def subscription():
    ONE, TWO, THREE= range(3)

    subscription_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^💳 Продлить подписку$"), __send_time_subs)],
        states={
            INPUT:[
                CallbackQueryHandler(__send_qiwi_url),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^⬅️ Назад в главное меню$"),__back_to_main_menu)],
    )

    return subscription_handler