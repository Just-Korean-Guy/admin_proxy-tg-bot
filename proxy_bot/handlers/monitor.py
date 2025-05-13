from telegram import Update
from telegram.ext import ContextTypes
import asyncio
import psutil
from keyboards.monitor import monitor_menu_keyboard, back_to_monitor_keyboard

from utils.sysinfo import parse_traffic_log, format_bytes
from config import TIMEOUT_SEC

# — Мониторинг —————————————————————————————————————

async def show_monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    await q.edit_message_text("📊 Мониторинг:", reply_markup=monitor_menu_keyboard())

    await asyncio.sleep(TIMEOUT_SEC)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # команда /stats
    await show_monitor(update, context)

async def monitor_traffic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = parse_traffic_log("/var/log/squid/access.log")
    
    if not data:
        text = "⚠️ Нет данных"
    else:
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        text = "\n".join(f"📈 {u}: {format_bytes(b)}" for u, b in sorted_data)

    await q.edit_message_text(text, reply_markup=back_to_monitor_keyboard())

    await asyncio.sleep(TIMEOUT_SEC)


async def monitor_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    cpu = psutil.cpu_percent(1); vm = psutil.virtual_memory(); du = psutil.disk_usage("/")
    text = (
        f"💽 CPU: {cpu:.1f}%\n"
        f"RAM: {vm.used//1024//1024}/{vm.total//1024//1024} MB ({vm.percent}%)\n"
        f"Disk: {du.used//1024//1024}/{du.total//1024//1024} MB ({du.percent}%)"
    )
    await q.edit_message_text(text, reply_markup=back_to_monitor_keyboard()
    )
    await asyncio.sleep(TIMEOUT_SEC)

