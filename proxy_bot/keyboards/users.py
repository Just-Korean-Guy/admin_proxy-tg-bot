from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_user_list_keyboard(creds: dict) -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(u, callback_data=f"user:{u}")] for u in creds.keys()]
    kb += [
        [InlineKeyboardButton("✏️ Добавить", callback_data="add:manual")],
        [InlineKeyboardButton("📋 Меню", callback_data="menu:main")],
    ]
    return InlineKeyboardMarkup(kb)

def user_action_keyboard(username: str) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton("🗑 Удалить", callback_data=f"del:{username}")],
        [InlineKeyboardButton("🔑 Пароль",  callback_data=f"show:{username}")],
        [InlineKeyboardButton("⬅️ Назад",   callback_data="menu:users")],
    ]
    return InlineKeyboardMarkup(kb)


def confirm_delete_keyboard(username: str) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton("✅ Да", callback_data=f"confirmdel:{username}")],
        [InlineKeyboardButton("❌ Нет", callback_data="menu:users")],
    ]
    return InlineKeyboardMarkup(kb)
