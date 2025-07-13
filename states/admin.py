from aiogram.fsm.state import State, StatesGroup

class EmployeeForm(StatesGroup):
    get_id = State()
    get_name = State()

class AddLocation(StatesGroup):
    waiting_for_location = State()
    