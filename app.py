#importing python library
from flask import Flask, redirect, render_template, request, session, url_for
from flaskext.mysql import MySQL
import pymysql
import re


#initializing flask app
app = Flask(__name__)
        
#creating sql object
mysql = MySQL(app)

#MySQL configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'simcard'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


#seting my flask route
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/enrol/", methods=["GET","POST"]) 
def enrol():
    #connect 
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    msg = ""
    #check for user details
    if request.method == "POST": 
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        idtype = request.form["idtype"]
        idnumber = request.form["idnumber"]
        pword = request.form["pword"]
        confpword = request.form["confpword"]

        #check if account exist in MySQL:
        cursor.execute('INSERT INTO enrol VALUES(%s, %s, %s, %s, %s, %s)',(firstname, lastname, idtype, idnumber, pword, confpword))
        
        conn.commit()
        cursor.close()
        #redirect url to facial for the next process
        return redirect("/facial")

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