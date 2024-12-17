# necessary libraries
import os
import sqlite3
import random
# ---
from flask import Flask,render_template
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
# ---
import API
import database

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

database.build()#This runs twice

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
            return redirect("/welcome")
        flash("Incorrect password")
        return redirect("/login")
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
    if not 'username' in session:
        flash("Log in to continue!")
        return redirect("/login")
    if request.method == "GET":
        return render_template("selectD.html",pfp=database.getPFP(session['userID']),points=database.getPoints(session['userID']))
    elif request.method == "POST":
        qType = request.form.get("genre")
        trivia = "ugh"
        if qType == "none":
            trivia = API.genTrivia()
        elif qType in ["easy", "medium", "hard"]:
            trivia = API.genTriviaDifficulty(qType)
        elif qType in ["music", "sport_and_leisure", "film_and_tv", "arts_and_literature", "history", "society_and_culture", "science", "geography", "food_and_drink", "general_knowledge"]:
            trivia = API.genTriviaCategory(qType)
        ID = API.getTriviaID(trivia)
        question = API.getQuestion(trivia)
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
        return render_template("question.html", pfp=database.getPFP(session['userID']),points=database.getPoints(session['userID']), isThisCorrect = iTC, A = answers, bgColor = bg, D = difficulty, C = category, Q = question)
    else:
        return render_template("questions.html") # wont happen

@app.route("/answer", methods=['GET','POST'])
def retAnswer():
    if not 'username' in session:
        flash("Log in to continue!")
        return redirect("/login")
    if request.method == "POST":
        result = request.form.get("ans")
        diff = request.form.get("difficulty")
        bg = "ugh"
        insult = "ugh"
        quote = "ugh"
        ID = "ugh"
        if result == "correct":
            bg = "emerald-200"
            if diff == "easy":
                database.addPoints(session['userID'], 1)
            elif diff == "medium":
                database.addPoints(session['userID'], 2)
            else:
                database.addPoints(session['userID'], 3)
        else:
            bg = "red-400"
            insult = API.genInsult()
            quote = API.getInsult(insult)
            ID = API.getInsultID(insult)
        return render_template("answer.html", pfp=database.getPFP(session['userID']),points=database.getPoints(session['userID']), R = result, I = quote, bgColor = bg, x = request.form.get("ans"))
    return redirect("/")

def addPack(cards):
    database.incrementPack(session['userID'])
    for i in cards:
        database.addCard(i, API.getAdvice(API.genAdvice()), session['userID'])

@app.route("/gacha", methods=['GET','POST'])
def gacha():
    if not 'username' in session:
        flash("Log in to continue!")
        return redirect("/login")
    points = database.getPoints(session['userID'])
    if request.method == "GET":
        return render_template("gacha.html",cards=[], pfp=database.getPFP(session['userID']), points=points)
    else:
        action = request.form.get("action")
        if action[0] == "R":
            if action == "R1":
                if points < 10:
                    flash("INSUFFICIENT POINTS")
                    return redirect("/")
                else:
                    P0 = [API.getCat(API.genCat())]
                    addPack(P0)
                    database.removePoints(session['userID'],10)
            if action == "R5":
                if points < 45:
                    flash("INSUFFICIENT POINTS")
                    return redirect("/")
                else:
                    P0 = API.genCat5()
                    addPack(P0)
                    database.removePoints(session['userID'],45)
        if action[-1] == "1":
            if points < 15:
                flash("INSUFFICIENT POINTS")
                return redirect("/")
            elif action == "SW1":
                P0 = [API.getCat(API.genCatSwimwear())]
                addPack(P0)
                database.removePoints(session['userID'],15)
            elif action == "M1":
                P0 = [API.getCat(API.genCatMaid())]
                addPack(P0)
                database.removePoints(session['userID'],15)
            elif action == "VT1":
                P0 = [API.getCat(API.genVtuber())]
                addPack(P0)
                database.removePoints(session['userID'],15)
        if action[-1] == "5":
            if points < 70:
                flash("INSUFFICIENT POINTS")
                return redirect("/")
            elif action == "SW5":
                P0 = API.genCatSwimwear5()
                addPack(P0)
                database.removePoints(session['userID'],70)
            elif action == "M5":
                P0 = API.genCatMaid5()
                addPack(P0)
                database.removePoints(session['userID'],70)
            elif action == "VT5":
                P0 = API.genVtuber5()
                addPack(P0)
                database.removePoints(session['userID'],70)
        return render_template("gacha.html",cards=P0 ,pfp=database.getPFP(session['userID']), points=points)

@app.route("/collection")
def collection():
    if not 'username' in session:
        flash("Log in to continue!")
        return redirect("/login")
    cards = database.showCards(session['userID'])
    emptiness = False
    if(len(cards) == 0):
        emptiness = True
    return render_template("collection.html",pfp=database.getPFP(session['userID']),points=database.getPoints(session['userID']), collection = cards, empty = emptiness)

@app.route("/welcome")
def welcome():
    if not 'username' in session:
        flash("Log in to continue!")
        return redirect("/login")
    points, packs, cards = database.welcomeDisp(session['userID'])
    #print(points, packs, cards)
    top = database.leaderboard()
    #print(top)
    topPoints = top[0][0:3]
    topPacks = top[1][0:3]
    topCards = top[2][0:3]
    #print(topPoints)
    #print(topPacks)
    #print(topCards)
    #print(database.getPFP(session['userID']))
    return render_template("welcome.html",pfp=database.getPFP(session['userID']),user=session['username'], points=points, packs=packs, cards=cards, PE=topPoints, C=topCards, O=topPacks)

@app.route("/profile", methods=['GET','POST'])
def profile():
    if not 'username' in session:
        flash("Log in to continue!")
        return redirect("/login")
    #print(request.form.get("profile"))
    if request.form.get("profile") != None:
        database.selectPFP(session['userID'],request.form.get("profile"))
    return redirect("/collection")

@app.route("/logout")
def logout():
    session.pop('username', None)
    #flash()#Flash a logout message here
    return redirect('/')#Similar to login page, just removes session

if __name__ == "__main__":
    app.debug = True
    app.run()
