from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.filters import Command
import manager.constants as const
from manager.formatters import format_operation, format_add_operation, format_del_operation, format_del_all_operations
from manager.logic import total_amount, filter_by_type, add_operation, find_operation_by_id, delete_operation, delete_all_operation
from utils import load_user_operations, save_user_operations
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards import main_menu_keyboard, operations_keyboard, settings_keyboard, info_operations_keyboard
from aiogram import F


router = Router()


async def show_menu(
        message: Message,
        keyboard: ReplyKeyboardMarkup,
        text: str = const.CHOICE_MENU_ITEM
):
    await message.answer(text, reply_markup=keyboard)


async def send_balance(message: Message):
    operations = load_user_operations(message)
    balance = total_amount(operations)
    await message.answer(f"💰 Текущий баланс: {balance} руб.")


async def send_show_all_operations(message: Message):
    operations = load_user_operations(message)
    if not operations:
        await message.answer(const.OPERATIONS_NOT_FOUND)
        return
    for operation in operations:
        await message.answer(
            format_operation(operation)
        )


async def send_show_income(message: Message):
    operations = load_user_operations(message)
    if not operations:
        await message.answer(const.OPERATIONS_NOT_FOUND)
        return
    show_income = filter_by_type(operations, const.INCOME)
    if not show_income:
        await message.answer(const.OPERATIONS_NOT_FOUND)
        return
    for operation in show_income:
        await message.answer(format_operation(operation))


async def send_show_expense(message: Message):
    operations = load_user_operations(message)
    if not operations:
        await message.answer(const.OPERATIONS_NOT_FOUND)
        return
    show_expense = filter_by_type(operations, const.EXPENSE)
    if not show_expense:
        await message.answer(const.OPERATIONS_NOT_FOUND)
        return
    for operation in show_expense:
        await message.answer(format_operation(operation))


class AddOperationStates(StatesGroup):
    operation_type = State()
    amount = State()
    category = State()
    description = State()


class DelOperationStates(StatesGroup):
    operation_id = State()


class DelAllOperationStates(StatesGroup):
    confirm = State()


async def start_add_operation(message: Message, state: FSMContext):
    await state.set_state(AddOperationStates.operation_type)
    await message.answer(const.ENTER_TYPE_OPERATION)


async def start_del_operation(message: Message, state: FSMContext):
    operations = load_user_operations(message)
    if not operations:
        await message.answer(const.OPERATIONS_NOT_FOUND)
        return
    await state.set_state(DelOperationStates.operation_id)
    await message.answer(const.ENTER_ID_FOR_DEL_OPERATION)


async def start_del_all(message: Message, state: FSMContext):
    operations = load_user_operations(message)
    if not operations:
        await message.answer(const.OPERATIONS_NOT_FOUND)
        return
    await state.set_state(DelAllOperationStates.confirm)
    await message.answer(const.CONFIRM_DEL_ALL_OPERATIONS)


@router.message(CommandStart())
async def start_main_menu_handler(message: Message):
    await show_menu(message, main_menu_keyboard, const.WELCOME_TEXT)


@router.message(F.text == const.MENU_OPERATIONS_BUTTON)
async def operations_menu_button(message: Message):
    await show_menu(message, operations_keyboard)


@router.message(F.text == const.SETTINGS_BUTTON)
async def settings_menu_button(message: Message):
    await show_menu(message, settings_keyboard, const.SETTINGS_TEXT)


@router.message(F.text == const.PERSONAL_MODE_BUTTON)
async def personal_mode_button(message: Message):
    await message.answer(const.PERSONAL_MODE_TEXT)
    await show_menu(message, settings_keyboard)


@router.message(F.text == const.FAMILY_MODE_BUTTON)
async def family_mode_button(message: Message):
    await message.answer(const.FAMILY_MODE_TEXT)
    await show_menu(message, settings_keyboard)


@router.message(F.text == const.MONEYBOX_BUTTON)
async def moneybox_button(message: Message):
    await message.answer(const.MONEYBOX_TEXT)
    await show_menu(message, main_menu_keyboard)


@router.message(F.text == const.INFO_OPERATIONS_BUTTON)
async def info_operations_menu_button(message: Message):
    await show_menu(message, info_operations_keyboard, const.INFO_OPERATIONS_TEXT)


@router.message(F.text == const.MAIN_MENU_BUTTON)
async def back_main_menu_button(message: Message):
    await show_menu(message, main_menu_keyboard)


@router.message(F.text == const.BACK_TO_MENU_OPERATIONS_BUTTON)
async def back_to_menu_operations_button(message: Message):
    await show_menu(message, operations_keyboard)


