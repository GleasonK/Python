from pyparsing import *
import urllib


def StripHTML(fin):
    # Remove Definition
    removeText = replaceWith(" ")
    removeWithSpace = replaceWith(" ")

    # Script tag
    scriptOpen,scriptClose = makeHTMLTags("script")
    scriptBody = scriptOpen + SkipTo(scriptClose) + scriptClose
    scriptBody.setParseAction(removeText)

    # Style tag
    styleOpen, styleClose = makeHTMLTags("style")
    styleBody = styleOpen + SkipTo(styleClose) + styleClose
    styleBody.setParseAction(removeText)

    # HTML tags
    anyTag,anyClose = makeHTMLTags(Word(alphas,alphanums+":_"))
    anyTag.setParseAction(removeText)
    anyClose.setParseAction(removeText)
    htmlComment.setParseAction(removeText)
    commonHTMLEntity.setParseAction(replaceHTMLEntity)


    # get some HTML
    HTMLfile = open(fin, 'r').read()

    # first pass, strip out tags and translate entities
    firstPass = (htmlComment | scriptBody | styleBody | commonHTMLEntity |
                anyTag | anyClose ).transformString(HTMLfile)
    # first pass leaves many blank lines, collapse these down
    repeatedNewlines = LineEnd() + OneOrMore(LineEnd())
    repeatedNewlines.setParseAction(replaceWith("\n\n"))
    secondPass = repeatedNewlines.transformString(firstPass)
    # print secondPass
    return str(secondPass)

if __name__=='__main__':
    fin = 'Data/test.txt'
    l = StripHTML(fin)