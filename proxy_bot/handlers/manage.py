import os
import subprocess
import datetime
import shutil
import asyncio

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import TIMEOUT_SEC
from utils.sysinfo import format_uptime  # для uptime_command

from keyboards.manage import manage_menu_keyboard, confirm_reboot_keyboard
from utils.misc import auto_delete_message

# — Управление —————————————————————————————————————

async def restart_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    try:
        await q.message.reply_text("🔁 Перезапуск proxy...")
        await asyncio.create_subprocess_exec("systemctl", "restart", "squid")
        await q.message.reply_text("✅ Proxy перезапущен.")
    except Exception as e:
        await q.message.reply_text(f"❌ Ошибка при перезапуске: {e}")

async def confirm_reboot_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    msg = await q.message.reply_text("❗ Подтвердить перезагрузку сервера?", reply_markup=confirm_reboot_keyboard())

    asyncio.create_task(auto_delete_message(context.bot, msg.chat_id, msg.message_id, delay=30))

async def reboot_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    try:
        await q.message.reply_text("🔄 Сервер перезагружается...")
        await asyncio.create_subprocess_exec("reboot")
    except Exception as e:
        await q.message.reply_text(f"❌ Ошибка при перезагрузке: {e}")

async def uptime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    up = format_uptime()
    await update.message.reply_text(f"⏱ Аптайм: {up}")
    await asyncio.sleep(TIMEOUT_SEC)

async def restore_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "♻️ *Восстановление вручную:*\n\n"
        "1\\. Скопируй архив обратно на сервер\n"
        "2\\. Распакуй:\n"
        "`tar xzf имя_архива\\.tar\\.gz -C /`\n\n"
        "3\\. Список пакетов:\n"
        "`dpkg --set-selections < package-list\\.txt`\n"
        "`apt-get dselect-upgrade`"
    )
    await update.message.reply_text(text, parse_mode="MarkdownV2")

async def restore_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await restore_info(q, context)



async def manual_backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import datetime
    import shutil

    total, used, free = shutil.disk_usage("/")
    percent_used = used / total * 100

    if percent_used >= 90:
        await update.message.reply_text("❗ Недостаточно места на диске. Бэкап отменён.")
        return

    now = datetime.datetime.now().strftime("%Y-%m-%d")
    bdir = "/root/backups"
    os.makedirs(bdir, exist_ok=True)

    # Пути к архивам
    etc_arc  = f"{bdir}/etc-backup-{now}.tar.gz"
    var_arc  = f"{bdir}/var-backup-{now}.tar.gz"
    pkg_txt  = f"{bdir}/package-list-{now}.txt"
    scripts_arc = f"{bdir}/scripts-backup-{now}.tar.gz"

    # Создание архивов
    subprocess.run(["tar", "czf", etc_arc, "/etc"], check=True)
    os.system(f"tar czf {var_arc} /var/backups")
    os.system(f"dpkg --get-selections > {pkg_txt}")
    os.system(f"tar czf {scripts_arc} /root/final-proxy-stack /root/proxy_bot /root/final-proxy-stack/proxy_bot/.env")

    if update.message:
        target = update.message
    else:
        target = update.callback_query.message

    async def send_file(path, label):
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / 1024 / 1024
            if size_mb < 49:
                with open(path, "rb") as f:
                    await target.reply_document(f, filename=os.path.basename(path), caption=label)
            else:
                await target.reply_text(f"⚠️ `{os.path.basename(path)}` слишком большой ({size_mb:.1f} MB), не отправлен.", parse_mode="Markdown")

    await send_file(etc_arc,  "🧩 Бэкап /etc")
    await send_file(var_arc,  "🧩 Бэкап /var/backups")
    await send_file(scripts_arc, "📁 Скрипты и бот")
    await send_file(pkg_txt,  "📄 Список пакетов")
    
    # Сохраняем подробную инструкцию в текстовый файл
    restore_path = f"{bdir}/README-restore-{now}.txt"
    shutil.copyfile(
        "/root/final-proxy-stack/proxy_bot/README-restore-template.txt",
        restore_path
    )

    await send_file(restore_path, "📄 Инструкция восстановления")

async def backup_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await manual_backup(update.callback_query, context)


async def clean_backups_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    script_path = "/root/clean_old_backups.sh"

    if os.path.isfile(script_path):
        try:
            os.system(script_path)
            msg = await q.message.reply_text("🗑 Старые бэкапы удалены.")
            asyncio.create_task(auto_delete_message(context.bot, msg.chat_id, msg.message_id, delay=10))
        except Exception as e:
            await q.message.reply_text(f"❌ Ошибка при запуске скрипта: {e}")
    else:
        await q.message.reply_text("⚠️ Скрипт очистки не найден.")


async def confirm_clean_all_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    kb = [
        [InlineKeyboardButton("✅ Да, удалить", callback_data="action:clean_all")],
        [InlineKeyboardButton("❌ Нет", callback_data="menu:manage")],
    ]
    msg = await q.message.reply_text("❗ Удалить *все* бэкапы из /root/backups/?", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
    asyncio.create_task(auto_delete_message(context.bot, msg.chat_id, msg.message_id, delay=30))

    await asyncio.sleep(TIMEOUT_SEC)

async def clean_all_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    os.system("rm -f /root/backups/*")
    await q.message.reply_text("🧨 Все бэкапы удалены.")
    await asyncio.sleep(TIMEOUT_SEC)

async def show_manage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    kb = [
        [InlineKeyboardButton("🔁 Рестарт proxy", callback_data="action:restart")],
        [InlineKeyboardButton("❗ Перезагрузка", callback_data="action:confirm_reboot")],
        [InlineKeyboardButton("📦 Бэкап",         callback_data="action:backup")],
        [InlineKeyboardButton("♻️ Восстановление", callback_data="action:restore")],
        [InlineKeyboardButton("🗑 Очистить бэкапы", callback_data="action:clean_backups")],
        [InlineKeyboardButton("🧨 Удалить все бэкапы", callback_data="action:confirm_clean_all")],
        [InlineKeyboardButton("📋 Меню",          callback_data="menu:main")],
    ]
    await q.edit_message_text("🛠 Управление:", reply_markup=InlineKeyboardMarkup(kb))
    await asyncio.sleep(TIMEOUT_SEC)


