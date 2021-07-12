import csv
import os
from collections import defaultdict

from sastadev import SDLOGGER, SD_DIR
from sastadev.treebankfunctions import getattval

underscore = "_"
FlatClass = 0
HeadDiaNew = 1
Class = 2

Headers = {}
Headers[FlatClass] = "FlatClass"
Headers[HeadDiaNew] = "HeadDiaNew"
Headers[Class] = "Class"

comma = ","

dictfilename = os.path.join(SD_DIR, "compoundfiles", "Ncompounds-attempt2.txt")
dictfile = open(dictfilename, 'r', encoding='utf8')

getwordsxpath = ".//node[@pt]"


def getcompounds(syntree):
    results = []
    tlist = syntree.xpath(getwordsxpath)
    for t in tlist:
        _ = getattval(t, 'word')
        lemma = getattval(t, 'lemma')
        pt = getattval(t, 'pt')
        if pt == 'n' and iscompound(lemma):
            results.append(t)
    return results


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))


def iscompound(str):
    if underscore in str:
        result = True
    else:
        result = str in compounds
    return result


mysep = "\\"
myquotechar = ''

compounds = nested_dict(2, str)

SDLOGGER.info("Initializing compound module...")
myreader = csv.reader(dictfile, delimiter=mysep)
for row in myreader:
    compounds[row[HeadDiaNew]][FlatClass] = row[FlatClass]
    compounds[row[HeadDiaNew]][Class] = row[Class]
