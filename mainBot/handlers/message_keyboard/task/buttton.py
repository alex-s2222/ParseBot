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
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton
)

from model.data import DB
from .. import view

START_ROUTES, CHECK_INPUT_URL, INPUT_TITLE_FROM_URL, DELETE, BACK = range(5)


#TODO спросить нельзя ли в отдельный класс для реализации или разбить весь файл на маленькие подмодули
async def __tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    markup = InlineKeyboardMarkup(view.task_keyboard)
    await update.message.reply_markdown_v2(text='Переход в Задачи',reply_markup=view.back_menu)
    await update.message.reply_text("Выберете пункт меню", reply_markup=markup)
    
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
    return CHECK_INPUT_URL


async def __back_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """кнопка назад выводим главную главиатуру """
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(view.task_keyboard)

    await query.edit_message_text(text="Выберете пункт меню", reply_markup=reply_markup)
    return START_ROUTES


async def __insert_url(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """ввод пользователя ссылку на авито и выводим ввод title"""

    #сохраняем url от пользовалеля что бы сделать title
    url = update.message.text
    user_data = context.user_data
    user_data['url'] = url
    
    await update.message.reply_text(text="введите описание для введенной ссылки")

    return INPUT_TITLE_FROM_URL


async def __input_title_from_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """получаем и вставляем в базу данных url и title"""
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
    
    return CHECK_INPUT_URL



# переименовать функцию и придумать отдельный метод для вывода кнопок
async def __delete_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.callback_query.from_user.id
    query = update.callback_query

    await query.answer()

    urls = DB.get_urls(user_id=id)

    # проверка есть ли активные задачи у пользователя
    if not urls:
        reply_markup = InlineKeyboardMarkup(view.back_button)
        await query.edit_message_text(text="активных задач нет", reply_markup=reply_markup) 
        return BACK

    titles = [url['title'] for url in urls]
    reply_markup = InlineKeyboardMarkup(view.create_title_button(titles=titles))

    await query.edit_message_text(f"выберите задачу", reply_markup=reply_markup)
    return DELETE


async def __delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #получаем данные с нажатой кнопки и удаляем задачу 
    query = update.callback_query
    await query.answer()
    # получаем данные
    title_id = int(query.data)
    user_id = query.from_user.id
    
    urls = DB.get_urls(user_id=user_id)
    title = urls[title_id]['title']

    DB.delete_url_by_title(user_id=user_id, title=title)

    await query.message.edit_text(f'задача удаленна')


#TODO придумать как убрать последнюю ссылку  (не особо важное для красоты)
async def __information_about_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """выводит  url и title пользователя"""
    id = update.callback_query.from_user.id
    query = update.callback_query
    await query.answer()
    
    #получаем массив urls 
    urls = DB.get_urls(user_id=id)

    # проверка есть ли активные задачи у пользователя 
    if not urls:
        reply_markup = InlineKeyboardMarkup(view.back_button)
        await query.edit_message_text(text="активных задач нет", reply_markup=reply_markup) 
        return BACK

    # формируем сообщение
    output_message = ''
    for url in urls:
        output_message += '\t________' + url['title'] + '________\n' + url['user_url'] + '\n\n'

    await query.message.reply_text(f"{output_message}") 


async def __back_to_main_menu(update: Update, context:ContextTypes.DEFAULT_TYPE):
    """выводим клавиатуру меню и завершаем диалог"""
    await update.message.reply_text(text='Переход в главное меню', reply_markup=view.main_keyboard)
    return ConversationHandler.END


def tasks() -> ConversationHandler:
    ONE, TWO, THREE= range(3)

    task_handler = ConversationHandler(
            entry_points=[MessageHandler(filters.Regex("^🗃Задачи$"),__tasks)],
            states={
                START_ROUTES: [
                    CallbackQueryHandler(__create_task, pattern="^" + str(ONE) + "$"),
                    # CallbackQueryHandler(__edit_menu, pattern="^" + str(TWO) + "$"),
                    CallbackQueryHandler(__delete_menu, pattern="^" + str(TWO) + "$"),
                    CallbackQueryHandler(__information_about_task, pattern="^" + str(THREE) + "$"),
                ],
                CHECK_INPUT_URL: [ 
                    CallbackQueryHandler(__back_task, pattern="^" + str(ONE) + "$"),
                    MessageHandler(filters.Regex("^(https://www.avito.ru/|https://www.m.avito.ru)"), __insert_url),
                    MessageHandler(filters.TEXT, __check_insert_url)
                ],
                INPUT_TITLE_FROM_URL: [
                    MessageHandler(filters.TEXT, __input_title_from_user)
                ],
                DELETE: [
                    CallbackQueryHandler(__delete),
                ],
                BACK: [
                    CallbackQueryHandler(__back_task, pattern="^" + str(ONE) + "$"),
                ]
                
            },
            fallbacks=[MessageHandler(filters.Regex("^⬅️ Назад в главное меню$"),__back_to_main_menu),
                       ],
        )
    return task_handler

