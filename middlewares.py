from aiogram import BaseMiddleware
import logging
from aiogram import types

class LoggingMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        logging.info(f"New message from {message.from_user.id} ({message.from_user.username}): {message.text}")
        await super().on_process_message(message, data)
