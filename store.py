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
            sql = "select * from category"
            cursor.execute(sql)
            return json.dumps({"CATEGORIES": cursor.fetchall()})
    except Exception as e:
        return json.dumps({'error': f'error with the db: {e}'})


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
