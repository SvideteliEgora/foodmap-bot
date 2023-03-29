from .database import DB


class BotProductsDB(DB):
    def find_products(self, product_name):
        """Находим все пересечения с product_name"""
        query = "SELECT * FROM bot_products WHERE title LIKE ?"
        result_query_title = self.cursor.execute(query, ('%' + product_name.title() + '%',)).fetchall()
        result_query_lower = self.cursor.execute(query, ('%' + product_name.lower() + '%',)).fetchall()
        full_result = result_query_lower + result_query_title
        result_json = []
        for item in full_result:
            result_json.append({
                'id': item[0],
                'title': item[1],
                'calories': item[2],
                'proteins': item[3],
                'fats': item[4],
                'carbohydrates': item[5]
            })
        return result_json

