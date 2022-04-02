from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    state1 = State()
    state2 = State()


class State_s(StatesGroup):
    state1 = State()


class State_del(StatesGroup):
    state1 = State()
