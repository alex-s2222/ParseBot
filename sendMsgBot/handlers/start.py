from telegram.ext import (
    ContextTypes
)
    
from telegram import (
    Update,
)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """парсит url из бд пользователя""" 
    user_id = update.message.from_user.id
    try:
        # удаляем работу 
        job_removed = remove_job_if_exists(str(user_id), context)
        
        context.job_queue.run_once(
            alarm, 5, chat_id=user_id, name=str(user_id), data=5)
        
        context.job_queue.run_repeating(
            alarm, 30, chat_id=user_id, name=str(user_id), data=30)
    
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Напишите /start")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send the alarm message."""
    job = context.job

    # запускаем парсер
    out_message = get_url(job.chat_id)
    if out_message:
        await context.bot.send_message(job.chat_id, text=out_message)
    else:
        return


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True