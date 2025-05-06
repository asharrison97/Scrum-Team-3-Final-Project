from flask import Flask, render_template, request, flash, url_for, redirect, jsonify
import mysql.connector
from mysql.connector import errorcode
import pygal
from pygal.style import *
import sqlite3

#create a flask app object and set app variables
app = Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/')
def admin():
    return render_template('admin.html')

@app.route('/reservations')
def reservations():
    return render_template('reservations.html')

#get a db connection
connR = sqlite3.connect('reservations.db') # reservations connection
connA = sqlite3.connect('admin.db') #admin connection
connR.row_factory = dict_factory
connA.row_factory = dict_factory
cursorR = connR.cursor() #reservations cursor
cursorA = connA.cursor() #admin cursor

#initiate tables if not already 
cursorR.execute('''CREATE TABLE IF NOT EXISTS reservations
(first text, last text, row test, col real, code integer)''')
cursorA.execute('''CREATE TABLE IF NOT EXISTS admin
(user text, password text)''') 

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
connA.commit()


# Query the data

# Fetch all rows
rowsR = cursorR.execute("SELECT * FROM reservations").fetchall()
rowsA = cursorA.execute("SELECT * FROM admin").fetchall()
# Close the connection
connR.close()
connA.close()

#printing database rows for testing
for row in rowsR:
    print(row) #prints correctly

#printing database rows for testing
for row in rowsA:
    print(row) #prints correctly


#run the application
app.run()


