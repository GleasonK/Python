## File: uBigData.py
## Author: Kevin Gleason
## Date: 5/22/14
## Use: Sample analysis of an unstructured big data set

from pyparsing import LineEnd, oneOf, Word, nums, Combine, restOfLine, \
    alphanums, OneOrMore, alphas, Group, printables, MatchFirst, Or

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## Open file and return input/output
def fOpen(file, type, fout):
    fin = open(file, type)
    data = fin.read()
    fin.close()
    wfile = open(fout, 'w')
    return data, wfile

#Set the standards that will be used later
def setStds():
    NL = LineEnd().suppress()
    integer = Word(nums)       # Define what integer is
    AmPm = oneOf('AM PM')
    date = Combine(integer + '/' + integer + '/' + integer)
    time = Combine(integer + ':' + integer + ':' + integer + " " + AmPm)
    return NL, date, time

# Define how the record will look
def setLines(NL, date , time):
    level = oneOf("Information Warning")('lvl')
    date_line = date('eDate')
    time_line = time('eTime')
    source = Or(OneOrMore(Word(alphas + '-' + " "))|Word(alphanums))
    eventID = Word(nums)('eID')
    taskCat = Word(alphanums)('tCat')
    info = Combine(Word(printables) + restOfLine)('info') + NL
    return level, date_line, time_line, source, eventID, taskCat, info

# Process the text from the current file
def processFile(fname):
    # Set the standard items, including what to ignore
    data, fout = fOpen(fname+'.txt', 'r', fname+'.csv')
    NL, date , time = setStds()
    level, date_line, time_line, source, eventID, taskCat, info = setLines(NL, date, time)
    irrelevant_data = MatchFirst(['-','"']) + restOfLine

    # Define what a record will look like
    record = Group((level + date_line + time_line + source + eventID + taskCat + info))
    record.ignore(irrelevant_data)

    # Find records in the text file
    records = OneOrMore(record).searchString(data)

    # Write the header for the csv file - followed by each line, remove any commas from file.
    fout.write("Level,Date,Time,EventID,TaskCategory,Info\n")
    for rec in records:
        for i in rec:
            #print rec[1], rec[2]
            for index in range(len(i)):
                i[index] = i[index].replace(',','')
            fout.write("%(lvl)s, %(eDate)s, %(eTime)s, %(eID)s, %(tCat)s, %(info)s\n" % i)

    print "Processing Completed"

## The main data extraction function
def main(fname):
    # Open the cvs file
    df = pd.read_csv(fname)  # , index_col=idx)

    ## Fields as follows: 'Level', ' Date', ' Time', ' EventID', ' TaskCategory', ' Info'
    fields = []
    for row in df:
        fields.append(row)

    # Make a data table from the csv - Sort by a field - Analyze using numpy
    dfx = df[fields]
    dfx = dfx.sort(['EventID'], ascending=True)
    dfx.set_index(["EventID", "Info"], inplace=True, drop=False, append=False)
    df_sort_by_info = dfx['Info'].groupby(level=1).agg([np.size])
    df_sort_by_info = df_sort_by_info.sort(['size'], ascending=False)

    # Plot the data
    my_colors = [(0/35.0, x/45.0, x/250.0) for x in range(45,10,-1)]
    df_sort_by_info.ix[1:35].plot(kind='barh',color=my_colors, title="Most Common Deployment Image Servicing and Management Calls")
    plt.show()

    # Write the data to a file for viewing
    ft = open('uOutput.txt', 'w')
    ft.write(str(df_sort_by_info.ix[1:100]))


if __name__ == '__main__':
    # Name the file for dataWork
    fname = 'uTest2'

    # If processed once, comment out
    # processFile(fname)
    main(fname+'.csv')