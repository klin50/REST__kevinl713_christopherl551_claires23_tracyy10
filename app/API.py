# import requests
import urllib.request
from urllib.request import Request
from urllib.request import urlopen
import json
import random

# create a list containing an insult and the corresponding ID
def genInsult():
    url = "https://evilinsult.com/generate_insult.php?type=json"
    API = urllib.request.urlopen(url)
    python_ify = json.loads(API.read())
    return [python_ify['number'], python_ify['insult']]

# param : the insult-list
def getInsult(liSt):
    return liSt[1]

# param : the insult-list
def getInsultID(liSt):
    return liSt[0]

# create a list containing a piece of advice and the corresponding ID
def genAdvice():
    url = "https://api.adviceslip.com/advice"
    API = urllib.request.urlopen(url)
    python_ify = json.loads(API.read())['slip']
    return [python_ify['id'], python_ify['advice']]

# param : the advice-list
def getAdvice(liSt):
    return liSt[1]

# param : the advice-list
def getAdviceID(liSt):
    return liSt[0]

# create a list containing a RANDOM cat and the corresponding ID
def genCat():
    # url = "https://api.nekosia.cat/api/v1/images/catgirl"
    # API = urllib.request.urlopen(url)
    # return API
    url = "https://api.nekosia.cat/api/v1/images/catgirl"
    req = Request(url, headers={'User-Agent': 'Modzilla/5.0'}) # ---> nekosia is recognizing that we are not accessing through a browser
    API = urlopen(req).read() # ---> thus, we must modify our header to pass as a browser (Modzilla/5.0 token)
    python_ify = json.loads(API)
    #pretty = json.dumps(python_ify, indent=2)   # ---> converts to json to pretty print
    return [python_ify['id'], python_ify['image']['original']['url']]

# generate random 10
def genCat5():
    url = "https://api.nekosia.cat/api/v1/images/general?additionalTags=girl&count=5"
    req = Request(url, headers={'User-Agent': 'Modzilla/5.0'})
    API = urlopen(req).read()
    python_ify = json.loads(API)
    pretty = json.dumps(python_ify, indent=2)
    getTen = []
    i = 0
    while i < 5:
        getTen.append(python_ify['images'][i]['image']['original']['url'])
        i+=1
    return getTen

# swimwear
def genCatSwimwear():
    url = "https://api.nekosia.cat/api/v1/images/general?additionalTags=swimwear"
    req = Request(url, headers={'User-Agent': 'Modzilla/5.0'})
    API = urlopen(req).read()
    python_ify = json.loads(API)
    return [python_ify['id'], python_ify['image']['original']['url']]

# generate swimwear 10
def genCatSwimwear5():
    url = "https://api.nekosia.cat/api/v1/images/general?additionalTags=swimwear&count=5"
    req = Request(url, headers={'User-Agent': 'Modzilla/5.0'})
    API = urlopen(req).read()
    python_ify = json.loads(API)
    pretty = json.dumps(python_ify, indent=2)
    getTen = []
    i = 0
    while i < 5:
        getTen.append(python_ify['images'][i]['image']['original']['url'])
        i+=1
    return getTen

# maid
def genCatMaid():
    url = "https://api.nekosia.cat/api/v1/images/general?additionalTags=maid"
    req = Request(url, headers={'User-Agent': 'Modzilla/5.0'})
    API = urlopen(req).read()
    python_ify = json.loads(API)
    return [python_ify['id'], python_ify['image']['original']['url']]

# generate maid 10
def genCatMaid5():
    url = "https://api.nekosia.cat/api/v1/images/general?additionalTags=maid&count=5"
    req = Request(url, headers={'User-Agent': 'Modzilla/5.0'})
    API = urlopen(req).read()
    python_ify = json.loads(API)
    pretty = json.dumps(python_ify, indent=2)
    getTen = []
    i = 0
    while i < 5:
        getTen.append(python_ify['images'][i]['image']['original']['url'])
        i+=1
    return getTen

# vtuber
def genVtuber():
    url = "https://api.nekosia.cat/api/v1/images/general?additionalTags=vtuber"
    req = Request(url, headers={'User-Agent': 'Modzilla/5.0'})
    API = urlopen(req).read()
    python_ify = json.loads(API)
    return [python_ify['id'], python_ify['image']['original']['url']]

