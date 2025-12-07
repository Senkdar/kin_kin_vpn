from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🪙 пополнить баланс", callback_data="menu_pay")],
            [InlineKeyboardButton(text="👥 Пригласить друга", callback_data="menu_invite")],
            [InlineKeyboardButton(text="📱 Мои устройства", callback_data="menu_devices")],
            [InlineKeyboardButton(text="➕ Добавить устройство", callback_data="add_device")],
        ]
    )


def back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="nav_back")],
            [InlineKeyboardButton(text="🏠 В главное меню", callback_data="nav_home")],
        ]
    )


def devices_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить устройство", callback_data="add_device")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="nav_back")],
            [InlineKeyboardButton(text="🏠 В главное меню", callback_data="nav_home")],
        ]
    )


def payments_amounts_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="50₽", callback_data="pay_amount:50"),
                InlineKeyboardButton(text="100₽", callback_data="pay_amount:100"),
                InlineKeyboardButton(text="300₽", callback_data="pay_amount:300"),
            ],
            [
                InlineKeyboardButton(text="500₽", callback_data="pay_amount:500"),
                InlineKeyboardButton(text="1000₽", callback_data="pay_amount:1000"),
                InlineKeyboardButton(text="2000₽", callback_data="pay_amount:2000"),
            ],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="nav_back")],
            [InlineKeyboardButton(text="🏠 В главное меню", callback_data="nav_home")],
        ]
    )


def payments_confirm_kb(tx_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить оплату (sandbox)", callback_data=f"pay_confirm:{tx_id}")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="nav_back")],
            [InlineKeyboardButton(text="🏠 В главное меню", callback_data="nav_home")],
        ]
    )

def payments_methods_kb(tx_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ СБП", callback_data=f"pay_method:sbp:{tx_id}"),
                InlineKeyboardButton(text="💳 Карта", callback_data=f"pay_method:card:{tx_id}"),
            ],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="nav_back")],
            [InlineKeyboardButton(text="🏠 В главное меню", callback_data="nav_home")],
        ]
    )


