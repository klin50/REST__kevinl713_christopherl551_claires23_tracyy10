# necessary libraries
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
import os
import sqlite3
# ---
import API
import database

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

database.build()

def connect():
    db = sqlite3.connect("rest.db")
    c = db.cursor()
    return c, db

def close():
    db.commit()
    db.close()

@app.route("/")
def home():
    if 'username' in session: #Checks if logged in
        logged = True
        uname = session['username']  #Displays username
        return render_template("home.html",logged=logged,uname=uname)
    logged = False
    return render_template("home.html",logged=logged)

@app.route("/login")
def disp_loginpage():
    return render_template('login.html') #Login Page Rendering

@app.route("/auth", methods=['POST'])
def authenticate():#Is called when the user enters their username & password into the form
    username = request.form.get('username')
    password = request.form.get('password')
    c, restdb = connect()
    info = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone() #Finds user's row based on the entered username
    restdb.close()
    stored_password = info[1] #Gets user's password from database
    if stored_password and stored_password[0] == password: #If password is correct
        session['username'] = username
        session['userID'] = info[3] #Based on userID in database
        return redirect("/")
    return render_template('login.html', error="Invalid username or password")

@app.route("/createAccount")
def disp_register(): #Register Page Rendering
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def register(): #Is called when user enters their username and password into the form
    username = request.form.get('username')
    password = request.form.get('password')
    c, restdb = connect()
    c.execute("INSERT INTO users(username, password, points) VALUES(?, ?, ?)", (username, password, 0))
    restdb.close()
    return redirect("/login")

def selectD():
    return render_template("selectD.html", x = "weeee")
def question():
    return render_template("question.html", x = "weeee")
def gacha():
    return render_template("gacha.html", x = "weeee")
def collection():
    c, restdb = connect()
    c.execute("SELECT * FROM cards WHERE userID = ?", session['userID'])
    restdb.close()
    return render_template("collection.html", x = "weeee")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('logout.html')#Similar to login page, just removes session

if __name__ == "__main__":
    app.debug = True
    app.run()