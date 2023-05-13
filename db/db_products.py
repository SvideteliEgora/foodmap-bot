from .db import DB


class ProductsDB(DB):
    def find_products(self, product_name) -> list:
        """Находим все пересечения с product_name"""
        query = "SELECT * FROM products WHERE title LIKE ?"
        result_query_title = self.cursor.execute(query, ('%' + product_name.title() + '%',)).fetchall()
        result_query_lower = self.cursor.execute(query, ('%' + product_name.lower() + '%',)).fetchall()
        full_result = result_query_lower + result_query_title
        results = []
        for item in full_result:
            results.append({
                'id': item[0],
                'title': item[1],
                'calories': item[2],
                'proteins': item[3],
                'fats': item[4],
                'carbohydrates': item[5]
            })
        return results

    def get_product(self, product_id) -> dict:
        """Находим продукт по product_id"""
        search_result = self.cursor.execute("SELECT * from products WHERE id = ?", (product_id,))
        result = search_result.fetchone()
        data = {
            'id': result[0],
            'title': result[1],
            'calories': result[2],
            'proteins': result[3],
            'fats': result[4],
            'carbohydrates': result[5]
        }

        return data