# generate vtuber 10
def genVtuber5():
    url = "https://api.nekosia.cat/api/v1/images/general?additionalTags=vtuber&count=5"
    req = Request(url, headers={'User-Agent': 'Modzilla/5.0'})
    API = urlopen(req).read()
    python_ify = json.loads(API)
    pretty = json.dumps(python_ify, indent=2)
    getTen = []
    i = 0
    while i < 5:
        getTen.append(python_ify['images'][i]['image']['original']['url'])
        i+=1
    return getTen

# param : the cat-list
def getCat(liSt):
    return liSt[1]

# param : the cat-list
def getCatID(liSt):
    return liSt[0]

# create a random trivia
def genTrivia():
    url = "https://the-trivia-api.com/v2/questions/?limit=1"
    API = urllib.request.urlopen(url)
    python_ify = json.loads(API.read())[0]
    answers=python_ify["incorrectAnswers"]
    answers.append(python_ify["correctAnswer"])
    random.shuffle(answers)
    return [python_ify['id'], python_ify['category'], python_ify["difficulty"], python_ify["question"]["text"], answers, python_ify["correctAnswer"]]

# specify difficulty
'''
    easy
    medium
    hard
'''
def genTriviaDifficulty(difficulty):
    if difficulty in ["easy", "medium", "hard"]:
        url = "https://the-trivia-api.com/v2/questions/?limit=1&difficulties="+difficulty
        API = urllib.request.urlopen(url)
        python_ify = json.loads(API.read())[0]
        answers=python_ify["incorrectAnswers"]
        answers.append(python_ify["correctAnswer"])
        return [python_ify['id'], python_ify['category'], python_ify["difficulty"], python_ify["question"]["text"], answers, python_ify["correctAnswer"]]
    else:
        return('''Error: only use "easy" "medium" "hard"
You inputted: '''+difficulty)

# specify category
'''
    music
    sport_and_leisure
    film_and_tv
    arts_and_literature
    history
    society_and_culture
    science
    geography
    food_and_drink
    general_knowledge
'''
def genTriviaCategory(cat):
    if cat in ["music", "sport_and_leisure", "film_and_tv", "arts_and_literature", "history", "society_and_culture", "science", "geography", "food_and_drink", "general_knowledge"]:
        url = "https://the-trivia-api.com/v2/questions/?limit=1&categories="+cat
        API = urllib.request.urlopen(url)
        python_ify = json.loads(API.read())[0]
        answers=python_ify["incorrectAnswers"]
        answers.append(python_ify["correctAnswer"])
        return [python_ify['id'], python_ify['category'], python_ify["difficulty"], python_ify["question"]["text"], answers, python_ify["correctAnswer"]]
    else:
        return('''Error: only use "music" "sport_and_leisure" "film_and_tv" "arts_and_literature" "history" "society_and_culture" "science" "geography" "food_and_drink" "general_knowledge"
You inputted: '''+cat)

# specify both difficulty and category
def genTriviaBoth(diff, cat):
    if cat in ["music", "sport_and_leisure", "film_and_tv", "arts_and_literature", "history", "society_and_culture", "science", "geography", "food_and_drink", "general_knowledge"] and diff in ["easy", "medium", "hard"]:
        url = "https://the-trivia-api.com/v2/questions/?limit=1&categories="+cat+"&difficulties="+diff
        API = urllib.request.urlopen(url)
        python_ify = json.loads(API.read())[0]
        answers=python_ify["incorrectAnswers"]
        answers.append(python_ify["correctAnswer"])
        return [python_ify['id'], python_ify['category'], python_ify["difficulty"], python_ify["question"]["text"], answers, python_ify["correctAnswer"]]
    else:
        return('''Error: You inputted: '''+diff +", "+cat)

# param : the trivia-list
def getQuestion(liSt):
    return liSt[3]

# param : the trivia-list
def getTriviaID(liSt):
    return liSt[0]

# param : the trivia-list
def getCategory(liSt):
    return liSt[1]

# param : the trivia-list
def getDifficulty(liSt):
    return liSt[2]

# shuffled list of answer choices
def getAnswers(liSt):
    random.shuffle(liSt[4])
    return liSt[4]

# returns correct answer
def getCorrectAnswer(liSt):
    return liSt[5]

# checks if answ is correct
def isCorrect(liSt, answ):
    if liSt[5] == answ:
        return True
    return False
