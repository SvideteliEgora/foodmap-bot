from .database import DB
from datetime import date


class UserFeedingDB(DB):

    def get_feeding_today(self, user_id):
        today = date.today()
        search_result = self.cursor.execute("SELECT * FROM user_feeding WHERE user_id = ? and feeding_date = ?", (user_id, today))
        data = search_result.fetchall()
        result = []
        if data:
            for item in data:
                result.append({
                    'id': item[0],
                    'feeding_date': item[1],
                    'feeding_time': item[2],
                    'product_id': item[3],
                    'product_weight': item[4],
                    'user_id': item[5]
                })

        return result

    def add_eaten_product(self, product_id, user_id, product_weight):
        self.cursor.execute("INSERT INTO user_feeding (product_id, product_weight, user_id) VALUES (?, ?, ?)",
                            (product_id, product_weight, user_id))
        return self.conn.commit()

