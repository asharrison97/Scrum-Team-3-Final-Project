from flask import Flask, render_template, request, flash, url_for, redirect, jsonify
import mysql.connector
from mysql.connector import errorcode
import pygal
from pygal.style import *
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'reservations.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'your_secret_key'

class Admin(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20), nullable=False)

#Create a class for reservations as well.

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/', methods=('GET',))
def admin():
    return render_template('admin.html')

@app.route('/admin/', methods=('POST,'))
def admin_post():
    username = request.form['username']
    password = request.form['password']

    if not username:
        flash('You must enter a username!')
        return render_template('index.html')
    elif not password:
        flash('You must enter a password!')
        return render_template('index.html')

@app.route('/reservations')
def reservations():
    return render_template('reservations.html')

#run the application
app.run(port=5007, debug=True)