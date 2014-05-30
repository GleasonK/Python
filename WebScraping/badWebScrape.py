## File: WebScrape.py
## Author: Kevin Gleason
## Date: 5/23/14
## Use: Scrape data from websites with mechanize and BeautifulSoup

import mechanize, urllib2
from bs4 import BeautifulSoup

# Global Variables
# BASE_URL = "http://denturesohio.co.nf"
# ARTICLE_URL_PREFIX = "http://denturesohio.co.nf/The Practice"

BASE_URL = "http://www.packtpub.com/article-network"
ARTICLE_URL_PREFIX = 'http://www.packtpub.com/article/'

# Define functions for scraping
def scrape_links(base_url, data):
    """
    Scrape links pointing to article pages
    """
    soup = BeautifulSoup(data)

    # Create mechanize links to be used
    # later by mechanize.Browser instance
    links = [mechanize.Link(base_url = base_url,
            url = str(anchor['href']),
            text = str(anchor.string),
            tag = str(anchor.name),
            attrs = [(str(name), str(value))
        for name, value, _, _ in anchor.attrs])
        for anchor in unicode(soup.findAll("a")).encode("utf-8")]

    return links

# Get data out of the articles
def scrape_articles(data):
    soup = BeautifulSoup(data)
    articles = [{'title': str(anchor.string),
                 'url': str(anchor['href'])}
    for anchor in [li.a for li in soup.findAll('li')]
    if anchor['href'].startswith(ARTICLE_URL_PREFIX)]
    return articles

# Main function
def main():
    # Set up for parsing
    articles = []

    # Get links data
    br = mechanize.Browser()
    data = br.open(BASE_URL).get_data()
    links = scrape_links(BASE_URL, data)

    articles.extend(scrape_articles(data))

    # Scrape articles content
    for link in links:
        data = br.follow_link(link).get_data()
        scrape_articles(data)
        br.back()

    # Output si the list of titles and URLs for each article found:
    print "Article Network:\n"
    print "nn".join(['Title: "%(title)s"nURL: "%(URL)s"'% \
                     article for article in articles])



# Main structure
if __name__ == '__main__':
    main()

