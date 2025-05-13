from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton("👥 Пользователи", callback_data="menu:users")],
        [InlineKeyboardButton("📊 Мониторинг", callback_data="menu:monitor")],
        [InlineKeyboardButton("🛠 Управление", callback_data="menu:manage")],
        [InlineKeyboardButton("📤 Поделиться", callback_data="menu:share")],
    ]
    return InlineKeyboardMarkup(kb)
