# /usr/bin/python3.4
__author__ = 'Coachify'

from flask import Flask, send_from_directory
from flask import Response
from flask import render_template
from flask import request
from functools import wraps
import mysql.connector
import json
import collections

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql@123",
    database="timetable"
)
conn = database.cursor()


def check_authenticate(username, password):
    return username == '123' and password == '123'


def authenticate():
    return Response(
        'Authorized User Login Area!', 401,
        {'WWW-Authenticate': 'Basic realm="User Login"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_authenticate(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


# define static files path
app = Flask(__name__, static_url_path='/static')


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/Program')
def show_timetable():
    conn.execute("SELECT * FROM TimeTable")
    data = conn.fetchall()
    return render_template("timetable.html", data=data[::-1])


# MySQL datas convert to JSON format
@app.route('/Api')
def ApiTech():
    conn.execute("SELECT * FROM TimeTable")
    data = conn.fetchall()
    objects_list = []
    for row in data:
        selected = collections.OrderedDict()
        selected['Batch'] = row[0]
        selected['Monday'] = row[1]
        selected['Tuesday'] = row[2]
        selected['Wednesday'] = row[3]
        selected['Thursday'] = row[4]
        selected['Friday'] = row[5]
        selected['Saturday'] = row[6]
        selected['Sunday'] = row[7]
        objects_list.append(selected)

    return json.dumps(objects_list)


@app.route('/Program/Add')
@requires_auth
def AreaFill():
    conn.execute("SELECT * FROM TimeTable")
    data = conn.fetchall()
    return render_template("Add.html", data=data[::-1])


# data post method
@app.route("/Program/Add/Send", methods=['POST'])
@requires_auth
def AddPostTable():
    Batch = str(request.form['batch'])
    Monday = str(request.form['monday'])
    Tuesday = str(request.form['tuesday'])
    Wednesday = str(request.form['wednesday'])
    Thursday = str(request.form['thursday'])
    Friday = str(request.form['friday'])
    Saturday = str(request.form['saturday'])
    Sunday = str(request.form['sunday'])

    sql = "INSERT INTO TimeTable(Batch, Monday, Tuesday, Wednesday, Thursday, Friday ,Saturday, Sunday) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (Batch, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)
    conn.execute(sql, val)

    # conn.execute('''INSERT INTO TimeTable(Time, Monday, Tuesday, Wednesday, Thursday, Friday ,Saturday, Sunday) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
    #              [Time, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday])
    database.commit()
    return "<script>document.location ='/Program/Add'</script>"


# data delete method
@app.route("/Program/Delete/<batch>/", methods=['GET'])
@requires_auth
def DeletePostItems(batch):
    conn.execute("DELETE FROM TimeTable WHERE Batch = %s", (batch,))
    database.commit()
    return "Deleted Item"



if __name__ == '__main__':
    # define flask run adress and port
    app.run(debug=True)
