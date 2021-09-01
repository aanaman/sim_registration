#importing python library
from flask import Flask, json, redirect, render_template, request, session, url_for, jsonify
import  requests
from flask.helpers import flash
from flaskext.mysql import MySQL
import pymysql
import re
import bcrypt
from base64 import *
import face_recognition


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


def get_base64(files):
    if len(files) > 0:
        b64file = b64encode(files['image'].read()).decode("utf-8")
        return b64file
    return ""


#seting my flask route
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/enrol/", methods=["GET","POST"]) 
def enrol():
    msg = ""
    error = ""
    #connect 
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    #check for user details
    if request.method == "POST" and "firstname" in request.form and "lastname" in request.form and "idtype" in request.form and "idnumber" in request.form and "pword" in request.form and "confpword" in request.form: 
        #create a variable for easy access
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        idtype = request.form["idtype"]
        idnumber = request.form["idnumber"]
        pword = request.form["pword"]
        confpword = request.form["confpword"]

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM enrol WHERE idnumber = %s', (idnumber))
        account = cursor.fetchone()

        # Check if account exists show error and validation checks
        if account:
            msg = 'Id number already exists!'

        elif not re.match(r'[A-Za-z0-9]+', firstname):
            msg = 'firstname must contain only characters and numbers!'

        elif not re.match(r'[A-Za-z0-9]+', lastname):
            msg = 'lastname must contain only characters and numbers!'

        elif not re.match(r'[A-Za-z0-9@#$]{6,12}', pword):

            msg = 'password must be 6 degit with special character!'

        elif len(idnumber) < 10 :
            error = 'Id number is not correct!'

        elif pword != confpword :
            error = 'password do not match'

        elif not firstname or not lastname or not idtype or not idnumber or not pword or not confpword:
            msg = 'Please fill out the form!'
            
        else:
        #check if account exist in MySQL:
            cursor.execute('INSERT INTO enrol VALUES(%s, %s, %s, %s, %s, %s)',(firstname, lastname, idtype, idnumber, pword, confpword))
            #hashed = bcrypt.hashpw(pword.encode('utf-8'),bcrypt.gensalt()) 
            conn.commit()
            cursor.close()
            return redirect("/verify")
    
    elif request.method == 'POST':
        msg = 'please fill the form!'
        #redirect url to facial for the next process

    return render_template('enrol.html', msg = msg , error = error)

            

@app.route('/verify/', methods=['GET', 'POST'])
def verify():
    msg = ""
    # Output message if something goes wrong...
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
            #session['id'] = account['id']
            session['idtype'] = account['idtype']
            session['idnumber'] = account['idnumber']
            #session['pword'] = pword['pword']
            # Redirect to home page
        
            return redirect("/facial")
        else:
            # Account doesnt exist or incorrect details
            msg = 'Invalid details!' 
    # Show the verify page with message (if any)
    return render_template('verify.html', msg = msg)



@app.route('/facial', methods=['GET','POST'])
def facial():
    if request.method =="POST":
        if request.method == "POST":
            image_file = request.form['file']
            path = os.path.join('./incomingImage',image_file.filename)
            image_file.save(path)
            return "good"

        """"image = request.form["image"]
        idnumber = "1234567892"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT image FROM capturedface WHERE idnumber = %s ", (idnumber))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        picture_of_existing = face_recognition.load_image_file(account)
        existing_face_encoding = face_recognition.face_encodings(picture_of_existing)[0]

        # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

        unknown_picture = face_recognition.load_image_file(image)
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

        # Now we can see the two face encodings are of the same person with `compare_faces`!

        results = face_recognition.compare_faces([existing_face_encoding], unknown_face_encoding)

        if results[0] == True:
            print("It's a picture of me!")
        else:
            print("It's not a picture of me!")


        api_key = 'T_72876c28-a773-4ac8-b650-4b0d27a6489b'
        headers = {'x-authorization': 'Basic edwardakorlie73@gmail.com:{api_key}'.format(api_key= api_key),'Content-Type': 'application/json'}
        data = request.form
        print(data)
        print(request.files)
        b64file = get_base64(request.files)
        payload = {"gallery":"tsatsu_bd","identifier":data["idnumber"],"image":b64file}
        print(headers)
        r = requests.post('https://api.bacegroup.com/v2/validate/voters_id', headers=headers, data=json.dumps(payload))

        print(r.text)

        return redirect('/register')"""


    return render_template('facial.html' )



@app.route('/register/', methods=['GET','POST'])
def register():
    msg = ""
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'idnumber' in request.form:
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        phonenumber = request.form["phonenumber"]
        dateofbirth = request.form["dateofbirth"]
        middlename = request.form["middlename"]
        idtype = request.form["idtype"]
        idnumber = request.form["idnumber"]
        dateissued = request.form["dateissued"]
        country = request.form["country"]
        address = request.form["address"]
        email = request.form["email"]

        cursor.execute('INSERT INTO register VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)',(firstname, lastname, phonenumber, dateofbirth, middlename, idtype, idnumber, dateissued, country, address, email ))
        conn.commit()
        cursor.close()
        msg = f"Hello, {firstname}  {lastname}  {middlename} you have successfully registred your new sim card"
        #redirect url to facial for the next process
        return render_template('alert.html' , msg = msg)  
        
    
    return render_template('register.html')




#running the app and turning debug mode on
if __name__ == "__main__":
    app.run(debug =True)
