from .database import DB


class ProductsDB(DB):

    def add_product(self, user_id, product):
        """Добoвляем продукт"""
        calories = round(product['proteins'] * 4 + product['fats'] * 9 + product['carbohydrates'] * 4)
        self.cursor.execute("INSERT INTO products (title, proteins, fats, carbohydrates, calories, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                            (product['title'], product['proteins'], product['fats'], product['carbohydrates'], calories, user_id))
        return self.conn.commit()

    def delete_product(self, product_id, user_id):
        """Удаляем продукт юзера по его id"""
        self.cursor.execute("DELETE FROM products WHERE id = ? and user_id = ?", (product_id, user_id))
        return self.conn.commit()

    def get_one_product(self,):
        pass

    def get_all_products(self, user_id):
        """Получаем все продукты пользователя"""
        result = self.cursor.execute("SELECT * FROM products WHERE id = ?", (user_id,))
        return result.fetchall()

    def delete_all_products(self, user_id):
        """Удаляем все продукты пользователя"""
        self.cursor.execute("DELETE FROM products WHERE user_id = ?", (user_id,))
        return self.conn.commit()

    def update_product(self, product_id, new_product):
        """Обнoвляем продукт пользователя"""
        calories = round(new_product['proteins'] * 4 + new_product['fats'] * 9 + new_product['carbohydrates'] * 4)
        self.cursor.execute("UPDATE product SET title = ?, proteins = ?, fats = ?, carbohydrates = ?, calories = ? WHERE id = ?",
                            (new_product['title'], new_product['proteins'], new_product['fats'],
                             new_product['carbohydrates']), calories, product_id)
        return self.conn.commit()
