import sqlite3

def build():
    database = sqlite3.connect("rest.db")
    c = database.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, points INTEGER, packs INTEGER, cards INTEGER, pfp TEXT, userID INTEGER PRIMARY KEY AUTOINCREMENT)")
    c.execute("CREATE TABLE IF NOT EXISTS cards(imgLink TEXT, advice TEXT, userID INTEGER, FOREIGN KEY (userID) REFERENCES users(userID))")
    #c.execute("CREATE TABLE IF NOT EXISTS used(advice BOOLEAN, insult BOOLEAN, image BOOLEAN, question BOOLEAN, propertyID TEXT)")

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
    matching = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
    if (len(matching) == 0): 
        c.execute("INSERT INTO users(username, password, points, packs, cards, pfp) VALUES(?, ?, ?, ?, ?, ?)", (username, password, 0, 0, 0, ""))
        close(db)
        return 0
    close(db)
    return 1

def incrementPack(ID):
    c,db = connect()
    print(c.execute("SELECT packs FROM users WHERE userID = ?", (ID,)).fetchall())
    numPacks = int(c.execute("SELECT packs FROM users WHERE userID = ?", (ID,)).fetchall()) + 1
    c.execute("UPDATE users SET packs=? WHERE userID = ?", (numPacks, ID))
    test = c.execute("SELECT packs FROM users WHERE userID = ?", (ID,)).fetchall()
    print("PACKS: " + test)
    close(db)

def addCard(img, advice, ID):
    c,db = connect()
    c.execute("INSERT INTO cards VALUES (?, ?, ?)", (img[1], advice, ID))
    numCards = c.execute("SELECT cards FROM users WHERE userID = ?", (ID,)).fetchall()
    c.execute("UPDATE users SET cards=? WHERE userID = ?", (numCards+1, ID))
    test = c.execute("SELECT cards FROM users WHERE userID = ?", (ID,)).fetchall()
    print("CARDS: " + test)
    close(db)

def showCards(ID):
    c,db = connect()
    collection = c.execute("SELECT imgLink, advice FROM cards WHERE userID = ?", (ID,)).fetchall()
    close(db)
    return collection

def addPoints(ID):
    c,db = connect()
    score = c.execute("SELECT points FROM users WHERE userID = ?", (ID,)).fetchall()
    c.execute("UPDATE users SET points=? WHERE userID = ?", (score+1, ID))
    test = c.execute("SELECT points FROM users WHERE userID = ?", (ID,)).fetchall()
    print("points: " + test)
    close(db)
    
def welcomeDisp(ID):
    c,db = connect()
    info = c.execute("SELECT points, packs, cards FROM users WHERE userID = ?", (ID,)).fetchall()
    close(db)
    info = info[0]
    return info[0], info[1], info[2]
    
def selectPFP(ID, pfpLink):
    c,db = connect()
    c.execute("UPDATE users SET pfp=? WHERE userID = ?", (pfpLink, ID))
    close(db)

# def checkUsed():
#     c,db = connect()
#     
#     close(db)


