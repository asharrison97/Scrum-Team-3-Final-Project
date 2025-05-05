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
conn = sqlite3.connect('reservations.db')
conn.row_factory = dict_factory
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS reservations
(first text, last text, row test, col real, code integer unique)''')
# Insert a row of data

#trying to get it to show in the db viewer
try:
    cursor.execute("INSERT INTO reservations VALUES ('Amanda', 'Smith', 'E', 54, 627485)")
    conn.commit()
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
#cursor.execute("INSERT INTO reservations VALUES ('Gerry','Neil','A',61,364758)")

# Save (commit) the changes
#conn.commit()


# Query the data
cursor.execute("SELECT * FROM reservations")
#selects all

# Fetch all rows
rows = cursor.fetchall()
# Close the connection
conn.close()

#printing database rows for testing
for row in rows:
    print(row) #prints correctly


#all_reservations = cursor.execute().fetchall()

#run the application
app.run()


