from telegram.ext import (
    ConversationHandler,
    filters,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
)

from telegram import (
    InlineKeyboardMarkup,
    Update,
)

from loguru import logger

from model.data import DB
from .. import view

START_ROUTES, CHECK_INPUT_URL, INPUT_TITLE_FROM_URL, DELETE, BACK = range(5)


async def __tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """переход в разговор Задачи"""
    user_id = update.message.from_user.id
    markup = InlineKeyboardMarkup(view.task_keyboard)
    await update.message.reply_markdown_v2(text='Переход в Задачи', reply_markup=view.back_menu)
    await update.message.reply_text("Выберете пункт меню", reply_markup=markup)

    logger.log("USER", f"User: {user_id} pressed to tasks")

    return START_ROUTES


# TODO сделать проверку на подписку
async def __create_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """просим пользователя ввести ссылку, выводим кноаку назад """
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    reply_markup = InlineKeyboardMarkup(view.back_button)

    await query.edit_message_text(
        text="Введите ссылку на avito", reply_markup=reply_markup
    )

    logger.log('USER', f'User {user_id} press input url')

    return CHECK_INPUT_URL


async def __back_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """кнопка назад выводим главную главиатуру """
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    reply_markup = InlineKeyboardMarkup(view.task_keyboard)

    await query.edit_message_text(text="Выберете пункт меню", reply_markup=reply_markup)

    logger.log('USER', f'User: {user_id} press back button')

    return START_ROUTES


async def __insert_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ввод пользователя ссылку на авито и выводим ввод title"""
    user_id = update.message.from_user.id
    # сохраняем url от пользовалеля что бы сделать title
    url = update.message.text
    user_data = context.user_data
    user_data['url'] = url

    await update.message.reply_text(text="введите описание для введенной ссылки")

    logger.log('USER', f'User: {user_id} input title for url')

    return INPUT_TITLE_FROM_URL


async def __input_title_from_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """получаем и вставляем в базу данных url и title"""
    user_id = update.message.from_user.id
    title = update.message.text
    user_data = context.user_data
    
    # проверяем уникальность вводимого описания пользователем
    if DB.check_user_titles(user_id=user_id, user_title=title):
        await update.message.reply_text(f'Задача с таким описанием уже существует, придумайте уникальное описание')
        return INPUT_TITLE_FROM_URL

    DB.insert_user_url_and_title(user_id=user_id, user_url=user_data['url'], user_title=title)

    user_data.clear()

    logger.log('USER', f'User {user_id} insert url and title in DB')

    await update.message.reply_text(f"ссылка и описание внесенны", reply_markup=view.main_keyboard)
    return ConversationHandler.END


async def __check_insert_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """пользователь ввел неправильную ссылку на avito"""
    reply_markup = InlineKeyboardMarkup(view.back_button)
    await update.message.reply_text(f"Ошибка, введите корректную ссылку на авито", reply_markup=reply_markup)

    return CHECK_INPUT_URL


async def __delete_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    query = update.callback_query

    await query.answer()

    urls = DB.get_urls(user_id=user_id)

    # проверка есть ли активные задачи у пользователя
    if not urls:
        reply_markup = InlineKeyboardMarkup(view.back_button)
        await query.edit_message_text(text="активных задач нет", reply_markup=reply_markup)
        return BACK

    titles = [url['title'] for url in urls]
    reply_markup = InlineKeyboardMarkup(
        view.create_title_button(titles=titles))

    logger.log('USER', f'User {user_id} view task for delete')

    await query.edit_message_text(f"выберите задачу", reply_markup=reply_markup)
    return DELETE


async def __delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # получаем данные с нажатой кнопки и удаляем задачу
    query = update.callback_query
    await query.answer()
    # получаем данные
    title_id = int(query.data)
    user_id = query.from_user.id

    # обрабатываем данные
    urls = DB.get_urls(user_id=user_id)
    title = urls[title_id]['title']

    # удаляем задачу из баззы данных
    DB.delete_url_by_title(user_id=user_id, title=title)

    # создаем кнопку назад к задачам
    reply_markup = InlineKeyboardMarkup(view.back_button)

    logger.log('USER', f'User {user_id} delete task')

    await query.message.edit_text(f'задача удаленна', reply_markup=reply_markup)
    return BACK


async def __information_about_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """выводит задачи и их назавние пользователю"""
    user_id = update.callback_query.from_user.id
    query = update.callback_query
    await query.answer()

    # получаем массив urls
    urls = DB.get_urls(user_id=user_id)

    # проверка есть ли активные задачи у пользователя
    if not urls:
        back_button = InlineKeyboardMarkup(view.back_button)
        await query.edit_message_text(text="активных задач нет", reply_markup=back_button)
        return BACK

    # формируем сообщение
    output_message = ''
    for url in urls:
        output_message += '\t________' + \
            url['title'] + '________\n' + url['user_url'] + '\n\n'

    back_button = InlineKeyboardMarkup(view.back_button)

    logger.log('USER', f'User {user_id}  view information about tasks')

    await query.message.edit_text(f"{output_message}", reply_markup=back_button)

    return BACK


async def __back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """выводим клавиатуру меню и завершаем диалог"""
    user_id = update.message.from_user.id

    # очищаем данные пользователя на всякий случай
    context.user_data.clear()

    await update.message.reply_text(text='Переход в главное меню', reply_markup=view.main_keyboard)

    logger.log('USER', f'User {user_id} back to main menu')

    return ConversationHandler.END


def tasks() -> ConversationHandler:
    ONE, TWO, THREE = range(3)

    task_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^🗃Задачи$"), __tasks)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(
                    __create_task, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(
                    __delete_menu, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(
                    __information_about_task, pattern="^" + str(THREE) + "$"),
            ],
            CHECK_INPUT_URL: [
                CallbackQueryHandler(
                    __back_task, pattern="^" + str(ONE) + "$"),
                    
                #TODO |^(https://m.avito.ru) 
                MessageHandler(filters.Regex("^(https://www.avito.ru/)"), __insert_url),
                MessageHandler(filters.TEXT, __check_insert_url)
            ],
            INPUT_TITLE_FROM_URL: [
                MessageHandler(filters.TEXT, __input_title_from_user)
            ],
            DELETE: [
                CallbackQueryHandler(__delete),
            ],
            BACK: [
                CallbackQueryHandler(
                    __back_task, pattern="^" + str(ONE) + "$"),
            ]

        },
        fallbacks=[MessageHandler(filters.Regex("^⬅️ Назад в главное меню$"), __back_to_main_menu),
                   ],
    )
    return task_handler
