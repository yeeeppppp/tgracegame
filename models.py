class User:
    def __init__(self, user_id, username, balance=1000, races_won=0, races_lost=0, total_races=0, job=None):
        self.user_id = user_id
        self.username = username
        self.balance = balance
        self.races_won = races_won
        self.races_lost = races_lost
        self.total_races = total_races
        self.job = job  

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "balance": self.balance,
            "races_won": self.races_won,
            "races_lost": self.races_lost,
            "total_races": self.total_races,
            "job": self.job,
        }

class Car:
    def __init__(self, name, max_speed, price, owner_id=None):
        self.name = name
        self.max_speed = max_speed
        self.price = price
        self.owner_id = owner_id

    def to_dict(self):
        return {
            "name": self.name,
            "max_speed": self.max_speed,
            "price": self.price,
            "owner_id": self.owner_id,
        }

class Job:
    def __init__(self, name, salary, rank):
        self.name = name 
        self.salary = salary  
        self.rank = rank  

    def to_dict(self):
        return {
            "name": self.name,
            "salary": self.salary,
            "rank": self.rank,
        }

CARS_LIST = [
    Car("Toyota Supra", 250, 35000),
    Car("Nissan Skyline", 240, 32000),
    Car("Mazda RX-7", 260, 30000),
    Car("Honda Civic", 220, 20000),
    Car("Subaru Impreza", 230, 25000),
    Car("Mitsubishi Lancer Evo", 240, 28000),
    Car("Nissan 350Z", 270, 35000),
    Car("Ford Mustang", 280, 40000),
    Car("Chevrolet Camaro", 290, 45000),
    Car("BMW M3", 280, 42000),
    Car("Porsche 911", 300, 60000),
    Car("Audi R8", 320, 75000),
    Car("Mercedes-Benz AMG", 310, 70000),
    Car("Lamborghini Gallardo", 330, 100000),
    Car("Ferrari F430", 340, 120000),
]

JOBS_LIST = [
    Job("Инженер", 1500, 1),
    Job("Менеджер", 2500, 2),
    Job("Директор", 4000, 3),
    Job("Владелец бизнеса", 7000, 4),
    Job("Предприниматель", 10000, 5),
    Job("Топ-менеджер", 15000, 6),
]
