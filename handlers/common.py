# handlers/common.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.reply import main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """
    Обработчик команды /start
    """
    await state.clear() 
    await message.answer(
        "Здравствуйте! Я ИИ-ассистент TechAI.kz для преподавателей 🤖\n\n"
        "Я (теперь на базе Google Gemini) помогу вам автоматизировать подготовку к занятиям.\n"
        "Выберите действие в меню:",
        reply_markup=main_menu
    )

@router.message(F.text == "ℹ️ Помощь")
async def cmd_help(message: Message):
    """
    Обработчик кнопки 'Помощь'
    """
    await message.answer(
        "Я могу:\n\n"
        "📝 *План лекции/семинара:*\n"
        "   - Помогу составить план по дисциплине, курсу и теме.\n\n"
        "❓ *Создать тест:*\n"
        "   - Сделаю тест по вашей теме и уровню сложности.\n\n"
        "(Функция генерации изображений отключена, т.к. API Gemini от AI Studio ее не поддерживает).",
        parse_mode="Markdown"
    )