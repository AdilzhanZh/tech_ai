# states/generation.py

from aiogram.fsm.state import State, StatesGroup

class PlanGeneration(StatesGroup):
    waiting_for_discipline = State() 
    waiting_for_course = State()    
    waiting_for_topic = State()      

class TestGeneration(StatesGroup):
    waiting_for_discipline = State()
    waiting_for_topic = State()
    waiting_for_count = State()
    waiting_for_difficulty = State()
