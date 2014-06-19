import urlparse, mechanize, StripHTML, HTMLParser
from pyparsing import *
from firebase import firebase


URL = "http://m.runpee.com"

def linkScrapeMech(url):
    urlparse.urlparse(url).hostname
    br = mechanize.Browser()
    movieLinks = []
    br.open(url)
    for i in br.links():
        if i.url.startswith("peeTime.php?return="):
            movieLinks.append(i.base_url + '/' + i.url);
    return movieLinks


def gather_data(links):
    br = mechanize.Browser()
    for link in links:
        br.open(link)
    data=[]; i=0;
    for link in links:
        i+=1
        buffer = "Link " + str(i) + " - " + str(link) + '\n'
        try:
            data.append(buffer + br.open(link).get_data())
        except:
            continue
    return data



def writeData(data, fname="Links.txt"):
    fout = open(fname,'w')
    if type(data) == list:
        for info in data:
            fout.write(info + "\n")
    else:
        fout.write(data + "\n")


def makeJSON(movie_data):
    peeTimes = movie_data[1:]
    peeTimesDict={}
    for i in range(len(peeTimes)/3):
        ptDict={}
        ptDict['When']=peeTimes[i*3+1]
        ptDict["Run"]=peeTimes[i*3+2]
        peeTimesDict[peeTimes[i*3]]=ptDict
    JSON={}
    JSON["name"] = movie_data[0]
    JSON["PeeTimes"] = peeTimesDict
    return JSON



def parseData(fin):
    # Stop Words
    movieTitleStop = Literal("Notes") # Safer
    movieTitleStopClean = Literal("    Notes")  # Cleaner

    # Types
    integer = Word(nums)
    NL = LineEnd().suppress()
    movieTitleHead = Combine(NL + Literal("PeeTimes for:"))
    peeTimeOutOf = Combine(integer + " " + Literal("of") + " " + integer)('peeNumber')

    # Lines
    movieTitleLine = (movieTitleHead.suppress() + SkipTo(movieTitleStopClean))('mTitle')
    peeTimeHead = (Literal("PeeTime").suppress() + peeTimeOutOf)('timeOfTime')     # ['PeeTime', '1 of 2']
    peeQue = Combine(integer + "  " + restOfLine)('peeQue') # SAFER
    peeQueClean = Combine(integer + SkipTo(" \n"))('peeQueClean')          # Kills ending space
    whenToGo = Combine(Literal("When to go:")+restOfLine) #SAFE
    whenToGoClean = (Literal("When to go:").suppress() + SkipTo(" \n"))('whenToGo') # Cleaner


    # Ignores

    # Parse Action
    record = movieTitleLine + OneOrMore(SkipTo(peeTimeHead).suppress() + peeTimeHead + peeQueClean + whenToGoClean)
    rec = record.searchString(fin)

    # Return a list of all the data to be written.
    try:
        json = makeJSON(rec[0])
        return json
    except:
        return



def firebase_connect():
    return firebase.FirebaseApplication('https://runpee-pebble.firebaseio.com/', None)

def firebase_get_movie_json(firebaseApp):
    names = firebaseApp.get('/movies',None)
    movies_json = []
    for movie in names:
        movies_json.append(firebaseApp.get('/movies', movie))
    return movies_json

def firebase_all_titles(movies_json):
    titles=[]
    for movie in movies_json:
        titles.append(movie['name'])
    return titles

def firebase_post_all(parsedJSONArray, allTitles):
    for movie in parsedJSONArray:
        if movie['name'] not in allTitles:
            print "Added " + movie['name']
            firebaseApp.post('/movies', movie)

def firebase_put_all(parsedJSONArray, allTitles):
    for movie in parsedJSONArray:
        if movie['name'] not in allTitles:
            print "Added " + movie['name']
            print movie
            firebaseApp.put('/movies', movie['name'].replace('.',''), movie)

def firebase_delete_all(firebaseApp):
    names = firebaseApp.get('/movies',None)
    for movie in names:
        firebaseApp.delete('/movies', movie)

if __name__=='__main__':
    SPLIT_STATEMENT = "\nSPLITTERSTATEMENT\n"
    ## Acquire Links and HTML data
    # links = linkScrapeMech(URL);
    # data = gather_data(links)
    # hp = HTMLParser.HTMLParser()
    # dataString = str(hp.unescape((SPLIT_STATEMENT).join(data)))
    #
    ## Write Data
    # writeData(dataString,'Data/RunPee/RunPee.html')
    # text = StripHTML.StripHTML('Data/RunPee/RunPee.html')
    # writeData(text, 'Data/RunPee/RunPeeData.txt')

    ## Acquire movie JSON
    parseArray = open('Data/RunPee/RunPeeData.txt', 'r').read().split(SPLIT_STATEMENT)
    parsedJSONArray = []
    for movie in parseArray:
        parsedJSONArray.append(parseData(movie))
    # fout = open('Data/RunPee/RunPeeDataParsed.txt', 'wb')
    # for movie_json in parsedJSONArray:
    #     fout.write(str(movie_json))
    #     fout.write(SPLIT_STATEMENT)

    ## Connect to firebase
    firebaseApp = firebase_connect()
    # firebaseApp.put('/movies', 'xmen', {'name':'movietitle'})


    ## Other Commands - If deleting all, must also use movies_json = {}

    # firebase_delete_all(firebaseApp)
    movies_json = firebase_get_movie_json(firebaseApp)
    # movies_json = {}
    titles = firebase_all_titles(movies_json)

    ## Post to Firebase -- Only posts movie titles not already there.
    # firebase_post_all(parsedJSONArray, titles)
    firebase_put_all(parsedJSONArray, titles)


    ## Reprint Test
    # movies_json2=firebase_get_movie_json(firebaseApp)
    # titles2=firebase_all_titles(movies_json2)
    # for title in titles2:
    #     print title

