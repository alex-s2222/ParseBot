from telegram.ext import (
    ContextTypes
)
    
from telegram import (
    Update,
)

from parseUrl.Parse import parseUrl


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """парсит url из бд пользователя""" 
    user_id = update.message.from_user.id
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

    # запускаем парсер
    data_urls = await parseUrl().get_message(user_id=job.chat_id)

    # delete
    from pprint import pprint
    pprint(data_urls)


    for data_url in data_urls:
        for title, url in data_url.items():
            if url:
                msq = f'\t#{title} \n'  +\
                        f'{url["output_user_url"]} \n' +\
                        f'{url["name"]} \n' +\
                        f'{url["price"]} \n'
                await context.bot.send_message(job.chat_id, text=msq)
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