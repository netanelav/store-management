from bottle import run, template, static_file, get, post, delete, request, response
from dal.mysql_db_adapter import MySqlDBAdapter
import json
import pymysql


_db_adapter = MySqlDBAdapter()

def start():
    run(host="localhost", port=7000, debug=True, reloder=True)

@get("/categories")
def get_categories():
    categories = _db_adapter.get_categories()
    return categories


@get("/category/<id:int>/products")
def products_by_category(id):
    products_by_category = _db_adapter.products_by_category(id)
    return products_by_category


@post("/category")
def add_category():
    add_category = _db_adapter.add_category()
    return add_category


@delete('/category/<id:int>')
def delete_category(id):
    delete_category = _db_adapter.delete_category(id)
    return delete_category


@get("/products")
def get_products():
    get_products = _db_adapter.get_products()
    return get_products


@get('/product/<id:int>')
def get_product(id):
    get_product = _db_adapter.get_product(id)
    return get_product


@post('/product')
def add_or_edit_product():
    add_or_edit_product = _db_adapter.add_or_edit_product()
    return add_or_edit_product


@delete('/product/<id:int>')
def delete_product(id):
    delete_product = _db_adapter.delete_product(id)
    return delete_product


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
