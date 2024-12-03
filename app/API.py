# import requests
import urllib.request
from urllib.request import Request
from urllib.request import urlopen
import json

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

# create a list containing a cat and the corresponding ID
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

# param : the cat-list
def getCat(liSt): 
    return liSt[1]

# param : the cat-list
def getCatID(liSt):
    return liSt[0]

