# handlers/image_handler.py

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile

from states.generation import ImageGeneration
from utils import api_client

router = Router()

@router.message(F.text == "🖼️ Создать изображение")
async def start_image(message: Message, state: FSMContext):
    await state.set_state(ImageGeneration.waiting_for_prompt)
    await message.answer(
        "Вы выбрали генерацию изображений.\n"
        "Пожалуйста, введите текстовое описание (промпт) для создания иллюстрации. "
        "Например: 'схема нейронной сети' или 'фото кампуса университета'."
    )

@router.message(ImageGeneration.waiting_for_prompt)
async def generate_image_handler(message: Message, state: FSMContext):
    prompt = message.text
    await state.clear()

    loading_msg = await message.answer("🎨 Ваш запрос принят. Генерирую изображение (NVIDIA Nemotron)...")

    image_url = await api_client.generate_image(prompt)

    await loading_msg.delete()

    if image_url and image_url.startswith("http"):
        await message.answer_photo(
            photo=URLInputFile(image_url),
            caption=f"✅ Изображение по запросу: '{prompt}'"
        )
    else:
        await message.answer(f"❌ Произошла ошибка: {image_url}")