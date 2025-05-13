from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


from keyboards.users import user_action_keyboard, confirm_delete_keyboard, get_user_list_keyboard


from telegram.ext import ContextTypes
import asyncio
import re
import logging
from utils.creds import load_creds, save_creds, generate_password
from utils.misc import auto_delete_message

from config import TIMEOUT_SEC


# — Пользователи ——————————————————————————————————————

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    creds = load_creds()
    if not creds:
        return await q.edit_message_text("⚠️ Нет сохранённых пользователей.")

    print("DEBUG | CREDS =", creds, "Тип:", type(creds), "Длина:", len(creds), flush=True)

    # Получаем текущую клавиатуру
    base_kb = [list(row) for row in get_user_list_keyboard(creds).inline_keyboard]


    # Отправляем
    await q.edit_message_text(
        "👥 Список пользователей:",
        reply_markup=InlineKeyboardMarkup(base_kb)
    )
    await asyncio.sleep(TIMEOUT_SEC)


async def handle_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    u = q.data.split(":",1)[1]
    await q.edit_message_text(f"👤 Пользователь: {u}", reply_markup=user_action_keyboard(u))


async def add_user_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["adding"] = True
    context.user_data["last_chat"] = (q.message.chat_id, q.message.message_id)

    msg = await q.message.reply_text("✏️ Введите логин (пароль сгенерируется):")
    context.user_data["input_msg_id"] = msg.message_id


async def add_user_exec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("adding"):
        return

    user = update.message.text.strip()
    user = user.lower()

    # Удаляем сообщение пользователя (ввод логина)
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

    # 🔒 Валидация логина
    if not re.fullmatch(r"[a-zA-Z0-9_-]{2,30}", user):
        msg = await update.message.reply_text(
            "⚠️ Логин может содержать только латинские буквы, цифры, дефис и подчёркивание (2–30 символов)."
        )
        asyncio.create_task(auto_delete_message(context.bot, msg.chat_id, msg.message_id, delay=7))
        return

    # Генерируем пароль и сохраняем
    pwd = generate_password()
    creds = load_creds()
    creds[user] = pwd
    save_creds(creds)

    # Отправляем ответ (логин + пароль)
    msg = await update.message.reply_text(f"✅ `{user}` | `{pwd}`", parse_mode="Markdown")
    asyncio.create_task(auto_delete_message(context.bot, msg.chat_id, msg.message_id, delay=15))

    # Обновляем список пользователей в inline
    chat_id, msg_id = context.user_data.get("last_chat", (None, None))
    if chat_id:
        await context.bot.edit_message_text(
            "👥 Список пользователей:",
            chat_id=chat_id, message_id=msg_id,
            reply_markup=get_user_list_keyboard(creds)
        )
    # Удаляем сообщение с просьбой ввести логин
    input_msg_id = context.user_data.pop("input_msg_id", None)
    if input_msg_id:
        try:
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=input_msg_id)
        except Exception as e:
            logging.warning(f"⚠️ Не удалось удалить сообщение ввода логина: {e}")

    context.user_data.pop("adding", None)

async def confirm_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    u = q.data.split(":",1)[1]
    msg = await q.message.reply_text(f"❓ Удалить `{u}`?", parse_mode="Markdown", reply_markup=confirm_delete_keyboard(u))

    asyncio.create_task(auto_delete_message(context.bot, msg.chat_id, msg.message_id, delay=30))

    await asyncio.sleep(TIMEOUT_SEC)

async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    u = str(q.data.split(":", 1)[1])
    creds = load_creds()

    if u in creds:
        del creds[u]
        save_creds(creds)
        msg = await q.message.reply_text(f"✅ `{u}` удалён.")
        asyncio.create_task(auto_delete_message(context.bot, msg.chat_id, msg.message_id, delay=10))

    else:
        msg = await q.message.reply_text("⚠️ Не найден", parse_mode="Markdown")
        asyncio.create_task(auto_delete_message(context.bot, msg.chat_id, msg.message_id, delay=10))


    # Перерисовываем список пользователей
    markup = get_user_list_keyboard(load_creds())
    await q.message.reply_text("👥 Список пользователей:", reply_markup=markup)
    await asyncio.sleep(TIMEOUT_SEC)

async def show_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    u = q.data.split(":",1)[1]
    pwd = load_creds().get(u)
    await q.message.reply_text(
        f"🔑 `{u}`: `{pwd}`" if pwd else "⚠️ Не найден",
        parse_mode="Markdown"
    )
    await asyncio.sleep(TIMEOUT_SEC)

