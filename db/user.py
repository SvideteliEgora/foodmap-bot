from .database import DB


class UsersDB(DB):

    def user_exists(self, user_id: int):
        """Проверяем, есть ли юзер в БД"""
        result = self.cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id, data: dict):
        """Добавляем юзера в БД"""
        self.cursor.execute("INSERT INTO users (id, name, gender, age, weight, height, active, target) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (user_id, data['name'], data['gender'], data['age'], data['weight'], data['height'], data['active'], data['target']))
        return self.conn.commit()

    def delete_user(self, user_id: int):
        """Удаляем юзера"""
        self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        return self.conn.commit()

    def update_user(self, user_id, user_data: dict):
        """Обновляем данные юзера"""
        self.cursor.execute("UPDATE users SET name = ?, gender = ?, age = ?, weight = ?, height = ?, active = ?, target = ?",
                            (user_data['name'], user_data['gender'], user_data['age'], user_data['weight'], user_data['height'],
                             user_data['active'], user_data['target']))
        return self.conn.commit()

    def get_user_profile(self, user_id):
        """Получаем данные юзера по user_id"""
        result = self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return result.fetchone()