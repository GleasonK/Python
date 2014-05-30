## File: sBigData.py
## Author: Kevin Gleason
## Date: 5/21/14
## Use: Sample analysis of a big data set. (8619 Rows)

import csv, xlrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyparsing import Word

## If using csv library
def openCSV(file):
    fin = open(file, 'rb')
    return fin, csv.reader(fin)

## Removes punctuation from strings
def replacePunctuation(words):
    from string import punctuation
    for p in punctuation:
        words=words.replace(p,'')

def countryMedals(df, country):
    return df.ix[country]['Total Medals']['sum']

def barColor(dPlot, color):
    #[i.set_color('r') for i in dPlot.get_children() if str(i).__contains__("Rectangle")]
    rects = []
    for i in dPlot.get_children():
        if "Rectangle" in str(i):
            rects.append(i)
    for i in rects[:len(rects)-1]:
        i.set_color(color)

## Based on frequency of field indicated, make color darker - not working, maybe use container.height
def bar_gradient(dPlot):
    #print "len: " + dPlot['Age']
    x=[]
    for i in dPlot.iteritems():
        x.append(i)
    # print "I AM I " + str(x)


def main(file='OlympicAthletes.csv', idx='Country'):
    ## Read the CSV excel file
    # Using csv library
    # fin, data = openCSV('OlympicAthletes.csv')
    # fin.close()

    # Using Pandas read_excel
    # Excel Files take awhile to open
    # reader = pd.read_excel(OlympicAthletes.xlsx, 'OlympicAthletes')

    # Using Pandas read_csv
    df = pd.read_csv(file)  # , index_col=idx)
    fields = []
    for row in df:
        fields.append(row )

    # Sort by countries and set indexes
    dfx = df[fields]
    dfx['Total Medals'] = dfx['Total Medals'].astype(int)
    dfx = dfx.sort(['Country'], ascending=True)
    dfx.set_index(['Country', 'Total Medals'], inplace=True, drop=False, append=False)

    # Group by field
    dfg = df[['Country', 'Total Medals']].groupby('Country').agg([np.mean, np.std, np.sum, np.size])
    us_sum = dfg.ix['United States']['Total Medals']['sum']
    ch_sum = countryMedals(dfg, 'China')
    gb_sum = countryMedals(dfg, 'Great Britain')
    print "Total Medals by Country"
    print "US: " + str(int(us_sum)), "China: " + str(int(ch_sum)), "GB: " + str(int(gb_sum))

    # Group by index
    dfgi = dfx['Total Medals'].groupby(level=[0]).agg([np.mean, np.sum])

    # Sort by Medals earned per Country
    df_sort_by_country = dfgi.sort(['sum'], ascending=True)
    df_sort_by_age = df[['Age', 'Total Medals']].groupby('Age').agg([np.sum])

    # Define Colors
    bar_gradient(df_sort_by_age)
    my_colors = [(x/42.0, x/43.0, 0.7) for x in range(len(df_sort_by_age))]

    # Plot the data
    aPlot = df_sort_by_age.ix[15:61].plot(kind='bar', color=my_colors, title='Olympic Medals by Age since 2000')
    aPlot.set_ylabel('Medals (#)')
    aPlot.tick_params(labelsize=9)
    for bar in aPlot.containers:
        plt.setp(bar, width=0.7)
    # plt.savefig('AgePlot.png')

    cPlot = df_sort_by_country.ix[80:].plot(kind='barh', color = 'r', title='Olympic Medals by Country since 2000')
    cPlot.set_ylabel('Medals(#)')
    cPlot.tick_params(labelsize=9)
    for bar in cPlot.containers:
        plt.setp(bar, height=0.7)

    plt.legend(loc='best')
    # plt.savefig('CountryPlot.png')
    plt.show()

    print "Read File - " + file


if __name__ == '__main__':
    main()
