from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def manage_menu_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton("🔁 Рестарт proxy", callback_data="action:restart")],
        [InlineKeyboardButton("❗ Перезагрузка", callback_data="action:confirm_reboot")],
        [InlineKeyboardButton("📦 Бэкап", callback_data="action:backup")],
        [InlineKeyboardButton("♻️ Восстановление", callback_data="action:restore")],
        [InlineKeyboardButton("🗑 Очистить бэкапы", callback_data="action:clean_backups")],
        [InlineKeyboardButton("🧨 Удалить все бэкапы", callback_data="action:confirm_clean_all")],
        [InlineKeyboardButton("📋 Меню", callback_data="menu:main")],
    ]
    return InlineKeyboardMarkup(kb)

def confirm_reboot_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton("✅ Да, перезагрузить", callback_data="reboot:yes")],
        [InlineKeyboardButton("❌ Нет", callback_data="menu:manage")],
    ]
    return InlineKeyboardMarkup(kb)
