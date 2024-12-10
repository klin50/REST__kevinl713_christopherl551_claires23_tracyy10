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
        return redirect("/welcome")
    return render_template("home.html")

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
            session['userID'] = info[6] #Based on userID in database
            #print(info)
            #print(info[3])
            #print(session['userID'])
            #print("Both")
            return redirect("/welcome")
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

# what is this func????
''' 
@app.route("/checkcorrect",methods=['GET','POST'])
def auth(): # what in the world is this func??
    question = request.form.get('question')
    answer = request.form.get('answer')
    info = database.auth(answer)
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
        return redirect("/incorrect")
    flash("Error")
    return redirect("/question")
'''

@app.route("/selection", methods=['GET','POST'])
def selectD():
    if request.method == "GET":
        return render_template("selectD.html")
    elif request.method == "POST":
        qType = request.form.get("genre")
        trivia = "ugh"
        if qType == "none":
            trivia = API.genTrivia()
        elif qType in ["easy", "medium", "hard"]:
            trivia = API.genTriviaDifficulty(qType)
        elif qType in ["music", "sport_and_leisure", "film_and_tv", "arts_and_literature", "history", "society_and_culture", "science", "geography", "food_and_drink", "general_knowledge"]:
            trivia = API.genTriviaCategory(qType)
        question = API.getQuestion(trivia)
        ID = API.getTriviaID(trivia)
        category = API.getCategory(trivia)
        difficulty = API.getDifficulty(trivia)
        bg = "ugh"
        if difficulty == "easy":
            bg = "white"
        elif difficulty == "medium":
            bg = "orange-300"
        else:
            bg = "red-400"
        answers = API.getAnswers(trivia)
        correctA = API.getCorrectAnswer(trivia)
        iTC = []
        for i in answers:
            if i == correctA:
                iTC.append("correct")
            else:
                iTC.append("incorrect")
        return render_template("question.html", isThisCorrect = iTC, A = answers, bgColor = bg, D = difficulty, C = category, Q = question)
    else:
        return render_template("questions.html") # wont happen

@app.route("/answer", methods=['GET','POST'])
def retAnswer():
    if request.method == "POST":
        result = request.form.get("ans")
        bg = "ugh"
        insult = "ugh"
        quote = "ugh"
        ID = "ugh"
        if result == "correct":
            bg = "emerald-200"
            database.addPoints(session['userID'])
        else:
            bg = "red-400"
            insult = API.genInsult()
            quote = API.getInsult(insult)
            ID = API.getInsultID(insult)
        # now give points etc, etc
        return render_template("answer.html", R = result, I = quote, bgColor = bg, x = request.form.get("ans"))
    return redirect("/")

@app.route("/gacha", methods=['GET','POST'])
def gacha():
    cat = API.genCat()
    slip = API.genAdvice()
    advice = API.getAdvice(slip)
    #database.checkUsed()
    database.incrementPack(session['userID'])
    for i in range(3):
        database.addCard(cat, advice, session['userID'])
        
    return render_template("gacha.html", img1 = API.getCat(cat), x = request.form.get("isThisCorrect"))

@app.route("/collection")
def collection():
    cards = database.showCards(session['userID'])
    return render_template("collection.html", collection = cards)

@app.route("/welcome")
def welcome():
    points, packs, cards = database.welcomeDisp(session['userID'])
    return render_template("welcome.html", points=points, packs=packs, cards=cards)

@app.route("/logout")
def logout():
    session.pop('username', None)
    #flash()#Flash a logout message here
    return redirect('/')#Similar to login page, just removes session

if __name__ == "__main__":
    app.debug = True
    app.run()
