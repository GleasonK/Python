## File: timeOut.py
## Date: 5/27/14
## Use: Run a python script for certain time then cut out
__author__ = 'Kevin Gleason'

import multiprocessing
import time

def printerFunction(word, n):
    for i in range(int(10*float(n))):
        print str(i), word
        time.sleep(1)

def timeOutFxn(fxn, fxnArgs, timeLimit):
    # Start the process
    p = multiprocessing.Process(target=fxn, name="printer", args=(x for x in fxnArgs))
    p.start()

    # Time Limit
      # time.sleep(timeLimit)

    # Terminate function process and cleanup if alive
      # p.join([timeout in seconds])
    p.join(timeLimit)
    if p.is_alive():
        print "Terminated process"
        p.terminate()
        p.join()

if __name__ == '__main__':
    timeOutFxn(printerFunction, ["HelloWorld", 1], 11)
    printerFunction("hi",0.5)