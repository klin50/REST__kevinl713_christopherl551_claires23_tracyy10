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
import random
# ---
import API
import database

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

database.build()

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

@app.route("/auth", methods=['GET', 'POST'])
def authenticate():#Is called when the user enters their username & password into the form
    username = request.form.get('username')
    password = request.form.get('password')
    info = database.auth(username)
    if info != None:
        stored_password = info[1] #Gets user's password from database
        if stored_password == password: #If password is correct
            session['username'] = username
            session['userID'] = info[3] #Based on userID in database
            #print(info)
            #print(info[3])
            #print(session['userID'])
            #print("Both")
            return redirect("/")
        #print("PW")
        flash("Invalid password")
        return redirect("/login")
    #print("User")
    flash("Invalid username")
    return redirect("/login")

@app.route("/createAccount")
def disp_register(): #Register Page Rendering
    return render_template('register.html')

@app.route("/register", methods=['GET', 'POST'])
def register(): #Is called when user enters their username and password into the form
    username = request.form.get('username')
    password = request.form.get('password')
    if (database.createUser(username, password) == 0):
        return redirect("/login")
    else:
        flash("Username already exists")
        return redirect("/createAccount")

@app.route("/selection", methods=['GET','POST'])
def selectD():
    difficulty = request.form.get('difficulty')
    topic = request.form.get('topic')
    if (API.genTriviaDifficulty('topic')):
        return redirect("/question")#Needs to be modified for both topic and difficulty combined
    return render_template("selectD.html", x = "weeee")

@app.route("/question", methods=['GET','POST'])
def question():
    set = []
    trivia = API.genTrivia()
    return render_template("question.html", trivia=trivia)

@app.route("/gacha", methods=['GET','POST'])
def gacha():
    cat = API.genCat()
    slip = API.genAdvice()
    advice = API.getAdvice(slip)
    #database.checkUsed()
    print(session['userID'])
    database.addCard(cat, advice, session['userID'])
    return render_template("gacha.html", img1 = API.getCat(cat))

@app.route("/collection")
def collection():
    cards = database.showCards(session['userID'])
    return render_template("collection.html", collection = cards)

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    #flash()#Flash a logout message here
    return redirect('/')#Similar to login page, just removes session

if __name__ == "__main__":
    app.debug = True
    app.run()
