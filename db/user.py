from .database import DB


class UsersDB(DB):

    def user_exists(self, user_id: int):
        """Проверяем, есть ли юзер в БД"""
        result = self.cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id, data: dict):
        """Добавляем юзера в БД"""
        self.cursor.execute("INSERT INTO users (id, name, gender, age, weight, height, active, target, daily_bzhu, "
                            "daily_calories, daily_water_allowance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (user_id, data['name'], data['gender'], data['age'], data['weight'], data['height'],
                             data['active'], data['target'], data['daily_bzhu'], data['daily_calories'],
                            data['daily_water_allowance']))
        return self.conn.commit()

    def delete_user(self, user_id: int):
        """Удаляем юзера"""
        self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        return self.conn.commit()

    def update_all_data_user(self, user_id, user_data: dict):
        """Обновляем данные юзера"""
        self.cursor.execute("UPDATE users SET name = ?, gender = ?, age = ?, weight = ?, height = ?, active = ?, "
                            "target = ?, daily_bzhu = ?, daily_calories = ?, daily_water_allowance = ? WHERE id = ?",
                            (user_data['name'], user_data['gender'], user_data['age'], user_data['weight'],
                             user_data['height'], user_data['active'], user_data['target'], user_data['daily_bzhu'],
                             user_data['daily_calories'], user_data['daily_water_allowance'], user_id))
        return self.conn.commit()

    def update_one_user_param(self, user_id, column, value):
        """Обнавляем один переданный параметр юзера"""
        self.cursor.execute("UPDATE users SET {} = ? WHERE id = ?".format(column), (value, user_id))
        return self.conn.commit()

    def get_user_profile(self, user_id) -> dict:
        """Получаем данные юзера по user_id"""
        result = self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        data = result.fetchone()
        user_profile = {
            'name': data[1],
            'gender': data[2],
            'age': data[3],
            'weight': data[4],
            'height': data[5],
            'active': data[6],
            'target': data[7],
            'daily_bzhu': data[8],
            'daily_calories': data[9],
            'daily_water_allowance': data[10]
        }

        return user_profile
