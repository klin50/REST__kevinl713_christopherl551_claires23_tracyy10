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
            return redirect("/welcome")
        flash("Invalid password")
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
        # now give points etc, etc
        return render_template("answer.html", R = result, I = quote, bgColor = bg, x = request.form.get("ans"))
    return redirect("/")

@app.route("/gacha", methods=['GET','POST'])
def gacha():
    # points = database.getPoints(session['userID']))
    points = database.getPoints("3")
    R1C = API.getCat(API.genCat()) # generate cover image of Random Pack
    SW1C = API.getCat(API.genCatSwimwear()) # generate cover image of Swimwear Pack
    M1C = API.getCat(API.genCatMaid()) # generate cover image of Random Pack
    VT1C = API.getCat(API.genVtuber()) # generate cover image of Random Pack
    if request.method == "GET":
        return render_template("gacha.html", P = points, r1c = R1C, sw1c = SW1C, m1c = M1C, vt1c = VT1C)
    else:
        action = request.form.get("action")
        P0 = P1 = P2 = P3 = P4 = P5 = P6 = P7 = P8 = P9 = "DNE"
        if action == "R1":
            # remove 10 points
            img = API.genCat()
            # store img ID --- or don't, are we allowing duplicate cards? if we do, then we should allow them to show off their 'top 10' cards from their collection for others to see when they click onto their profile
            P0 = API.getCat(img)
        elif action == "R10":
            # remove 90 points
            imgL = API.genCat10()
            # store img IDs
            P0 = API.getCat(imgL[0])
            P1 = API.getCat(imgL[1])
            P2 = API.getCat(imgL[2])
            P3 = API.getCat(imgL[3])
            P4 = API.getCat(imgL[4])
            P5 = API.getCat(imgL[5])
            P6 = API.getCat(imgL[6])
            P7 = API.getCat(imgL[7])
            P8 = API.getCat(imgL[8])
            P9 = API.getCat(imgL[9])
        elif action == "SW1":
            # remove 15 points
            img = API.genCatSwimwear()
            # store img ID
            P0 = API.getCat(img)
        elif action == "SW10":
            # remove 135 points
            imgL = API.genCatSwimwear10()
            # store img IDs
            P0 = API.getCat(imgL[0])
            P1 = API.getCat(imgL[1])
            P2 = API.getCat(imgL[2])
            P3 = API.getCat(imgL[3])
            P4 = API.getCat(imgL[4])
            P5 = API.getCat(imgL[5])
            P6 = API.getCat(imgL[6])
            P7 = API.getCat(imgL[7])
            P8 = API.getCat(imgL[8])
            P9 = API.getCat(imgL[9])
        elif action == "M1":
            # remove 15 points
            img = API.genCatMaid()
            # store img ID
            P0 = API.getCat(img)
        elif action == "M10":
            # remove 135 points
            imgL = API.genCatMaid10()
            # store img IDs
            P0 = API.getCat(imgL[0])
            P1 = API.getCat(imgL[1])
            P2 = API.getCat(imgL[2])
            P3 = API.getCat(imgL[3])
            P4 = API.getCat(imgL[4])
            P5 = API.getCat(imgL[5])
            P6 = API.getCat(imgL[6])
            P7 = API.getCat(imgL[7])
            P8 = API.getCat(imgL[8])
            P9 = API.getCat(imgL[9])
        elif action == "VT1":
            # remove 15 points
            img = API.genVtuber()
            # store img ID
            P0 = API.getCat(img)
        elif action == "VT10":
            # remove 135 points
            imgL = API.genVtuber10()
            # store img IDs
            P0 = API.getCat(imgL[0])
            P1 = API.getCat(imgL[1])
            P2 = API.getCat(imgL[2])
            P3 = API.getCat(imgL[3])
            P4 = API.getCat(imgL[4])
            P5 = API.getCat(imgL[5])
            P6 = API.getCat(imgL[6])
            P7 = API.getCat(imgL[7])
            P8 = API.getCat(imgL[8])
            P9 = API.getCat(imgL[9])
        return render_template("gacha.html", p0 = P0, p1 = P1, p2 = P2, p3 = P3, p4 = P4, p5 = P5, p6 = P6, p7 = P7, p8 = P8, p9 = P9, P = points, r1c = R1C, sw1c = SW1C, m1c = M1C, vt1c = VT1C)

@app.route("/collection")
def collection():
    cards = database.showCards(session['userID'])
    emptiness = False
    if(len(cards) == 0):
        emptiness = True
    return render_template("collection.html", collection = cards, empty = emptiness)

@app.route("/welcome")
def welcome():
    points, packs, cards = database.welcomeDisp(session['userID'])
    top = database.leaderboard()
    #print(top)
    topPoints = top[0][0:3]
    topPacks = top[1][0:3]
    topCards = top[2][0:3]
    #print(topPoints)
    #print(topPacks)
    #print(topCards)
    return render_template("welcome.html", points=points, packs=packs, cards=cards, PE=topPoints, C=topCards, O=topPacks)

@app.route("/logout")
def logout():
    session.pop('username', None)
    #flash()#Flash a logout message here
    return redirect('/')#Similar to login page, just removes session

if __name__ == "__main__":
    app.debug = True
    app.run()
