from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import manager.constants as const

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=const.MENU_OPERATIONS_BUTTON),
            KeyboardButton(text=const.MONEYBOX_BUTTON)
        ],
        [
            KeyboardButton(text=const.SETTINGS_BUTTON),
            KeyboardButton(text=const.HELP_BUTTON)
        ]
    ],
    resize_keyboard=True
)

operations_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=const.BALANCE_BUTTON),
            KeyboardButton(text=const.INFO_OPERATIONS_BUTTON)
        ],
        [
            KeyboardButton(text=const.ADD_OPERATION_BUTTON),
            KeyboardButton(text=const.DEL_OPERATION_BUTTON)
        ],
        [
            KeyboardButton(text=const.DEL_ALL_OPERATIONS_BUTTON)
        ],
        [
            KeyboardButton(text=const.MAIN_MENU_BUTTON)
        ]
    ],
    resize_keyboard=True
)

settings_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=const.PERSONAL_MODE_BUTTON),
            KeyboardButton(text=const.FAMILY_MODE_BUTTON)
        ],
        [
            KeyboardButton(text=const.MAIN_MENU_BUTTON)
        ]
    ],
    resize_keyboard=True
)

info_operations_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=const.SHOW_INCOME_BUTTON),
            KeyboardButton(text=const.SHOW_EXPENSE_BUTTON)
        ],
        [
            KeyboardButton(text=const.SHOW_ALL_OPERATIONS_BUTTON)
        ],
        [
            KeyboardButton(text=const.BACK_TO_MENU_OPERATIONS_BUTTON)
        ],

    ],
    resize_keyboard=True
)
