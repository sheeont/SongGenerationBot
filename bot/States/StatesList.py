from aiogram.fsm.state import State, StatesGroup


class StateList(StatesGroup):
    waiting_for_initial_text = State()
    waiting_for_confirmation = State()
