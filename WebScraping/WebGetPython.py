## File: WebGetPython.py
## Author: Kevin Gleason
## Date: 5/30/14
## Use: Alternative to wget and curl in python
import urllib2

__author__ = 'Kevin Gleason'


def webManager():
    manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    uri = raw_input("URI: ")
    login = raw_input("Login: ")
    password = raw_input("Password: ")
    manager.add_password(None, uri, login, password)
    handler = urllib2.HTTPBasicAuthHandler(manager)
    return manager

def viewInfo(result):
    length = result.info()['Content-Length']
    print length
    print result.info()
    print result.read()



if __name__=='__main__':
    URL = raw_input("Input wget url: ")
    manager_needed = raw_input("Need web auth manager? (y/n) ")
    director = urllib2.OpenerDirector()
    if manager_needed.lower()=="y":
        manager = webManager()
        director.add_handler(manager)
    request = urllib2.Request(URL, headers = {'Accept' : 'application/xml'})
    result = director.open(request)
    result.read()
    #viewInfo(result)

