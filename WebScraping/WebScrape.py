## File: WebScrape.py
## Author: Kevin Gleason
## Date: 5/23/14
## Use: Scrape data from websites with mechanize and BeautifulSoup

import urllib, urlparse
import mechanize
import StripHTML
from bs4 import BeautifulSoup
import re

# Global Variables
URL = raw_input("Input URL to scrape: ")
THRESHOLD = int(raw_input("Input recursion depth of scrape: "))
# BASE_URL = raw_input("Input Base-URL of site: ")

  # Sample URLs
# URL = "http://www.theonion.com"
# URL = "http://kevinagleason.co.nf"

# Define functions
def checkList(url, list):
    if url not in list and urlparse.urlparse(url).hostname in url:
        return True
    return False

# Check if URL is js or other
def checkURL(url, IGNORE_WORDS):
    for ig in IGNORE_WORDS:
        if ig in url:
            return True
    return False

def writeData(data, fname="Links.txt"):
    fout = open(fname,'w')
    if type(data) == list:
        for info in data:
            fout.write(info + "\n")
    else:
        fout.write(data + "\n")

# Scrape data
def get_data(browser, links):
    data = []
    for link in links:
        data = browser.follow_link(link).get_data()

# Check the type of scrape occurring
def isURLinScrapeType(link, type, url=URL):
    if type=="all":
        return True
    elif type=="rel":
        if url in link:
            return True
    else:
        type = type.split(", ")
        for url in type:
            if url in link:
                return True
    return False


def filter_links(links, type="all", baseURL=URL):
    # All links branching from site
    if type=="all":
        return links
    # Base url only
    elif type=="rel":
        tmp = []
        for link in links:
            if baseURL in link:
                tmp.append(link)
        return tmp
    # List of base_urls allowed
    else:
        type = type.split(", ")
        tmp=[]
        for url in type:
            for link in links:
                if url in link:
                    tmp.append(link)
        return tmp


# Crawler functions
# Use Mechanize - not recommended
def linkScrapeMech(url):
    urlparse.urlparse(url).hostname
    br = mechanize.Browser()
    urls = [url]
    visited = [url]

    while len(urls) > 0:
        try:
            br.open(urls.pop(0))
            for link in br.links():
                newurl = urlparse.urljoin(link.base_url,link.url)
                host = urlparse.urlparse(newurl).hostname or ''
                path = urlparse.urlparse(newurl).path or ''
                newurl = "http://"+host+path

                if checkList(newurl, visited):
                    visited.append(newurl)
                    urls.append(newurl)
                    print newurl #uncomment to view crawl
        except:
           try:
               urls.pop(0)
           except:
               return visited
    return visited # Not needed

# Use BeautifulSoup
# THRESHOLD = 2 ## WHERE TO PUT THIS
def linkScrapeSoup(url, depth=0, type="all", base_url=URL):
    htmltext = urllib.urlopen(url)
    soup = BeautifulSoup(htmltext)
    visited=[url]
    for tag in soup.findAll('a',href=True):
        raw = tag['href']
        IGNORE_SYMBOLS = ["@", "()","..","(",")"]
        if not '.' in raw or checkURL(raw, IGNORE_SYMBOLS):
            continue

        host = urlparse.urlparse(raw).hostname or ''
        path = urlparse.urlparse(raw).path or ''

        # Make the new URL
        if host == "":
            if not path.startswith('/') and path != '':
                newurl = url + str('/'+path)
            else:
                newurl = base_url + str(path)
        else:
            print "Host: " + host
            newurl = "http://" + str(host) + str(path)
        print "  " + newurl

        # If url is not in the Scrape type scope, continue
        if not isURLinScrapeType(newurl, type):
            continue
        # Recursion depth allowed
        if depth + 1 < THRESHOLD:
            linkR = linkScrapeSoup(newurl, depth+1)

            for lnkR in linkR:
                if checkList(lnkR, visited):
                    visited.append(lnkR)

        if checkList(newurl, visited):
            print "  Added " + newurl
            visited.append(newurl)

    return visited

def scrape_data(fname, fout="Output.txt"):
    br = mechanize.Browser()
    links = [line.rstrip() for line in open(fname, 'r')]
    data=[]; i=0;
    for link in links:
        i+=1
        buffer = "Link " + str(i) + " - " + str(link) + '\n'
        try:
            data.append(buffer + br.open(link).get_data())
        except:
            continue
    return data

# Gather all link data
def gather_data(url=URL, type='rel', base_url=URL):
    links = linkScrapeMech(URL)
    # links = linkScrapeSoup(url, type=type, base_url=base_url)
    flinks = filter_links(links,type=type)
    return flinks

# Main loop
if __name__ == '__main__':
    # Name The File and Type
    fname = raw_input("Enter input-output file name: ")
    ctype = raw_input("Enter Crawl type (all, rel, base_urls): ")

    # Assign filenames
    fnameText = fname + ".txt";
    fnameHTML = fname + ".html"
    fnameData = fname + "Data.txt"

    # Gather the Data
    links = gather_data(type=ctype)
    writeData(links, "Data/" + fnameText)
    print "Links gathered. Wrote links to " + fnameText

    # Scrape the Data
    print "Scraping data from pages..."
    l = scrape_data('Data/' + fnameText)
    writeData(l, 'Data/' + fnameHTML)
    print "Process complete. HTML Data written to " + fnameData

    # Remove HTML tags
    print "Converting HTML to visible text..."
    text = StripHTML.StripHTML('Data/' + fnameHTML)
    writeData(text, 'Data/' + fnameData)