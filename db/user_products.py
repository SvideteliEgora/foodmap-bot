from .database import DB


class UserProductsDB(DB):

    def add_product(self, user_id, product):
        """Добoвляем продукт"""
        calories = round(product['proteins'] * 4 + product['fats'] * 9 + product['carbohydrates'] * 4)
        self.cursor.execute("INSERT INTO user_products (title, proteins, fats, carbohydrates, calories, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                            (product['title'], product['proteins'], product['fats'], product['carbohydrates'], calories, user_id))
        return self.conn.commit()

    def delete_product(self, product_id, user_id):
        """Удаляем продукт юзера по его id"""
        self.cursor.execute("DELETE FROM user_products WHERE id = ? and user_id = ?", (product_id, user_id))
        return self.conn.commit()

    def get_one_product(self,):
        pass

    def get_all_products(self, user_id):
        """Получаем все продукты пользователя"""
        search_result = self.cursor.execute("SELECT * FROM user_products WHERE id = ?", (user_id,))
        result = search_result.fetchall()
        all_products_by_user = []
        if result:
            for item in result:
                all_products_by_user.append({
                    'id': item[0],
                    'title': item[1],
                    'proteins': item[2],
                    'fats': item[3],
                    'carbohydrates': item[4],
                    'calories': item[5],
                    'user_id': item[6]
                })

        return all_products_by_user

    def delete_all_products(self, user_id):
        """Удаляем все продукты пользователя"""
        self.cursor.execute("DELETE FROM user_products WHERE user_id = ?", (user_id,))
        return self.conn.commit()

    def update_product(self, product_id, new_product):
        """Обнoвляем продукт пользователя"""
        calories = round(new_product['proteins'] * 4 + new_product['fats'] * 9 + new_product['carbohydrates'] * 4)
        self.cursor.execute("UPDATE user_products SET title = ?, proteins = ?, fats = ?, carbohydrates = ?, calories = ? WHERE id = ?",
                            (new_product['title'], new_product['proteins'], new_product['fats'],
                             new_product['carbohydrates']), calories, product_id)
        return self.conn.commit()
