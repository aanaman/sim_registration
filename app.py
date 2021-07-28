from types import MethodDescriptorType
from flask import (Flask,redirect,render_template,request,session,url_for,jsonify) 
import json
import requests
from base64 import *



app = Flask(__name__)
        

@app.route('/')
def index():
    return render_template('home.html')



@app.route('/enrol', methods=['GET','POST']) 
def enrol():
    return render_template('enrol.html')



@app.route('/verify', methods=['GET', 'POST'])
def verify():
    return render_template('verify.html')



@app.route('/home', methods=['GET','POST'])
def home():
    return render_template('home.html')


@app.route('/facial', methods=['GET','POST'])
def facial():
    return render_template('facial.html')


if __name__ == "__main__":
    app.debug =True
    app.run() 