# ——— Стандартные импорты ——————————————————————

import asyncio
import logging
from config import BOT_TOKEN, AUTHORIZED_USER_ID, SHARE_IP, SHARE_PORT, PASSWD_FILE, CREDS_FILE, ACCESS_LOG, GPG_PASS, TIMEOUT_SEC

# ——— Telegram API ————————————————————————————
from telegram import Update, BotCommand, BotCommandScopeDefault
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)



# ——— Внутренние модули (utils, handlers, keyboards) ——————
from utils.creds import generate_password, save_creds, load_creds, sync_with_squid
from utils.sysinfo import parse_traffic_log, format_uptime, format_bytes
from utils.misc import auto_delete_message

from handlers.main_menu import start
from handlers.monitor import show_monitor, monitor_traffic, monitor_system
from handlers.users import (
    list_users,
    handle_user,
    add_user_prompt,
    add_user_exec,
    confirm_delete,
    delete_user,
    show_password,
)
from handlers.manage import (
    show_manage,
    restart_proxy,
    confirm_reboot_prompt,
    reboot_server,
    uptime_command,
    manual_backup,
    backup_handler,
    clean_backups_handler,
    confirm_clean_all_handler,
    clean_all_handler,
    restore_info,
    restore_inline,
)
from handlers.share import share_proxy_info

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")



# ——— Slash-команды (для меню Telegram) ————————————————

COMMANDS = [
    BotCommand("start",  "🔧 Главное меню"),
    BotCommand("backup",  "📦 Бэкап"),
    BotCommand("share",  "📤 IP и порт прокси"),
]



# ——— Инициализация бота и команд —————————————————————

async def on_startup(app):
    # Регистрируем slash-команды
    await app.bot.set_my_commands(COMMANDS, scope=BotCommandScopeDefault())


# Инициализация бота  
application = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()


# ——— Запуск приложения ————————————————————————————————————

if __name__ == "__main__":

    # ——— Команды (slash и текстовые) ————————————————————————
    application.add_handler(CommandHandler("start",    start))
    application.add_handler(CommandHandler("stats",    show_monitor))
    application.add_handler(CommandHandler("uptime",   uptime_command))
    application.add_handler(CommandHandler("restart",  restart_proxy))
    application.add_handler(CommandHandler("reboot",   reboot_server))
    application.add_handler(CommandHandler("share",    share_proxy_info))
    application.add_handler(CommandHandler("backup",   manual_backup))
    application.add_handler(CommandHandler("restore",  restore_info))

    # ——— Подтверждения и действия ——————————————————————————
    application.add_handler(CallbackQueryHandler(confirm_reboot_prompt,         pattern="^action:confirm_reboot$"))
    application.add_handler(CallbackQueryHandler(reboot_server,                 pattern="^reboot:yes$"))
    application.add_handler(CallbackQueryHandler(backup_handler,                pattern="^action:backup$"))
    application.add_handler(CallbackQueryHandler(restore_inline,                pattern="^action:restore$"))
    application.add_handler(CallbackQueryHandler(clean_backups_handler,         pattern="^action:clean_backups$"))
    application.add_handler(CallbackQueryHandler(confirm_clean_all_handler,     pattern="^action:confirm_clean_all$"))
    application.add_handler(CallbackQueryHandler(clean_all_handler,             pattern="^action:clean_all$"))

    # ——— Главное меню ————————————————————————————————
    application.add_handler(CallbackQueryHandler(start,                         pattern="^menu:main$"))
    application.add_handler(CallbackQueryHandler(share_proxy_info,              pattern="^menu:share$"))

    # ——— Пользователи ——————————————————————————————————————
    application.add_handler(CallbackQueryHandler(list_users,                    pattern="^menu:users$"))
    application.add_handler(CallbackQueryHandler(handle_user,                   pattern="^user:"))
    application.add_handler(CallbackQueryHandler(add_user_prompt,               pattern="^add:manual$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,     add_user_exec))
    application.add_handler(CallbackQueryHandler(confirm_delete,                pattern="^del:"))
    application.add_handler(CallbackQueryHandler(delete_user,                   pattern="^confirmdel:"))
    application.add_handler(CallbackQueryHandler(show_password,                 pattern="^show:"))

    # ——— Мониторинг ————————————————————————————————————————
    application.add_handler(CallbackQueryHandler(show_monitor,                  pattern="^menu:monitor$"))
    application.add_handler(CallbackQueryHandler(monitor_traffic,               pattern="^monitor:traffic$"))
    application.add_handler(CallbackQueryHandler(monitor_system,                pattern="^monitor:system$"))

    # ——— Управление ————————————————————————————————————————
    application.add_handler(CallbackQueryHandler(show_manage,                   pattern="^menu:manage$"))
    application.add_handler(CallbackQueryHandler(restart_proxy,                 pattern="^action:restart$"))


# Запуск бота  
    application.run_polling()