@router.message(Command('help'))
async def help_handler(message: Message):
    await show_menu(message, main_menu_keyboard, const.HELP_MENU_TEXT)


@router.message(F.text == const.HELP_BUTTON)
async def help_menu_button(message: Message):
    await show_menu(message, main_menu_keyboard, const.HELP_MENU_TEXT)


@router.message(F.text == const.BALANCE_BUTTON)
async def balance_button(message: Message):
    await send_balance(message)
    await show_menu(message, operations_keyboard)


@router.message(F.text == const.SHOW_ALL_OPERATIONS_BUTTON)
async def show_all_operations_button(message: Message):
    await send_show_all_operations(message)
    await show_menu(message, info_operations_keyboard)


@router.message(F.text == const.SHOW_INCOME_BUTTON)
async def show_income_button(message: Message):
    await send_show_income(message)
    await show_menu(message, info_operations_keyboard)


@router.message(F.text == const.SHOW_EXPENSE_BUTTON)
async def show_expense_button(message: Message):
    await send_show_expense(message)
    await show_menu(message, info_operations_keyboard)


@router.message(F.text == const.ADD_OPERATION_BUTTON)
async def add_button(message: Message, state: FSMContext):
    await start_add_operation(message, state)


@router.message(AddOperationStates.operation_type)
async def add_operation_type(message: Message, state: FSMContext):
    op_type = message.text.strip().lower()
    if op_type not in [const.INCOME, const.EXPENSE]:
        await message.answer(const.ENTER_TYPE_OPERATION)
        return
    await state.update_data(operation_type=op_type)
    await state.set_state(AddOperationStates.amount)
    await message.answer(const.ENTER_AMOUNT_OPERATION)


@router.message(AddOperationStates.amount)
async def add_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.strip())
    except ValueError:
        await message.answer(const.WARNING_ENTER_DIGIT)
        return
    await state.update_data(amount=amount)
    await state.set_state(AddOperationStates.category)
    await message.answer(const.ENTER_CATEGORY_OPERATION)


@router.message(AddOperationStates.category)
async def add_category(message: Message, state: FSMContext):
    category = message.text.strip()
    await state.update_data(category=category)
    await state.set_state(AddOperationStates.description)
    await message.answer(const.ENTER_DECRIPTION_OPERATION)


@router.message(AddOperationStates.description)
async def add_description(message: Message, state: FSMContext):
    description = message.text.strip()
    await state.update_data(description=description)

    data = await state.get_data()

    operations = load_user_operations(message)

    add_new_operation = add_operation(
        operations,
        data['operation_type'],
        data['amount'],
        data['category'],
        data['description']
    )

    save_user_operations(message, operations)
    await message.answer(format_add_operation(add_new_operation))
    await state.clear()
    await show_menu(message, operations_keyboard)


@router.message(F.text == const.DEL_OPERATION_BUTTON)
async def del_button(message: Message, state: FSMContext):
    await start_del_operation(message, state)


@router.message(DelOperationStates.operation_id)
async def del_operation_by_id(message: Message, state: FSMContext):
    try:
        op_id = int(message.text)
    except ValueError:
        await message.answer(const.WARNING_ENTER_DIGIT)
        return
    operations = load_user_operations(message)
    operation_to_delete = find_operation_by_id(operations, op_id)
    if not operation_to_delete:
        await message.answer(f"Операций c ID: {op_id} не найдено!")
        await state.clear()
        await show_menu(message, operations_keyboard)
        return
    operation_delete_to_format = delete_operation(
        operations, operation_to_delete)
    save_user_operations(message, operations)
    await message.answer(format_del_operation(operation_delete_to_format))
    await state.clear()
    await show_menu(message, operations_keyboard)


@router.message(F.text == const.DEL_ALL_OPERATIONS_BUTTON)
async def del_all_button(message: Message, state: FSMContext):
    await start_del_all(message, state)


@router.message(DelAllOperationStates.confirm)
async def del_all(message: Message, state: FSMContext):
    confirm_operation = message.text.strip().lower()
    if confirm_operation not in ['да', 'нет']:
        await message.answer("Введите: 'Да' или 'Нет': ")
        return
    await state.update_data(confirm=confirm_operation)
    if confirm_operation == 'да':
        operations = load_user_operations(message)
        delete_all_operation(operations)
        save_user_operations(message, operations)
        await message.answer(format_del_all_operations())
    elif confirm_operation == 'нет':
        await message.answer(const.CANCEL_DEL_ALL_OPERATIONS)
    await state.clear()
    await show_menu(message, operations_keyboard)
