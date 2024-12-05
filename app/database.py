import sqlite3

def build():
    database = sqlite3.connect("rest.db")
    c = database.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, points INTEGER, userID INTEGER PRIMARY KEY AUTOINCREMENT)")
    c.execute("CREATE TABLE IF NOT EXISTS cards(imgLink TEXT, advice BOOLEAN, insult BOOLEAN, quote TEXT, userID INTEGER, FOREIGN KEY (userID) REFERENCES users(userID))")
    c.execute("CREATE TABLE IF NOT EXISTS used(advice BOOLEAN, insult BOOLEAN, image BOOLEAN, question BOOLEAN, propertyID TEXT)")

    database.commit()
    database.close()

def connect():
    db = sqlite3.connect("rest.db")
    c = db.cursor()
    return c, db

def close(db):
    db.commit()
    db.close()
    
def auth(username):
    c,db = connect()
    info = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone() #Finds user's row based on the entered username
    close(db)
    return info

def createUser(username, password):
    c,db = connect()
    matching = c.execute("SELECT * FROM users WHERE username = ?", username[0]).fetchall()
    if (len(matching) == 0): 
        c.execute("INSERT INTO users(username, password, points) VALUES(?, ?, ?)", (username, password, 0))
        close(db)
        return 0
    close(db)
    return 1


print(auth("cookie"))







