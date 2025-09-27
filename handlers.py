from aiogram import types
from aiogram.enums import ParseMode  # Исправлено на aiogram.enums
from database import get_user, add_user, get_car_choices, get_car_by_name, get_user_car, start_race, get_car_stats, increase_salary, buy_car, add_user_car, update_user_data
from aiogram.dispatcher import Dispatcher
from aiogram.filters import Command
from aiogram.utils.markdown import text, bold
from random import randint


# Обработчик команды /start
async def start(update: types.Message):
    user = update.from_user
    if not get_user(user.id):
        add_user(user.id, user.username)

    car_choices = get_car_choices()
    buttons = [
        types.KeyboardButton(car["name"]) for car in car_choices
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
    
    await update.answer(
        text="Привет, {}! Добро пожаловать в дрифт-симулятор.\nВыберите одну из машин для начала!".format(user.first_name),
        reply_markup=keyboard
    )

async def profile(update: types.Message):
    user = update.from_user
    user_data = get_user(user.id)

    if user_data:
        profile_info = text(
            f"Профиль {bold(user.first_name)}:\n",
            f"Баланс: ${user_data['balance']}\n",
            f"Гонки: {user_data['total_races']}\n",
            f"Побед: {user_data['races_won']}\n",
            f"Поражений: {user_data['races_lost']}"
        )
        await update.answer(profile_info, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.answer("Вы не зарегистрированы в системе, используйте команду /start.")

async def choose_car(update: types.Message):
    user = update.from_user
    car_name = update.text
    car = get_car_by_name(car_name)
    
    if car:
        await update.answer(f"Вы выбрали {car_name} с максимальной скоростью {car['max_speed']} км/ч.")
        user_car = get_user_car(user.id)
        if user_car:
            await update.answer("У вас уже есть машина. Прокачайте её или выберите новую!")
        else:
            add_user_car(user.id, car["name"])
            await update.answer(f"Теперь у вас есть {car_name}.")
    else:
        await update.answer("Эта машина недоступна для выбора.")

async def help(update: types.Message):
    help_text = text(
        "/start - начать игру и выбрать машину\n",
        "/profile - показать информацию о вашем профиле\n",
        "/race @username - начать гонку с упомянутым пользователем\n",
        "/earn - заработать деньги с автопарка\n",
        "/buy - приобрести машину\n",
        "/help - вывести доступные команды"
    )
    await update.answer(help_text, parse_mode=ParseMode.MARKDOWN)

async def race(update: types.Message):
    user = update.from_user
    mentioned_user = update.entities[0].user if update.entities else None

    if mentioned_user:
        user_data = get_user(user.id)
        opponent_data = get_user(mentioned_user.id)

        if not user_data or not opponent_data:
            await update.answer("Один или оба участника не зарегистрированы!")
            return

        user_car = get_user_car(user.id)
        opponent_car = get_user_car(mentioned_user.id)
        
        if not user_car or not opponent_car:
            await update.answer("Один из участников не выбрал машину!")
            return

        user_speed = get_car_stats(user_car)["max_speed"]
        opponent_speed = get_car_stats(opponent_car)["max_speed"]

        user_result = randint(user_speed - 10, user_speed + 10)
        opponent_result = randint(opponent_speed - 10, opponent_speed + 10)

        winner = user if user_result > opponent_result else mentioned_user
        await update.answer(f"Гонка завершена! Победил {winner.first_name}!")

        if winner == user:
            user_data['races_won'] += 1
            opponent_data['races_lost'] += 1
        else:
            opponent_data['races_won'] += 1
            user_data['races_lost'] += 1

        update_user_data(user.id, user_data)
        update_user_data(mentioned_user.id, opponent_data)
    else:
        await update.answer("Упомяните пользователя для начала гонки!")

async def earn(update: types.Message):
    user = update.from_user
    user_data = get_user(user.id)
    
    if not user_data:
        await update.answer("Вы не зарегистрированы в системе, используйте команду /start.")
        return

    user_car = get_user_car(user.id)
    
    if not user_car:
        await update.answer("Вы не выбрали машину. Выберите машину через команду /start.")
        return

    car_stats = get_car_stats(user_car)
    earnings = randint(50, 150) * (car_stats["max_speed"] // 100)
    user_data["balance"] += earnings

    update_user_data(user.id, user_data)
    
    await update.answer(f"Вы заработали ${earnings}. Ваш новый баланс: ${user_data['balance']}")

async def buy_car(update: types.Message):
    user = update.from_user
    user_data = get_user(user.id)
    
    if not user_data:
        await update.answer("Вы не зарегистрированы в системе, используйте команду /start.")
        return

    available_cars = get_car_choices()
    car_buttons = [types.KeyboardButton(car["name"]) for car in available_cars]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*car_buttons)
    
    await update.answer(
        "Выберите машину для покупки:",
        reply_markup=keyboard
    )

async def confirm_buy_car(update: types.Message):
    user = update.from_user
    car_name = update.text
    car = get_car_by_name(car_name)

    if car:
        user_data = get_user(user.id)

        if user_data["balance"] >= car["price"]:
            user_data["balance"] -= car["price"]
            add_user_car(user.id, car_name)
            update_user_data(user.id, user_data) 
            
            await update.answer(f"Поздравляем, вы купили {car_name} за ${car['price']}!")
        else:
            await update.answer(f"У вас недостаточно средств для покупки {car_name}.")
    else:
        await update.answer("Эта машина недоступна для покупки.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(profile, commands="profile")
    dp.register_message_handler(choose_car, lambda message: message.text in [car['name'] for car in get_car_choices()])
    dp.register_message_handler(help, commands="help")
    dp.register_message_handler(race, commands="race")
    dp.register_message_handler(earn, commands="earn")
    dp.register_message_handler(buy_car, commands="buy")
    dp.register_message_handler(confirm_buy_car, lambda message: message.text in [car['name'] for car in get_car_choices()])
