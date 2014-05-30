__author__ = 'Kevin Gleason'

import numpy as nu
import pyparsing as pp

def allFxn(module):
    counter = 0
    for item in dir(module):
        if counter == 4:
            print item
            counter = 0
        else:
            print item + " ",
            counter += 1

def lamRec(x, y):
    if len(y(x))%3==0:
        print y(x)
        return x
    else:
        return lamRec(y(x), lambda y:y[:3])

print lamRec("HelloWorl", lambda y:y[1:])

