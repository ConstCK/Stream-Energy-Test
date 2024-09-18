from aiogram.fsm.state import StatesGroup, State


class Stages(StatesGroup):
    password_verifying = State()
    authed = State()
    authorization = State()
    adding_title = State()
    adding_content = State()
    adding_tags = State()
    selecting_tags = State()
