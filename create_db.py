import sqlite3


def create_db():
    connection = sqlite3.connect('foodmap.db')

    # Create User table
    connection.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        gender TEXT,
        age INTEGER,
        weight REAL,
        height REAL,
        active TEXT,
        target TEXT
    )
    ''')

    # Create Product table
    connection.execute('''
    CREATE TABLE products (
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
    CREATE TABLE feeding (
        id INTEGER PRIMARY KEY,
        feeding_date TIMESTAMP DEFAULT (DATE(CURRENT_TIMESTAMP)),
        feeding_time TIME DEFAULT (strftime('%H:%M:%S', 'now', 'localtime')),
        product_id INTEGER,
        product_quantity INTEGER,
        user_id INTEGER,
        FOREIGN KEY (product_id) REFERENCES products (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    connection.commit()
    connection.close()


def insert():
    conn = sqlite3.connect('foodmap.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (id, name, gender, age, weight, height, active, target) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   ('12356', 'John doe', 'male', 30, 80.3, 1.8, 'moderate', 'lose_weight'))

    users = cursor.execute("SELECT * FROM users")
    print(users.fetchall())

    conn.commit()
    conn.close()


def insert1():
    conn = sqlite3.connect('foodmap.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO feeding (product_id, product_quantity, user_id) VALUES (?, ?, ?)",
                   (1, 100, 123))

    f = cursor.execute("SELECT * FROM feeding")
    print(f.fetchall())

    conn.commit()
    conn.close()


