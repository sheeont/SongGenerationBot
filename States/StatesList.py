from aiogram.fsm.state import State, StatesGroup


class StateList(StatesGroup):
    wait_text_enter_state = State()
    text_editing_state = State()
    generate_content_state = State()
