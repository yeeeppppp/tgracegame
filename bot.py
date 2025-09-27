import logging
from aiogram import Bot, Dispatcher, types
from aiogram import Router
from database import add_user, get_user, initialize_database, get_all_cars, update_user_car
from config import TOKEN
from handlers import register_handlers
from middlewares import LoggingMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

initialize_database()

dp.middleware.setup(LoggingMiddleware())

register_handlers(dp)

if __name__ == "__main__":
    dp.run_polling()
