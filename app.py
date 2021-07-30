#importing python library
from flask import (Flask,redirect,render_template,request,session,url_for,jsonify) 
from flaskext.mysql import MySQL
from pymysql import connect
import pymysql
import re
import json
import requests
from base64 import *


#initializing flask app
app = Flask(__name__)
        
#creating sql object
mysql = MySQL()

#MySQL configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'simregistration'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


#seting my flask route
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/enrol/', methods=['GET','POST']) 
def enrol():
    #connect to my database

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    #output message if something goes wrong
    msg = "Check your details provided"

    #checking if "user detais" exists 
    if request.method == "POST" and 'firstname' in request.form and 'lastname'in request.form and 'idtype' in request.form and 'idnumber' in request.form and 'password' in request.form:
        #create varibales for easy access
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        idtype = request.form['idtype']
        idnumber = request.form['idnumber']
        password = request.form['password']

        #check if account exists uinsg MYSQL
        cursor.execute(
            'SELECT * FROM enrol WHERE idnumber = %s AND firstname = %s AND idtype = %s', (idnumber,firstname,idtype))
        account = cursor.fetchone()

        #if account exisit show error and validation checks
        if account:
            msg  = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',idnumber):
            msg = 'invalid idnumber'
        elif not re.match(r'[A-Za-z0-9]+' , firstname):
            msg = 'firstname and lastname must conatin only charcater and numbers!'
        elif not idtype or not password or not idnumber:
            msg = 'Kindly fill the form!'
        else:
            cursor.execute('INSERT INTO account VALUES (NULL, %s, %s, %s, %s)', 
            (firstname,lastname,idtype,idnumber,password))
            conn.commit()

            msg = 'you have enrol sucesssfully! visit the home page and verify'
    elif request.method == 'POST':
        msg = 'Kindly fill the form!'
    
    #shows the enrollment form with message if any
    return render_template('enrol.html', msg = msg)

            





@app.route('/verify/', methods=['GET', 'POST'])
def verify():
    return render_template('verify.html')



@app.route('/facial/', methods=['GET','POST'])
def facial():
    return render_template('facial.html')



@app.route('/register/', methods=['GET','POST'])
def register():
    return render_template('register.html')





#running the app and turning debug mode on
if __name__ == "__main__":
    app.run(debug =True)