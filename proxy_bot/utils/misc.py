import asyncio
import logging



async def auto_delete_message(bot, chat_id, message_id, delay=5):
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logging.warning(f"❌ Не удалось удалить сообщение: {e}")