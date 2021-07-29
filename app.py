#importing python library
from flask import (Flask,redirect,render_template,request,session,url_for,jsonify) 
from flaskext.mysql import MySQL
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
    return render_template('enrol.html')



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