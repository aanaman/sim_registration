#importing python library
from flask import Flask, redirect, render_template, request, session, url_for


#initializing flask app
app = Flask(__name__)
        
#creating sql object
#mysql = MySQL(app)

#MySQL configuration



#seting my flask route
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/enrol/", methods=["GET","POST"]) 
def enrol():
    if request.method == "POST":
        req = request.form
        firstname = req["firstname"]
        lastname = req["lastname"]
        idnumber = req["idnumber"]
        idtype = req["idtype"]
        password = req["password"]
        confpassword = req["confpassword"]
        
        print(firstname,lastname,idnumber,idtype,password,confpassword)
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