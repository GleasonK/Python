import urlparse, mechanize, StripHTML, HTMLParser
from pyparsing import *

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
    peeTimeHead = Literal("PeeTime").suppress() + peeTimeOutOf     # ['PeeTime', '1 of 2']
    peeQue = Combine(integer + "  " + restOfLine)('peeQue') # SAFER
    peeQueClean = Combine(integer + SkipTo(" \n"))          # Kills ending space
    whenToGo = Combine(Literal("When to go:")+restOfLine) #SAFE
    whenToGoClean = Literal("When to go:").suppress() + SkipTo(" \n") # Cleaner


    # Ignores

    # Parse Action
    record = movieTitleLine + OneOrMore(SkipTo(peeTimeHead).suppress() + peeTimeHead + peeQueClean + whenToGoClean)
    rec = record.searchString(fin)

    # Return a list of all the data to be written.
    try:
        return rec[0]
    except:
        return


if __name__=='__main__':
    SPLIT_STATEMENT = "\nSPLITTERSTATEMENT\n"
    links = linkScrapeMech(URL);
    data = gather_data(links)
    hp = HTMLParser.HTMLParser()
    dataString = str(hp.unescape((SPLIT_STATEMENT).join(data)))

    writeData(dataString,'Data/RunPee/RunPee.html')

    text = StripHTML.StripHTML('Data/RunPee/RunPee.html')
    writeData(text, 'Data/RunPee/RunPeeData.txt')

    parseArray = open('Data/RunPee/RunPeeData.txt', 'r').read().split(SPLIT_STATEMENT)
    parsedArray = []
    for movie in parseArray:
        parsedArray.append(parseData(movie))
    fout = open('Data/RunPee/RunPeeDataParsed.txt', 'w')
    for movie in parsedArray:
        print "Movie", movie
        for item in movie:
            fout.write(item+", ")
        fout.write("\n")
    # parseData('Data/RunPeeData.txt')
