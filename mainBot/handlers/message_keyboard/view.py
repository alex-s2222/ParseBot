from telegram import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)
from typing import List

from handlers.main_keyboard.view import MENUKEYBOARD


__stage = [i for i in range(3)]

task_keyboard = [
        [InlineKeyboardButton('Создать задачу', callback_data=str(__stage[0]))],
        # [InlineKeyboardButton('Редактировать', callback_data=str(__stage[1]))],
        [InlineKeyboardButton('Удалить задачу',callback_data=str(__stage[1]))],
        [InlineKeyboardButton('Информация о задачах', callback_data=str(__stage[2]))],
    ]

back_button = [
        [
            InlineKeyboardButton("Назад", callback_data=str(__stage[0])),
        ],
]

time_subs_keyboard = [
    [InlineKeyboardButton('1 день', callback_data=str(__stage[0]))],
    [InlineKeyboardButton('1 неделя', callback_data=str(__stage[1]))],
    [InlineKeyboardButton('1 месяц', callback_data=str(__stage[2]))],
]

main_keyboard = ReplyKeyboardMarkup(MENUKEYBOARD, resize_keyboard=True)

back_menu = ReplyKeyboardMarkup([['⬅️ Назад в главное меню']], resize_keyboard=True, one_time_keyboard=True)


def create_title_button(titles: list) -> List[InlineKeyboardButton] :
    """создаем кнопки из title"""
    titles_keyboard = []

    for i , title in enumerate(titles):
            titles_keyboard.append([InlineKeyboardButton(title, callback_data=str(i))])

    return titles_keyboard