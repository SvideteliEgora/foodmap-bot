from .database import DB
from datetime import date


class FeedingDB(DB):

    def get_feeding_today(self, user_id):
        today = date.today()
        result = self.cursor.execute("SELECT * FROM feeding WHERE user_id = ? and feeding_date = ?", (user_id, today))
        return result.fetchall()

    def add_eaten_product(self, product_id, user_id, product_quantity):
        self.cursor.execute("INSERT INTO feeding (product_id, product_quantity, user_id) VALUES (?, ?, ?)",
                            (product_id, product_quantity, user_id))
        return self.conn.commit()

