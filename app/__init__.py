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

@app.route("/")
def home():
    return render_template("home.html", x = "weeee")
def login():
    return render_template("login.html", x = "weeee")
def register():
    return render_template("register.html", x = "weeee")
def selectD():
    return render_template("selectD.html", x = "weeee")
def question():
    return render_template("question.html", x = "weeee")
def gacha():
    return render_template("gacha.html", x = "weeee")
def collection():
    return render_template("collection.html", x = "weeee")
def logout():
    return redirect(url_for("/"))

if __name__ == "__main__":
    app.debug = True
    app.run()