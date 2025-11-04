# handlers/test_handler.py

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from states.generation import TestGeneration
from keyboards.inline import get_disciplines_keyboard
from utils import api_client

router = Router()

def get_difficulty_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Легкий", callback_data="difficulty_easy"),
            InlineKeyboardButton(text="Средний", callback_data="difficulty_medium"),
        ],
        [
            InlineKeyboardButton(text="Сложный (с эссе)", callback_data="difficulty_hard")
        ],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel_action")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(F.text == "❓ Создать тест")
async def start_test(message: Message, state: FSMContext):
    await state.set_state(TestGeneration.waiting_for_discipline)
    await message.answer(
        "Вы выбрали создание теста.\nПожалуйста, выберите **дисциплину**:",
        reply_markup=get_disciplines_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(TestGeneration.waiting_for_discipline)
async def select_discipline(callback: CallbackQuery, state: FSMContext):
    
    full_discipline_name = ""
    for row in callback.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                full_discipline_name = button.text
                break
    
    await state.update_data(discipline=full_discipline_name)
    
    await state.set_state(TestGeneration.waiting_for_topic)
    await callback.message.edit_text(
        f"Дисциплина: {full_discipline_name}. Теперь введите **тему** для теста:"
    )
    await callback.answer()

@router.message(TestGeneration.waiting_for_topic)
async def get_topic(message: Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await state.set_state(TestGeneration.waiting_for_count)
    await message.answer("Тема принята. Теперь введите **количество вопросов** (например, 10):")


@router.message(TestGeneration.waiting_for_count)
async def get_count(message: Message, state: FSMContext):
  
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число (например, 5, 10, 20).")
        return
    
    await state.update_data(count=int(message.text))
    await state.set_state(TestGeneration.waiting_for_difficulty)
    await message.answer(
        "Отлично. Теперь выберите **уровень сложности**:",
        reply_markup=get_difficulty_keyboard()
    )

@router.callback_query(TestGeneration.waiting_for_difficulty)
async def generate_test_handler(callback: CallbackQuery, state: FSMContext):
    # "difficulty_easy" -> "easy"
    difficulty = callback.data.split("_")[1]
    
    full_difficulty_name = ""
    for row in callback.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                full_difficulty_name = button.text
                break

    await state.update_data(difficulty=full_difficulty_name)
    
    user_data = await state.get_data()
    await state.clear()

    topic = user_data.get('topic')
    loading_msg = await callback.message.edit_text(
        f"🧠 Ваш запрос принят. Обращаюсь к ИИ OpenRouter...\n"
        f"Генерирую тест по теме: '{topic}'"
    )

    generated_text = await api_client.generate_test(
        discipline=user_data.get("discipline"),
        topic=topic,
        count=user_data.get("count"),
        difficulty=user_data.get("difficulty")
    )

    await loading_msg.delete()

    if generated_text.startswith("❌"):
        await callback.message.answer(generated_text)
    else:
      
        try:
            file_to_send = api_client.create_text_file(
                text=generated_text,
                filename=f"test_{topic[:15]}.docx" 
            )
            await callback.message.answer_document(
                document=file_to_send,
                caption=f"✅ Ваш тест по теме '{topic}' готов!"
            )
        except Exception as e:
            await callback.message.answer(f"Ошибка при создании файла: {e}\n\n{generated_text}")
    
    await callback.answer()