#importing python library
from flask import Flask, redirect, render_template, request, session, url_for
from flaskext.mysql import MySQL
import pymysql
import re


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


@app.route("/enrol/", methods=["GET","POST"]) 
def enrol():
    #connect 
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    msg = ""
    #check for user details
    if request.method == "POST" and "firstname" in request.form and "lastname" in request.form and "idnumber" in request.form and "idtype" in request.form and "pword" in request.form and "confpword" in request.form:
        #create variables for each access
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        idnumber = request.form["idnumber"]
        idtype = request.form["idtype"]
        pword = request.form["pword"]
        confpword = request.form["confpword"]

        #check if account exist in MySQL:
        cursor.execute(
            'SELECT * FROM enrol WHERE firstname = %s and lastname = %s and idnumber = %s and idtype = %s and pword = %s and confpword',(firstname, lastname, idnumber, idtype, pword, confpword))
        account = cursor.fetchone()
        #if account exists show error and validation checks
        if account:
            msg = "Account already exist"
        elif not re.match(r'[A-Za-z0-9]+',firstname):
            msg = 'firstname must contain only characters and numbers!'
        elif not firstname or not idnumber or not pword:
            msg = 'please fill out the form'
        else:
            cursor.execute('INSERT INTO enrol VALUES (NULL, %s, %s, %s, %s, %s)',
            (firstname, lastname, idnumber, idtype, pword, confpword))

            conn.commit()

            msg = "You have Successfully Registered!"
    elif request.method == "POST":
        msg = "Please fill out the form!"
        #redirect url to facial for the next process
        #return redirect("/facial")

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