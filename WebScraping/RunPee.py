import urlparse, mechanize, StripHTML
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
            # newurl = "http://"+host+path
            # movieLinks.append(newurl)
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
    string = "lol PeeTimes for:  Blended    Notes about these Peetimes:  I would recommend the 1st Peetime. it doesn&#39;t have any plot or character development and if you don&#39;t make it back in the allotted time you still won&#39;t miss anything important.  PeeTime 1 of 2  41  minutes into movie =  4  minute Peetime"
    string2 = "PeeTime 1 of 2"

    # Stop Words
    movieTitleStop = Literal("    Notes")
    peeTimeStop = Literal("end credits?")


    # Types
    integer = Word(nums)
    NL = LineEnd().suppress()
    movieTitleHead = Combine(NL + Literal("PeeTimes for:"))
    # movieTitle = OneOrMore(~movieTitleStop + Word(alphanums))
    # movieTitleStop.setParseAction(replaceWith(""))
    peeTimeOutOf = Combine(integer + " " + Literal("of") + " " + integer)('peeNumber')


    peeQue = Combine(integer + "  " + restOfLine)('peeQue') # SAFER
    peeQueClean = Combine(integer + SkipTo(" \n"))          # Kills ending space

    whenToGo = Combine(Literal("When to go:")+restOfLine) #SAFE
    whenToGoClean = Literal("When to go:").suppress() + SkipTo(" \n") # Cleaner

    PQWhenToGo = peeQueClean + whenToGo

    peeTimeHead = Literal("PeeTime").suppress() + peeTimeOutOf     # ['PeeTime', '1 of 2']

    # Will catch [['PeeTime 1 of 2']]
    peeTimez = Combine(Word(alphanums) + " " + peeTimeOutOf)('comb') # + Literal("of") + integer)

    movieTitleLine = (movieTitleHead.suppress() + SkipTo(movieTitleStop))('mTitle')
    # Open Data

    # Test
    # sample = Group(movieTitleLine + OneOrMore(SkipTo(peeTimeHead).suppress() + peeTimeHead + peeQueClean))
    # test = movieTitleLine.searchString(fin)
    # test2 = sample.searchString(fin)
    # print "TEST" + str(test)
    # print "Test2" + str(test2)

    # Lines
    # peeTitle = Combine(movieTitleHead + movieTitle + movieTitleStop)
    peeTime = Combine(peeTimeHead + integer + Literal("of") + integer + restOfLine + NL)


    # Ignores

    # Parse Action
    record = movieTitleLine + OneOrMore(SkipTo(peeTimeHead).suppress() + peeTimeHead + peeQueClean + whenToGoClean)
    # recd = record.searchString(fin)
    # records = OneOrMore(record).searchString(fin)
    # print recd
    # print records
    rec = record.searchString(fin)
    print rec
    # for lst in rec:
    #     for i in lst:
    #         print i

    # Return a list of all the data to be written.
    try:
        return rec[0]
    except:
        return


if __name__=='__main__':
    SPLIT_STATEMENT = "\nSPLITTERSTATEMENT\n"
    links = linkScrapeMech(URL);
    data = gather_data(links)
    dataString = (SPLIT_STATEMENT).join(data)

    writeData(dataString,'Data/RunPee/RunPeehtml')

    text = StripHTML.StripHTML('Data/RunPee/RunPee.html')
    writeData(text, 'Data/RunPee/RunPeeData.txt')

    parseArray = open('Data/RunPee/RunPeeData.txt', 'r').read().split(SPLIT_STATEMENT)
    parsedArray = []
    for movie in parseArray:
        parsedArray.append(parseData(movie))
    for i in parsedArray:
        print "Movie", i
    # parseData('Data/RunPeeData.txt')
