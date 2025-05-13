from telegram import Update
from telegram.ext import ContextTypes
from config import SHARE_IP, SHARE_PORT, TIMEOUT_SEC
import asyncio


async def share_proxy_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        q = update.callback_query; await q.answer()
        await q.message.reply_text(f"📤 IP: `{SHARE_IP}`\nPort: `{SHARE_PORT}`", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"📤 IP: `{SHARE_IP}`\nPort: `{SHARE_PORT}`", parse_mode="Markdown")
    await asyncio.sleep(TIMEOUT_SEC)