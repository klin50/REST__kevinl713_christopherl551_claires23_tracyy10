import os
from flask import Flask, render_template, request, session, redirect
import sqlite3
import csv
import urllib.request
import json
import requests

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret
'''
@app.route("/")
def home():
    if 'username' in session: #Checks if logged in
        logged = True
        uname = session['username']  #Displays username
        logged = False
    return render_template("home.html",logged=logged,uname=uname)
@app.route("/login")
def disp_loginpage():
    return render_template('login.html') #Login Page Rendering

@app.route("/auth", methods=['POST'])
def authenticate():#Is called when the user tries to log into their account
    username = request.form.get('username')
    password = request.form.get('password')
    stored_password = getPass(username)
    if stored_password and stored_password[0] == password:
        session['username'] = username
        return redirect("/")
    return render_template('login.html', error="Invalid username or password")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return
'''
@app.route("/")
def nasa():
    request = requests.get("https://api.nekosia.cat/api/v1/images/catgirl/").json()
    print(request['image'])
    return render_template("gacha.html",img1 = request['image']['original']['url'])

if __name__ == "__main__":
    app.debug = True
    app.run()
