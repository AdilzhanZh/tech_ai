# utils/api_client.py

import io
import google.generativeai as genai
from aiogram.types import BufferedInputFile
import config

from docx import Document

try:
    genai.configure(api_key=config.GEMINI_API_KEY)
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    model = genai.GenerativeModel(
        config.GEMINI_CHAT_MODEL,
        safety_settings=safety_settings
    )
except Exception as e:
    print(f"Ошибка конфигурации Gemini: {e}")
    model = None


async def generate_plan(discipline: str, course: str, topic: str):
    if not model:
        return "❌ Ошибка: Модель Gemini не инициализирована. Проверьте API-ключ."

    system_prompt = (
        "Ты — ИИ-ассистент для преподавателей ВУЗов. Твоя задача — "
        "создавать подробные, методологически верные планы лекций или семинарских занятий "
        "для студентов университета. Ответ должен быть на русском языке, в формате Markdown."
    )
    
    user_prompt = (
        f"Создай подробный план занятия (лекции или семинара).\n"
        f"Дисциплина: {discipline}\n"
        f"Курс: {course}\n"
        f"Тема занятия: {topic}\n\n"
        "План должен включать: цели и задачи занятия, ключевые концепции, "
        "структуру (этапы) занятия, вопросы для обсуждения (если это семинар) "
        "и список рекомендуемой литературы (5-7 источников)."
    )

    try:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = await model.generate_content_async(full_prompt)
        return response.text
    except Exception as e:
        print(f"Ошибка Gemini API (generate_plan): {e}")
        if "response.prompt_feedback" in str(e):
             return "❌ Ошибка: Ваш запрос был заблокирован фильтром безопасности Google."
        return f"❌ Произошла ошибка API Gemini: {e}"

async def generate_test(discipline: str, topic: str, count: int, difficulty: str):
    if not model:
        return "❌ Ошибка: Модель Gemini не инициализирована."
        
    system_prompt = (
        "Ты — ИИ-ассистент для преподавателей ВУЗов. Твоя задача — создавать "
        "тестовые задания по заданной теме для проверки знаний студентов. "
        "Ответ должен быть на русском языке, в формате Markdown."
    )
    
    user_prompt = (
        f"Создай тест для студентов.\n"
        f"Дисциплина: {discipline}\n"
        f"Тема: {topic}\n"
        f"Количество вопросов: {count}\n"
        f"Уровень сложности: {difficulty}\n\n"
        "Включи вопросы разных типов (например, с выбором ответа, "
        "на соответствие и открытые вопросы, требующие краткого эссе). "
        "В конце ОБЯЗАТЕЛЬНО предоставь блок с правильными ответами/ключами."
    )
    
    try:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = await model.generate_content_async(full_prompt)
        return response.text
    except Exception as e:
        print(f"Ошибка Gemini API (generate_test): {e}")
        if "response.prompt_feedback" in str(e):
             return "❌ Ошибка: Ваш запрос был заблокирован фильтром безопасности Google."
        return f"❌ Произошла ошибка API Gemini: {e}"



def create_text_file(text: str, filename: str):
    """
    Создает .docx файл в памяти из текста, сохраняя переносы строк.
    """
    doc = Document()
    
    for line in text.split('\n'):
        doc.add_paragraph(line)
    
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0) 
    
    return BufferedInputFile(file=file_stream.getvalue(), filename=filename)