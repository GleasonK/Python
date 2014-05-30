## File: introToNatural.py
## Author: Kevin Gleason
## Date: 5/27/14
## Use: Introduction to the capabilities of the Natural Language Toolkit

from __future__ import division  # floating division
from nltk.book import *
# import time, multiprocessing

# Print all words ending in ing
def endsWithLetters(fname, letters="ing"):
    for line in open(fname, 'r'):
        for word in line.split():
            if word.endswith(letters):
                print word

# Main function
def lexicalFunctions1(concordance, common_context, lex_plot_words, text=text1):
      # Assumes all books were loaded properly
    # Find sentences with concordance word
    print "\nFinding occurrences of '" + concordance + "' in", text.name
    text.concordance(concordance)

    # Find similar words in range of context
    print "\nFinding similar words to '" + concordance + "' in", text.name
    text.similar(concordance)

    # Find common context of two words
    print "\nFinding common context of '"+ "', '".join(i for i in common_context) + "' in", text.name
    text.common_contexts(common_context)

    print "\nGenerating random set of words from", text.name
    text.generate()

    # Create lexical dispersion graph of words
    print "\nCreating lexical dispersion graph of '"+ "', '".join([i for i in lex_plot_words]) + "' in", text.name
    text.dispersion_plot(lex_plot_words)
    print "Process complete."

# Vocabulary functions
def vocabFunctions(wordInText, text=text1):
    # Number of words in text
    text_len = len(text)
    print "\nNumber of tokens in", text.name + ":"
    print text_len

    # Number of unique tokens and vocab split up
    sortedSetText = sorted(set(text))
    sortedSetText_len = len(sortedSetText)
    print "\nNumber of unique tokens in", text.name + ":"
    print sortedSetText_len

    # Find word richness
    print "\nWord richness of", text.name + ":"
    print text_len/sortedSetText_len

    # Find percent occurrence of a word
    countOfWord = text.count(wordInText)
    print "\nCount | percent of word '" + wordInText + "' in", text.name + ":"
    print countOfWord, "|", 100 * countOfWord/text_len

# Calculate word frequencies
def wordFrequency(wordInText, longWordLen, commonFreq, text=text1):
    # List the most frequent words
    fdist = FreqDist(text)
    mostFreq = fdist.keys()
    print "\nMost frequent words in text"
    print mostFreq[:50]

    # Plot the most frequent words
    print "\nPlotting the most frequent words..."
    fdist.plot(50, cumulative=True)
    print "Process complete"

    # Find long words only
    setOfText = set(text)
    print "\nFinding words of at least length", str(longWordLen)
    long_words = [w for w in setOfText if len(w) > longWordLen]
    print sorted(long_words)
    # print "Frequently occurring long words: "
    # common_long_words = [w for w in long_words if fdist[w] > commonFreq]



if __name__=='__main__':
    # Load all books with from nltk.books import *
    lexicalFunctions1(concordance="whale", common_context=["whale", "monster"],\
                     lex_plot_words=["whale","ship","waves", "harpoon", "kill"],\
                     text=text1)
    vocabFunctions("love", text=text1)
    wordFrequency(wordInText="whale", longWordLen=15, commonFreq=0, text=text1)