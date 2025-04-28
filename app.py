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
    #get a db connection
    # conn = sqlite3.connect('reservations.db')
    # conn.row_factory = dict_factory
    # cur = conn.cursor()
    # all_reservations = cur.execute().fetchall()

    return render_template('index.html')

#run the application
app.run()


