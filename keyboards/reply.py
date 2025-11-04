# keyboards/reply.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 План лекции/семинара"),
            KeyboardButton(text="❓ Создать тест"),
        ],
        [
            KeyboardButton(text="ℹ️ Помощь"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие из меню:"
)