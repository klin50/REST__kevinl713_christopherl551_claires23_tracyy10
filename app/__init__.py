# necessary libraries
from flask import Flask
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
    return render_template("home.html", x = "weeee")
def login():
    return render_template("login.html", x = "weeee")
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
        info = c.execute("SELECT * FROM users WHERE username = ?", username).fetchone()
        session['userID'] = info['userID']
        return redirect("/")
    return render_template('login.html', error="Invalid username or password")

@app.route("/createAccount")
def disp_register():
    return render_template('register.html')

@app.route("/register", methods=['POST'])

def register():
    username = request.form.get('username')
    password = request.form.get('password')
    c.execute("INSERT INTO users VALUES(?, ?, ?)", (username, password, 0))
    return render_template("register.html")

def selectD():
    return render_template("selectD.html", x = "weeee")
def question():
    return render_template("question.html", x = "weeee")
def gacha():
    return render_template("gacha.html", x = "weeee")
def collection():
    c.execute("SELECT * FROM cards WHERE userID = ?", session['userID'])
    return render_template("collection.html", x = "weeee")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('logout.html')#Similar to login page, just removes session

if __name__ == "__main__":
    app.debug = True
    app.run()
