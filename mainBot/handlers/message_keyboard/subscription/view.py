from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from handlers.main_keyboard.view import MENUKEYBOARD


__stage = [i for i in range(3)]

time_subs_keyboard = [
    [InlineKeyboardButton('1 день', callback_data=str(__stage[0]))],
    [InlineKeyboardButton('1 неделя', callback_data=str(__stage[1]))],
    [InlineKeyboardButton('1 месяц', callback_data=str(__stage[2]))],
]