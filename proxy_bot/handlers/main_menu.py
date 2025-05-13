from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from keyboards.main import main_menu_keyboard
from config import AUTHORIZED_USER_ID

import logging



# ——— HANDLERS ————————————————————————————————————————————

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid != AUTHORIZED_USER_ID:
        logging.warning(f"❌ Запрет доступа: Telegram ID {uid} | username: @{update.effective_user.username}")

        # 🔔 Отправка уведомления тебе (админу)
        await context.bot.send_message(
            chat_id=AUTHORIZED_USER_ID,
            text=f"🚨 Попытка доступа!\nID: `{uid}`\nUsername: @{update.effective_user.username or '—'}",
            parse_mode="Markdown"
        )

        target = update.callback_query or update.message
        return await target.reply_text("❌ Доступ запрещён.")

    markup = main_menu_keyboard()
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("🔧 Главное меню:", reply_markup=markup)
    else:
        await update.message.reply_text("🔧 Главное меню:", reply_markup=markup)