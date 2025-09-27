from database import get_user, update_user_data, add_user_car, get_car_by_name
from models import Car


def check_balance(user_id):
    user = get_user(user_id)
    if user:
        return user[3]
    return 0  

# Функция для покупки машины
def buy_car(user_id, car_name):
    user = get_user(user_id)
    car = get_car_by_name(car_name)
    if not car:
        return "Машина не найдена!"
    if user[3] < car.price:
        return "Недостаточно средств для покупки этой машины."

    add_user_car(user_id, car_name) 

    user[3] -= car.price
    update_user_data(user_id, user[1], user[3], user[4], user[5], user[6])  # Обновляем данные пользователя
    return f"Вы успешно купили {car_name}!"

def start_race(user_id, opponent_id, car_name):
    user = get_user(user_id)
    opponent = get_user(opponent_id)

    user_car = get_user_car(user_id)
    if user_car != car_name:
        return "У вас нет такой машины для участия в гонке!"

    opponent_car = get_user_car(opponent_id)
    if opponent_car != car_name:
        return f"У {opponent['username']} нет такой машины для гонки!"

    return race_result(user_id, opponent_id, car_name)

def race_result(user_id, opponent_id, car_name):
    user = get_user(user_id)
    opponent = get_user(opponent_id)
    user_car = get_car_by_name(car_name)
    opponent_car = get_car_by_name(opponent['car'])

    user_speed = user_car.max_speed
    opponent_speed = opponent_car.max_speed

    if user_speed > opponent_speed:
        user[4] += 1 
        opponent[5] += 1  
        result = f"{user['username']} победил в гонке!"
    elif user_speed < opponent_speed:
        user[5] += 1  
        opponent[4] += 1  
        result = f"{opponent['username']} победил в гонке!"
    else:
        result = "Ничья!"

    user[6] += 1
    opponent[6] += 1

    update_user_data(user_id, user[1], user[3], user[4], user[5], user[6])  # Обновляем данные пользователя
    update_user_data(opponent_id, opponent[1], opponent[3], opponent[4], opponent[5], opponent[6])  # Обновляем данные противника

    return result

def get_user_car(user_id):
    user = get_user(user_id)
    return user['car'] if user else None

def earn_from_park(user_id):
    user = get_user(user_id)
    if user:
        # Увеличиваем баланс на 10% от стоимости машины (для примера)
        earnings = sum([car.price * 0.1 for car in get_user_cars(user_id)])
        user[3] += earnings
        update_user_data(user_id, user[1], user[3], user[4], user[5], user[6])  # Обновляем данные пользователя
        return f"Вы заработали ${earnings:.2f} с вашего автопарка!"
    return "Ошибка при увеличении заработка!"

def get_user_cars(user_id):
    cars = []
    user = get_user(user_id)
    if user:
        for car in user['cars']:
            cars.append(get_car_by_name(car))
    return cars

def promote_user(user_id):
    user = get_user(user_id)
    if user:
        job_list = get_jobs()
        current_job = user['job']
        next_job = job_list[current_job + 1] if current_job < len(job_list) - 1 else None
        if next_job:
            user['job'] = next_job['name']
            user['salary'] = next_job['salary']
            update_user_data(user_id, user[1], user[3], user[4], user[5], user[6], user['job'])
            return f"Поздравляем! Вы были повышены на должность {next_job['name']}!"
        return "Вы достигли высшего ранга!"
    return "Ошибка при повышении!"

def get_jobs():
    return [
        {"name": "Инженер", "salary": 1500},
        {"name": "Менеджер", "salary": 2500},
        {"name": "Директор", "salary": 4000},
        {"name": "Предприниматель", "salary": 7000},
        {"name": "Топ-менеджер", "salary": 10000},
    ]
