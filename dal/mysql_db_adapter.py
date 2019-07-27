from .base_database_adapter import BaseDatabaseAdapter
from bottle import template, request, response
import pymysql
import json


class MySqlDBAdapter(BaseDatabaseAdapter):
    def __init__(self):
        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password="mysql",
                                          db="store",
                                          charset="utf8",
                                          cursorclass=pymysql.cursors.DictCursor)

    def get_categories(self):
        try:
            with self.connection.cursor() as cursor:
                sql = "select * from categories"
                cursor.execute(sql)
                return json.dumps({"STATUS": "SUCCESS", "CATEGORIES": cursor.fetchall()})
        except Exception as e:
            return json.dumps({"STATUS": "ERROR", "MSG": f"{e}"})

    def products_by_category(self, id):
        try:
            with self.connection.cursor() as cursor:
                sql = f"select * from products where category = '{id}' order by id asc, favorite desc"
                cursor.execute(sql)
                return json.dumps({"STATUS": "SUCCESS", "MSG": "Products fetched", "PRODUCTS": cursor.fetchall()})
        except Exception as e:
            if response.status_code == 404:
                return json.dumps({"STATUS": "ERROR", "MSG": "category not found"})
            elif response.status_code == 500:
                return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CODE": 500})
            else:
                return json.dumps({"STATUS": "ERROR", "MSG": f"{e}"})

    def add_category(self):
        name = request.forms.get("name")
        try:
            with self.connection.cursor() as cursor:
                sql = f"insert into categories (name) values ('{name}')"
                cursor.execute(sql)
                self.connection.commit()
                response.status = 201
                return json.dumps({"STATUS": "SUCCESS", "MSG": "The category was successfully created", "CAT_ID": cursor.lastrowid})
        except Exception as e:
            if response.status_code == 200:
                return json.dumps({"STATUS": "ERROR", "MSG": "category already exists"})
            elif response.status_code == 400:
                return json.dumps({"STATUS": "ERROR", "MSG": "bad request"})
            elif response.status_code == 400:
                return json.dumps({"STATUS": "ERROR", "MSG": "internal error"})
            else:
                return json.dumps({"STATUS": "ERROR", "MSG": f"{e}"})

    def delete_category(self, id):
        try:
            with self.connection.cursor() as cursor:
                sql = f"delete from categories where id = '{id}'"
                cursor.execute(sql)
                self.connection.commit()
                response.status = 201
                return json.dumps({"STATUS": "SUCCESS", "MSG": "Category was successfully deleted", "CAT_ID": id})
        except Exception as e:
            if response.status_code == 404:
                return json.dumps({"STATUS": "ERROR", "MSG": "Category not found", "CAT_ID": id})
            elif response.status_code == 500:
                return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CAT_ID": id})
            else:
                return json.dumps({"STATUS": "ERROR", "MSG": f"{e}"})

    def get_products(self):
        try:
            with self.connection.cursor() as cursor:
                sql = "select * from products"
                cursor.execute(sql)
                return json.dumps({"STATUS": "SUCCESS", "MSG": "Products fetched", "PRODUCTS": cursor.fetchall()})
        except Exception as e:
            return json.dumps({"STATUS": "ERROR", "MSG": f"Internal Error{e}"})

    def get_product(self, id):
        try:
            with self.connection.cursor() as cursor:
                sql = f"select * from products where id = '{id}'"
                cursor.execute(sql)
                return json.dumps({"STATUS": "SUCCESS", "MSG": "The product was fetched successfully", "PRODUCT": cursor.fetchall()})
        except Exception as e:
            if response.status_code == 404:
                return json.dumps({"STATUS": "ERROR", "MSG": "Product was not found"})
            elif response.status_code == 500:
                return json.dumps({"STATUS": "ERROR", "MSG": "Internal error"})
            else:
                return json.dumps({"STATUS": "ERROR", "MSG": f"{e}"})

    def add_or_edit_product(self):
        id = request.forms.get('id')
        category = request.forms.get('category')
        title = request.forms.get('title')
        desc = request.forms.get('desc')
        favorite = request.forms.get('favorite')
        price = request.forms.get('price')
        img_url = request.forms.get('img_url')
        favorite = 1 if favorite == "on" else 0
        try:
            for i in [category, title, desc, favorite, price, img_url]:
                if i == "" or i is None:
                    return json.dumps({"STATUS": "ERROR", "MSG": "Some parameters are missing"})
            with self.connection.cursor() as cursor:
                products = json.loads(self.get_products())
                for prod in products['PRODUCTS']:
                    if title != prod["title"]:
                        sql = f"insert into products (title, category, description, favorite, price, img_url) VALUES ('{title}', '{category}', '{desc}', '{favorite}', '{price}', '{img_url}')"
                    else:
                        prod_id = prod["id"]
                        sql = f"update products set title = '{title}', category = '{category}', description = '{desc}', favorite = '{favorite}', price = '{price}', img_url = '{img_url}' where id = '{prod_id}'"
                        break
                cursor.execute(sql)
                self.connection.commit()
                response.status = 201
                return json.dumps({"STATUS": "SUCCESS", "MSG": "Product was added/updated successfully", "PRODUCT_ID": cursor.lastrowid})
        except Exception as e:
            if response.status_code == 404:
                return json.dumps({"STATUS": "ERROR", "MSG": "Category not found"})
            elif response.status_code == 500:
                return json.dumps({"STATUS": "ERROR", "MSG": "Internal Error"})
            else:
                return json.dumps({"STATUS": "ERROR", "MSG": f"{e}"})

    def delete_product(self, id):
        try:
            with self.connection.cursor() as cursor:
                sql = f"delete from products where id = '{id}'"
                cursor.execute(sql)
                self.connection.commit()
                response.status = 201
                return json.dumps({"STATUS": "SUCCESS", "MSG": "The product was deleted successfully"})
        except Exception as e:
            if response.status_code == 404:
                return json.dumps({"STATUS": "ERROR", "MSG": "Product not found"})
            elif response.status_code == 500:
                return json.dumps({"STATUS": "ERROR", "MSG": "Internal error"})
            else:
                return json.dumps({"STATUS": "ERROR", "MSG": f"{e}"})
