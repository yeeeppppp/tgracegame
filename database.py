import sqlite3

DB_NAME = "race_simulator.db"

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        balance INTEGER DEFAULT 1000,
                        races_won INTEGER DEFAULT 0,
                        races_lost INTEGER DEFAULT 0,
                        total_races INTEGER DEFAULT 0)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS cars (
                        car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        max_speed INTEGER,
                        price INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_cars (
                        user_id INTEGER,
                        car_id INTEGER,
                        FOREIGN KEY(user_id) REFERENCES users(user_id),
                        FOREIGN KEY(car_id) REFERENCES cars(car_id))''')

    cars = [
        ("Nissan Skyline", 300, 5000),
        ("Toyota Supra", 290, 4500),
        ("Mazda RX7", 270, 4000),
        ("Honda Civic", 220, 3500),
        ("Subaru Impreza", 250, 4000),
        ("Mitsubishi Lancer Evolution", 280, 4200),
        ("Toyota AE86", 240, 3800),
        ("Nissan Silvia S15", 260, 4000),
        ("Toyota Chaser", 270, 4300),
        ("Nissan 350Z", 290, 4500),
        ("Mazda MX-5", 200, 3000),
        ("Honda NSX", 310, 5500),
        ("Subaru WRX STI", 280, 4600),
        ("Nissan 240SX", 250, 3900),
        ("Toyota Mark II", 260, 4100)
    ]

    for car in cars:
        cursor.execute("INSERT OR IGNORE INTO cars (name, max_speed, price) VALUES (?, ?, ?)", car)

    conn.commit()
    conn.close()

def get_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(zip([column[0] for column in cursor.description], row))
    return None

def add_user(user_id, username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def get_all_cars():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    conn.close()
    return cars

def get_car_by_name(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE name = ?", (name,))
    car = cursor.fetchone()
    conn.close()

    if car:
        return dict(zip([column[0] for column in cursor.description], car))
    return None

def add_user_car(user_id, car_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_cars (user_id, car_id) VALUES (?, ?)", (user_id, car_id))
    conn.commit()
    conn.close()

def get_user_car(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT car_id FROM user_cars WHERE user_id = ?", (user_id,))
    car = cursor.fetchone()
    conn.close()

    return car[0] if car else None

def update_user_data(user_id, data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = ?, races_won = ?, races_lost = ?, total_races = ? WHERE user_id = ?",
                   (data["balance"], data["races_won"], data["races_lost"], data["total_races"], user_id))
    conn.commit()
    conn.close()

def get_car_stats(car_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE car_id = ?", (car_id,))
    car = cursor.fetchone()
    conn.close()

    if car:
        return dict(zip([column[0] for column in cursor.description], car))
    return None

def increase_balance(user_id, amount):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def increase_salary(user_id, amount):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))

def buy_car(user_id, car_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cars WHERE name = ?", (car_name,))
    car = cursor.fetchone()
    
    if car:
        car_price = car[2]

        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
        
        if user_data:
            current_balance = user_data[0]
            if current_balance >= car_price:
                cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (car_price, user_id))
                cursor.execute("INSERT INTO user_cars (user_id, car_name) VALUES (?, ?)", (user_id, car_name))
                conn.commit()
                conn.close()
                return True  
            else:
                conn.close()
                return False
        else:
            conn.close()
            return False
    else:
        conn.close()
        return False

def update_user_car(user_id, new_car_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user_cars SET car_id = ? WHERE user_id = ?", (new_car_id, user_id))
    conn.commit()
    conn.close()

def get_car_choices():
    return [
        {"name": "Toyota Supra", "price": 5000, "max_speed": 250},
        {"name": "Nissan Skyline", "price": 6000, "max_speed": 270},
    ]

def start_race(user_id, opponent_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT car_id FROM user_cars WHERE user_id = ?", (user_id,))
    user_car = cursor.fetchone()
    cursor.execute("SELECT car_id FROM user_cars WHERE user_id = ?", (opponent_id,))
    opponent_car = cursor.fetchone()

    if user_car and opponent_car:
        cursor.execute("UPDATE users SET total_races = total_races + 1 WHERE user_id = ?", (user_id,))
        cursor.execute("UPDATE users SET total_races = total_races + 1 WHERE user_id = ?", (opponent_id,))
        conn.commit()

    conn.close()
