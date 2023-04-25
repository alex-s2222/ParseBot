from telegram import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)
from typing import List

from handlers.main_keyboard.view import MENUKEYBOARD


__stage = [i for i in range(4)]

task_keyboard = [
        [InlineKeyboardButton('Создать задачу', callback_data=str(__stage[0]))],
        [InlineKeyboardButton('Редактировать', callback_data=str(__stage[1]))],
        [InlineKeyboardButton('Удалить задачу',callback_data=str(__stage[2]))],
        [InlineKeyboardButton('Информация о задачах', callback_data=str(__stage[3]))],
    ]

back_button = [
        [
            InlineKeyboardButton("Назад", callback_data=str(__stage[0])),
        ],
]

main_keyboard = ReplyKeyboardMarkup(MENUKEYBOARD, one_time_keyboard=True, resize_keyboard=True)


#TODO нужно сделать проверку на уникальность вводимых title 
def create_title_button(titles: list) -> List[InlineKeyboardButton] :
    """создаем кнопки из title"""
    titles_keyboard = []

    for i , title in enumerate(titles):
            titles_keyboard.append([InlineKeyboardButton(title, callback_data=str(i))])

    return titles_keyboard