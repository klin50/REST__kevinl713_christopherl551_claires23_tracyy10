import os
from build_db import *
from flask import Flask, render_template, request, session, redirect
import sqlite3   
import csv       

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

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
    return render_template('logout.html')#Similar to login page, just removes session

if __name__ == "__main__":
    app.debug = True
    app.run()
