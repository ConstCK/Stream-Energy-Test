from aiogram.fsm.state import StatesGroup, State


class Stages(StatesGroup):
    authenticated = State()
