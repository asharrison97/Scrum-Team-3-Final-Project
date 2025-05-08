from flask import Flask, render_template, request, flash, url_for, redirect, jsonify
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from mysql.connector import errorcode
import pygal
import os
from pygal.style import *
import sqlite3

#create a flask app object and set app variables
app = Flask(__name__)
app.secret_key = "super secret key"
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'reservations.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Reservation(db.Model):
    code = db.Column(db.String(200), primary_key=True)
    first = db.Column(db.String(200), nullable=False)
    last = db.Column(db.String(200), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Task {self.code}>'
# class Admin(db.Model):
#     user = db.Column(db.String(200), nullable=False)
#     password = db.Column(db.String(20), nullable=False)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

codeString = "INFOTC4320"
def alternate_strings(str1, codeString):
    result = ''.join([a + b for a, b in zip(str1, codeString)])  # Combine pairs of characters
    result += str1[len(codeString):] + codeString[len(str1):]  # Append leftover characters from the longer string
    return result

#get a db connection
def create_connection(db_file):
    conn = sqlite3.connect(db_file, check_same_thread=False)
    conn.row_factory = dict_factory
    return conn

def create_reservation(conn, reservation):
    sql = ''' INSERT INTO reservations(code, first, last, row, col) VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, reservation)
    conn.commit()
# connR = sqlite3.connect('reservations.db', check_same_thread=False) # reservations connection
# connA = sqlite3.connect('admin.db') #admin connection
# connR.row_factory = dict_factory
# connA.row_factory = dict_factory
# cursorR = connR.cursor() #reservations cursor
# cursorA = connA.cursor() #admin cursor

#initiate tables if not already 
# cursorR.execute('''CREATE TABLE IF NOT EXISTS reservations
# ( code integer, first text, last text, row test, col real)''')
# cursorA.execute('''CREATE TABLE IF NOT EXISTS admin
# (user text, password text)''') 

# Logic for loading index page with GET and POST methods.
@app.route('/', methods=('GET',))
def index():
    return render_template('index.html')

@app.route("/" , methods=['POST'])
def index_get_post():
    select = request.form.get('options')
    if select == "default":
        flash('Please select a valid option!')
        return redirect(url_for('index'))
    elif select == "administrator":
        return redirect(url_for('admin'))
    elif select == "reservations":
        return redirect(url_for('reservations'))

# Logic for loading admin page with GET and POST methods.
@app.route('/admin/', methods=('GET',))
def admin():
    return render_template('admin.html')

@app.route('/admin/', methods=('POST',))
def admin_post():
    username = request.form['username']
    password = request.form['password']

    if not username:
        flash('You must enter a username!')
        return redirect(url_for('index'))
    elif not password:
        flash('You must enter a password!')
        return redirect(url_for('index'))

# Logic for loading reservations page with GET and POST methods.
@app.route('/reservations', methods=['GET'])
def reservations():
    return render_template('reservations.html')

@app.route('/reservations', methods=["POST"])
def reservations_post():
    firstName = request.form['first']
    lastName = request.form['last']
    row = request.form['row']
    col = request.form['seat']
    code = alternate_strings(firstName, codeString)

    if not firstName:
        flash('You must enter a first name!')
        return render_template('reservations.html')
    elif not lastName:
        flash('You must enter a lat name!')
        return render_template('reservations.html')
    
    conn = create_connection('reservations.db')
    new_reservation = Reservation(code=code, first=firstName, last=lastName, row=row, col=col)
    create_reservation(conn, (new_reservation.code, new_reservation.first, new_reservation.last, new_reservation.row, new_reservation.col))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Insert a row of data testing

#trying to get it to show in the db viewer
# try:
#     cursor.execute("INSERT INTO reservations VALUES ('Amanda', 'Smith', 'E', 54, 627485)")
#     conn.commit()
# except sqlite3.Error as e:
#     print(f"An error occurred: {e}")
#cursor.execute("INSERT INTO reservations VALUES ('Gerry','Neil','A',61,364758)")

#cursorA.execute("INSERT INTO admin VALUES ('AdminBigBoss123','$pot1987')")

# Save (commit) the changes
#connA.commit()


# Query the data

# Fetch all rows
# rowsR = cursorR.execute("SELECT * FROM reservations").fetchall()
# rowsA = cursorA.execute("SELECT * FROM admin").fetchall()
# Close the connection

#connA.close()

# #printing database rows for testing
# for row in rowsR:
#     print(row) #prints correctly

# #printing database rows for testing
# for row in rowsA:
#     print(row) #prints correctly


#run the application
app.run()