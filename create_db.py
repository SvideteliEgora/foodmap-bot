import sqlite3


def create_db():
    connection = sqlite3.connect('foodmap.db')

    # Create User table
    connection.execute('''
    CREATE TABLE user_profiles (
        id INTEGER PRIMARY KEY,
        name TEXT,
        gender TEXT,
        age INTEGER,
        weight REAL,
        height REAL,
        active TEXT,
        target TEXT,
        daily_bzhu TEXT DEFAULT "30/30/40",
        daily_calories INTEGER,
        daily_water_allowance INTEGER
    )
    ''')

    # Create Product table
    connection.execute('''
    CREATE TABLE user_products (
        id INTEGER PRIMARY KEY,
        title TEXT,
        proteins REAL,
        fats REAL,
        carbohydrates REAL,
        calories INTEGER,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Create Feeding table
    connection.execute('''
    CREATE TABLE user_feeding (
        id INTEGER PRIMARY KEY,
        feeding_date TIMESTAMP DEFAULT (DATE(CURRENT_TIMESTAMP)),
        feeding_time TIME DEFAULT (strftime('%H:%M:%S', 'now', 'localtime')),
        product_id INTEGER,
        product_quantity INTEGER,
        user_id INTEGER,
        FOREIGN KEY (product_id) REFERENCES search_products (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    connection.commit()
    connection.close()


def update_column():

    # создаем соединение с базой данных
    conn = sqlite3.connect('foodmap.db')
    c = conn.cursor()

    # изменяем название столбца
    c.execute("ALTER TABLE user_feeding RENAME COLUMN product_quantity TO product_weight")

    conn.commit()
    conn.close()


def add_column():
    conn = sqlite3.connect('foodmap.db')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE user_profiles ADD COLUMN daily_pfc TEXT")
    conn.commit()
    conn.close()
