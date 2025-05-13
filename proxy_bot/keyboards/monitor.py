from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def monitor_menu_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton("📈 Трафик", callback_data="monitor:traffic")],
        [InlineKeyboardButton("💽 Нагрузка", callback_data="monitor:system")],
        [InlineKeyboardButton("📋 Меню", callback_data="menu:main")],
    ]
    return InlineKeyboardMarkup(kb)

def back_to_monitor_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="menu:monitor")]])

