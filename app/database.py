import sqlite3

db = "rest.db"

database = sqlite3.connect(db)
c = database.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, userID INTEGER PRIMARY KEY AUTOINCREMENT, points INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS cards(imgLink TEXT, advice BOOLEAN, insult BOOLEAN, quote TEXT, userID INTEGER, FOREIGN KEY (userID) REFERENCES users(userID))")
c.execute("CREATE TABLE IF NOT EXISTS used(advice BOOLEAN, insult BOOLEAN, img BOOLEAN, propertyID TEXT)")