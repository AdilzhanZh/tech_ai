# handlers/plan_handler.py

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import URLInputFile 

from states.generation import PlanGeneration
from keyboards.inline import get_disciplines_keyboard, get_courses_keyboard
from utils import api_client

router = Router()

@router.message(F.text == "📝 План лекции/семинара")
async def start_plan(message: Message, state: FSMContext):
    await state.set_state(PlanGeneration.waiting_for_discipline)
    await message.answer(
        "Вы выбрали создание плана занятия.\nПожалуйста, выберите **дисциплину**:",
        reply_markup=get_disciplines_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "cancel_action")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Действие отменено.")
    await callback.answer()

@router.callback_query(PlanGeneration.waiting_for_discipline)
async def select_discipline(callback: CallbackQuery, state: FSMContext):
    # "discipline_ml" -> "ml"
    discipline = callback.data.split("_")[1] 
    
    full_discipline_name = ""
    for row in callback.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                full_discipline_name = button.text
                break
    
    await state.update_data(discipline=full_discipline_name)
    
    await state.set_state(PlanGeneration.waiting_for_course)
    await callback.message.edit_text(
        f"Дисциплина: {full_discipline_name}. Теперь выберите **курс**:",
        reply_markup=get_courses_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(PlanGeneration.waiting_for_course)
async def select_course(callback: CallbackQuery, state: FSMContext):
    # "course_1" -> "1"
    course = callback.data.split("_")[1] 
    await state.update_data(course=f"{course} курс")
    
    await state.set_state(PlanGeneration.waiting_for_topic)
    await callback.message.edit_text(
        f"Курс: {course}. Теперь введите **тему занятия**:"
    )
    await callback.answer()

@router.message(PlanGeneration.waiting_for_topic)
async def generate_plan_handler(message: Message, state: FSMContext):
    topic = message.text
    user_data = await state.get_data()
    await state.clear()
    
    loading_msg = await message.answer(
        "🧠 Ваш запрос принят. Обращаюсь к ИИ OpenRouter...\n"
        f"Генерирую план по теме: '{topic}'"
    )
    
    generated_text = await api_client.generate_plan(
        discipline=user_data.get("discipline"),
        course=user_data.get("course"),
        topic=topic
    )
    
    await loading_msg.delete()
    
    if generated_text.startswith("❌"):
        await message.answer(generated_text)
    else:
        
        try:
            file_to_send = api_client.create_text_file(
                text=generated_text,
                filename=f"plan_{topic[:15]}.docx"  
            )
            await message.answer_document(
                document=file_to_send,
                caption=f"✅ Ваш план занятия по теме '{topic}' готов!"
            )
        except Exception as e:
            await message.answer(f"Ошибка при создании файла: {e}\n\n{generated_text}")