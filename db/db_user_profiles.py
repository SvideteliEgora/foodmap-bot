from .db import DB


class UserProfilesDB(DB):

    def user_exists(self, user_id: int):
        """Проверяем, есть ли юзер в БД"""
        result = self.cursor.execute("SELECT id FROM user_profiles WHERE id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id, data: dict):
        """Добавляем юзера в БД"""
        self.cursor.execute("INSERT INTO user_profiles (id, name, gender, age, weight, height, active, target, "
                            "daily_calories, daily_water_allowance, daily_pfc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (user_id, data['name'], data['gender'], data['age'], data['weight'], data['height'],
                             data['active'], data['target'], data['daily_calories'],
                             data['daily_water_allowance'], data['daily_pfc']))
        return self.conn.commit()

    def delete_user(self, user_id: int):
        """Удаляем юзера"""
        self.cursor.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
        return self.conn.commit()

    def update_all_data_user(self, user_id, user_data: dict):
        """Обновляем данные юзера"""
        self.cursor.execute("UPDATE user_profiles SET name = ?, gender = ?, age = ?, weight = ?, height = ?, active = ?, "
                            "target = ?, daily_bzhu = ?, daily_calories = ?, daily_water_allowance = ? WHERE id = ?",
                            (user_data['name'], user_data['gender'], user_data['age'], user_data['weight'],
                             user_data['height'], user_data['active'], user_data['target'], user_data['daily_bzhu'],
                             user_data['daily_calories'], user_data['daily_water_allowance'], user_id))
        return self.conn.commit()

    def update_one_user_param(self, user_id, column, value):
        """Обнавляем один переданный параметр юзера"""
        self.cursor.execute("UPDATE user_profiles SET {} = ? WHERE id = ?".format(column), (value, user_id))
        return self.conn.commit()

    def get_one_user_param(self, user_id, column):
        """Получаем конкретный параметр"""
        search_result = self.cursor.execute("SELECT {}  FROM user_profiles  WHERE id = ?".format(column), (user_id,))
        data = search_result.fetchone()[0]

        return data

    def get_pfc_ratio(self, user_id):
        """Получаем соотношение БЖУ"""
        search_result = self.cursor.execute("SELECT pfc_ratio FROM user_profiles WHERE id = ?", (user_id,))
        result = search_result.fetchone()
        pfc_ratio_list = result[0].split('/')
        data = {
            'p': pfc_ratio_list[0],
            'f': pfc_ratio_list[1],
            'c': pfc_ratio_list[2]
        }

        return data

    def get_daily_pfc(self, user_id):
        """Получаем ежедневное БЖУ пользователя"""
        search_result = self.cursor.execute("SELECT daily_pfc FROM user_profiles WHERE id = ?", (user_id,))
        result = search_result.fetchone()
        pfc_ratio_list = result[0].split('/')
        data = {
            'p': pfc_ratio_list[0],
            'f': pfc_ratio_list[1],
            'c': pfc_ratio_list[2]
        }

        return data

    def get_user_profile(self, user_id) -> dict:
        """Получаем данные юзера по user_id"""
        search_result = self.cursor.execute("SELECT * FROM user_profiles WHERE id = ?", (user_id,))
        result = search_result.fetchone()
        data = {
            'id': result[0],
            'name': result[1],
            'gender': result[2],
            'age': result[3],
            'weight': result[4],
            'height': result[5],
            'active': result[6],
            'target': result[7],
            'pfc_ratio': result[8],
            'daily_calories': result[9],
            'daily_water_allowance': result[10],
            'daily_pfc': result[11]
        }

        return data
