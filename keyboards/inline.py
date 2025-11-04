# keyboards/inline.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_disciplines_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Машинное обучение", callback_data="discipline_ml")],
        [InlineKeyboardButton(text="Теория графов", callback_data="discipline_graphs")],
        [InlineKeyboardButton(text="Python (Asyncio)", callback_data="discipline_python")],
        [InlineKeyboardButton(text="Облачные вычисления", callback_data="discipline_cloud")],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel_action")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_courses_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="1 курс", callback_data="course_1"),
            InlineKeyboardButton(text="2 курс", callback_data="course_2"),
        ],
        [
            InlineKeyboardButton(text="3 курс", callback_data="course_3"),
            InlineKeyboardButton(text="4 курс", callback_data="course_4"),
        ],
         [InlineKeyboardButton(text="Отмена", callback_data="cancel_action")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)