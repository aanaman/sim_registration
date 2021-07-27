from flask import (Flask,redirect,render_template,request,session,url_for,jsonify) 
import json
import requests
from base64 import *



app = Flask(__name__)
        
 
@app.route('/')
def index():
    return redirect(url_for('login'))

def validation_post_data(data_object):
    if ("username" in data_object and "image" in data_object):
        return True
    else:
        return False

def get_base64(files):
    if len(files) > 0:
        b64file = b64encode(files['image'].read()).decode("utf-8")
        return b64file
    return ""
    
@app.route('/index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        api_key = 'T_72876c28-a773-4ac8-b650-4b0d27a6489b'
        headers = {'x-authorization': 'Basic edwardakorlie73@gmail.com:{api_key}'.format(api_key= api_key),'Content-Type': 'application/json'}
        data = request.form
        print(data)
        print(request.files)
        b64file = get_base64(request.files)
        payload = {"gallery":"tsatsu_bd","identifier":data["username"],"image":b64file}
        print(headers)
        r = requests.post('https://api.bacegroup.com/v2/verify', headers=headers, data=json.dumps(payload))
        print(r.json())
    return render_template('index.html')



@app.route("/verify", methods=["GET", "POST"])
def signup():
    if request.method =="POST":
        api_key = 'T_72876c28-a773-4ac8-b650-4b0d27a6489b'
        headers = {'x-authorization': 'Basic edwardakorlie73@gmail.com:{api_key}'.format(api_key= api_key),'Content-Type': 'application/json'}
        data = request.form
        print(data)
        print(request.files)
        b64file = get_base64(request.files)
        payload = {"gallery":"tsatsu_bd","identifier":data["username"],"image":b64file}
        print(headers)
        r = requests.post('https://api.bacegroup.com/v2/enroll', headers=headers, data=json.dumps(payload))

        print(r.text)
    return render_template("signup.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("profile.html")



if __name__ == "__main__":
    app.debug =True
    app.run() 