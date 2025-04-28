from flask import Flask, render_template, request, flash, url_for, redirect
import mysql.connector
from mysql.connector import errorcode
import pygal
from pygal.style import *

#create a flask app object and set app variables
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRECT_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

#create a connection object to the hr database
def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port="6603",
            database="hr"
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
            exit()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
            exit()
        else:
            print(err)
            print("ERROR: Service not available")
            exit()

    return mydb

def get_dependent(code):
    #get a connection to the database
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    query = 'SELECT * FROM dependents WHERE dependent_id = %s;'
    cursor.execute(query, (code,))
    dependent = cursor.fetchone()
    return dependent

#use app.route to create a flask view for the index page of the web app
@app.route('/')
def index():
    #get a db connection
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)

    #execute a query to get all dependents from the dependents table
    query = """
    SELECT d.dependent_id, CONCAT(d.first_name, ' ', d.last_name) AS dependent_name, d.relationship, CONCAT(e.first_name, " ", e.last_name) AS employee_name, e.employee_id
    FROM dependents d
    LEFT JOIN employees e ON d.employee_id = e.employee_id;
    """
    cursor.execute(query)

    #fetch the results
    dependents = cursor.fetchall()

    #send the results to the index.html template to be displayed
    return render_template('index.html', dependents=dependents)

#create a view/route to edit a dependent
#view/route responds to GET requests
#pass the dependent id as a url parameter
@app.route('/<code>/edit/', methods=('GET',))
def edit(code):
    #dependent id is sent as a url parameter
    #get the dependent id and send to the edit.html template
    dependent = get_dependent(code)
    return render_template('edit.html', dependent=dependent)

#create a route/view to edit a dependent
#route responds to POST requests
#pass the dependent id as a url parameter
@app.route('/<code>/edit/', methods=('POST',))
def edit_post(code):
    #get the dependent being edited
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)
    dependent = get_dependent(code)

    #get the dependent information from the form that was submitted
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    relationship = request.form['relationship']

    #validate that all necessary information was submitted
    #if any data missing flash an error
    if not first_name:
        flash('First name is required')
    elif not last_name:
        flash('Last name is required')
    elif not relationship:
        flash('Relationship is required')

    #if everythiog is ok: connect to the DB, update the record, 
    # close the connection, redirect to the homepage
    update_query = """
                UPDATE dependents 
                SET first_name = %s, last_name = %s, relationship = %s
                WHERE dependent_id = %s;
                """
    cursor.execute(update_query, (first_name, last_name, relationship, code))
    mydb.commit()
    mydb.close()

    #redirect to the hamepage
    return redirect(url_for('index'))

#route/view to delete a dependent
#delete route will only be acessible with the POST method
#the dependent id is passed as a url parameter
@app.route('/<code>/delete/', methods=('POST',))
def delete(code):
    #get a connection to the database
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)

    #get the dependent
    dependent = get_dependent(code)

    #create and execute the delete query, commit changes
    delete_query = 'DELETE FROM dependents WHERE dependent_id = %s;'
    cursor.execute(delete_query, (code,))

    #flash a succese message
    flash(f"Dependent {dependent['first_name']} was successfully deleted")

    mydb.commit()
    mydb.close()

    #redirect to the home page after deleting
    return redirect(url_for('index'))
    
#run the application
app.run(port=5005, debug=True)