from telegram.ext import (
    ContextTypes
)
    
from telegram import (
    Update,
)
from telegram.constants import ParseMode

from parseUrl.Parse import parseUrl
from model.data import DB
from loguru import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """парсит url из бд пользователя""" 
    user_id = update.message.from_user.id
    logger.debug(f'User: {user_id} press start')
    try:
        # удаляем работу 
        job_removed = remove_job_if_exists(str(user_id), context)
        
        context.job_queue.run_once(
            create_task, 5, chat_id=user_id, name=str(user_id), data=5)
        
        context.job_queue.run_repeating(
            create_task, 30, chat_id=user_id, name=str(user_id), data=30)
    
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Напишите /start")


async def create_task(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    
    if DB.check_user_subscription(user_id=job.chat_id):
        # если у пользователя нет подписки
        remove_job_if_exists(str(job.chat_id), context)
        text = 'Оплатите подписку в основном боте, что бы продолжить пользоваться ботом'

        logger.debug(f'User:{job.chat_id} END subscription')

        await context.bot.send_message(job.chat_id, text=text)
    else:
        # запускаем парсер
        data_urls = await parseUrl().get_message(user_id=job.chat_id)
        
        logger.debug(f'{job.chat_id} DATA {data_urls}')
        
        for data_url in data_urls:
            for title, url in data_url.items():
                if url:
                    msq = f'#{title.replace(" ", "_")} \n'  +\
                            f'👉\t{url["name"]} \n\n' +\
                            f'💸\t{url["price"]} ₽ \n\n' +\
                            f'📍\t{url["location"]} \n\n'+\
                            f'✅\t' + f'<a href="{url["output_user_url"]}">Ссылка</a>'
                    await context.bot.send_message(job.chat_id, text=msq, parse_mode=ParseMode.HTML)
                else:
                    continue


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True