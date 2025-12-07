from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def devices_list_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить устройство", callback_data="add_device")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="nav_back")],
            [InlineKeyboardButton(text="🏠 В главное меню", callback_data="nav_home")],
        ]
    )


def devices_add_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=" Mac", callback_data="dev_platform:mac"),
                InlineKeyboardButton(text="🤖 Android", callback_data="dev_platform:android"),
                InlineKeyboardButton(text="🪟 Windows", callback_data="dev_platform:windows"),
            ],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="nav_back")],
            [InlineKeyboardButton(text="🏠 В главное меню", callback_data="nav_home")],
        ]
    )


