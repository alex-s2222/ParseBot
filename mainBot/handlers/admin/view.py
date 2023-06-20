from telegram import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)
from handlers.main_keyboard.view import MENUKEYBOARD

__stage = [i for i in range(1)]


time_subs_keyboard = [
    [
        InlineKeyboardButton('Добавить подписку', callback_data=str(__stage[0]))
    ],
]

back_button = [
        [
            InlineKeyboardButton("Назад", callback_data=str(__stage[0])),
        ],
]

back_menu = ReplyKeyboardMarkup([['⬅️ Назад в главное меню']], resize_keyboard=True, one_time_keyboard=True)

main_keyboard = ReplyKeyboardMarkup(MENUKEYBOARD, resize_keyboard=True)
