#importing python library
from flask import Flask, redirect, render_template, request, session, url_for
from flaskext.mysql import MySQL
import pymysql
import re


#initializing flask app
app = Flask(__name__)
        
#creating sql object
mysql = MySQL(app)

#setting a secret key for your application
app.secret_key = "finalyear"

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
    
    #check for user details
    if request.method == "POST": 
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        idtype = request.form["idtype"]
        idnumber = request.form["idnumber"]
        pword = request.form["pword"]
        confpword = request.form["confpword"]

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM enrol WHERE idnumber = %s and idtype = %s and pword =%s', (idnumber, idtype, pword))
        account = cursor.fetchone()

        # Check if account exists show error and validation checks
        if account:
            msg = 'Account already exists!'

        elif not re.match(r'[A-Za-z0-9]+', firstname):
            msg = 'Username must contain only characters and numbers!'

        elif not re.match(r'[A-Za-z0-9]+', firstname):
            msg = 'Username must contain only characters and numbers!'
        elif not idnumber or not idtype or not pword:
            msg = 'Please fill out the form!'
        else:
        #check if account exist in MySQL:
            cursor.execute('INSERT INTO enrol VALUES(%s, %s, %s, %s, %s, %s)',(firstname, lastname, idtype, idnumber, pword, confpword))    
        conn.commit()
        cursor.close()
        #redirect url to facial for the next process
        return redirect("/facial")

    return render_template('enrol.html')

            

@app.route('/verify/', methods=['GET', 'POST'])
def verify():
    # Output message if something goes wrong...
    msg = 'Incorrect user details/password!'
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'idtype' in request.form and 'idnumber' in request.form and 'pword' in request.form:
        # Create variables for easy access
        idtype = request.form['idtype']
        idnumber = request.form['idnumber']
        pword = request.form['pword']
        # Check if account exists using MySQL
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM enrol WHERE idtype = %s AND idnumber = %s AND pword = %s', (idtype, idnumber, pword))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['idtype'] = account['idtype']
            session['idnumber'] = account['idnumber']
            #session['pword'] = pword['pword']
            # Redirect to home page
            return redirect("/facial")
        else:
            # Account doesnt exist or incorrect details
            flash = "Incorrect user details!"
    # Show the verify page with message (if any)
    return render_template('verify.html', msg =msg)



@app.route('/facial/', methods=['GET','POST'])
def facial():
    return render_template('facial.html')



@app.route('/register/', methods=['GET','POST'])
def register():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        phonenumber = request.form["phonenumber"]
        dateofbirth = request.form["dateofbirth"]
        middlename = request.form["middlename"]
        idnumber = request.form["idnumber"]
        dateissued = request.form["dateissued"]
        address = request.form["address"]
        email = request.form["email"]
        
        #check if account exist in MySQL:
        cursor.execute('INSERT INTO register VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s)',(firstname, lastname, phonenumber, dateofbirth, middlename, idnumber, dateissued, address,email ))
        
        conn.commit()
        cursor.close()
        #redirect url to facial for the next process
        #return "Hello, you have successfully registred your sim card"
        return redirect("/facial")

    return render_template('register.html')







#running the app and turning debug mode on
if __name__ == "__main__":
    app.run(debug =True)