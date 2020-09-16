import os
import csv
# import logging
from collections import defaultdict
from .treebankfunctions import getattval


underscore = "_"
FlatClass = 0
HeadDiaNew = 1
Class = 2

Headers = {}
Headers[FlatClass] = "FlatClass"
Headers[HeadDiaNew] = "HeadDiaNew"
Headers[Class] = "Class"

comma = ","
# programfolder = r'.'
programfolder = os.path.dirname(os.path.abspath(__file__))
dictfilename = os.path.join(
    programfolder, 'compoundfiles', 'Ncompounds-attempt2.txt')
dictfile = open(dictfilename, 'r', encoding='utf8')

getwordsxpath = ".//node[@pt]"


def getcompounds(syntree):
    results = []
    tlist = syntree.xpath(getwordsxpath)
    for t in tlist:
        w = getattval(t, 'word')
        pt = getattval(t, 'pt')
        if pt == 'n' and iscompound(w):
            results.append(t)
    return results


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))


def iscompound(str):
    if underscore in str:
        result = True
    else:
        result = str in compounds
    return result


mysep = "\\"
myquotechar = ''

compounds = nested_dict(2, str)

# logging.info("Initializing compound module...")
myreader = csv.reader(dictfile, delimiter=mysep)
for row in myreader:
    compounds[row[HeadDiaNew]][FlatClass] = row[FlatClass]
    compounds[row[HeadDiaNew]][Class] = row[Class]


def test():
    while True:
        word = input("Give a word:")
        if iscompound(word):
            print("{} is a compound".format(word))
        else:
            print("{} is  NOT a compound".format(word))
