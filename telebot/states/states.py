from aiogram.fsm.state import StatesGroup, State


class Stages(StatesGroup):
    password_verifying = State()
    authenticated = State()
    authorization = State()
