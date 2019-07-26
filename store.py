from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="mysql",
                             db="store",
                             charset="utf8",
                             cursorclass=pymysql.cursors.DictCursor)


@get("/categories")
def get_categories():
    try:
        with connection.cursor() as cursor:
            sql = "select * from categories"
            cursor.execute(sql)
            return json.dumps({"CATEGORIES": cursor.fetchall()})
    except Exception as e:
        return json.dumps({'error': f'error with the db: {e}'})


@post("/category")
def add_category():
    name = request.forms.get("name")
    try:
        with connection.cursor() as cursor:
            sql = f"insert into categories (name) values ('{name}')"
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"CAT_ID": cursor.lastrowid, "CODE": 201})
    except Exception as e:
        return json.dumps({'error': f'could not add category: {e}'})


@delete('/category/<id:int>')
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = f"delete from categories where id = '{id}'"
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"CAT_ID": id})
    except Exception as e:
        return json.dumps({'error': f'could not remove category: {e}'})


@get("/products")
def get_products():
    try:
        with connection.cursor() as cursor:
            sql = "select * from products"
            cursor.execute(sql)
            return json.dumps({"PRODUCTS": cursor.fetchall()})
    except Exception as e:
        return json.dumps({'error': f'error with the db: {e}'})


@get('/product/<id:int>')
def get_product(id):
    try:
        with connection.cursor() as cursor:
            sql = f"select * from products where id = '{id}'"
            cursor.execute(sql)
            product = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCT": product, "CODE": 200})
    except Exception as e:
        return json.dumps({'error': f'error with the db: {e}'})


@get("/category/<id:int>/products")
def products_by_category(id):
    try:
        with connection.cursor() as cursor:
            sql = f"select * from products where category = '{id}'"
            cursor.execute(sql)
            return json.dumps({"PRODUCTS": cursor.fetchall()})
    except Exception as e:
        return json.dumps({'error': f'error with the db: {e}'})


@post('/product')
def add_or_edit_product():
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
                return json.dumps({"STATUS": "ERROR", "MSG": "Some parameters are missing", "CODE": 400})
        with connection.cursor() as cursor:
            products = json.loads(get_products())
            for prod in products['PRODUCTS']:
                if title != prod["title"]:
                    sql = f"insert into products (title, category, description, favorite, price, img_url) VALUES ('{title}', '{category}', '{desc}', '{favorite}', '{price}', '{img_url}')"
                else:
                    prod_id = prod["id"]
                    sql = f"update products set title = '{title}', category = '{category}', description = '{desc}', favorite = '{favorite}', price = '{price}', img_url = '{img_url}' where id = '{prod_id}'"
                    break
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "Product was added/updated successfully", "PRODUCT_ID": cursor.lastrowid, "CODE": 201})
    except Exception as e:
        return json.dumps({'error': f'could not add/edit product: {e}'})


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


# run(host='0.0.0.0', port=argv[1])
run(host="localhost", port=7000, debug=True, reloder=True)
